# -*- coding: utf-8 -*-
"""Scans the links in links.js and writes the failures to rapor.md.

Meant for GitHub Actions; runs locally too:  python data/ci_check.py

One classification drives both the report and verified.json. The first
version used two: the report called only 404/410/no-answer "dead", while
verified.json marked everything outside a short list of blocking codes as
dead -- so a 400 or a 418 from a bot-shy site read as "suspect" in the report
and showed up on the site as a Dead badge. Eleven live entries carried one.

    ok       the page answered below 400
    dead     404 or 410, or the host name does not resolve
    suspect  anything else: other 4xx/5xx, timeouts, refused connections, TLS
             failures -- the usual signature of bot blocking or a slow server,
             not of a page that is gone

An entry is marked "olu" (the Dead badge on the site) only after DEAD_AFTER
consecutive dead scans; a first dead scan counts as suspect. Sites go down
for an afternoon, and a directory that removes a link on one bad Monday
teaches its readers to ignore the badge.

data/manual.json holds decisions a person made after checking by hand
("opens fine in a browser; the scanner gets a 404"). They win over the scan in
verified.json, so a weekly run cannot undo them -- the first version of this
check re-flagged every hand-verified entry each Monday. They are still listed
in the report while the scan keeps failing, so a stale decision gets noticed.
"""
import json
import re
import io
import os
import sys
import datetime
import concurrent.futures as cf

import requests
import urllib3

urllib3.disable_warnings()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import readlinks  # noqa: E402
from notes import key  # noqa: E402
from linkstate import classify, next_state, DEAD_AFTER  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
# The Accept header matters: crates.io answers the same URL as an API or as the
# page depending on it, and without text/html it returns 404 to the scanner.
HEADERS = {'User-Agent': UA, 'Accept-Language': 'tr,en;q=0.9',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

# HEAD is tried first because it is cheap, but only a GET is believed: plenty of
# servers refuse HEAD or answer it differently from a real page load. The first
# version retried only on a short list of codes -- not 404 -- so a HEAD-shy
# site (Kaggle, Wolfram Alpha, crates.io) was marked dead on a HEAD 404 while
# serving the page to every browser.

# requests wraps a failed DNS lookup in a plain ConnectionError; the cause is
# only visible in the message. A name that does not resolve is a gone domain,
# unlike a refused or timed-out connection.
DNS_SIGNS = ('NameResolutionError', 'getaddrinfo failed', 'Name or service not known',
             'nodename nor servname', 'No address associated', 'Temporary failure in name')

MANUAL_STATES = ('ok', 'engel')


def check(rec):
    """None when the link is fine, otherwise what went wrong."""
    url = rec['url']
    out = {'name': rec['name'], 'url': url, 'cat': rec.get('cat_tr', '')}
    for method in ('head', 'get'):
        try:
            try:
                r = requests.request(method, url, headers=HEADERS,
                                     timeout=(6, 14), allow_redirects=True,
                                     verify=True, stream=(method == 'get'))
            except requests.exceptions.SSLError:
                r = requests.request(method, url, headers=HEADERS,
                                     timeout=(6, 14), allow_redirects=True,
                                     verify=False, stream=(method == 'get'))
            if method == 'get':
                r.close()
            out['status'] = r.status_code
            out.pop('error', None)
            out.pop('dns', None)
            if r.status_code < 400:
                return None
            if method == 'head':
                continue                # never trust a failed HEAD; ask again with GET
            return out
        except requests.exceptions.RequestException as e:
            out['status'] = 0
            out['error'] = type(e).__name__
            out['dns'] = any(s in repr(e) for s in DNS_SIGNS)
    return out


def load_manual():
    path = os.path.join(ROOT, 'data', 'manual.json')
    if not os.path.exists(path):
        return {}
    data = json.load(io.open(path, encoding='utf-8'))
    bad = [k for k, v in data.items() if v.get('s') not in MANUAL_STATES]
    if bad:
        raise ValueError('manual.json: "s" must be one of %s -- %s' % (MANUAL_STATES, bad[:3]))
    return data


def write_verified(links, results, manual, today):
    """Refreshes verified.json and returns {url: final status} for the report.

    The site shows "last verified" on every entry and this file is where that
    comes from. "f" counts consecutive dead scans.
    """
    path = os.path.join(ROOT, 'data', 'verified.json')
    ver = json.load(io.open(path, encoding='utf-8')) if os.path.exists(path) else {}
    final = {}
    for l in links:
        k = key(l['url'])
        ent = next_state(ver.get(k, {}), classify(results.get(l['url'])), manual.get(k), today)
        ver[k] = ent
        final[l['url']] = ent['s']

    # Entries removed from the directory leave their verification behind. The
    # file had once accumulated 251 such keys against 988 records. Anything
    # with no record is dropped on each run.
    live = set()
    for l in links:
        k = key(l['url'])
        live.add(k)
        live.add(re.split(r'[?#]', k)[0].rstrip('/'))
    for k in [k for k in ver if k not in live]:
        del ver[k]

    json.dump(ver, io.open(path, 'w', encoding='utf-8', newline='\n'),
              ensure_ascii=False, indent=1)
    return final


def _row(r, extra=''):
    st = r.get('error') or r['status']
    return '| %s | %s | `%s`%s | %s |' % (r['name'], r['cat'], st, extra, r['url'])


def report(links, results, final, manual, today):
    failing = [r for r in results.values()]
    over = [r for r in failing if key(r['url']) in manual]
    rest = [r for r in failing if key(r['url']) not in manual]
    dead = [r for r in rest if final.get(r['url']) == 'olu']
    first = [r for r in rest if classify(r) == 'dead' and final.get(r['url']) != 'olu']
    suspect = [r for r in rest if classify(r) == 'suspect']

    print('scanned: %d | dead: %d | first dead scan: %d | suspect: %d | manual: %d'
          % (len(links), len(dead), len(first), len(suspect), len(over)))

    path = os.path.join(ROOT, 'rapor.md')
    if not failing:
        if os.path.exists(path):
            os.remove(path)             # a clean week reads as clean
        return 0

    head = '| Entry | Category | Status | URL |\n|---|---|---|---|'
    L = ['# Link check - %s' % today, '', '`%d` links scanned.' % len(links), '']
    sections = [
        (dead, 'Dead (%d)' % len(dead),
         'Dead on %d consecutive scans (404/410 or the domain no longer '
         'resolves). Marked dead on the site. Replace or remove.' % DEAD_AFTER),
        (first, 'Failed once (%d)' % len(first),
         'Dead on this scan only. Not marked on the site yet; another dead scan '
         'next week will. Worth a look now if the domain looks lapsed.'),
        (suspect, 'Suspect (%d)' % len(suspect),
         'Other errors, timeouts or refused connections -- usually bot blocking '
         'or a slow server. These most likely open fine in a browser.'),
        (over, 'Held by manual.json (%d)' % len(over),
         'Still failing the scan, but a person checked these by hand and '
         'recorded a decision in data/manual.json. Revisit if it looks stale.'),
    ]
    for rows, title, blurb in sections:
        if not rows:
            continue
        L += ['## ' + title, '', blurb, '', head]
        for r in sorted(rows, key=lambda x: (x['cat'], x['name'])):
            L.append(_row(r))
        L.append('')
    L.append('<sub>Generated by `data/ci_check.py`.</sub>')
    io.open(path, 'w', encoding='utf-8').write('\n'.join(L))
    return 1 if dead else 0


def main():
    links = readlinks.read(ROOT)
    manual = load_manual()
    today = datetime.date.today().isoformat()
    with cf.ThreadPoolExecutor(max_workers=16) as ex:
        results = {r['url']: r for r in ex.map(check, links) if r}
    final = write_verified(links, results, manual, today)
    return report(links, results, final, manual, today)


if __name__ == '__main__':
    sys.exit(main())
