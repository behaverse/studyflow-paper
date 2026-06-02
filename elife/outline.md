# eLife Paper — Structure and Status

**Working title:** *Studyflow: a BPMN-based visual notation for end-to-end specification of experimental research in cognitive sciences*

---

## Paper structure

### §1 Introduction

| § | Title | Summary | Status |
|---|---|---|---|
| 1.1 | The reproducibility gap is in *processes*, not just data | Process is the missing half of reproducibility; voluntary narrative checklists have empirically failed and a machine-readable, human-understandable representation of the *processes* that generated the data is what's needed. | drafted |
| 1.2 | Current practice fragments the study across artifacts | Today's tooling organizes into four families (figures, checklists, data standards, code) that each cover one slice and force researchers to maintain divergent artifacts that drift. | drafted |
| 1.3 | BPMN as a foundation | Studyflow extends BPMN, a mature ISO-standard process notation with a built-in extension mechanism, rather than inventing a new language. | drafted |
| 1.4 | Contributions | Five independently usable artifacts: a LinkML language specification, layered schemas, worked example diagrams, the Studyflow Modeler, and the Studyflow Runner. The paper-structure roadmap paragraph was removed (signposting). | drafted |

### §2 Results

One worked example threads the whole section: a single study that administers a **six-task Behaverse battery** (n-back, digit span, multiple-object tracking, pattern comparison, Belval matrices, Belval card sorting) to human participants and a **panel of agents (model × persona × task)**, walked through its full lifecycle. §2.1–§2.4 describe the artifacts; §2.5–§2.9 are the lifecycle (Design → Collect → Analyze → Model → Report).

| § | Title | Summary | Status |
|---|---|---|---|
| 2.1 | The Studyflow language | BPMN 2.0 plus four research extensions (`Study` container, cognitive activity types, data elements and operations, decision-making gateways), partitioned into a small core, a companion cognitive layer, and four optional domain schemas. | drafted |
| 2.2 | The Studyflow Modeler | A client-side, schema-driven `bpmn-js` editor whose palette and inspector are generated from the moddle schemas so language and editor stay in sync. | drafted |
| 2.3 | The Studyflow Runner | A separate client-side application that parses, validates, and walks a participant or agent through a `.studyflow` diagram node by node, with seeded determinism and three response sources for Behaverse tasks (Unity in-game bot, runner-side random, per-trial LLM bridge). | drafted |
| 2.4 | The three views (Study / Gantt / Checklist) | One source renders three ways (Study for procedural structure, Gantt for wall-clock timing, Checklist for reporting-guideline coverage), each tuned to a different reader. | drafted |
| 2.5 | Design: the protocol, randomization, and reporting scaffolding | The battery study designed as a CONSORT 2025 / SPIRIT 2025-scaffolded RCT; attrition encoded as boundary error events makes the diagram's topology match the trial's, so the published figure *is* the file that ran the study. | drafted (reframed from "Demonstration I — CONSORT") |
| 2.6 | Collect: one diagram, many executors | The 6-task battery administered to humans + a model × persona × task agent panel; n-back is the worked detail (Figure 7); each task is a nested Behaverse timeline of blocks; the screenshot/vision pathway is essential for the spatial tasks; folds in multi-agent/choreography. | drafted; `[N]`/`[X.X]` placeholders pending real seed-42 runs (no human numbers claimed). Backed by `cognitive_battery.studyflow` (authored). |
| 2.7 | Analyze and compare | A reproducible RT + accuracy pipeline over the collected trials, grouped by task × executor × persona, with process and data on one diagram and schema-bound I/O, is itself the pre-registration of the analysis. | drafted (folds old 2.7 + 2.9); `[GAP]` on the worked RT dataset. |
| 2.8 | Model: a machine-learning pipeline in the same notation | The same battery trials feed a model; OmniProcess sketches multimodal preprocessing/training (EEG, fMRI, behavioral) with multiverse-expansion branches as first-class elements. | drafted (was 2.10); deployed pipeline forthcoming. |
| 2.9 | Report and publish | The CONSORT figure is exported from the file that ran the study; reporting-guideline conformance (eleven listed) becomes a checkable diagram property. | drafted (folds old 2.8 reporting-guideline coverage) |

### §3 Discussion

| § | Title | One-line summary | Status |
|---|---|---|---|
| 3.1 | What Studyflow changes | Stakeholder alignment, versioned artifacts, independent specification, process-and-data on one diagram, one protocol with many executors, together yielding trust by construction. | drafted |
| 3.2 | Relationship to existing ecosystems | Studyflow complements rather than replaces execution stacks (Nextflow, CWL), data standards (BIDS, BDM), reporting guidelines (CONSORT, SPIRIT), and sibling BPMN profiles, occupying the space that LinkML/NIDM/BIDS/ARTEM-IS together leave open. | drafted |
| 3.3 | Future directions | Roadmap: timeseries/event-marker data structures, storage/governance operations, tidyverse-mirrored operators, runner support for parallel gateways and true stratified allocation and choreography traversal, empirical UX studies, and language extensions. | drafted |

### Code and data availability

| Section | One-line summary | Status |
|---|---|---|
| Code and data availability | MIT-licensed and browser-only artifacts; hosted modeler and runner URLs; repository pointers for the modeler, the canonical LinkML schema, and the example diagrams (the battery, the CONSORT/SPIRIT templates, and the three agent-profiling bot demos). | drafted |

**Methods folded into §2 (RSA-style):** the former §M.1–M.8 sections were dissolved into the results body. The LinkML schema as single source of truth, the BPMN extension mechanism, the schema layering, the modeler / runner architectures, the layered validation, the publishing flow, and the three views are now covered inline in §2.1–§2.4 and §2.6. The EBNF grammar lives in the repository spec; Listings 1, 2, and 3 are referenced from supplementary materials. The formal tuple definition has been dropped as not eLife-audience-friendly. The §2 results intro and the §1.4 paper-structure roadmap were removed so the text reads stand-alone (no "this section / next section" signposting, no in-text repo paths/URLs/section cross-references).

---

## Figures and listings

| # | Title | Source / status |
|---|---|---|
| **F1** | "Many artifacts, one study" schematic | to be designed |
| **F2** | Studyflow element palette | [`assets/figures/fig1.studyflow.svg`](../assets/figures/fig1.studyflow.svg) — exists |
| **F3** | Modeler UI | Compose from [`screenshots/`](../assets/figures/screenshots/), needs composition |
| **F4** | Runner walkthrough (battery) | record from §2.6; should include an LLM-bot trial-log panel (`[claude:claude-haiku-4-5] trial 17 → "Match"`) and at least one spatial task solved via the screenshot pathway |
| **F5** | Three views of same diagram | Study + Gantt + Checklist |
| **F6** | CONSORT 2025 vs Studyflow | [`old/consort2025.jpg`](../assets/figures/old/consort2025.jpg) + [`fig2.studyflow.svg`](../assets/figures/fig2.studyflow.svg) + [`old/consort_annotated.studyflow.png`](../assets/figures/old/consort_annotated.studyflow.png) — exists |
| **F7** | N-back: slide → Studyflow → XML (worked task detail) | exists |
| **F8** | RT analysis pipeline + dplyr side-by-side | docs/reference/data.qmd; needs rendering |
| **F9** | SPIRIT 2025 vs Studyflow SPIRIT (three views) | exists in examples |
| **F10** | Process + data: EEG `bids:Dataset` example | now folded into §2.7 prose; figure no longer referenced — drop or re-cite |
| **F11** | OmniProcess preprocessing pipeline | TODO; anchors §2.8 |
| **F12** | Three-runtime composition (human / RL / LLM from one source) | TODO; anchors §2.6 |
| **F13** | Agent-panel profile (accuracy + RT per model × persona × task vs. random baseline) | TODO; depends on running the bot demos + battery with seed 42 — placeholders in place in §2.6 |
| **F14** | The 6-task battery as a Studyflow | render/export from `cognitive_battery.studyflow` (authored) |
| **L1** | LinkML schema excerpt | now in supplementary (was Listing 1) |
| **L2** | XML serialization example | now in supplementary (was Listing 2) |
| **L3** | EBNF grammar | now in supplementary (was Listing 3) |
| **Table 2** | Reporting-guideline coverage matrix (§2.9) | CONSORT/SPIRIT marked Yes; 9 others TODO. CONSORT 2025 = **30 items** (not 25). |
| **Table 3** | Agent-panel profile summary (model × persona × task × accuracy × median RT × random-fallback rate) | TODO; depends on running the bot demos + battery with seed 42 — placeholders in place in §2.6 |

---

## Open decisions

- **Empirical anchor for §2.6** — run the three bot demos (`bot_external`, `bot_claude`, `bot_ollama`) plus `cognitive_battery.studyflow` with seed 42 to fill the `[N]`/`[X.X]%` placeholders across model × persona × task (up to ~6 tasks × 3 models × 3 personas + random baseline). No human numbers are claimed; human arm is described as protocol.
- **Empirical commitment for §2.7** — which worked RT dataset for Figure 8? The agent-panel pilot (seed 42) is the reproducible anchor; a human battery RT dataset can slot into the same schema when available.
- **Ethics statement** — needed only if human-subject data is collected; the bot-mode battery pilot avoids this for the first submission.
- **MIT LICENSE** — the `studyflow-modeler` repo has no top-level LICENSE file and no `license` field in `package.json` (only the LinkML schema header says MIT). The paper claims "MIT-licensed" in §2.2 and Code-and-data. Add the LICENSE file (spawned as a separate task).
- **LinkML "versioned separately"** — §2.2 / Code-and-data say the canonical LinkML schema lives at `github.com/behaverse/schemas`, but in the modeler checkout it is bundled under `src/assets/schemas/studyflow.linkml.yaml`. Confirm the separate repo exists, or soften the claim.
- **Schema version sync** — minor spread across files: `package.json` 26.0505.dev2, `studyflow.linkml.yaml` 26.0526-dev1, moddle schemas 26.0528. (The earlier 25.x mismatch is resolved.)
- **`%!VERIFY` entries in `references.bib`** — Zotero double-check pending; new entries added this round: `hair2019iicarus` (IICARus PLOS ONE RCT) and `hopewell2025consort` (CONSORT 2025, co-published in BMJ/Lancet/JAMA/Nature Medicine/PLOS Medicine).

---

## Resources

| What | Where |
|---|---|
| The full draft prose | [`paper.qmd`](paper.qmd) |
| §2.6 task and protocol runbook | [`nback_demo.qmd`](nback_demo.qmd) — **stale**: describes the old N-back-only §2.6; needs updating to the 6-task battery |
| Checklist | [`checklist.md`](checklist.md) |
| Old draft | [`../archived/`](../archived/) |
| The modeler app | [`../../studyflow-modeler/`](../../studyflow-modeler/) |
| Modeler docs | [`../../studyflow-modeler/docs/`](../../studyflow-modeler/docs/) |
| Schemas | [`../../studyflow-modeler/src/assets/schemas/`](../../studyflow-modeler/src/assets/schemas/) |
| Example diagrams | [`../../studyflow-modeler/src/assets/examples/`](../../studyflow-modeler/src/assets/examples/) |
| **6-task battery (new, §2.6)** | [`cognitive_battery.studyflow`](../../studyflow-modeler/src/assets/examples/cognitive_battery.studyflow) |
| N-back study | [`lablink_demo1.studyflow`](../../studyflow-modeler/src/assets/examples/lablink_demo1.studyflow) |
| CONSORT / SPIRIT templates | [`consort2025.studyflow`](../../studyflow-modeler/src/assets/examples/consort2025.studyflow) · [`spirit2025.studyflow`](../../studyflow-modeler/src/assets/examples/spirit2025.studyflow) |
| Shipping bot demos | [`bot_external.studyflow`](../../studyflow-modeler/src/assets/examples/bot_external.studyflow) · [`bot_claude.studyflow`](../../studyflow-modeler/src/assets/examples/bot_claude.studyflow) · [`bot_ollama.studyflow`](../../studyflow-modeler/src/assets/examples/bot_ollama.studyflow) |
