# The example study

`example_study.studyflow.yaml` is the paper's example study (`paper-v3.qmd`): one Studyflow file carrying the protocol,
the cohort, both tasks down to the trial, and the analysis. It is a collaboration of three pools. **Actor** has no
process: whoever its `implementation` names answers every message the study sends it. **Each subject** is the
protocol one subject walks, eight instances (`participantMultiplicity`), its lanes the three CONSORT phases.
**Analysis and report** runs once, after the last subject.

Each task is a sub-process drawn to the trial: a timeline step (`simulate://simon`, 30 trials; `simulate://nback`,
two test blocks of 28 digits) that makes the trials as a subject sees them and, apart, their key (each trial's right
answer and condition), a multi-instance sub-process whose one task sends each trial and the subject's instruction to
the Actor pool, and a record step (`simulate://record`) that scores the answers by the key and appends one row per
trial to `data/trials.jsonl`. No subject is sent the key: the simulated participant tells the right answer from the
stimulus and the rule, as a language model has to. The analysis is unchanged in structure from this file's previous version (commit
`e24e0fb`) except that latency is gone (a pool asked one message at a time has no response time the study controls)
and the divergence classifier standardizes its features (the planted run showed that without it the classifier
scores 0% under leave-one-out).

## The sealed files

The files differ from `example_study.studyflow.yaml` in one line, the Actor's `implementation`:

| File | Actor | Protocol digest |
| --- | --- | --- |
| `example_study.studyflow.yaml` | `simulate://planted` | `sha256:cf618897260557f1a870df96cdf53823b367791fae0e04e10f6f34715fbfaf19` |
| `example_study-null.studyflow.yaml` | `simulate://null` | `sha256:22a631fde3feccb698c2ee5eaa3999156c07c3d87902d36ea596ba36f9587afe` |
| `example_study-gemma4-e2b.studyflow.yaml` | `ollama://gemma4:e2b-mlx` | `sha256:c2866cfabc2b52f64af0b8e8e30a04bf8822d14b5e8eb03a6b07f50af62d1e5d` |
| `example_study-gemma4-12b.studyflow.yaml` | `ollama://gemma4:12b-it-qat` | `sha256:f33d6c97592950c93027571df83f8538d612fc5724973959ebfbf9d4fca5133f` |
| `example_study-llama3.1-8b.studyflow.yaml` | `ollama://llama3.1:8b` | `sha256:dc6515c392a3f4902673c5df770f51b3ad6b02cbac208d7cd43e4bdea5b26b4c` |

Digests computed on 2026-09-30 with a build of the modeler's `main` after the answer key was kept from the subject
(the modeler's `simulate` fix, "a subject is never sent a trial's answer"). Any edit to a sealed file changes them,
and they will change again when the files are re-spelled at the modeler release the paper cites. The planted and null
files were run on 2026-09-29, before the key was split off: those runs sent each trial with its answer to the
simulated participant, which read its answer from it. Told the answer by the stimulus and the rule instead, it gives
the same answers, so the file run with the key kept apart gives the same trials and results byte for byte; the runs
are re-made at the release. The three language-model twins are run by the
author, after the release, and their results are pending.

## Running it

```sh
studyflow run --runtime local example_study.studyflow.yaml --repo run
studyflow run --runtime local example_study-null.studyflow.yaml --repo run-null
studyflow validate run/example_study.studyflow.yaml
```

`studyflow` is a CLI built from the modeler at commit `bfbea295`, which reproduces both runs (the `v26.9.29` release
has no `simulate` skill). It needs `uv`; each run takes about four minutes and needs no
model server or task build. A run directory is a git repository of its own (the provenance record), so keep it
out of any commit of this folder, and delete it before re-running.

## Other folders

- `run/`, `run-null/`: the executed copies, the trials, the results and the run repositories of the two runs.
- `encoded/`: two published studies encoded from their Methods sections alone (Hedge et al. 2018; Kucina et al. 2023),
  with `unstated` where the section does not give a value.
- `blind-faults/`: twelve deviations seeded into the fault library's small study by an agent that never saw the
  checks (`faults.json` lists them), scored in the paper's blind-calibration table.
- `run-2026-09-21-previous-protocol/`: the 2026-09-21 run of an earlier protocol (Behaverse WebGL tasks, one language
  model, four subjects), kept for reference.
