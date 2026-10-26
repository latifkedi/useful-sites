# -*- coding: utf-8 -*-
"""Checks the wiring between files that nothing else cross-checks.

    python data/test_repo.py

Standard library only, writes nothing, needs no build. Run by build.yml.

  labels     Every label an issue form, a workflow or dependabot.yml names is
             listed in .github/labels.yml. GitHub does not create a label an
             issue form names: new-link, broken-entry and approved did not
             exist for weeks, so submissions arrived unlabelled and the
             approval workflow could never fire.
  sources    Every source in sources.py states its licence and copyright, for
             the credits page.
  manual     Every manual.json entry has a decision date "d" and a recheck
             date "r" (ci_check.load_manual refuses a file without them, but
             only inside the weekly scan).
"""
import glob
import io
import json
import os
import re
import sys

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(D)
GH = os.path.join(ROOT, '.github')
sys.path.insert(0, D)

fails = []


def check(ok, msg):
    print(('  ok   ' if ok else '  FAIL ') + msg)
    if not ok:
        fails.append(msg)


def read(p):
    return io.open(p, encoding='utf-8').read()


def declared_labels():
    return {m.strip().strip('"\'') for m in
            re.findall(r'^- name:\s*(.+?)\s*$', read(os.path.join(GH, 'labels.yml')), re.M)}


def _names(inner):
    """'["a", b]' or "'a'" -> ['a', 'b']."""
    return [x.strip().strip('"\'') for x in inner.strip().strip('[]').split(',') if x.strip()]


def used_labels():
    """{label: [file, ...]} for every label name a form, workflow or dependabot names."""
    out = {}
    files = (glob.glob(os.path.join(GH, 'ISSUE_TEMPLATE', '*.yml'))
             + glob.glob(os.path.join(GH, 'workflows', '*.yml'))
             + [os.path.join(GH, 'dependabot.yml')])
    pats = [
        r'^\s*labels:\s*(\[[^\]]*\])',                                  # labels: [a, b]   (YAML)
        r'labels:\s*(\[[^\]]*\])',                                      # labels: ['a']    (github-script)
        r"labels:\s*('[^']+'|\"[^\"]+\")",                              # labels: 'a'      (listForRepo)
        r"contains\([^)]*labels[^)]*,\s*('[^']+')\)",                   # contains(...labels.*.name, 'a')
        r"label\.name\s*==\s*('[^']+')",                                # github.event.label.name == 'a'
        r"removeLabel\([^)]*name:\s*('[^']+')",                         # issues.removeLabel({name: 'a'})
    ]
    for f in files:
        if not os.path.exists(f):
            continue
        src = read(f)
        for p in pats:
            for m in re.finditer(p, src, re.M):
                for n in _names(m.group(1)):
                    out.setdefault(n, set()).add(os.path.relpath(f, ROOT).replace(os.sep, '/'))
    return out


def main():
    print('labels')
    have = declared_labels()
    used = used_labels()
    check(bool(have), '.github/labels.yml lists labels')
    check({'new-link', 'broken-entry', 'approved', 'link-check'} <= set(used),
          'the label scan finds the labels the automation is known to use')
    missing = {n: sorted(fs) for n, fs in used.items() if n not in have}
    check(not missing, 'every label named in a form or workflow is in labels.yml'
          + ('' if not missing else ' -- missing: %s' % missing))

    print('sources')
    from sources import SOURCES
    bad = [k for k, s in SOURCES.items()
           if not (s.get('licence') or '').strip() or not (s.get('copyright') or '').strip()]
    check(not bad, 'every source states its licence and copyright' + (' -- missing: %s' % bad if bad else ''))
    spdx = re.compile(r'^([A-Za-z0-9.+-]+|unspecified|all-rights-reserved)$')
    odd = [k for k, s in SOURCES.items() if not spdx.match(s.get('licence') or '')]
    check(not odd, 'licence is an SPDX id, "unspecified" or "all-rights-reserved"' + (' -- %s' % odd if odd else ''))
    check('community' in SOURCES, 'submissions have a source of their own (community)')

    print('manual.json')
    manual = json.loads(read(os.path.join(D, 'manual.json')))
    iso = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    nodate = [k for k, v in manual.items() if not iso.match(v.get('d', '')) or not iso.match(v.get('r', ''))]
    check(not nodate, 'every entry has "d" and "r" as YYYY-MM-DD' + (' -- %s' % nodate[:5] if nodate else ''))
    check(all(v.get('s') in ('ok', 'engel') for v in manual.values()), 'every entry has "s" ok or engel')

    print()
    if fails:
        print('%d check(s) failed' % len(fails))
        return 1
    print('all checks passed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
