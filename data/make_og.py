# -*- coding: utf-8 -*-
"""Regenerates og.png, the social preview image.

The image is committed, but it carries the record count and the site address
baked into the pixels, so it goes stale silently whenever either changes. This
script existed only as a scratch file for a while, which meant nobody could
regenerate it -- that is the gap this file closes.

    python data/make_og.py

The count is read from links.js rather than passed in, so it cannot drift. The
title uses the serif the site already ships; the remaining lines fall back
through a list of system faces, since bundling a sans and a mono purely for
this one image is not worth the bytes.

Needs Pillow, which is not otherwise a dependency:  pip install pillow
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(D)
sys.path.insert(0, D)
import readlinks                          # noqa: E402
from emit import SITE                     # noqa: E402
from notes import GROUPS                  # noqa: E402

W, H = 1200, 630
S = 2                        # supersampling factor
# The fihrist tokens (style.css :root, light): ink on paper, one red.
BG = (246, 241, 231)         # --bg
FG = (28, 26, 22)            # --fg
DIM = (91, 86, 76)           # --dim
FAINT = (104, 98, 86)        # --faint, WCAG AA on every background it sits on
RULE = (221, 213, 196)       # --rule
RED = (168, 50, 31)          # --red
WM = 0.12                    # the watermark enso's opacity over the paper
PAD = 84

MONO = ['consola.ttf', 'DejaVuSansMono.ttf', 'cour.ttf',
        'LiberationMono-Regular.ttf']
DIRS = [r'C:\Windows\Fonts', '/usr/share/fonts/truetype/dejavu',
        '/usr/share/fonts/truetype/liberation', '/Library/Fonts']


def system_font(names, size):
    for d in DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def mix(a, b, t):
    """a laid over b at opacity t."""
    return tuple(round(b[i] + (a[i] - b[i]) * t) for i in range(3))


def enso(d, cx, cy, r, w, colour):
    """The site's enso (M43 12 A22 22 0 1 0 51 30): an open circle whose gap
    sits between three o'clock and the upper right, with round ends."""
    d.arc([cx - r, cy - r, cx + r, cy + r], 0, 306, fill=colour, width=w)
    for deg in (0, 306):
        a = math.radians(deg)
        ex = cx + (r - w / 2) * math.cos(a)
        ey = cy + (r - w / 2) * math.sin(a)
        d.ellipse([ex - w / 2, ey - w / 2, ex + w / 2, ey + w / 2], fill=colour)


def count(n):
    f = n // 100 * 100
    return '{:,}'.format(f).replace(',', '.') + ('+' if n > f else '')


def main():
    rows = readlinks.read(ROOT)
    n = len(rows)
    cats = len({r['cat'] for r in rows})
    fields = len(GROUPS)
    host = SITE.split('//', 1)[-1]

    # Drawn at twice the size and scaled down: Pillow does not antialias arcs,
    # and the enso's edges show it at 1x.
    serif = os.path.join(ROOT, 'fonts', 'serif-%d.woff2')
    mark = ImageFont.truetype(serif % 600, 30 * S)
    hero = ImageFont.truetype(serif % 400, 64 * S)
    mono = system_font(MONO, 23 * S)

    img = Image.new('RGB', (W * S, H * S), BG)
    d = ImageDraw.Draw(img)

    # The watermark enso behind the hero, as on the home page, and the small
    # one that stands in for a logo.
    enso(d, (W - 190) * S, 250 * S, 250 * S, 11 * S, mix(RED, BG, WM))
    enso(d, (PAD + 20) * S, 104 * S, 20 * S, 5 * S, RED)
    d.text(((PAD + 56) * S, 104 * S), 'Kullanışlı Siteler', font=mark, fill=FG,
           anchor='lm')

    # The hero sentence, with the count in red like the page's <em>.
    x, y = PAD * S, 200 * S
    for part, colour in (('Elle derlenmiş ', FG), (count(n), RED),
                         (' bağlantı.', FG)):
        d.text((x, y), part, font=hero, fill=colour)
        x += d.textlength(part, font=hero)
    d.text((PAD * S, y + 82 * S), 'Her biri benzerlerinden nerede',
           font=hero, fill=DIM)
    d.text((PAD * S, y + 164 * S), 'ayrıldığını söylüyor.', font=hero, fill=DIM)

    d.line([PAD * S, 494 * S, (W - PAD) * S, 494 * S], fill=RULE, width=S)
    lead = '%d ALAN · %d BAŞLIK' % (fields, cats)
    d.text((PAD * S, 522 * S), lead, font=mono, fill=FAINT)
    d.text(((W - PAD) * S, 522 * S), host, font=mono, fill=DIM, anchor='ra')
    # A handful of inks on one paper: a 128-colour palette loses nothing
    # visible and halves the file.
    img = img.resize((W, H), Image.LANCZOS).quantize(128)

    out = os.path.join(ROOT, 'og.png')
    img.save(out, 'PNG', optimize=True)
    print('og.png: %d records, %s, %.1f KB'
          % (n, host, os.path.getsize(out) / 1024))


if __name__ == '__main__':
    main()
