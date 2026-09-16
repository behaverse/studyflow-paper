#!/bin/sh
# Render one manuscript figure from its source in this folder.
#   MODELER=/path/to/studyflow-modeler ./render.sh fig-step1-design [scale]
# A `<name>.studyflow.yaml` is drawn by the modeler: the missing waypoints are filled in (layout.py), the
# modeler is driven headlessly, its exported SVG rasterized at `scale` (default 4) with the print size stamped
# in, and the studyflow source embedded into the PNG. A hand-drawn `<name>.svg` panel is rasterized the same
# way, with no diagram to embed. Needs the modeler repo with `npm ci` done, `npx playwright install chromium`,
# and `npm run build -w @behaverse/studyflow-cli`; render.mjs is copied next to the repo's package.json so it
# can import @playwright/test.
set -e
SRC=$(cd "$(dirname "$0")" && pwd)
MODELER=${MODELER:?set MODELER to the studyflow-modeler checkout}
OUT=${OUT:-$SRC/..}
cp "$SRC/render.mjs" "$SRC/views.mjs" "$MODELER/"
trap 'rm -f "$MODELER/render.mjs" "$MODELER/views.mjs"' EXIT
if [ -f "$SRC/$1.svg" ]; then
  cd "$MODELER" && node render.mjs "$SRC/$1.svg" "$OUT/$1.png" "${2:-4}"
  exit
fi
mkdir -p /tmp/studyflow-figs
python3 "$SRC/layout.py" "$SRC/$1.studyflow.yaml" "/tmp/studyflow-figs/$1.studyflow.yaml"
cd "$MODELER" && node render.mjs "/tmp/studyflow-figs/$1.studyflow.yaml" "$OUT/$1.studyflow.png" "${2:-4}"
