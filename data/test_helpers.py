# -*- coding: utf-8 -*-
"""Unit tests for the pure helper functions build.py and tags.py rely on.

    python data/test_helpers.py

test_build.py checks the build's *output*; this checks a few of the
functions that produce it, the ones a silent regression in would not
show up as a missing record or a thinner category -- a note file that
loads when it should not, or a tag quietly not collapsing, say. Same plain
check() style as test_build.py: no pytest, nothing to install to run this.
"""
import datetime
import io
import json
import os
import shutil
import sys
import tempfile

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)

import build                            # noqa: E402  (running this re-runs the build)
import emit                             # noqa: E402
import from_issue                       # noqa: E402
import linkstate                       # noqa: E402
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

    print('linkstate.github_target')
    gt = linkstate.github_target
    check(gt('https://github.com/donnemartin/system-design-primer') == ('repo', 'donnemartin', 'system-design-primer'),
          'an owner/repo URL is a repository')
    check(gt('https://github.com/foo/bar/tree/main/docs') == ('repo', 'foo', 'bar'),
          'a path inside a repository still names that repository')
    check(gt('https://github.com/foo/bar.git') == ('repo', 'foo', 'bar'), 'a .git suffix is not part of the name')
    check(all(gt(u)[0] == 'page' for u in ('https://github.com/scoverage', 'https://github.com/LiteEMF?tab=repositories',
                                           'https://github.com/even-realities/', 'https://github.com/foo/repositories')),
          'user and organisation pages (and their tabs) are not repositories')
    check(gt('https://github.com/topics/rust') is None and gt('https://example.com/x') is None,
          'GitHub feature pages and other sites are neither')

    print('linkstate: name check, recheck, orphans')
    check(not linkstate.name_check_applies('https://www.youtube.com/@abdul_bari/videos', 'Abdul Bari'),
          'a YouTube page cannot be judged by its words')
    check(not linkstate.name_check_applies('https://example.com/', '  '), 'a page with no title cannot be judged by its words')
    check(linkstate.name_check_applies('https://example.com/', 'Example'), 'an ordinary page with a title can')
    check(linkstate.recheck_due({'d': '2025-01-01'}, '2026-10-10'), 'a decision older than a year is due without an r')
    check(not linkstate.recheck_due({'d': '2026-06-01'}, '2026-10-10'), 'a recent decision without an r is not due')
    check(linkstate.recheck_due({'d': '2026-06-01', 'r': '2026-10-01'}, '2026-10-10'), 'a passed r is due')
    check(not linkstate.recheck_due({'d': '2026-01-01', 'r': '2027-01-01'}, '2026-10-10'), 'r overrides the year rule')
    check(linkstate.recheck_date('2026-10-10') == '2027-04-08', 'a new decision is looked at again in 180 days')
    check(linkstate.orphan_keys(['a.com', 'b.com/x', 'gone.com'], ['https://a.com/', 'https://b.com/x?y=1'],
                                lambda u: u.split('://')[1].rstrip('/')) == ['gone.com'],
          'orphan_keys finds the key no record carries, matching with or without the query')

    print('linkstate.stale_years')
    check(linkstate.stale_years('Heroku dropped its free tier in 2022.', 2026) == [],
          'a past-tense fact with an old year is not stale')
    check(linkstate.stale_years('The latest release is from 2023.', 2026) == [2023],
          'an old year beside "latest" is a claim that can go stale')
    check(linkstate.stale_years('Son sürüm 2022, depo durgun.', 2026) == [2022], 'the Turkish form is caught too')
    check(linkstate.stale_years('The latest release is from 2025.', 2026) == [], 'a recent year is fine')

    print('linkstate freshness tiers')
    check(linkstate.recheck_days('yz_model') == 90 and linkstate.recheck_days('finans') == 90,
          'AI categories and finance/crypto are rechecked every 90 days')
    check(linkstate.recheck_days('kitaplik') == 365 and linkstate.recheck_days(None) == 365,
          'everything else every 365 days')
    t0 = 1767225600   # 2026-01-01
    check(not linkstate.description_due('yz_arac', 'https://a.dev', t0, '2026-02-01'),
          'a record is not due before one interval has passed since it arrived')
    check(linkstate.description_due('yz_arac', 'https://a.dev', t0, '2026-04-01')
          and not linkstate.description_due('yz_arac', 'https://a.dev', t0, '2026-04-08'),
          'it falls due in the week its 90-day interval ends, and only that week')
    check(not linkstate.description_due('web', 'https://a.dev', t0, '2026-04-01')
          and linkstate.description_due('web', 'https://a.dev', t0, '2027-01-01'),
          'the 365-day tier is due a year after arrival, not at 90 days')
    days = [(datetime.date(2026, 1, 5) + datetime.timedelta(days=n)).isoformat() for n in range(90)]
    check(sum(linkstate.description_due('finans', 'https://no-date.example', None, d) for d in days) == 7,
          'a record without an arrival date is due for one week in every 90 days (phase from its URL)')
    check(linkstate.time_claims('Free tier, now in beta; join the waitlist.') == ['beta', 'free', 'waitlist'],
          'price, beta and waitlist claims are found')
    check(linkstate.time_claims('A lock-free queue with a free-form schema.') == [],
          '"lock-free" and "free-form" are not price claims')
    check(linkstate.time_claims('Ücretsiz planı var.') == ['ücretsiz'], 'the Turkish form is caught too')
    due_rows = [{'cat': 'yz_arac', 'url': 'https://x%d.dev' % i, 'added': t0, 'tr': '', 'en': 'Free to use.'}
                for i in range(30)]
    due_rows.append({'cat': 'yz_arac', 'url': 'https://plain.dev', 'added': t0, 'tr': '', 'en': 'A tool.'})
    picked, over = linkstate.claim_rechecks(due_rows, '2026-04-01', cap=25)
    check(len(picked) == 25 and over == 5 and all(r['claims'] == ['free'] for r in picked),
          'the weekly claim list is capped, the overflow counted, records without a claim left out')

    print('from_issue: tag cap and removed URLs')
    check(from_issue.cap_tags(['ücretsiz', 'a', 'b', 'açık-kaynak', 'c', 'd', 'e']) == ['ücretsiz', 'a', 'b', 'açık-kaynak', 'c', 'd'],
          'at most four tags besides price and licence survive, price and licence untouched')
    tmpf = tempfile.mkdtemp()
    try:
        rp = os.path.join(tmpf, 'removed.txt')
        io.open(rp, 'w', encoding='utf-8').write('# comment\nhttps://www.gone.example/\tcrypto news\n')
        check(from_issue.removed_reason('http://gone.example', rp) == 'crypto news',
              'a URL in removed.txt is found by its key, with its reason')
        check(from_issue.removed_reason('https://kept.example', rp) is None
              and from_issue.removed_reason('https://x.example', os.path.join(tmpf, 'none.txt')) is None,
              'an unlisted URL, or no removed.txt at all, is not refused')
    finally:
        shutil.rmtree(tmpf)

    print('linkstate.may_write')
    check(not linkstate.may_write(['ci_check.py'], {}), 'a scan run by hand leaves verified.json and health.json alone')
    check(linkstate.may_write(['ci_check.py', '--write'], {}), '--write lets a scan refresh them')
    check(linkstate.may_write([], {'GITHUB_ACTIONS': 'true'}), 'the weekly workflow refreshes them')
    check(not linkstate.may_write([], {'GITHUB_ACTIONS': 'false'}), 'only a real Actions run counts')

    print('linkstate.classify')
    check(linkstate.classify(None) == 'ok', 'no failure is ok')
    check(linkstate.classify({'status': 404}) == 'dead', '404 is dead')
    check(linkstate.classify({'status': 0, 'dns': True}) == 'dead',
          'a host name that does not resolve is dead')
    check(all(linkstate.classify({'status': c}) == 'suspect' for c in (400, 403, 418, 429, 503, 522)),
          'other codes are suspect, not dead -- the 400/418 false Dead badges')
    check(linkstate.classify({'status': 0, 'error': 'ReadTimeout', 'dns': False}) == 'suspect',
          'a timeout is suspect, not dead')

    print('linkstate.next_state')
    day = '2026-09-28'
    once = linkstate.next_state({'d': '2026-09-21', 's': 'ok'}, 'dead', None, day)
    check(once['s'] == 'engel' and once['f'] == 1,
          'one dead scan is not enough for a Dead badge')
    twice = linkstate.next_state(once, 'dead', None, '2026-10-05')
    check(twice['s'] == 'olu' and twice['f'] == 2 and twice['d'] == day,
          'the second consecutive dead scan marks it dead and keeps the last good date')
    check(linkstate.next_state(twice, 'ok', None, day) == {'d': day, 's': 'ok'},
          'a good scan clears the count')
    check(linkstate.next_state(once, 'suspect', None, day).get('f') == 1,
          'a suspect scan neither confirms nor clears the count')
    check(linkstate.next_state(twice, 'dead', {'s': 'ok'}, day) == {'d': day, 's': 'ok'},
          'a manual decision wins over the scan')

    print('tags.normalise')
    check(tags.normalise(['saas', 'açık-kaynak']) == ['ücretli', 'açık-kaynak'],
          'aliases map to their canonical tag, order preserved')
    check(tags.normalise(['bu-etiket-yok']) == [],
          'an unmapped tag is dropped rather than guessed at')
    check(tags.normalise(['python', 'python']) == ['python'],
          'duplicates collapse to one')

    # The same three cases as test_search.js checks against app.js
    # firstSentence(); the pre-rendered home depends on the two agreeing.
    print('emit._first')
    one = 'Bu bir kayıt açıklamasıdır ve kırk karakteri rahatça geçer. İkinci cümle.'
    check(emit._first(one) == 'Bu bir kayıt açıklamasıdır ve kırk karakteri rahatça geçer.',
          'returns the first sentence of 40-150 characters')
    check(emit._first('Kısa, noktasız bir not') == 'Kısa, noktasız bir not',
          'a short text without a full stop comes back whole')
    check(emit._first('kelime ' * 30) == ' '.join(['kelime'] * 17) + '…',
          'a long text without one is cut at a word, with an ellipsis')
    check(emit._first('abcdefghi, ' * 20) == ', '.join(['abcdefghi'] * 10) + '…',
          'the cut drops a dangling comma before the ellipsis')

    print()
    if fails:
        print('%d check(s) failed' % len(fails))
        return 1
    print('all checks passed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
