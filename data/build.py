# -*- coding: utf-8 -*-
"""Turns the curator notes into the site data.

Reads data/notes/<category>.json (see notes.py for the record format) and
writes:
  ../links.js      records + Turkish descriptions   (loaded first)
  ../links.en.js   English descriptions             (on language switch)
  plus feed.xml, sitemap.xml, robots.txt and the static pages under ../k/

The two languages are split because the descriptions are most of the
payload; shipping one language makes the first load noticeably lighter.

The build used to merge the notes with metadata extracted from the owner's
personal bookmark export (meta.json, added.json). The bookmarks are kept
separately now, so nothing here reads them: each record carries what it
needs, including its real arrival date where one is known.
"""
import json
import io
import re
import os
import sys
import collections

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from notes import load_records, key, CATS, GROUPS  # noqa: E402
from tags import normalise, LABELS, FACETS  # noqa: E402
from picks import PICKS               # noqa: E402
from sources import SOURCES           # noqa: E402
from intros import INTROS             # noqa: E402
import emit                           # noqa: E402


def _base(k):
    return re.split(r'[?#]', k)[0].rstrip('/')


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

out = []
for n in load_records():
    k = key(n['url'])
    rec = {
        'url': n['url'],
        'name': n['name'],
        'cat': n['cat'],
        'tags': normalise(n['tags']),
        'tr': n['tr'],
        'en': n['en'],
        'src': n['src'],
    }
    if n.get('added'):
        rec['added'] = n['added']
    if n['url'] in PICKS:
        rec['pick'] = 1
    h = HEALTH.get(k) or HEALTH.get(_base(k))
    if h and h.get('s') in ('arşiv', 'bayat', 'yok'):
        rec['hs'] = h['s']
        if h.get('p'):
            rec['hp'] = h['p']

    v = VERIFIED.get(k) or VERIFIED.get(_base(k))
    if v:
        rec['ver'] = v['d']
        if v['s'] == 'engel':
            rec['verw'] = 1          # bot-blocked - needs a manual look
        elif v['s'] == 'olu':
            rec['dead'] = 1          # no response last scan - point at archive
    out.append(rec)

# Records with no known arrival date ("added" absent in the note) need a
# stand-in. One flat value would flatten "newest first" into noise, so
# each intake gets the date it actually arrived.
FALLBACK = 1787000000          # AI tools added while compiling the directory
SRC_ADDED = {
    'bwapsv': 1787000000,      # first external import
    'cdcruz': 1787345600,      # 21 Aug 2026 intake
    'awesome-uw': 1787345600,
    'invesp': 1787345600,
    'seccert': 1787777600,   # 26 Aug 2026 intake
    'lowkwiki': 1789073600,  # 10 Sep 2026 intake
    'rustlearn': 1789689600,
    'javalinks': 1789689600,
    'mathlinks': 1789689600,
    'econ': 1789689600,
    'dataeng': 1789689600,
    'dsbest': 1789689600,
    'testsites': 1789689600,
    'piracy': 1789689600,
    'awesomelist': 1789689600,
    'awesomeproj': 1789689600,
    'quarbby': 1789689600,
    'gmartins': 1789689600,
    'velvia': 1789689600,
}
for r in out:
    if 'added' not in r:
        r['added'] = SRC_ADDED.get(r['src'], FALLBACK)

order = [c[0] for c in CATS]
out.sort(key=lambda r: (order.index(r['cat']) if r['cat'] in order else 99,
                        r['name'].lower()))

# Category labels travel once, in window.CATS, not on every record: the two
# label fields repeated on 1,900 records were 13% of links.js.
core, en = [], []
for r in out:
    core.append({
        'url': r['url'], 'name': r['name'], 'cat': r['cat'], 'tags': r['tags'],
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
    # Indices into LINKS rather than names: names were not guaranteed unique
    # (sixteen were duplicated at one point), and the names cost 100 KB.
    rel = [j for _, _, j in puan[:3]]
    if rel:
        r['rel'] = rel

J = dict(ensure_ascii=False, separators=(',', ':'))
groups = [{'key': k, 'tr': tr, 'en': en_, 'cats': cats}
          for (k, tr, en_, cats) in GROUPS]
# newline='\n' matters: without it a Windows build writes CRLF, and the CI
# "committed output matches a fresh build" check (which rebuilds on Linux, LF)
# then fails on links.js alone. emit.py already pins '\n' on every page.
io.open(os.path.join(D, '..', 'links.js'), 'w', encoding='utf-8', newline='\n').write(
    '/* Otomatik uretildi - data/build.py */\n'
    'window.SOURCES=' + json.dumps(SOURCES, **J) + ';\n'
    'window.TAGLABELS=' + json.dumps(LABELS, **J) + ';\n'
    'window.TAGFACETS=' + json.dumps([[k, tr, en_, ts] for k, tr, en_, ts in FACETS], **J) + ';\n'
    'window.CATS=' + json.dumps([list(c) for c in CATS], **J) + ';\n'
    'window.GROUPS=' + json.dumps(groups, **J) + ';\n'
    'window.INTROS=' + json.dumps(INTROS, **J) + ';\n'
    'window.LINKS=' + json.dumps(core, **J) + ';\n')
io.open(os.path.join(D, '..', 'links.en.js'), 'w', encoding='utf-8', newline='\n').write(
    '/* Otomatik uretildi - data/build.py */\nwindow.LINKS_EN=' + json.dumps(en, **J) + ';\n')

# The text version, for crawlers and for visitors without JavaScript:
# category pages, sitemap, robots and the Atom feed. The app is untouched.
_pages = emit.write_all(core, CATS, INTROS, LABELS, os.path.join(D, '..'), en)
emit.write_issue_form(CATS, os.path.join(D, '..'))

# ------------------------------------------------------------------ cache stamp
# The address of links.js never changes, so after an update a browser can serve
# the old data file while index.html is fresh: new categories simply do not
# appear, and nothing says why. Writing a digest of the content into the query
# makes the address change whenever the content does.
def _stamp():
    import hashlib
    ix = os.path.join(D, '..', 'index.html')
    src = io.open(ix, encoding='utf-8').read()
    # app.js too: it is hand-written, but a browser holding yesterday's copy
    # against today's links.js is the same stale-pairing problem.
    for name in ('links.js', 'links.en.js', 'app.js'):
        h = hashlib.sha1(io.open(os.path.join(D, '..', name), 'rb').read()).hexdigest()[:8]
        pat = re.compile(r'(["\'])' + re.escape(name) + r'(?:\?v=[0-9a-f]+)?\1')
        src = pat.sub(lambda m, n=name, d=h: m.group(1) + n + '?v=' + d + m.group(1), src)
    src = _og_copy(src)
    io.open(ix, 'w', encoding='utf-8', newline='').write(src)


def _count(n):
    """1903 -> '1.900+': a round floor, so the line changes a few times a year
    rather than on every intake, and never claims more than is there."""
    f = n // 100 * 100
    return '{:,}'.format(f).replace(',', '.') + ('+' if n > f else '')


def _og_copy(src):
    # The social preview line carried '1000+ bağlantı, 24 başlık' long after
    # both numbers had moved. It is written from the data now.
    line = ('%s bağlantı, %d alan, %d başlık. Her kayıtta ne işe yaradığı ve '
            'benzerlerinden nerede ayrıldığı yazılı.'
            % (_count(len(core)), len(GROUPS), len({r['cat'] for r in core})))
    return re.sub(r'(<meta property="og:description" content=")[^"]*(">)',
                  lambda m: m.group(1) + line + m.group(2), src, count=1)


def _readme():
    # The README's count said 1,080 for weeks after it had passed 1,700. The
    # two numbers sit between markers now and are written from the data.
    p = os.path.join(D, '..', 'README.md')
    if not os.path.exists(p):
        return
    src = io.open(p, encoding='utf-8').read()
    out = re.sub(r'(<!-- n -->)[^<]*(<!-- /n -->)',
                 lambda m: m.group(1) + _count(len(core)).replace('.', ',') + m.group(2), src)
    out = re.sub(r'(<!-- c -->)[^<]*(<!-- /c -->)',
                 lambda m: m.group(1) + str(len({r['cat'] for r in core})) + m.group(2), out)
    if out != src:
        io.open(p, 'w', encoding='utf-8', newline='\n').write(out)


_stamp()
_readme()

tc = collections.Counter(t for r in out for t in r['tags'])
print('records        :', len(out))
print('distinct tags  :', len(tc))
print('untagged       :', sum(1 for r in out if not r['tags']))
print('real dates     :', sum(1 for r in out if r['added'] != FALLBACK))
print('start-here     :', sum(1 for r in out if r.get('pick')), '/', len(PICKS))
_sc = collections.Counter(r['src'] for r in out)
print('sources        :', dict(_sc))
print('verified       :', sum(1 for r in core if r.get('ver')))
print('with related   :', sum(1 for r in core if r.get('rel')))
print('repo flagged   :', sum(1 for r in core if r.get('hs')))
print('static pages   :', len(_pages), '+ sitemap, robots, feed')
