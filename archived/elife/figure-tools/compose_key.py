#!/usr/bin/env python3
"""Paste the symbol key under a rendered figure, at the figure's own scale.

Usage: compose_key.py <figure.png> <key.png> <out.png>

Both are drawn by render.mjs at the same MM_PER_UNIT and the same raster scale, so the key needs no
resizing: it is pasted left-aligned below the diagram, and its notes print at the size of the figure's
own labels. The figure's `pHYs` chunk (its print size) is carried over to the composite.
"""
import struct
import sys

from PIL import Image

fig_path, key_path, out_path = sys.argv[1:4]
fig = Image.open(fig_path).convert('RGB')
key = Image.open(key_path).convert('RGB')

PAD = max(8, fig.width // 100)
width = max(fig.width, key.width + 2 * PAD)
height = fig.height + 2 * PAD + key.height + PAD
canvas = Image.new('RGB', (width, height), 'white')
canvas.paste(fig, (0, 0))
canvas.paste(key, (PAD, fig.height + 2 * PAD))
canvas.save(out_path)


def phys_chunk(png: bytes) -> bytes | None:
    """The pHYs chunk (length, type, data, crc) of a PNG, searched from the end of IHDR."""
    at = 33
    while at + 8 <= len(png):
        length = struct.unpack('>I', png[at:at + 4])[0]
        if png[at + 4:at + 8] == b'pHYs':
            return png[at:at + 12 + length]
        at += 12 + length
    return None


chunk = phys_chunk(open(fig_path, 'rb').read())
if chunk:
    composed = open(out_path, 'rb').read()
    open(out_path, 'wb').write(composed[:33] + chunk + composed[33:])
print(out_path, canvas.size)
