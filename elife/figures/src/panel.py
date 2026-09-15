#!/usr/bin/env python3
"""Rasterize a hand-drawn SVG panel at the figures' one print scale.

Usage: panel.py in.svg out.png

Like render.mjs: 4x raster, and a pHYs chunk so 1 SVG unit prints at 0.175 mm. Needs rsvg-convert.
"""
import struct, subprocess, sys, zlib

SCALE, MM_PER_UNIT = 4, 0.175
src, out = sys.argv[1:3]
png = subprocess.run(['rsvg-convert', '-z', str(SCALE), src], check=True, capture_output=True).stdout
ppm = round(SCALE / MM_PER_UNIT * 1000)
body = b'pHYs' + struct.pack('>IIB', ppm, ppm, 1)
chunk = struct.pack('>I', 9) + body + struct.pack('>I', zlib.crc32(body))
open(out, 'wb').write(png[:33] + chunk + png[33:])  # after the signature and IHDR
