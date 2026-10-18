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
    pages(rows)


# ------------------------------------------------------------------ per page
# Every heading page and every goal path gets its own preview: the heading's
# name, its area above it, how many records it holds, and the site's red enso.
# Shared on its own, a heading link used to show the site-wide card, which
# says nothing about where the link goes. Written to og/<key>.png and
# og/path-<slug>.png; emit.py points a page at its image only when the file is
# there. These are not in the service worker's precache (it caches what
# index.html asks for, and the home page never asks for them).
LIMIT = 45 * 1024            # each image stays small; the build does not need them


def floor10(n):
    """48 -> '40+': the image is made by hand, so its number should not go
    stale with every record added; it never claims more than is there."""
    return str(n) if n < 10 else '%d%s' % (n // 10 * 10, '+' if n % 10 else '')


def tr_upper(s):
    """Turkish capitals: i is İ and ı is I (str.upper() gives GELIŞTIRICI)."""
    return s.replace('i', 'İ').replace('ı', 'I').upper()


def fit(d, text, path, size, width):
    """The largest size up to `size` at which text fits in one or two lines."""
    while size > 28:
        f = ImageFont.truetype(path, size * S)
        if d.textlength(text, font=f) <= width * S:
            return f, [text]
        words = text.split(' ')
        for i in range(len(words) - 1, 0, -1):
            a, b = ' '.join(words[:i]), ' '.join(words[i:])
            if d.textlength(a, font=f) <= width * S and d.textlength(b, font=f) <= width * S:
                return f, [a, b]
        size -= 4
    return ImageFont.truetype(path, size * S), [text]


def card(out, kicker, title, sub, foot, host):
    serif = os.path.join(ROOT, 'fonts', 'serif-%d.woff2')
    mark = ImageFont.truetype(serif % 600, 26 * S)
    mono = system_font(MONO, 22 * S)
    subf = ImageFont.truetype(serif % 400, 34 * S)

    img = Image.new('RGB', (W * S, H * S), BG)
    d = ImageDraw.Draw(img)
    enso(d, (W - 150) * S, 300 * S, 230 * S, 11 * S, mix(RED, BG, WM))
    enso(d, (PAD + 18) * S, 96 * S, 18 * S, 5 * S, RED)
    d.text(((PAD + 50) * S, 96 * S), 'Kullanışlı Siteler · Useful Sites', font=mark, fill=FG, anchor='lm')

    d.text((PAD * S, 182 * S), kicker, font=mono, fill=RED)
    hero, lines = fit(d, title, serif % 600, 76, W - 2 * PAD)
    y = 226
    lh = hero.size / S * 1.12
    for ln in lines:
        d.text((PAD * S, y * S), ln, font=hero, fill=FG)
        y += lh
    if sub and sub != title:
        d.text((PAD * S, (y + 14) * S), sub, font=subf, fill=DIM)

    d.line([PAD * S, 494 * S, (W - PAD) * S, 494 * S], fill=RULE, width=S)
    d.text((PAD * S, 522 * S), foot, font=mono, fill=FAINT)
    d.text(((W - PAD) * S, 522 * S), host, font=mono, fill=DIM, anchor='ra')
    img = img.resize((W, H), Image.LANCZOS).quantize(48)
    img.save(out, 'PNG', optimize=True)
    size = os.path.getsize(out)
    if size > LIMIT:
        img.quantize(16).save(out, 'PNG', optimize=True)
        size = os.path.getsize(out)
    return size


def pages(rows):
    from notes import CATS
    from paths import PATHS
    host = SITE.split('//', 1)[-1]
    odir = os.path.join(ROOT, 'og')
    if not os.path.isdir(odir):
        os.makedirs(odir)
    n = {}
    for r in rows:
        n[r['cat']] = n.get(r['cat'], 0) + 1
    field = {k: (g[1], g[2]) for g in GROUPS for k in g[3]}
    jobs = []
    for k, tr, en in CATS:
        if n.get(k):
            f = field.get(k, ('', ''))
            c = floor10(n[k])
            jobs.append((k, '%s · %s' % (tr_upper(f[0]), f[1].upper()), tr, en,
                         '%s BAĞLANTI · %s LINKS' % (c, c)))
    for p in PATHS:
        s = len(p['steps'])
        jobs.append(('path-' + p['en_slug'], 'ÖĞRENME YOLU · LEARNING PATH', p['tr'], p['en'],
                     '%d ADIM · %d STEPS' % (s, s)))
    big = []
    for name, kicker, title, sub, foot in jobs:
        size = card(os.path.join(odir, name + '.png'), kicker, title, sub, foot, host)
        if size > LIMIT:
            big.append(name)
    print('og/: %d images%s' % (len(jobs), ', over %d KB: %s' % (LIMIT // 1024, big) if big else ''))


if __name__ == '__main__':
    main()
