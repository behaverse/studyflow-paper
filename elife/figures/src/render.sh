#!/bin/sh
# Render the manuscript figures from this folder's sources, with the modeler checkout in $MODELER.
#   MODELER=~/workspace/behaverse/studyflow-modeler src/render.sh              # every figure (~10 min)
#   MODELER=... src/render.sh fig-step1-design fig-views                        # just these
# A `<name>.studyflow.yaml` is laid out (layout.py), drawn by the modeler (render.mjs), rasterized at 4x
# with its print size stamped, and the studyflow embedded in the PNG. A hand-drawn `<name>.svg` is only
# rasterized. `fig-elements` is the modeler's own kitchen sink; `fig-views` composes the modeler's view
# dialogs of the combined study (views.mjs, compose_views.py); `fig-s2-modeler` is a modeler screenshot
# (modeler.mjs); `fig-overview` is built by fig-overview.py. Needs the modeler with `npm ci`, playwright's
# chromium, the CLI built; `uv` (compose_views.py) and draw.io desktop (fig-overview).
set -e
SRC=$(cd "$(dirname "$0")" && pwd); OUT=$SRC/..; TMP=/tmp/studyflow-figs; mkdir -p "$TMP"
export MODELER=${MODELER:?set MODELER to the studyflow-modeler checkout}
ALL="fig-step1-design fig-step2-run fig-step2-nback fig-step3-analyze fig-step3-decision fig-step3-coordinator fig-step4-report fig-combined fig-consort figS1-multimodal
     fig-consort-reference fig-step2-nback-classic fig-elements fig-views fig-s2-modeler fig-overview"
trap 'rm -f "$MODELER/render.mjs" "$MODELER/views.mjs" "$MODELER/modeler.mjs"' EXIT
# the scripts run from the modeler checkout, to import its playwright; each is copied there just before it runs
mjs() { cp "$SRC/$1" "$MODELER/"; (cd "$MODELER" && node "$@"); }
# fig-combined is the executable example study: the executed copy when there is one, else the deposited file.
src_of() { case $1 in
  fig-combined) s=$OUT/../study; [ -f "$s/run/example_study.studyflow.yaml" ] && echo "$s/run/example_study.studyflow.yaml" || echo "$s/example_study.studyflow.yaml" ;;
  *) echo "$SRC/$1.studyflow.yaml" ;;
 esac; }
laid() { python3 "$SRC/layout.py" "$(src_of "$1")" "$TMP/$1.studyflow.yaml"; echo "$TMP/$1.studyflow.yaml"; }
for f in ${@:-$ALL}; do
  case $f in
    fig-combined)             mm=0.19 ;;    # 948 units + the one-row key; 11-unit labels at 5.9 pt
    fig-elements)             mm=0.115 ;;
    *-reference|*-classic)    mm=0.185 ;;   # hand-drawn panels sharing a row with a diagram
    *)                        mm=0.2 ;;     # the common scale: 11-12 unit labels print at 6.2-6.8 pt
  esac
  export MM_PER_UNIT=$mm
  case $f in
    fig-elements)   mjs render.mjs skills/studyflow/examples/kitchensink.studyflow.yaml "$OUT/$f.studyflow.png" ;;
    fig-views)      rm -rf "$TMP/views"; mkdir -p "$TMP/views"; y=$(laid fig-combined); mjs views.mjs "$y" "$TMP/views"
                    uv run --quiet --with pillow python3 "$SRC/compose_views.py" "$TMP/views" "$OUT/$f.studyflow.png" ;;
    fig-s2-modeler) y=$(laid fig-step2-run); mjs modeler.mjs "$y" "$OUT/$f.png" ;;
    # the combined study carries the symbol key (fig-key) as a strip under it, drawn at the same scale
    fig-combined)   y=$(laid fig-combined); mjs render.mjs "$y" "$TMP/combined.png"
                    k=$(laid fig-key); mjs render.mjs "$k" "$TMP/key.png"
                    uv run --quiet --with pillow python3 "$SRC/compose_key.py" "$TMP/combined.png" "$TMP/key.png" "$TMP/combined-keyed.png"
                    node "$MODELER/packages/cli/dist/studyflow.mjs" convert --into "$TMP/combined-keyed.png" "$y" "$OUT/$f.studyflow.png" ;;
    fig-overview)   python3 "$SRC/fig-overview.py" --render --export ;;
    *) if [ -f "$SRC/$f.svg" ]; then mjs render.mjs "$SRC/$f.svg" "$OUT/$f.png"
       else y=$(laid "$f"); mjs render.mjs "$y" "$OUT/$f.studyflow.png"; fi ;;
  esac
done
