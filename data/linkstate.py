# -*- coding: utf-8 -*-
"""The link-check rules, with no network in sight.

ci_check.py does the requests; this decides what a result means and how an
entry in verified.json moves from one scan to the next. Kept apart so the rules
can be unit-tested in the build job, which does not install requests.
"""

import datetime
import re

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
