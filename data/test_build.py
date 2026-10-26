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

import linkstate                        # noqa: E402
import readlinks                        # noqa: E402
from notes import CATS, GROUPS, FIELD_NOTES, load_records  # noqa: E402
from notes import key as notes_key     # noqa: E402
from intros import INTROS               # noqa: E402
from picks import PICKS                 # noqa: E402
from sources import SOURCES             # noqa: E402
from tags import CANON, LABELS, FACETS  # noqa: E402
from tags import UNCOUNTED, MIN_TAGS, MAX_TAGS, LEVELS, LEVEL_CATS  # noqa: E402
from emit import SITE as EMIT_SITE, HOME_TX, esc as esc_html  # noqa: E402
from paths import PATHS                 # noqa: E402
from taghubs import INTROS as TAG_INTROS, MIN_N as TAG_MIN, SKIP as TAG_SKIP, slug as tag_slug  # noqa: E402

MIN_RECORDS = 1850
MIN_CATEGORIES = 48
# Records with fewer than tags.MIN_TAGS tags outside price & licence. A ceiling,
# the other way round from MIN_RECORDS: lower it as thin records get a second
# tag that their own text supports, never raise it to let a new thin one in.
# 99 when the rule arrived (October 2026): mostly stock-photo and icon banks,
# news boards and productivity apps, where no topic tag could be justified.
THIN_MAX = 99

MIN_DESC = 30
DIFF_FLOOR = 0.99
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

    _l = io.open(os.path.join(ROOT, 'links.js'), encoding='utf-8').read()
    AXES_JS = json.loads(_l[_l.index('window.AXES=') + 12:_l.index(';', _l.index('window.AXES='))])
    en = io.open(os.path.join(ROOT, 'links.en.js'), encoding='utf-8').read()
    en_list = json.loads(en[en.index('['):en.rindex(';')])
    en_n = len(en_list)
    check(en_n == len(rows),
          'English descriptions match record count: %d vs %d' % (en_n, len(rows)))
    tr_src = io.open(os.path.join(ROOT, 'desc.tr.js'), encoding='utf-8').read()
    tr_n = len(json.loads(tr_src[tr_src.index('['):tr_src.rindex(';')]))
    check(tr_n == len(rows),
          'Turkish descriptions (desc.tr.js) match record count: %d vs %d' % (tr_n, len(rows)))
    links_src = io.open(os.path.join(ROOT, 'links.js'), encoding='utf-8').read()
    check('"tr":"' not in links_src.split('window.LINKS=', 1)[1],
          'links.js carries no descriptions (they live in desc.tr.js and links.en.js)')

    print('verification data')
    _ver = json.load(io.open(os.path.join(ROOT, 'data', 'verified.json'), encoding='utf-8'))
    _orph = linkstate.orphan_keys(_ver, [d['url'] for d in rows], notes_key)
    check(not _orph, 'verified.json has no key that no record carries'
          + (' -- %s' % _orph[:3] if _orph else ''))
    _man = json.load(io.open(os.path.join(ROOT, 'data', 'manual.json'), encoding='utf-8'))
    _morph = linkstate.orphan_keys(_man, [d['url'] for d in rows], notes_key)
    check(not _morph, 'manual.json has no decision about a record that is gone'
          + (' -- %s' % _morph[:3] if _morph else ''))

    print('tags')
    _maliyet = ('ücretsiz', 'freemium', 'ücretli')
    _cift = [d['name'] for d in rows if len([t for t in d['tags'] if t in _maliyet]) != 1]
    check(not _cift, 'every record carries exactly one of ücretsiz / freemium / ücretli'
          + (' -- %d: %s' % (len(_cift), _cift[:3]) if _cift else ''))
    def _sayi(d):
        return len([t for t in d['tags'] if t not in UNCOUNTED])
    _fazla = [d['name'] for d in rows if _sayi(d) > MAX_TAGS]
    check(not _fazla, 'no record carries more than %d tags outside price & licence' % MAX_TAGS
          + (' -- %d: %s' % (len(_fazla), _fazla[:3]) if _fazla else ''))
    _ince = [d['name'] for d in rows if _sayi(d) < MIN_TAGS]
    check(len(_ince) <= THIN_MAX, 'records with fewer than %d tags outside price & licence: %d (ceiling %d)'
          % (MIN_TAGS, len(_ince), THIN_MAX))
    _seviye = [d['name'] for d in rows
               if (set(d['tags']) & set(LEVELS) and d['cat'] not in LEVEL_CATS)
               or len(set(d['tags']) & set(LEVELS)) > 1]
    check(not _seviye, 'a level (başlangıç / orta / ileri) only on learning records, one at most'
          + (' -- %s' % _seviye[:3] if _seviye else ''))

    print('comparisons (vs)')
    _vs = [d for d in rows if d.get('vs')]
    # A ratchet like the others: raise it as comparisons are written, never lower it.
    check(len(_vs) >= 420, 'records that carry a curated comparison: %d (floor 420)' % len(_vs))
    check(all(0 <= j < len(rows) and j != i and 0 <= a < len(AXES_JS)
              for i, d in enumerate(rows) for j, a in d.get('vs', [])),
          'every vs points at another record and a known axis')

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

    # Superlatives are the sentences a page stops being true of first, and
    # nobody rechecks them: "de facto standard", "the largest" and the like.
    # "One of the largest" and "among the oldest" are claims that stay true.
    ABS = re.compile(r'\bde facto\b|(?<!of )(?<!among )\bthe (?:largest|biggest|fastest|best open)\b', re.I)
    ABS_OK = {'Stable Diffusion WebUI', 'Image Max URL'}   # "installed base ... still the largest"; "largest/original version"
    mutlak = [d['name'] for i, d in enumerate(rows)
              if ABS.search(en_list[i]) and d['name'] not in ABS_OK]
    check(not mutlak, 'no description claims "de facto" or "the largest/biggest/fastest"'
          + (' -- %s' % mutlak[:3] if mutlak else ''))

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

    # "Benzerleri": up to three from the same heading, plus at most one from
    # another heading of the same area; never the record itself.
    alan = {k: g[0] for g in GROUPS for k in g[3]}
    kotu_rel = []
    for i, d in enumerate(rows):
        rel = d.get('rel') or []
        disari = [j for j in rel if 0 <= j < len(rows) and rows[j]['cat'] != d['cat']]
        if (len(rel) > 4 or i in rel or any(not (0 <= j < len(rows)) for j in rel) or len(disari) > 1
                or any(alan.get(rows[j]['cat']) != alan.get(d['cat']) for j in disari)):
            kotu_rel.append(d['name'])
    check(not kotu_rel, 'related entries: at most 4, one from another heading of the same area at most'
          + (' -- %s' % kotu_rel[:3] if kotu_rel else ''))

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

    # Every entry on a static page is linkable (k/diller.html#python-swaroopch-com),
    # ids are unique on the page, and the ItemList's anchored urls land on them.
    sorunlu = []
    for k in sorted(kullanilan):
        for sub in ('', 'en'):
            html = io.open(os.path.join(ROOT, 'k', sub, k + '.html'), encoding='utf-8').read()
            ids = re.findall(r'<article class="rec" id="([^"]+)"', html)
            recs = html.count('<article class="rec"')
            hedef = re.findall(r'"url":"[^"#]*/k/(?:en/)?%s\.html#([^"]+)"' % re.escape(k), html)
            if len(ids) != recs or len(set(ids)) != len(ids) or hedef != ids:
                sorunlu.append(os.path.join(sub, k))
    check(not sorunlu, 'every static entry has a unique anchor, and the ItemList points at them'
          + (' -- %s' % sorunlu[:3] if sorunlu else ''))

    eksik_akis = [k for k in sorted(kullanilan)
                  if not (os.path.exists(os.path.join(ROOT, 'feed', k + '.xml'))
                          and os.path.exists(os.path.join(ROOT, 'feed', 'en', k + '.xml')))]
    check(not eksik_akis, 'per-category Atom feed in both languages'
          + (' -- missing: %s' % eksik_akis[:3] if eksik_akis else ''))

    for h in (('k', 'index.html'), ('k', 'en', 'index.html')):
        check(os.path.exists(os.path.join(ROOT, *h)),
              'static hub page: ' + '/'.join(h))

    print('goal paths')
    bykey = {notes_key(d['url']): d for d in rows}
    yol_sorun = []
    for p in PATHS:
        ad = p.get('en_slug', '?')
        if not (8 <= len(p['steps']) <= 15):
            yol_sorun.append('%s: %d steps' % (ad, len(p['steps'])))
        if not all(p.get(f) for f in ('tr', 'en', 'tr_slug', 'en_slug')) or not all(p['intro']):
            yol_sorun.append('%s: title, slug or intro missing in a language' % ad)
        for u, w_tr, w_en in p['steps']:
            d = bykey.get(notes_key(u))
            if not d:
                yol_sorun.append('%s: %s is not a record' % (ad, u))
            elif 'arşivlenmiş' in d['tags'] or d.get('hs') == 'arşiv' or d.get('dead'):
                yol_sorun.append('%s: %s is archived or dead' % (ad, u))
            if not (w_tr.strip() and w_en.strip()) or w_tr.strip() == w_en.strip():
                yol_sorun.append('%s: %s lacks a why-now line in both languages' % (ad, u))
        if len({notes_key(u) for u, _, _ in p['steps']}) != len(p['steps']):
            yol_sorun.append('%s: a step repeats' % ad)
    check(len(PATHS) == 8, 'eight goal paths (%d)' % len(PATHS))
    check(not yol_sorun, 'every path has 8-15 live, non-archived steps with a why-now line in TR and EN'
          + (' -- %s' % yol_sorun[:3] if yol_sorun else ''))
    slugs = [p['tr_slug'] for p in PATHS] + [p['en_slug'] for p in PATHS]
    check(len(set(slugs)) == len(slugs) and all(re.match(r'^[a-z0-9-]+$', s) for s in slugs),
          'path slugs are unique and ASCII')
    yok = [s for s in ['k/yol/index.html', 'k/en/path/index.html']
           + ['k/yol/%s.html' % p['tr_slug'] for p in PATHS]
           + ['k/en/path/%s.html' % p['en_slug'] for p in PATHS]
           if not os.path.exists(os.path.join(ROOT, *s.split('/')))]
    check(not yok, 'every path page exists in both languages, with its index'
          + (' -- %s' % yok[:3] if yok else ''))

    print('tag pages')
    _tn = collections.Counter(t for d in rows for t in d['tags'])
    hub_tags = [t for t in CANON if t not in TAG_SKIP and _tn[t] >= TAG_MIN]
    check(len(hub_tags) >= 40, 'tags with a page: %d (floor 40)' % len(hub_tags))
    girissiz_t = [t for t in CANON if t not in TAG_SKIP and not (t in TAG_INTROS and all(TAG_INTROS[t]))]
    check(not girissiz_t, 'every tag that can have a page has an intro in TR and EN'
          + (' -- %s' % girissiz_t[:5] if girissiz_t else ''))
    tslug = [tag_slug(t) for t in CANON]
    check(len(set(tslug)) == len(tslug) and all(re.match(r'^[a-z0-9-]+$', s) for s in tslug),
          'tag slugs are unique and ASCII')
    beklenen = {tag_slug(t) + '.html' for t in hub_tags} | {'index.html'}
    for sub in (('k', 't'), ('k', 'en', 'tag')):
        var = set(os.listdir(os.path.join(ROOT, *sub))) if os.path.isdir(os.path.join(ROOT, *sub)) else set()
        check(var == beklenen, 'tag pages in %s: exactly the tags on %d+ records'
              % ('/'.join(sub), TAG_MIN) + (' -- off: %s' % sorted(var ^ beklenen)[:4] if var != beklenen else ''))
    ince = []
    for t in hub_tags:
        h = io.open(os.path.join(ROOT, 'k', 't', tag_slug(t) + '.html'), encoding='utf-8').read()
        if h.count('<article class="rec"') != _tn[t]:
            ince.append(t)
    check(not ince, 'each tag page lists every record carrying the tag'
          + (' -- %s' % ince[:3] if ince else ''))
    # A tag page is a pointer list: name, first sentence, the record's place on
    # its heading page. Repeating every description doubled the corpus.
    uzun = []
    for t in hub_tags:
        h = io.open(os.path.join(ROOT, 'k', 'en', 'tag', tag_slug(t) + '.html'), encoding='utf-8').read()
        if '<span class="host">' in h or len(re.findall(
                r'<p class="desc">[^<]*(?:<code>[^<]*</code>[^<]*)*<a href="\.\./[a-z_]+\.html#[a-z0-9-]+">', h)) != _tn[t]:
            uzun.append(t)
    check(not uzun, 'tag pages show a first sentence and a link to the heading page anchor, not the full entry'
          + (' -- %s' % uzun[:3] if uzun else ''))

    print('sitemap')
    sm = io.open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    locs = re.findall(r'<loc>([^<]+)</loc>', sm)
    hedefsiz = [u for u in locs if u != EMIT_SITE + '/'
                and not os.path.exists(os.path.join(ROOT, *u[len(EMIT_SITE) + 1:].split('/')))]
    check(not hedefsiz, 'every sitemap URL is a committed file (%d URLs)' % len(locs)
          + (' -- %s' % hedefsiz[:3] if hedefsiz else ''))
    statik = sorted('k/' + os.path.relpath(os.path.join(dp, f), os.path.join(ROOT, 'k')).replace(os.sep, '/')
                    for dp, _, fs in os.walk(os.path.join(ROOT, 'k')) for f in fs if f.endswith('.html'))
    haritasiz = [s for s in statik if '%s/%s' % (EMIT_SITE, s) not in locs and s != 'k/en/index.html']
    check(not haritasiz, 'every static page is in the sitemap (k/en/index.html, which forwards to /, aside)'
          + (' -- %s' % haritasiz[:3] if haritasiz else ''))
    check('%s/k/en/index.html' % EMIT_SITE not in locs, 'k/en/index.html, a forward to /, is not in the sitemap')
    check(len(set(locs)) == len(locs), 'no URL is in the sitemap twice')
    blocks = re.findall(r'<url>(.*?)</url>', sm, re.S)
    xdef = [b for b in blocks if re.search(r'hreflang="en" href="([^"]+)"', b).group(1)
            != re.search(r'hreflang="x-default" href="([^"]+)"', b).group(1)]
    check(bool(blocks) and not xdef, 'every sitemap entry names the English page as x-default'
          + (' -- %d' % len(xdef) if xdef else ''))
    mods = re.findall(r'<lastmod>([^<]+)</lastmod>', sm)
    check(len(mods) == len(locs) and all(re.match(r'^\d{4}-\d{2}-\d{2}$', m) for m in mods),
          'every sitemap URL has a <lastmod> date')
    check(len(set(mods)) >= 5, '<lastmod> is per page, from the data: %d distinct dates over %d URLs'
          % (len(set(mods)), len(mods)))

    print('also see, social images')
    yoksun = []
    for k in sorted(kullanilan):
        for sub, head in (('', 'Ayrıca bak'), ('en', 'Also see')):
            h = io.open(os.path.join(ROOT, 'k', sub, k + '.html'), encoding='utf-8').read()
            m = re.search(r'<h2 class="sh">%s</h2><p>(.*?)</p>' % head, h)
            if not m or len(re.findall(r'<a href="([a-z_]+)\.html"', m.group(1))) < 3:
                yoksun.append(os.path.join(sub, k))
    check(not yoksun, 'every heading page suggests at least three related headings'
          + (' -- %s' % yoksun[:3] if yoksun else ''))
    ogdir = os.path.join(ROOT, 'og')
    pngs = sorted(f for f in os.listdir(ogdir) if f.endswith('.png')) if os.path.isdir(ogdir) else []
    agir = [f for f in pngs if os.path.getsize(os.path.join(ogdir, f)) > 45 * 1024]
    check(not agir, 'per-page social images stay under 45 KB (%d images)' % len(pngs)
          + (' -- %s' % agir[:3] if agir else ''))
    eksik_og = [k for k in sorted(kullanilan) if k + '.png' not in pngs] + \
               ['path-' + p['en_slug'] for p in PATHS if 'path-%s.png' % p['en_slug'] not in pngs]
    check(not eksik_og, 'every heading and path has its own social image (run data/make_og.py)'
          + (' -- %s' % eksik_og[:3] if eksik_og else ''))
    sw = io.open(os.path.join(ROOT, 'sw.js'), encoding='utf-8').read()
    check('og/' not in sw, 'the service worker does not precache the social images')

    # hreflang yalnizca simetrikse ise yariyor: A dili B'yi gosteriyorsa
    # B de A'yi gostermeli, ve her sayfa kendini isaret etmeli.
    for rel in ('k/kuantum.html', 'k/en/kuantum.html'):
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
    check(all(re.search(r'data-%s="%s\?v=[0-9a-f]{8}"' % (a, re.escape(b)), ix)
              for a, b in (('tr', 'desc.tr.js'), ('en', 'links.en.js'))) and 'boot.js?v=' in ix,
          'boot.js and the two description files carry cache stamps')
    css_path = os.path.join(ROOT, 'style.css')
    css = io.open(css_path, encoding='utf-8').read() if os.path.exists(css_path) else None
    m_css = re.search(r'<style id="css">\n(.*?)</style>', ix, re.S)
    check(css is not None and bool(m_css) and m_css.group(1) == css,
          'index.html inlines style.css byte for byte')
    check(len(re.findall(r'<h1\b', ix)) == 1 and ('<em>%s</em>' % '{:,}'.format(len(rows))) in ix,
          'index.html has one h1, the hero, carrying the live record count')
    check('<a class="logo"' in ix and not re.search(r'<h1[^>]*>\s*Kullanışlı Siteler', ix),
          'the wordmark is a link, not a heading')
    govde = re.sub(r':root[^{]*\{[^}]*\}', '', css or '')
    hex_ = re.findall(r'(?<=[\s:,(])#[0-9a-fA-F]{3,8}(?=[\s;,)}!])', govde)
    check(css is not None and not hex_, 'style.css takes every colour from its :root tokens'
          + (' -- literals: %s' % sorted(set(hex_))[:5] if hex_ else ''))
    # Every page under k/, the path and tag folders included.
    sayfalar = [os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(ROOT, 'k'))
                for f in fs if f.endswith('.html')]
    kotu = []
    for p in sayfalar:
        t = io.open(p, encoding='utf-8').read()
        if ('style.css?v=' not in t or "style-src 'self';" not in t or '<style' in t
                or 'class="static"' not in t):
            kotu.append(os.path.relpath(p, ROOT))
    check(sayfalar and not kotu, 'static pages link style.css, allow only self styles, carry no inline style'
          + (' -- %s' % kotu[:3] if kotu else ''))
    # The pre-rendered homepage must describe the same fields app.js would draw,
    # and its strings must still be the ones app.js uses (they are copies).
    on = ix[ix.index('<main id="list"'):ix.index('</main>')]
    check('data-pre="1"' in on and all(esc_html(g[2]) in on for g in GROUPS),
          'index.html carries the pre-rendered homepage with every field')
    app = io.open(os.path.join(ROOT, 'app.js'), encoding='utf-8').read()
    def _parcalar(v):
        return [p for p in re.split(r'%[ds]', v) if p]
    kopya = [k for k, v in HOME_TX.items() if not all(p in app for p in _parcalar(v))]
    check(not kopya, 'pre-render strings still match app.js'
          + (' -- drifted: %s' % kopya if kopya else ''))
    check('app.js?v=' in ix and 'app.js?v=0"' not in ix, 'app.js carries a real cache stamp')
    parts = sorted(f for f in os.listdir(os.path.join(ROOT, 'src', 'app')) if f.endswith('.js'))
    joined = ''.join(io.open(os.path.join(ROOT, 'src', 'app', f), encoding='utf-8', newline='').read() for f in parts)
    check(joined == app, 'app.js is exactly src/app/*.js joined in name order (edit the parts, not app.js)')
    s_at, a_at = ix.find('src="search.js?v='), ix.find('src="app.js?v=')
    check(0 <= s_at < a_at, 'index.html loads a stamped search.js before app.js')
    # Installable and offline: the manifest is linked and allowed by the CSP,
    # every icon it names exists, and the service worker app.js registers is
    # there to register.
    check('<link rel="manifest" href="manifest.webmanifest">' in ix and "manifest-src 'self'" in ix,
          'index.html links the web manifest and its CSP allows it')
    man = json.load(io.open(os.path.join(ROOT, 'manifest.webmanifest'), encoding='utf-8'))
    missing = [i['src'] for i in man.get('icons', []) if not os.path.exists(os.path.join(ROOT, i['src']))]
    check(man.get('start_url') == './' and not missing and
          any(i.get('purpose') == 'maskable' for i in man.get('icons', [])),
          'the manifest starts at ./ and every icon it names exists, one of them maskable'
          + (' -- missing: %s' % missing if missing else ''))
    check(os.path.exists(os.path.join(ROOT, 'sw.js')) and 'serviceWorker.register("sw.js")' in app,
          'app.js registers sw.js, and sw.js exists')
    check("'unsafe-inline'" not in ix.split('script-src', 1)[1].split(';', 1)[0],
          'no inline script allowed by the CSP')
    check('KULLANICI' not in ix, 'no placeholder repository address left')

    extra_checks(rows, kullanilan)

    print()
    if fails:
        print('%d check(s) failed' % len(fails))
        return 1
    print('all checks passed')
    return 0


# ------------------------------------------------------------------ trust, feeds, open data
# A page larger than this is a list nobody reads to the end. Measured October
# 2026: heading pages 18-122 KB with the trust line (ogrenme the largest, 102 KB
# before it); the largest tag page (awesome-liste) 252 KB once tag pages became
# pointer lists (294 KB before). Raise them on purpose, not to make a build green.
PAGE_BUDGET = 300 * 1024
CAT_BUDGET = 128 * 1024


class _Head(object):
    """canonical, hreflang alternates and Atom alternates of one page."""

    def __init__(self, html):
        m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
        self.canon = m.group(1) if m else None
        self.alts = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', html))
        self.feeds = re.findall(r'<link rel="alternate" type="application/atom\+xml"[^>]* href="([^"]+)"', html)


def _file_of(url):
    if url == EMIT_SITE + '/':
        return 'index.html'
    return url[len(EMIT_SITE) + 1:] if url.startswith(EMIT_SITE + '/') else None


def extra_checks(rows, kullanilan):
    import csv
    import xml.dom.minidom
    import sitepages
    SITE = EMIT_SITE
    pages = sorted('k/' + os.path.relpath(os.path.join(dp, f), os.path.join(ROOT, 'k')).replace(os.sep, '/')
                   for dp, _, fs in os.walk(os.path.join(ROOT, 'k')) for f in fs if f.endswith('.html'))
    src = {p: io.open(os.path.join(ROOT, *p.split('/')), encoding='utf-8').read() for p in pages + ['index.html']}
    heads = {p: _Head(h) for p, h in src.items()}

    print('hreflang')
    fwd = src['k/en/index.html']
    check('http-equiv="refresh" content="0; url=../../"' in fwd and
          '<link rel="canonical" href="%s/">' % SITE in fwd and 'hreflang' not in fwd,
          'k/en/index.html forwards to / with / as canonical, and claims no language pair')
    check(heads['k/index.html'].alts.get('en') == SITE + '/'
          and heads['index.html'].alts.get('tr') == SITE + '/k/index.html',
          '/ and k/index.html name each other as their English and Turkish pages')
    sorun = []
    for p, hd in heads.items():
        if p == 'k/en/index.html':
            continue
        me = SITE + '/' + (p if p != 'index.html' else '')
        if not hd.alts or hd.canon != me:
            sorun.append('%s: canonical/alternates' % p)
            continue
        if hd.alts.get('x-default') != hd.alts.get('en'):
            sorun.append('%s: x-default is not the English page' % p)
        if me not in (hd.alts.get('tr'), hd.alts.get('en')):
            sorun.append('%s: does not list itself' % p)
        for lang in ('tr', 'en'):
            o = heads.get(_file_of(hd.alts.get(lang, '')))
            if o is None or o.alts.get('tr') != hd.alts.get('tr') or o.alts.get('en') != hd.alts.get('en'):
                sorun.append('%s: %s pair missing or asymmetric' % (p, lang))
    check(not sorun, 'hreflang on all %d pages: self-canonical, reciprocal, x-default = English' % len(heads)
          + (' -- %s' % sorun[:3] if sorun else ''))

    print('feeds')
    xmls = ['sitemap.xml', 'feed.xml'] + sorted(
        os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, '/')
        for dp, _, fs in os.walk(os.path.join(ROOT, 'feed')) for f in fs)
    kotu = []
    for x in xmls:
        try:
            xml.dom.minidom.parse(os.path.join(ROOT, *x.split('/')))
        except Exception as e:          # any parse error is the failure
            kotu.append('%s: %s' % (x, e))
    check(not kotu, 'the sitemap and all %d feeds are well-formed XML' % (len(xmls) - 1)
          + (' -- %s' % kotu[:2] if kotu else ''))
    beklenen = ({'feed/%s.xml' % k for k in kullanilan} | {'feed/en/%s.xml' % k for k in kullanilan}
                | {'feed/en.xml', 'feed/changes.xml', 'feed/en/changes.xml'})
    var = {x for x in xmls if x.startswith('feed/')}
    check(var == beklenen, 'feed/ holds exactly the heading, site-wide and changes feeds in both languages'
          + (' -- off: %s' % sorted(var ^ beklenen)[:4] if var != beklenen else ''))
    yanlis = []
    for x in ('feed.xml', 'feed/en.xml', 'feed/en/diller.xml', 'feed/diller.xml'):
        t = io.open(os.path.join(ROOT, *x.split('/')), encoding='utf-8').read()
        links = re.findall(r'<entry>\s*<title>[^<]*</title>\s*<link href="([^"]+)"', t)
        if (not links or not all(re.match(re.escape(SITE) + r'/k/(en/)?[a-z_]+\.html#[a-z0-9-]+$', u) for u in links)
                or 'type="application/atom+xml"' not in t or '<content type="html">' not in t):
            yanlis.append(x)
    check(not yanlis, 'feed entries link to the entry on its heading page, the site itself in the content'
          + (' -- %s' % yanlis if yanlis else ''))
    check(heads['index.html'].feeds == ['feed/en.xml'], '/ advertises the English feed (feed/en.xml)')
    ak = []
    for p, hd in heads.items():
        if p in ('index.html', 'k/en/index.html'):
            continue
        dil = 'en/' if p.startswith('k/en/') else ''
        if not hd.feeds or not all(f == SITE + ('/feed/en.xml' if dil else '/feed.xml')
                                   or re.match(re.escape(SITE + '/feed/' + dil) + r'[a-z_]+\.xml$', f)
                                   for f in hd.feeds):
            ak.append(p)
    check(not ak, 'every page advertises a feed in its own language' + (' -- %s' % ak[:3] if ak else ''))

    print('trust on the static pages')
    eksik = []
    for k in sorted(kullanilan):
        for sub in ('', 'en/'):
            h = src['k/%s%s.html' % (sub, k)]
            n = h.count('<article class="rec"')
            if (h.count('<a class="arch" href="https://web.archive.org/web/') < n
                    or h.count('<span class="age">') + h.count('<span class="badge chk">') != n):
                eksik.append(sub + k)
    check(not eksik, 'every heading-page entry shows its check date (or "not scanned") and a Wayback link'
          + (' -- %s' % eksik[:3] if eksik else ''))
    dead = [d for d in rows if d.get('dead')]
    olu_yok = [d['name'] for d in dead if 'badge dead' not in src['k/en/%s.html' % d['cat']]]
    check(not olu_yok, 'a dead entry carries the Dead badge on its page (%d dead now)' % len(dead)
          + (' -- %s' % olu_yok[:3] if olu_yok else ''))
    ayak = [p for p in pages if p != 'k/en/index.html' and not all(
        x in src[p] for x in ('about.html">', 'changes.html">', 'github.com/latifkedi/useful-sites"',
                              '/blob/main/LICENSE"'))]
    check(not ayak, 'every static page ends with the methodology, changes, repository and licence links'
          + (' -- %s' % ayak[:3] if ayak else ''))

    print('about, changes, digests, alternatives')
    for f, en_f in (('about.html', 'about.html'), ('changes.html', 'changes.html'),
                    ('t/index.html', 'tag/index.html'), ('tesekkur.html', 'credits.html')):
        check(('k/' + f) in src and ('k/en/' + en_f) in src, 'k/%s and k/en/%s exist' % (f, en_f))
    ab = src['k/en/about.html']
    check(all(x in ab for x in ('machine-assisted and human-reviewed', 'github.com/latifkedi"',
                                'data/v1/links.json', 'data/v1/links.csv', 'credits.html#src-kedi'))
          and '"maintainer": {"@type": "Person", "name": "latifkedi", "url": "https://github.com/latifkedi"}' in ab,
          'the about page discloses AI assistance, names the maintainer, links the open data and the sources')
    check('makine yardımıyla yazılmış, insan tarafından' in src['k/about.html'],
          'the Turkish about page carries the same disclosure')
    weeks = sorted(p for p in pages if p.startswith('k/week/'))
    weeks_en = sorted(p for p in pages if p.startswith('k/en/week/'))
    check(1 <= len(weeks) <= sitepages.WEEKS and [w[7:] for w in weeks] == [w[10:] for w in weeks_en],
          'weekly digests: %d, the same weeks in both languages, at most %d' % (len(weeks), sitepages.WEEKS))
    ch = src['k/en/changes.html']
    check(all(('week/%s"' % w[7:]) in ch for w in weeks), 'the changes page links every weekly digest')
    rem = [l.split('\t')[0] for l in io.open(os.path.join(D, 'removed.txt'), encoding='utf-8')
           if l.strip() and not l.startswith('#')]
    check(all(esc_html(u) in ch for u in rem), 'the changes page lists every removal in removed.txt (%d)' % len(rem))
    alts = sitepages.alt_clusters(rows)
    check(len([p for p in pages if p.startswith('k/alt/')]) == len(alts)
          == len([p for p in pages if p.startswith('k/en/alt/')])
          and all(len(a['rivals']) >= sitepages.ALT_MIN for a in alts),
          'alternatives pages: %d, one per entry with %d+ curated rivals, in both languages'
          % (len(alts), sitepages.ALT_MIN))
    bagsiz = [a['slug'] for a in alts
              if 'href="alt/%s.html"' % a['slug'] not in src['k/en/%s.html' % rows[a['i']]['cat']]]
    check(not bagsiz, 'each alternatives page is linked from its entry on the heading page'
          + (' -- %s' % bagsiz[:3] if bagsiz else ''))
    cr = src['k/en/credits.html']
    srcs = {d['src'] for d in rows}
    lisanssiz = sorted(k for k in srcs if 'id="src-%s"' % k not in cr)
    check(not lisanssiz and cr.count('Licence: ') == len(srcs),
          "the credits page states every source's licence" + (' -- %s' % lisanssiz if lisanssiz else ''))

    print('open data')
    lj = json.load(io.open(os.path.join(D, 'v1', 'links.json'), encoding='utf-8'))
    with io.open(os.path.join(D, 'v1', 'links.csv'), encoding='utf-8', newline='') as f:
        cv = list(csv.reader(f))
    check(lj['count'] == len(lj['records']) == len(rows) == len(cv) - 1,
          'data/v1: links.json and links.csv carry every record (%d)' % len(rows))
    check(cv[0] == sitepages.FIELDS and all(list(r) == sitepages.FIELDS for r in lj['records']),
          'data/v1: exactly the documented fields, in order')
    check([r['url'] for r in lj['records']] == [d['url'] for d in rows] == [r[0] for r in cv[1:]],
          "data/v1: the directory's own order, the same in both files")
    schema = io.open(os.path.join(D, 'v1', 'SCHEMA.md'), encoding='utf-8').read()
    check(all('`%s`' % f in schema for f in sitepages.FIELDS) and 'CC BY 4.0' in schema,
          'data/v1/SCHEMA.md documents every field and the licence')

    print('page weight')
    agir = [p for p in pages if len(src[p].encode('utf-8')) > PAGE_BUDGET]
    check(not agir, 'no static page over %d KB' % (PAGE_BUDGET // 1024) + (' -- %s' % agir[:3] if agir else ''))
    agir = [k for k in kullanilan for sub in ('', 'en/')
            if len(src['k/%s%s.html' % (sub, k)].encode('utf-8')) > CAT_BUDGET]
    check(not agir, 'no heading page over %d KB' % (CAT_BUDGET // 1024) + (' -- %s' % agir[:3] if agir else ''))

    print('numbers in the docs')
    from coverage import counts
    cov = {name: n for n, name in counts(rows)}
    contrib = re.sub(r'\s+', ' ', io.open(os.path.join(ROOT, 'CONTRIBUTING.md'), encoding='utf-8').read())
    said = {'WebAssembly': 'WebAssembly', 'regular expressions': 'Regular expressions',
            'accessibility': 'Accessibility (a11y)', 'typesetting': 'LaTeX / typesetting',
            'maps and GIS': 'GIS / maps', 'low-code and no-code': 'Low-code / no-code',
            'cryptography for learners': 'Cryptography'}
    yanlis, gorulen = [], 0
    for phrase, topic in said.items():
        m = re.search(re.escape(phrase) + r' \((\d+)\)', contrib)
        if m:
            gorulen += 1
            if int(m.group(1)) != cov[topic]:
                yanlis.append('%s: %s, coverage.py says %d' % (phrase, m.group(1), cov[topic]))
    check(gorulen == len(said) and not yanlis, 'CONTRIBUTING.md quotes the coverage.py counts as they are'
          + (' -- %s' % yanlis if yanlis else '') + (' -- %d of %d found' % (gorulen, len(said)) if gorulen != len(said) else ''))
    readme = io.open(os.path.join(ROOT, 'README.md'), encoding='utf-8').read()
    n_ = len(rows) // 100 * 100
    check('<!-- n -->{:,}{}<!-- /n -->'.format(n_, '+' if len(rows) > n_ else '') in readme
          and '<!-- c -->%d<!-- /c -->' % len(kullanilan) in readme,
          'README.md states the record and heading counts the build wrote')
    ntag = []
    for f in ('CONTRIBUTING.md', os.path.join('data', 'README.md')):
        for m in re.finditer(r'(\d+) canonical tags', io.open(os.path.join(ROOT, f), encoding='utf-8').read()):
            if int(m.group(1)) != len(CANON):
                ntag.append(f)
    check(not ntag, 'the docs give the number of canonical tags as it is (%d)' % len(CANON)
          + (' -- %s' % ntag if ntag else ''))

    print('verification data, social images')
    ver = json.load(io.open(os.path.join(D, 'verified.json'), encoding='utf-8'))
    check(re.match(r'^\d{4}-\d{2}-\d{2}$', ver.get('scanned') or '') is not None
          and not [k for k, v in ver.items() if k != 'scanned' and v.get('d') and v.get('s') != 'olu'],
          'verified.json carries the scan date once ("scanned"); only dead entries keep their own "d"')
    from paths import PATHS
    claimed = {k + '.png' for k in kullanilan} | {'path-%s.png' % p['en_slug'] for p in PATHS}
    og = {f for f in os.listdir(os.path.join(ROOT, 'og')) if f.endswith('.png')}
    check(og == claimed, 'og/ holds exactly one image per heading and path'
          + (' -- off: %s' % sorted(og ^ claimed)[:4] if og != claimed else ''))


if __name__ == '__main__':
    sys.exit(main())
