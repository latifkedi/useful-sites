# -*- coding: utf-8 -*-
"""Records in data/manual.json that a person opened these addresses in a browser.

    python data/mark_ok.py https://doaj.org https://etherscan.io ...

The weekly scan gets 403 from sites behind a bot challenge (Cloudflare and the
like) and cannot tell them from dead ones. Open the address yourself; if the
real page loads, run this with the address exactly as it appears in the
directory. Each one is written as "ok" with today's date and a date to look again
("r", half a year on), and a scan that keeps failing is then reported as held by
manual.json instead of suspect; when "r" comes the weekly report asks for a recheck. Addresses
that are not in the directory are refused, so a typo cannot add a stray entry.
"""
import datetime
import io
import json
import os
import sys

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)

import linkstate   # noqa: E402
import readlinks   # noqa: E402
from ci_check import key   # noqa: E402

ROOT = os.path.join(D, '..')
NOTE = ('Opened in a real browser on %s with its real page; the weekly scanner '
        'gets a bot-block response from this site.')


def main(urls):
    if not urls:
        print(__doc__)
        return 1
    known = {key(r['url']): r['name'] for r in readlinks.read(ROOT)}
    path = os.path.join(D, 'manual.json')
    manual = json.load(io.open(path, encoding='utf-8'))
    today = datetime.date.today().isoformat()
    bad = [u for u in urls if key(u) not in known]
    if bad:
        print('not in the directory (nothing written): ' + ', '.join(bad))
        return 1
    for u in urls:
        manual[key(u)] = {'d': today, 'r': linkstate.recheck_date(today), 's': 'ok', 'note': NOTE % today}
        print('ok  %s  (%s)' % (known[key(u)], u))
    io.open(path, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(dict(sorted(manual.items())), ensure_ascii=False, indent=1) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
