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


def orphan_keys(keys, urls, keyfn):
    """Keys of verified.json (or manual.json) that no record in the directory carries.

    A removed or re-addressed record leaves its entry behind; the file once held 251
    such keys against 988 records. Matches a record by its key with and without the
    query string, as the scan always has.
    """
    live = set()
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
# A week's review list stays short enough to be read; the overflow is counted, and
# next week brings a different slice of records anyway.
CLAIM_CAP = 25


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


def claim_rechecks(rows, today, cap=CLAIM_CAP):
    """Records due this week whose description makes a perishable claim.

    rows: dicts with cat, url, added (or None), tr, en. Returns (picked, overflow):
    at most `cap` of them, the 90-day tier first, and how many were left out.
    """
    due = []
    for r in rows:
        words = time_claims((r.get('tr') or '') + ' ' + (r.get('en') or ''))
        if words and description_due(r.get('cat'), r.get('url'), r.get('added'), today):
            due.append(dict(r, claims=words))
    due.sort(key=lambda r: (recheck_days(r.get('cat')), r.get('url') or ''))
    return due[:cap], max(0, len(due) - cap)


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


def next_state(prev, c, manual_entry, today):
    """One entry's verified.json value after a scan classified as c.

    Pure, so the rules can be tested without a network: ok resets the count;
    suspect keeps it (neither confirms nor clears); dead increments it and
    only reaches "olu" at DEAD_AFTER. A manual decision overrides all three.
    """
    if manual_entry:
        return {'d': today, 's': manual_entry['s']}
    f = prev.get('f', 0)
    if c == 'ok':
        return {'d': today, 's': 'ok'}
    if c == 'suspect':
        return dict({'d': today, 's': 'engel'}, **({'f': f} if f else {}))
    f += 1
    if f >= DEAD_AFTER:
        # The date is left alone -- a stale date carries its own warning --
        # and the status lets the site point at the archive.
        return {'d': prev.get('d', today), 's': 'olu', 'f': f}
    return {'d': today, 's': 'engel', 'f': f}
