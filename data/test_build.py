# -*- coding: utf-8 -*-
"""Smoke test for the build output.

    python data/test_build.py

A broken part file does not raise: `add()` simply never runs for the entries
below the error, the build reports a smaller number, and nobody notices until
a category looks thin. Nothing asserted that the count had not collapsed.

These checks are deliberately blunt. They do not judge whether a description
is good; they catch the failures that are silent -- records vanishing, a
category losing its introduction, a pick pointing at a URL that no longer
exists, the two language files falling out of step.

MIN_RECORDS is a floor, not the current count. Raise it on purpose when the
directory grows; never lower it to make a red build green.
"""
import collections
import io
import json
import os
import re
import sys

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(D)
sys.path.insert(0, D)

import readlinks                        # noqa: E402
from notes import CATS, GROUPS, FIELD_NOTES, load_records  # noqa: E402
from intros import INTROS               # noqa: E402
from picks import PICKS                 # noqa: E402
from sources import SOURCES             # noqa: E402
from tags import CANON, LABELS, FACETS  # noqa: E402
from emit import SITE as EMIT_SITE, HOME_TX, esc as esc_html  # noqa: E402

MIN_RECORDS = 1850
MIN_CATEGORIES = 43

MIN_DESC = 30
DIFF_FLOOR = 0.72
# Comparative language in either description counts as saying how it differs.
DIFF_TR = re.compile(r'(farkı|farklı|yerine|aksine|oysa|karşın|kıyasla|göre daha|değil|benzer|ayrıl|'
                     r'tersine|alternatif|daha (hafif|hızlı|basit|sade|derin|kapsamlı|az|çok|yeni|eski))', re.I)
DIFF_EN = re.compile(r'(unlike|instead of|rather than|whereas|compared|alternative|differs|than |, not |'
                     r'not a |lighter|heavier)', re.I)
TRACKING = re.compile(r'[?&](utm_[a-z]+|fbclid|gclid|ab_channel|si|ref|ref_src|mc_[ce]id|igshid)=', re.I)

fails = []


def check(ok, msg):
    print(('  ok   ' if ok else '  FAIL ') + msg)
    if not ok:
        fails.append(msg)


def main():
    print('build output')
    rows = readlinks.read(ROOT)
    check(len(rows) >= MIN_RECORDS,
          'records: %d (floor %d)' % (len(rows), MIN_RECORDS))

    en = io.open(os.path.join(ROOT, 'links.en.js'), encoding='utf-8').read()
    en_list = json.loads(en[en.index('['):en.rindex(';')])
    en_n = len(en_list)
    check(en_n == len(rows),
          'English descriptions match record count: %d vs %d' % (en_n, len(rows)))

    print('records')
    eksik = [d['name'] for d in rows
             if not all(d.get(f) for f in ('url', 'name', 'cat', 'tr'))]
    check(not eksik, 'every record has url, name, category and description'
          + (' -- missing: %s' % eksik[:3] if eksik else ''))

    etiketsiz = [d['name'] for d in rows if not d.get('tags')]
    check(not etiketsiz, 'every record carries at least one tag'
          + (' -- bare: %s' % etiketsiz[:3] if etiketsiz else ''))

    disi = sorted({t for d in rows for t in d['tags']} - set(CANON))
    check(not disi, 'no tag outside the canonical set'
          + (' -- stray: %s' % disi[:5] if disi else ''))

    yuzey = [t for f in FACETS for t in f[3]]
    check(sorted(yuzey) == sorted(CANON),
          'every canonical tag sits in exactly one filter facet'
          + (' -- off: %s' % sorted(set(yuzey) ^ set(CANON)) if set(yuzey) != set(CANON) else ''))

    gorunmez = sorted({t for d in rows for t in d['tags']} - set(LABELS))
    check(not gorunmez, 'every tag has a display label'
          + (' -- missing: %s' % gorunmez[:5] if gorunmez else ''))

    seen, dup = set(), []
    for d in rows:
        k = re.sub(r'^https?://(www\.)?', '', d['url'].lower()).rstrip('/')
        if k in seen:
            dup.append(d['name'])
        seen.add(k)
    check(not dup, 'no duplicate URLs' + (' -- %s' % dup[:3] if dup else ''))

    # javascript: ya da data: bir URL kayda girerse esc() onu durdurmaz --
    # kacislar HTML icindir, sema icin degil. Uretimde asla olmadi; burada
    # olmadigini soyleyen tek sey bu satir.
    sema = [d['name'] for d in rows if not d['url'].startswith(('http://', 'https://'))]
    check(not sema, 'every URL is http or https'
          + (' -- %s' % sema[:3] if sema else ''))

    duz = [d['name'] for d in rows if d['url'].startswith('http://')]
    check(len(duz) <= 5, 'at most 5 plaintext http URLs (now %d)' % len(duz))

    # A record written from an issue carries a "review" note until a person has
    # done the description pass. The approve-link pull request stays red until
    # then -- that is the point of failing here rather than warning.
    bekleyen = [r['name'] for r in load_records() if r.get('review')]
    check(not bekleyen, 'no record still awaiting a description pass'
          + (' -- %s' % bekleyen[:3] if bekleyen else ''))

    kaynaksiz = sorted({d['src'] for d in rows} - set(SOURCES))
    check(not kaynaksiz, 'every record has a declared source'
          + (' -- unknown: %s' % kaynaksiz if kaynaksiz else ''))

    # Ayni adli iki kayit hem okuru ikiletiyor hem de ad uzerinden kurulan
    # iliskileri ("Ilgili") yanlis kayda baglayabiliyordu; 16 cift vardi.
    adlar = collections.Counter(d['name'].lower().strip() for d in rows)
    ikiz = sorted(k for k, v in adlar.items() if v > 1)
    check(not ikiz, 'no two records share a name'
          + (' -- %s' % ikiz[:3] if ikiz else ''))

    # Reklam tiklamasindan kopyalanan bir adres (utm_campaign=...) kayda
    # girmisti. Izleme parametresi kaydin kimligini de bozar: ayni sayfa
    # parametreli ve parametresiz iki ayri kayit gibi gorunur.
    izli = [d['name'] for d in rows if TRACKING.search(d['url'])]
    check(not izli, 'no tracking parameters in URLs'
          + (' -- %s' % izli[:3] if izli else ''))

    # The directory's promise is two things per entry: what it does and where it
    # parts ways with its neighbours. The second half was missing from over half
    # the records after the bulk intakes. This is a ratchet, like MIN_RECORDS:
    # raise DIFF_FLOOR as descriptions are rewritten, never lower it.
    farkli = [d for i, d in enumerate(rows)
              if DIFF_TR.search(d['tr']) or DIFF_EN.search(en_list[i])]
    oran = len(farkli) / float(len(rows))
    check(oran >= DIFF_FLOOR, 'descriptions that say how the entry differs: %.0f%% (floor %.0f%%)'
          % (100 * oran, 100 * DIFF_FLOOR))

    kisa = [d['name'] for d in rows if len(d['tr']) < MIN_DESC]
    check(not kisa, 'every Turkish description is at least %d characters' % MIN_DESC
          + (' -- %s' % kisa[:3] if kisa else ''))
    en_all = json.loads(en[en.index('['):en.rindex(';')])
    ayni = [rows[i]['name'] for i, t in enumerate(en_all) if t.strip() == rows[i]['tr'].strip()]
    check(not ayni, 'no English description is a copy of the Turkish one'
          + (' -- %s' % ayni[:3] if ayni else ''))

    print('categories')
    keys = [c[0] for c in CATS]
    kullanilan = {d['cat'] for d in rows}
    check(len(kullanilan) >= MIN_CATEGORIES,
          'categories in use: %d (floor %d)' % (len(kullanilan), MIN_CATEGORIES))

    yabanci = sorted(kullanilan - set(keys))
    check(not yabanci, 'no record in an undeclared category'
          + (' -- %s' % yabanci if yabanci else ''))

    girissiz = sorted(kullanilan - set(INTROS))
    check(not girissiz, 'every category in use has an introduction'
          + (' -- %s' % girissiz if girissiz else ''))

    print('fields')
    alan = [k for g in GROUPS for k in g[3]]
    check(sorted(alan) == sorted(keys),
          'every category sits in exactly one top-level field'
          + (' -- off: %s' % sorted(set(alan) ^ set(keys)) if set(alan) != set(keys) else '')
          + (' -- twice: %s' % sorted({k for k in alan if alan.count(k) > 1})
             if len(alan) != len(set(alan)) else ''))

    notsuz = [g[0] for g in GROUPS
              if not (g[0] in FIELD_NOTES and all(FIELD_NOTES[g[0]]))]
    check(not notsuz, 'every field has a one-line note in both languages'
          + (' -- %s' % notsuz if notsuz else ''))

    print('picks')
    urls = {d['url'] for d in rows}
    kayip = sorted(PICKS - urls)
    check(not kayip, 'every start-here URL resolves to a record'
          + (' -- %s' % kayip[:3] if kayip else ''))
    # Baslangic noktasi olmayan bir kategoride "◆ Buradan basla" suzgeci bos
    # donuyor ve alan sayfasindaki kartin orneklemi rastgele secilmis kaliyor.
    # Sekiz yeni kategori bu durumdaydi.
    secili = collections.Counter(d['cat'] for d in rows if d['url'] in PICKS)
    az = sorted(k for k in kullanilan if secili.get(k, 0) < 2)
    check(not az, 'every category has at least two start-here picks'
          + (' -- %s' % az if az else ''))

    print('static output')
    for name in ('sitemap.xml', 'robots.txt', 'feed.xml', 'og.png'):
        check(os.path.exists(os.path.join(ROOT, name)), 'exists: ' + name)
    for k in sorted(kullanilan):
        tr = os.path.join(ROOT, 'k', k + '.html')
        en_p = os.path.join(ROOT, 'k', 'en', k + '.html')
        if not (os.path.exists(tr) and os.path.exists(en_p)):
            check(False, 'static pages for category: ' + k)
    check(True, 'static pages present in both languages for %d categories'
          % len(kullanilan))

    eksik_akis = [k for k in sorted(kullanilan)
                  if not (os.path.exists(os.path.join(ROOT, 'feed', k + '.xml'))
                          and os.path.exists(os.path.join(ROOT, 'feed', 'en', k + '.xml')))]
    check(not eksik_akis, 'per-category Atom feed in both languages'
          + (' -- missing: %s' % eksik_akis[:3] if eksik_akis else ''))

    for h in (('k', 'index.html'), ('k', 'en', 'index.html')):
        check(os.path.exists(os.path.join(ROOT, *h)),
              'static hub page: ' + '/'.join(h))

    # hreflang yalnizca simetrikse ise yariyor: A dili B'yi gosteriyorsa
    # B de A'yi gostermeli, ve her sayfa kendini isaret etmeli.
    for rel, other in (('k/kuantum.html', 'k/en/kuantum.html'),
                       ('k/en/kuantum.html', 'k/kuantum.html')):
        h = io.open(os.path.join(ROOT, *rel.split('/')), encoding='utf-8').read()
        check('hreflang="tr"' in h and 'hreflang="en"' in h,
              'both hreflang pairs on ' + rel)
        check(('canonical" href="%s/%s"' % (EMIT_SITE, rel)) in h,
              'self-canonical on ' + rel)

    # Sitedeki gonderim formu kategoriyi Ingilizce etiketiyle onceden seciyor;
    # issue formunda o etiket yoksa GitHub secimi sessizce yok sayiyor.
    form = io.open(os.path.join(ROOT, '.github', 'ISSUE_TEMPLATE', 'new-link.yml'),
                   encoding='utf-8').read().split(chr(10))
    i = form.index('    id: cat')
    secenek = []
    for satir in form[i:]:
        if satir.startswith('        - '):
            secenek.append(json.loads(satir[10:]))
        elif secenek:
            break
    check(secenek == [c[2] for c in CATS] + ['Not sure'],
          'issue form categories match notes.CATS exactly')

    ix = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    check('links.js?v=' in ix, 'links.js carries a cache stamp')
    # The pre-rendered homepage must describe the same fields app.js would draw,
    # and its strings must still be the ones app.js uses (they are copies).
    on = ix[ix.index('<main id="list"'):ix.index('</main>')]
    check('data-pre="1"' in on and all(esc_html(g[1]) in on for g in GROUPS),
          'index.html carries the pre-rendered homepage with every field')
    app = io.open(os.path.join(ROOT, 'app.js'), encoding='utf-8').read()
    kopya = [k for k, v in HOME_TX.items() if (v.split('%')[0] if k == 'lead' else v) not in app]
    check(not kopya, 'pre-render strings still match app.js'
          + (' -- drifted: %s' % kopya if kopya else ''))
    check('app.js?v=' in ix and 'app.js?v=0"' not in ix, 'app.js carries a real cache stamp')
    check("'unsafe-inline'" not in ix.split('script-src', 1)[1].split(';', 1)[0],
          'no inline script allowed by the CSP')
    check('KULLANICI' not in ix, 'no placeholder repository address left')

    print()
    if fails:
        print('%d check(s) failed' % len(fails))
        return 1
    print('all checks passed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
