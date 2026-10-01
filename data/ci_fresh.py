# -*- coding: utf-8 -*-
"""Audits descriptions against what the linked page says today.

    python data/ci_fresh.py            # everything
    python data/ci_fresh.py bwapsv     # one source only

A link check answers "does it respond". This answers a different question:
"is it still the thing we described". Those come apart in three ways, and all
three have already happened in this directory:

  taken over  The domain resolves and serves somebody else entirely.
              branition.com became a gambling site, issuehub.io a game-server
              advertisement, odeo.com an Indonesian casino. Every one of them
              returns HTTP 200 and passes a link check without complaint.

  renamed     The product still exists under another name, or pivoted. The
              recorded name no longer appears anywhere on the page.

  dated       The description makes a claim tied to a year that has since
              passed -- "the 2023 licensing fight", "as of 2024".

None of this is auto-corrected. The output is a review list, because deciding
whether a description has gone stale needs a person.
"""
import io
import os
import re
import sys
import datetime
import concurrent.futures as cf

import requests
import urllib3

urllib3.disable_warnings()

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(D)
sys.path.insert(0, D)
import readlinks                        # noqa: E402

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
HEADERS = {'User-Agent': UA, 'Accept-Language': 'tr,en;q=0.9'}

# Wording that only appears on a page nobody is running any more.


# TLS dogrulamasi aciktir. Ilk surumde her istek verify=False ile gidiyordu --
# eski sertifikali birkac siteyi kurtarmak icin, ama bedeli buydu: aradaki biri
# yaniti degistirebilir ve tarama "canli" ya da "temiz" diye rapor eder. Ozellikle
# ci_fresh.py icerige bakip karar verdigi icin bu sessiz bir yanlis kaynagi.
# Simdi once dogrulanarak deneniyor; yalnizca sertifika hatasinda, o kayda ozel
# olarak dogrulamasiz bir kez daha bakiliyor.
def get(url, **kw):
    kw.setdefault('headers', HEADERS)
    kw.setdefault('timeout', (6, 15))
    kw.setdefault('allow_redirects', True)
    try:
        return requests.get(url, verify=True, **kw)
    except requests.exceptions.SSLError:
        return requests.get(url, verify=False, **kw)


# Deliberately narrow. The first attempt matched "under construction" anywhere
# in the body and flagged Stroustrup's C++11 FAQ, learn-c.org and njal.la --
# all three merely contain the phrase somewhere. A parked page announces itself
# in the title or in its first screenful, so that is where this looks.
PARKED = re.compile(
    r'(domain (is |may be )?for sale|buy this domain|this domain is available|'
    r'parked (free )?(at|by)|sedoparking|afternic|hugedomains|dan\.com|'
    r'inquire about this domain|domain name is for sale|'
    r'default web site page|apache2 (ubuntu|debian) default|welcome to nginx)', re.I)
PARKED_TITLE = re.compile(
    r'(for sale|under construction|coming soon|site en construction|'
    r'welcome to nginx|domain (default|parking))', re.I)

# Gambling and adult-redirect takeovers share a small vocabulary.
HIJACK = re.compile(
    r'(situs|togel|slot gacor|bandar|judi|casino online|prediksi|'
    r'link alternatif|toto slot|rtp live)', re.I)

THIS_YEAR = datetime.date.today().year
YEAR = re.compile(r'\b(19[89]\d|20[0-4]\d)\b')


def words(t):
    return set(re.findall(r'[a-z0-9]+', t.lower()))


def fetch(d):
    out = {'name': d['name'], 'url': d['url'], 'src': d['src'],
           'cat': d.get('cat_tr', ''), 'flags': [], 'note': ''}
    try:
        r = get(d['url'], timeout=(6, 18))
    except requests.exceptions.RequestException as e:
        out['flags'].append('ulasilamadi')
        out['note'] = type(e).__name__
        return out

    if r.status_code >= 400:
        # ci_check.py already reports these; not this script's job.
        return out

    body = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', r.text[:200000],
                  flags=re.S | re.I)
    text = re.sub(r'<[^>]+>', ' ', body)
    text = re.sub(r'\s+', ' ', text)

    m = re.search(r'<title[^>]*>(.*?)</title>', r.text[:60000], re.S | re.I)
    title = re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''
    out['title'] = title[:90]

    if PARKED.search(text[:1500]) or PARKED_TITLE.search(title):
        out['flags'].append('park')
    if HIJACK.search(title) or HIJACK.search(text[:3000]):
        out['flags'].append('ele-gecmis')

    # Is the recorded name still anywhere on the page? Only asked where the
    # answer means something. A Turkish descriptive title ("20 Dakikada Tum Ag
    # Kavramlari") will never appear on an English page, and a JavaScript-only
    # shell returns almost no text -- the first run flagged 107 records, nearly
    # all of them for one of those two reasons.
    ad = {w for w in words(d['name']) if len(w) > 2}
    urun_adi = (len(d['name'].split()) <= 3
                and not re.search(r'[şğıİöçüŞĞÖÇÜ]', d['name']))
    if (ad and urun_adi and len(text) > 2500
            and not (ad & words(title))
            and not (ad & words(text[:8000]))):
        out['flags'].append('ad-yok')

    # A claim pinned to a year that has since passed.
    yil = [int(y) for y in YEAR.findall(d['tr'])]
    eski = [y for y in yil if y <= THIS_YEAR - 2]
    if eski:
        out['flags'].append('tarihli')
        out['note'] = ', '.join(str(y) for y in sorted(set(eski)))

    return out


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    rows = readlinks.read(ROOT)
    if only:
        rows = [d for d in rows if d['src'] == only]
    print('taranan: %d kayit%s' % (len(rows), (' (%s)' % only) if only else ''),
          file=sys.stderr)

    with cf.ThreadPoolExecutor(max_workers=14) as ex:
        res = list(ex.map(fetch, rows))

    flagged = [r for r in res if r['flags']]
    by = {}
    for r in flagged:
        for f in r['flags']:
            by.setdefault(f, []).append(r)

    for k in ('ele-gecmis', 'park', 'ad-yok', 'tarihli', 'ulasilamadi'):
        print('%-12s %d' % (k, len(by.get(k, []))))

    if not flagged:
        return 0

    BASLIK = {
        'ele-gecmis': ('Ele geçirilmiş olabilir',
                       'Sayfa açılıyor ama içerik kumar/spam kalıplarıyla eşleşti. '
                       'Elle bakılmalı; doğruysa kayıt çıkarılmalı.'),
        'park': ('Park edilmiş ya da boş',
                 'Alan adı satılık, varsayılan sunucu sayfası ya da yapım aşamasında.'),
        'ad-yok': ('Kaydın adı sayfada geçmiyor',
                   'Ürün yeniden adlandırılmış, yön değiştirmiş ya da alan adı el '
                   'değiştirmiş olabilir. Yanlış pozitif oranı en yüksek başlık bu.'),
        'tarihli': ('Açıklamada eskimiş yıl',
                    'Açıklama iki yıldan eski bir yıla atıf yapıyor; hâlâ doğru mu diye bakılmalı.'),
        'ulasilamadi': ('Yanıt vermedi',
                        'Bu tarama sırasında bağlantı kurulamadı.'),
    }

    L = ['# Açıklama tazeliği — %s' % datetime.date.today().isoformat(), '',
         '`%d` kayıt tarandı. Aşağıdakiler ölü değil; **anlattığımız şey olmaktan '
         'çıkmış olabilir.**' % len(rows), '']
    for k in ('ele-gecmis', 'park', 'ad-yok', 'tarihli', 'ulasilamadi'):
        grup = by.get(k)
        if not grup:
            continue
        bas, aciklama = BASLIK[k]
        L += ['## %s (%d)' % (bas, len(grup)), '', aciklama, '',
              '| Kayıt | Kaynak | Sayfa başlığı / not | URL |', '|---|---|---|---|']
        for r in sorted(grup, key=lambda x: x['name'].lower()):
            L.append('| %s | %s | %s | %s |'
                     % (r['name'], r['src'],
                        (r.get('title') or r.get('note') or '')[:70], r['url']))
        L.append('')

    L.append('<sub>Generated by `data/ci_fresh.py`.</sub>')
    io.open(os.path.join(ROOT, 'rapor-tazelik.md'), 'w',
            encoding='utf-8').write('\n'.join(L))
    print('rapor-tazelik.md yazildi: %d kayit isaretli' % len(flagged))
    return 0


if __name__ == '__main__':
    sys.exit(main())
