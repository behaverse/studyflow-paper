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

## The sealed files

The three files differ in one line, the Actor's `implementation`:

| File | Actor | Protocol digest |
| --- | --- | --- |
| `example_study.studyflow.yaml` | `ollama://gemma4:e2b-mlx` | `sha256:e2b45736a3e40495832e1d203015925c410fa2ac19e1d18ec05a49f81d03dce1` |
| `example_study-gemma4-12b.studyflow.yaml` | `ollama://gemma4:12b-it-qat` | `sha256:bff65427f5c9a2a9c0b80b0879824443e9b45cb0b53215088a77787c7aa0d8bd` |
| `example_study-llama3.1-8b.studyflow.yaml` | `ollama://llama3.1:8b` | `sha256:c6e13551f99778e2ca0236af46c19b04c2e1808b8e651675c85e21582036e2f0` |

Digests computed on 2026-10-02 with a build of the modeler's main at `1e2897bd`. Any edit to the protocol changes
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
| `pipeline-check/planted.studyflow.yaml` | `simulate://planted` | `sha256:cf618897260557f1a870df96cdf53823b367791fae0e04e10f6f34715fbfaf19` |
| `pipeline-check/null.studyflow.yaml` | `simulate://null` | `sha256:22a631fde3feccb698c2ee5eaa3999156c07c3d87902d36ea596ba36f9587afe` |

Both were run on 2026-10-02 by a CLI built from the modeler's main at `722fd5c9` (`run-planted/`, `run-null/`: the
executed copy, the trials, the results and the run repository of each); each executed copy validates, its protocol
matching the digest its run recorded. A random gateway draws for each subject from the seed, the gateway and the
subject's number, so these runs deal the arms differently from the runs of 2026-09-29, which are archived in
`../../archived/elife/study-runs-2026-09-29/` with the faulty re-run of 2026-10-02 (its CLI replayed one subject's
allocation for all eight).

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
