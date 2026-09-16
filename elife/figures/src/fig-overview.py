#!/usr/bin/env python3
"""Build @fig-overview: ../fig-overview.drawio and, with --export, ../fig-overview.studyflow.png.

The Studyflow content is real: `fig-overview.studyflow.yaml` (the example study compacted to one row) is drawn
by the reference modeler and its Gantt, Checklist and Provenance views are the modeler's own dialogs, captured
by views.mjs. This script lays the surrounding figure out in draw.io (the lifecycle grid, today's artifacts,
the tool-coverage bars, panel headers) and embeds those renders as images, so no Studyflow element is
redrawn by hand. Columns follow the strip: each lifecycle stage is as wide as its part of the diagram.

    python3 src/fig-overview.py --render           # modeler renders into src/build/ (needs $MODELER)
    python3 src/fig-overview.py --export           # drawio -> PNG (draw.io desktop), print size, studyflow embedded

960 units wide = 180 mm at 0.1875 mm/unit; 12-unit labels print at 6.4 pt. The embedded views are thumbnails
(their text prints at about 4 pt); fig-views and fig-consort show the same views at full size.
"""
import base64, html, json, os, re, struct, subprocess, sys, zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
BUILD = HERE / 'build'
MM_PER_UNIT, SCALE = 0.1875, 4
MODELER = os.environ.get('MODELER', str(HERE.parents[3] / 'studyflow-modeler'))

STEP = {'design': ('#dbe6f2', '#4e6f95'), 'run': ('#dcebd6', '#5c8a55'),
        'analyze': ('#e6dff1', '#7a67a6'), 'report': ('#f6e8c9', '#a2803c')}
RED = ('#f1d0cd', '#ac5a54')
INK, GREY, MUTED, DATA = '#1a1a1a', '#5c5c56', '#8a8a83', '#4E5D6C'
BEIGE = ('#EFE9DF', '#6f5f3b')
FONT, MONO = 'IBM Plex Sans', 'IBM Plex Mono'
ICONS = json.loads((HERE / 'icons.json').read_text())   # name -> draw.io image style (inline svg), figure furniture only

# ---------------------------------------------------------------- modeler renders
LAID = Path('/tmp/studyflow-figs/fig-overview.studyflow.yaml')   # the source with its flows routed (layout.py)
if '--render' in sys.argv or '--export' in sys.argv:
    BUILD.mkdir(exist_ok=True); LAID.parent.mkdir(exist_ok=True)
    subprocess.run(['python3', HERE / 'layout.py', HERE / 'fig-overview.studyflow.yaml', LAID], check=True)
if '--render' in sys.argv:
    for m in ('render.mjs', 'views.mjs'):
        (Path(MODELER) / m).write_bytes((HERE / m).read_bytes())
    try:
        subprocess.run(['node', 'render.mjs', LAID, BUILD / 'strip.studyflow.png', str(SCALE)], cwd=MODELER, check=True)
        subprocess.run(['node', 'views.mjs', LAID, BUILD], cwd=MODELER, check=True)
    finally:
        for m in ('render.mjs', 'views.mjs'): (Path(MODELER) / m).unlink(missing_ok=True)

cells, _n = [], [0]


def nid():
    _n[0] += 1
    return f'c{_n[0]}'


def cell(value, style, x, y, w, h):
    i = nid()
    cells.append(f'<mxCell id="{i}" value="{html.escape(value, quote=True)}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" as="geometry"/></mxCell>')
    return i


def edge(src, tgt, style, ex, ey, nx, ny):
    style += f'exitX={ex};exitY={ey};exitDx=0;exitDy=0;entryX={nx};entryY={ny};entryDx=0;entryDy=0;'
    cells.append(f'<mxCell id="{nid()}" style="{style}" edge="1" parent="1" source="{src}" target="{tgt}">'
                 f'<mxGeometry relative="1" as="geometry"/></mxCell>')


def text(value, x, y, w, h, size=12, color=INK, align='left', bold=False, italic=False, font=FONT):
    st = (f'text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;overflow=visible;align={align};'
          f'verticalAlign=middle;fontFamily={font};fontSize={size};fontColor={color};fontStyle={1 if bold else 2 if italic else 0}')
    return cell(value, st, x, y, w, h)


def icon(name, x, y, size=16, color=GREY):
    st = ICONS[name]
    if color != GREY:
        m = re.search(r'image=data:image/svg\+xml,([^;]+);', st)
        svg = base64.b64decode(m.group(1)).decode().replace('#5c5c56', color)
        st = st.replace(m.group(1), base64.b64encode(svg.encode()).decode())
    return cell('', st, x, y, size, size)


def png_size(path):
    return struct.unpack('>II', path.read_bytes()[16:24])


def image(path, x, y, w):
    """Embed a build PNG at `w` units wide (resampled to the export's 4 px/unit); returns its height."""
    pw, ph = png_size(path)
    h = w * ph / pw
    small = BUILD / 'embed' / path.name; small.parent.mkdir(exist_ok=True)
    subprocess.run(['sips', '--resampleWidth', str(round(w * SCALE)), path, '--out', small], check=True, capture_output=True)
    b64 = base64.b64encode(small.read_bytes()).decode()
    cell('', f'shape=image;html=1;imageAspect=0;aspect=fixed;image=data:image/png,{b64};', x, y, w, h)
    return h


def pill(x, y, label):
    cell(label, f'rounded=1;absoluteArcSize=1;arcSize=9;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#b4b4ad;'
         f'strokeWidth=1;fontFamily={FONT};fontSize=10;fontStyle=0;fontColor={INK};align=center;verticalAlign=middle;', x - 62, y, 124, 18)


def header(x, y, w, name, ico, who, whoic):
    hdr = cell('', f'rounded=0;whiteSpace=wrap;html=1;fillColor=#f4f4f2;strokeColor=#cdcdc7;', x, y, w, 22)
    icon(ico, x + 8, y + 4, 14, INK)
    text(name, x + 26, y, 120, 22, size=12, bold=True)
    ww = len(who) * 6.2 + 4
    text(who, x + w - 8 - ww, y, ww, 22, size=11, color=MUTED, align='right')
    icon(whoic, x + w - 24 - ww, y + 5, 13, MUTED)
    return hdr


PROJ = 'edgeStyle=orthogonalEdgeStyle;html=1;strokeColor=#7a7a74;strokeWidth=1.4;dashed=1;dashPattern=5 4;endArrow=open;endSize=6;'

# ---------------------------------------------------------------- grid, sized by the strip
X0, W = 20, 920
STRIP = BUILD / 'strip.studyflow.png'
sw_px, sh_px = png_size(STRIP)
S = (W - 4) / (sw_px / SCALE)                    # strip units -> canvas units (fits the container)
STRIP_H = sh_px / SCALE * S
# stage boundaries in strip units: after the allocation join, after the battery, after the analysis
BOUNDS = [0, 452, 607, 760, sw_px / SCALE]
COLS = ['design', 'run', 'analyze', 'report']
NAMES = ['Design', 'Run', 'Analyze', 'Report']
cx = lambda i: X0 + 2 + BOUNDS[i] * S
cw = lambda i: (BOUNDS[i + 1] - BOUNDS[i]) * S

FY = 366                                          # the file container
FH = 30 + STRIP_H + 6
STRIP_BOTTOM = FY + FH


def band_title(letter, title, y):
    text(letter, X0 - 4, y, 16, 18, size=14, bold=True)
    text(title, X0 + 14, y, 700, 18, size=12, color='#3d3d3a')


for i, c in enumerate(COLS):
    f, s = STEP[c]
    cell('', f'rounded=0;whiteSpace=wrap;html=1;fillColor={f};strokeColor=none;opacity=32;', cx(i) + 2, 40, cw(i) - 4, STRIP_BOTTOM - 40)
for i, (c, n, ic) in enumerate(zip(COLS, NAMES, ['pencil-simple', 'play-circle', 'sigma', 'newspaper'])):
    f, s = STEP[c]
    cell(n, f'shape=step;perimeter=stepPerimeter;whiteSpace=wrap;html=1;shapeInside=1;fixedSize=1;size=12;fillColor={f};'
            f'strokeColor={s};strokeWidth=1.2;fontColor={INK};fontFamily={FONT};fontSize=13;fontStyle=1;spacingLeft=16;',
         cx(i) + 2, 10, cw(i) - 4, 26)
    icon(ic, cx(i) + cw(i) / 2 - 12 - 3.4 * len(n) - 8, 15, 16, s)

# ---------------------------------------------------------------- a) today
band_title('a', 'Today: one artifact per audience', 48)
ARTS = [[('Protocol PDF', 'file-text', 'researcher', 'account-details-outline'),
         ('Ethics application', 'stamp', 'ethics board', 'account-group-outline')],
        [('Experiment<br>script', 'file-code', 'engineer', 'account-hard-hat-outline'),
         ('Task<br>screens', 'monitor', 'participant', 'account-outline')],
        [('Analysis<br>notebook', 'notebook', 'analyst', 'account-search-outline')],
        [('Checklists', 'list-checks', 'reviewer', 'account-eye-outline'),
         ('Manuscript<br>figure', 'chart-bar', 'replicator', 'account-convert-outline')]]
for i, items in enumerate(ARTS):
    pos = [0.5] if len(items) == 1 else ([0.3, 0.7] if cw(i) > 300 else [0.22, 0.78])
    for p, (name, ic, who, whoic) in zip(pos, items):
        x = cx(i) + cw(i) * p
        cell('', f'shape=note;size=12;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor={DATA};strokeWidth=1.3;', x - 24, 72, 48, 56)
        icon(ic, x - 11, 90, 22, DATA)
        two = '<br>' in name
        text(name, x - 60, 134, 120, 28 if two else 16, size=12, align='center', bold=True)
        yy = 165 if two else 152
        fs = 10 if cw(i) < 300 else 11
        ww = len(who) * fs * 0.56
        icon(whoic, x - 8 - ww / 2, yy + 1, 13, MUTED)
        text(who, x + 8 - ww / 2, yy, ww + 6, 16, size=fs, color=MUTED, align='left')

# ---------------------------------------------------------------- b) existing tools
band_title('b', 'Existing tools: each covers a slice of the lifecycle', 190)
TOOLS = [('Reporting guidelines', 'book-open-text', [0, 3]), ('Experiment builders', 'cursor-click', [1]),
         ('Evaluation harnesses', 'gauge', [1, 2]), ('Data standards', 'database', [1, 2]), ('Workflow engines', 'git-branch', [2])]
y = 212
for name, ic, span in TOOLS:
    runs = [[span[0]]]
    for c in span[1:]:
        (runs[-1].append(c) if c == runs[-1][-1] + 1 else runs.append([c]))
    for r in runs:
        cell('', f'rounded=1;absoluteArcSize=1;arcSize=3;whiteSpace=wrap;html=1;fillColor={BEIGE[0]};strokeColor=none;',
             cx(r[0]) + 6, y, cx(r[-1]) + cw(r[-1]) - cx(r[0]) - 12, 17)
    icon(ic, cx(span[0]) + 12, y + 2, 13, BEIGE[1])
    text(name, cx(span[0]) + 29, y, 200, 17, size=11, color=BEIGE[1])
    y += 21
cell('whole study: none', f'rounded=1;absoluteArcSize=1;arcSize=3;whiteSpace=wrap;html=1;fillColor=none;strokeColor={RED[1]};'
     f'dashed=1;dashPattern=4 3;fontFamily={FONT};fontSize=11;fontStyle=2;fontColor={RED[1]};', X0 + 6, y + 2, W - 12, 17)

# ---------------------------------------------------------------- c) the file, drawn by the modeler
band_title('c', 'Studyflow: one file for every stage, a view for every audience', FY - 20)
file_id = cell('', f'rounded=1;absoluteArcSize=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#b4b4ad;strokeWidth=1.2;',
               X0, FY, W, FH)
text('example_study.studyflow', X0 + 10, FY + 5, 220, 16, size=11, color=MUTED, font=MONO)
text('Study view', X0 + W - 176, FY + 5, 80, 16, size=12, bold=True, align='right')
icon('account-details-outline', X0 + W - 90, FY + 6, 13, MUTED)
text('researcher', X0 + W - 74, FY + 5, 66, 16, size=11, color=MUTED)
# existing tools plug into the file rather than being replaced
pill(cx(1) + cw(1) / 2, FY + 4, 'jsPsych / Behaverse tasks')
pill(cx(2) + cw(2) / 2 + 10, FY + 4, 'python:// analysis code')
image(STRIP, X0 + 2, FY + 30, W - 4)

# ---------------------------------------------------------------- c) the modeler's views of the file
PY = STRIP_BOTTOM + 34
GAP, LW = 12, 556
RW = W - LW - GAP
LX, RX = X0, X0 + LW + GAP
tops = {}


def panel(x, y, w, name, ico, who, whoic, images, arrow_x, gap=6, entry=None):
    hdr = header(x, y, w, name, ico, who, whoic)
    yy = y + 22 + gap
    for p in images:
        yy += image(p, x + 4, yy, w - 8) + gap
    cell('', f'rounded=1;absoluteArcSize=1;arcSize=5;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#cdcdc7;', x, y, w, yy - y)
    edge(file_id, hdr, PROJ, (arrow_x - X0) / W, 1, entry if entry is not None else (arrow_x - x) / w, 0)
    return yy


y1 = panel(LX, PY, LW, 'Gantt view', 'rows', 'ethics board', 'account-group-outline', [BUILD / 'view-gantt.png'], LX + LW / 2)
y2 = panel(RX, PY, RW, 'Checklist view', 'check-square', 'reviewer', 'account-eye-outline',
           sorted(BUILD.glob('view-checklist-*.png')), RX + RW / 2)
# the run history sits under the schedule; its arrow leaves the file beside the Gantt panel and turns in at its corner
y3 = panel(LX, y1 + 14, LW, 'Provenance view', 'git-branch', 'replicator', 'account-convert-outline',
           [BUILD / 'view-provenance.png'], LX + LW + GAP / 2, entry=0.96)
H = max(y2, y3) + 12

# ---------------------------------------------------------------- write
xml = ('<mxfile host="fig-overview.py" agent="src/fig-overview.py" version="31.4.5">\n'
       '  <diagram id="studyflow-overview" name="overview">\n'
       f'    <mxGraphModel dx="1200" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" '
       f'page="1" pageScale="1" pageWidth="1000" pageHeight="{round(H + 20)}" math="0" shadow="0" background="#ffffff">\n'
       '      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n        '
       + '\n        '.join(cells) + '\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n')
drawio = OUT / 'fig-overview.drawio'
drawio.write_text(xml)
print(f'wrote {drawio} ({len(cells)} cells, {W} x {H:.0f} units = {W * MM_PER_UNIT:.0f} x {H * MM_PER_UNIT:.0f} mm)')

if '--export' in sys.argv:
    raw = BUILD / 'fig-overview.raw.png'
    subprocess.run(['/Applications/draw.io.app/Contents/MacOS/draw.io', '-x', '-f', 'png', '-s', str(SCALE), '-e', '-b', '0',
                    '-o', str(raw), str(drawio)], check=True, stderr=subprocess.DEVNULL)
    data = raw.read_bytes()   # stamp the print size (pHYs after IHDR), as render.mjs does for the modeler figures
    ppm = round(SCALE / MM_PER_UNIT * 1000)
    body = b'pHYs' + ppm.to_bytes(4, 'big') * 2 + b'\x01'
    raw.write_bytes(data[:33] + (9).to_bytes(4, 'big') + body + zlib.crc32(body).to_bytes(4, 'big') + data[33:])
    final = OUT / 'fig-overview.studyflow.png'   # the deposited figure carries the diagram it shows, like its siblings
    # the laid-out copy, as render.sh embeds for every other figure: a flow's colour lives on its routed edge
    subprocess.run(['node', 'packages/cli/dist/studyflow.mjs', 'convert', '--into', raw, LAID, final],
                   cwd=MODELER, check=True)
    print(f'exported {final}')
