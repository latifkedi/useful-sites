# -*- coding: utf-8 -*-
"""Unit tests for the pure helper functions build.py and tags.py rely on.

    python data/test_helpers.py

test_build.py checks the build's *output*; this checks a few of the
functions that produce it, the ones a silent regression in would not
show up as a missing record or a thinner category -- a note file that
loads when it should not, or a tag quietly not collapsing, say. Same plain
check() style as test_build.py: no pytest, nothing to install to run this.
"""
import io
import json
import os
import shutil
import sys
import tempfile

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)

import build                            # noqa: E402  (running this re-runs the build)
import notes                            # noqa: E402
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

    print('notes.validate')
    src = {'kedi': {}}
    good = {'url': 'https://a.dev', 'name': 'A', 'tags': ['python'],
            'tr': 'Bir şey.', 'en': 'A thing.', 'src': 'kedi'}
    check(notes.validate(good, src) == [], 'a complete record has no problems')
    check(any('missing "tr"' in p for p in notes.validate(
        {k: v for k, v in good.items() if k != 'tr'}, src)),
        'a missing required field is reported by name')
    check(any('url' in p for p in notes.validate(dict(good, url='javascript:alert(1)'), src)),
          'a non-http(s) URL is refused (esc() cannot stop a javascript: scheme)')
    check(any('unknown source' in p for p in notes.validate(dict(good, src='nope'), src)),
          'an undeclared source is refused')
    check(any('unknown field' in p for p in notes.validate(dict(good, cat='web'), src)),
          'an unknown field is refused (the category is the file, not a field)')
    check(any('added' in p for p in notes.validate(dict(good, added='2026'), src)),
          '"added" must be an integer')

    print('notes.load_records')
    tmp = tempfile.mkdtemp()
    try:
        def put(name, recs):
            io.open(os.path.join(tmp, name), 'w', encoding='utf-8').write(json.dumps(recs))
        put('web.json', [good])
        put('ag.json', [dict(good, url='https://b.dev', name='B')])
        recs = notes.load_records(tmp, src)
        check([r['cat'] for r in recs] == ['web', 'ag'],
              'records come back in CATS order, each tagged with its file as category')
        check(recs[0] is not good and 'cat' not in good,
              'the loader returns new objects and leaves the input untouched')

        put('ag.json', [dict(good, url='http://www.a.dev/')])
        try:
            notes.load_records(tmp, src)
            check(False, 'a duplicate URL across files raises')
        except notes.NoteError as e:
            check('duplicate URL' in str(e) and 'web.json #1' in str(e),
                  'a duplicate URL across files raises, naming where the first one is')

        os.remove(os.path.join(tmp, 'ag.json'))
        put('yok_boyle.json', [])
        try:
            notes.load_records(tmp, src)
            check(False, 'a file for an undeclared category raises')
        except notes.NoteError:
            check(True, 'a file for an undeclared category raises')

        os.remove(os.path.join(tmp, 'yok_boyle.json'))
        io.open(os.path.join(tmp, 'web.json'), 'w', encoding='utf-8').write('[{"url": ')
        try:
            notes.load_records(tmp, src)
            check(False, 'broken JSON raises instead of silently dropping records')
        except notes.NoteError:
            check(True, 'broken JSON raises instead of silently dropping records')
    finally:
        shutil.rmtree(tmp)

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
