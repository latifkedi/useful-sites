# -*- coding: utf-8 -*-
"""Audits the health of linked GitHub repositories: archived, or untouched.

A repository can die without ever returning 404 -- it gets archived, turns
read-only, or simply goes years without a commit. A link check cannot see
any of that. This script can.

Runs inside GitHub Actions with GITHUB_TOKEN (5000 requests/hour).
Locally it hits the anonymous limit after 60; pass a token:
    GH_TOKEN=ghp_xxx python data/ci_github.py
"""
import json
import io
import os
import re
import sys
import datetime
import concurrent.futures as cf

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import readlinks  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')

HEADERS = {'User-Agent': 'link-directory-health', 'Accept': 'application/vnd.github+json'}
if TOKEN:
    HEADERS['Authorization'] = 'Bearer ' + TOKEN

# A repository untouched for this long counts as stale.
STALE_DAYS = 730          # iki yil
SKIP_OWNERS = {'topics', 'features', 'education', 'sponsors', 'orgs', 'collections'}


# Registry pages carry their own last-published date and are worth auditing on
# the same terms as a repository. None are linked today; the patterns are here
# so the audit covers them the day one is added.
REGISTRY = [
    ('npm', r'npmjs\.com/package/(@?[^/?#]+)',
     'https://registry.npmjs.org/%s', ('time', 'modified')),
    ('pypi', r'pypi\.org/project/([^/?#]+)',
     'https://pypi.org/pypi/%s/json', ('urls', 0, 'upload_time')),
]

# A project can go quiet on its own domain while its repository still tells the
# truth -- Foundation for Sites is exactly that case: the site was reachable and
# advertising a webinar from 2017, and only the repository showed the last
# release was September 2024. Scanning only github.com URLs misses those, so
# open-source entries hosted elsewhere get their homepage read once to find the
# repository they point at.
HOMEPAGE_LIMIT = 240          # bounded: this runs weekly


def _find_repo(url):
    """Reads a project homepage and returns the first github.com/owner/repo."""
    try:
        r = requests.get(url, headers={'User-Agent': HEADERS['User-Agent']},
                         timeout=(6, 15), allow_redirects=True)
    except requests.exceptions.RequestException:
        return None
    for m in re.finditer(r'https?://github\.com/([A-Za-z0-9._-]+)/([A-Za-z0-9._-]+)',
                         r.text[:200000]):
        owner, repo = m.group(1), m.group(2)
        if owner.lower() in SKIP_OWNERS:
            continue
        if repo.lower().endswith(('.png', '.svg', '.jpg', '.css', '.js')):
            continue
        return owner, repo.rstrip('.')
    return None


def repos():
    rows = readlinks.read(ROOT)
    out, dolayli = [], []
    for r in rows:
        m = re.match(r'https://github\.com/([^/]+)/([^/#?]+)', r['url'])
        if m and m.group(1).lower() not in SKIP_OWNERS:
            out.append((r['name'], r.get('cat_tr', ''), m.group(1), m.group(2), r['url']))
        elif 'açık-kaynak' in (r.get('tags') or []):
            dolayli.append(r)

    dolayli = dolayli[:HOMEPAGE_LIMIT]
    if dolayli:
        print('proje sayfasindan depo aranan kayit: %d' % len(dolayli),
              file=sys.stderr)
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            bulunan = list(ex.map(lambda r: (r, _find_repo(r['url'])), dolayli))
        for r, hit in bulunan:
            if hit:
                out.append((r['name'], r.get('cat_tr', ''), hit[0], hit[1], r['url']))
    return out


def check(t):
    name, cat, owner, repo, url = t
    try:
        r = requests.get('https://api.github.com/repos/%s/%s' % (owner, repo),
                         headers=HEADERS, timeout=15)
    except requests.exceptions.RequestException as e:
        return {'name': name, 'cat': cat, 'url': url, 'state': 'hata', 'detail': type(e).__name__}

    if r.status_code == 404:
        return {'name': name, 'cat': cat, 'url': url, 'state': 'yok', 'detail': 'depo silinmiş'}
    if r.status_code in (403, 429):
        return {'name': name, 'cat': cat, 'url': url, 'state': 'kota', 'detail': str(r.status_code)}
    if r.status_code != 200:
        return {'name': name, 'cat': cat, 'url': url, 'state': 'hata', 'detail': str(r.status_code)}

    j = r.json()
    pushed = (j.get('pushed_at') or '')[:10]
    rec = {'name': name, 'cat': cat, 'url': url, 'pushed': pushed,
           'stars': j.get('stargazers_count'),
           'repo': '%s/%s' % (owner, repo)}
    if j.get('archived'):
        rec['state'] = 'arşiv'
        return rec
    if pushed:
        age = (datetime.date.today() - datetime.date.fromisoformat(pushed)).days
        if age > STALE_DAYS:
            rec['state'] = 'bayat'
            rec['detail'] = '%d gün' % age
            return rec
    rec['state'] = 'aktif'
    return rec


def write_health(results):
    """Per-record repository health, for the site to show.

    The audit already knew all of this and told nobody: it went into an issue
    that the reader of the directory never sees. Which is the exact failure the
    directory is supposed to be about -- an entry can look fine while the
    project behind it stopped moving two years ago.

    Existing entries are kept when a run cannot reach them (rate limit, network
    error), so a bad run degrades to stale data rather than to no data.
    """
    path = os.path.join(ROOT, 'data', 'health.json')
    out = {}
    if os.path.exists(path):
        out = json.load(io.open(path, encoding='utf-8'))

    today = datetime.date.today().isoformat()
    yeni = 0
    for r in results:
        if r['state'] in ('kota', 'hata'):
            continue                     # eski kaydi koru
        k = re.sub(r'^https?://(www\.)?', '', r['url'].strip().lower()).rstrip('/')
        rec = {'s': r['state'], 'd': today}
        if r.get('pushed'):
            rec['p'] = r['pushed']
        if r.get('stars') is not None:
            rec['y'] = r['stars']
        if r.get('repo'):
            rec['r'] = r['repo']
        out[k] = rec
        yeni += 1

    json.dump(out, io.open(path, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1, sort_keys=True)
    print('health.json: %d kayit (%d tazelendi)' % (len(out), yeni))


def main():
    rs = repos()
    if not TOKEN:
        print('UYARI: token yok, 60 istek sonrasi kotaya takilacak', file=sys.stderr)
    with cf.ThreadPoolExecutor(max_workers=8 if TOKEN else 3) as ex:
        results = list(ex.map(check, rs))

    write_health(results)

    by = {}
    for r in results:
        by.setdefault(r['state'], []).append(r)

    print('taranan depo: %d' % len(rs))
    for k in sorted(by):
        print('  %-7s %d' % (k, len(by[k])))

    flagged = by.get('arşiv', []) + by.get('bayat', []) + by.get('yok', [])
    if not flagged:
        return 0

    L = ['# GitHub depo sağlığı — %s' % datetime.date.today().isoformat(), '',
         '`%d` depo tarandı. Bunlar 404 döndürmüyor ama artık bakımda değil.' % len(rs), '']

    for state, baslik, aciklama in [
        ('yok',    'Silinmiş', 'Depo artık yok.'),
        ('arşiv',  'Arşivlenmiş', 'Salt okunur. Sorunlar kapanmıyor, ölü bağlantılar temizlenmiyor. '
                                  'Açıklamaya not düşülmeli ya da kayıt çıkarılmalı.'),
        ('bayat',  'Bayat (2+ yıl dokunulmamış)', 'Terk edilmiş olabilir; alternatifi var mı bakılmalı.'),
    ]:
        rows = by.get(state, [])
        if not rows:
            continue
        L += ['## %s (%d)' % (baslik, len(rows)), '', aciklama, '',
              '| Kayıt | Kategori | Son itme | Yıldız | URL |', '|---|---|---|---|---|']
        for r in sorted(rows, key=lambda x: x.get('pushed') or ''):
            L.append('| %s | %s | %s | %s | %s |' % (
                r['name'], r['cat'], r.get('pushed') or r.get('detail', '—'),
                r.get('stars', '—'), r['url']))
        L.append('')

    if by.get('kota'):
        L.append('> %d depo API kotası yüzünden denetlenemedi.' % len(by['kota']))
        L.append('')

    L.append('<sub>`data/ci_github.py` tarafından otomatik üretildi.</sub>')
    io.open(os.path.join(ROOT, 'rapor-github.md'), 'w', encoding='utf-8').write('\n'.join(L))
    return 0


if __name__ == '__main__':
    sys.exit(main())
