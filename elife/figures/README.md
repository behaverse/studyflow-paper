# Figures

The figures `../paper-v3.qmd` cites, one PNG per `@fig-…` label. Every figure that shows a study is a Studyflow
diagram drawn by the reference modeler, and its PNG carries that diagram: `studyflow info <png>` reads it back, and
the modeler opens the PNG as the study. Each PNG also carries its print size.

| Figure | What it shows | Its diagram |
|:--|:--|:--|
| `fig-overview` | the lifecycle grid, today's artifacts and tools, and the example study with three of the modeler's views (Gantt, Checklist, Provenance) | `src/fig-overview.studyflow.yaml`, laid out in `fig-overview.drawio` |
| `fig-combined` | the executable example study, as the run left it | for now the planted pipeline-check run (`../study/pipeline-check/run-planted/`, its executed copy with four flow labels widened, layout only), with the one-row key `src/fig-key.studyflow.yaml` under it; redrawn from a language-model run of `../study/example_study.studyflow.yaml` |
| `fig-consort` | the CONSORT participant flow (the Manuscript Figure view), beside `fig-consort-reference` | `src/fig-consort.studyflow.yaml` |
| `fig-step1-design` … `fig-step4-report` | the study built one step at a time | `src/fig-step*.studyflow.yaml` |
| `fig-step2-nback`, beside `fig-step2-nback-classic` | the N-back drawn out, beside a slide-style drawing of it | `src/fig-step2-nback.studyflow.yaml` |
| `fig-views` | the Gantt, Provenance and Checklist views of `fig-combined` at full size | screenshots of the modeler's dialogs; no diagram embedded |
| `fig-elements` | every element the palette offers | the modeler's kitchen sink example |
| `fig-s2-modeler` | the modeler editing Step 2 | a screenshot |

`fig-consort-reference` and `fig-step2-nback-classic` are the two hand-drawn panels; their sources are the `.svg`
files in `src/`.

## How the diagrams relate

- The step figures, `fig-consort` and `fig-overview` simplify the example study and reuse its element ids, so a reader
  can match any box to one in `fig-combined`. `fig-step3-decision` is its `Congruency` question expanded.
- The CONSORT phases are lanes directly in the subjects' pool, never groups and never a sub-process. A pool holds lanes,
  and anything that needs another level becomes another pool. Each lane carries the tint of its lifecycle step.
- The step figures draw the deposited plan, so their counts print `n=0`. `fig-combined`, `fig-consort` and
  `fig-overview` print a run's counts. `fig-combined` is the current pipeline-check run itself. The `state:` block of
  `fig-consort.studyflow.yaml` is the earlier run's (`../../archived/elife/study-runs-2026-09-29/run-planted/`), copied
  byte for byte but for `Record the completion`, which that run did not have: the step and its two flows carry the
  count of the flow they replace. `fig-overview.studyflow.yaml` carries the same run's block with a longer timeline of
  runs, plus a count for each flow its compaction draws: the count of the path that flow stands for in the run.
  `studyflow validate` reports both copies for what they are, drawings of the study rather than the protocol that ran:
  a seal warning on both, and on `fig-overview` a second start event, the analysis's, which the study draws in a pool
  of its own.
- The Provenance view in `fig-overview` shows two runs: the reported one, and a re-run after its `Analysis` record was
  invalidated, which branches at that step (`../../archived/elife/study-runs-2026-09-29/run-planted-rerun/`). Its steps carry
  the records of both run repositories. That re-run replayed one subject's allocation for all eight, which the modeler
  has since fixed. These three figures show the `simulate://` pipeline check until a language-model run of the
  Behaverse study replaces them.

## Rebuilding

The scripts that drew these PNGs (layout, colouring, composing the key and the views, the draw.io overview, and the
history merge for the overview) are archived in `../../archived/elife/figure-tools/`, with `render.sh` as the entry
point. To redraw a figure, open its diagram in the modeler and export it, or restore those scripts beside `src/`. The
PNGs re-rendered on 2026-10-02 embed their `src` file as it is, not the copy `layout.py` routes: the modeler routes a
flow that has no waypoints itself.
