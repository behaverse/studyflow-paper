# Figures for the eLife paper

This folder collects the figures and listings referenced by [`../paper.md`](../paper.md). Drop authored figures here as they are produced; the table below tracks which are done, which are gaps, and which need composition from existing assets.

## Conventions

- **File naming.** `fig1_shortname.svg`, `fig2_…`, … `fig12_…`, `figM1_…` matching the figure numbers in `paper.md`. Lowercase, no zero-padding; methods figure uses `figM` prefix. Use SVG for line drawings/diagrams, PNG for screenshots/composites.
- **Sizing.** Target eLife column widths: 88 mm (single column) for inline figures, 180 mm (full width) for multi-panel composites.
- **Source files.** When a figure is composed from a Studyflow diagram, commit both the rendered SVG and the underlying `.studyflow` source (or pin a commit SHA from `studyflow-modeler/src/assets/examples/`) so reviewers can verify the figure traces back to a runnable file.
- **Captions.** Drafted in `paper.md` next to each figure reference. Keep captions self-contained — a reader skimming figures should understand the claim without reading the body.

---

## Figure inventory

| # | Title | Status | Effort | Owner |
|---|---|---|---|---|
| F1 | "Many artifacts, one study" schematic | **gap** | half-day | ? |
| F2 | Studyflow element palette | exists; needs caption | 30 min | ? |
| F3 | Modeler UI composite | needs composition | 2 h | ? |
| F4 | Runner walkthrough composite | **gap** (depends on §2.6 round-trip) | half-day | Hoorieh |
| F5 | Three views: Study / Timeline / Checklist | partial — Checklist screenshot is gap | 30 min once Checklist view ships | ? |
| F6 | CONSORT 2025 vs Studyflow | exists; needs composition + caption | 30 min | ? |
| F7 | N-back: slide → Studyflow → XML | exists; needs composition + caption | 30 min | ? |
| F8 | Executors: one interface, four packages (§2.6) | **drafted** — `fig8_executors.svg` | done | Claude/Morteza |
| F9 | Agent-panel accuracy & RT profiles (§2.6) | **gap** (depends on seed-42 runs) | 2 h | ? |
| F10 | RT analysis pipeline + dplyr side-by-side | **gap** (depends on §2.7) | 2 h | ? |
| F11 | OmniProcess subgraph (preprocessing pipeline) | **gap** | 2 h | ? |
| F12 | SPIRIT 2025: three-view rendering | source exists; needs renders | half-day | ? |
| F-M1 | Modeler architecture block diagram | **gap** | half-day | ? |

**Renumbered (2026-06):** figures are now numbered in order of first mention in `paper.qmd`. Executor schematic 12→8, agent panel 13→9, RT-analysis pipeline 8→10, SPIRIT rendering 9→12; OmniProcess stays 11. The former *Process + data: EEG `bids:Dataset` exemplar* (previously F10) was removed — it had no in-text citation, and its process-and-data demonstration is now carried by the OmniProcess multimodal figure (F11) together with the worked `Record EEG` / BIDS-dataset example in the Discussion.

Listings (L1–L3) are inline in `paper.md` and need no separate files. Supplementary Table S1 (full element catalog) is a separate gap tracked in [`../tasks.md`](../tasks.md).

---

## Per-figure specifications

### F1 — "Many artifacts, one study" schematic

**Where it lands:** §1.2 (Current practice fragments the study across artifacts).

**What it shows:** A single study reaching four stakeholder audiences through four incompatible artifacts that drift over time. Proposed layout: 4-panel grid, one panel per artifact family with its characteristic failure mode.

- Panel a — Prose: a protocol PDF with a redline annotation showing how it diverged from the running code.
- Panel b — Box-and-arrow: a CONSORT-style flow figure with a stale arrow / orphan box.
- Panel c — Code: a Nextflow / GitHub Actions config snippet, opaque to a non-engineer reviewer.
- Panel d — Ontology / schema: a BIDS/CSVW JSON sidecar, with a comment "no process semantics."

Centre callout: "One study. Four artifacts. Four divergent representations of the same procedure."

**Style:** illustrative line drawing, restrained colour, suitable for a black-and-white print render.

### F2 — Studyflow element palette

**Where it lands:** §2.1 (The Studyflow language).

**Status:** exists at [`../../assets/figures/fig1.studyflow.svg`](../../assets/figures/fig1.studyflow.svg).

**Action:** copy into this folder as `fig2_element-palette.svg`. Caption from `paper.md` §2.1 ("the partition into core and optional domain extensions") — keep concise.

### F3 — Modeler UI composite

**Where it lands:** §2.2 (The Studyflow Modeler).

**Status:** four annotated screenshots already exist at [`../../../studyflow-modeler/docs/assets/img/screenshots/`](../../../studyflow-modeler/docs/assets/img/screenshots/) — `3-drag.png`, `4-inspector.png`, `8-simulate.png`, `9-publish.png`.

**Action:** compose a 2×2 grid, annotate each panel with the seven-step workflow callouts (palette → inspector → simulate → publish). Save as `fig3_modeler-ui.png`.

### F4 — Runner walkthrough composite

**Where it lands:** §2.3 (The Studyflow Runner).

**Status:** gap. Depends on the §2.6 bot-mode round-trip (see [`../checklist.md`](../checklist.md)).

**What it shows:** Four to six panels following a participant through the §2.6 N-back: consent screen → Welcome instruction → mid-1-back (Behaverse Unity iframe) → end-screen with completion code. Run on `seed=42` for reproducibility. Save as `fig4_runner-walkthrough.png` plus a thumbnail of the original `.studyflow` next to it.

### F5 — Three views of the same diagram

**Where it lands:** §2.4 (The three views).

**Existing assets:**
- Study view source: render of [`../../assets/figures/fig2.studyflow.svg`](../../assets/figures/fig2.studyflow.svg) or `fig3.studyflow.svg`.
- Timeline (Gantt) view: [`../../../studyflow-modeler/docs/assets/img/gantt_task.studyflow.svg`](../../../studyflow-modeler/docs/assets/img/gantt_task.studyflow.svg) and [`timeline_patterns.png`](../../../studyflow-modeler/docs/assets/img/timeline_patterns.png).
- Checklist view: **gap** — needs a screenshot of the modeler's Checklist view once that view is ready.

**Action:** compose a 3-panel figure once the Checklist screenshot is available. Save as `fig5_three-views.png`.

### F6 — CONSORT 2025 vs Studyflow

**Where it lands:** §2.5 (Demonstration I — CONSORT).

**Existing assets:**
- Panel a (reference): [`../../assets/figures/old/consort2025.jpg`](../../assets/figures/old/consort2025.jpg).
- Panel b (Studyflow reproduction): [`../../assets/figures/fig2.studyflow.svg`](../../assets/figures/fig2.studyflow.svg).
- Panel c (annotated comparison): [`../../assets/figures/old/consort_annotated.studyflow.png`](../../assets/figures/old/consort_annotated.studyflow.png).

**Action:** compose as `fig6_consort.png`. Write caption from `paper.md` §2.5 lead.

### F7 — N-back: slide → Studyflow → XML

**Where it lands:** §2.6 (Demonstration II — N-back).

**Existing assets:**
- Panel a: traditional slide-style figure at [`../../assets/figures/old/nback.png`](../../assets/figures/old/nback.png).
- Panel b: Studyflow diagram at [`../../assets/figures/fig3.studyflow.svg`](../../assets/figures/fig3.studyflow.svg).
- Panel c: XML snippet — already drafted in [`../paper.md`](../paper.md) and in `joss/paper.md`. Render as a small code block within the figure.

**Action:** compose as `fig7_nback.png`. The trial-by-trial encoding shown here is pedagogical; §2.6 prose now also describes the block-level `behaverse:behaverseTask` encoding that is actually executed by the runner — caption should acknowledge both.

### F8 — Executors: one interface, four packages

**Where it lands:** §2.6 ("Four kinds of executor"), referenced in prose as Figure 8.

**Status:** drafted — [`fig8_executors.svg`](fig8_executors.svg). Hand-authored line drawing, full-width.

**What it shows:** one Studyflow diagram feeds the Runner, which prepares each executor's environment once and, per trial, marshals the inputs into and records the outputs from a single executor function, `executor(stimulus, responses, timing, frame?) -> (response, response_time)`. Four interchangeable packages implement that one interface: a human package that renders a participant-facing UI and blocks on a person, CogEnv driving an RL policy through the Behaverse assessment bot interface, CogPonder (PonderNet RNN) returning a response and a pondered response time, and a language-model package (vision-capable models also read the rendered frame). All four write to one trials table (BDM, Psych-DS-compatible) whose columns are fixed by the schema, so the human arm and the agent panel compare row for row.

**To finalize:** the diagram reflects the intended uniform-interface architecture; redraw only if that interface or the CogPonder package changes shape before submission. Keep restrained colour (one teal accent), legible in black and white.

### F9 — Agent-panel accuracy & RT profiles

**Where it lands:** §2.6 ("Profiling a panel of agents"), referenced in prose as Figure 9.

**Status:** gap. Depends on the seed-42 panel runs (the `@tbl-agents` data is `[FILL]`).

**What it shows:** per-task accuracy and median response-time profiles across the five model series (uniform-random baseline, CogPonder, RL via CogEnv, open-weight text LLMs, vision-language Claude) with the ten-participant human arm overlaid, so trait-faithfulness across tasks and the human-versus-agent ordering are both visible. Save as `fig9_agent-panel.svg` (commit the underlying summary data alongside).

### F10 — RT analysis pipeline + dplyr side-by-side

**Where it lands:** §2.7 (Demonstration III — A reproducible analysis pipeline).

**Status:** gap, depends on §2.7 empirical commitment.

**Source content:** the worked `RTAnalysis` example in [`../../../studyflow-modeler/docs/reference/data.qmd`](../../../studyflow-modeler/docs/reference/data.qmd) has the EBNF/YAML form of the Studyflow and an equivalent dplyr code block. Render the Studyflow subprocess as a diagram (left panel) next to the dplyr code (right panel). Save as `fig10_rt-pipeline.png`.

### F11 — OmniProcess subgraph

**Where it lands:** §2.10 (Beyond data collection: multimodal preprocessing).

**Status:** gap. Author from the four-movement spec in `paper.md` §2.10: **Ingest** (Datasets from a DataCatalog) → **Modality-specific preprocessing** (parallel `PreprocessfMRI` and `PreprocessEEG` subprocesses, plus BDM behavioral conversion) → **Multiverse expansion** (`Compose` branching on alternative parameter sets) → **Harmonised corpus output** (back to the catalog under canonical addresses).

The diagram should be authorable in the modeler using elements that already ship in the `omniprocess` schema layer (`PreprocessfMRI`, `PreprocessEEG`, `Transform`, `Map`, `Reduce`, `Filter`, `Compose`). Save the source as `fig11_omniprocess.studyflow` and the render as `fig11_omniprocess.svg`. Caption should note that this is a use-case sketch (deployed pipeline forthcoming).

### F12 — SPIRIT 2025: three-view rendering

**Where it lands:** §2.8 (Coverage across reporting guidelines).

**Source:** [`../../../studyflow-modeler/src/assets/examples/spirit2025.studyflow`](../../../studyflow-modeler/src/assets/examples/spirit2025.studyflow) (378 lines, exists). Reference image: [`../../assets/figures/old/spirit2025.jpg`](../../assets/figures/old/spirit2025.jpg).

**Action:** render three views from `spirit2025.studyflow` — Study, Timeline (the SPIRIT schedule), Checklist — and place alongside the reference image as a 4-panel composite. Save as `fig12_spirit.png`.

### F-M1 — Modeler architecture block diagram

**Where it lands:** §M.4 (Modeler architecture).

**Status:** gap. Block diagram with four columns:

1. **Schemas** (left): canonical LinkML schema at `schemas/studyflow/schema.linkml.yaml`, the six moddle YAML schemas at `studyflow-modeler/src/assets/schemas/`.
2. **Core library** (centre-left): `src/lib/core/` modules — `parsers/moddle-schema.ts`, `parsers/studyflow.ts`, the `extensions/` directory (attrs / defaults / attributeDefinitions / extensionType / resolve / wrapper).
3. **Apps** (centre-right): `src/modeler/` packages (palette / inspector / contextpad / render / simulation / commands) and `src/runner/` (nodes / phase machine).
4. **Outputs** (right): `.studyflow` files (BPMN 2.0 XML), the Behaverse Data Server, exported SVG/PNG figures.

Arrows show data/schema flow. Save as `figM1_architecture.svg`.

---

## Listings (inline in `paper.md`, no separate files needed)

- **L1** — LinkML schema excerpt (§M.1). Done.
- **L2** — XML serialization example with `studyflow:` and `cognitive:` namespaces (§M.2). Done.
- **L3** — EBNF grammar (§M.8). Done.

If the EBNF moves to Supplementary Information (an option flagged in §M.8), L3 stays as-is in the supplement.
