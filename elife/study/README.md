# The example study

`example_study.studyflow.yaml` is the paper's example study (paper-v4): one Studyflow file carrying the protocol,
the cohort, both tasks down to the trial, and the analysis. It is a collaboration of three pools. **Actor** has no
process: whoever its `implementation` names answers every message the study sends it. **Each subject** is the
protocol one subject walks, eight instances (`participantMultiplicity`), its lanes the three CONSORT phases.
**Analysis and report** runs once, after the last subject.

Each task is a sub-process drawn to the trial: a timeline step (`simulate://simon`, 30 trials; `simulate://nback`,
two test blocks of 28 digits), a multi-instance sub-process whose one task sends each trial and the subject's
instruction to the Actor pool, and a record step (`simulate://record`) that scores the answers and appends one row
per trial to `data/trials.jsonl`. The analysis is unchanged in structure from paper-v3 except that latency is gone
(a pool asked one message at a time has no response time the study controls) and the divergence classifier
standardizes its features (the planted run showed that without it the classifier scores 0% under leave-one-out).

## The sealed files

The files differ from `example_study.studyflow.yaml` in one line, the Actor's `implementation`:

| File | Actor | Protocol digest |
| --- | --- | --- |
| `example_study.studyflow.yaml` | `simulate://planted` | `sha256:b31e928d7a1bafb89fba8b5b1972b4f2018b02dc638628ad9845a292aea1f38e` |
| `example_study-null.studyflow.yaml` | `simulate://null` | `sha256:db032e27880987c48ddd02a160bf24f985e249922b73c3639849d74599c04eaf` |
| `example_study-gemma4-e2b.studyflow.yaml` | `ollama://gemma4:e2b-mlx` | `sha256:d30e3dc6a9666ff2881b903fd33df71fc2d633a0fd1e31034fccd83ed9e49b10` |
| `example_study-gemma4-12b.studyflow.yaml` | `ollama://gemma4:12b-it-qat` | `sha256:ce307725e508313c49ecd63047e339fdad96919599ec185f6b18a5c843fd1aa4` |
| `example_study-llama3.1-8b.studyflow.yaml` | `ollama://llama3.1:8b` | `sha256:57344d7f94e4ebac26ff6164e18f87dda91f1b87e93ed8e1999def1c5f77b97f` |

Digests from the modeler at commit `bfbea295` (branch `review-followups`); any edit to a sealed file changes them.
Only the planted and null files were run for paper-v4; the language-model twins are sealed, not run.

## Running it

```sh
studyflow run --runtime local example_study.studyflow.yaml --repo run
studyflow run --runtime local example_study-null.studyflow.yaml --repo run-null
studyflow validate run/example_study.studyflow.yaml
```

`studyflow` is the CLI built from the pinned commit. It needs `uv`; each run takes about four minutes and needs no
model server or task build. A run directory is a git repository of its own (the provenance record), so keep it
out of any commit of this folder, and delete it before re-running.

## Other folders

- `run/`, `run-null/`: the executed copies, the trials, the results and the run repositories of the two runs.
- `encoded/`: two published studies encoded from their Methods sections alone (Hedge et al. 2018; Kucina et al. 2023),
  with `unstated` where the section does not give a value.
- `blind-faults/`: twelve deviations seeded into the fault library's small study by an agent that never saw the
  checks (`faults.json` lists them), scored in the paper's blind-calibration table.
- `run-2026-09-21-previous-protocol/`: the run of the paper-v3 protocol (Behaverse WebGL tasks, one language
  model), kept for reference.
