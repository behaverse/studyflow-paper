# eLife Paper — Structure and Status

**Working title:** *Studyflow: a BPMN-based notation, modeler, and runner for end-to-end specification of experimental research workflows in cognitive sciences*

**Related files in this folder:**
- [`paper.qmd`](./paper.qmd) — full manuscript draft
- [`references.bib`](./references.bib) - merged bibliography
- [`checklist.md`](./checklist.md) - checklist
- [`nback_demo.qmd`](./nback_demo.qmd) — notebook for the §2.6

---

## Paper structure

| Section | Subsections | Status |
|---|---|---|
| **§1 Introduction** | 1.1 The reproducibility gap is in processes · 1.2 Current practice fragments the study · 1.3 BPMN as a foundation · 1.4 Contributions and roadmap (4 artifacts) | drafted |
| **§2 Results** | 2.1 The Studyflow language · 2.2 The Modeler · 2.3 The Runner · 2.4 Three views (Study/Timeline/Checklist) · 2.5 CONSORT demo · 2.6 N-back end-to-end · 2.7 RT analysis pipeline · 2.8 Reporting-guideline coverage · 2.9 Process + data in one diagram · 2.10 OmniProcess (multimodal preprocessing) · 2.11 Multi-agent / choreography | drafted; §2.6 and §2.7 carry empirical `[GAP]` markers |
| **§3 Discussion** | 3.1 What Studyflow changes · 3.2 Relationship to existing ecosystems · 3.3 Limitations · 3.4 Future directions | drafted |
| **§4 Methods**| M.1 LinkML schema as single source of truth · M.2 BPMN extension mechanism · M.3 Domain-specific extensions (5 sub-subsections) · M.4 Modeler architecture · M.5 Runner architecture · M.6 Validation and publishing · M.7 Three views · M.8 EBNF grammar · M.9 Reproducibility statement | drafted; F-M1 architecture diagram is `[MISSING]` |

**Schema framing:** Moddle schema in `studyflow-modeler/src/assets/schemas/` is presented as the canonical single source of truth.

---

## Figures and listings

| # | Title | Source / status |
|---|---|---|
| **F1** | "Many artifacts, one study" schematic | to be designed |
| **F2** | Studyflow element palette | [`assets/figures/fig1.studyflow.svg`](../assets/figures/fig1.studyflow.svg) — exists |
| **F3** | Modeler UI | Compose from [`screenshots/ exists, needs composition |
| **F4** | Runner walkthrough | record from §2.6 runbook |
| **F5** | Three views of same diagram | Study + Timeline + Checklist |
| **F6** | CONSORT 2025 vs Studyflow | [`old/consort2025.jpg`](../assets/figures/old/consort2025.jpg) + [`fig2.studyflow.svg`](../assets/figures/fig2.studyflow.svg) + [`old/consort_annotated.studyflow.png`](../assets/figures/old/consort_annotated.studyflow.png) - exists |
| **F7** | N-back: slide -> Studyflow -> XML | exists |
| **F8** | RT analysis pipeline + dplyr side-by-side | docs/reference/data.qmd; needs rendering |
| **F9** | SPIRIT 2025 vs Studyflow SPIRIT (three views) | exists in examples |
| **F10** | Process + data: EEG `bids:Dataset` example | TODO: small new diagram |
| **F11** | preprocessing pipeline | TODO: from §2.10 spec |
| **F-M1** | Modeler architecture diagram | TODO |
| **L1** | LinkML schema excerpt | exists needs update |
| **L2** | XML serialization example | exists needs update |
| **L3** | EBNF grammar | exists needs update |
| **Table 2** | Reporting-guideline coverage matrix | CONSORT/SPIRIT marked Yes; 9 others are TODO |

---

## Open decisions

- **Empirical commitment for §2.6** - bot-mode via `demo1.studyflow` pending execution.
- **Empirical commitment for §2.7** - which RT dataset?
- **Ethics statement** - needed if §2.6/§2.7 uses human-subject data; bot-mode path avoids this.
- **Schema version** - `schemas/studyflow/README.md` v25.0414 lags `schema.linkml.yaml` header v25.1217.dev. Fix this.
- **`%!VERIFY` entries in `references.bib`** — 11 well-known references tagged for Zotero double-check (BIDS, OSC 2015, FAIR, CSVW, Nextflow, CWL, STROBE, STARD, SPIRIT 2013, Kinsman 2021, Teytelman 2016).

---

## Resources

| What | Where |
|---|---|
| The full draft prose | [`paper.md`](paper.md) |
| §2.6 task and protocol | [`nback_demo.md`](nback_demo.md) |
| Old draft | [`../archived/`](../archived/) |
| The modeler app | [`../../studyflow-modeler/`](studyflow-modeler/) |
| Modeler docs | [`studyflow-modeler/docs/`](../../studyflow-modeler/docs/) |
| Schemas | [`studyflow-modeler/src/assets/schemas/`](../../studyflow-modeler/src/assets/schemas/) |
| Example diagrams | [`studyflow-modeler/src/assets/examples/`](../../studyflow-modeler/src/assets/examples/) |
