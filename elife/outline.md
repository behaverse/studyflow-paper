# eLife Paper — Structure and Status

**Working title:** *Studyflow: a BPMN-based notation, modeler, and runner for end-to-end specification of experimental research workflows in cognitive sciences*

**Related files in this folder:**
- [`paper.qmd`](./paper.qmd) — full manuscript draft
- [`references.bib`](./references.bib) — merged bibliography
- [`checklist.md`](./checklist.md) — checklist
- [`nback_demo.qmd`](./nback_demo.qmd) — notebook for §2.6

---

## Paper structure

### §1 Introduction

| § | Title | One-line summary | Status |
|---|---|---|---|
| 1.1 | The reproducibility gap is in *processes*, not just data | Process is the missing half of reproducibility; voluntary narrative checklists have empirically failed and a machine-readable, human-understandable representation of the *processes* that generated the data is what's needed. | drafted |
| 1.2 | Current practice fragments the study across artifacts | Today's tooling sorts into four families (figures, checklists, data standards, code) that each cover one slice and force researchers to maintain divergent artifacts that drift. | drafted |
| 1.3 | BPMN as a foundation | Studyflow extends BPMN — a mature, ISO-standard process notation with a built-in extension mechanism — rather than inventing a new graphical language. | drafted |
| 1.4 | Contributions and roadmap | Five independently usable artifacts: a LinkML language specification, layered moddle YAML runtime schemas, worked example diagrams, the Studyflow Modeler, and the Studyflow Runner. | drafted |

### §2 Results

| § | Title | One-line summary | Status |
|---|---|---|---|
| 2.1 | The Studyflow language | BPMN 2.0 plus four research extensions (`Study` container, cognitive activity types, data elements and operations, research gateways), partitioned into a small core and optional domain schemas. | drafted |
| 2.2 | The Studyflow Modeler | A client-side, schema-driven React + `bpmn-js` editor whose palette and inspector are regenerated from the moddle schemas so language and editor stay in sync. | drafted |
| 2.3 | The Studyflow Runner | A separate client-side application that parses, validates, and walks a participant or agent through a `.studyflow` diagram node by node, with seeded determinism and three response sources for Behaverse tasks. | drafted |
| 2.4 | The three views (Study / Gantt / Checklist) | One source renders three ways — Study for procedural structure, Gantt for wall-clock timing, Checklist for reporting-guideline coverage — each tuned to a different reader. | drafted |
| 2.5 | Demonstration I — CONSORT-style randomized controlled trial | A 423-line CONSORT-2025 reference diagram shows that attrition encoded as boundary error events makes the diagram's topology match the trial's topology, so the figure in the paper *is* the file that ran the trial. | drafted |
| 2.6 | Demonstration II — N-back end-to-end | An N-back authored in the modeler and run in the runner closes the "single diagram, many audiences" loop, with Psych-DS-conformant trials emerging from the same source. | drafted; empirical `[GAP]` on the human pilot (the LLM-agent pilot is now §2.12). |
| 2.7 | Demonstration III — A reproducible analysis pipeline | A reaction-time analysis encoded as data-operation markers with schema-bound input/output is itself the pre-registration of the analysis. | drafted; `[GAP]` on the specific RT dataset to use. |
| 2.8 | Coverage across reporting guidelines | Reporting guidelines are structurally a controlled vocabulary plus a checklist plus a flow diagram, so all eleven listed are expressible as a Studyflow and conformance becomes a property of the diagram. | drafted |
| 2.9 | Process and data: one diagram | Process and data live on the same diagram with schema bindings to BIDS/Psych-DS/BDM/CSVW, so contracts between upstream and downstream tasks are verifiable without leaving the file. | drafted |
| 2.10 | Beyond data collection: multimodal preprocessing and foundation-model training | ML pipelines face the same fragmentation as experimental protocols; an OmniProcess Studyflow can specify multimodal harmonisation (EEG, fMRI, behavioural) with multiverse-expansion branches as first-class elements. | drafted; deployed pipeline is forthcoming. |
| 2.11 | Multi-agent / choreography | Joint-action, dyadic, parent-child, and human-LLM confederate designs are modelled through BPMN choreography tasks at the protocol layer above signal-time synchronization (LSL). | drafted |
| 2.12 | Agent profiling: one diagram, three executions | The same `.studyflow` source drives three runtimes today (human participants via the Behaverse Data Server, classic RL agents via CogEnv, and LLM agents via the runner's per-trial bridge to Claude or Ollama), turning the diagram into both a participant protocol and an agent-benchmarking spec without porting. | drafted (new); references shipping demos `demo3_external_bot`, `demo4_llm_bot`, `demo5_ollama_bot`. |

### §3 Discussion

| § | Title | One-line summary | Status |
|---|---|---|---|
| 3.1 | What Studyflow changes | Six numbered advances (stakeholder alignment, versionable artifacts, specification independence, process-and-data on one diagram, reporting-guideline conformance as a property, one protocol with many executors) that together yield trust by construction. | drafted (restructured as numbered list, RSA-style) |
| 3.2 | Relationship to existing ecosystems | Studyflow complements rather than replaces execution stacks (Nextflow, CWL), data standards (BIDS, BDM), reporting guidelines (CONSORT, SPIRIT), and sibling BPMN profiles, occupying the procedural plane that LinkML/NIDM/BIDS/ARTEM-IS together leave open. | drafted; the process-mining boundary moved here from §3.3 |
| 3.3 | Future directions | Roadmap: timeseries/event-marker data structures, storage/governance operations, tidyverse-mirrored operators, runner support for parallel gateways and stratified allocation, downstream-engine emitters (Kedro, Nextflow, NiPype), empirical readability studies, and language extensions for adaptive and single-subject designs. | drafted; absorbs former limitations on adoption + awkward designs. |

### Code and data availability

| Section | One-line summary | Status |
|---|---|---|
| Code and data availability | MIT-licensed and browser-only artifacts; hosted modeler and runner URLs; repository pointers for the modeler, the canonical LinkML schema, and the example diagrams (including the three agent-profiling demos referenced in §2.12). | drafted |

**Methods folded into §2 (RSA-style):** the former §M.1–M.8 sections were dissolved into the results body. The LinkML schema as single source of truth, the BPMN extension mechanism, the schema layering, the modeler / runner architectures, the layered validation, the publishing flow, and the three views are now covered inline in §2.1–§2.4 and §2.12. The EBNF grammar lives in the repository spec; Listings 1, 2, and 3 are referenced from supplementary materials. The formal tuple definition has been dropped as not eLife-audience-friendly.

---

## Figures and listings

| # | Title | Source / status |
|---|---|---|
| **F1** | "Many artifacts, one study" schematic | to be designed |
| **F2** | Studyflow element palette | [`assets/figures/fig1.studyflow.svg`](../assets/figures/fig1.studyflow.svg) — exists |
| **F3** | Modeler UI | Compose from [`screenshots/`](../assets/figures/screenshots/), needs composition |
| **F4** | Runner walkthrough | record from §2.6 runbook; should now include an LLM-bot trial-log panel (`[claude:claude-haiku-4-5] trial 17 → "Match"`) |
| **F5** | Three views of same diagram | Study + Gantt + Checklist |
| **F6** | CONSORT 2025 vs Studyflow | [`old/consort2025.jpg`](../assets/figures/old/consort2025.jpg) + [`fig2.studyflow.svg`](../assets/figures/fig2.studyflow.svg) + [`old/consort_annotated.studyflow.png`](../assets/figures/old/consort_annotated.studyflow.png) — exists |
| **F7** | N-back: slide → Studyflow → XML | exists |
| **F8** | RT analysis pipeline + dplyr side-by-side | docs/reference/data.qmd; needs rendering |
| **F9** | SPIRIT 2025 vs Studyflow SPIRIT (three views) | exists in examples |
| **F10** | Process + data: EEG `bids:Dataset` example | TODO: small new diagram |
| **F11** | OmniProcess preprocessing pipeline | TODO: from §2.10 spec |
| **F12** | Three-runtime composition (human / RL / LLM from one source) | TODO; new, anchors §2.12 |
| **F13** | LLM-agent pilot results (accuracy + RT per persona vs. random baseline) | TODO; depends on running demo4/demo5 with seed 42 — placeholders in place in §2.12 |
| **L1** | LinkML schema excerpt | now in supplementary (was Listing 1) |
| **L2** | XML serialization example | now in supplementary (was Listing 2) |
| **L3** | EBNF grammar | now in supplementary (was Listing 3) |
| **Table 2** | Reporting-guideline coverage matrix | CONSORT/SPIRIT marked Yes; 9 others TODO |
| **Table 3** | LLM-agent pilot summary (configuration × accuracy × median RT × random-fallback rate) | TODO; depends on running demo3/4/5 — placeholders in place in §2.12 |

---

## Open decisions

- **Empirical commitment for §2.6** — LLM-agent pilot is now anchored in §2.12 (Figure 13, Table 3 placeholders); human pilot still TBD.
- **Run demo3, demo4, demo5 with seed 42 to fill §2.12 placeholders** — the prose is in place; only the numbers ([X.X]%, [N] trials) are missing.
- **Empirical commitment for §2.7** — which RT dataset?
- **Ethics statement** — needed if §2.6/§2.7 uses human-subject data; the LLM-agent pilot in §2.12 avoids this for §2.6.
- **Schema version** — `schemas/studyflow/README.md` v25.0414 lags `schema.linkml.yaml` header v25.1217.dev. Fix this.
- **`%!VERIFY` entries in `references.bib`** — 11 well-known references tagged for Zotero double-check (BIDS, OSC 2015, FAIR, CSVW, Nextflow, CWL, STROBE, STARD, SPIRIT 2013, Kinsman 2021, Teytelman 2016).

---

## Resources

| What | Where |
|---|---|
| The full draft prose | [`paper.qmd`](paper.qmd) |
| §2.6 task and protocol | [`nback_demo.qmd`](nback_demo.qmd) |
| Old draft | [`../archived/`](../archived/) |
| The modeler app | [`../../studyflow-modeler/`](../../studyflow-modeler/) |
| Modeler docs | [`../../studyflow-modeler/docs/`](../../studyflow-modeler/docs/) |
| Schemas | [`../../studyflow-modeler/src/assets/schemas/`](../../studyflow-modeler/src/assets/schemas/) |
| Example diagrams | [`../../studyflow-modeler/src/assets/examples/`](../../studyflow-modeler/src/assets/examples/) |
| Shipping LLM-bot demos | [`demo3_external_bot.studyflow`](../../studyflow-modeler/src/assets/examples/demo3_external_bot.studyflow) · [`demo4_llm_bot.studyflow`](../../studyflow-modeler/src/assets/examples/demo4_llm_bot.studyflow) · [`demo5_ollama_bot.studyflow`](../../studyflow-modeler/src/assets/examples/demo5_ollama_bot.studyflow) |
