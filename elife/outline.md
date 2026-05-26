# eLife Paper — Structure and Status

**Working title:** *Studyflow: a BPMN-based notation, modeler, and runner for end-to-end specification of experimental research workflows in cognitive sciences*

**Canonical source:** [`paper.md`](./paper.md) — full draft, ~11.7k words. This file is a navigation/status document only; the paper is the source of truth.

**Related files in this folder:**
- [`paper.md`](./paper.md) — full manuscript draft
- [`references.bib`](./references.bib) — merged bibliography (80 entries)
- [`tasks.md`](./tasks.md) — remaining work, with effort estimates
- [`nback_demo.md`](./nback_demo.md) — runbook for the §2.6 empirical anchor

---

## Paper structure

| Section | Subsections | Status |
|---|---|---|
| **Front matter** | Title, authors (Ansarinia, Afkari Roshan, Cardoso-Leite), abstract (~156 w), impact statement (~39 w), keywords | drafted |
| **§1 Introduction** (~1.2k w) | 1.1 The reproducibility gap is in processes · 1.2 Current practice fragments the study · 1.3 BPMN as a foundation · 1.4 Contributions and roadmap (4 artifacts) | drafted |
| **§2 Results** (~5.5k w) | 2.1 The Studyflow language · 2.2 The Modeler · 2.3 The Runner · 2.4 Three views (Study/Timeline/Checklist) · 2.5 CONSORT demo · 2.6 N-back end-to-end · 2.7 RT analysis pipeline · 2.8 Reporting-guideline coverage · 2.9 Process + data in one diagram · 2.10 OmniProcess (multimodal preprocessing) · 2.11 Multi-agent / choreography | drafted; §2.6 and §2.7 carry empirical `[GAP]` markers |
| **§3 Discussion** (~1.5k w) | 3.1 What Studyflow changes · 3.2 Relationship to existing ecosystems · 3.3 Limitations · 3.4 Future directions | drafted |
| **§4 Methods** (~2.5k w) | M.1 LinkML schema as single source of truth · M.2 BPMN extension mechanism · M.3 Domain-specific extensions (5 sub-subsections) · M.4 Modeler architecture · M.5 Runner architecture · M.6 Validation and publishing · M.7 Three views · M.8 EBNF grammar · M.9 Reproducibility statement | drafted; F-M1 architecture diagram is `[GAP]` |

**Schema framing:** LinkML schema in `behaverse/schemas/studyflow/` is presented as the canonical single source of truth (the framing the bio-literature audience expects); the moddle YAML mirror at `studyflow-modeler/src/assets/schemas/` is the runtime materialisation `bpmn-moddle` consumes.

---

## Figures and listings inventory

| # | Title | Source / status |
|---|---|---|
| **F1** | "Many artifacts, one study" schematic | `[GAP]` — to be designed |
| **F2** | Studyflow element palette | [`assets/figures/fig1.studyflow.svg`](../assets/figures/fig1.studyflow.svg) — exists |
| **F3** | Modeler UI composite | Compose from [`screenshots/{3-drag,4-inspector,8-simulate,9-publish}.png`](../../studyflow-modeler/docs/assets/img/screenshots/) — exists, needs composition |
| **F4** | Runner walkthrough composite | `[GAP]` — record from §2.6 runbook |
| **F5** | Three views of same diagram | Study + Timeline ([`gantt_task.studyflow.svg`](../../studyflow-modeler/docs/assets/img/gantt_task.studyflow.svg)) exist; Checklist view screenshot is `[GAP, small]` |
| **F6** | CONSORT 2025 vs Studyflow | [`old/consort2025.jpg`](../assets/figures/old/consort2025.jpg) + [`fig2.studyflow.svg`](../assets/figures/fig2.studyflow.svg) + [`old/consort_annotated.studyflow.png`](../assets/figures/old/consort_annotated.studyflow.png) — exists |
| **F7** | N-back: slide → Studyflow → XML | [`old/nback.png`](../assets/figures/old/nback.png) + [`fig3.studyflow.svg`](../assets/figures/fig3.studyflow.svg) + XML snippet — exists |
| **F8** | RT analysis pipeline + dplyr side-by-side | Source content in [`docs/reference/data.qmd`](../../studyflow-modeler/docs/reference/data.qmd); needs rendering |
| **F9** | SPIRIT 2025 vs Studyflow SPIRIT (three views) | [`old/spirit2025.jpg`](../assets/figures/old/spirit2025.jpg) + renders from [`spirit2025.studyflow`](../../studyflow-modeler/src/assets/examples/spirit2025.studyflow) — source exists, renders to author |
| **F10** | Process + data: EEG `bids:Dataset` exemplar | `[GAP, small]` — small new diagram |
| **F11** | OmniProcess subgraph (preprocessing pipeline) | `[GAP]` — author from §2.10 spec |
| **F-M1** | Modeler architecture block diagram | `[GAP]` — Methods figure |
| **L1** | LinkML schema excerpt | Inline in §M.1 — done |
| **L2** | XML serialization example | Inline in §M.2 — done |
| **L3** | EBNF grammar | Inline in §M.8 — done |
| **Table 2** | Reporting-guideline coverage matrix | In §2.8 — CONSORT/SPIRIT marked Yes; 9 others marked `[GAP, small]` |

---

## Open decisions (high-level)

- **Empirical commitment for §2.6** — bot-mode round-trip via `demo1.studyflow` recommended in [`nback_demo.md`](./nback_demo.md). Pending execution.
- **Empirical commitment for §2.7** — RT dataset choice pending (Pedro/Morteza).
- **Ethics statement** — needed if §2.6/§2.7 uses human-subject data; bot-mode path avoids this.
- **Schema-repo version reconciliation** — `schemas/studyflow/README.md` v25.0414 lags `schema.linkml.yaml` header v25.1217.dev; cross-repo edit pending.
- **`%!VERIFY` entries in `references.bib`** — 11 well-known references tagged for Zotero double-check (BIDS, OSC 2015, FAIR, CSVW, Nextflow, CWL, STROBE, STARD, SPIRIT 2013, Kinsman 2021, Teytelman 2016, plus the scoping-review entry that needs author/journal verification).

---

## Where to look for what

| If you want… | Look at |
|---|---|
| The full draft prose | [`paper.md`](./paper.md) |
| Remaining work / effort estimates | [`tasks.md`](./tasks.md) |
| §2.6 round-trip protocol | [`nback_demo.md`](./nback_demo.md) |
| Source content (Quarto chapters, old drafts) | [`../archived/`](../archived/) |
| The modeler app source | [`../../studyflow-modeler/`](../../studyflow-modeler/) |
| Modeler docs (reference, guides, examples) | [`../../studyflow-modeler/docs/`](../../studyflow-modeler/docs/) |
| Schemas (moddle runtime) | [`../../studyflow-modeler/src/assets/schemas/`](../../studyflow-modeler/src/assets/schemas/) |
| Schema (LinkML canonical) | [`../../schemas/studyflow/schema.linkml.yaml`](../../schemas/studyflow/schema.linkml.yaml) |
| Example diagrams | [`../../studyflow-modeler/src/assets/examples/`](../../studyflow-modeler/src/assets/examples/) (`consort2025.studyflow`, `spirit2025.studyflow`, `demo0/1/2.studyflow`) |
