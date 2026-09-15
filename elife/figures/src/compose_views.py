#!/usr/bin/env python3
"""Compose fig-views from the Study view (the battery, cropped from fig-combined), the Gantt/Checklist/Provenance
dialog captures, and the Figure view (fig-consort), for a 180 mm page: (a) and (b) down the left column, (e) down
the right, (c) and (d) side by side below.
Usage: compose_views.py <study.png> <gantt.png> <checklist.png> <provenance.png> <figure.png> <out.png>"""
import os, struct, sys, zlib
from PIL import Image, ImageDraw, ImageFont
study, gantt, check, prov, figure, out = sys.argv[1:7]
W = 5400; PAD = 40; GAP = 80; LABEL_H = 110  # W pixels print at 180 mm
font = next(ImageFont.truetype(p, 72) for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf') if os.path.exists(p))
COL = (W - 2 * PAD - GAP) // 2
def fit_w(path, w):
    im = Image.open(path).convert('RGB'); return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
a, b, e, c, d = (fit_w(p, COL) for p in (study, gantt, figure, check, prov))
top = max(a.height + b.height + GAP + 2 * LABEL_H, e.height + LABEL_H)
H = PAD + top + GAP + LABEL_H + max(c.height, d.height) + PAD
canvas = Image.new('RGB', (W, H), 'white')
draw = ImageDraw.Draw(canvas)
def place(im, x, y, letter, title):
    draw.text((x, y), f'{letter}  {title}', fill='black', font=font)
    canvas.paste(im, (x, y + LABEL_H))
    return y + LABEL_H + im.height
left, right = PAD, PAD + COL + GAP
y = place(a, left, PAD, 'a', 'Study view (the battery)') + GAP
place(b, left, y, 'b', 'Gantt view')
place(e, right, PAD, 'e', 'Figure view (CONSORT flow)')
y = PAD + top + GAP
place(c, left, y, 'c', 'Checklist view')
place(d, right, y, 'd', 'Provenance view')
canvas.save(out)
# pHYs, so the composite prints 180 mm wide.
png = open(out, 'rb').read(); ppm = round(W / 0.180)
body = b'pHYs' + struct.pack('>IIB', ppm, ppm, 1)
open(out, 'wb').write(png[:33] + struct.pack('>I', 9) + body + struct.pack('>I', zlib.crc32(body)) + png[33:])
print(out, canvas.size)
