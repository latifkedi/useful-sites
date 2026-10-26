"""Drop verified.json keys that no record carries any more.

The weekly scan runs for an hour against the main it checked out; link-check.yml
then moves to the current main before it rebuilds. If someone removed or
re-addressed a record in between, the scan's verified.json still holds its key
and test_build rejects the file. This prunes against whatever main is now, the
same rule ci_check applies at the end of a scan.

    python data/prune_verified.py
"""
import io
import json
import os
import sys

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from linkstate import orphan_keys  # noqa: E402
from notes import load_records, key  # noqa: E402

path = os.path.join(D, 'verified.json')
ver = json.load(io.open(path, encoding='utf-8'))
scanned = ver.pop('scanned', None)
gone = orphan_keys(ver, [r['url'] for r in load_records()], key)
for k in gone:
    del ver[k]
out = dict({'scanned': scanned}, **ver) if scanned else ver
json.dump(out, io.open(path, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('pruned %d key(s) from verified.json' % len(gone))
