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

The cohort is artificial — eight subjects, eight instances of the subjects' pool (BPMN's
`participantMultiplicity`, drawn as the three-bar parallel marker at the foot of the pool's title band with
`×8` under it, which is where the pool's name used to say it; the subjects do not depend on one another, so
this is a multiplicity and not a loop), all played by Gemma 4 on a local
Ollama (`gemma4:e2b-mlx`). Each subject is screened with a comprehension check, allocated to a
cautious or an impulsive disposition in permuted blocks of four (so eight subjects split four and four), and takes two tasks
from the Behaverse build (`WO` / `SimonTask`, one block of 30 trials whose congruency is drawn per
trial; `NB` / `XCIT_NB_01`, the 1-back the build's human studies run: three tutorial blocks and a practice block,
then two test blocks of 28 digits, all of which run and of which the analysis keeps the test blocks). Every trial goes to the
model as one message and comes back as one response; at the study's grain that exchange is one pair of
message flows drawn on the subjects' pool, which every task inside inherits, and @fig-step2-run draws it
per task. A third message, `all subjects complete`, leaves the subjects' pool once, after its last
instance ends, and starts the analysis pool; the `Trials` dataset sits between the two lab pools, written
by both tasks and read by the analysis. The analysis is
seven preregistered operations: read the recorded trials, keep the answered trials of the test blocks, per-subject
accuracy in each task (and the size of the smaller arm), group statistics, the two questions, and the figure.
Each question is a collapsed sub-process that ends in a decision, at an end event named for its claim state:
**Not testable** when the cohort is below the minimum the decision rules set, else **Supported** or **Not
supported** by its test against their alpha. The congruency effect is a one-sided one-sample t test on each
subject's accuracy cost (congruent minus incongruent); the divergence between the dispositions is a logistic
regression on each subject's accuracy in the two tasks, scored leave-one-subject-out against a permutation of the
arm labels across subjects, which replaces the dummy-classifier baseline. Accuracy is the measure throughout: a
language model's latency is the time its server took to generate the reply, so it is reported (`congruency.csv`)
and not tested. Every threshold sits once in the **Decision rules** Parameters
object wired into the analysis, and the trials dataset is bound to the CSVW **Trial schema** that
`studyflow validate` checks the columns of the first operation against. Nothing in the file is code written
for this study.

## Running it

From the repository root, with a Behaverse WebGL build on hand:

```sh
UNITY_BUILD_PATH=~/workspace/behaverse/assessment-unity/Build/WebGL \
  studyflow run --runtime local elife/study/example_study.studyflow.yaml --repo elife/study/run
```

`studyflow` is `node <studyflow-modeler>/packages/cli/dist/studyflow.mjs`, built from the paper's pinned tag. It needs `uv` and a
local Ollama serving `gemma4:e2b-mlx` (manifest digest `sha256:c4e49a77…`, the id `ollama list` prints). The second sealed file,
`example_study-gemma4-12b.studyflow.yaml`, differs from this one in one line, the actor's `implementation`
(`ollama://gemma4:12b-it-qat`, digest `sha256:38044be4…`); run it with `--repo elife/study/run-gemma4-12b`. Each task carries
`implementation: behaverse://assessment-unity@26.08`, the `productVersion` the WebGL build reports in its `index.html`
(`WebGL.wasm.unityweb` sha256 `f1b767dc…`, `WebGL.data.unityweb` sha256 `9a64bb96…`); the runner does not check that line, it
records the build's `releaseTag` with every event, but the line sits inside the protocol digest, so the seal covers it. The
model's sampling parameters cannot be set from the file: the executor sends none, the Modelfile defaults apply, and every
exchange records them with the model digest in the run repository's commits. A `random` actor is not a one-line swap here,
because the tasks answer the pool's message flows, which only the language-model runner plays. A subject who misses more than 20 % of a task's trials leaves at
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
- `results/` — `per_subject.csv`, `group.csv`, `congruency.csv`, `congruency_test.json`, `accuracy.png`,
  and, when both arms are large enough to test it, `divergence.json`. Which claim state
  each question reached is in the executed copy's `_meta.reached` (`C_Supported`, `D_Not_Testable`, …).
- `studyflow.log` — the walk, message by message.

## The figure

`figures/src/render.sh fig-combined` draws @fig-combined from the executed copy when
`run/example_study.studyflow.yaml` exists, and from the deposited file otherwise. The run in `run/` is the one the
paper reports: four subjects, allocated two and two, all four completing the protocol; the congruency question at
Not supported, and the two between-arm questions at Not testable. That run walked the previous protocol (latency
tested, both tasks pooled, the `Debug` 1-back, the Simon block stopped at 15 trials, arms named by their whole
prompt); run the study again before re-rendering. `studyflow validate run/example_study.studyflow.yaml`
confirms that its protocol is the deposited one (`protocol matches run run`) and that its counts balance;
`studyflow info <file>` prints the full protocol digest of any copy, deposited or executed. The digest ignores the drawing,
the state and the run records, and drops values equal to schema defaults, so quote it together with the pinned tag. After a new
run, copy the `state:` block of the executed copy into `figures/src/fig-consort.studyflow.yaml` and
`figures/src/fig-overview.studyflow.yaml`, and re-render `fig-combined`, `fig-consort`, `fig-overview` and
`fig-views`.

## Why the file is spelled the way the tools write it

The deposited file is kept in the spelling `studyflow convert` writes (`studyflow convert example_study.studyflow.yaml
example_study.studyflow.yaml` rewrites it in place), because the runner writes the executed copy in that spelling.
Deposited that way, the diff between the file and its executed copy holds only additions, the run's records and
state, which is the deviation report the paper shows; a hand-spelled file would differ from its executed copy on every
line the writer orders or wraps differently, although its protocol digest would not change.
