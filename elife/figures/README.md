# Figures

The figures `../paper-v3.qmd` cites, one PNG per `@fig-…` label. Every figure that shows a study is a Studyflow
diagram drawn by the reference modeler, and its PNG carries that diagram: `studyflow info <png>` reads it back, and
the modeler opens the PNG as the study. Each PNG also carries its print size.

| Figure | What it shows | Its diagram |
|:--|:--|:--|
| `fig-overview` | the lifecycle grid, today's artifacts and tools, and the example study with three of the modeler's views (Gantt, Checklist, Provenance) | `src/fig-overview.studyflow.yaml`, laid out in `fig-overview.drawio` |
| `fig-combined` | the executable example study, as the run left it | `../study/run/example_study.studyflow.yaml`, with the one-row key `src/fig-key.studyflow.yaml` under it |
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
  `fig-overview` are one study and print the run's counts: the `state:` block of `fig-consort.studyflow.yaml` is the
  run's (`../study/run/`), copied byte for byte, and `fig-overview.studyflow.yaml` has the same block with a longer
  timeline of runs. `studyflow validate` reports both copies for what they are, drawings of the study rather than the
  protocol that ran: a seal warning on both, and unbalanced counts where `fig-overview` compacts the study.
- The Provenance view in `fig-overview` shows two runs: the reported one, and a re-run after its `Analysis` record was
  invalidated, which branches at that step (`../study/run-2026-10-02-rerun/`, see `../study/README.md`). Its steps carry
  the records of both run repositories.

## Rebuilding

The scripts that drew these PNGs (layout, colouring, composing the key and the views, the draw.io overview, and the
history merge for the overview) are archived in `../../archived/elife/figure-tools/`, with `render.sh` as the entry
point. To redraw a figure, open its diagram in the modeler and export it, or restore those scripts beside `src/`.
