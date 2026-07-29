# Figures for the eLife paper

This folder collects the figures and listings referenced by [`../paper.qmd`](../paper.qmd). Drop authored figures here as they are produced; the table below tracks which are done, which are gaps, and which need composition from existing assets.

## Conventions

- **One PNG per figure, and the PNG is the source.** Every figure lives in this folder as a single flat `.png` — no `svg/`, no `png/`, no separate `.studyflow` sidecar. The diagram source travels *inside* the image: the Studyflow BPMN XML in a `studyflow` `iTXt` chunk (before `IEND`), and a draw.io `<mxfile>` in an `mxfile` `tEXt` chunk (before `IDAT`, URI-encoded). So each deposited figure reopens in the Studyflow modeler *and* in draw.io as an editable diagram, which is the claim §2.2 and the Discussion make about deposited figures.
- **File naming.** `fig-<label>.png`, where `<label>` is exactly the `@fig-…` cross-reference the manuscript cites (`fig-overview.png` for `@fig-overview`). Lowercase, hyphenated. Where a figure has panels that are not composited yet, the panel takes a suffix (`fig-nback-classic.png`).
- **Sizing.** Target eLife column widths: 88 mm (single column) for inline figures, 180 mm (full width) for multi-panel composites. Figures are rasterized to fill a 180 × 240 mm box at 600 dpi (scale clamped to 3×–8× of the diagram's own pixel size), so every one clears 300 dpi at print width with headroom.
- **Captions.** Drafted in `paper-v3.qmd` next to each figure reference. Keep captions self-contained: a reader skimming figures should understand the claim without reading the body.

### Regenerating a figure

From `studyflow-modeler`:

```
npm run figures:render -- ../studyflow-paper/elife/figures fig-nback     # one
npm run figures:render -- ../studyflow-paper/elife/figures --all        # every figure
```

It opens each figure in the modeler, exports **SVG** (vector, and the format the modeler embeds both payloads into), rasterizes it at the figure's current pixel width, and writes the `studyflow` and `mxfile` chunks back on. Two things that matter: the app's own PNG export rasterizes at 1×, which is under print resolution, and re-using the existing width means nothing shifts in the manuscript layout. The diagram interchange inside the payload is preserved, so a re-render reproduces the authored layout rather than re-flowing it.

A figure is rendered from `<stem>.migrated.xml` if one sits beside it, otherwise from the diagram already inside its own `.png` — which is how a schema migration or a hand edit gets applied: drop the XML next to the figure, render, delete the XML.

By hand instead: re-export **PNG** from the modeler with both embed toggles on (Export dialog → Image → PNG → *Embed Studyflow source* + *Embed draw.io diagram*), accepting the 1× raster; `src/modeler/models/exporters/pngEmbedding.ts` has `embedStudyflowIntoPng` / `embedDrawioIntoPng` if you rasterize yourself.

To read a figure back: open the `.png` directly in the modeler (`Open File…`), or in draw.io. `fig-overview.png` is draw.io-authored and carries only the draw.io payload; the two `fig1_gap_panel*.png` sketches are hand-written SVG with no diagram source and carry neither.

---

## Files on disk (2026-07-28)

One file per cross-reference: the filename **is** the `@fig-…` label the manuscript cites. The embedded diagram's own name is quoted below because it is what identifies the figure — not the filename, which is derived from it.

| File | Cited as | Embedded diagram | Pixels | `studyflow` | `mxfile` | Size |
|---|---|---|---|---|---|---|
| `fig-overview.png` | `@fig-overview` | *(draw.io, 3 panels: Problem / Gap / Solution)* | 4419×3753 | — | yes | 479 KB |
| `fig-elements.png` | `@fig-elements` | Studyflow element catalog (kitchen sink) | 3900×6312 | yes | yes | 1243 KB |
| `fig-consort.png` | `@fig-consort` | CONSORT participant flow | 4252×5079 | yes | yes | 1135 KB |
| `fig-example-design.png` | `@fig-example-design` | Step 1 — Design | 4252×3061 | yes | yes | 615 KB |
| `fig-nback.png` | `@fig-nback` (panel b) | N-back trial | 4252×3037 | yes | yes | 562 KB |
| `fig-nback-classic.png` | `@fig-nback` (panel a) | *(raster slide, no source)* | 584×220 | — | — | 13 KB |
| `fig-example-run.png` | `@fig-example-run` | Step 2 — Run | 4252×4082 | yes | yes | 870 KB |
| `fig-pipeline.png` | `@fig-pipeline` | Analysis pipeline | 1866×6012 | yes | yes | 665 KB |
| `fig-example-analyze.png` | `@fig-example-analyze` | Step 3 — Analyze | 4252×4547 | yes | yes | 882 KB |
| `fig-example-report.png` | `@fig-example-report` | Step 4 — Report | 4252×2220 | yes | yes | 325 KB |
| `fig-views.png` | `@fig-views` | study.studyflow | 2601×5904 | yes | yes | 893 KB |
| `fig-combined.png` | `@fig-combined` | Example study (human and artificial cohorts) | 3792×9358 | yes | yes | 1959 KB |

**Not yet cited by the caption list**, left under their old names rather than given invented labels:

| File | Embedded diagram | Pixels | `studyflow` | `mxfile` |
|---|---|---|---|---|
| `figS1_multimodal.png` | Multimodal preprocessing and training | 4252×2116 | yes | yes |
| `figS3_runner.png` | Runner walkthrough | 1936×6224 | yes | yes |
| `rt_analysis.png` | RT Analysis | 4252×2227 | yes | yes |
| `fig1_gap_panelA.png`, `fig1_gap_panelB.png` | *(hand-written SVG sketches, superseded by `fig-overview.png`)* | — | — | — |
| `todo_fig_extensions.png` | *(raster, no source)* | 2400×1080 | — | — |

**Panels still to composite.** `@fig-consort` panel a is the published CONSORT 2025 reference flow, which is not in this folder; `fig-consort.png` is panel b only. `@fig-nback` is split across `fig-nback-classic.png` (a) and `fig-nback.png` (b). `@fig-views` shows the Study view; the Gantt, Checklist, and post-run CONSORT projections are not rendered yet.

`elife_figures.drawio` stays as the draw.io master, now three pages:

- `overview` — the source of `fig-overview.png`. **Ahead of the deposited PNG** (2026-07-29): it gained the icon layer below, so `fig-overview.png` needs re-exporting before submission.
- `consort` — two reference rasters, carried by no figure here, so deleting the master would lose them.
- `icons` — the figure's icon set as a palette: 35 line icons (lifecycle stages, actors, artifacts, tool families, the studyflow stack, the six views, callout marks). Each is inline SVG carried in the cell's own style (`image=data:image/svg+xml,…`), not a draw.io stencil reference, so a figure using them exports stand-alone. Drag one onto the canvas, or copy a cell's style, to reuse them elsewhere.

---

## Figure inventory

| # | Title | §  | Status | Effort |
|---|---|---|---|---|
| F1 | "Many artifacts, one study" schematic | §1.2 | **gap** | half-day |
| F2 | Studyflow element palette / layers | §2.1 | **drafted** — `fig-elements.png` | needs caption |
| F3 | Modeler UI composite | §2.3 | needs composition | 2 h |
| F4 | Runner walkthrough composite | §2.3 | **gap** (depends on §3.2 round-trip) | half-day |
| F5 | Four views: Study / Gantt / Checklist / Figure | §2.2 | partial — Checklist screenshot is a gap | 30 min once Checklist view ships |
| F6 | CONSORT 2025 vs Studyflow | §3.1 | exists; needs composition + caption | 30 min |
| F7 | N-back: slide → Studyflow → XML | §3.2 | exists; needs composition + caption | 30 min |
| F8 | One executor, many actors (one interface, four packages) | §3.2 | **drafted** — `fig8_executors.svg` | done |
| F9 | Agent-cohort accuracy & RT profiles | §3.2 | **gap** (depends on seed-42 runs) | 2 h |
| F10 | RT analysis pipeline + dplyr side-by-side | §3.3 | **gap** (depends on §3.3 dataset) | 2 h |
| F11 | Multimodal preprocessing/training pipeline | §3.4 | **gap** | 2 h |
| F12 | SPIRIT 2025: three-view rendering | §3.5 | source exists; needs renders | half-day |

**Numbering (2026-06):** figures are numbered in order of first mention in `paper.qmd`. The executor schematic is Fig 8, the agent cohort Fig 9, the RT-analysis pipeline Fig 10, the multimodal pipeline Fig 11, and the SPIRIT rendering Fig 12. The former *Process + data: EEG `bids:Dataset` exemplar* was removed (no in-text citation); its process-and-data point is carried by F11 plus the worked `Record EEG` / BIDS-dataset example in the Discussion.

Listings (L1-L4) are inline in `paper.qmd` and need no separate files. Supplementary Table S1 (full element catalog) is in `paper.qmd`.

---

## Per-figure specifications

### F1 — "Many artifacts, one study" schematic
**Where it lands:** §1.2 (Current practice fragments the study across artifacts).

**What it shows:** A single study reaching four stakeholder audiences through four incompatible artifacts that drift over time. Proposed layout: 4-panel grid, one panel per artifact family with its characteristic failure mode.

- Panel a — Prose: a protocol PDF with a redline annotation showing how it diverged from the running code.
- Panel b — Box-and-arrow: a CONSORT-style flow figure with a stale arrow / orphan box.
- Panel c — Code: a Nextflow / GitHub Actions config snippet, opaque to a non-engineer reviewer.
- Panel d — Ontology / schema: a BIDS/CSVW JSON sidecar, with a comment "no process semantics."

Centre callout: "One study. Four artifacts. Four divergent representations of the same procedure." Illustrative line drawing, restrained colour, legible in black and white.

### F2 — Studyflow element palette / layers
**Where it lands:** §2.1 (Studyflow as a formal object).

**Status:** drafted — [`fig-elements.png`](fig-elements.png), exported (2026-07-16) from `studyflow-modeler/src/assets/examples/kitchensink.studyflow` (the *Studyflow element catalog*). One live instance of every palette element, one labelled band per schema: the BPMN 2.0 base first (events, gateways, activities, data), then the studyflow core and the domain extensions that specialize it. Attribute values echo the paper's example study (consent form, completion code, eligibility criteria, N-back scene, BDM trials dataset). The PNG carries the full source in its `studyflow` chunk, so the deposited figure is the editable diagram.

**Action:** caption from §2.1 (core vs optional domain layers). Re-export from the modeler if the schemas change.

### F3 — Modeler UI composite
**Where it lands:** §2.3 (The Studyflow toolkit — modeler).

**Status:** four annotated screenshots exist at [`../../../studyflow-modeler/docs/assets/img/screenshots/`](../../../studyflow-modeler/docs/assets/img/screenshots/) — `3-drag.png`, `4-inspector.png`, `8-simulate.png`, `9-publish.png`.

**Action:** compose a 2×2 grid with workflow callouts (palette → inspector → simulate → publish). Save as `fig3_modeler-ui.png`.

### F4 — Runner walkthrough composite
**Where it lands:** §2.3 (The Studyflow toolkit — runner).

**Status:** gap. Depends on the §3.2 bot-mode round-trip (see [`../_checklist.md`](../_checklist.md)).

**What it shows:** four to six panels following a participant through the §3.2 n-back: consent screen → instruction → mid-task (Behaverse Unity iframe) → end-screen with completion code. Run on `seed=42`. Save as `fig4_runner-walkthrough.png` with a thumbnail of the original `.studyflow` beside it.

### F5 — Four views of the same diagram
**Where it lands:** §2.2 (Multiple views: Study / Gantt / Checklist / Figure).

**Existing assets:**
- Study view: render of [`../../assets/figures/fig2.studyflow.svg`](../../assets/figures/fig2.studyflow.svg).
- Gantt view: [`../../../studyflow-modeler/docs/assets/img/gantt_task.studyflow.svg`](../../../studyflow-modeler/docs/assets/img/gantt_task.studyflow.svg) and `timeline_patterns.png`.
- Checklist view: **gap** — needs a screenshot once that view is ready.
- Figure view: a curated SVG export with elements shown/hidden.

**Action:** compose once the Checklist screenshot is available. Save as `fig5_views.png`.

### F6 — CONSORT 2025 vs Studyflow
**Where it lands:** §3.1 (Design).

**Existing assets:**
- Panel a (reference): [`../../assets/figures/old/consort2025.jpg`](../../assets/figures/old/consort2025.jpg).
- Panel b (Studyflow reproduction): [`../../assets/figures/fig2.studyflow.svg`](../../assets/figures/fig2.studyflow.svg).
- Panel c (annotated comparison): [`../../assets/figures/old/consort_annotated.studyflow.png`](../../assets/figures/old/consort_annotated.studyflow.png).

**Action:** compose as `fig6_consort.png`. Caption from §3.1.

### F7 — N-back: slide → Studyflow → XML
**Where it lands:** §3.2 (Enroll and run).

**Existing assets:**
- Panel a: traditional slide-style figure at [`../../assets/figures/old/nback.png`](../../assets/figures/old/nback.png).
- Panel b: Studyflow diagram at [`../../assets/figures/fig3.studyflow.svg`](../../assets/figures/fig3.studyflow.svg).
- Panel c: the XML snippet of Listing 3.

**Action:** compose as `fig7_nback.png`. The trial-by-trial encoding is pedagogical; §3.2 also describes the single cognitive-task encoding the runner actually expands — caption should acknowledge both.

### F8 — One executor, many actors
**Where it lands:** §3.2 ("One executor, many actors"), referenced as Figure 8.

**Status:** drafted — [`fig8_executors.svg`](fig8_executors.svg). Hand-authored line drawing, full-width.

**What it shows:** one Studyflow diagram feeds the runner, which per trial marshals inputs into and records outputs from a single executor function, `executor(stimulus, responses, timing, frame?) -> (response, response_time)`. Four interchangeable packages implement that one interface: a human package that renders a participant-facing UI and blocks on a person, CogEnv driving an RL policy through the Behaverse assessment bot interface, CogPonder (PonderNet RNN) returning a response and a pondered response time, and a language-model package (vision-capable models also read the rendered frame). All four write to one trials table (BDM, Psych-DS-compatible), so human and agent co-subjects compare row for row.

**To finalize:** redraw only if the interface or the CogPonder package changes shape before submission. Restrained colour (one accent), legible in black and white.

### F9 — Agent-cohort accuracy & RT profiles
**Where it lands:** §3.2 ("The agent cohort"), referenced as Figure 9.

**Status:** gap. Depends on the seed-42 cohort runs (the `@tbl-agents` data is `[FILL]`).

**What it shows:** per-task accuracy and median response-time profiles across the model series (uniform-random baseline, CogPonder, RL via CogEnv, open-weight text LLMs, vision-language Claude) with the ten-participant human arm overlaid, so trait-faithfulness across tasks and the human-versus-agent ordering are both visible. Save as `fig9_agent-cohort.svg` (commit the summary data alongside).

### F10 — RT analysis pipeline + dplyr side-by-side
**Where it lands:** §3.3 (Measure agreement).

**Status:** gap, depends on the §3.3 dataset.

**Source:** the worked `RTAnalysis` example in [`../rt_analysis.studyflow`](../rt_analysis.studyflow) (and `studyflow-modeler/docs/reference/data.qmd`) has the Studyflow form and an equivalent dplyr block. Render the subprocess (left panel) next to the dplyr code (right panel). Save as `fig10_rt-pipeline.png`.

### F11 — Multimodal preprocessing/training pipeline
**Where it lands:** §3.4 (Model agreement).

**Status:** gap. Author from the spec in §3.4: **Ingest** (Datasets from a DataCatalog) → **modality-specific preprocessing** (parallel `PreprocessfMRI` / `PreprocessEEG`, plus BDM behavioral conversion) → **multiverse expansion** (`Compose` branching on alternative parameter sets) → **harmonised corpus output** (back to the catalog under canonical addresses).

Authorable in the modeler from the `omniprocess` schema layer (`PreprocessfMRI`, `PreprocessEEG`, `Transform`, `Map`, `Reduce`, `Filter`, `Compose`). Save source as `fig11_multimodal.studyflow` and render as `fig11_multimodal.svg`. Caption: a use-case sketch (deployed pipeline forthcoming).

### F12 — SPIRIT 2025: three-view rendering
**Where it lands:** §3.5 (Report).

**Source:** [`../../../studyflow-modeler/src/assets/examples/spirit2025.studyflow`](../../../studyflow-modeler/src/assets/examples/spirit2025.studyflow) (exists). Reference image: [`../../assets/figures/old/spirit2025.jpg`](../../assets/figures/old/spirit2025.jpg).

**Action:** render Study, Gantt (the SPIRIT schedule), and Checklist views from `spirit2025.studyflow`, alongside the reference image as a composite. Save as `fig12_spirit.png`.

---

## Listings (inline in `paper.qmd`, no separate files)

- **L1** — Studyflow LinkML language excerpt (§2.1). Done.
- **L2** — moddle definition of two research gateways (§2.1). Done.
- **L3** — n-back task serialized as BPMN 2.0 XML (§3.2). Done.
- **L4** — EBNF grammar (§5.3). Done.
