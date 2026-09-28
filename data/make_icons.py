# -*- coding: utf-8 -*-
"""Regenerates the app icons in icons/: the site's enso, red on paper.

    python data/make_icons.py

They are committed; rerun this only when the mark or the palette changes.
The enso is drawn with make_og.py's helper, so the icons, the social image
and the header logo stay one shape (M43 12 A22 22 0 1 0 51 30 in a 60-unit
box, stroke 5). The maskable icon keeps the enso inside the central 80%,
the safe zone that launchers may crop to a circle or squircle.

Needs Pillow, which is not otherwise a dependency:  pip install pillow
"""
import os
import sys

from PIL import Image, ImageDraw

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(D)
sys.path.insert(0, D)
from make_og import BG, RED, S, enso     # noqa: E402

OUT = os.path.join(ROOT, 'icons')

# name, size, enso radius and stroke as fractions of the size
ICONS = [
    ('icon-192.png', 192, 22 / 60, 5 / 60),
    ('icon-512.png', 512, 22 / 60, 5 / 60),
    ('apple-touch-icon.png', 180, 22 / 60, 5 / 60),
    ('icon-maskable-512.png', 512, 0.28, 0.064),
]


def draw(size, r, w):
    big = size * S
    img = Image.new('RGB', (big, big), BG)
    enso(ImageDraw.Draw(img), big / 2, big / 2, r * big, max(2, round(w * big)), RED)
    return img.resize((size, size), Image.LANCZOS).quantize(64)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, size, r, w in ICONS:
        p = os.path.join(OUT, name)
        draw(size, r, w).save(p, 'PNG', optimize=True)
        print('%-24s %4d px  %5.1f KB' % (name, size, os.path.getsize(p) / 1024))


if __name__ == '__main__':
    main()
