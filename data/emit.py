# -*- coding: utf-8 -*-
"""The static output that crawlers and JavaScript-less visitors get.

The app draws itself entirely from links.js, and that has a cost: the
<main> Google sees is empty. Not one word of 717 descriptions is indexed,
which for a link directory is close to not existing.

This closes that gap. Every category gets an HTML page carrying the real
text; the app still behaves as a single page, but a crawler or a visitor
without JavaScript finds something readable.

Writes:
  robots.txt      sitemap pointer
  sitemap.xml     index + category pages
  feed.xml        newest entries (Atom) -- how anyone follows the directory
  k/<category>.html      Turkish
  k/en/<category>.html   English
"""
import io
import os
import json
import datetime

SITE = 'https://latifkedi.github.io/useful-sites'
FEED_N = 40


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def _iso(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')


def _day(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')


# The static pages carry none of the app shell; their only job is to be
# readable. Same tokens, same typography, no JavaScript.
STYLE = """@font-face{
font-family:"Serif Fallback";src:local("Georgia"),local("Times New Roman"),local("Iowan Old Style");
size-adjust:98.7%;ascent-override:105%;descent-override:34%;line-gap-override:0%}
@font-face{font-family:"Source Serif 4";font-style:normal;font-weight:400;font-display:swap;
src:url("__F__/serif-400.woff2") format("woff2")}
@font-face{font-family:"Source Serif 4";font-style:normal;font-weight:600;font-display:swap;
src:url("__F__/serif-600.woff2") format("woff2")}
:root{--bg:#fcfbf9;--fg:#191817;--dim:#57544e;--faint:#77746d;
--rule:#e4e0d8;--accent:#a8451f;--accent-soft:#f6ece6;
--serif:"Source Serif 4","Serif Fallback",Georgia,"Times New Roman",serif}
@media (prefers-color-scheme:dark){:root{--bg:#1a1c20;--fg:#e2e0da;--dim:#a3a09a;
--faint:#86837c;--rule:#33363c;--accent:#e78b62;--accent-soft:#2a211c}}
*{box-sizing:border-box}
body{margin:0 auto;padding:0 24px 72px;max-width:820px;background:var(--bg);color:var(--fg);
font:17px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
a{color:var(--fg)}
header{padding:48px 0 20px;border-bottom:1px solid var(--rule)}
.up{font:12.5px/1 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:var(--dim);
text-decoration:none;letter-spacing:.04em}
.up:hover{color:var(--accent)}
h1{font:600 31px/1.2 var(--serif);letter-spacing:-.014em;margin:16px 0 0}
.intro{color:var(--dim);font-size:16px;line-height:1.7;margin:12px 0 0;max-width:66ch}
.n{font:12.5px/1 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:var(--faint);
margin-top:10px;display:block}
article{padding:16px 0 16px 14px;border-left:2px solid var(--rule);margin:26px 0 0}
article h2{font:600 18px/1.3 var(--serif);letter-spacing:-.004em;margin:0;display:inline}
article h2 a{text-decoration:none}
article h2 a:hover{color:var(--accent)}
.host{font:12px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:var(--faint);margin-left:8px}
p.d{color:var(--dim);font-size:15.5px;line-height:1.7;margin:7px 0 0}
p.t{font:12px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:var(--faint);margin:8px 0 0}
nav.other{margin:56px 0 0;padding-top:22px;border-top:1px solid var(--rule);
font-size:15px;line-height:2}
nav.other a{color:var(--dim);text-decoration:none;margin-right:18px}
nav.other a:hover{color:var(--accent)}
footer{margin-top:40px;padding-top:20px;border-top:1px solid var(--rule);
color:var(--faint);font-size:14px;line-height:1.8}
footer a{color:var(--dim)}"""

PAGE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:; font-src 'self'; base-uri 'none'; form-action 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title} — {site_name}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site_name}">
<meta property="og:title" content="{title} — {site_name}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{site}/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/atom+xml" title="{feed_title}" href="{feed_url}">
<link rel="alternate" hreflang="tr" href="{alt_tr}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="x-default" href="{alt_tr}">
<script type="application/ld+json">{jsonld}</script>
<style>{style}</style>
</head>
<body>
<header>
<a class="up" href="{home}">← {site_name}</a>
<h1>{title}</h1>
<p class="intro">{intro}</p>
<span class="n">{count} {word_links}</span>
</header>
<main>
{items}
</main>
<nav class="other">{others}</nav>
<footer>
{foot}
</footer>
</body>
</html>
"""


def _jsonld(title, canon, rows, L):
    """ItemList: a crawler sees the list as a list rather than as prose.

    The static pages already carry the text, but nothing told a machine what
    the structure was -- this is what separates a section of a directory from
    an arbitrary article.
    """
    ogeler = []
    for i, (_, d) in enumerate(rows, 1):
        ogeler.append(
            '{"@type":"ListItem","position":%d,"url":%s,"name":%s}'
            % (i, json.dumps(d['url'], ensure_ascii=False),
               json.dumps(d['name'], ensure_ascii=False)))
    return ('{"@context":"https://schema.org","@type":"ItemList",'
            '"name":%s,"url":%s,"inLanguage":"%s","numberOfItems":%d,'
            '"itemListOrder":"https://schema.org/ItemListOrderAscending",'
            '"itemListElement":[%s]}'
            % (json.dumps(title, ensure_ascii=False),
               json.dumps(canon, ensure_ascii=False), L['code'],
               len(rows), ','.join(ogeler)))


HUB = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; \
style-src 'unsafe-inline'; img-src 'self' data:; font-src 'self'; \
base-uri 'none'; form-action 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{site_name}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site_name}">
<meta property="og:title" content="{site_name}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{site}/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/atom+xml" title="{site_name}" href="{site}/feed.xml">
<link rel="alternate" hreflang="tr" href="{site}/k/index.html">
<link rel="alternate" hreflang="en" href="{site}/k/en/index.html">
<link rel="alternate" hreflang="x-default" href="{site}/">
<script type="application/ld+json">{jsonld}</script>
<style>{style}
.hub{{margin:26px 0 0}}
.hub li{{list-style:none;margin:0 0 2px;padding:12px 0;border-bottom:1px solid var(--rule)}}
.hub ul{{padding:0;margin:0}}
.hub a{{font:600 18px/1.3 var(--serif);text-decoration:none}}
.hub a:hover{{color:var(--accent)}}
.hub .c{{font:12px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:var(--faint);margin-left:8px}}
.hub .f{{font:11.5px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:var(--faint);text-decoration:none;margin-left:10px;border-bottom:1px dotted var(--rule)}}
.hub .f:hover{{color:var(--accent);border-bottom-color:var(--accent)}}
.hub p{{margin:5px 0 0;color:var(--dim);font-size:15px;line-height:1.6;max-width:70ch}}</style>
</head>
<body>
<header>
<a class="up" href="{site}/">{app_link}</a>
<h1>{site_name}</h1>
<p class="intro">{desc}</p>
<span class="n">{total} {word_links} · {ncat} {word_cats}</span>
</header>
<main class="hub"><ul>
{items}
</ul></main>
<footer>
{foot}
</footer>
</body>
</html>
"""


def _host(u):
    h = u.split('//', 1)[-1].split('/', 1)[0]
    return h[4:] if h.startswith('www.') else h


def _item(d, taglbl, desc, li):
    tags = ', '.join(taglbl.get(t, [t, t])[li] for t in d.get('tags', [])[:6])
    return (
        '<article>\n'
        '<h2><a href="%s" rel="noopener noreferrer nofollow">%s</a></h2>'
        '<span class="host">%s</span>\n'
        '<p class="d">%s</p>\n'
        '%s'
        '</article>'
    ) % (esc(d['url']), esc(d['name']), esc(_host(d['url'])), esc(desc),
         ('<p class="t">%s</p>\n' % esc(tags)) if tags else '')


# Turkish and English differ only in the words around the list, so the two
# runs share everything except this table. A crawler arriving from an English
# query used to land on a Turkish page; hreflang now pairs them up.
LANGS = {
    'tr': {
        'code': 'tr', 'li': 0, 'ci': 1, 'dir': '', 'fonts': '../fonts',
        'name': 'Kullanışlı Siteler', 'links': 'bağlantı', 'cats': 'başlık',
        'app_link': '← Aranabilir sürüme dön',
        'feed_word': 'akış', 'feed_tip': 'Bu başlığın Atom akışı',
        'hub_desc': ('Yazılım, yapay zeka, güvenlik ve bilim üzerine açıklamalı '
                     'bağlantı dizini. Her kayıtta ne işe yaradığı ve '
                     'benzerlerinden nerede ayrıldığı yazılı.'),
        'hub_foot': ('Bu sayfa dizinin metin hâli. Arama, etiket süzgeci ve '
                     'sıralama için aranabilir sürümü kullan.'),
        'foot': ('Bu sayfa dizinin {t} bölümünün metin hâli. Arama, etiket süzgeci '
                 've İngilizce açıklamalar için <a href="{s}/?cat={k}">dizine dön</a>. '
                 '<a href="{s}/k/en/{k}.html">In English</a>'),
    },
    'en': {
        'code': 'en', 'li': 1, 'ci': 2, 'dir': 'en/', 'fonts': '../../fonts',
        'name': 'Useful Sites', 'links': 'links', 'cats': 'headings',
        'app_link': '← Back to the searchable version',
        'feed_word': 'feed', 'feed_tip': 'Atom feed for this heading',
        'hub_desc': ('An annotated directory of links on software, AI, security '
                     'and science. Every entry states what the resource does and '
                     'where it parts ways with its neighbours.'),
        'hub_foot': ('The plain-text edition of the directory. For search, tag '
                     'filtering and sorting, use the searchable version.'),
        'foot': ('The plain-text edition of the {t} section. For search, tag '
                 'filtering and Turkish descriptions, <a href="{s}/?cat={k}">go to '
                 'the directory</a>. <a href="{s}/k/{k}.html">Türkçe</a>'),
    },
}


def write_all(core, cats, intros, taglbl, out_dir, en_desc):
    """core: the record list as written to links.js. cats: [(key, tr, en)].

    en_desc is the parallel list of English descriptions, so the English pages
    carry English text rather than the Turkish original with an English shell.
    """
    written = []
    for lang, L in sorted(LANGS.items()):
        kdir = os.path.join(out_dir, 'k', L['dir'].strip('/')) if L['dir'] \
            else os.path.join(out_dir, 'k')
        if not os.path.isdir(kdir):
            os.makedirs(kdir)

        order = [c[0] for c in cats]
        label = dict((c[0], c[L['ci']]) for c in cats)
        by_cat = {}
        for i, d in enumerate(core):
            by_cat.setdefault(d['cat'], []).append((i, d))

        for k in order:
            rows = by_cat.get(k)
            if not rows:
                continue
            intro = (intros.get(k) or ('', ''))[L['li']]
            others = ' '.join(
                '<a href="%s.html">%s</a>' % (esc(o), esc(label[o]))
                for o in order if o != k and by_cat.get(o))
            canon = '%s/k/%s%s.html' % (SITE, L['dir'], k)
            desc = (intro or label[k])[:180]
            items = []
            for i, d in rows:
                text = en_desc[i] if L['li'] == 1 and i < len(en_desc) else d['tr']
                items.append(_item(d, taglbl, text, L['li']))
            io.open(os.path.join(kdir, k + '.html'), 'w',
                    encoding='utf-8', newline='\n').write(PAGE.format(
                        lang=L['code'], site_name=esc(L['name']),
                        title=esc(label[k]), desc=esc(desc), canon=canon, site=SITE,
                        home=SITE + '/', intro=esc(intro),
                        style=STYLE.replace('__F__', L['fonts']),
                        count=len(rows), word_links=esc(L['links']), key=esc(k),
                        feed_title=esc('%s — %s' % (label[k], L['name'])),
                        feed_url='%s/feed/%s%s.xml' % (SITE, L['dir'], k),
                        alt_tr='%s/k/%s.html' % (SITE, k),
                        alt_en='%s/k/en/%s.html' % (SITE, k),
                        items='\n'.join(items), others=others,
                        jsonld=_jsonld(label[k], canon, rows, L),
                        foot=L['foot'].format(t=esc(label[k]), s=SITE, k=esc(k))))
            if lang == 'tr':
                written.append(k)

    _hubs(core, cats, intros, out_dir)
    _cat_feeds(core, cats, en_desc, out_dir)
    _sitemap(written, out_dir)
    _robots(out_dir)
    _feed(core, dict((c[0], c[1]) for c in cats), out_dir)
    return written


def _hubs(core, cats, intros, out_dir):
    """Her iki dil icin statik kategori dizini.

    index.html uygulamanin kendisi ve dili istemci tarafinda degistiriyor --
    yani tarayici botu icin yalnizca Turkce bir sayfa. Ingilizce icerik k/en/
    altinda zaten duruyordu ama ona acilan bir giris yoktu ve ana sayfada hic
    hreflang yoktu. Bu iki sayfa o giris.
    """
    say = {}
    for d in core:
        say[d['cat']] = say.get(d['cat'], 0) + 1
    order = [c[0] for c in cats]

    for lang, L in sorted(LANGS.items()):
        label = dict((c[0], c[L['ci']]) for c in cats)
        satir = []
        for k in order:
            if not say.get(k):
                continue
            intro = (intros.get(k) or ('', ''))[L['li']]
            # Her basligin kendi akisi var; abonelik konuya inebilsin diye
            # dizinde de gorunuyor, yoksa yalnizca sayfa kaynaginda kalirdi.
            satir.append(
                '<li><a href="%s.html">%s</a><span class="c">%d</span>'
                '<a class="f" href="../feed/%s%s.xml" title="%s">%s</a>'
                '<p>%s</p></li>'
                % (esc(k), esc(label[k]), say[k], esc(L['dir']), esc(k),
                   esc(L['feed_tip']), esc(L['feed_word']), esc(intro)))
        canon = '%s/k/%sindex.html' % (SITE, L['dir'])
        io.open(os.path.join(out_dir, 'k', L['dir'].strip('/'), 'index.html')
                if L['dir'] else os.path.join(out_dir, 'k', 'index.html'),
                'w', encoding='utf-8', newline='\n').write(HUB.format(
                    lang=L['code'], site_name=esc(L['name']), desc=esc(L['hub_desc']),
                    canon=canon, site=SITE, style=STYLE.replace('__F__', L['fonts']),
                    total=len(core), ncat=len(satir), word_links=esc(L['links']),
                    word_cats=esc(L['cats']), app_link=esc(L['app_link']),
                    items='\n'.join(satir), foot=esc(L['hub_foot']),
                    jsonld=_hub_jsonld(L, canon, order, label, say)))


def _hub_jsonld(L, canon, order, label, say):
    ogeler = []
    i = 0
    for k in order:
        if not say.get(k):
            continue
        i += 1
        ogeler.append('{"@type":"ListItem","position":%d,"url":%s,"name":%s}'
                      % (i, json.dumps('%s/k/%s%s.html' % (SITE, L['dir'], k)),
                         json.dumps(label[k], ensure_ascii=False)))
    return ('{"@context":"https://schema.org","@type":"CollectionPage",'
            '"name":%s,"url":%s,"inLanguage":"%s",'
            '"mainEntity":{"@type":"ItemList","numberOfItems":%d,'
            '"itemListElement":[%s]}}'
            % (json.dumps(L['name'], ensure_ascii=False),
               json.dumps(canon), L['code'], i, ','.join(ogeler)))


def _sitemap(keys, out_dir):
    """Site haritasi, dil ciftlerini de bildiriyor.

    hreflang zaten sayfalarin kendisinde var ve tek basina yeterli; burada
    tekrar edilmesinin sebebi Google'in ikisini capraz dogrulamasi -- eksik
    ya da asimetrik bir eslesme boylece daha erken goruluyor.
    """
    today = datetime.date.today().isoformat()
    ciftler = [('%s/k/%s.html' % (SITE, k), '%s/k/en/%s.html' % (SITE, k))
               for k in keys]
    ciftler.insert(0, ('%s/k/index.html' % SITE, '%s/k/en/index.html' % SITE))

    satir = ['  <url><loc>%s</loc><lastmod>%s</lastmod><priority>1.0</priority>'
             '</url>' % (esc(SITE + '/'), today)]
    for tr, en in ciftler:
        for u, p in ((tr, '0.8'), (en, '0.7')):
            satir.append(
                '  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority>\n'
                '    <xhtml:link rel="alternate" hreflang="tr" href="%s"/>\n'
                '    <xhtml:link rel="alternate" hreflang="en" href="%s"/>\n'
                '    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>\n'
                '  </url>' % (esc(u), today, p, esc(tr), esc(en), esc(tr)))

    io.open(os.path.join(out_dir, 'sitemap.xml'), 'w',
            encoding='utf-8', newline='\n').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + '\n'.join(satir) + '\n</urlset>\n')


def _robots(out_dir):
    io.open(os.path.join(out_dir, 'robots.txt'), 'w',
            encoding='utf-8', newline='\n').write(
        'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % SITE)


def _atom(baslik, altbaslik, self_url, alt_url, rows, en_desc, L):
    """Tek bir Atom akisi. rows: [(indeks, kayit)], zaten sirali gelir."""
    now = _iso(rows[0][1].get('added', 0) if rows else 0)
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="%s">' % L['code'],
             '<title>%s</title>' % esc(baslik),
             '<subtitle>%s</subtitle>' % esc(altbaslik),
             '<link href="%s" rel="self"/>' % esc(self_url),
             '<link href="%s"/>' % esc(alt_url),
             '<id>%s</id>' % esc(self_url),
             '<updated>%s</updated>' % now]
    for i, d in rows:
        metin = en_desc[i] if L['li'] == 1 and en_desc and i < len(en_desc) else d['tr']
        parts.append(
            '<entry>\n'
            '  <title>%s</title>\n'
            '  <link href="%s"/>\n'
            '  <id>%s</id>\n'
            '  <updated>%s</updated>\n'
            '  <summary>%s</summary>\n'
            '</entry>' % (esc(d['name']), esc(d['url']), esc(d['url']),
                          _iso(d.get('added', 0)), esc(metin)))
    parts.append('</feed>')
    return '\n'.join(parts) + '\n'


def _cat_feeds(core, cats, en_desc, out_dir):
    """Kategori basina akis.

    Tek bir kuresel akis, yalnizca guvenlik baglantilarini takip etmek isteyen
    birine her seyi gonderiyordu. Yirmi dort kucuk akis, aboneligi konuya
    indirgiyor -- dizine geri donmenin en dusuk surtunmeli yolu bu.
    """
    by_cat = {}
    for i, d in enumerate(core):
        by_cat.setdefault(d['cat'], []).append((i, d))

    n = 0
    for lang, L in sorted(LANGS.items()):
        fdir = os.path.join(out_dir, 'feed', L['dir'].strip('/')) if L['dir'] \
            else os.path.join(out_dir, 'feed')
        if not os.path.isdir(fdir):
            os.makedirs(fdir)
        label = dict((c[0], c[L['ci']]) for c in cats)
        for k, rows in by_cat.items():
            rows = sorted(rows, key=lambda t: -t[1].get('added', 0))[:FEED_N]
            io.open(os.path.join(fdir, k + '.xml'), 'w',
                    encoding='utf-8', newline='\n').write(_atom(
                        '%s — %s' % (label[k], L['name']), L['hub_desc'],
                        '%s/feed/%s%s.xml' % (SITE, L['dir'], k),
                        '%s/k/%s%s.html' % (SITE, L['dir'], k),
                        rows, en_desc, L))
            n += 1
    return n


def _feed(core, label, out_dir):
    """Newest entries. As the directory grows this is the only sane way
    for anyone to follow it."""
    rows = sorted(core, key=lambda d: -d.get('added', 0))[:FEED_N]
    # <updated> comes from the newest entry, not from the clock. Using the
    # clock made every build produce a feed.xml diff even when no link had
    # changed, which buries real changes in noise.
    now = _iso(rows[0].get('added', 0) if rows else 0)
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<feed xmlns="http://www.w3.org/2005/Atom">',
             '<title>Kullanışlı Siteler</title>',
             '<subtitle>Yazılım, yapay zeka, güvenlik ve bilim üzerine '
             'açıklamalı bağlantı dizini</subtitle>',
             '<link href="%s/feed.xml" rel="self"/>' % SITE,
             '<link href="%s/"/>' % SITE,
             '<id>%s/</id>' % SITE,
             '<updated>%s</updated>' % now]
    for d in rows:
        parts.append(
            '<entry>\n'
            '  <title>%s</title>\n'
            '  <link href="%s"/>\n'
            '  <id>%s</id>\n'
            '  <updated>%s</updated>\n'
            '  <category term="%s"/>\n'
            '  <summary>%s</summary>\n'
            '</entry>' % (
                esc(d['name']), esc(d['url']), esc(d['url']),
                _iso(d.get('added', 0)), esc(label.get(d['cat'], d['cat'])),
                esc(d['tr'])))
    parts.append('</feed>')
    io.open(os.path.join(out_dir, 'feed.xml'), 'w',
            encoding='utf-8', newline='\n').write('\n'.join(parts) + '\n')
