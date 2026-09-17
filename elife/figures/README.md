# Figures

The figures `../paper-v3.qmd` cites, one PNG per `@fig-…` label, all generated from [`src/`](src/).

```sh
MODELER=~/workspace/behaverse/studyflow-modeler src/render.sh                 # every figure, ~10 min
MODELER=~/workspace/behaverse/studyflow-modeler src/render.sh fig-consort     # one of them
```

`src/render.sh` is the list of figures, their sources and their print scales; each script says what it does at its top.

- `fig-*.studyflow.yaml` — hand-written diagrams, drawn by the modeler. `layout.py` routes the flows that carry no `waypoint`; `colorize.py` colours everything by the step it belongs to (its docstring is the palette and the rule); labels cite run state as `{count}` / `{reached}`.
- `fig-*.svg` — the two hand-drawn panels (the CONSORT 2025 template, the slide-style N-back).
- `fig-views` — the modeler's Gantt, Provenance and Checklist dialogs of `fig-combined` (`views.mjs`, `compose_views.py`); `fig-s2-modeler` — a modeler screenshot of Step 2 (`modeler.mjs`); `fig-elements` — the modeler's kitchen sink.
- `fig-overview` — `fig-overview.py` lays the lifecycle grid out in draw.io and embeds the modeler's renders of `fig-overview.studyflow.yaml` (the example study compacted to one row) and of its views. Edit the yaml or the script, never `fig-overview.drawio`, which it overwrites. `icons.json` is the draw.io icon palette for the non-Studyflow furniture.

Every `.studyflow.png` carries its diagram (`studyflow info <png>` reads it back; the modeler opens it) and its print size in a `pHYs` chunk. `fig-combined`, `fig-consort` and `fig-overview` are one study: keep their `state` blocks (counts, `_meta.prov`) identical.

Leftovers with no citation, kept for their sources: `figS3-runner.studyflow.png`, `rt_analysis.studyflow.png`, `fig1_gap_panel*.png`, `todo_fig_extensions.png`, `fig-consort.drawio` (two reference rasters).
