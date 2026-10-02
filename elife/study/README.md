# The example study

`example_study.studyflow.yaml` is the paper's example study (`paper-v3.qmd`): one Studyflow file carrying the protocol,
the cohort, both tasks, and the analysis. It is a collaboration of three pools. **Actor** has no process: the language
model its `implementation` names (`ollama://…`, a local Ollama) answers every message the study sends it, and keeps one
conversation per subject (`memory: conversation`). **Each subject** is the protocol one subject walks, eight instances
for now (`participantMultiplicity`, a placeholder the author raises for the reported runs), its lanes the three CONSORT
phases. **Analysis and report** runs once, after the last subject.

Both tasks are the Behaverse battery's, played by its Unity WebGL build (`behaverse:Task`): the Simon task (`WO` on the
`SimonTask` timeline, one block whose exit rule, `Trials: 30` in the `Simon_Timeline` Parameters, is the one place the
study sets its length) and the 1-back (`NB` on `XCIT_NB_01`: three tutorial blocks, a practice block, and two test
blocks of 28 digits, which the analysis keeps). Each task sends every trial to the Actor pool along one pair of message
flows (`behaverse:Trial` out, `behaverse:Response` back) and writes the build's records to `data/trials.jsonl`. The
Parameters with a `Bot:` entry say how the build plays for an actor that is not a person; they are not the protocol.
Both tasks name the build they were written for, `behaverse://assessment-unity@26.10` (its `productVersion`, built from
assessment-unity's `refactor` at `635eb4434`, the first build whose Simon task describes its stimulus to an agent);
the runner does not check it, and each run records the version of the build that played it.

## The study files

The three files differ in one line, the Actor's `implementation`:

| File | Actor | Protocol digest |
| --- | --- | --- |
| `example_study.studyflow.yaml` | `ollama://gemma4:e2b-mlx` | `sha256:f577ace032295c514a4e74c72b6da6b879c14aaefa57da2c1e7c4fe50ed39937` |
| `example_study-gemma4-12b.studyflow.yaml` | `ollama://gemma4:12b-it-qat` | `sha256:32c54b68068731b5acf8ffddbaaf45b5faa34d7e31037ac9675237f7fb94a683` |
| `example_study-llama3.1-8b.studyflow.yaml` | `ollama://llama3.1:8b` | `sha256:1046c97b6dbdb6454ff66dbe9022d46c3776bc59b10cbc82665de25ae8aff2a8` |

Digests computed on 2026-10-02 with a build of the modeler's main at `c7e40477` (`studyflow info`), after the labels and documentation of all seven files took the paper's wording (the two arms are instruction conditions, the second question is the difference between them, its test writes the data object named `Difference test`, and the report's checklist asks that the model, prompts and sampling settings be recorded with each exchange). Before that, two changes to all five files: the discontinuation threshold became one property of the subject's process (`max_unanswered`) that both tasks' exits read, and a step on the completion path (`Record_Completion`, before the completion end event) appends each completer's subject and arm to a Completers dataset (`data/completers.jsonl`), whose trials are the only ones the analysis reads, so a subject discontinued on either task, or excluded, is never analysed and leaves the classifier no missing value. The Completers dataset is bound to a schema of its two columns, so a cohort in which nobody completes reads it as an empty table, and the analysis then ends both questions at *Not testable* (the figure is drawn only when someone was analysed). Appending one record per subject to a `.jsonl` dataset, and reading a not-yet-written one as empty, need the python runner of the modeler's branch `feat/subject-exits` (commits `57ef0393` and `a6f09259`), merged into the modeler's main on 2026-10-02 (as `7f835c09` and `1002fa26` after main was rebased); with an earlier runtime these files fail at `Record_Completion`. Any edit to the protocol changes
them, the cohort size included; the drawing, the Gantt progress and checklist ticks do not. The language-model runs are
pending: the author runs them, with more subjects, once the Behaverse runner sends each trial's stimulus to the model.

## The pipeline check

`pipeline-check/` holds the same registered analysis on a variant whose tasks are `simulate://` timelines (a Simon task
of 30 trials, a 1-back of two test blocks of 28 digits) and whose actor is a simulated participant, in two copies that
differ in that one line: `planted.studyflow.yaml` (`simulate://planted`, less accurate on incongruent Simon trials and
under the impulsive instruction) and `null.studyflow.yaml` (`simulate://null`, equally accurate everywhere). Because
the truth is known, the registered analysis must reach *Supported* on both questions in the planted run and *Not
supported* in the null run, and it does (the paper's `tbl-planted`).

| File | Actor | Protocol digest |
| --- | --- | --- |
| `pipeline-check/planted.studyflow.yaml` | `simulate://planted` | `sha256:6c2c0ee7f0a24c450565fda7734d81f1ef5b98a1c52d79e3e7983309c10cbe8f` |
| `pipeline-check/null.studyflow.yaml` | `simulate://null` | `sha256:07941a7330b423a38ed909916c5d9247115bb9cebe960d100de79ebf8ef69e91` |

Both were re-run on 2026-10-02 by a CLI built from the modeler's main at `c7e40477`, after the rewording
(`run-planted/`, `run-null/`: the executed copy, the trials, the results and the run repository of each). Their trials,
completers and results are byte-identical to those of the runs made earlier that day, after the two changes above, at
the modeler's `feat/subject-exits` (`a6f09259`); those reproduced the tables and decisions of the earlier runs exactly; those runs, made at `722fd5c9` before the changes,
are in `../../archived/elife/study-runs-2026-10-02-before-completers/`. Each executed copy validates, its protocol
matching the digest its run recorded. A random gateway draws for each subject from the seed, the gateway and the
subject's number, so these runs deal the arms differently from the runs of 2026-09-29, which are archived in
`../../archived/elife/study-runs-2026-09-29/` with the faulty re-run of 2026-10-02 (its CLI replayed one subject's
allocation for all eight).

`pipeline-check/forced-discontinuation/` and `pipeline-check/nobody-completes/` hold two further copies of `planted.studyflow.yaml` that differ from it only in `max_unanswered` (0.05 and 0.0; protocol digests `sha256:eb056ba6…` and `sha256:68f378bb…`), each with its run of 2026-10-02 (`run-005/`, `run-0/`, re-run at `c7e40477` after the rewording, with the same subjects, results and claim states): the first discontinues four of the eight subjects and the analysis of the four who completed reaches *Supported* on the congruency question and *Not testable* on the instruction-condition question, and the second discontinues all eight and ends both questions at *Not testable* with no figure (the paper's Methods, the pipeline-check paragraph). Like the other run folders, these two runs are git repositories of their own and stay out of any commit of this folder.

## Running it

```sh
studyflow run --runtime local pipeline-check/planted.studyflow.yaml --repo pipeline-check/run-planted
studyflow run --runtime local pipeline-check/null.studyflow.yaml --repo pipeline-check/run-null
studyflow validate pipeline-check/run-planted/planted.studyflow.yaml
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
