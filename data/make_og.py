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
import io
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
# The site's monochrome ink-on-paper tokens (index.html :root).
BG = (250, 249, 245)
FG = (20, 19, 16)
DIM = (99, 96, 90)
FAINT = (110, 107, 99)       # --faint, WCAG AA against the background
RULE = (227, 223, 214)
MOTIF = (233, 229, 220)      # the background circles, barely there
PAD = 84

SANS = ['segoeui.ttf', 'DejaVuSans.ttf', 'Arial.ttf', 'arial.ttf',
        'LiberationSans-Regular.ttf']
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


def count(n):
    f = n // 100 * 100
    return '{:,}'.format(f).replace(',', '.') + ('+' if n > f else '')


def main():
    rows = readlinks.read(ROOT)
    n = len(rows)
    cats = len({r['cat'] for r in rows})
    fields = len(GROUPS)
    host = SITE.split('//', 1)[-1]

    title = ImageFont.truetype(os.path.join(ROOT, 'fonts', 'serif-600.woff2'), 76)
    body = system_font(SANS, 31)
    mono = system_font(MONO, 23)

    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)

    # The same quiet concentric-circle motif the site draws behind its content.
    cx, cy = W - 96, 96
    for r in (70, 140, 215, 300, 395):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=MOTIF, width=2)

    d.text((PAD, 150), 'Kullanışlı Siteler', font=title, fill=FG)
    d.text((PAD, 264), 'Her kayıtta bağlantının ne yaptığı ve', font=body, fill=DIM)
    d.text((PAD, 308), 'benzerlerinden nerede ayrıldığı yazılı.', font=body, fill=DIM)
    d.line([PAD, 404, W - PAD, 404], fill=RULE, width=1)
    lead = '%s BAĞLANTI' % count(n)
    d.text((PAD, 432), lead, font=mono, fill=FG)
    d.text((PAD + d.textlength(lead + '   ', font=mono), 432),
           '%d ALAN · %d BAŞLIK' % (fields, cats), font=mono, fill=FAINT)
    d.text((PAD, 502), host, font=mono, fill=DIM)

    out = os.path.join(ROOT, 'og.png')
    img.save(out, 'PNG', optimize=True)
    print('og.png: %d records, %s, %.1f KB'
          % (n, host, os.path.getsize(out) / 1024))


if __name__ == '__main__':
    main()
