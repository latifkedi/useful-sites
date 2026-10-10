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

# topic -> regex over "name + tags + English description"
TOPICS = {
    'WebAssembly': r'webassembly|\bwasm\b',
    'Accessibility (a11y)': r'accessib|\ba11y\b|wcag',
    'Regular expressions': r'\bregex|regular expression',
    'LaTeX / typesetting': r'latex|typesetting',
    'GIS / maps': r'\bgis\b|openstreetmap|geospatial|cartograph',
    'Compilers / interpreters': r'compiler|interpreter|parser',
    'Operating-system internals': r'kernel|operating system',
    'Embedded / microcontrollers': r'arduino|microcontroller|embedded|esp32|raspberry',
    'Game development': r'game dev|gamedev|unity|godot|unreal',
    'Cryptography': r'cryptograph|encryption',
    'Digital audio / music': r'\bmusic\b|\baudio\b|synth',
    'Video / streaming': r'\bvideo\b|streaming|ffmpeg',
    'Chess / puzzles': r'\bchess\b|puzzle',
    'Astronomy / space': r'astronom|\bspace\b|telescope',
    'Biology / genomics': r'biolog|genom|bioinformat',
    'Chemistry': r'chemi',
    'Linguistics / languages': r'linguist|language learning|dictionary|grammar',
    'Low-code / no-code': r'low-code|no-code|nocode',
    'Open hardware / 3D printing': r'3d print|open hardware|cad\b',
    'Law / privacy regulation': r'\bgdpr\b|\blaw\b|legal|regulation',
    'Accessibility of content (reading)': r'screen reader|dyslexi',
    'Career / interviews': r'interview|career|resume|\bcv\b',
    'Developer experience / docs': r'documentation|docs',
    'Performance / profiling': r'profil|performance|benchmark',
    'Observability / monitoring': r'observab|monitoring|tracing',
}


def main():
    rows = readlinks.read(ROOT)
    texts = [' '.join([r['name']] + r.get('tags', []) + [r.get('tr', '')]).lower() for r in rows]
    en_path = os.path.join(ROOT, 'links.en.js')
    import json
    src = io.open(en_path, encoding='utf-8').read()
    en = json.loads(src[src.index('['):src.rindex(';')])
    texts = [t + ' ' + e.lower() for t, e in zip(texts, en)]
    out = []
    for name, pat in TOPICS.items():
        rx = re.compile(pat, re.I)
        n = sum(1 for t in texts if rx.search(t))
        out.append((n, name))
    print('%d records' % len(rows))
    for n, name in sorted(out):
        print('%5d  %s' % (n, name))


if __name__ == '__main__':
    main()
