#!/bin/sh
# Render one manuscript figure from its .studyflow.yaml source.
#   MODELER=/path/to/studyflow-modeler ./render.sh fig-step1-design [scale]
# Needs the modeler repo with `npm ci` done, `npx playwright install chromium`,
# and `npm run build -w @behaverse/studyflow-cli`. Copies render.mjs next to the
# repo's package.json so it can import @playwright/test, fills in the missing
# waypoints (layout.py), drives the modeler headlessly, rasterizes the exported
# SVG at `scale` (default 4) and embeds the studyflow source into the PNG.
set -e
SRC=$(cd "$(dirname "$0")" && pwd)
MODELER=${MODELER:?set MODELER to the studyflow-modeler checkout}
OUT=${OUT:-$SRC/..}
mkdir -p /tmp/studyflow-figs
python3 "$SRC/layout.py" "$SRC/$1.studyflow.yaml" "/tmp/studyflow-figs/$1.studyflow.yaml"
cp "$SRC/render.mjs" "$SRC/views.mjs" "$MODELER/"
trap 'rm -f "$MODELER/render.mjs" "$MODELER/views.mjs"' EXIT
cd "$MODELER" && node render.mjs "/tmp/studyflow-figs/$1.studyflow.yaml" "$OUT/$1.studyflow.png" "${2:-4}"
