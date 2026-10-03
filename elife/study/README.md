# The example study

`example_study.studyflow.yaml` is the paper's example study (`paper-v3.qmd`): one Studyflow file carrying the protocol,
the cohort, both tasks, and the analysis. It is a collaboration of three pools. **Actor** has no process: the language
model its `implementation` names (`ollama://…`, a local Ollama) answers every message the study sends it, and keeps one
conversation per subject (`memory: conversation`). **Each subject** is the protocol one subject walks, eight instances
for now (`participantMultiplicity`, a placeholder the author raises for the reported runs), its lanes the three CONSORT
phases. **Analysis and report** runs once, after the last subject.

Both tasks are the Behaverse battery's, played by its Unity WebGL build (`behaverse:Task`): the Simon task (`WO` on
the `SimonTask` timeline) and the 1-back (`NB` on `XCIT_NB_01`: three tutorial blocks, a practice block, and two test
blocks of 28 digits, which the analysis keeps). Their run-critical values are written in the file and merged over the
build's own: `Simon_Timeline` ("Simon protocol") states the Simon block (30 trials, its timing, draws and feedback),
`NBack_Protocol` the 1-back's practice and test blocks; the 1-back's tutorials run as the build ships them, and the
build draws the Simon task's congruency order when the task starts and records its seed with every trial. Each task
sends every trial to the Actor pool along one pair of message flows (`behaverse:Trial` out, `behaverse:Response` back)
and writes the build's records to `data/trials.jsonl`. The Parameters with a `Bot:` entry, drawn in the Actor pool, say
how the build plays for an actor that is not a person and where that departs from the protocol: the build keeps its own
clock (`Speed: 1`), and every trial waits up to 30 s for the actor's answer (a person has 5 s in the Simon task and
2.7 s per digit in the 1-back).
Both tasks name the build they were written for, `behaverse://assessment-unity@26.10` (its `productVersion`, built from
assessment-unity's `refactor` at `635eb4434`, the first build whose Simon task describes its stimulus to an agent);
the runner does not check it, and each run records the version of the build that played it.

## The study files

The three files differ in one line, the Actor's `implementation`:

| File | Actor | Protocol digest |
| --- | --- | --- |
| `example_study.studyflow.yaml` | `ollama://gemma4:e2b-mlx` | `sha256:cfe92a375a5d324da34f9871af8facb562762f60adafd0b52a84fd246c44c4fa` |
| `example_study-gemma4-12b.studyflow.yaml` | `ollama://gemma4:12b-it-qat` | `sha256:3213e7b5705c3d90922368201eb23f835cd841076dbeed53694c73dd841edda5` |
| `example_study-llama3.1-8b.studyflow.yaml` | `ollama://llama3.1:8b` | `sha256:20912640ecd1b2459198e26d152d0f434b65b12e01aefd76b517108b55352ebf` |

Digests computed on 2026-10-03 with a build of the modeler's `feat/wave2` at `8541b1c8`, in main since `543cfaa1` (`studyflow info`), after three changes (`../../archived/notes/adoption-objections-plan.md`, wave 2): the exits' labels read `{max_unanswered:%}` instead of repeating 20%; the congruency question tests in one call (`pingouin.pairwise_tests`, paired, one-sided) instead of five; and, in the three example-study files, the tasks' run-critical values are written out and the actor is given 30 s per trial at the build's own clock. Before that, on 2026-10-02 at the modeler's main `c7e40477`, the labels and documentation of all seven files took the paper's wording (the two arms are instruction conditions, the second question is the difference between them, its test writes the data object named `Difference test`, and the report's checklist asks that the model, prompts and sampling settings be recorded with each exchange). Before that, two changes to all five files: the discontinuation threshold became one property of the subject's process (`max_unanswered`) that both tasks' exits read, and a step on the completion path (`Record_Completion`, before the completion end event) appends each completer's subject and arm to a Completers dataset (`data/completers.jsonl`), whose trials are the only ones the analysis reads, so a subject discontinued on either task, or excluded, is never analysed and leaves the classifier no missing value. The Completers dataset is bound to a schema of its two columns, so a cohort in which nobody completes reads it as an empty table, and the analysis then ends both questions at *Not testable* (the figure is drawn only when someone was analysed). Appending one record per subject to a `.jsonl` dataset, and reading a not-yet-written one as empty, need the python runner of the modeler's branch `feat/subject-exits` (commits `57ef0393` and `a6f09259`), merged into the modeler's main on 2026-10-02 (as `7f835c09` and `1002fa26` after main was rebased); with an earlier runtime these files fail at `Record_Completion`. Any edit to the protocol changes
them, the cohort size included; the drawing, the Gantt progress and checklist ticks do not. The language-model runs are
pending: the author runs them, with hundreds of subjects per model (a multiple of four, so that the permuted blocks
split the arms evenly); at the build's own clock a subject takes about 7 to 15 minutes, depending on how fast the
model answers. The local runtime runs the instances of a pool one after another (the paper's `tbl-departures`), so a
cohort of 300 takes about 35 to 75 hours per model unless the runtime runs them at once.

On 2026-10-03 two notes of the three files were reworded to what the runner does, with no change to the protocol's
behaviour: the screening checklist's executor item ("recorded with every exchange", not "pinned") and the first
inclusion criterion ("Registered model, at a version recorded with every exchange", not "a pinned model tag"). Notes
enter the digest, so the three digests above predate that edit; they change again when `participantMultiplicity` is
raised for the reported runs. Recompute them with `studyflow info` before the runs.

## The pipeline check

`pipeline-check/` holds the same registered analysis on a variant whose tasks are `simulate://` timelines (a Simon task
of 30 trials, a 1-back of two test blocks of 28 digits) and whose actor is a simulated participant, in two copies that
differ in that one line: `planted.studyflow.yaml` (`simulate://planted`, less accurate on incongruent Simon trials and
under the impulsive instruction) and `null.studyflow.yaml` (`simulate://null`, equally accurate everywhere). Because
the truth is known, the registered analysis must reach *Supported* on both questions in the planted run and *Not
supported* in the null run, and it does (the paper's `tbl-planted`).

| File | Actor | Protocol digest |
| --- | --- | --- |
| `pipeline-check/planted.studyflow.yaml` | `simulate://planted` | `sha256:8268b53e2a332deb9c9de443785933041a804c7fb77345069ebcaa82c01c39d8` |
| `pipeline-check/null.studyflow.yaml` | `simulate://null` | `sha256:2047a9739c296f725da9cbb3c0ff721224f0213b451030dccec55eb09eb0b830` |

Both were re-run on 2026-10-02 by a CLI built from the modeler's `feat/wave2` at `cf548588` (in main since `543cfaa1`), after
the wave-2 changes above (`run-planted/`, `run-null/`: the executed copy, the trials, the results and the run
repository of each). Their tests, decisions, `group.csv` and `per_subject.csv` are identical to those of the runs made
earlier that day at `c7e40477`, now in `../../archived/elife/study-runs-2026-10-02-before-wave2/`; those runs' trials,
completers and results were byte-identical to those of the runs made before them, after the two changes above, at
the modeler's `feat/subject-exits` (`a6f09259`); those reproduced the tables and decisions of the earlier runs exactly; those runs, made at `722fd5c9` before the changes,
are in `../../archived/elife/study-runs-2026-10-02-before-completers/`. Each executed copy validates, its protocol
matching the digest its run recorded. A random gateway draws for each subject from the seed, the gateway and the
subject's number, so these runs deal the arms differently from the runs of 2026-09-29, which are archived in
`../../archived/elife/study-runs-2026-09-29/` with the faulty re-run of 2026-10-02 (its CLI replayed one subject's
allocation for all eight).

`pipeline-check/forced-discontinuation/` and `pipeline-check/nobody-completes/` hold two further copies of `planted.studyflow.yaml` that differ from it only in `max_unanswered` (0.05 and 0.0; protocol digests `sha256:f3f3710a…` and `sha256:f7f8b069…`), each with its run of 2026-10-02 (`run-005/`, `run-0/`, re-run at `feat/wave2` `cf548588` after the wave-2 changes, with the same subjects, results and claim states; until then their labels said 20%, the drift the new label check exists to prevent): the first discontinues four of the eight subjects and the analysis of the four who completed reaches *Supported* on the congruency question and *Not testable* on the instruction-condition question, and the second discontinues all eight and ends both questions at *Not testable* with no figure (the paper's Methods, the pipeline-check paragraph). Like the other run folders, these two runs are git repositories of their own and stay out of any commit of this folder.

`pipeline-check/unstandardized/planted-unstandardized.studyflow.yaml` is a third copy of `planted.studyflow.yaml`
(2026-10-03) without the `StandardScaler` before the classifier (and its documentation says so). It keeps the fault the
paper reports in the pipeline-check paragraph of Methods: fitted to unstandardized accuracies, the classifier scored 0%
under leave-one-out. It has not been run or validated yet; run it as below into `run-unstandardized/` and check that
result before submission.

## Running it

```sh
studyflow run --runtime local pipeline-check/planted.studyflow.yaml --repo pipeline-check/run-planted
studyflow run --runtime local pipeline-check/null.studyflow.yaml --repo pipeline-check/run-null
studyflow validate pipeline-check/run-planted/planted.studyflow.yaml
studyflow run --runtime local pipeline-check/unstandardized/planted-unstandardized.studyflow.yaml --repo pipeline-check/unstandardized/run-unstandardized
studyflow run --runtime local example_study.studyflow.yaml --repo run
```

Until the next release, `studyflow` is a CLI built from the modeler's main (`npm install && npm run build` in a clone;
`node packages/cli/dist/studyflow.mjs`); its `--version` still prints 26.9.29, and the `v26.9.29` release has no
`simulate` skill. The local runtime needs `uv`. A pipeline-check run takes under a minute and needs no model server or
task build. The example study needs an Ollama server holding the three model tags and the Behaverse WebGL build
(`UNITY_BUILD_PATH`, or an `assessment-unity` checkout beside the modeler). A run directory is a git repository of its
own (the provenance record), so keep it out of any commit of this folder, and delete it before re-running.

## Other folders

- `encoded/`: two published studies encoded from their Methods sections alone (Hedge et al. 2018; Kucina et al. 2023),
  with `unstated` where the section does not give a value.
- `blind-faults/`: twelve deviations seeded into the fault library's small study by an agent that never saw the
  checks (`faults.json` lists them), scored in the paper's blind-calibration table.
- `run-2026-09-21-previous-protocol/`: the 2026-09-21 run of an earlier protocol (Behaverse WebGL tasks, one language
  model, four subjects), kept for reference; at the modeler's main it no longer validates (its expressions are not
  FEEL).
