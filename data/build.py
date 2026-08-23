# -*- coding: utf-8 -*-
"""Merges the curator notes with fetched metadata into the site data.

Writes:
  ../links.js      records + Turkish descriptions   (loaded first)
  ../links.en.js   English descriptions             (on language switch)
  plus feed.xml, sitemap.xml, robots.txt and the static pages under ../k/

The two languages are split because the descriptions are most of the
payload; shipping one language makes the first load noticeably lighter.
"""
import json
import io
import re
import os
import sys
import html
import collections

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from notes import NOTES, CATS          # noqa: E402
from tags import normalise, LABELS    # noqa: E402
from picks import PICKS               # noqa: E402
from sources import SOURCES, DEFAULT  # noqa: E402
from intros import INTROS             # noqa: E402
from recat import BY_NAME            # noqa: E402
import emit                           # noqa: E402

BOOKMARKS = r'C:\Users\Cebrail\Documents\code\duzen\bookmarks_duzenli.html'
def _load(name):
    p = os.path.join(D, name)
    return json.load(io.open(p, encoding='utf-8')) if os.path.exists(p) else []


# Three metadata sources: the original bookmark archive, the external
# list, and a later export. Anything without a note is dropped below.
meta = _load('meta.json') + _load('ext_meta.json')
def _base(k):
    return re.split(r'[?#]', k)[0].rstrip('/')


# Both the full and the query-stripped form of every known URL. Without
# both, 'site.com/' and 'site.com/?utm=x' count as two separate records.
_have = set()
for _m in meta:
    _k = re.sub(r'^https?://(www\.)?', '', _m['url'].lower()).rstrip('/')
    _have.add(_k)
    _have.add(_base(_k))

# For notes that appear in no metadata file (newly added ones), synthesise
# a metadata record out of the note's own URL.
for _k, _n in sorted(NOTES.items()):
    if _n.get('url') and _k not in _have and _base(_k) not in _have:
        meta.append({'url': _n['url'], 'path': '', 'title': _n['name']})
        _have.add(_k)
        _have.add(_base(_k))


def key(u):
    u = re.sub(r'^https?://', '', u.strip().lower())
    u = re.sub(r'^www\.', '', u)
    return u.rstrip('/')


# ------------------------------------------------------------------ added dates
# The ADD_DATE field in the bookmark export says when a link was collected.
# It was extracted once and frozen into added.json, so the build no longer
# depends on a path on one particular machine and produces the same output
# in CI. Use refresh_added() when the bookmark file is at hand.
ADDED = {}
_ap = os.path.join(D, 'added.json')
if os.path.exists(_ap):
    ADDED = dict((k, int(v)) for k, v in
                 json.load(io.open(_ap, encoding='utf-8')).items())


def refresh_added():
    if not os.path.exists(BOOKMARKS):
        print('bookmark file not found; added.json left as is')
        return
    for ln in io.open(BOOKMARKS, encoding='utf-8'):
        m = re.search(r'<DT><A HREF="([^"]*)"[^>]*ADD_DATE="(\d+)"', ln.strip())
        if m:
            k = key(html.unescape(m.group(1)))
            ts = int(m.group(2))
            if 946684800 < ts < 2200000000:        # a sane 2000-2039 range
                ADDED[k] = max(ADDED.get(k, 0), ts)
    json.dump(ADDED, io.open(_ap, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0, sort_keys=True)
    print('added.json refreshed:', len(ADDED))

PATHMAP = [
    ('Bilişim/Yol Haritaları', 'ogrenme'), ('Bilişim/Eğitim Platformları', 'ogrenme'),
    ('Bilişim/Sertifika & Sınav', 'ogrenme'), ('Bilişim/Pratik & Egzersiz', 'pratik'),
    ('Bilişim/Programlama Dilleri', 'diller'), ('Bilişim/Web & Frontend', 'web'),
    ('Bilişim/Backend & Framework', 'backend'), ('Bilişim/Sistem Tasarımı & API', 'backend'),
    ('Bilişim/Mobil & Masaüstü', 'mobil'), ('Bilişim/Veritabanı', 'veritabani'),
    ('Bilişim/DevOps & Altyapı', 'devops'), ('Bilişim/Ağ & Linux', 'ag'),
    ('Bilişim/IT Destek & Sistem', 'ag'), ('Bilişim/Siber Güvenlik', 'guvenlik'),
    ('Bilişim/Veri Bilimi & ML', 'veri'), ('Bilişim/Yapay Zeka/AI Altyapı', 'yz_altyapi'),
    ('Bilişim/Yapay Zeka/API & Geliştirme', 'yz_altyapi'),
    ('Bilişim/Yapay Zeka/Agent & Claude', 'yz_altyapi'),
    ('Bilişim/Yapay Zeka/AI Araçları', 'yz_arac'),
    ('Bilişim/Yapay Zeka/Üretken Araçlar', 'yz_arac'),
    ('Bilişim/Yapay Zeka/Sohbet', 'yz_model'), ('Bilişim/Yapay Zeka/Model Arşivi', 'yz_model'),
    ('Bilişim/Yapay Zeka', 'yz_model'),
    ('Bilişim/Donanım, CAD & Robotik/Akıllı Gözlük', 'gozluk'),
    ('Bilişim/Donanım, CAD & Robotik', 'donanim'), ('Bilişim/Kuantum Bilişim', 'kuantum'),
    ('Bilişim/Araçlar', 'araclar'), ('Bilişim/Referans', 'referans'),
    ('Bilişim/GitHub Koleksiyonları', 'referans'), ('Bilim & Düşünce', 'bilim'),
]


def cat_of(path):
    for pre, c in PATHMAP:
        if path.startswith(pre):
            return c
    return 'araclar'


# A second URL form of the same source - no reason to list it twice.
SKIP = {
    'servicedesk-simulator.com/#ticket/inc0012871/ad',
    'learn-anything.xyz/c-libraries',
}

# Per-record verification: ci_check.py refreshes verified.json weekly.
VERIFIED = {}
_vp = os.path.join(D, 'verified.json')
if os.path.exists(_vp):
    VERIFIED = json.load(io.open(_vp, encoding='utf-8'))

# Repository health: ci_github.py refreshes health.json weekly. A link can
# answer perfectly while the project behind it has been archived or untouched
# for years -- the audit knew that and only told an issue. Now the record does.
HEALTH = {}
_hp = os.path.join(D, 'health.json')
if os.path.exists(_hp):
    HEALTH = json.load(io.open(_hp, encoding='utf-8'))

out, missing, seen = [], [], set()
for m in meta:
    k = key(m['url'])
    if k in seen or k in SKIP:
        continue
    seen.add(k)
    n = NOTES.get(k) or NOTES.get(re.split(r'[?#]', k)[0].rstrip('/'))
    if not n:
        missing.append((k, m.get('title', '')[:60]))
        continue
    rec = {
        'url': m['url'],
        'name': n['name'],
        # BY_NAME wins: it is the reclassification pass, see data/recat.py
        'cat': BY_NAME.get(n['name']) or n.get('cat') or cat_of(m['path']),
        'tags': normalise(n.get('tags', [])),
        'tr': n['tr'],
        'en': n['en'],
        'src': n.get('src') or DEFAULT,
    }
    ts = ADDED.get(k) or ADDED.get(re.split(r'[?#]', k)[0].rstrip('/'))
    if ts:
        rec['added'] = ts
    if m['url'] in PICKS:
        rec['pick'] = 1
    h = HEALTH.get(k) or HEALTH.get(re.split(r'[?#]', k)[0].rstrip('/'))
    if h and h.get('s') in ('arşiv', 'bayat', 'yok'):
        rec['hs'] = h['s']
        if h.get('p'):
            rec['hp'] = h['p']

    v = VERIFIED.get(k) or VERIFIED.get(re.split(r'[?#]', k)[0].rstrip('/'))
    if v:
        rec['ver'] = v['d']
        if v['s'] == 'engel':
            rec['verw'] = 1          # bot-blocked - needs a manual look
        elif v['s'] == 'olu':
            rec['dead'] = 1          # no response last scan - point at archive
    out.append(rec)

# Records that never appeared in the bookmark archive have no ADD_DATE, so they
# need a stand-in. One flat value would flatten "newest first" into noise, so
# each intake gets the date it actually arrived.
FALLBACK = 1787000000          # AI tools added while compiling the directory
SRC_ADDED = {
    'bwapsv': 1787000000,      # first external import
    'cdcruz': 1787345600,      # 21 Aug 2026 intake
    'awesome-uw': 1787345600,
    'invesp': 1787345600,
}
for r in out:
    if 'added' not in r:
        r['added'] = SRC_ADDED.get(r['src'], FALLBACK)

order = [c[0] for c in CATS]
out.sort(key=lambda r: (order.index(r['cat']) if r['cat'] in order else 99,
                        r['name'].lower()))

cmap = {c[0]: (c[1], c[2]) for c in CATS}

core, en = [], []
for r in out:
    ct, ce = cmap.get(r['cat'], (r['cat'], r['cat']))
    core.append({
        'url': r['url'], 'name': r['name'], 'cat': r['cat'],
        'cat_tr': ct, 'cat_en': ce, 'tags': r['tags'],
        'tr': r['tr'], 'added': r['added'], 'src': r['src'],
    })
    if r.get('ver'):
        core[-1]['ver'] = r['ver']
    if r.get('verw'):
        core[-1]['verw'] = 1
    if r.get('dead'):
        core[-1]['dead'] = 1
    if r.get('hs'):
        core[-1]['hs'] = r['hs']
        if r.get('hp'):
            core[-1]['hp'] = r['hp']
    if r.get('pick'):
        core[-1]['pick'] = 1
    en.append(r['en'])

# ------------------------------------------------------------------ related
# The three records in the same category with the most tag overlap. The
# point is a "if this was useful, look at that" thread; directories tend
# to leave neighbouring entries invisible to each other.
by_cat = {}
for i, r in enumerate(core):
    by_cat.setdefault(r['cat'], []).append(i)

# Two shared tags is the bar for a good suggestion, but applying it flatly left
# 85 records with no neighbours at all -- usually the ones carrying few tags,
# which are exactly the ones a reader is least able to place. Those fall back to
# a single shared tag rather than being left orphaned.
for i, r in enumerate(core):
    ts = set(r['tags'])
    if not ts:
        continue
    for esik in (2, 1):
        puan = []
        for j in by_cat[r['cat']]:
            if j == i:
                continue
            ort = len(ts & set(core[j]['tags']))
            if ort >= esik:
                puan.append((ort, -abs(j - i), j))
        if puan:
            break
    puan.sort(reverse=True)
    rel = [core[j]['name'] for _, _, j in puan[:3]]
    if rel:
        r['rel'] = rel

J = dict(ensure_ascii=False, separators=(',', ':'))
io.open(os.path.join(D, '..', 'links.js'), 'w', encoding='utf-8').write(
    '/* Otomatik uretildi - data/build.py */\n'
    'window.SOURCES=' + json.dumps(SOURCES, **J) + ';\n'
    'window.TAGLABELS=' + json.dumps(LABELS, **J) + ';\n'
    'window.INTROS=' + json.dumps(INTROS, **J) + ';\n'
    'window.LINKS=' + json.dumps(core, **J) + ';\n')
io.open(os.path.join(D, '..', 'links.en.js'), 'w', encoding='utf-8').write(
    '/* Otomatik uretildi - data/build.py */\nwindow.LINKS_EN=' + json.dumps(en, **J) + ';\n')

# The text version, for crawlers and for visitors without JavaScript:
# category pages, sitemap, robots and the Atom feed. The app is untouched.
_pages = emit.write_all(core, CATS, INTROS, LABELS, os.path.join(D, '..'), en)

# ------------------------------------------------------------------ cache stamp
# The address of links.js never changes, so after an update a browser can serve
# the old data file while index.html is fresh: new categories simply do not
# appear, and nothing says why. Writing a digest of the content into the query
# makes the address change whenever the content does.
def _stamp():
    import hashlib
    ix = os.path.join(D, '..', 'index.html')
    src = io.open(ix, encoding='utf-8').read()
    for name in ('links.js', 'links.en.js'):
        h = hashlib.sha1(io.open(os.path.join(D, '..', name), 'rb').read()).hexdigest()[:8]
        pat = re.compile(r'(["\'])' + re.escape(name) + r'(?:\?v=[0-9a-f]+)?\1')
        src = pat.sub(lambda m, n=name, d=h: m.group(1) + n + '?v=' + d + m.group(1), src)
    io.open(ix, 'w', encoding='utf-8', newline='').write(src)


_stamp()

tc = collections.Counter(t for r in out for t in r['tags'])
print('records        :', len(out))
print('distinct tags  :', len(tc))
print('untagged       :', sum(1 for r in out if not r['tags']))
print('without a note :', len(missing))
print('real dates     :', sum(1 for r in out if r['added'] != FALLBACK))
print('start-here     :', sum(1 for r in out if r.get('pick')), '/', len(PICKS))
_sc = collections.Counter(r['src'] for r in out)
print('sources        :', dict(_sc))
print('verified       :', sum(1 for r in core if r.get('ver')))
print('with related   :', sum(1 for r in core if r.get('rel')))
print('repo flagged   :', sum(1 for r in core if r.get('hs')))
print('static pages   :', len(_pages), '+ sitemap, robots, feed')
if missing:
    io.open(os.path.join(D, 'missing.txt'), 'w', encoding='utf-8').write(
        '\n'.join('%s\t%s' % t for t in missing))
