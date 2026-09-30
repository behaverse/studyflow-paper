# Submission plan: eLife, Tools and Resources

Target: submit on **Fri 2026-10-16**. The date is fixed; the scope is not.

## Decisions (2026-09-26)

- Venue: eLife only, as Tools and Resources. JOSS is dropped.
- The paper pins one release of the toolkit. The modeler's `main` keeps moving and never enters the paper.
- The demo run is sealed (protocol digest), deposited, then run once. (Superseded 2026-09-30: no registry deposit before the runs; the files are sealed, their digests recorded in the repository, then run, and the paper states that order.)
- Run scope: 8 subjects per model (4 per arm, so both questions are testable) and 2 or 3 models that already run at the pinned tag. More tasks: parked. (Superseded 2026-09-30: the reported runs are the planted cohort of 8 simulated participants and its null twin; the three language-model twins are run too, by the author, results pending.)
- Models: one sealed file per model, identical except for the actor's `implementation`. The figures keep their structure, and that one-line diff demonstrates R7.
- The manuscript lives in both the Google Doc and `elife/paper-v3.qmd`; they sync only at the three checkpoints below.

## Freeze contract

1. **Pin.** Figures render only from a modeler worktree at the pinned tag. The Unity WebGL build and the model tags are pinned too. (2026-09-30: the pinned tag is the modeler release after the design-review follow-ups; the current study uses no WebGL build.)
2. **Seal, then run once.** After the seal, a protocol change costs a new run plus a line in the deviation report.
3. **Parking lot.** New ideas go to `POST_SUBMISSION.md`, not into the paper.
4. **Cut-offs.** Figure styling ends Fri Oct 2. New references end Fri Oct 9. Final Doc/qmd sync on Tue Oct 13.
5. **Oct 16 is a date, not a quality bar.** Whatever is unfinished gets cut, moved to the supplement, or listed under Limitations.

## Week 1: pin, seal, run (Mon Sep 28 to Fri Oct 2)

- [x] Pick the tag: `v26.9.29`, released 2026-09-28 with `npm run release` (GitHub release, Homebrew, https://behaverse.org/studyflow-modeler/). (Superseded 2026-09-30: `v26.9.29` has no `simulate` skill and cannot run the current study; the paper cites the release tagged after the design-review follow-ups, `[TODO: modeler release]` until then.)
- [x] Worktree at the tag: `~/workspace/behaverse/studyflow-modeler-paper` rebuilt at `v26.9.29` (CLI reports 26.9.29); `render.sh` runs from it with `MODELER=~/workspace/behaverse/studyflow-modeler-paper`. (2026-09-30: it stays at `v26.9.29` until the release is tagged, then moves to it.)
- [x] Record the Unity WebGL build and the model tags in the study file: `implementation: behaverse://assessment-unity@26.08` on both tasks (the build's own `productVersion`; no schema field exists for it, no runner reads it, the seal covers it; file hashes in `elife/study/README.md`), the model as `ollama://<tag>` (the only actor field; digests are recorded per exchange in the run repository). The build's git describe (`v26.08-39dada445-24-gc46a67742`) describes the checkout, not the build: its files predate those commits. (Superseded 2026-09-30: the current study has no Behaverse task and no WebGL build; its tasks are `simulate://simon` and `simulate://nback`. The model tags survive in the three language-model twins.)
- [x] Set 8 subjects per model (`participantMultiplicity`)
- [x] Make one copy of the study file per model: three sealed files in `elife/study/`, `example_study` (`ollama://gemma4:e2b-mlx`), `example_study-gemma4-12b` (`ollama://gemma4:12b-it-qat`) and `example_study-llama3.1-8b` (`ollama://llama3.1:8b`, Meta), each differing from the first in that one line; the pool is now named `Language model` so the name holds for all three. Llama 3.1 8B must be pulled before its run (`ollama pull llama3.1:8b`, about 4.9 GB). (Superseded 2026-09-30: `example_study` is now the planted file, `simulate://planted`, with a null twin, `example_study-null`, and three language-model twins, `example_study-gemma4-e2b`, `-gemma4-12b` and `-llama3.1-8b`, each one line apart from it; the pool is named `Actor`.)
- [x] `studyflow validate` each sealed file and note its protocol digest (`studyflow info` prints it in full). At `v26.9.29`, 2026-09-28 (after the branch counts on the gateway arrows): e2b `sha256:79f2500d…`, 12b `sha256:85cc79a4…`, llama `sha256:b956d503…`. Any later edit to a sealed file changes these; re-check before the deposit. (Superseded 2026-09-30: the five current digests are in `elife/study/README.md`; they change again when the files are re-spelled at the modeler release.)
- [ ] Deposit the sealed files on OSF or Zenodo (timestamped) (Superseded 2026-09-30: no registry deposit before the runs. The study files and runs still need a deposit DOI for Data availability; see "Needs the author".)
- [ ] Run once per model, then `studyflow validate` each executed copy. Keep the run the figures show in `elife/study/run/` (render.sh reads it there) and the others in `elife/study/run-<model>/` (2026-09-30: planted and null ran on 2026-09-29, into `run/` and `run-null/`, and both executed copies validate; both are re-run at the modeler release, and the author runs the three language-model twins.)
- [ ] Fill `tbl-agents`, `tbl-analyses`, `lst-diff`, and the Results paragraph at the end of Step 3 (2026-09-30: `tbl-planted`, `lst-diff` and the end of Step 3 now come from the planted and null runs; `tbl-agents` is the twins' table, `[TODO]` until their runs; there is no `tbl-analyses` any more.)
- [x] Add a Model column to `tbl-agents`, and one sentence in Step 2 saying the sealed files differ in one line
- [ ] Copy the `state:` block of the run in `elife/study/run/` into the `fig-consort` and `fig-overview` sources, then re-render every figure from the worktree. The pinned modeler's SVG export adds margin to seven figures (fig-key 24 units wider, the fig-overview strip 21, fig-step3-analyze 18): check the column edges in `fig-overview.py` (`BOUNDS`) after the render; `fig-elements` changes one glyph (EEG store). `fig-s2-modeler` is already re-rendered (Timeline `XCIT_NB_01`). (2026-09-30: moved to "At the modeler release"; seven figure sources must first be rebuilt from the current study, and `fig-s2-modeler`, which shows the previous protocol's Step 2, must be re-shot.)
- [ ] **Checkpoint 1 (Fri Oct 2):** sync the Doc and the qmd, update the qmd's `Mirrors the Google Doc` line, and clear the Doc-only TODOs (equivalence margin, thresholds, fig-overview redraw) against the qmd (2026-09-30: the qmd no longer has that line, removed in `e24e0fb`, and the current study has no equivalence question.)

## Week 2: text (Mon Oct 5 to Fri Oct 9)

- [ ] Pedro's 10 open comments in the Doc (Jul 29)
- [x] Discussion: the "say why this matters" TODO
- [x] Reproducibility: the allocation concealment TODO (Done 2026-09-30 in the merge: Reproducibility says the example study has no human participants, and that a seed deposited with the file makes a human cohort's allocation foreseeable unless it is withheld until enrollment closes.)
- [x] `tbl-compare`: fill the three empty rows, or move it to Supplementary Note 2 (Superseded 2026-09-30: `tbl-compare` is dropped; the Discussion's prose comparison and Appendix 2 stay.)
- [ ] `tbl-analyses`: merge it into the text, or keep it (Superseded 2026-09-30: the merged paper has no `tbl-analyses`.)
- [x] `fig-consort` TODO: cut it, or add one sentence on per-branch counts
- [x] Refresh the supplement (audited statement by statement against `b098fe8d` on 2026-09-27 and corrected: Appendix 1 describes the modeler, browser runner and local runtime as they are; Table S1 built from the schemas (34 rows, `tbl-elements-catalog`); the grammar listing rewritten to the schema's names; `tbl-claims` and `tbl-faults` re-checked, one claim marked pending the re-run; the jsPsych listing now validates; `fig-s3-runner` cut, since its PNG showed no runner screen. Left: the "outdated" note itself is gone only when you have read the new text once.)
- [ ] Framing for Tools and Resources: the problem and the formal object first, the demo as a demo (2026-09-30: the merged paper frames the example as a verification against a planted truth rather than a demo.)
- [x] Time-box (2 days max): encode one published lab study and report what its methods section left unspecified. If it is not done by Fri Oct 9, move it to `POST_SUBMISSION.md` (Done: two, Hedge et al. 2018 and Kucina et al. 2023, encoded from their Methods sections; Results Step 5, `tbl-encoded`, `elife/study/encoded/`.)
- [ ] **Checkpoint 2 (Fri Oct 9):** sync, then send to Pedro and Hoorieh for sign-off

## Week 3: ship (Mon Oct 12 to Fri Oct 16)

- [ ] Zenodo: enable the GitHub integration for `studyflow-modeler` and `schemas`, publish GitHub releases at the pinned tags, and add the DOIs to Data availability (2026-09-30: the modeler's tag is the release after the design-review follow-ups. Data availability also needs a deposit DOI for `elife/study/`: the paper repository is private, and `run/` and `run-null/` are untracked.)
- [ ] Author contributions: CRediT roles
- [ ] `quarto render elife`, then read the PDF once, start to end
- [ ] **Checkpoint 3 (Tue Oct 13):** final sync; after it, both copies freeze
- [ ] Post the preprint (eLife reviews preprints)
- [x] Cover letter: problem, formal object, demo, fault calibration (10 of 12 seeded faults caught) (Updated 2026-09-30: 10 of 12 is the authors' own fault library; the letter now reports the blind calibration, 1 of 12 by the validator and 12 of 12 by the digest, beside the planted and null runs, the two encoded studies, and that a human cohort is not shown.)
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

- Abstract 150–200 words (now 235); a proposal is below. Title done (110 characters).
- Funding, Acknowledgements, CRediT roles, AI-use statement: author input.
- Data availability needs persistent identifiers (Zenodo DOIs, the deposit of the sealed files and the runs) and the URL of the WebGL build binary on the Studyflow website.
- Preprint: bioRxiv's scope excludes work not premised on biology; the guide accepts any versioned preprint server, so PsyArXiv (versioned DOIs) around Oct 13, posted by us.
- Figure files at upload: TIFF/PDF/EPS at 300 dpi, one file per figure, no subcaptions (three figures use panels); the PNGs' embedded studyflow is lost in conversion, so attach each figure's `.studyflow.yaml` as source data.
- MDAR checklist to fill at submission; fee USD 3,750 at the point of commitment to review.
- Main text is about 8,200 words (Introduction to Future work, legends excluded); the guide suggests 5,000. Limitations and Future work could fold into the Discussion.

Decisions needed from you:

- Third model: decided 2026-09-28, Meta's `llama3.1:8b` (the largest Llama that fits this laptop; Llama 4 is 16x17B upward). Sealed; pulled 2026-09-28 (`ollama list` id 46e0c10c039e, 4.9 GB). Timing: the old 4-subject run took 3.5 min with shorter timelines; 8 subjects on the full timelines, twice, plus a 12B model, will take a good part of a day. Ollama sends no sampling parameters, so the file cannot set temperature or seed.
- WebGL build: decided 2026-09-28, distributed as a binary from the Studyflow website, runnable by anyone without a license, Behaverse tasks only; the paper says so, with a TODO for the URL.
- Whether `tbl-compare` stays in Appendix 2 (as done) or returns to the main text (eLife asks Tools and Resources papers for a comparison with existing methods; the Discussion's prose comparison remains in the main text either way).
- Google Doc sync method (see the drift measurement).

Proposed, not applied:

- Title: decided 2026-09-28 in the Doc and applied to the qmd and the cover letter: "Studyflow, a visual notation for coordinating experiments in the cognitive sciences, from design to publication" (111 characters).
- Abstract (200 words):

  > A cognitive science study is spread across several artifacts (protocol, experiment script, data, analysis pipeline, reports, figures), and no single one of them fully records what was done. Data have standards such as BIDS; the process that produced them still lives in scattered text, slides, and custom code, so reproducing a study means reconstructing that process from all of those artifacts at once. We present Studyflow, a visual notation that gives the experimental process one representation that is machine-readable, human-understandable, and executable. One diagram serves as the protocol, the runnable study, the analysis specification, and the publication figure, each a view for a different audience, so there is no second copy to drift. Studyflow formulates a study as a typed directed graph, realized as a BPMN 2.0 extension with the elements experimental research needs. We demonstrate it on an example study whose single file enrolls, screens, administers, and analyzes a cohort of artificial agents, each analysis question ending in a registered claim state; a human cohort would take the same protocol through the same interface. A validator caught ten of twelve faults seeded into a study. The schema and an open-source modeler, validator, and runner are released under permissive licenses.

## Status 2026-09-30

Decisions made today:

- `elife/paper-v3.qmd` is the manuscript again. The gains of the rewrite `elife/paper-v4.qmd` (2026-09-29, `012c763`) are merged into it in place, and `elife/_quarto.yml` points at v3 again. Main text is about 6,650 words (Introduction to the end of the Discussion; abstract 199), with Limitations and Future work folded into the Discussion.
- The example study is the planted-effect cohort of eight simulated participants (`simulate://planted`) and its null twin (`simulate://null`), both run on 2026-09-29 (`elife/study/run/`, `run-null/`). The three language-model twins are run too, by the author; until then `tbl-agents` has `[TODO]` cells, and Results Step 3 and Methods each have a `[TODO: language-model twin runs]` sentence.
- No registry deposit before the runs. The paper states the actual order: the files were sealed, their digests recorded in the repository, and then run (Methods, "The example study").
- The modeler version is no longer `v26.9.29` or `bfbea295`. The paper carries `[TODO: modeler release]` until the design-review follow-ups in `studyflow-modeler` are finished (behaverse/software-design issue 70; a separate session is moving the two runtimes onto one engine), then cites the release tagged after them. What happens at that release is listed under "At the modeler release".
- `tbl-compare` is dropped, as the design review asks (a table where the tool scores itself reads as advocacy); the Discussion's prose comparison and Appendix 2 stay.
- "A human cohort would take the same protocol through the same interface" is retracted to a design goal the paper does not demonstrate (Limitations; R7 in `tbl-requirements`).

Done today, all uncommitted:

- Merge of v4 into v3: v4's abstract and impact statement; the planted and null results (`tbl-planted`, `lst-diff`), the classifier fault the planted run exposed, Step 5 on the two encoded studies (`tbl-encoded`), the blind calibration (`tbl-blind`), "connected" for "sound", the two runtimes stated as not equivalent, FEEL expressions; `tbl-agents` became the twins' table; `[@REF]` became `[@claesen2021adherence; @hair2019iicarus]`; the allocation-concealment TODO closed in Reproducibility.
- `elife/_quarto.yml` back on `paper-v3.qmd`.
- Bibliography: 57 entries corrected (versions of record, article numbers, duplicate DOI URLs) and `morris2019simulation` added (237 entries). DOI links fixed in the extension's `elife/_extensions/elife/vancouver-elife.bst` (`https://doi.org/` prefix; all 172 DOI links in the v4 PDF were broken); the copy in `elife/` is overwritten at every render.
- Cover letter (473 words) and glossary (`elife/UBIQUITOUS_LANGUAGE.md`) updated to the merged paper; so are `elife/study/README.md`, the root `README.md` and `POST_SUBMISSION.md`.

From today's audits:

- The authors' own fault library catches 10 of 12 seeded faults; of 12 faults seeded blind (`elife/study/blind-faults/`), `studyflow validate` errors on 1 and the protocol digest differs on all 12. Nothing on disk records how the blind seeding was done.
- The two published studies encoded from their Methods sections leave about ten run-critical parameters unstated each (10 and 9).
- Licences: tools MIT, schema CC BY 4.0.
- 8 of the 15 figure files still show the previous protocol, and none was rendered from the current study; seven figure sources must be rebuilt from it.
- Nothing on disk records the planted run with the unstandardized classifier that the paper reports; the fault reproduces on the planted data (0 of 8 correct under leave-one-out).
- The runs of 2026-09-29 were made from an uncommitted modeler working tree; `bfbea295`, committed minutes later (unpushed, untagged), reproduces their digests, trials and results. The run record names only `studyflow-cli/26.9.29`.
- The paper repository is private, and `run/` and `run-null/` are untracked, so Data availability needs the deposit DOI.
- The Google Doc still mirrors v3 as of 2026-09-21, and the merge rewrote most of the main text, so Checkpoint 1 is close to a full re-sync (answer or archive Pedro's threads first).
- eLife's clause accepting any versioned preprint server is written for Review Articles; confirm with eLife before posting to PsyArXiv.

## At the modeler release

When the design-review follow-ups are finished and a release is tagged after them, in this order:

- [ ] Tag the release; replace `[TODO: modeler release]` in `paper-v3.qmd` (Methods "The example study", `tbl-claims` caption, "Availability and use") and fill the DOIs in Data availability.
- [ ] Before re-sealing: remove "30 trials" from the Simon task's note so `trials: 30` is the only place the number appears; decide whether the boundary events' conditions keep their braces (the paper quotes `{Simon_Record.failedTrialRate} > 0.2`); check the Hedge encoding's `trials per block` (240 × 3 over five blocks implies 144).
  - [ ] Also reword the sealed file's notes that still describe the previous protocol, since they print in the Study and Checklist views: the screening checklist's "Executor configuration pinned (model id, sampling parameters)", the eligibility criterion's "pinned model tag", the filter checklist's "response window" and "tutorial and practice blocks", and the 1-back note's "about a third repeating" (12 of the 56 digits repeat).
- [ ] Re-spell the study files with the release's `studyflow convert`, re-seal them, and COMMIT them before re-running, so that the Methods' statement of the order (sealed, digests recorded in the repository, then run) is true; update the digests in `elife/study/README.md`; then put the commit and dates in the Methods placeholder.
- [ ] Re-run planted and null and check `tbl-planted`; run the three language-model twins (author) and fill `tbl-agents`, the twins sentence in Results Step 3 and the twins sentence in Methods.
- [ ] Keep a planted run with the unstandardized classifier as a file and a run: the paper reports that fault and nothing on disk records it.
- [ ] Regenerate every listing (`lst-minimal-study`, `lst-step1-design`, `lst-step2-run`, `lst-swap`, `lst-step3-analyze`, `lst-diff`, `lst-grammar`), the seeded-error printout in "Validation and its calibration", the test paths in `tbl-claims`, and the outcomes in `tbl-faults` and `tbl-blind` (re-run `validate` on the fault library and on the twelve blind faults).
- [ ] Rewrite for one engine: the Limitations paragraph "The two runtimes are not equivalent", the last sentence of the Notation's Execution subsection, the Methods paragraph on the local runtime (`skills/local/run.py`), Appendix 1, the runtime rows of `tbl-claims`, and the R7 row of `tbl-requirements` if a second actor kind can then be shown.
- [ ] Figures: rebuild the seven stale sources from the current study (`fig-step1-design`, `fig-step2-run`, `fig-step2-nback`, `fig-step3-analyze`, `fig-step3-decision`, `fig-consort`, `fig-overview`), re-render every figure from `studyflow-modeler-paper` at the tag, re-shoot `fig-s2-modeler`, and read each caption against its new image.

## Needs the author

- [ ] Funding: funders, grant numbers, the authors on each grant, and whether the funders had a role in the work.
- [ ] Acknowledgements, or a statement that there are none.
- [ ] CRediT roles: each author confirms or corrects the proposal at the end of `elife/cover-letter.md`.
- [ ] The AI-use statement (eLife policy; the TODO at the end of Methods, after "Availability and use").
- [ ] Zenodo DOIs of the modeler and schemas releases, and the deposit DOI of `elife/study/` (sealed files, executed copies and run repositories, encoded studies, blind faults).
- [ ] Suggested reviewers and editors: the four slots in `elife/cover-letter.md`.
- [ ] Confirm `[@REF]` → `[@claesen2021adherence; @hair2019iicarus]` (Introduction, "even when standard research practices are endorsed").
- [ ] How the blind seeding was done: which agent, and what it was given (the TODO in Methods, "Validation and its calibration").
- [ ] Four bibliography questions from today's check:
  - PsyNet (`harrison2026psynet`) now cites Harrison et al. 2020, "Gibbs Sampling with People" (NeurIPS), the paper PsyNet's developers ask users to cite: keep it, or cite the software?
  - `aguilar2022experiments`: keep the 2022 arXiv preprint, or cite its version of record (Sci Rep 2024, retitled "Experiments as Code and its application to VR studies in human-building interaction")?
  - Versions of record replaced several cited preprints, so some printed years no longer match their keys (e.g. `beal2022labop` prints 2023) and two author lists changed (`mialon2024gaia`, `bean2025construct`): revert any preprint cited on purpose (the old entries are in `git show 012c763:elife/references.bib`)?
  - `dmnspec` cites DMN 1.3 (2021): which DMN/FEEL version do the runtimes follow?
- [ ] Read the supplement once and remove its "outdated" NOTE (top of "Supplementary materials").
- [ ] Pedro's open comments in the Doc.
- [ ] Co-authors' sign-off: Pedro and Hoorieh.
