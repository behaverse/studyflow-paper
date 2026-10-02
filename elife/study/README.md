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
| `example_study.studyflow.yaml` | `simulate://planted` | `sha256:f5a4afc5a2c39fbfdf75c109e76880b923373ae6400b50d6cbc16a755e40ac93` |
| `example_study-null.studyflow.yaml` | `simulate://null` | `sha256:3510cfc231f69c5bb76d7426fcdb2a11cad295a660f14aa8b1f7ba0644a98be7` |
| `example_study-gemma4-e2b.studyflow.yaml` | `ollama://gemma4:e2b-mlx` | `sha256:2f3f89d12b6985701a82dd23b6f1c397a9ad9bc56368d299e247f38533632928` |
| `example_study-gemma4-12b.studyflow.yaml` | `ollama://gemma4:12b-it-qat` | `sha256:c5e0e242f0c1b6013fc91662687e1a37e7fa066f398b8cda8bcb994bdcce4732` |
| `example_study-llama3.1-8b.studyflow.yaml` | `ollama://llama3.1:8b` | `sha256:9e5b947d350538de52fb98ead1a229fade9c1934931dc5e553349311b79b0380` |

Digests computed on 2026-10-01 with a build of the modeler's main at `6389edc1`, where the modeler reads and writes a study as the study model its YAML spells (moddle only reads and writes BPMN XML), after the answer key was kept from
the subject (the modeler's `simulate` fix, "a subject is never sent a trial's answer") and after the scoring of a
reply moved into the files: each asking step's data output names, in FEEL, which option a reply gives, and the record
step counts only an answer that is one of the options. Since the same day a random gateway draws for each subject
from the seed, the gateway and the subject's number, so the release runs deal the arms differently from the runs of
2026-09-29. Any edit to the protocol of a sealed file changes them; its spelling does not (the files were re-spelled
as that build writes them, and their digests, read from the YAML or from the BPMN XML it spells, stayed). The planted and null
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
- `run-2026-10-02-rerun/`: a copy of `run/` re-run on 2026-10-02 after its `Analysis` record was invalidated, by the
  CLI that made `run/` (studyflow-modeler at 39314fe9), so its history branches there; the subjects are simulated, so
  it called no model. Only the overview figure's Provenance view reads it
  (`../../archived/elife/figure-tools/overview-history.py` merges its records with `run/`'s); `run/` stays as the run
  left it.
