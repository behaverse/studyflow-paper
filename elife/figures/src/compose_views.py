#!/usr/bin/env python3
"""Compose fig-views from the Study view (combined), the Gantt/Checklist/Provenance dialog captures, and the Figure view (consort).
Usage: compose_views.py <study.png> <gantt.png> <checklist.png> <provenance.png> <figure.png> <out.png>"""
import sys
from PIL import Image, ImageDraw, ImageFont
study, gantt, check, prov, figure, out = sys.argv[1:7]
H = 3000; GAP = 90; PAD = 60; LABEL_H = 110
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 84)
def fit_h(path, h):
    im = Image.open(path).convert('RGB'); return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
def fit_w(path, w):
    im = Image.open(path).convert('RGB'); return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
body = H - LABEL_H
a = fit_h(study, body); e = fit_h(figure, body)
RW = 2000
b, c, d = (fit_w(p, RW) for p in (gantt, check, prov))
right_h = b.height + c.height + d.height + 2 * (GAP + LABEL_H)
W = PAD * 2 + a.width + GAP + RW + GAP + e.width
canvas = Image.new('RGB', (W, PAD * 2 + LABEL_H + max(body, right_h)), 'white')
draw = ImageDraw.Draw(canvas)
def place(im, x, y, letter, title):
    draw.text((x, y), f'{letter}  {title}', fill='black', font=font)
    canvas.paste(im, (x, y + LABEL_H))
    return y + LABEL_H + im.height
x = PAD; place(a, x, PAD, 'a', 'Study view'); x += a.width + GAP
y = PAD
y = place(b, x, y, 'b', 'Gantt view') + GAP
y = place(c, x, y, 'c', 'Checklist view') + GAP
y = place(d, x, y, 'd', 'Provenance view')
x += RW + GAP; place(e, x, PAD, 'e', 'Figure view (CONSORT flow after execution)')
canvas.save(out); print(out, canvas.size)
