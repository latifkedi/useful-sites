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
  k/yol/, k/en/path/     the goal paths of paths.py, and their index
  k/t/, k/en/tag/        one page per tag on enough records (taghubs.py)
"""
import io
import os
import re
import json
import datetime
import hashlib

from sources import SOURCES
from notes import key as url_key

SITE = 'https://latifkedi.github.io/useful-sites'
FEED_N = 40


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def _iso(ts):
    return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def _day(ts):
    return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime('%Y-%m-%d')


# The static pages carry none of the app shell; their only job is to be
# readable. They link the one stylesheet the app inlines, with a content
# stamp so a browser never pairs a new page with an old stylesheet.
ENSO = ('<svg class="enso" viewBox="0 0 60 60" aria-hidden="true">'
        '<path d="M43 12A22 22 0 1 0 51 30"/></svg>')

HEAD = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self'; img-src 'self' data:; font-src 'self'; base-uri 'none'; form-action 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site_name}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<link rel="alternate" type="application/atom+xml" title="{feed_title}" href="{feed_url}">
<link rel="alternate" hreflang="tr" href="{alt_tr}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="x-default" href="{alt_x}">
<script type="application/ld+json">{jsonld}</script>
<link rel="stylesheet" href="{css}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 60'><path d='M43 12A22 22 0 1 0 51 30' fill='none' stroke='%23a8321f' stroke-width='6' stroke-linecap='round'/></svg>">
</head>
<body class="static">
<div class="wrap">
<header class="top">
<a class="logo" href="{home}">""" + ENSO + """<span>{site_name}</span></a>
<nav class="acts"><a class="lnk" href="{app}">{app_link}</a><a class="lnk" href="{other_lang}">{other_word}</a></nav>
</header>
"""

PAGE = HEAD + """<main class="catpage">
<p class="crumb"><a href="{hub}">{hub_name}</a></p>
<h1 class="ph">{h1}</h1>
<p class="lede">{intro}</p>
<p class="count">{count} {word_links}</p>
<div class="recs">
{items}
</div>
{also}<nav class="other"><h2 class="sh">{others_head}</h2><p>{others}</p></nav>
</main>
<footer>
{foot}
</footer>
</div>
</body>
</html>
"""


def _css_href(out_dir, L, sub=False):
    """sub: the page sits one folder below its language's root (k/yol/, k/en/tag/)."""
    h = hashlib.sha1(io.open(os.path.join(out_dir, 'style.css'), 'rb').read()).hexdigest()[:8]
    return ('../../' if L['dir'] else '../') + ('../' if sub else '') + 'style.css?v=' + h


def _og(out_dir, name):
    """A page's own social image (og/<name>.png, written by make_og.py) when it
    exists, else the site's. make_og.py needs Pillow and is run by hand, so a
    heading added since its last run falls back rather than pointing nowhere."""
    if os.path.exists(os.path.join(out_dir, 'og', name + '.png')):
        return '%s/og/%s.png' % (SITE, name)
    return SITE + '/og.png'


def _code(t):
    # app.js descHTML() ile ayni: `kod` parcalari <code> olarak.
    return re.sub(r'`([^`<>]+)`', r'<code>\1</code>', t)


def _anchors(rows):
    """Each entry's id on its category page, from its URL key -- the key the
    app's ?e= permalink uses: letters and digits kept, every other run one
    hyphen (python.swaroopch.com -> python-swaroopch-com). It follows the
    URL, not the name, so renaming an entry keeps its links. A clash on the
    same page gets -2, -3 in list order."""
    seen, out = set(), []
    for _, d in rows:
        base = re.sub(r'[^a-z0-9]+', '-', url_key(d['url'])).strip('-') or 'e'
        a, n = base, 1
        while a in seen:
            n += 1
            a = '%s-%d' % (base, n)
        seen.add(a)
        out.append(a)
    return out


def _jsonld(title, canon, rows, L, ids):
    """ItemList: a crawler sees the list as a list rather than as prose.

    The static pages already carry the text, but nothing told a machine what
    the structure was -- this is what separates a section of a directory from
    an arbitrary article.
    """
    # All-in-one-page list: each item's url is its anchor on this page; the
    # site it describes sits in "item".
    ogeler = []
    for i, ((_, d), a) in enumerate(zip(rows, ids), 1):
        ogeler.append(
            '{"@type":"ListItem","position":%d,"url":%s,"name":%s,'
            '"item":{"@type":"WebSite","name":%s,"url":%s}}'
            % (i, json.dumps(canon + '#' + a), json.dumps(d['name'], ensure_ascii=False),
               json.dumps(d['name'], ensure_ascii=False), json.dumps(d['url'], ensure_ascii=False)))
    return ('{"@context":"https://schema.org","@type":"ItemList",'
            '"name":%s,"url":%s,"inLanguage":"%s","numberOfItems":%d,'
            '"itemListOrder":"https://schema.org/ItemListOrderAscending",'
            '"itemListElement":[%s]}'
            % (json.dumps(title, ensure_ascii=False),
               json.dumps(canon, ensure_ascii=False), L['code'],
               len(rows), ','.join(ogeler)))


HUB = HEAD + """<main class="fieldpage">
<h1 class="ph">{h1}</h1>
<p class="lede">{intro}</p>
<p class="count">{count} {word_links} · {ncat} {word_cats}</p>
<ol class="toc">
{items}
</ol>
{extra}</main>
<footer>
{foot}
</footer>
</div>
</body>
</html>
"""


def _host(u):
    h = u.split('//', 1)[-1].split('/', 1)[0]
    return h[4:] if h.startswith('www.') else h


def _item(d, taglbl, desc, li, n, aid):
    tags = ' · '.join(taglbl.get(t, [t, t])[li] for t in d.get('tags', [])[:6])
    return (
        '<article class="rec" id="%s"><span class="no">%d</span><div class="rb">\n'
        '<div class="nm"><a class="name" href="%s" rel="noopener noreferrer nofollow">%s</a>'
        '<span class="host">%s</span></div>\n'
        '<p class="desc">%s</p>\n'
        '%s'
        '</div></article>'
    ) % (esc(aid), n, esc(d['url']), esc(d['name']), esc(_host(d['url'])), _code(esc(desc)),
         ('<div class="mt"><span class="itags">%s</span></div>\n' % esc(tags)) if tags else '')


# Turkish and English differ only in the words around the list, so the two
# runs share everything except this table. A crawler arriving from an English
# query used to land on a Turkish page; hreflang now pairs them up.
LANGS = {
    'tr': {
        'code': 'tr', 'li': 0, 'ci': 1, 'dir': '', 'fonts': '../fonts',
        'hub_name': 'Fihrist', 'others_head': 'Diğer başlıklar', 'other_word': 'English',
        'name': 'Kullanışlı Siteler', 'links': 'bağlantı', 'cats': 'başlık',
        'app_link': '← Aranabilir sürüme dön',
        'feed_word': 'akış', 'feed_tip': 'Bu başlığın Atom akışı',
        'hub_desc': ('Yazılımdan yapay zekaya, güvenlikten ekonomiye ve mimariye '
                     'on alanda elle derlenmiş, açıklamalı bağlantı dizini. Her '
                     'kayıtta ne işe yaradığı ve benzerlerinden nerede ayrıldığı yazılı.'),
        'hub_foot': ('Bu sayfa dizinin metin hâli. Arama, etiket süzgeci ve '
                     'sıralama için aranabilir sürümü kullan.'),
        'foot': ('Bu sayfa dizinin {t} bölümünün metin hâli. Arama, etiket süzgeci '
                 've İngilizce açıklamalar için <a href="{s}/?cat={k}&amp;lang=tr">dizine dön</a>. '
                 '<a href="{s}/k/en/{k}.html">In English</a>'),
        'pdir': 'yol', 'tdir': 't', 'also_head': 'Ayrıca bak',
        'paths_head': 'Öğrenme yolları', 'tags_head': 'Etiketler', 'other_tags': 'Diğer etiketler',
        'steps': 'adım', 'npaths': 'yol', 'tag_word': 'etiket',
        'paths_desc': ('Bir alana nereden başlanır, sonra ne gelir: dizindeki kayıtlardan elle '
                       'sıralanmış sekiz yol. Her adımda neden o noktada geldiği yazılı.'),
        'path_foot': ('Her adım dizindeki bir kayda bağlı; açıklamanın tamamı ve benzerleri '
                      'başlık sayfasında.'),
        'tag_foot': ('Bu sayfa dizinin {t} etiketli kayıtlarının metin hâli. Süzgeçleri birleştirmek '
                     've aramak için <a href="{s}/?tag={q}&amp;lang=tr">dizine dön</a>.'),
    },
    'en': {
        'code': 'en', 'li': 1, 'ci': 2, 'dir': 'en/', 'fonts': '../../fonts',
        'hub_name': 'Index', 'others_head': 'Other headings', 'other_word': 'Türkçe',
        'name': 'Useful Sites', 'links': 'links', 'cats': 'headings',
        'app_link': '← Back to the searchable version',
        'feed_word': 'feed', 'feed_tip': 'Atom feed for this heading',
        'hub_desc': ('A hand-curated, annotated link directory across ten areas, '
                     'from software and AI to security, economics and architecture. '
                     'Every entry states what the resource does and where it parts '
                     'ways with its neighbours.'),
        'hub_foot': ('The plain-text edition of the directory. For search, tag '
                     'filtering and sorting, use the searchable version.'),
        'foot': ('The plain-text edition of the {t} section. For search, tag '
                 'filtering and Turkish descriptions, <a href="{s}/?cat={k}">go to '
                 'the directory</a>. <a href="{s}/k/{k}.html">Türkçe</a>'),
        'pdir': 'path', 'tdir': 'tag', 'also_head': 'Also see',
        'paths_head': 'Learning paths', 'tags_head': 'Tags', 'other_tags': 'Other tags',
        'steps': 'steps', 'npaths': 'paths', 'tag_word': 'tag',
        'paths_desc': ('Where to start in a field and what comes next: eight routes put in order by '
                       'hand from entries in the directory, each step saying why it comes where it does.'),
        'path_foot': ('Every step links to an entry in the directory; its full description and its '
                      'neighbours are on the heading page.'),
        'tag_foot': ('The plain-text edition of the entries tagged {t}. To combine filters and search, '
                     '<a href="{s}/?tag={q}">go to the directory</a>.'),
    },
}


def _intro_links(text, core, yer):
    """The intro, escaped, with the records it names linked to their place on
    the static pages -- the same rule as app.js introHTML(): longer names
    first, each name once and at a word boundary, names under four letters
    left alone."""
    s, links = esc(text), []
    for d in sorted((d for d in core if len(d['name']) >= 4 and d['url'] in yer),
                    key=lambda d: -len(esc(d['name']))):
        m = re.search(r'(?<![\w\x00])%s(?![\w\x01])' % re.escape(esc(d['name'])), s)
        if not m:
            continue
        links.append('<a href="%s">%s</a>' % (esc(yer[d['url']]), esc(d['name'])))
        s = s[:m.start()] + '\x00%d\x01' % (len(links) - 1) + s[m.end():]
    return re.sub(r'\x00(\d+)\x01', lambda m: links[int(m.group(1))], s)


def write_all(core, cats, intros, taglbl, out_dir, en_desc):
    """core: the record list as written to links.js. cats: [(key, tr, en)].

    en_desc is the parallel list of English descriptions, so the English pages
    carry English text rather than the Turkish original with an English shell.
    """
    written = []
    near = also_see(core, cats)
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
        # Every entry's place on the static pages, so an intro can link the
        # records it names (same folder: diller.html#python-swaroopch-com).
        yer = {}
        for k, rows in by_cat.items():
            for (_, d), a in zip(rows, _anchors(rows)):
                yer[d['url']] = '%s.html#%s' % (k, a)

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
            items, ids = [], _anchors(rows)
            for n, (i, d) in enumerate(rows, 1):
                text = en_desc[i] if L['li'] == 1 and i < len(en_desc) else d['tr']
                items.append(_item(d, taglbl, text, L['li'], n, ids[n - 1]))
            io.open(os.path.join(kdir, k + '.html'), 'w',
                    encoding='utf-8', newline='\n').write(PAGE.format(
                        lang=L['code'], site_name=esc(L['name']),
                        title=esc('%s — %s' % (label[k], L['name'])), h1=esc(label[k]),
                        desc=esc(desc), canon=canon, site=SITE,
                        home=SITE + ('/?lang=en' if L['li'] else '/?lang=tr'),
                        app='%s/?cat=%s&amp;lang=%s' % (SITE, esc(k), 'en' if L['li'] else 'tr'),
                        app_link=esc(L['app_link']),
                        other_lang='%s/k/%s%s.html' % (SITE, '' if L['li'] else 'en/', esc(k)),
                        other_word=esc(L['other_word']),
                        hub='index.html', hub_name=esc(L['hub_name']),
                        intro=_intro_links(intro, core, yer), css=_css_href(out_dir, L),
                        count=len(rows), word_links=esc(L['links']),
                        feed_title=esc('%s — %s' % (label[k], L['name'])),
                        feed_url='%s/feed/%s%s.xml' % (SITE, L['dir'], k),
                        alt_tr='%s/k/%s.html' % (SITE, k),
                        alt_en='%s/k/en/%s.html' % (SITE, k),
                        alt_x='%s/k/%s.html' % (SITE, k),
                        items='\n'.join(items), others=others,
                        others_head=esc(L['others_head']),
                        also=_also_html(near.get(k), label, L),
                        og_image=_og(out_dir, k),
                        jsonld=_jsonld(label[k], canon, rows, L, ids),
                        foot=L['foot'].format(t=esc(label[k]), s=SITE, k=esc(k))))
            if lang == 'tr':
                written.append(k)

    tags = tag_hubs(core)
    extra = _paths(core, cats, en_desc, out_dir) + _tag_pages(core, tags, taglbl, en_desc, out_dir)
    _hubs(core, cats, intros, out_dir, tags, taglbl)
    _cat_feeds(core, cats, en_desc, out_dir)
    _sitemap(written, core, out_dir, extra)
    _robots(out_dir)
    _feed(core, dict((c[0], c[1]) for c in cats), out_dir)
    _credits(core, out_dir)
    return written + [tr for tr, _ in extra]


# ------------------------------------------------------------------ also see
# Each heading page ends with "Other headings": all 47 others, in field order,
# which is a table of contents rather than a suggestion. "Also see" is the
# suggestion: the three headings whose records are tagged most alike (cosine
# similarity of the per-heading tag counts, price tags left out because every
# heading has them in the same proportions), then the headings its curated
# comparisons (vs) reach into. Similarities are rounded before sorting and ties
# break on the key, so the order cannot wobble between machines.
COST = ('ücretsiz', 'freemium', 'ücretli')
ALSO_N, ALSO_VS = 3, 3


def also_see(core, cats):
    import math
    prof = {}
    for d in core:
        p = prof.setdefault(d['cat'], {})
        for t in d['tags']:
            if t not in COST:
                p[t] = p.get(t, 0) + 1
    norm = {k: math.sqrt(sum(v * v for v in p.values())) for k, p in prof.items()}
    vs = {}
    for d in core:
        for j, _ in d.get('vs', []):
            o = core[j]['cat']
            if o != d['cat']:
                for a, b in ((d['cat'], o), (o, d['cat'])):
                    vs.setdefault(a, {})
                    vs[a][b] = vs[a].get(b, 0) + 1
    out = {}
    for k in (c[0] for c in cats):
        if k not in prof:
            continue
        sims = []
        for o, p in prof.items():
            if o == k or not norm[k] or not norm[o]:
                continue
            dot = sum(n * p.get(t, 0) for t, n in prof[k].items())
            sims.append((-round(dot / (norm[k] * norm[o]), 9), o))
        top = [o for _, o in sorted(sims)[:ALSO_N]]
        more = [o for n, o in sorted((-n, o) for o, n in vs.get(k, {}).items()) if o not in top]
        out[k] = top + more[:ALSO_VS]
    return out


def _also_html(keys, label, L):
    if not keys:
        return ''
    return ('<nav class="other"><h2 class="sh">%s</h2><p>%s</p></nav>\n'
            % (esc(L['also_head']), ' '.join('<a href="%s.html">%s</a>' % (esc(o), esc(label[o]))
                                             for o in keys)))


# ------------------------------------------------------------------ shared bits
def _places(core):
    """Every entry's place on its heading page: url -> (cat, anchor)."""
    by_cat, yer = {}, {}
    for d in core:
        by_cat.setdefault(d['cat'], []).append((0, d))
    for k, rows in by_cat.items():
        for (_, d), a in zip(rows, _anchors(rows)):
            yer[d['url']] = (k, a)
    return yer


def _sub_page(L, out_dir, path_tr, path_en, **kw):
    """The fields every page one folder below k/ or k/en/ shares."""
    tr, en = '%s/k/%s' % (SITE, path_tr), '%s/k/en/%s' % (SITE, path_en)
    base = dict(lang=L['code'], site_name=esc(L['name']), site=SITE,
                canon=en if L['li'] else tr, css=_css_href(out_dir, L, sub=True),
                home=SITE + ('/?lang=en' if L['li'] else '/?lang=tr'),
                app_link=esc(L['app_link']),
                other_lang=tr if L['li'] else en, other_word=esc(L['other_word']),
                feed_title=esc(L['name']), feed_url='%s/feed.xml' % SITE,
                alt_tr=tr, alt_en=en, alt_x=tr, hub_name=esc(L['hub_name']),
                og_image=SITE + '/og.png', also='')
    base.update(kw)
    return base


def _dir(out_dir, L, sub):
    d = os.path.join(out_dir, 'k', *([L['dir'].strip('/')] if L['dir'] else []) + [sub])
    if not os.path.isdir(d):
        os.makedirs(d)
    return d


def _write(out_dir, L, sub, name, html):
    io.open(os.path.join(_dir(out_dir, L, sub), name), 'w', encoding='utf-8', newline='\n').write(html)


def _prune(out_dir, L, sub, keep):
    """A tag that drops below the threshold, or a renamed path, would leave its
    old page behind: still committed, still served, linked from nowhere."""
    d = _dir(out_dir, L, sub)
    for f in sorted(os.listdir(d)):
        if f.endswith('.html') and f not in keep:
            os.remove(os.path.join(d, f))


# ------------------------------------------------------------------ goal paths
PATH_PAGE = HEAD + """<main class="catpage">
<p class="crumb"><a href="../index.html">{hub_name}</a><b>/</b><a href="index.html">{paths_head}</a></p>
<h1 class="ph">{h1}</h1>
<p class="lede">{intro}</p>
<p class="count">{count} {word_links}</p>
<div class="recs">
{items}
</div>
<nav class="other"><h2 class="sh">{others_head}</h2><p>{others}</p></nav>
</main>
<footer>
{foot}
</footer>
</div>
</body>
</html>
"""


def _paths(core, cats, en_desc, out_dir):
    """The goal paths of data/paths.py, one page each plus an index per
    language. Returns the sitemap pairs (tr url, en url)."""
    from paths import PATHS
    byurl = {url_key(d['url']): (i, d) for i, d in enumerate(core)}
    yer = _places(core)
    pairs = [('%s/k/yol/index.html' % SITE, '%s/k/en/path/index.html' % SITE)]
    for lang, L in sorted(LANGS.items()):
        li = L['li']
        label = dict((c[0], c[L['ci']]) for c in cats)
        slug = 'en_slug' if li else 'tr_slug'
        toc = []
        for p in PATHS:
            rows, why = [], []
            for u, w_tr, w_en in p['steps']:
                i, d = byurl[url_key(u)]
                rows.append((i, d))
                why.append(w_en if li else w_tr)
            ids = _anchors(rows)
            items = []
            for n, ((i, d), a, w) in enumerate(zip(rows, ids, why), 1):
                k, ca = yer[d['url']]
                items.append(
                    '<article class="rec" id="%s"><span class="no">%d</span><div class="rb">\n'
                    '<p class="path"><a href="../%s.html#%s">%s</a></p>\n'
                    '<div class="nm"><a class="name" href="%s" rel="noopener noreferrer nofollow">%s</a>'
                    '<span class="host">%s</span></div>\n'
                    '<p class="desc">%s</p>\n'
                    '</div></article>'
                    % (esc(a), n, esc(k), esc(ca), esc(label[k]), esc(d['url']), esc(d['name']),
                       esc(_host(d['url'])), esc(w)))
            title = p[L['code']]
            path_tr, path_en = 'yol/%s.html' % p['tr_slug'], 'path/%s.html' % p['en_slug']
            kw = _sub_page(L, out_dir, path_tr, path_en)
            others = ' '.join('<a href="%s.html">%s</a>' % (esc(o[slug]), esc(o[L['code']]))
                              for o in PATHS if o is not p)
            _write(out_dir, L, L['pdir'], p[slug] + '.html', PATH_PAGE.format(
                title=esc('%s — %s' % (title, L['paths_head'])), h1=esc(title),
                desc=esc(p['intro'][li][:180]), intro=esc(p['intro'][li]),
                app=kw['home'], paths_head=esc(L['paths_head']),
                count=len(rows), word_links=esc(L['steps']), items='\n'.join(items),
                others_head=esc(L['paths_head']), others=others,
                foot=esc(L['path_foot']),
                jsonld=_jsonld(title, kw['canon'], rows, L, ids),
                **dict(kw, og_image=_og(out_dir, 'path-' + p['en_slug']))))
            toc.append('<li><a class="tt" href="%s.html"><span class="tn">%s</span><span class="ld"></span>'
                       '<span class="n">%d</span></a><p class="td">%s</p></li>'
                       % (esc(p[slug]), esc(title), len(rows), esc(p['intro'][li])))
            if lang == 'tr':
                pairs.append(('%s/k/%s' % (SITE, path_tr), '%s/k/en/%s' % (SITE, path_en)))
        kw = _sub_page(L, out_dir, 'yol/index.html', 'path/index.html')
        ogeler = ','.join('{"@type":"ListItem","position":%d,"url":%s,"name":%s}'
                          % (n, json.dumps('%s/k/%s%s/%s.html' % (SITE, L['dir'], L['pdir'], p[slug])),
                             json.dumps(p[L['code']], ensure_ascii=False))
                          for n, p in enumerate(PATHS, 1))
        _write(out_dir, L, L['pdir'], 'index.html', HUB.replace(
            '<main class="fieldpage">',
            '<main class="fieldpage">\n<p class="crumb"><a href="../index.html">{hub_name}</a></p>').format(
            title=esc('%s — %s' % (L['paths_head'], L['name'])), h1=esc(L['paths_head']),
            desc=esc(L['paths_desc'][:180]), intro=esc(L['paths_desc']), app=kw['home'],
            count=sum(len(p['steps']) for p in PATHS), word_links=esc(L['steps']),
            ncat=len(PATHS), word_cats=esc(L['npaths']), items='\n'.join(toc), extra='',
            foot=esc(L['path_foot']),
            jsonld=('{"@context":"https://schema.org","@type":"CollectionPage","name":%s,"url":%s,'
                    '"inLanguage":"%s","mainEntity":{"@type":"ItemList","numberOfItems":%d,'
                    '"itemListElement":[%s]}}'
                    % (json.dumps(L['paths_head'], ensure_ascii=False), json.dumps(kw['canon']),
                       L['code'], len(PATHS), ogeler)),
            **kw))
        _prune(out_dir, L, L['pdir'], {p[slug] + '.html' for p in PATHS} | {'index.html'})
    return pairs


# ------------------------------------------------------------------ tag hubs
def tag_hubs(core):
    """[(tag, slug, count)] for every tag that gets a page, in canonical order."""
    from taghubs import MIN_N, SKIP, slug
    from tags import CANON
    n = {}
    for d in core:
        for t in d['tags']:
            n[t] = n.get(t, 0) + 1
    return [(t, slug(t), n[t]) for t in CANON if t not in SKIP and n.get(t, 0) >= MIN_N]


def _tag_pages(core, tags, taglbl, en_desc, out_dir):
    from urllib.parse import quote
    from taghubs import INTROS
    pairs = []
    for lang, L in sorted(LANGS.items()):
        li = L['li']
        for t, s, _ in tags:
            rows = [(i, d) for i, d in enumerate(core) if t in d['tags']]
            ids = _anchors(rows)
            items = [_item(d, taglbl, en_desc[i] if li and i < len(en_desc) else d['tr'], li, n, a)
                     for n, ((i, d), a) in enumerate(zip(rows, ids), 1)]
            name = taglbl[t][li]
            intro = INTROS[t][li]
            kw = _sub_page(L, out_dir, 't/%s.html' % s, 'tag/%s.html' % s)
            q = esc(quote(t, safe=''))
            _write(out_dir, L, L['tdir'], s + '.html', PAGE.format(
                title=esc('%s · %s — %s' % (name, L['tag_word'].capitalize(), L['name'])),
                h1=esc(name), desc=esc(intro[:180]), intro=esc(intro),
                app='%s/?tag=%s&amp;lang=%s' % (SITE, q, L['code']),
                hub='../index.html', count=len(rows), word_links=esc(L['links']),
                items='\n'.join(items), others_head=esc(L['other_tags']),
                others=' '.join('<a href="%s.html">%s</a>' % (esc(o), esc(taglbl[ot][li]))
                                for ot, o, _ in tags if ot != t),
                foot=L['tag_foot'].format(t=esc(name), s=SITE, q=q),
                jsonld=_jsonld(name, kw['canon'], rows, L, ids), **kw))
            if lang == 'tr':
                pairs.append(('%s/k/t/%s.html' % (SITE, s), '%s/k/en/tag/%s.html' % (SITE, s)))
        _prune(out_dir, L, L['tdir'], {s + '.html' for _, s, _ in tags})
    return pairs


# key, tr label, en label, tr note, en note, url  -- driven by data/sources.py
CREDITS_TX = {
    'tr': {
        'title': 'Katkıda Bulunanlar',
        'intro': ('Dizindeki bağlantılar iki kaynaktan gelir: derleyenin kendi arşivi ve aşağıdaki '
                  'herkese açık koleksiyonlar. Her koleksiyondan yalnız kapsam içi, canlı ve kayda değer '
                  'olanlar alındı; açıklamalar kopyalanmadı, projelerin kendi belgelerine bakılarak '
                  'yeniden yazıldı. Emeği geçen herkese teşekkürler.'),
        'own': 'Derleyenin kendi arşivi — tek tek gözden geçirildi.',
        'links': 'bağlantı',
        'chow': 'Sen de katkıda bulun',
        'ctext': ('Ölü ya da hatalı bir kayıt görürsen, ya da yeni bir bağlantı önermek istersen, '
                  'GitHub üzerinden bir <a href="{repo}/issues/new/choose">issue aç</a>. Öneriler '
                  'yayımlanmadan önce elle gözden geçirilir.'),
        'back': '← Kullanışlı Siteler',
    },
    'en': {
        'title': 'Contributors & Credits',
        'intro': ("The directory's links come from two places: the curator's own archive and the "
                  'public collections below. From each collection only the in-scope, live and '
                  'worthwhile entries were taken; the descriptions were not copied but rewritten from '
                  "each project's own documentation. Thanks to everyone whose work fed this."),
        'own': "The curator's own archive — reviewed one by one.",
        'links': 'links',
        'chow': 'Contribute',
        'ctext': ('Spotted a dead or wrong entry, or want to suggest a new link? Open an '
                  '<a href="{repo}/issues/new/choose">issue on GitHub</a>. Suggestions are reviewed '
                  'by hand before they are published.'),
        'back': '← Useful Sites',
    },
}


def _credits(core, out_dir):
    """A standing credits page naming every source that fed the directory.

    Built from data/sources.py so it can never drift from the source chips in
    the app: same labels, same notes, plus the count and a link out.
    """
    count = {}
    for d in core:
        count[d.get('src')] = count.get(d.get('src'), 0) + 1
    order = sorted(SOURCES, key=lambda k: (k != 'kedi', -count.get(k, 0)))
    repo = 'https://github.com/latifkedi/useful-sites'

    for lang, L in sorted(LANGS.items()):
        T = CREDITS_TX[lang]
        rows = []
        for k in order:
            s = SOURCES[k]
            n = count.get(k, 0)
            if not n:
                continue
            name = s['label_tr'] if lang == 'tr' else s['label_en']
            note = (s['note_tr'] if lang == 'tr' else s['note_en']) if k != 'kedi' else T['own']
            url = s.get('url')
            head = ('<a class="name" href="%s" rel="noopener noreferrer">%s</a>' % (esc(url), esc(name))) \
                if url else ('<span class="name">%s</span>' % esc(name))
            rows.append(
                '<article class="rec"><span class="no">%d</span><div class="rb">'
                '<div class="nm">%s<span class="host">%d %s</span></div>'
                '<p class="desc">%s</p></div></article>'
                % (len(rows) + 1, head, n, esc(T['links']), esc(note)))
        canon = '%s/k/%s%s' % (SITE, L['dir'], 'tesekkur.html' if lang == 'tr' else 'credits.html')
        alt_tr = '%s/k/tesekkur.html' % SITE
        alt_en = '%s/k/en/credits.html' % SITE
        html = PAGE.format(
            lang=L['code'], site_name=esc(L['name']),
            title=esc('%s — %s' % (T['title'], L['name'])), h1=esc(T['title']),
            desc=esc(T['intro'][:180]), canon=canon, site=SITE,
            home=SITE + ('/?lang=tr' if lang == 'tr' else '/?lang=en'),
            app=SITE + ('/?lang=tr' if lang == 'tr' else '/?lang=en'), app_link=esc(L['app_link']),
            other_lang=alt_en if lang == 'tr' else alt_tr, other_word=esc(L['other_word']),
            hub='index.html', hub_name=esc(L['hub_name']),
            intro=T['intro'], css=_css_href(out_dir, L),
            count=len([1 for k in order if count.get(k)]),
            word_links=esc('kaynak' if lang == 'tr' else 'sources'),
            feed_title=esc(L['name']), feed_url='%s/feed.xml' % SITE,
            alt_tr=alt_tr, alt_en=alt_en, alt_x=alt_tr, also='', og_image=SITE + '/og.png',
            jsonld=json.dumps({'@context': 'https://schema.org', '@type': 'AboutPage',
                               'name': T['title'], 'url': canon}, ensure_ascii=False),
            items='\n'.join(rows)
            + '\n<article class="rec"><span class="no"></span><div class="rb"><div class="nm">'
              '<span class="name">%s</span></div><p class="desc">%s</p></div></article>'
              % (esc(T['chow']), T['ctext'].format(repo=repo)),
            others_head=esc(L['name']), others='<a href="%s">%s</a>' % (esc(SITE + ('/?lang=tr' if lang == 'tr' else '/?lang=en')), esc(T['back'])),
            foot=('<a href="%s">%s</a>' % (esc(SITE + ('/?lang=tr' if lang == 'tr' else '/?lang=en')),
                                           esc(T['back']))))
        fn = 'tesekkur.html' if lang == 'tr' else 'credits.html'
        kdir = os.path.join(out_dir, 'k') if lang == 'tr' else os.path.join(out_dir, 'k', 'en')
        io.open(os.path.join(kdir, fn), 'w', encoding='utf-8', newline='\n').write(html)


def _hubs(core, cats, intros, out_dir, tags, taglbl):
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
                '<li><a class="tt" href="%s.html"><span class="tn">%s</span><span class="ld"></span>'
                '<span class="n">%d</span></a><p class="td">%s</p>'
                '<p class="ts"><a href="../feed/%s%s.xml" title="%s">%s</a></p></li>'
                % (esc(k), esc(label[k]), say[k], esc(intro), esc(L['dir']), esc(k),
                   esc(L['feed_tip']), esc(L['feed_word'])))
            # k/en/index.html iki kat derinde: akis adresi ../../feed/en/ olmali
            # (onceden ../feed/en/ yaziliyordu ve /k/feed/en/'e, olmayan bir yere cikiyordu).
            if L['dir']:
                satir[-1] = satir[-1].replace('href="../feed/', 'href="../../feed/', 1)
        canon = '%s/k/%sindex.html' % (SITE, L['dir'])
        # The ways in that are not headings: the goal paths and the tag pages.
        from paths import PATHS
        slug = 'en_slug' if L['li'] else 'tr_slug'
        extra = ('<nav class="other"><h2 class="sh">%s</h2><p>%s</p></nav>\n'
                 '<nav class="other"><h2 class="sh">%s</h2><p>%s</p></nav>\n'
                 % (esc(L['paths_head']),
                    ' '.join('<a href="%s/%s.html">%s</a>' % (L['pdir'], esc(p[slug]), esc(p[L['code']]))
                             for p in PATHS),
                    esc(L['tags_head']),
                    ' '.join('<a href="%s/%s.html">%s</a>' % (L['tdir'], esc(s), esc(taglbl[t][L['li']]))
                             for t, s, _ in tags)))
        io.open(os.path.join(out_dir, 'k', L['dir'].strip('/'), 'index.html')
                if L['dir'] else os.path.join(out_dir, 'k', 'index.html'),
                'w', encoding='utf-8', newline='\n').write(HUB.format(
                    lang=L['code'], site_name=esc(L['name']), title=esc(L['name']), h1=esc(L['name']),
                    desc=esc(L['hub_desc']), intro=esc(L['hub_desc']),
                    canon=canon, site=SITE, css=_css_href(out_dir, L),
                    home=SITE + ('/?lang=en' if L['li'] else '/?lang=tr'),
                    app=SITE + ('/?lang=en' if L['li'] else '/?lang=tr'),
                    app_link=esc(L['app_link']),
                    other_lang='%s/k/%sindex.html' % (SITE, '' if L['li'] else 'en/'),
                    other_word=esc(L['other_word']),
                    feed_title=esc(L['name']), feed_url='%s/feed.xml' % SITE,
                    alt_tr='%s/k/index.html' % SITE, alt_en='%s/k/en/index.html' % SITE,
                    alt_x=SITE + '/',
                    count=len(core), ncat=len(satir), word_links=esc(L['links']),
                    word_cats=esc(L['cats']), items='\n'.join(satir), foot=esc(L['hub_foot']),
                    extra=extra, og_image=SITE + '/og.png',
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


def _sitemap(keys, core, out_dir, extra=()):
    """Site haritasi, dil ciftlerini de bildiriyor.

    hreflang zaten sayfalarin kendisinde var ve tek basina yeterli; burada
    tekrar edilmesinin sebebi Google'in ikisini capraz dogrulamasi -- eksik
    ya da asimetrik bir eslesme boylece daha erken goruluyor.

    <lastmod> saatten degil, en yeni kaydin eklenme tarihinden gelir. Saati
    kullanmak her build'i farkli bir gunde farkli bir sitemap.xml uretmeye
    itiyordu; CI'in "committed cikti taze build ile ayni" kontrolu de bu
    yuzden patliyordu.
    """
    today = _day(max((d.get('added', 0) for d in core), default=0))
    ciftler = [('%s/k/%s.html' % (SITE, k), '%s/k/en/%s.html' % (SITE, k))
               for k in keys]
    ciftler.insert(0, ('%s/k/index.html' % SITE, '%s/k/en/index.html' % SITE))
    ciftler.append(('%s/k/tesekkur.html' % SITE, '%s/k/en/credits.html' % SITE))
    ciftler.extend(extra)          # goal paths and tag pages

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
             '<subtitle>On alanda elle derlenmiş, açıklamalı bağlantı '
             'dizini</subtitle>',
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


# ------------------------------------------------------------------ issue form
# The "Suggest a link" form had its own hand-kept category list. It drifted:
# twelve categories added later were missing, and one it did have no longer
# matched ("AI · Agents, RAG & Infra"). The site's submit dialog preselects the
# category by its English label, and GitHub silently ignores a value that is
# not among the options -- so the choice was lost for a third of the directory.
# The options are rewritten from notes.CATS on every build now.
ISSUE_FORM = os.path.join('.github', 'ISSUE_TEMPLATE', 'new-link.yml')


def write_issue_form(cats, out_dir):
    path = os.path.join(out_dir, ISSUE_FORM)
    if not os.path.exists(path):
        return None
    src = io.open(path, encoding='utf-8').read()
    lines = src.split('\n')
    try:
        i = lines.index('    id: cat')
        o = next(n for n in range(i, len(lines)) if lines[n].strip() == 'options:')
        v = next(n for n in range(o + 1, len(lines)) if not lines[n].startswith('        - '))
    except (ValueError, StopIteration):
        raise ValueError('%s: could not find the category options block' % ISSUE_FORM)
    opts = ['        - ' + json.dumps(c[2], ensure_ascii=False) for c in cats]
    opts.append('        - "Not sure"')
    out = '\n'.join(lines[:o + 1] + opts + lines[v:])
    if out != src:
        io.open(path, 'w', encoding='utf-8', newline='\n').write(out)
    return path


# ------------------------------------------------------------------ homepage
# The homepage used to be empty until links.js (190 KB gzipped) had downloaded
# and run: nothing to read on a slow connection for seconds. Its content is
# now written into index.html at build time -- the same markup homeHTML()
# produces for English, the default language, from the same data -- so the
# first paint already shows the ten fields. app.js leaves this block in place
# on its first render (data-pre); re-rendering identical markup would replay
# the fade-in. These strings mirror app.js T.en; test_build checks they have
# not drifted.
HOME_TX = {
    'hero': ('<em>%s</em> links, picked by hand. Each one says where it parts '
             'ways with its neighbours.'),
    'hStart': 'Start Here',
    'fxHead': 'Index',
    'fxNote': '%d areas, %d headings',
    'recent': 'Recently Added',
    'hAll': 'See everything in one list →',
    'proof': ('%s links · last checked %s · %s flagged archived or dormant · '
              'no trackers · works offline'),
    'tryLbl': 'Try:',
}
# app.js T.en.tryQs: example queries under the hero, each one runs a search.
HOME_TRY = ['llm', 'postgres', 'regex', 'self-hosted', 'diagram', 'color palette']
# app.js AYLAR.en, for the proof line's date (fmtDay: '12 Oct 2026').
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def _day_label(iso):
    return '%d %s %s' % (int(iso[8:10]), MONTHS[int(iso[5:7]) - 1], iso[:4]) if iso else ''

# app.js ROMAN ile ayni: alan numaralari GROUPS sirasindaki yerleri.
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']


def _first(t):
    # app.js firstSentence(): the first sentence of 40-150 characters, or
    # else 120 characters cut at a word, with an ellipsis.
    t = t or ''
    m = re.match(r'^(.{40,150}?[.!?])(\s|$)', t)
    if m:
        return m.group(1)
    if len(t) <= 120:
        return t
    cut = t[:120]
    sp = cut.rfind(' ')
    return re.sub(r'[\s,;:—–-]+$', '', cut[:sp] if sp > 60 else cut) + '…'


def _short(label):
    # app.js shortCat(): alanin icinde 'YZ · Modeller' yerine 'Modeller'.
    return re.sub(r'^\S{1,3} · ', '', label)


def home_html(core, cats, groups, en):
    from urllib.parse import quote   # encodeURIComponent's safe set, below
    bycat = {}
    for d in core:
        bycat[d['cat']] = bycat.get(d['cat'], 0) + 1
    lbl = dict((c[0], c[2]) for c in cats)

    seen, strip = set(), []
    for i, d in enumerate(core):
        if d.get('pick') and d['cat'] not in seen and len(strip) < 6:
            seen.add(d['cat'])
            strip.append((d, en[i]))

    fx, nf = [], 0
    for gi, g in enumerate(groups):
        full = [k for k in g['cats'] if bycat.get(k)]
        n = sum(bycat[k] for k in full)
        if not n:
            continue
        nf += 1
        link = ('href="?cat=%s" data-cat="%s"' % (esc(full[0]), esc(full[0])) if len(full) == 1
                else 'href="?f=%s" data-field="%s"' % (esc(g['key']), esc(g['key'])))
        fx.append('<li class="fe"><a class="ft" %s><span class="rn">%s</span>'
                  '<span class="fn">%s</span><span class="ld"></span><span class="n">%d</span></a>'
                  '<p class="fc">%s</p></li>'
                  % (link, ROMAN[gi], esc(g['en']), n, ', '.join(
                      '<a href="?cat=%s" data-cat="%s">%s</a>' % (esc(k), esc(k), esc(_short(lbl[k])))
                      for k in full)))

    # The proof line: live numbers, the same ones app.js homeHTML() counts.
    checked = max((d.get('ver') or '' for d in core), default='')
    proof = HOME_TX['proof'] % ('{:,}'.format(len(core)), _day_label(checked),
                                '{:,}'.format(sum(1 for d in core if d.get('hs'))))
    tryq = ''.join('<a class="chip" href="?q=%s" data-q="%s">%s</a>'
                   % (quote(q, safe="-_.!~*'()"), esc(q), esc(q)) for q in HOME_TRY)

    picks = ''
    if strip:
        picks = ('<section class="hsec hp"><h2 class="k">%s</h2><ol class="hpicks">%s</ol></section>'
                 % (esc(HOME_TX['hStart']), ''.join(
                     '<li><a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
                     '<p>%s</p></li>' % (esc(d['url']), esc(d['name']), esc(_first(e)))
                     for d, e in strip)))
    return ('<div class="home" data-pre="1">'
            '<p class="proof">%s</p><p class="tryq"><span>%s</span>%s</p>%s'
            '<section class="hsec"><h2 class="k">%s<span>%s</span></h2>'
            '<ol class="fx">%s</ol></section>'
            '<p class="hlinks"><a href="?new=1" data-recent="1">%s →</a>'
            '<a href="?sort=az" data-all="1">%s</a></p></div>'
            % (esc(proof), esc(HOME_TX['tryLbl']), tryq, picks,
               esc(HOME_TX['fxHead']), esc(HOME_TX['fxNote'] % (nf, len(bycat))),
               ''.join(fx), esc(HOME_TX['recent']), esc(HOME_TX['hAll'])))


def write_home(core, cats, groups, out_dir, en):
    path = os.path.join(out_dir, 'index.html')
    src = io.open(path, encoding='utf-8').read()
    out = re.sub(r'(<main id="list" tabindex="-1">)(.*?)(</main>)',
                 lambda m: m.group(1) + home_html(core, cats, groups, en) + m.group(3),
                 src, count=1, flags=re.S)
    # Giris cumlesi baslikta duruyor, <main>'de degil: arama kutusu onunla
    # icerik arasina girebilsin diye. Sayi her derlemede veriden yaziliyor.
    out = re.sub(r'(<h1 class="hero" id="hero">)(.*?)(</h1>)',
                 lambda m: m.group(1) + HOME_TX['hero'] % '{:,}'.format(len(core)) + m.group(3),
                 out, count=1, flags=re.S)
    if out != src:
        io.open(path, 'w', encoding='utf-8', newline='').write(out)
