# Waves 1 and 2: change list (2026-10-02)

This file lists the changes made to answer the objections in `adoption-objections-plan.md`. Each entry gives the old text, the new text, the reason, and the evidence. Nothing here is committed.

## Wave 1 (paper only)

### Stage P1: corrections

| Where | Old | New | Reason |
|:--|:--|:--|:--|
| Introduction, L59 | "…rather than by any tool or vendor, so a Studyflow file outlives the software that wrote it." | "…so any BPMN tool can read and draw a Studyflow file without the software that wrote it, while running it follows the Studyflow specification (Materials and methods)." | Overclaim (objection 5): a generic BPMN engine does not run Studyflow's semantics (`tbl-departures`). |
| Limitations, single source of truth | "A project that no longer uses our toolkits is left with a valid, standard file that no single tool owns." | Adds: "…and any BPMN tool can draw. Running it again, however, needs a runtime that follows the Studyflow specification, since a generic BPMN engine does not read the extensions and few engines run BPMN's own execution semantics [@geiger2016bpmn]. What has to outlive our implementation is therefore the specification, and at present one group maintains both." | Same overclaim, plus the single-lab concern stated plainly. M13 (wave 3) answers it with a published specification and a conformance suite. |
| Methods, pipeline check | "The five study files were then sealed again." | "Both fixes changed the protocol, so each of the five study files carries a new fingerprint." | "Sealed" is retired (no sealing or deposit). |

The `tbl-copies` caption ("The labels drawn on the diagram repeat some of these values as text…") waits for M1 and S2. Once the labels read the value, the caption changes.

### Stage P2: new Discussion subsection "What a researcher gains, and what it costs"

- **Where:** after "One artifact instead of a document trail", before "Where Studyflow sits among workflow tools". About 260 words.
- **Gains:**
  - Design checks before recruitment (`tbl-faults`).
  - The registered analysis run on simulated participants before enrolment. The pipeline check found two real faults (an unstandardized classifier, and a crash when a participant was discontinued), as the Methods describe.
  - Participant flow and schedule come as views.
- **Costs:**
  - A notation and a modeler to learn.
  - More than a thousand lines for a two-task pilot.
  - Trial-level content stays in the task software unless written into the file (`tbl-scope`).
  - The balance is unmeasured (Limitations).
- **Reason:** objection 4. The day-one gains were implicit; the costs were not stated.
- **Citations:** only existing keys (`wilson2019tensimple`, plus cross-references).

### Stage P3: Methods, "Expressiveness and limits": scope paragraph and `tbl-scope`

- **Where:** before "The walk is a profile of BPMN 2.0's execution semantics".
- **Content:** one paragraph saying that the notation coordinates, and that a trial's order and timing are registered only when written into the settings wired to the task. Then `tbl-scope`: eleven designs, with how the file states each and whether the local and browser runtimes run it.
- **Reasons:** objections 2 and 7. The paper did not say which designs run where.
- **Evidence (modeler main, 2aff980c):**
  - `engine/allocation.ts` applies only simple and block allocation, and warns "unapplied" for the rest.
  - A browser session refuses a concealed allocation.
  - Timers are a wait in the walk; in the browser, `setTimeout` on an open page.
  - The browser runtime keeps data in its session, offers an `events.jsonl` download, and uploads to the Behaverse data server only when recording is switched on.
  - `python://` has a local runner only.
  - The eeg skill is vocabulary only ("Nothing executes these elements yet").
- **Will change after wave 2:**
  - the allocation row, from M5;
  - the trial row, from M4 (registered trial lists);
  - the row on recording data, in wave 3 (M9).

### Stage L: backup Limitations paragraph (Option B of `limitations-backup.md`)

- **Where:** a new paragraph in Limitations, after "A human cohort taking the same file…". About 190 words. It is written as prose, not the list of the backup file.
- **Reason:** objections 1, 2, 3, 5, 6 and 7, stated as limitations and future work in case wave 2 does not land. The evidence is the "Facts behind the text" table of `limitations-backup.md` (modeler main, 2aff980c).
- **Sentences to revise if wave 2 lands:**
  - "twelve calls": M2 shortens the analysis.
  - "The labels drawn on the diagram repeat some values as text that nothing checks": M1.
  - "Stratified allocation, minimization": M5.
  - "A run's version-controlled history holds every exchange": M7.
  - The trial-order sentence: D3 and M4.

## Wave 2 (modeler, study files, paper sync)

### Modeler (studyflow-modeler, integration branch `feat/wave2` at cf548588, from main 2aff980c; nothing merged into main, nothing pushed)

| Item | Branch | What it does | Tests |
|:--|:--|:--|:--|
| M1 | `feat/wave2-labels` | A `{name}` placeholder in a label reads the value the file declares before any run (a property's value, or a key of the Parameters wired into a sub-process). `{name:%}` draws a fraction as a percentage. `validate` warns when a label copies, as a number, a value its element's conditions read | `core/state-document`, `core/labels` |
| M2 | `feat/wave2-short-analyses` | The data contract checks a test's `dv`, `within`, `between` and `subject` columns. A python example decides one question by *p* and one by a Bayes factor (`pingouin.pairwise_tests`, `pingouin.bayesfactor_ttest`) | `core/data-contract`, `skills/python/test_local.py`, shipped-example loops |
| M4 | `feat/wave2-registered-materials` | A data element's `digest` and a start event's `consentFormDigest` register a material by its content. The digest enters the protocol fingerprint; `validate` checks the content and `run` refuses a changed material. A shipped example plays a registered trial list (CSV + CSVW) one trial at a time | `core/materials`, `core/protocol-digest`, `modeler/cli-checks`, `python/test_local` |
| M5 | `feat/wave2-allocation` | Alternation, stratified permuted blocks and Pocock–Simon minimization (range method, p = 0.8) run in the walk. A browser session refuses strata and minimization; the "unapplied" warning is gone. A counterbalanced-order example | `core/engine` (draws fixture extended) |
| M7 | `feat/wave2-private-runs` | `--author` names a run's author; without it, no one is named (no OS username). `--data-outside-history` commits only the executed study and the digests of the other files | `runtime-local/cli-run`, `runtime-local/run-repo` |
| M12 | `feat/wave2-lighter-files` | A sub-process drawn closed with undrawn contents gets them drafted when the study opens. Expanding frames only what it shows. Style lines: none were defaults, so nothing saved | `canvas/layout`, `canvas/canvas` |

- **Gate on `feat/wave2`:** typecheck, lint, and 501 unit tests pass. The unit lane was run through a config that lifts the repo's `.claude/**` ignore, because worktree paths contain `.claude/`.
- **Merge conflicts:** in `docs/reference.qmd` (the validate paragraph), `packages/core/README.md` (the checks map line) and `skills/python/test_local.py`. All were resolved by keeping both sides.
- **Open choice (M12):** a modeler save now writes the drafted Analysis drawing (+218 lines on the example study; the fingerprint does not change).
- **Incident (M2):** a stray `git stash pop` applied an old shared stash; one file was restored. The stash entry is still in the list, unchanged.

### Study files (S2, partial: the Behaverse values are still in progress)

Applied to all seven protocol files (the three example-study files, `pipeline-check/planted`, `null`, `forced-discontinuation/planted-005`, `nobody-completes/planted-0`):
- **Labels (M1):**
  - `"> 20% unanswered"` → `"> {max_unanswered:%} unanswered"`;
  - "Discontinued: more than 20% …" → "more than {max_unanswered:%} …".
  - This fixes real drift: `planted-005` (0.05) and `planted-0` (0) labelled their exits "20%".
- **Congruency (M2):**
  - The nested per-subject cost sub-process and `scipy.stats.ttest_1samp` are replaced by one `pingouin.pairwise_tests` call (paired, one-sided). `pingouin==0.7.0` is added to the dependencies.
  - Calls: 12 → 8 for this question's path. Nesting: 3 → 2 levels.
  - The feasibility gate now reads `analysed_subjects` instead of `congruency_n`. The two are equal in this protocol: 30 Simon trials, and a completer leaves at most 20% unanswered.
  - The three Behaverse files add one sentence: Simon's neutral trials are a third level, and the decision reads the first row, Congruent against Incongruent (pingouin sorts levels alphabetically).
- **Pipeline check re-run** on `feat/wave2` (old runs moved to `archived/elife/study-runs-2026-10-02-before-wave2/`):
  - The planted, null, forced-discontinuation and nobody-completes results match the earlier runs to every digit, and every claim state is the same. `group.csv` and `per_subject.csv` are byte-identical.
  - New fingerprints: planted `sha256:8268b53e…`, null `sha256:2047a973…`, `planted-005` `sha256:f3f3710a…`, `planted-0` `sha256:f7f8b069…`.
  - Each executed copy validates.

### Paper sync (stage W2)

| Where | Change | Reason |
|:--|:--|:--|
| Step 3 text (L157), `fig-step3-analyze` caption | "SciPy's one-sample *t* test" → "pingouin's paired *t* test"; panel (b) now reads "the descriptive table, …, the one-sided paired t test, one library call on the trials" | M2 |
| `lst-diff` | New `when` and `plan` (8268b53e…); `congruency_n: 8` removed, `subjects: 8` added under `congruency_test` | Re-run |
| `tbl-rule`, Test and direction | "one-sample *t* test of each subject's accuracy cost" → "paired *t* test …, the same test as the accuracy cost against zero" | M2 |
| `tbl-copies` caption | "The labels … repeat some of these values …; the run and the analysis do not read them" → "The diagram's labels show the discontinuation threshold by reading that one value, not by repeating it" | M1 (also closes P1's `tbl-copies` item) |
| `tbl-planted` note | Fingerprints → `8268b53e…` and `2047a973…` | Re-run |
| Methods, the example study | The test is described as a paired *t* test in one library call; neutral Simon trials enter no comparison the decision reads | M2 |
| `tbl-scope` | Allocation row → local "Runs"; browser "Alternation runs; stratified allocation and minimization are refused…". Trial row adds "a trial list registered by the digest of its content" | M5, M4 |
| Limitations (stage L paragraph) | Simon sentence follows D3 option E. "twelve calls" removed. The labels sentence removed. The data-protection sentence follows M7. The allocation sentence → "Return visits and EEG acquisition are described … not run, and stratified allocation and minimization run only in the local runtime" | M1, M2, M5, M7, D3 |
| `tbl-claims` | Four new rows: labels; registered materials; allocation algorithms; data outside history and author | M1, M4, M5, M7 |

### Behaverse step (D3, decided by the user on 2026-10-03: Simon generator written out, a lean 1-back, the actor's window fixed now)

- **Modeler:** `feat/wave2-behaverse-actor`, merged into `feat/wave2` as 8541b1c8.
  - `simulate://planted|null` now answers the trials the Behaverse build sends. They arrive as the whole message, so before the fix it replied `READY` to every trial.
  - The battery prompt reaching the simulated subject as `null` is now written out from its template.
  - One test fails without each fix.
- **Example-study files (all three):** they still differ only in the actor's line.
  - `Simon_Timeline` ("Simon protocol") states the build's Simon values: 30 trials; uniform congruent, incongruent and neutral draws; uniform correct-button draws; onset 1 s; display 1 s; 5 s to answer; feedback after every trial; 0.5 s between trials.
  - A new `NBack_Protocol` states the practice block (14) and the test blocks (28 + 28, in fixed orders), with 0.5 s per digit and a 2.2 s interval. The tutorials stay in the build.
  - `Bot:` elements:
    - `Speed: 1` and a 30 s window (Simon: a trial-level `MaxResponseTime: 30` beside `Bot:`). Before, the actor had about 1 s of real time per trial, while the runner waited 4.75 s.
    - The two inert keys are removed.
    - The documentation is corrected, and the elements are drawn in the Actor pool.
  - 1,395 → 1,590 lines.
  - **Verified headless with 2 subjects:**
    - `simulate://planted`: both completed. The only unanswered trials were its planted non-answers, each closed at 30.0 s.
    - An actor delayed 5 s: all 292 trials were answered.
    - The stated values reach the build: Simon onset 1.000–1.018 s; 1-back blocks 14/28/28 with the stated test orders.
  - New digests: `cfe92a37…`, `3213e7b5…`, `20912640…`.
- **Paper:**
  - `tbl-encoded` gets a third row: the example study audited against its own file. The caption says so.
  - Results ("Prose leaves…"): one sentence on that audit. The file states timing, block sizes and test orders, and leaves the 1-back tutorials and the Simon order (drawn when the task starts, recorded) to the task software.
  - The Reproducibility sentence on the tasks' streams is rewritten.
  - `lst-step2-run`: the listing shows `NBack_Protocol` wired in, the new `Bot_Pace_NB`, and the label `{max_unanswered:%}`. The caption now says the actor's settings depart from the protocol (up to 30 s per digit instead of 2.7 s) instead of "not part of the protocol".
  - The `fig-step2-nback` caption now says the timings drawn are the protocol's for a person, and the actor's settings give up to 30 s.
- **Study README:**
  - the task paragraph;
  - all digests;
  - the wave-2 re-run, and where the old runs went;
  - the drift the label fix removed;
  - the LLM-run duration.

### M12 follow-up (asked by the user)

- `78a04dee`: what a draft drew of a closed sub-process stays out of the file until an edit touches it.
  - The mark is an in-memory set of ids in the Study. Nothing new goes in the file.
  - Opening and saving the example study now gives back its original 1,490 lines, byte-identical. It gave 1,708 before.
  - The empty-layout whole-study draft still saves.
- Merged into `feat/wave2` as 8e698016.
- **Gate:** typecheck, lint, unit and 40 e2e tests pass.

### Two fixes found along the way (merged into `feat/wave2`)

- **BPMN XML round trip** (`fix/wave2-xml-roundtrip`, 4 commits):
  - **The bug:** a value that is not text went into the XML as `String(value)` and came back as text, so `max_unanswered: 0.2` returned as `"0.2"` and the fingerprint changed. Lists and numbers under `values` or `additionalArguments` crashed the export. The plan and the browser runner also garbled or dropped such values; the browser had left the paper's `0.2` unbound.
  - **Now:** values keep their types, and both study files keep their digest through the XML.
  - **Verification:** the planted and null runs are byte-identical afterwards.
  - **Paper:** a new `tbl-claims` row, "A file converts to BPMN 2.0 XML and back without changing its protocol" (`core/studyflow-yaml`).
- **Caption size** (`fix/wave2-label-size`, 46d4cfc1):
  - **The bug:** a label was sized from its name as written (`{max_unanswered:%}`) but drawn resolved, so its box was too tall. In `fig-combined` the 1-back exit line crossed the label.
  - **Fix:** one `drawnNameOf` now feeds both the drawing and the sizing.
- **Integration gate at ccdb4379:** typecheck, lint, 503 unit, 40 e2e.

### Figures

- **Re-rendered** from `feat/wave2`: `fig-step3-decision` (the one-call congruency question), `fig-step3-analyze`, `fig-step2-run` (protocols wired in, actor settings in the actor's pool, 30 s), `fig-step2-nback` (the protocol's timings for a person: 0.5 s, 2.2 s, 2.7 s window), `fig-consort`, `fig-overview`, `fig-combined`, `fig-views`.
- **Second pass** after the caption-size fix: `fig-combined`, `fig-step2-run`, `fig-consort`, `fig-overview`, `fig-views` and `fig-s2-modeler` (it now shows the current Step 2).
  - In `fig-combined`, the 1-back exit label no longer touches its line.
  - `fig-overview` gives "Which instruction? (n=8)" its own label box, because the exclusion line crossed it.
- **Every figure's PNG** embeds its source byte for byte, and each changed source validates with only the expected warnings.
- **Captions changed:**
  - `fig-step2-run`: each task reads its protocol and the actor's settings (30 s).
  - `fig-step2-nback`: the timings drawn are the protocol's; the task reads the 1-back protocol and the actor's settings.
  - `fig-views` (b): "and the fingerprint of the protocol it followed" removed, because the Provenance view does not show it.

## State at the end of waves 1 and 2 (2026-10-03)

- **Modeler:**
  - On 2026-10-03, at the user's request, main was fast-forwarded to `feat/wave2` (543cfaa1, which had merged main's latest, 98661082). Gate there: typecheck, lint, 516 unit, 43 e2e.
  - Every wave-2 branch and worktree was deleted once merged.
  - Not pushed.
- **Study files:** digests are unchanged under the merged build, and `run-planted` still validates.
- **Paper repo:** uncommitted. Changed:
  - `paper-v3.qmd`;
  - the seven study files, the study README, six figure sources, and the eight re-rendered PNGs plus `fig-s2-modeler`.
  - Untracked: four new run folders (git repositories of their own), the archive `archived/elife/study-runs-2026-10-02-before-wave2/`, and this file, `adoption-objections-plan.md` and `limitations-backup.md`.
- **Render check:** `paper-v3.qmd` renders to HTML with no warnings against the committed files. In the full manuscript render, Quarto also renders the `.md` files in `elife/` as notebooks, and `limitations-backup.md` (its `@tbl-…` references) and the untracked `paper-v3p.qmd` and `audience-cuts.md` (not mine) produce crossref warnings there.
- **Left for later waves:** P4 (the Bayes-factor rule in Step 3), P5 (Limitations rewritten from the delivered tooling), P6 (a data-protection paragraph in Methods) and P7 (the paper's numbers read from the study file). Also M3 (R and pinned scripts), M6, M8, M9, M10, M11, M13 and M14.
- **Behaverse runs:** the language-model runs now take about 7–15 min per subject at the build's own clock.
