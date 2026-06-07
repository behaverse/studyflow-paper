# Figures for the eLife paper

This folder collects the figures and listings referenced by [`../paper.qmd`](../paper.qmd). Drop authored figures here as they are produced; the table below tracks which are done, which are gaps, and which need composition from existing assets.

## Conventions

- **File naming.** `fig1_shortname.svg`, `fig2_…`, … `fig12_…` matching the figure numbers in `paper.qmd`. Lowercase, no zero-padding. Use SVG for line drawings/diagrams, PNG for screenshots/composites.
- **Sizing.** Target eLife column widths: 88 mm (single column) for inline figures, 180 mm (full width) for multi-panel composites.
- **Source files.** When a figure is composed from a Studyflow diagram, commit both the rendered SVG and the underlying `.studyflow` source (or pin a commit SHA from `studyflow-modeler/src/assets/examples/`) so reviewers can verify the figure traces back to a runnable file.
- **Captions.** Drafted in `paper.qmd` next to each figure reference. Keep captions self-contained: a reader skimming figures should understand the claim without reading the body.

---

## Figure inventory

| # | Title | §  | Status | Effort |
|---|---|---|---|---|
| F1 | "Many artifacts, one study" schematic | §1.2 | **gap** | half-day |
| F2 | Studyflow element palette / layers | §2.1 | exists; needs caption | 30 min |
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

**Status:** exists at [`../../assets/figures/fig1.studyflow.svg`](../../assets/figures/fig1.studyflow.svg).

**Action:** copy into this folder as `fig2_element-palette.svg`. Caption from §2.1 (core vs optional domain layers).

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
