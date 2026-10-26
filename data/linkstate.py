# -*- coding: utf-8 -*-
"""The link-check rules, with no network in sight.

ci_check.py does the requests; this decides what a result means and how an
entry in verified.json moves from one scan to the next. Kept apart so the rules
can be unit-tested in the build job, which does not install requests.
"""

import datetime
import re
import zlib

DEAD_CODES = {404, 410}
DEAD_AFTER = 2

# github.com paths that are GitHub's own pages, not an owner.
GITHUB_SITE = {'topics', 'features', 'education', 'sponsors', 'orgs', 'collections',
               'marketplace', 'settings', 'search', 'explore', 'trending', 'about'}
# Second path segments that are a tab of a user or organisation page.
GITHUB_TABS = {'repositories', 'followers', 'following', 'stars', 'projects',
               'packages', 'people', 'sponsoring', 'teams'}


def github_target(url):
    """What a github.com URL points at, for the repository audit.

    ('repo', owner, name) for a repository or a path inside one; ('page', owner,
    None) for a user or organisation page -- which has no single repository to
    judge, and used to be scanned like a project homepage, its first link
    taken as "the" repository and a 404 reported as a deleted repo; None for
    GitHub's own pages and for other sites.
    """
    m = re.match(r'https?://(?:www\.)?github\.com/([^/?#]+)(?:/([^/?#]+))?', url or '', re.I)
    if not m or m.group(1).lower() in GITHUB_SITE:
        return None
    owner, name = m.group(1), m.group(2)
    if not name or name.lower() in GITHUB_TABS:
        return ('page', owner, None)
    return ('repo', owner, re.sub(r'\.git$', '', name).rstrip('.'))


# A YouTube page is a JavaScript shell: the scan sees an empty or generic title
# and almost no text, so "is the recorded name still on the page" has no answer.
YOUTUBE = re.compile(r'https?://(?:[a-z0-9-]+\.)?(?:youtube\.com|youtu\.be)/', re.I)


def name_check_applies(url, title):
    """Whether "the name is missing from the page" can mean anything for this page.

    ci_fresh's "name not on the page" list was half noise: 19 of its 50 entries
    were YouTube channels and 34 had no <title> at all. A page with no title, and
    a site whose page is a script shell, cannot be judged by its words.
    """
    return bool((title or '').strip()) and not YOUTUBE.match(url or '')


# A decision made by hand is true on the day it is made. Sites change hands (es6console.com
# went from a JavaScript console to a betting site), so every entry in manual.json
# carries a date to look again, "r"; one written without it is due a year after "d".
RECHECK_DAYS = 365


def recheck_due(entry, today):
    """Whether a manual.json entry is due for another look (ISO dates)."""
    r = entry.get('r')
    if r:
        return r <= today
    d = entry.get('d')
    if not d:
        return True
    return (datetime.date.fromisoformat(d) + datetime.timedelta(days=RECHECK_DAYS)).isoformat() <= today


def recheck_date(today, days=180):
    """The "r" that a new manual.json entry gets: look again in half a year."""
    return (datetime.date.fromisoformat(today) + datetime.timedelta(days=days)).isoformat()


# verified.json keys that are not a record: the date of the scan that wrote the file.
META_KEYS = ('scanned',)


def orphan_keys(keys, urls, keyfn):
    """Keys of verified.json (or manual.json) that no record in the directory carries.

    A removed or re-addressed record leaves its entry behind; the file once held 251
    such keys against 988 records. Matches a record by its key with and without the
    query string, as the scan always has. The file's own META_KEYS are not records.
    """
    live = set(META_KEYS)
    for u in urls:
        k = keyfn(u)
        live.add(k)
        live.add(re.split(r'[?#]', k)[0].rstrip('/'))
    return sorted(k for k in keys if k not in live)


# A year in a description is usually a fact about the past ("dropped its free tier
# in 2022", "in development since 2011") and stays true. It is a claim that can go
# stale only when it is set beside a word that speaks of now: "latest release
# 2023", "currently version 5 (2024)". ci_fresh used to flag every year older than
# two: 22 of 22 hits were past-tense facts, so the list taught nobody anything.
PRESENT = re.compile(
    r'(latest|newest|current|currently|as of|today|right now|at present|'
    r'son sürüm|en yeni|güncel|şu an|şimdilik|bugün)(?![a-zçğıöşüÇĞİÖŞÜ])', re.I)
YEAR = re.compile(r'\b(19[89]\d|20[0-4]\d)\b')


def stale_years(text, this_year, window=45):
    """Years older than two that sit within `window` characters of a word about now."""
    out = set()
    for m in YEAR.finditer(text or ''):
        y = int(m.group(1))
        if y > this_year - 2:
            continue
        near = text[max(0, m.start() - window):m.end() + window]
        if PRESENT.search(near):
            out.add(y)
    return sorted(out)


# Freshness tiers. A description goes stale at the speed of its field: an AI tool's
# pricing, model list or waitlist changes within a quarter, a textbook's in years.
# So a record is due a description recheck every 90 days in the AI categories and
# finance/crypto, every 365 elsewhere. Stateless on purpose: the due week is
# derived from the record's arrival date (or, without one, from a hash of its URL),
# so a weekly run sees each record once per interval and nothing has to be stored.
FAST_PREFIXES = ('yz_',)
FAST_CATS = ('finans',)
FAST_DAYS, SLOW_DAYS = 90, 365
WEEK = 7

# The words that make a description perishable: what it costs and whether you can
# get in. "lock-free" and "free-form" are not price claims, hence the lookarounds.
CLAIM = re.compile(r'(?<![-\w])(free|ücretsiz\w*|beta|waitlist|wait-list|bekleme listesi|'
                   r'early access|erken erişim)(?![-\w])', re.I)
# A week's review list stays short enough to be read. What does not fit is carried
# into the next week's list, ahead of that week's own records -- still stateless:
# each run replays the last CARRY_WEEKS weeks of the queue from the same rules.
CLAIM_CAP = 25
CARRY_WEEKS = 8


def recheck_days(cat):
    """How often a record in this category is due a description recheck."""
    cat = cat or ''
    return FAST_DAYS if cat.startswith(FAST_PREFIXES) or cat in FAST_CATS else SLOW_DAYS


def description_due(cat, url, added, today, window=WEEK):
    """Whether a record's description falls due in the week starting `today` (ISO date).

    `added` is the record's unix arrival time or None. A record is never due before
    one full interval has passed since it arrived.
    """
    days = recheck_days(cat)
    t = datetime.date.fromisoformat(today).toordinal()
    if added:
        start = datetime.datetime.fromtimestamp(added, datetime.timezone.utc).date().toordinal()
    else:
        start = zlib.crc32((url or '').encode('utf-8')) % days
    age = t - start
    return age >= days and age % days < window


def time_claims(text):
    """The perishable words (price, beta, waitlist) a description contains, lowercased."""
    return sorted({m.group(1).lower() for m in CLAIM.finditer(text or '')})


def claim_rechecks(rows, today, cap=CLAIM_CAP, carry_weeks=CARRY_WEEKS):
    """Records due this week whose description makes a perishable claim.

    rows: dicts with cat, url, added (or None), tr, en. Returns (picked, overflow):
    at most `cap` of them, and how many are left for next week.

    The overflow used to be dropped ("next interval brings them back" -- 90 or
    365 days later). Now the queue is replayed week by week from `carry_weeks`
    ago: each week takes `cap` records, oldest due week first, then the 90-day
    tier, then an order shuffled by hash of URL and week so that one site does
    not always sort first. Same inputs, same list: nothing is stored.
    """
    claims = []
    for r in rows:
        words = time_claims((r.get('tr') or '') + ' ' + (r.get('en') or ''))
        if words:
            claims.append(dict(r, claims=words))
    t = datetime.date.fromisoformat(today)
    queue = []
    for back in range(carry_weeks, -1, -1):
        week = t - datetime.timedelta(days=WEEK * back)
        w = week.isoformat()
        for r in claims:
            if description_due(r.get('cat'), r.get('url'), r.get('added'), w):
                queue.append((week.toordinal(), recheck_days(r.get('cat')),
                              zlib.crc32(('%s %s' % (r.get('url') or '', w)).encode('utf-8')), r))
        queue.sort(key=lambda q: q[:3])
        picked, queue = queue[:cap], queue[cap:]
    return [q[3] for q in picked], len(queue)


def scan_changes(prev, new):
    """What moved between two verified.json snapshots ({key: entry}).

    The weekly report used to repeat every failing link every week, so the
    one that broke this week drowned among the fifty that were already known.
    Returns {'newly_dead', 'newly_failing', 'recovered'} as sorted key lists;
    a key absent from `prev` counts as previously ok.
    """
    out = {'newly_dead': [], 'newly_failing': [], 'recovered': []}
    for k, e in new.items():
        was = (prev.get(k) or {}).get('s', 'ok')
        now = e.get('s')
        if now == 'olu' and was != 'olu':
            out['newly_dead'].append(k)
        elif now == 'engel' and was == 'ok':
            out['newly_failing'].append(k)
        elif now == 'ok' and was in ('engel', 'olu'):
            out['recovered'].append(k)
    return {k: sorted(v) for k, v in out.items()}


def health_changes(prev, new):
    """What moved between two health.json snapshots ({key: {'s': state}}).

    Returns {state: [keys]} for keys that reached arşiv, bayat or yok this run,
    and 'recovered' for keys that left one of them.
    """
    bad = ('arşiv', 'bayat', 'yok')
    out = {'yok': [], 'arşiv': [], 'bayat': [], 'recovered': []}
    for k, e in new.items():
        was = (prev.get(k) or {}).get('s')
        now = e.get('s')
        if now in bad and now != was:
            out[now].append(k)
        elif was in bad and now not in bad:
            out['recovered'].append(k)
    return {k: sorted(v) for k, v in out.items()}


def may_write(argv, env):
    """Whether a scan may rewrite the tracked data files (verified.json, health.json).

    Only the weekly workflow -- or someone who asks with --write -- does. A scan
    run by hand used to rewrite both files, and committing them collided with the
    bot's commit on main: two people's scans, one file of ~3,800 changed lines,
    one rebase conflict every time. The report is still written either way.
    """
    return '--write' in argv or env.get('GITHUB_ACTIONS') == 'true'


def classify(result):
    if result is None:
        return 'ok'
    if result.get('status') in DEAD_CODES or result.get('dns'):
        return 'dead'
    return 'suspect'


def next_state(prev, c, manual_entry, today, last_scan=None):
    """One entry's verified.json value after a scan classified as c.

    Pure, so the rules can be tested without a network: ok resets the count;
    suspect keeps it (neither confirms nor clears); dead increments it and
    only reaches "olu" at DEAD_AFTER. A manual decision overrides all three.

    The file carries the scan's date once, at the top ("scanned"), and an
    entry carries its own "d" only where that differs: a dead entry keeps the
    date of the scan it first failed on (a stale date carries its own warning, and the site
    points at the archive). Every other entry was checked on the scanned date,
    so it needs none. Writing today's date into all 1,900 entries made every
    weekly commit a 1,900-line diff that hid the few entries that changed;
    now only a change of state touches an entry. `today` is the date of this
    scan, `last_scan` the "scanned" date of the previous one.
    """
    if manual_entry:
        return {'s': manual_entry['s']}
    f = prev.get('f', 0)
    if c == 'ok':
        return {'s': 'ok'}
    if c == 'suspect':
        return dict({'s': 'engel'}, **({'f': f} if f else {}))
    f += 1
    if f >= DEAD_AFTER:
        return {'d': prev.get('d') or last_scan or today, 's': 'olu', 'f': f}
    return {'s': 'engel', 'f': f}
