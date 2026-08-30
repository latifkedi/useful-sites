# -*- coding: utf-8 -*-
"""Unit tests for the pure helper functions build.py and tags.py rely on.

    python data/test_helpers.py

test_build.py checks the build's *output*; this checks a few of the
functions that produce it, the ones a silent regression in would not
show up as a missing record or a thinner category -- a wrong category
mapping or a tag quietly not collapsing, say. Same plain check() style
as test_build.py: no pytest, nothing to install to run this.
"""
import os
import sys

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)

import build                            # noqa: E402  (running this re-runs the build)
import tags                             # noqa: E402

fails = []


def check(ok, msg):
    print(('  ok   ' if ok else '  FAIL ') + msg)
    if not ok:
        fails.append(msg)


def main():
    print('build.key')
    check(build.key('https://WWW.Example.com/path/') == 'example.com/path',
          'strips scheme, www and trailing slash')
    check(build.key('http://example.com') == build.key('https://example.com/'),
          'scheme and trailing slash do not change identity')

    print('build.cat_of')
    check(build.cat_of('Bilişim/Programlama Dilleri/Python') == 'diller',
          'a mapped path resolves to its category')
    check(build.cat_of('Bilişim/Siber Güvenlik') == 'guvenlik',
          'a top-level mapped path resolves correctly')
    check(build.cat_of('Hiç Böyle Bir Yol Yok') == 'araclar',
          'an unmapped path falls back to araclar rather than raising')

    print('tags.normalise')
    check(tags.normalise(['saas', 'açık-kaynak']) == ['ücretli', 'açık-kaynak'],
          'aliases map to their canonical tag, order preserved')
    check(tags.normalise(['bu-etiket-yok']) == [],
          'an unmapped tag is dropped rather than guessed at')
    check(tags.normalise(['python', 'python']) == ['python'],
          'duplicates collapse to one')

    print()
    if fails:
        print('%d check(s) failed' % len(fails))
        return 1
    print('all checks passed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
