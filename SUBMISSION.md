# Submission plan: eLife, Tools and Resources

Target: submit on **Fri 2026-10-16**. The date is fixed; the scope is not.

## Decisions (2026-09-26)

- Venue: eLife only, as Tools and Resources. JOSS is dropped.
- The paper pins one release of the toolkit. The modeler's `main` keeps moving and never enters the paper.
- The demo run is sealed (protocol digest), deposited, then run once.
- Run scope: 8 subjects per model (4 per arm, so both questions are testable) and 2 or 3 models that already run at the pinned tag. More tasks: parked.
- Models: one sealed file per model, identical except for the actor's `implementation`. The figures keep their structure, and that one-line diff demonstrates R7.
- The manuscript lives in both the Google Doc and `elife/paper-v3.qmd`; they sync only at the three checkpoints below.

## Freeze contract

1. **Pin.** Figures render only from a modeler worktree at the pinned tag. The Unity WebGL build and the model tags are pinned too.
2. **Seal, then run once.** After the seal, a protocol change costs a new run plus a line in the deviation report.
3. **Parking lot.** New ideas go to `POST_SUBMISSION.md`, not into the paper.
4. **Cut-offs.** Figure styling ends Fri Oct 2. New references end Fri Oct 9. Final Doc/qmd sync on Tue Oct 13.
5. **Oct 16 is a date, not a quality bar.** Whatever is unfinished gets cut, moved to the supplement, or listed under Limitations.

## Week 1: pin, seal, run (Mon Sep 28 to Fri Oct 2)

- [ ] Pick the tag: cut it on Monday from main with `npm run release` in the modeler (it bumps `package.json`, commits, tags; the date rule gives `v26.9.29`, or pass `26.10.1`). Never hand-tag: the CLI's `--version` and every run's `with: studyflow-cli/…` come from `package.json`. `v26.9.28` (2026-09-18) predates `studyflow validate` (37732e44, 2026-09-21), which no tag contains. Main `b098fe8d` audited 2026-09-27: 381 unit tests pass, typecheck and lint pass, no TODO in packages/skills/docs; the CLI output is byte-identical to the last pre-refactor commit for this study.
- [ ] Worktree at the tag: `~/workspace/behaverse/studyflow-modeler-paper` exists, built, detached at main `b098fe8d` (2026-09-27) as a provisional pin; once the tag exists, `git -C ~/workspace/behaverse/studyflow-modeler-paper checkout <tag> && npm ci && npm run build`. `render.sh` runs from it with `MODELER=~/workspace/behaverse/studyflow-modeler-paper` (fig-step1-design and fig-step4-report already re-rendered from it)
- [x] Record the Unity WebGL build and the model tags in the study file: `implementation: behaverse://assessment-unity@26.08` on both tasks (the build's own `productVersion`; no schema field exists for it, no runner reads it, the seal covers it; file hashes in `elife/study/README.md`), the model as `ollama://<tag>` (the only actor field; digests are recorded per exchange in the run repository). The build's git describe (`v26.08-39dada445-24-gc46a67742`) describes the checkout, not the build: its files predate those commits.
- [x] Set 8 subjects per model (`participantMultiplicity`)
- [x] Make one copy of the study file per model: `elife/study/example_study-gemma4-12b.studyflow.yaml` (`ollama://gemma4:12b-it-qat`, the only other model pulled; `diff` shows one line). A `random` third arm is not a one-line swap (the tasks answer the pool's message flows, which only the model runner plays); a third model means pulling one first.
- [ ] `studyflow validate` each sealed file and note its protocol digest (`studyflow info` prints it in full). At 2026-09-27, before the tag: e2b `sha256:e48fcd6d…`, 12b `sha256:64050026…`. Re-check after the tag is cut, since the digest drops schema defaults.
- [ ] Deposit the sealed files on OSF or Zenodo (timestamped)
- [ ] Run once per model, then `studyflow validate` each executed copy. Keep the run the figures show in `elife/study/run/` (render.sh reads it there) and the others in `elife/study/run-<model>/`
- [ ] Fill `tbl-agents`, `tbl-analyses`, `lst-diff`, and the Results paragraph at the end of Step 3
- [x] Add a Model column to `tbl-agents`, and one sentence in Step 2 saying the sealed files differ in one line
- [ ] Copy the `state:` block of the run in `elife/study/run/` into the `fig-consort` and `fig-overview` sources, then re-render every figure from the worktree. The pinned modeler's SVG export adds margin to seven figures (fig-key 24 units wider, the fig-overview strip 21, fig-step3-analyze 18): check the column edges in `fig-overview.py` (`BOUNDS`) after the render; `fig-elements` changes one glyph (EEG store). `fig-s2-modeler` is already re-rendered (Timeline `XCIT_NB_01`).
- [ ] **Checkpoint 1 (Fri Oct 2):** sync the Doc and the qmd, update the qmd's `Mirrors the Google Doc` line, and clear the Doc-only TODOs (equivalence margin, thresholds, fig-overview redraw) against the qmd

## Week 2: text (Mon Oct 5 to Fri Oct 9)

- [ ] Pedro's 10 open comments in the Doc (Jul 29)
- [x] Discussion: the "say why this matters" TODO
- [ ] Reproducibility: the allocation concealment TODO
- [x] `tbl-compare`: fill the three empty rows, or move it to Supplementary Note 2
- [ ] `tbl-analyses`: merge it into the text, or keep it
- [x] `fig-consort` TODO: cut it, or add one sentence on per-branch counts
- [x] Refresh the supplement (audited statement by statement against `b098fe8d` on 2026-09-27 and corrected: Appendix 1 describes the modeler, browser runner and local runtime as they are; Table S1 built from the schemas (34 rows, `tbl-elements-catalog`); the grammar listing rewritten to the schema's names; `tbl-claims` and `tbl-faults` re-checked, one claim marked pending the re-run; the jsPsych listing now validates; `fig-s3-runner` cut, since its PNG showed no runner screen. Left: the "outdated" note itself is gone only when you have read the new text once.)
- [ ] Framing for Tools and Resources: the problem and the formal object first, the demo as a demo
- [ ] Time-box (2 days max): encode one published lab study and report what its methods section left unspecified. If it is not done by Fri Oct 9, move it to `POST_SUBMISSION.md`
- [ ] **Checkpoint 2 (Fri Oct 9):** sync, then send to Pedro and Hoorieh for sign-off

## Week 3: ship (Mon Oct 12 to Fri Oct 16)

- [ ] Zenodo: enable the GitHub integration for `studyflow-modeler` and `schemas`, publish GitHub releases at the pinned tags, and add the DOIs to Data availability
- [ ] Author contributions: CRediT roles
- [ ] `quarto render elife`, then read the PDF once, start to end
- [ ] **Checkpoint 3 (Tue Oct 13):** final sync; after it, both copies freeze
- [ ] Post the preprint (eLife reviews preprints)
- [x] Cover letter: problem, formal object, demo, fault calibration (10 of 12 seeded faults caught)
- [ ] **Submit (Fri Oct 16)**

## Done means

- `grep -n TODO elife/paper-v3.qmd` prints nothing: every TODO is done, cut, or moved to `POST_SUBMISSION.md`
- Every figure was rendered from the pinned tag, and every executed study validates
- Pedro and Hoorieh have signed off
- Submitted

## Status 2026-09-27 (session notes)

Done today, all uncommitted in `elife/`:

- Eight subjects per model: study file (`participantMultiplicity` 8, doc strings), `fig-consort`, `fig-step1-design`, `fig-step4-report`, `fig-key` sources, both READMEs, and the paper's Step 2, Methods, `tbl-agents` (4 per arm) and the fig-overview caption. Study file re-spelled with the pinned CLI's `studyflow convert`; validates; protocol digest `sha256:54e5f9a1…` before the build and model pins are added.
- Text: the Discussion "why this matters" sentence; the fig-consort per-branch-counts sentence; `tbl-compare` filled (three rows, a rubric paragraph) and moved under Appendix 2, one sentence left in the main text.
- eLife structure (from the eLife-guide audit): Materials and methods, Data availability, Author contributions and Competing interests are main sections again (they sat under "Supplementary materials"); new Ethics section (no human participants); Funding and Acknowledgements added as TODOs; an "Availability and use" subsection in Methods (install, the three CLI commands, hardware); Supplementary Notes renamed Appendix 1 and 2; supplementary figures no longer carry a hard-coded "Figure S1" that printed as "Figure 11. Figure S1."; license wording corrected (modeler MIT, schema CC BY 4.0).
- `elife/cover-letter.md` drafted (439 words), with reviewer slots and a CRediT proposal to confirm.
- Bibliography: zero BibTeX errors (was 24); about 60 entries corrected from Crossref or arXiv, several of which carried another paper's metadata. The 40 remaining "empty author and editor" warnings come from the eLife style file's handling of `@misc`.
- Pins: the study file carries the WebGL build (`behaverse://assessment-unity@26.08`) and the sealed second-model copy exists; `fig-s2-modeler` re-rendered from the pinned build; the Doc drift measured and `elife/doc-sync.py` written (see the Google Doc decision below).
- Quarto build checked: PDF renders, every cross-reference and citation resolves; BibTeX had 24 errors from incomplete entries (cleanup in progress).

eLife requirements not yet met (source: the eLife-RP author instructions, reviewer.elifesciences.org/author-guide redirects there):

- Abstract 150–200 words (now 235); title up to 120 characters (now 121); a proposal for both is below.
- Funding, Acknowledgements, CRediT roles, AI-use statement: author input.
- Data availability needs persistent identifiers (Zenodo DOIs, the deposit of the sealed files and the runs) and must say how a reader obtains the Behaverse WebGL build: `behaverse/assessment-unity` is private and has no license, so the example study is not re-runnable by a reader as things stand. Decision needed: deposit the WebGL build (Zenodo) or make a release public.
- Preprint: bioRxiv's scope excludes work not premised on biology; the guide accepts any versioned preprint server, so PsyArXiv (versioned DOIs) around Oct 13, posted by us.
- Figure files at upload: TIFF/PDF/EPS at 300 dpi, one file per figure, no subcaptions (three figures use panels); the PNGs' embedded studyflow is lost in conversion, so attach each figure's `.studyflow.yaml` as source data.
- MDAR checklist to fill at submission; fee USD 3,750 at the point of commitment to review.
- Main text is about 8,200 words (Introduction to Future work, legends excluded); the guide suggests 5,000. Limitations and Future work could fold into the Discussion.

Decisions needed from you:

- Third model: the second (`gemma4:12b-it-qat`) is sealed; a third needs another open model pulled (a different family would make the one-line-diff point stronger). Timing: the old 4-subject run took 3.5 min with shorter timelines; 8 subjects on the full timelines, twice, plus a 12B model, will take a good part of a day. Ollama sends no sampling parameters, so the file cannot set temperature or seed.
- The WebGL build's availability (above).
- Whether `tbl-compare` stays in Appendix 2 (as done) or returns to the main text (eLife asks Tools and Resources papers for a comparison with existing methods; the Discussion's prose comparison remains in the main text either way).
- Google Doc sync method (see the drift measurement).

Proposed, not applied:

- Title (116 characters): "Studyflow, an executable visual notation for experimental workflows in cognitive science, from design to publication".
- Abstract (200 words):

  > A cognitive science study is spread across several artifacts (protocol, experiment script, data, analysis pipeline, reports, figures), and no single one of them fully records what was done. Data have standards such as BIDS; the process that produced them still lives in scattered text, slides, and custom code, so reproducing a study means reconstructing that process from all of those artifacts at once. We present Studyflow, a visual notation that gives the experimental process one representation that is machine-readable, human-understandable, and executable. One diagram serves as the protocol, the runnable study, the analysis specification, and the publication figure, each a view for a different audience, so there is no second copy to drift. Studyflow formulates a study as a typed directed graph, realized as a BPMN 2.0 extension with the elements experimental research needs. We demonstrate it on an example study whose single file enrolls, screens, administers, and analyzes a cohort of artificial agents, each analysis question ending in a registered claim state; a human cohort would take the same protocol through the same interface. A validator caught ten of twelve faults seeded into a study. The schema and an open-source modeler, validator, and runner are released under permissive licenses.
