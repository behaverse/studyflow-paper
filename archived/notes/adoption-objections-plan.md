# Answering a cognitive scientist's objections: plan (2026-10-02)

This plan answers the eight objections a skeptical experimental psychologist raises after reading `paper-v3.qmd` and trying the modeler. It is grounded in two surveys of studyflow-modeler at main, 2026-10-02. Nothing has been changed yet.

Each objection gets one or more of three kinds of answer:
- **Tool**: a change in studyflow-modeler, with its test.
- **Study**: a new or changed study file, or a new run.
- **Paper**: text in `paper-v3.qmd`.

Paper claims follow the tool: a claim enters `tbl-claims` only once its test exists. Manuscript edits go in small stages, as before.

## 1. Objection → answer

| # | Objection | What is true at modeler main | Answer | Items |
|:--|:--|:--|:--|:--|
| 1 | I can't run my participants | Browser run data stays in memory; the only exit is a "Download events.jsonl" button. The only server sink is the Behaverse Data Server, opt-in per visiting browser. No resume, no write-back of counts. No JATOS/Pavlovia/OSF. Behaverse ships only as a binary | Tool, Paper | M9, M10, P2, P5 |
| 2 | Trial-level decisions sit outside the diagram | Simon congruency comes from the build's own generator, which the seed doesn't reach; `XCIT_NB_01` is a name; `Bot:` pacing sits on the task; no trial-list element; jsPsych nested timelines aren't imported and its randomization isn't seeded | Tool, Study, Paper | M4, M10, S2, P3 |
| 3 | The analysis is harder than a script (and no R; claim states are tied to *p*) | One *t* test takes 12 pandas/SciPy calls across 3 levels of nesting; no `r://` runner; formula APIs are untested; no Bayes-factor or interval example | Tool, Study, Paper | M2, M3, S2, P4 |
| 4 | Too costly to learn, for too little payoff now | 1,490 lines (19% drawing, 11% documentation); 12 departures from BPMN; no templates; no usability evidence; day-one gains are not stated | Tool, Paper | M11, M12, P2, P5 |
| 5 | The single source of truth is weaker than claimed | Labels hard-code "20%" beside `max_unanswered: 0.2`, and placeholders read only run state; there is no text export, so prose is written by hand; the digest has no timestamp; "outlives the software" is an overclaim | Tool, Paper | M1, M6, M13, P1, P7 |
| 6 | Trust and privacy | Validator checks form only. Python steps run as plain subprocesses with no sandbox, and `docker://` has no runner. The run repository commits everything, with the OS username in git | Tool, Paper | M7, M8, P6 |
| 7 | My paradigm isn't covered | No counterbalancing, adaptive or multi-session elements. `stratifyBy`, minimization and alternation are in the schema but not applied. EEG is vocabulary only; browser timers are `setTimeout` | Tool, Paper | M5, M14, P3 |
| 8 | The demonstration is only language models, n = 8, TODOs | LLM runs pending; planted/null are the only finished runs | Study, Paper | S1, P2, P5 |

## 2. Decisions (user, 2026-10-02)

- **D1. Human cohort: Limitations only.**
  - No human cohort in this submission.
  - The human data path (M9, M10) is built and tested, and the paper says it is implemented but not demonstrated with people.
  - Usability stays an open hypothesis in the Limitations.
- **D2. Analysis: library calls, formula APIs, R, and version-pinned scripts.**
  - A step may call a library function (`python://`, `r://`) or a function in a script the study ships (`python://./analysis.py:fn`, `r://./analysis.R:fn`).
  - The script is pinned by its content digest, which enters the protocol fingerprint, so editing the script is a protocol change.
  - *Assumed, not decided:* the example study keeps library calls (shorter, through formula APIs); a shipped modeler example shows the script step.
- **D3. Trial level: not asked; plan assumes the recommendation.** Run-critical trial values are written into the study file, a trial list is registered as a data object with a content digest, task randomization is seeded from the study seed, and the actor's accommodations (`Bot:`) move to the actor's pool.
- **D4. Manuscript numbers: rendered from the study file (P7).**
- **D5. Data sinks: all three.** A study-level sink with DataPipe (OSF, no server), JATOS (self-hosted, session state for resume) and the Behaverse Data Server adapters. The Behaverse server is configured by the study, not opted into per visiting browser. Plus `studyflow collect`.

## 3. Changes

Sizes are rough estimates: S ≤ 1 day, M 2–5 days, L > 1 week.

### Paper only (can start now, staged)

- **P1. Corrections (5).**
  - L59 and L234: the exported XML keeps the structure and attributes any BPMN tool can read and draw, but running it follows the Studyflow specification. So what outlives the tools is the specification and the file, not execution in generic engines.
  - L684: "sealed again" goes, per [no sealing].
  - `tbl-copies` caption: the labels' repeated values stay until M1 lands.
  - S.
- **P2. Discussion: "Who it is for and what it gives on day one".**
  - Checks before any data: a column typo, an unreachable exit, overlapping criteria.
  - Simulate before you collect: run your own registered analysis on planted and null participants, the pipeline check, as a researcher's first use.
  - CONSORT and Gantt figures for free.
  - Then what it costs. Ends with an honest "what runs where" table (P3).
  - S–M.
- **P3. Methods "Expressiveness and limits": a "what runs where" table.**
  - Rows are constructs: between-subject allocation, stratified allocation, counterbalanced orders, trial lists, adaptive procedures, multi-session, EEG acquisition.
  - Columns: the notation, the local runtime, the browser runtime.
  - Plus one sentence of scope: Studyflow coordinates; trial-level content is in the file only when written there (D3).
  - S.
- **P4. Step 3: the claim state is not tied to *p*.**
  - A gateway condition is FEEL over any result, so a Bayes factor or an interval rule draws the same way.
  - Cite the M2 example. In Methods, one sentence on R (M3).
  - S, after M2/M3.
- **P5. Limitations rewritten from what waves 2–4 deliver.**
  - Human cohort (D1): the browser path to a data sink and `studyflow collect` are implemented and tested (M9, M10) but no person has taken the study.
  - Why language models: they are the cheapest actor that fails the way people do (an answer outside the options, no answer in time), so every exit fires on real failures.
  - Usability: still a hypothesis.
  - Also: the validator's meaning gap, and single-lab maintenance (M13).
  - S, last.
- **P6. Methods: a data-protection paragraph.** What a run repository holds, the pseudonymised ids and data-outside-git defaults (M7), and what a deposited executed copy carries. S, after M7.
- **P7. The paper reads its numbers from the study file (D4).**
  - A Quarto shortcode such as `{{< studyflow study/example_study.studyflow.yaml Simon_Timeline ExitRules Trials >}}` renders a value from the file.
  - Build it as a Lua extension that parses the YAML through `pandoc.read` as front matter (spike first). Ship it from the modeler, so any author can use it, and install it into `elife/_extensions`.
  - Replace every example-study value in the prose, captions and tables (30 trials, one in five, blocks of four, 1:1, alpha, minimum per arm, permutations, the counts after the run). The paper then demonstrates its own claim.
  - M, after S2, because values move in the file.

### Modeler (studyflow-modeler, each with its test and a `tbl-claims` row)

- **M1. Labels read values.**
  - Placeholders resolve declared property and Parameters values as well as run state, with one format suffix (`{max_unanswered:%}` → 20%).
  - `validate` warns when a label carries a number literal that equals a value the element reads ("use {…}").
  - Code: `packages/core/src/model/state.ts`, `checks/`.
  - S–M.
- **M2. Short analyses and non-*p* rules.**
  - A tested example where one step does the congruency test on trial-level data. Candidate: `pingouin.pairwise_tests` with `within`, `subject` and `alternative`, averaging per subject; check its `aggfunc` before relying on it. Or a nested `statsmodels.formula.api` call.
  - A second question decided by a Bayes factor (`pingouin.ttest`, `BF10 > 3`).
  - `data-contract.ts` learns to read column names in a `formula` string.
  - Code: `skills/python/examples`, `skills/python/test_local.py`.
  - M.
- **M3. `r://` runner and pinned script steps (D2).**
  - **R.** A new `skills/r` calls `pkg::fn` through Rscript. Data frames pass as Parquet or CSV, `@version` is checked against `packageVersion`, and dependencies are pinned per study. Example: `stats::t.test` and `lme4::lmer`.
  - **Scripts.** `python://./analysis.py:fn` and `r://./analysis.R:fn` call a function in a file the study ships.
    - The file is a registered material (M4): its content digest is written on the step and enters the protocol fingerprint.
    - `validate` checks the digest, and `run` refuses a script that changed.
    - The diff of a changed script shows as a protocol change.
  - The data contract checks the columns a script step names in its arguments; what the script reads inside is not checked (said in P3).
  - L.
- **M4. Registered materials (D3a).**
  - A data object or consent URI may carry a `digest`, and `validate` checks the file's content against it. Trial lists, stimulus sets and consent forms then enter the registered protocol.
  - A shipped example: a trial list (CSV plus CSVW schema), produced by any tool (SweetPea is cited), wired to a task and iterated by a multi-instance loop. The engine already supports `loopDataInputRef` over a list.
  - M.
- **M5. Allocation honesty.**
  - Apply `stratifyBy` with permuted blocks within strata, or remove `stratifyBy`, minimization and alternation from the schema until they run.
  - A counterbalanced-order example: one arm per task order, permuted blocks.
  - Code: `packages/core/src/engine/allocation.ts`.
  - M.
- **M6. Text exports.**
  - A "Methods draft" export (participants, design, procedure, analysis, each sentence naming its element).
  - An OSF/AsPredicted preregistration export that carries the protocol digest, so a registry's timestamp covers the fingerprint.
  - Both an `ExportFormat` in `modeler/src/diagram/formats.ts` and `studyflow convert --into md`.
  - M.
- **M7. Privacy defaults.**
  - Participant ids pseudonymised in records.
  - A run option that keeps raw data out of git history and commits only digests of data files.
  - The prov author is configurable instead of the OS username.
  - A `studyflow` share command that writes an executed copy with counts and decisions but no raw data.
  - Code: `packages/runtime-local/src/prov.ts`, `run.ts`.
  - M.
- **M8. Trust.**
  - Before running a file not written on this machine, `studyflow run` lists every external call (scheme, function, version) and asks once (`--trust` to skip).
  - A container runner for `python://` steps (podman or docker, image pinned by digest, network off). Closes the containers row of `tbl-claims`.
  - M–L.
- **M9. Browser data sink (D5).**
  - **Sink.** A study-level `dataSink` that the browser runtime sends trials and events to as the session runs, with the completion recorded.
  - **Adapters:**
    - DataPipe (OSF).
    - JATOS (`jatos.js`; its study session data gives return visits, M14).
    - The Behaverse Data Server, moved from a hard-coded URL and a per-browser checkbox in `skills/behaverse/browser/dataServer.ts` to the study's own setting.
    - A generic HTTPS POST.
  - **Ids.** Reads `PROLIFIC_PID` as the participant id.
  - **Collect.** `studyflow collect <file> <records…>` folds sessions from any sink into the executed copy (counts, prov) and runs flow consistency. This makes the CONSORT figure work for a human cohort.
  - **Tests.** End-to-end with a local mock sink, in Playwright.
  - L.
- **M10. jsPsych for real tasks.**
  - Import nested timelines (today they become a plugin called "timeline").
  - Seed `jsPsych.randomization` from the study seed and participant.
  - Write the trial data's columns to a schema.
  - This gives an open-source path for the two example tasks.
  - M.
- **M11. Templates.** "New study from template": between-subjects trial, within-subject experiment, online questionnaire, and the pipeline check (planted/null) of any of them. S–M.
- **M12. Lighter files.** Default styles so a drawn element carries no `stroke`/`fill`/`font` unless changed (111 of the 288 drawing lines in the example), and auto-layout of undrawn sub-processes. S–M.
- **M13. Specification and conformance.** Publish the specification as a versioned document, and the draw fixture plus the fault library as a conformance suite another implementation can run. Answers the single-lab concern. M.
- **M14. Adaptive and multi-session (spike).** One example of a staircase as a loop over a library's update function (e.g. `questplus`), checking that its state persists across steps. Return visits in the browser through the JATOS adapter (M9). The result is a working example or a precise limitation in P3. M.

### Study files and runs

- **S1. Language-model cohorts, as already planned**, with more subjects. They also show the real failure modes that fire the exits.
- **S2. The example study under its own audit.**
  - Apply `tbl-encoded`'s columns to the example study, as a third row.
  - With D3a, write the Simon and 1-back run-critical values into the file (sequence or its generator seed, ISI, deadline, stimulus duration, congruent proportion), and move `Bot:` to the actor.
  - With M1, labels read `max_unanswered`.
  - With M2, the congruency question shrinks from 12 calls to about 3.
  - Re-run the pipeline check. Fingerprints change; no sealing.
- **S3. Dropped (D1).** No human cohort in this submission. The comprehension study, run through Studyflow, remains the natural follow-up and goes into Future work.
- **S4 (optional).** Fill the `unstated` values of hedge2018 and kucina2023 from their shared code and supplements, and run each encoding on simulated participants. This shows that the encoding is the replication protocol.

## 4. Order

| Wave | Items | Unlocks |
|:--|:--|:--|
| 1, now | P1, P2, P3 | Objections 4, 5, 7 answered in text; no tool dependency |
| 2, small tool | M1, M2, M4, M5, M7, M12 → S2 | Objections 2, 3, 5, 6 shown in the example study |
| 3, medium tool | M3, M6, M8, M9, M10, M11, M13, M14 spike | Objections 1, 3, 6, 7; the human data path exists and is tested |
| 4, study | S1, S4 optional | Objection 8 with the language-model data |
| 5, paper | P4, P5, P6, P7, `tbl-claims` rows, `tbl-encoded` third row | Paper matches what the tool and runs show, and reads its numbers from the file |

## 5. Not planned, and why

- **A trial-level authoring language of our own.** jsPsych, PsychoPy and SweetPea do this. Studyflow registers their output (M4, M10) rather than competing.
- **Validator checks of statistical meaning** (difference vs equivalence). This would need a hypothesis attribute per question, against [BPMN-native over new attributes]. It stays a reader's judgement, stated in the Limitations.
- **Sealing, DOI deposit, Zenodo.** Per [no sealing]. M6's registry export gives the timestamp through the researcher's own registry.

## 6. Risks

- Wave 3 is several weeks of modeler work; M9 and M3 are the largest.
- Without a human cohort, objections 1, 4 and 8 are answered by tested tooling and honest Limitations, not by data. A reviewer may still ask for the cohort.
- P7's Lua YAML parsing through `pandoc.read` is unproven, so spike it before rewriting prose around it.
- Every study-file change re-runs the pipeline check and changes fingerprints, so the figures and `lst-diff` are re-rendered once, after wave 2.
- Each new tool claim adds a `tbl-claims` row and a test, which keeps the paper honest but lengthens Methods.

[no custom computation]: memory `no-custom-computation-in-diagrams`
[no sealing]: memory `no-sealing-or-doi-deposit`
[BPMN-native over new attributes]: memory `bpmn-native-over-new-attributes`
