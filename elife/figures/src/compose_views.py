#!/usr/bin/env python3
"""Compose fig-views from the modeler's own view captures (views.mjs): the Gantt chart across the page, the
provenance log under it, and the checklist cards in two columns below, for a 180 mm page width.
Usage: compose_views.py <captures dir> <out.png>"""
import glob, os, struct, sys, zlib
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1:3]
W = 5400; PAD = 30; GAP = 60; LABEL_H = 90  # W pixels print at 180 mm
font = next(ImageFont.truetype(p, 64) for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf') if os.path.exists(p))
FULL = W - 2 * PAD
COL = (FULL - GAP) // 2
def fit_w(path, w):
    im = Image.open(path).convert('RGB'); return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
gantt = fit_w(f'{src}/view-gantt.png', FULL)
prov = fit_w(f'{src}/view-provenance.png', FULL)
cards = [fit_w(p, COL) for p in sorted(glob.glob(f'{src}/view-checklist-*.png'))]
left, right = cards[:-1], cards[-1:]  # the last card alone on the right
col_h = lambda ims: sum(im.height for im in ims) + GAP // 2 * max(0, len(ims) - 1)
H = PAD + LABEL_H + gantt.height + GAP + LABEL_H + prov.height + GAP + LABEL_H + max(col_h(left), col_h(right)) + PAD
canvas = Image.new('RGB', (W, H), 'white')
draw = ImageDraw.Draw(canvas)
def label(x, y, letter, title):
    draw.text((x, y), f'{letter}  {title}', fill='black', font=font); return y + LABEL_H
y = label(PAD, PAD, 'a', 'Gantt view'); canvas.paste(gantt, (PAD, y)); y += gantt.height + GAP
y = label(PAD, y, 'b', 'Provenance view'); canvas.paste(prov, (PAD, y)); y += prov.height + GAP
y = label(PAD, y, 'c', 'Checklist view')
for x, ims in ((PAD, left), (PAD + COL + GAP, right)):
    yy = y
    for im in ims: canvas.paste(im, (x, yy)); yy += im.height + GAP // 2
canvas.save(out)
png = open(out, 'rb').read(); ppm = round(W / 0.180)  # pHYs: the composite prints 180 mm wide
body = b'pHYs' + struct.pack('>IIB', ppm, ppm, 1)
open(out, 'wb').write(png[:33] + struct.pack('>I', 9) + body + struct.pack('>I', zlib.crc32(body)) + png[33:])
print(out, canvas.size, f'{W/ppm*1000:.0f} x {H/ppm*1000:.0f} mm')
