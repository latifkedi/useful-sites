# -*- coding: utf-8 -*-
"""The link-check rules, with no network in sight.

ci_check.py does the requests; this decides what a result means and how an
entry in verified.json moves from one scan to the next. Kept apart so the rules
can be unit-tested in the build job, which does not install requests.
"""

DEAD_CODES = {404, 410}
DEAD_AFTER = 2


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
