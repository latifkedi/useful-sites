# -*- coding: utf-8 -*-
"""Reads the record list back out of links.js.

This is its own module because of a bug. Every script used to do it with
`src[src.index('['):src.rindex(';')]`. Then window.TAGLABELS was added to
links.js, its first `[` now comes earlier in the file, and the slice landed
on malformed JSON -- both CI scripts started failing silently. The workflow
had continue-on-error set, so it stayed green for weeks while doing nothing.

This reader looks for the window.LINKS= marker explicitly and finds the end
of the array by counting brackets. Adding another variable to links.js does
not break it.
"""
import io
import json
import os

MARK = 'window.LINKS='


def _labelled(rows):
    # links.js no longer repeats the category labels on every record; the CI
    # scripts still report by label, so they are put back here from notes.CATS.
    from notes import CATS
    lbl = {c[0]: (c[1], c[2]) for c in CATS}
    out = []
    for d in rows:
        tr, en = lbl.get(d.get('cat'), (d.get('cat', ''), d.get('cat', '')))
        out.append(dict(d, cat_tr=tr, cat_en=en))
    return out


def read(root):
    path = os.path.join(root, 'links.js')
    src = io.open(path, encoding='utf-8').read()

    i = src.find(MARK)
    if i < 0:
        raise ValueError('links.js icinde %s yok' % MARK)
    i += len(MARK)
    if src[i] != '[':
        raise ValueError('%s ardindan dizi beklenirken %r geldi' % (MARK, src[i]))

    depth, instr, esc = 0, False, False
    for j in range(i, len(src)):
        c = src[j]
        if instr:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                instr = False
            continue
        if c == '"':
            instr = True
        elif c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                return _labelled(json.loads(src[i:j + 1]))
    raise ValueError('links.js icindeki dizi kapanmiyor')
