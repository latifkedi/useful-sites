# -*- coding: utf-8 -*-
"""How many records touch each topic, to see where the directory is thin.

    python data/coverage.py

A rough instrument: it counts records whose name, tags or English description
contain a topic's words, so "regex" also counts a tutorial that merely mentions
it. Use it to spot a gap, not to measure one. The topics are the ones a
programmer, a data person or a maker is likely to look for; CONTRIBUTING.md says
which of them the directory wants more of and which it leaves out on purpose.
"""
import io
import os
import re
import sys

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)

import readlinks   # noqa: E402

ROOT = os.path.join(D, '..')

# topic -> regex over "name + tags + descriptions", or 'tag:<canonical tag>' to count
# a tag exactly. The natural sciences (chemistry, biology, astronomy) and hobbies
# (chess) were dropped: CONTRIBUTING.md leaves them out on purpose, so counting them
# only produced gaps nobody intends to fill.
TOPICS = {
    'WebAssembly': r'webassembly|\bwasm\b',
    'Accessibility (a11y)': r'accessib|\ba11y\b|wcag',
    'Regular expressions': r'\bregex|regular expression',
    'LaTeX / typesetting': r'latex|typesetting',
    'GIS / maps': r'\bgis\b|openstreetmap|geospatial|cartograph|geojson|shapefile',
    'Compilers / interpreters': r'compiler|interpreter|parser',
    'Operating-system internals': r'kernel|operating system',
    'Embedded / microcontrollers': r'arduino|microcontroller|embedded|esp32|raspberry',
    'Game development': r'game dev|gamedev|unity|godot|unreal',
    'Cryptography': r'cryptograph|encryption',
    'Digital audio / music': r'\bmusic\b|\baudio\b|synth',
    'Video / streaming': r'\bvideo\b|streaming|ffmpeg',
    'Linguistics / languages': r'linguist|language learning|dictionary|grammar',
    'Low-code / no-code': r'low-code|no-code|nocode',
    'Open hardware / 3D printing': r'3d print|open hardware|cad\b',
    'Law / regulation': r'\bgdpr\b|\blaw\b|legal|regulation|legislation|mevzuat|kvkk',
    'Research tools (citations, literature)': r'reference manager|citation|literature|scholarly|bibliograph',
    'Turkish-language resources': 'tag:türkçe',
    'Accessibility of content (reading)': r'screen reader|dyslexi',
    'Career / interviews': r'interview|career|resume|\bcv\b',
    'Developer experience / docs': r'documentation|docs',
    'Performance / profiling': r'profil|performance|benchmark',
    'Observability / monitoring': r'observab|monitoring|tracing',
}


def counts(rows=None):
    """[(count, topic)] in TOPICS order. test_build compares CONTRIBUTING.md's
    bracketed numbers with these."""
    rows = rows if rows is not None else readlinks.read(ROOT)
    texts = [' '.join([r['name']] + r.get('tags', []) + [r.get('tr', '')]).lower() for r in rows]
    en_path = os.path.join(ROOT, 'links.en.js')
    import json
    src = io.open(en_path, encoding='utf-8').read()
    en = json.loads(src[src.index('['):src.rindex(';')])
    texts = [t + ' ' + e.lower() for t, e in zip(texts, en)]
    out = []
    for name, pat in TOPICS.items():
        if pat.startswith('tag:'):
            n = sum(1 for r in rows if pat[4:] in r.get('tags', []))
        else:
            rx = re.compile(pat, re.I)
            n = sum(1 for t in texts if rx.search(t))
        out.append((n, name))
    return out


def main():
    rows = readlinks.read(ROOT)
    print('%d records' % len(rows))
    for n, name in sorted(counts(rows)):
        print('%5d  %s' % (n, name))


if __name__ == '__main__':
    main()
