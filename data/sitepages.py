# -*- coding: utf-8 -*-
"""The static pages that are about the directory rather than a slice of it.

emit.py writes the heading, path and tag pages; this writes, in both
languages, the pages a reader goes to when deciding whether to trust it:

  k/about.html, k/en/about.html          how it is made and kept, from ABOUT.tr.md / ABOUT.md
  k/changes.html, k/en/changes.html      what was removed and why, what arrived each month
  k/week/<YYYY-Www>.html, k/en/week/     one digest per recent week with additions
  feed/changes.xml, feed/en/changes.xml  those digests as Atom
  k/alt/<slug>.html, k/en/alt/           "X alternatives", from the curated vs comparisons
  k/t/index.html, k/en/tag/index.html    the tag pages, listed
  data/v1/links.json, data/v1/links.csv  the records as open data (see data/v1/SCHEMA.md)

Every date comes from the data (a record's "added", the last scan's date),
never from the clock, so two builds of the same data write the same bytes.
Only records whose note carries its own "added" count as dated additions: the
rest carry the date of their intake, which says when a batch arrived, not when
anything was decided about them.
"""
import collections
import csv
import datetime
import io
import json
import os
import re

import emit
from emit import SITE, LANGS, HEAD, esc, _css_href, _anchors, _places, _home, site_foot, trust
from emit import _item_short, _first, _host, _code, _day, _prune, newest, atom, REPO
from axes import AXES
from sources import SOURCES

D = os.path.dirname(os.path.abspath(__file__))

WEEKS = 12            # digest pages kept: the most recent weeks that had additions
WEEK_CAP = 250        # records listed on one digest page; the rest are counted
ALT_MIN = 3           # rivals an entry needs before it gets an alternatives page

MONTHS = {'tr': ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos',
                 'Eylül', 'Ekim', 'Kasım', 'Aralık'],
          'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                 'September', 'October', 'November', 'December']}

TX = {
    'tr': {
        'about': 'Hakkında ve yöntem',
        'about_lede': ('Dizinin nasıl derlendiği, nasıl denetlendiği, kayıtların nereden geldiği '
                       've hangi koşullarla kullanılabileceği.'),
        'src_head': 'Kaynaklar ve lisansları',
        'src_text': ('Her kayıt, onu dizine getiren kaynağı taşır. Kaynakların seçkileri kendi '
                     'lisanslarıyla kalır; açıklamalar burada yazıldı ve CC BY 4.0. '
                     'Ayrıntı <a href="{credits}">teşekkür sayfasında</a>.'),
        'data_head': 'Açık veri',
        'data_text': ('Kayıtların tamamı makinece okunur biçimde: <a href="{json}">links.json</a>, '
                      '<a href="{csv}">links.csv</a>, alanların tarifi <a href="{schema}">SCHEMA.md</a>. '
                      'Açıklamalar CC BY 4.0; kaynak seçkileri kendi lisanslarını korur.'),
        'more_head': 'Dizinde gezinmek',
        'alts_head': 'Alternatif sayfaları',
        'alts_text': ('Dizinde en az {n} rakibiyle karşılaştırılan kayıtlar için birer sayfa: '
                      'her rakip ve ayrıldığı tek nokta.'),
        'changes': 'Değişiklikler',
        'changes_lede': ('Dizinden bilerek çıkarılanlar ve gerekçeleri, son haftaların özetleri ve '
                         'kendi eklenme tarihini taşıyan kayıtların aylara göre dağılımı.'),
        'removed_head': 'Bilerek çıkarılanlar',
        'removed_note': 'Gerekçeler bakımcının notlarından, İngilizce.',
        'weeks_head': 'Son haftalar',
        'months_head': 'Aylara göre eklenenler',
        'months_note': ('Yalnız kendi eklenme tarihini taşıyan {n} kayıt sayıldı; toplu alımlardan '
                        'gelenler alımın tarihini taşıdığı için burada yok.'),
        'entries': 'kayıt', 'entry': 'kayıt',
        'week_title': '{y} yılı {w}. hafta',
        'week_lede': '{a} ile {b} arasında dizine eklenen {n} kayıt.',
        'week_more': 'Bu haftanın {n} kaydı daha var; başlık sayfalarında.',
        'prev': '← Önceki hafta', 'next': 'Sonraki hafta →',
        'feed_title': 'Kullanışlı Siteler — haftalık değişiklikler',
        'alt_title': '{x} alternatifleri',
        'alt_lede': ('Dizinde {x} ile doğrudan karşılaştırılan {n} kayıt ve her birinin ondan '
                     'ayrıldığı nokta.'),
        'alt_anchor': 'Karşılaştırılan',
        'differs': 'Ayrıldığı nokta',
        'tags_title': 'Etiketler',
        'tags_lede': ('En az {n} kayıtta geçen etiketlerin her birine bir sayfa: kaydın adı, ilk '
                      'cümlesi ve başlık sayfasındaki yeri.'),
        'ntags': 'etiket',
    },
    'en': {
        'about': 'About & methodology',
        'about_lede': ('How the directory is compiled and checked, where its entries come from, '
                       'and the terms under which it can be reused.'),
        'src_head': 'Sources and their licences',
        'src_text': ('Every entry carries the source that brought it in. A source\'s selection '
                     'keeps its own licence; the descriptions were written here and are CC BY 4.0. '
                     'Details on the <a href="{credits}">credits page</a>.'),
        'data_head': 'Open data',
        'data_text': ('Every record in machine-readable form: <a href="{json}">links.json</a>, '
                      '<a href="{csv}">links.csv</a>, with the fields described in '
                      '<a href="{schema}">SCHEMA.md</a>. The descriptions are CC BY 4.0; the '
                      'selections taken from other compilations keep their own licences.'),
        'more_head': 'Finding your way',
        'alts_head': 'Alternatives pages',
        'alts_text': ('One page for each entry that the directory compares with at least {n} '
                      'rivals: every rival, and the one thing on which it parts ways.'),
        'changes': 'Changes',
        'changes_lede': ('What was taken out on purpose and why, a digest of each recent week, '
                         'and the entries that carry their own arrival date, by month.'),
        'removed_head': 'Removed on purpose',
        'removed_note': 'Reasons as the maintainer recorded them.',
        'weeks_head': 'Recent weeks',
        'months_head': 'Additions by month',
        'months_note': ('Counts only the {n} entries that carry their own arrival date; those from '
                        'bulk intakes carry the intake\'s date and are left out.'),
        'entries': 'entries', 'entry': 'entry',
        'week_title': 'Week {w}, {y}',
        'week_lede': '{n} {e} added to the directory between {a} and {b}.',
        'week_more': '{n} more entries arrived this week; they are on their heading pages.',
        'prev': '← Previous week', 'next': 'Next week →',
        'feed_title': 'Useful Sites — weekly changes',
        'alt_title': '{x} alternatives',
        'alt_lede': ('The {n} entries in the directory that are compared directly with {x}, and '
                     'where each one parts ways with it.'),
        'alt_anchor': 'Compared with',
        'differs': 'Differs in',
        'tags_title': 'Tags',
        'tags_lede': ('One page for each tag on at least {n} entries: the entry\'s name, its first '
                      'sentence and its place on its heading page.'),
        'ntags': 'tags',
    },
}

TEXT = HEAD + """<main class="catpage prose">
<p class="crumb">{crumb}</p>
<h1 class="ph">{h1}</h1>
<p class="lede">{intro}</p>
{body}
</main>
<footer>
{foot}
</footer>
</div>
</body>
</html>
"""


def _kw(L, out_dir, tr, en, sub, **kw):
    """The HEAD fields of a page at k/<tr> and k/en/<en>."""
    trs, ens = '%s/k/%s' % (SITE, tr), '%s/k/en/%s' % (SITE, en)
    base = dict(lang=L['code'], site_name=esc(L['name']), canon=ens if L['li'] else trs,
                css=_css_href(out_dir, L, sub=sub), home=SITE + ('/?lang=en' if L['li'] else '/?lang=tr'),
                app_link=esc(L['app_link']), other_lang=trs if L['li'] else ens,
                other_word=esc(L['other_word']), feed_title=esc(L['feed_name']),
                feed_url='%s/%s' % (SITE, L['feed']), alt_tr=trs, alt_en=ens, alt_x=ens,
                og_image=SITE + '/og.png', app=SITE + ('/?lang=en' if L['li'] else '/?lang=tr'))
    base.update(kw)
    return base


def _crumb(L, sub, *extra):
    parts = ['<a href="%s">%s</a>' % (_home(L, sub), esc(L['hub_name']))]
    parts += ['<a href="%s">%s</a>' % (esc(h), esc(t)) for h, t in extra]
    return '<b>/</b>'.join(parts)


def _page(out_dir, L, path, html):
    p = os.path.join(out_dir, 'k', *([L['dir'].strip('/')] if L['dir'] else []) + path.split('/'))
    if not os.path.isdir(os.path.dirname(p)):
        os.makedirs(os.path.dirname(p))
    io.open(p, 'w', encoding='utf-8', newline='\n').write(html)


def _fold(s):
    from taghubs import slug
    return re.sub(r'[^a-z0-9]+', '-', slug(s.lower())).strip('-') or 'x'


# ------------------------------------------------------------------ markdown
def _inline(s):
    s = esc(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*([^*]+)\*(?![\w*])', r'<em>\1</em>', s)

    def link(m):
        href = m.group(2)
        if not re.match(r'^(https?:|#|mailto:)', href):
            href = '%s/blob/main/%s' % (REPO, href)       # a path in the repository
        return '<a href="%s">%s</a>' % (href, m.group(1))
    return re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, s)


def markdown(text):
    """The small part of Markdown ABOUT.md uses: ## and ### headings,
    paragraphs, - lists, > quotes, **bold**, *italic*, `code` and links. The
    first # heading is the page's own <h1> and is left out, and so is a
    one-line <!-- comment --> (a note to whoever edits the file)."""
    out, para, items, quote = [], [], [], []

    def flush():
        if para:
            out.append('<p>%s</p>' % _inline(' '.join(para)))
            del para[:]
        if items:
            out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % _inline(i) for i in items))
            del items[:]
        if quote:
            out.append('<blockquote><p>%s</p></blockquote>' % _inline(' '.join(quote)))
            del quote[:]

    for line in text.split('\n'):
        s = line.strip()
        if not s or s == '---' or (s.startswith('<!--') and s.endswith('-->')):
            flush()
        elif s.startswith('# '):
            flush()
        elif s.startswith('### '):
            flush()
            out.append('<h3>%s</h3>' % _inline(s[4:]))
        elif s.startswith('## '):
            flush()
            out.append('<h2 class="sh">%s</h2>' % _inline(s[3:]))
        elif s.startswith('- '):
            if para or quote:
                flush()
            items.append(s[2:])
        elif s.startswith('>'):
            if para or items:
                flush()
            quote.append(s.lstrip('> '))
        elif items and line.startswith('  '):
            items[-1] += ' ' + s
        else:
            if items or quote:
                flush()
            para.append(s)
    flush()
    return '\n'.join(out)


# ------------------------------------------------------------------ alternatives
def alt_clusters(core):
    """Entries the directory compares with at least ALT_MIN others.

    The curated comparisons (vs) are edges between two records, written on one
    side. An entry with three or more of them is the centre of a real choice
    ("what else is there besides X, and how does each differ"), so it gets a
    page. A centre whose whole cluster is already inside a bigger page is
    skipped: the same four records twice is not two pages' worth.
    Returns [{'i', 'slug', 'rivals': [(j, axis index)]}], in directory order.
    """
    adj = collections.defaultdict(dict)
    for i, d in enumerate(core):
        for j, a in d.get('vs', []):
            adj[i].setdefault(j, a)
            adj[j].setdefault(i, a)
    cands = sorted((i for i in adj if len(adj[i]) >= ALT_MIN),
                   key=lambda i: (-len(adj[i]), core[i]['name'].lower()))
    chosen, covered = [], []
    for i in cands:
        group = {i} | set(adj[i])
        if any(group <= c for c in covered):
            continue
        covered.append(group)
        chosen.append(i)
    out, used = [], set()
    for i in sorted(chosen):
        s = base = _fold(core[i]['name'])
        n = 1
        while s in used:
            n += 1
            s = '%s-%d' % (base, n)
        used.add(s)
        rivals = sorted(adj[i].items(), key=lambda t: (t[1], core[t[0]]['name'].lower()))
        out.append({'i': i, 'slug': s, 'rivals': rivals})
    return out


def _alt_pages(core, cats, en_desc, alts, out_dir):
    places = _places(core)
    pairs = []
    for lang, L in sorted(LANGS.items()):
        T, li = TX[lang], L['li']
        label = dict((c[0], c[L['ci']]) for c in cats)

        def desc(i):
            return en_desc[i] if li else core[i]['tr']

        for a in alts:
            d = core[a['i']]
            k, ca = places[d['url']]
            rows = [(j, core[j]) for j, _ in a['rivals']]
            ids = _anchors(rows)
            items = []
            for n, ((j, r), aid, (_, ax)) in enumerate(zip(rows, ids, a['rivals']), 1):
                rk, rca = places[r['url']]
                items.append(
                    '<article class="rec" id="%s"><span class="no">%d</span><div class="rb">\n'
                    '<p class="path">%s: %s</p>\n'
                    '<div class="nm"><a class="name" href="%s" rel="noopener noreferrer nofollow">%s</a>'
                    '<span class="host">%s</span></div>\n'
                    '<p class="desc">%s <a href="../%s.html#%s">%s</a></p>\n'
                    '<div class="mt">%s</div>\n'
                    '</div></article>'
                    % (esc(aid), n, esc(T['differs']), esc(AXES[ax][1 + li]), esc(r['url']),
                       esc(r['name']), esc(_host(r['url'])), _code(esc(_first(desc(j)))),
                       esc(rk), esc(rca), esc(L['in_cat'] % label[rk]), trust(r, L)))
            title = T['alt_title'].format(x=d['name'])
            body = ('<div class="recs">\n<article class="rec"><span class="no">◆</span><div class="rb">\n'
                    '<p class="path">%s</p>\n'
                    '<div class="nm"><a class="name" href="%s" rel="noopener noreferrer nofollow">%s</a>'
                    '<span class="host">%s</span></div>\n'
                    '<p class="desc">%s <a href="../%s.html#%s">%s</a></p>\n<div class="mt">%s</div>\n'
                    '</div></article>\n%s\n</div>'
                    % (esc(T['alt_anchor']), esc(d['url']), esc(d['name']), esc(_host(d['url'])),
                       _code(esc(_first(desc(a['i'])))), esc(k), esc(ca), esc(L['in_cat'] % label[k]),
                       trust(d, L), '\n'.join(items)))
            path = 'alt/%s.html' % a['slug']
            kw = _kw(L, out_dir, path, path, True)
            lede = T['alt_lede'].format(x=d['name'], n=len(rows))
            ld = ('{"@context":"https://schema.org","@type":"ItemList","name":%s,"url":%s,"inLanguage":"%s",'
                  '"numberOfItems":%d,"itemListElement":[%s]}'
                  % (json.dumps(title, ensure_ascii=False), json.dumps(kw['canon']), L['code'], len(rows),
                     ','.join('{"@type":"ListItem","position":%d,"url":%s,"name":%s}'
                              % (n, json.dumps(kw['canon'] + '#' + aid), json.dumps(r['name'], ensure_ascii=False))
                              for n, ((_, r), aid) in enumerate(zip(rows, ids), 1))))
            _page(out_dir, L, path, TEXT.format(
                title=esc('%s — %s' % (title, L['name'])), h1=esc(title), desc=esc(lede[:180]),
                intro=esc(lede), body=body, jsonld=ld,
                crumb=_crumb(L, True, ('../%s.html' % k, label[k])),
                foot=site_foot(L, sub=True), **kw))
            if lang == 'tr':
                pairs.append(('%s/k/%s' % (SITE, path), '%s/k/en/%s' % (SITE, path),
                              newest([(a['i'], d)] + rows)))
        _prune(out_dir, L, 'alt', {a['slug'] + '.html' for a in alts})
    return pairs


# ------------------------------------------------------------------ tag index
def _tag_index(core, tags, taglbl, out_dir):
    from taghubs import INTROS, MIN_N
    pairs = []
    for lang, L in sorted(LANGS.items()):
        T, li = TX[lang], L['li']
        toc = ''.join('<li><a class="tt" href="%s.html"><span class="tn">%s</span><span class="ld"></span>'
                      '<span class="n">%d</span></a><p class="td">%s</p></li>\n'
                      % (esc(s), esc(taglbl[t][li]), n, esc(INTROS[t][li])) for t, s, n in tags)
        kw = _kw(L, out_dir, 't/index.html', 'tag/index.html', True)
        lede = T['tags_lede'].format(n=MIN_N)
        _page(out_dir, L, '%s/index.html' % L['tdir'], TEXT.replace('catpage prose', 'fieldpage').format(
            title=esc('%s — %s' % (T['tags_title'], L['name'])), h1=esc(T['tags_title']),
            desc=esc(lede[:180]), intro=esc(lede), crumb=_crumb(L, True),
            body='<p class="count">%d %s</p>\n<ol class="toc">\n%s</ol>' % (len(tags), esc(T['ntags']), toc),
            jsonld=('{"@context":"https://schema.org","@type":"CollectionPage","name":%s,"url":%s,'
                    '"inLanguage":"%s"}' % (json.dumps(T['tags_title'], ensure_ascii=False),
                                            json.dumps(kw['canon']), L['code'])),
            foot=site_foot(L, sub=True), **kw))
    rows = [(i, d) for i, d in enumerate(core) if any(t in d['tags'] for t, _, _ in tags)]
    pairs.append(('%s/k/t/index.html' % SITE, '%s/k/en/tag/index.html' % SITE, newest(rows)))
    return pairs


# ------------------------------------------------------------------ about
def _about(core, alts, out_dir, scanned):
    count = collections.Counter(d['src'] for d in core)
    pairs = []
    for lang, L in sorted(LANGS.items()):
        T, li = TX[lang], L['li']
        src = io.open(os.path.join(D, '..', 'ABOUT.md' if li else 'ABOUT.tr.md'), encoding='utf-8').read()
        credits = 'credits.html' if li else 'tesekkur.html'
        up = '../../' if li else '../'
        srcs = ''.join('<li><a href="%s#src-%s">%s</a> — %d %s · %s</li>'
                       % (credits, esc(k), esc(SOURCES[k]['label_en' if li else 'label_tr']), count[k],
                          esc(L['links']), emit._licence(SOURCES[k], lang).split(' · <span')[0])
                       for k in sorted(SOURCES, key=lambda k: (k != 'kedi', -count[k], k)) if count[k])
        alts_html = ' '.join('<a href="alt/%s.html">%s</a>' % (esc(a['slug']), esc(core[a['i']]['name']))
                             for a in sorted(alts, key=lambda a: core[a['i']]['name'].lower()))
        body = (markdown(src)
                + '\n<h2 class="sh">%s</h2>\n<p>%s</p>\n<ul>%s</ul>'
                % (esc(T['src_head']), T['src_text'].format(credits=credits), srcs)
                + '\n<h2 class="sh">%s</h2>\n<p>%s</p>'
                % (esc(T['data_head']), T['data_text'].format(
                    json=up + 'data/v1/links.json', csv=up + 'data/v1/links.csv',
                    schema=REPO + '/blob/main/data/v1/SCHEMA.md'))
                + '\n<h2 class="sh">%s</h2>\n<p>%s</p>\n<p class="ilinks">%s</p>'
                % (esc(T['alts_head']), esc(T['alts_text'].format(n=ALT_MIN)), alts_html)
                + '\n<h2 class="sh">%s</h2>\n<p class="ilinks">%s · %s · <a href="changes.html">%s</a> · '
                  '<a href="%s">%s</a></p>'
                % (esc(T['more_head']),
                   '<a href="%s/index.html">%s</a>' % (L['pdir'], esc(L['paths_head'])),
                   '<a href="%s/index.html">%s</a>' % (L['tdir'], esc(L['tags_head'])),
                   esc(T['changes']), _home(L), esc(L['hub_name'])))
        kw = _kw(L, out_dir, 'about.html', 'about.html', False)
        ld = json.dumps({'@context': 'https://schema.org', '@type': 'AboutPage', 'name': T['about'],
                         'url': kw['canon'], 'inLanguage': L['code'],
                         'maintainer': {'@type': 'Person', 'name': 'latifkedi',
                                        'url': 'https://github.com/latifkedi'},
                         'license': 'https://creativecommons.org/licenses/by/4.0/'}, ensure_ascii=False)
        _page(out_dir, L, 'about.html', TEXT.format(
            title=esc('%s — %s' % (T['about'], L['name'])), h1=esc(T['about']),
            desc=esc(T['about_lede'][:180]), intro=esc(T['about_lede']), body=body, jsonld=ld,
            crumb=_crumb(L, False), foot=site_foot(L), **kw))
    pairs.append(('%s/k/about.html' % SITE, '%s/k/en/about.html' % SITE, scanned))
    return pairs


# ------------------------------------------------------------------ changes
def _removed():
    out = []
    p = os.path.join(D, 'removed.txt')
    if not os.path.exists(p):
        return out
    for line in io.open(p, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip() or line.startswith('#'):
            continue
        url, _, why = line.partition('\t')
        out.append((url.strip(), why.strip()))
    return out


def _week_of(ts):
    y, w, _ = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).date().isocalendar()
    return '%d-W%02d' % (y, w)


def _week_span(wk):
    y, w = int(wk[:4]), int(wk[6:])
    a = datetime.date.fromisocalendar(y, w, 1)
    return a, a + datetime.timedelta(days=6)


def _n(T, n):
    return T['entry'] if n == 1 else T['entries']


def _fmt(day, lang):
    return '%d %s %d' % (day.day, MONTHS[lang][day.month - 1], day.year)


def _changes(core, cats, en_desc, out_dir, real, scanned):
    places = _places(core)
    dated = [(i, d) for i, d in enumerate(core) if real[i]]
    by_week = collections.defaultdict(list)
    by_month = collections.defaultdict(list)
    for i, d in dated:
        by_week[_week_of(d['added'])].append((i, d))
        by_month[_day(d['added'])[:7]].append((i, d))
    weeks = sorted(by_week, reverse=True)[:WEEKS]
    order = {c[0]: n for n, c in enumerate(cats)}
    removed = _removed()
    pairs = []
    for lang, L in sorted(LANGS.items()):
        T, li = TX[lang], L['li']
        label = dict((c[0], c[L['ci']]) for c in cats)
        # ---- one digest page per recent week
        entries = []
        for n_w, wk in enumerate(weeks):
            rows = sorted(by_week[wk], key=lambda t: (order.get(t[1]['cat'], 99), t[1]['name'].lower()))
            shown = rows[:WEEK_CAP]
            ids = _anchors(shown)
            items = []
            for n, ((i, d), a) in enumerate(zip(shown, ids), 1):
                k, ca = places[d['url']]
                items.append(_item_short(d, en_desc[i] if li else d['tr'], L, n, a,
                                         '../%s.html#%s' % (k, ca), label[k]))
            a_day, b_day = _week_span(wk)
            title = T['week_title'].format(y=wk[:4], w=int(wk[6:]))
            lede = T['week_lede'].format(n=len(rows), e=_n(T, len(rows)), a=_fmt(a_day, lang), b=_fmt(b_day, lang))
            nav = []
            if n_w + 1 < len(weeks):
                nav.append('<a href="%s.html">%s</a>' % (weeks[n_w + 1], esc(T['prev'])))
            if n_w > 0:
                nav.append('<a href="%s.html">%s</a>' % (weeks[n_w - 1], esc(T['next'])))
            body = ('<div class="recs">\n%s\n</div>\n%s<nav class="other"><p>%s</p></nav>'
                    % ('\n'.join(items),
                       '<p class="count">%s</p>\n' % esc(T['week_more'].format(n=len(rows) - len(shown)))
                       if len(rows) > len(shown) else '', ' '.join(nav)))
            path = 'week/%s.html' % wk
            kw = _kw(L, out_dir, path, path, True)
            _page(out_dir, L, path, TEXT.format(
                title=esc('%s — %s' % (title, L['name'])), h1=esc(title), desc=esc(lede[:180]),
                intro=esc(lede), body=body,
                jsonld=('{"@context":"https://schema.org","@type":"CollectionPage","name":%s,"url":%s,'
                        '"inLanguage":"%s"}' % (json.dumps(title, ensure_ascii=False),
                                                json.dumps(kw['canon']), L['code'])),
                crumb=_crumb(L, True, ('../changes.html', T['changes'])),
                foot=site_foot(L, sub=True), **kw))
            names = ', '.join(d['name'] for _, d in rows[:30]) + (' …' if len(rows) > 30 else '')
            entries.append((kw['canon'], title, kw['canon'], max(d['added'] for _, d in rows),
                            '<p>%s</p><p>%s</p>' % (esc(lede), esc(names)), None))
            if lang == 'tr':
                pairs.append(('%s/k/%s' % (SITE, path), '%s/k/en/%s' % (SITE, path), newest(rows)))
        _prune(out_dir, L, 'week', {wk + '.html' for wk in weeks})
        fdir = os.path.join(out_dir, 'feed', *([L['dir'].strip('/')] if L['dir'] else []))
        io.open(os.path.join(fdir, 'changes.xml'), 'w', encoding='utf-8', newline='\n').write(atom(
            T['feed_title'], T['changes_lede'], '%s/feed/%schanges.xml' % (SITE, L['dir']),
            '%s/k/%schanges.html' % (SITE, L['dir']), entries, L))

        # ---- the changes page
        rem = ''.join('<li>%s — <span lang="en">%s</span></li>' % (esc(u), esc(w))
                      for u, w in removed)
        wl = ''.join('<li><a href="week/%s.html">%s</a> — %d %s</li>'
                     % (wk, esc(T['week_title'].format(y=wk[:4], w=int(wk[6:]))), len(by_week[wk]),
                        esc(_n(T, len(by_week[wk])))) for wk in weeks)
        ml = []
        for m in sorted(by_month, reverse=True):
            rows = by_month[m]
            per = collections.Counter(d['cat'] for _, d in rows)
            ml.append('<h3>%s %s — %d %s</h3>\n<p class="ilinks">%s</p>'
                      % (MONTHS[lang][int(m[5:]) - 1], m[:4], len(rows), esc(_n(T, len(rows))),
                         ' · '.join('<a href="%s.html">%s</a> %d' % (esc(k), esc(label[k]), per[k])
                                    for k in sorted(per, key=lambda k: (-per[k], order.get(k, 99))))))
        body = ('<h2 class="sh">%s</h2>\n<ul>%s</ul>\n'
                '<h2 class="sh">%s</h2>\n<p>%s</p>\n<ul>%s</ul>\n'
                '<h2 class="sh">%s</h2>\n<p>%s</p>\n%s'
                % (esc(T['weeks_head']), wl,
                   esc(T['removed_head']), esc(T['removed_note']), rem,
                   esc(T['months_head']), esc(T['months_note'].format(n=len(dated))), '\n'.join(ml)))
        kw = _kw(L, out_dir, 'changes.html', 'changes.html', False,
                 feed_title=esc(T['feed_title']), feed_url='%s/feed/%schanges.xml' % (SITE, L['dir']))
        _page(out_dir, L, 'changes.html', TEXT.format(
            title=esc('%s — %s' % (T['changes'], L['name'])), h1=esc(T['changes']),
            desc=esc(T['changes_lede'][:180]), intro=esc(T['changes_lede']), body=body,
            jsonld=('{"@context":"https://schema.org","@type":"CollectionPage","name":%s,"url":%s,'
                    '"inLanguage":"%s"}' % (json.dumps(T['changes'], ensure_ascii=False),
                                            json.dumps(kw['canon']), L['code'])),
            crumb=_crumb(L, False), foot=site_foot(L), **kw))
    pairs.insert(0, ('%s/k/changes.html' % SITE, '%s/k/en/changes.html' % SITE,
                     newest(dated) if dated else scanned))
    return pairs


# ------------------------------------------------------------------ open data
FIELDS = ['url', 'name', 'category', 'tags', 'tr', 'en', 'src', 'licence', 'added', 'verified', 'state']


def state(d):
    """One word for what the last scans found, worst first."""
    if d.get('dead'):
        return 'dead'
    if d.get('hs') == 'yok':
        return 'repo-deleted'
    if d.get('hs') == 'arşiv' or 'arşivlenmiş' in d.get('tags', ()):
        return 'archived'
    if d.get('hs') == 'bayat':
        return 'dormant'
    if d.get('verw'):
        return 'blocked'
    return 'ok' if d.get('ver') else 'unchecked'


def open_data(core, en_desc, out_dir):
    """data/v1/links.json and links.csv: every record, in the directory's own
    order (heading, then name), one JSON object per line so a change shows as
    a one-line diff. Fields and their meaning: data/v1/SCHEMA.md."""
    rows = [{'url': d['url'], 'name': d['name'], 'category': d['cat'], 'tags': d['tags'],
             'tr': d['tr'], 'en': en_desc[i], 'src': d['src'],
             'licence': SOURCES.get(d['src'], {}).get('licence', 'unspecified'), 'added': _day(d['added']),
             'verified': d.get('ver') or '', 'state': state(d)} for i, d in enumerate(core)]
    vdir = os.path.join(out_dir, 'data', 'v1')
    if not os.path.isdir(vdir):
        os.makedirs(vdir)
    io.open(os.path.join(vdir, 'links.json'), 'w', encoding='utf-8', newline='\n').write(
        '{"schema":"%s/blob/main/data/v1/SCHEMA.md","licence":"descriptions: CC-BY-4.0; the selection behind each record keeps the licence of its source (field licence)","count":%d,"records":[\n%s\n]}\n'
        % (REPO, len(rows), ',\n'.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) for r in rows)))
    with io.open(os.path.join(vdir, 'links.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(FIELDS)
        for r in rows:
            w.writerow([' '.join(r[k]) if k == 'tags' else r[k] for k in FIELDS])
    return len(rows)


def write(core, cats, en_desc, taglbl, tags, alts, out_dir, scanned, real):
    """Everything above; returns the sitemap entries (tr url, en url, lastmod)."""
    open_data(core, en_desc, out_dir)
    return (_about(core, alts, out_dir, scanned) + _changes(core, cats, en_desc, out_dir, real, scanned)
            + _tag_index(core, tags, taglbl, out_dir) + _alt_pages(core, cats, en_desc, alts, out_dir))
