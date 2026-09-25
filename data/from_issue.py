# -*- coding: utf-8 -*-
"""Turns an approved issue into a directory record.

Run by .github/workflows/approve-link.yml when a maintainer puts the
`approved` label on a "Suggest a link" issue. It appends a record to
data/notes/<category>.json, rebuilds, and the workflow opens a pull request with the result.

The point is not to save typing. It is that a submission which sits in an
issue is worth nothing until someone transcribes it, and transcription is
exactly the step that gets postponed. This closes that gap while leaving the
final say with a human: the workflow opens a PR, it does not merge one.

Nothing here trusts the issue text. The URL is checked, duplicates are
refused, tags go through the canonical table, and the record is written as JSON
data -- there is no code for a submission to break into.
"""
import io
import json
import os
import re
import sys

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)

from notes import CATS, load_records  # noqa: E402
from tags import normalise            # noqa: E402
from sources import DEFAULT           # noqa: E402

NOTES = os.path.join(D, 'notes')
CAT_BY_EN = dict((c[2], c[0]) for c in CATS)


class Refused(Exception):
    """Something in the issue makes it unusable. The workflow reports it."""


def fields(body):
    """Splits a GitHub issue-form body into {heading: value}.

    Issue forms render as '### Label' followed by the value. Empty optional
    fields come through as the literal '_No response_'.
    """
    out, key, buf = {}, None, []
    for line in (body or '').replace('\r\n', '\n').split('\n'):
        if line.startswith('### '):
            if key:
                out[key] = '\n'.join(buf).strip()
            key, buf = line[4:].strip().lower(), []
        elif key:
            buf.append(line)
    if key:
        out[key] = '\n'.join(buf).strip()
    for k, v in list(out.items()):
        if v == '_No response_':
            out[k] = ''
    return out


def norm(u):
    u = re.sub(r'^https?://', '', u.strip().lower())
    u = re.sub(r'^www\.', '', u)
    return u.rstrip('/')


def parse(body):
    f = fields(body)
    url = f.get('url', '').strip()
    if not re.match(r'^https?://[^\s<>"]+\.[^\s<>"]+$', url):
        raise Refused('URL does not look like a URL: %r' % url[:120])
    if len(url) > 400:
        raise Refused('URL is absurdly long')

    name = ' '.join(f.get('name', '').split())[:80]
    if not name:
        raise Refused('Name is empty')

    what = ' '.join(f.get('what does it do?', '').split())
    diff = ' '.join(f.get('how does it differ?', '').split())
    if not what:
        raise Refused('"What does it do?" is empty')

    cat = CAT_BY_EN.get(f.get('category', '').strip())

    raw = [t.strip() for t in re.split(r'[,;]', f.get('tags (optional)', '')) if t.strip()]
    tg = normalise(raw)[:6]

    return {'url': url, 'name': name, 'cat': cat, 'tags': tg,
            'what': what[:400], 'diff': diff[:400]}


def already_there(url):
    # Checked against the notes themselves, not the built links.js: the notes
    # are the source of truth, and links.js can lag behind an unbuilt edit.
    have = set()
    for d in load_records(NOTES):
        k = norm(d['url'])
        have.add(k)
        have.add(re.split(r'[?#]', k)[0].rstrip('/'))
    k = norm(url)
    return k in have or re.split(r'[?#]', k)[0].rstrip('/') in have


def record(rec, issue):
    """The note to append, as plain data.

    Nothing from the issue is ever written as code any more: notes are JSON,
    so a crafted description has nothing to break out into. The submitter
    wrote one language in one voice, so both fields carry the same text, and
    the "review" field says so -- test_build.py fails while it is present,
    which keeps the pull request red until a person has done the pass.
    """
    tr = rec['what'] + ((' ' + rec['diff']) if rec['diff'] else '')
    why = 'from issue #%d -- description needs a pass: one language, one voice' % issue
    if not rec['cat']:
        why += '; category was "Not sure", filed under araclar'
    return {'url': rec['url'], 'name': rec['name'], 'tags': rec['tags'],
            'tr': tr, 'en': tr, 'src': DEFAULT, 'review': why}


def append(note, cat):
    path = os.path.join(NOTES, cat + '.json')
    have = json.load(io.open(path, encoding='utf-8')) if os.path.exists(path) else []
    io.open(path, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(have + [note], ensure_ascii=False, indent=2) + '\n')


def main():
    body = os.environ.get('ISSUE_BODY', '')
    issue = int(os.environ.get('ISSUE_NUMBER', '0') or 0)
    try:
        rec = parse(body)
        if already_there(rec['url']):
            raise Refused('This URL is already in the directory')
    except Refused as e:
        io.open(os.path.join(D, '..', 'issue-error.txt'), 'w',
                encoding='utf-8').write(str(e))
        print('refused:', e)
        return 1

    cat = rec['cat'] or 'araclar'
    append(record(rec, issue), cat)
    print('appended to notes/%s.json:' % cat, rec['name'], '->', rec['url'])
    print('category:', rec['cat'] or 'araclar (was Not sure)')
    print('tags    :', rec['tags'] or '(none)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
