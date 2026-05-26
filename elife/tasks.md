# eLife Paper — Remaining Work

The full draft is in [`paper.md`](./paper.md). This file lists what is still left to do, with effort estimates and owners.

**Tag legend:** `[D]` decision · `[E]` empirical · `[F]` figure/asset · `[V]` verification · `[X]` cross-repo · `[S]` submission

---

## Critical path (3 items gate submission)

1. **[E] §2.6 N-back round-trip** — the empirical anchor of the paper. See [`nback_demo.md`](./nback_demo.md). Bot-mode path is the cheapest (≈ 1 day, no IRB needed). Drives Figure 4 and resolves §2.6's two `[GAP]` markers.
2. **[E] §2.7 RT pipeline demo** — pick one Pedro-group RT dataset; encode preprocessing + analysis; show outputs match a published analysis. Drives Figure 8.
3. **[F] Figures still to author** — F1 schematic, F3 modeler composite, F4 runner composite, F5 Checklist screenshot, F8 RT pipeline, F9 SPIRIT renders, F10 EEG/BIDS exemplar, F11 OmniProcess subgraph, F-M1 modeler architecture.

Everything else is parallelizable around these.

---

## Phase A — Decisions still open

- [ ] **[D] Empirical depth for §2.6** — bot-mode pilot only (cheap, no IRB) vs. human-subject pilot (needs IRB-light). Recommended: bot-mode for first submission; human pilot for reviewer-response. Owner: Morteza. Effort: 15 min.
- [ ] **[D] §2.7 RT dataset** — which dataset from Pedro's group anchors §2.7. Owner: Pedro + Morteza. Effort: 30 min.
- [ ] **[D] Ethics statement scope** — only needed if §2.6/§2.7 uses human pilots; bot-mode path skips this. Owner: Pedro. Effort: 30 min.
- [ ] **[D] Author list** — same as JOSS (Ansarinia, Afkari Roshan, Cardoso-Leite)? Confirm before submission. Owner: Morteza. Effort: 10 min.

## Phase B — Empirical work

- [ ] **[E] §2.6 bot-mode round-trip** — author/select `.studyflow` (use `demo1.studyflow`), publish via modeler, run with `?seed=42`, capture runner-state screenshots, export trial CSV. Per [`nback_demo.md`](./nback_demo.md). Owner: Morteza + Hoorieh. Effort: 1 day.
- [ ] **[E] §2.7 RT pipeline demo** — encode preprocessing + analysis as Studyflow subprocess; reproduce a published analysis on the chosen dataset; supplementary `.studyflow` + summary figure. Owner: Pedro + Morteza. Effort: 2–3 days.
- [ ] **[E] CONSORT 25-item coverage table for §2.5** — inspect [`consort2025.studyflow`](../../studyflow-modeler/src/assets/examples/consort2025.studyflow) (423 lines) against the CONSORT 2025 checklist; classify each item as machine-checked / encoded-as-attribute / author-discipline. Owner: Hoorieh. Effort: half-day.
- [ ] **[E] (Optional)** Readability study — 5–10 cognitive scientists rate sample diagrams. Reviewer-friendly addition for revision; skip for v1. Effort: 1 week.

## Phase C — Figures to author

- [ ] **[F] F1** — "many artifacts, one study" schematic (4-panel: prose, box-arrow, code, ontology, each with failure mode). New design work. Effort: half-day.
- [ ] **[F] F3** — Modeler UI composite. 2×3 from existing screenshots (`3-drag`, `4-inspector`, `8-simulate`, `9-publish`); compose, annotate, label. Effort: 2 h.
- [ ] **[F] F4** — Runner walkthrough composite. 4–6 panels (consent → instruction → trial → questionnaire → end). Depends on §2.6 round-trip. Effort: half-day.
- [ ] **[F] F5** — Checklist-view screenshot. Timeline + Study views already exist; Checklist is the missing piece. Effort: 30 min once the Checklist view is available in the modeler build.
- [ ] **[F] F8** — RT analysis pipeline + dplyr side-by-side. Source already in [`docs/reference/data.qmd`](../../studyflow-modeler/docs/reference/data.qmd); render clean. Depends on §2.7. Effort: 2 h.
- [ ] **[F] F9** — SPIRIT 2025: three-panel (Study / Timeline / Checklist views from [`spirit2025.studyflow`](../../studyflow-modeler/src/assets/examples/spirit2025.studyflow) + reference image). Effort: half-day.
- [ ] **[F] F10** — Small EEG/BIDS exemplar diagram (`bids:Dataset` linked to `Record EEG` task). Effort: 2 h.
- [ ] **[F] F11** — OmniProcess subgraph (Ingest → Preprocess{fMRI,EEG} → Multiverse → Corpus). Author from §2.10 spec. Effort: 2 h.
- [ ] **[F] F-M1** — Modeler architecture block diagram (schemas → core library → modeler+runner → BDS). Effort: half-day.

## Phase D — Bib / cross-repo cleanups

- [ ] **[V] Verify 11 `%!VERIFY` bib entries** — Zotero pass to confirm volume/issue/pages for `osc2015`, `bids`, `fair`, `csvw`, `nextflow`, `cwl`, `strobe`, `stard`, `spirit2013`, `kinsman2021`, `teytelman2016`. Effort: 30 min.
- [ ] **[V] Verify scoping-review entry** — `visualmodelinglanguagesscopingreview` currently has `[Authors to verify]` placeholder; confirm authors and venue from PMC11607556. Effort: 15 min.
- [ ] **[X] Reconcile schemas-repo version** — `behaverse/schemas/studyflow/README.md` says v25.0414, lags the LinkML header v25.1217.dev. Cross-repo edit. Effort: 5 min (one-line README change + commit + tag).
- [ ] **[V] Pin example-diagram commits** — for §M.9, capture stable commit SHAs of `consort2025.studyflow`, `spirit2025.studyflow`, the §2.6 N-back source, and the §2.7 RT-pipeline source. Effort: 30 min.

## Phase E — Submission

- [ ] **[S] Add caption + label for every figure** — F1–F11 + F-M1. Effort: 1 h once figures land.
- [ ] **[S] Add caption for every listing** — L1–L3 already have inline lead-ins; tighten. Effort: 30 min.
- [ ] **[S] Add Supplementary Table S1** — full element catalog (referenced in §2.1). Compile from `partials/elements.qmd` + `M/ref/elements`. Effort: 2 h.
- [ ] **[S] AI usage disclosure** — eLife requires. Effort: 15 min.
- [ ] **[S] Author contributions (CRediT)** — Effort: 15 min.
- [ ] **[S] Conflict-of-interest declarations** — Effort: 15 min.
- [ ] **[S] Data and code availability statement** — link to repo URLs (already pinned in §M.9). Effort: 15 min.
- [ ] **[S] Ethics statement** — depends on Phase A decision. Effort: 15 min once decided.
- [ ] **[S] eLife T&R pre-submission checklist** — house-style review. Effort: 1 h.
- [ ] **[S] Word-count check** — current 11.7k; eLife T&R typical 8–12k. Trim if needed; §M.8 EBNF can move to supplementary. Effort: 30 min if trimming.

---

## Quick wins (each <1 h, unblock other work)

1. **[V]** Zotero pass on 11 `%!VERIFY` entries — 30 min.
2. **[X]** One-line schemas-repo README edit — 5 min.
3. **[D]** Bot-mode commitment for §2.6 — 15 min (then start Phase B).
4. **[S]** AI usage disclosure paragraph — 15 min.

---

## Done in earlier turns (for reference)

- §1–§3 + §M.1–§M.9 drafted (per-agent assembly + edits)
- Bib merge from `references.bib` + `joss_references.bib` → `elife/references.bib` (80 entries)
- 13 `[CITE: …]` placeholders resolved
- §2 intro paragraph added (§2.4 → §2.5 transition)
- §2.6 two-encoding clarification (trial-by-trial vs. block-level)
- §2.6 CogEnv paragraph added (cites `@ansarinia2022cogenv` + `@defossez2020bdm` + `@ansarinia2022cogtext`)
- §2.10 reframed as OmniProcess multimodal-preprocessing use case
- §3.2 DAG-limit paragraph added (cites `@ghareeb2025`)
- LinkML restored as canonical schema source (bio-literature framing)
- Version reconciliation in §M.9 (paper-side wording)
- `Q2-OLD`, `archived.md`, `7_grammar.qmd` moved to `archived/`
- Per-agent draft files in `elife/draft/` deleted (paper.md has diverged)
