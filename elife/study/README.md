# The example study

`example_study.studyflow.yaml` is the paper's example study as a study you can run: one Studyflow
file carrying the protocol, the cohort, the battery and the analysis. It is one collaboration of three
pools, because a pool is the boundary of a system, and nothing is nested deeper than one level inside
one: **Gemma 4 (language model)** is a system of its own, so it is a black box the study exchanges
messages with; **Each subject** is the protocol one subject walks; **Analysis and report**
is the same lab system as the subjects' pool but on a different beat, once over the whole cohort rather
than once per subject, which is why it is a pool of its own. The subjects' pool is divided into the three
CONSORT phases — **Enrolment**, **Allocation**, **Follow-up** — as lanes, and into nothing else, so the
figure reads down the phases the way a CONSORT participant flow does, each exit leaving from the right
edge of the phase it belongs to. The lanes carry the tint and the pool none, and the multiplicity marker sits in the pool's
title band, which no lane reaches, so no lane has to give way to it.

The cohort is artificial — four subjects, four instances of the subjects' pool (BPMN's
`participantMultiplicity`, drawn as the three-bar parallel marker at the foot of the pool's title band with
`×4` under it, which is where the pool's name used to say it; the subjects do not depend on one another, so
this is a multiplicity and not a loop), all played by Gemma 4 on a local
Ollama (`gemma4:e2b-mlx`). Each subject is screened with a comprehension check, allocated at random to a
cautious or an impulsive disposition, and takes two tasks
from the Behaverse build (`WO` / `SimonTask`, a Simon task whose congruency is drawn per trial, stopped
at 15 trials by the bot settings; `NB` / `Debug`, two blocks of 16, all 32 run). Every trial goes to the
model as one message and comes back as one response; at the study's grain that exchange is one pair of
message flows drawn on the subjects' pool, which every task inside inherits, and @fig-step2-run draws it
per task. A third message, `all subjects complete`, leaves the subjects' pool once, after its last
instance ends, and starts the analysis pool; the `Trials` dataset sits between the two lab pools, written
by both tasks and read by the analysis. The analysis is
eight preregistered operations — read the recorded trials, drop the ones nobody answered, per-subject
accuracy and latency, group statistics, the congruency effect, the agreement between the two
dispositions, the divergence from a random baseline, and the figure. Three are one call to a library
function; the other five are collapsed sub-processes holding the two to four calls that operation takes.
Nothing in the file is code written for this study.

## Running it

From the repository root, with a Behaverse WebGL build on hand:

```sh
UNITY_BUILD_PATH=~/workspace/behaverse/assessment-unity/Build/WebGL \
  studyflow run --runtime local elife/study/example_study.studyflow.yaml --repo elife/study/run
```

`studyflow` is `node <studyflow-modeler>/packages/cli/dist/studyflow.mjs`. It needs `uv` and a
local Ollama serving `gemma4:e2b-mlx`. A subject who misses more than 20 % of a task's trials leaves at
that task's **conditional boundary event** — `{Task_Interference.failedTrialRate} > 0.2`, a BPMN
condition on the task's own result rather than an attribute of the task — and is counted at
`Discontinued`. A browser window opens for each task of each subject and closes itself when the task
ends; leave it in front, since the runner's anti-throttle flags are what keep an occluded window running
at full speed. Delete `elife/study/run/` before re-running, or the counters and the allocation draws
carry on from the last run — and note that the run directory is a git repository of its own (the
provenance record), so keep it out of any commit of `elife/study/`.

## What the run leaves in `run/`

- `example_study.studyflow.yaml` — the executed copy: the same study with a `state:` block holding
  `_meta.prov` (what ran, when, with which seed), `_meta.reached` (how many tokens reached each
  element, which is what every `(n={reached})` label prints) and the scope's last property values.
- `data/trials.jsonl` — one line per recorded event, from every task of every subject: the build's
  own frame under `trialContext`, and under `context` the subject and the properties in scope,
  including the allocated `arm`.
- `results/` — `per_subject.csv`, `group.csv`, `congruency.csv`, `agreement.json`,
  `divergence.json`, `baseline.json`, `accuracy.png`.
- `studyflow.log` — the walk, message by message.

## The figure

`figures/src/render.sh fig-combined` draws @fig-combined from the executed copy when
`run/example_study.studyflow.yaml` exists, and from the deposited file otherwise.
**There is no `run/` right now**: the run made before the study became a three-pool collaboration
no longer matches this file, so every figure currently renders the deposited plan and every `(n=…)`
label prints `n=0`. A fresh run refills them; re-render `fig-combined`, `fig-consort`, `fig-overview`
and `fig-views` afterwards.
