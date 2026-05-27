# §2.6 N-back Round-Trip — Empirical Protocol

The §2.6 empirical commitment is a round-trip — *authored diagram → published to data server → run via runner with seeded determinism → trial CSV*. This document specifies the anchor artifact and the runbook so a teammate can execute without further specification.

**Status:** the §2.6 prose is in its final form. The two-encoding clarification (trial-by-trial pedagogical vs. block-level executable) has been applied; the CogEnv paragraph has been added; what remains is to land the pilot data and Figure 4. Two `[GAP]` markers in §2.6 of [`paper.md`](./paper.md) (lines 154 and the Figure 4 reference at line 105) will be resolved by the runbook below.

---

## 1. The anchor artifact

**Use** [`studyflow-modeler/src/assets/examples/demo1.studyflow`](../../studyflow-modeler/src/assets/examples/demo1.studyflow) — existing, shipping, validated.

`demo1.studyflow` is already a complete LabLink protocol that exercises every primitive §2.6 claims: a consenting start event, a markdown Welcome instruction, PHQ-9 + GAD-7 baseline questionnaires, a 1-back warm-up (`behaverse:behaverseTask scene="NB"` with inline block configuration including an `agentMode="bot"` configuration), a `cognitive:randomGateway` allocating to three N-back arms (2-back symbols, 2-back digits human, 1-back demo), post-task PHQ-9, and a terminating end event with a Prolific-style completion code. **Do not author a parallel N-back file.**

If a leaner standalone version is wanted for Figure 7 clarity later, derive it by stripping `demo1.studyflow` to just the consent → Welcome → 1-back warm-up → end path; save the result alongside the paper.

## 2. Encoding note (already reflected in §2.6)

Two legitimate N-back encodings are referenced in the paper, and §2.6 now distinguishes them explicitly:

- **Trial-by-trial encoding (pedagogical, Figure 7).** Each trial is a separate `bpmn2:task` carrying `studyflow:url="behaverse://show_stimulus"` with boundary timer events for stimulus duration and ITI. Useful as a diagrammatic explanation of trial structure but does not scale.
- **Block-level encoding (executable, the runner).** One `bpmn2:task` carries `behaverse:behaverseTask scene="NB"` with an inline YAML block that the Behaverse Unity runtime expands into individual trials. This is what `demo1.studyflow` uses and what the runner executes.

The round-trip below uses the block-level encoding.

## 3. Round-trip runbook

Four required steps; total elapsed time ≈ 2 h. Step 5 (human-subject pilot) is optional.

### Step 1 — Open and verify the anchor

1. Open <https://behaverse.org/studyflow-modeler/app> in Chrome or Firefox.
2. Sign in with a Behaverse API key (guest mode cannot publish).
3. *File → Open* → select `demo1.studyflow` from a local clone of `studyflow-modeler`.
4. Verify the modeler renders all elements without errors. Check inspector panels for the warm-up task, the random gateway, and the three N-back arms.

**Deliverable:** one modeler screenshot of the loaded diagram (panel a of Figure 4).

### Step 2 — Simulate before publishing

1. Click *Simulate* (top toolbar).
2. Step through each node. Confirm gateway routing fires, PHQ-9/GAD-7 render the instrument UIs, and the random allocation branches.
3. If any node aborts simulation, file an issue against `studyflow-modeler` and pause this protocol.

### Step 3 — Publish

1. *File → Publish*. The modeler uploads to the Behaverse Data Server tied to the API key.
2. Capture the participant-facing URL the server returns.
3. Tag the local source with a `version` attribute on the `Study` element so the file matches what is published. Commit the tag and the URL to the paper repo at `elife/assets/nback_published_url.txt`.

**Deliverable:** screenshot of the publish dialog (panel b of Figure 4) plus the URL.

### Step 4 — Run via the runner with a seed (bot mode — no IRB needed)

1. Open <https://behaverse.org/studyflow-modeler/run.html?studyflow_url=URL&seed=42> in an incognito window, substituting the published URL.
2. Confirm the runner walks: consent → Welcome → PHQ-9 → GAD-7 → 1-back warm-up (bot mode via `agentMode="bot"`) → random gateway → one of three N-back arms (decided by seed=42) → post-PHQ-9 → end.
3. Repeat with `seed=43`, `seed=44`, `seed=45` to verify the random gateway deterministically picks different arms across seeds.

**Deliverables:**
- Four runner screenshots stitched into a single composite figure (Figure 4): consent, mid-instruction, mid-1-back, end-screen-with-completion-code.
- The bot-emitted trial CSV at `elife/assets/pilot_trials_bot.csv` (BDM trials-level schema, Psych-DS-compatible).
- One-paragraph summary at `elife/assets/pilot_summary.md`: seed, mean accuracy, median RT, mean RT-SD (computed from the bot output).

### Step 5 — (Optional) Human-subject pilot

Only if reviewer response requires real human data. Re-run Step 4 with `agentMode` removed and recruit n = 5 lab members or Prolific opt-ins, all with `seed=42` for reproducibility. Requires the ethics decision in [`tasks.md`](./tasks.md) Phase A to be resolved first.

## 4. Ethics

**Recommended path:** Step 4 only, bot mode. Bot runs are not human-subject research and require no IRB. They exercise the entire round-trip and produce a valid trials CSV; §2.6 prose would note that the pilot is a bot validation. This is enough to land §2.6 in the first submission. Queue Step 5 as a strengthening if reviewers ask.

## 5. What §2.6 becomes after the runbook lands

The two `[GAP]` markers in §2.6 are resolved:

- The "pilot data + runner-state screenshots" GAP (currently `[GAP: actual pilot data (n participants, seed, summary accuracy and median RT) and runner-state screenshots …]`) is replaced with one line: `bot-mode validation with seed=42; accuracy 0.XX, median RT YYY ms; runner-state composite in Figure 4`.
- The Figure 4 `[GAP]` reference is resolved by the Step 4 deliverables.

The CogEnv paragraph and the two-encoding clarification are already in §2.6 and need no further edits.

## 6. Effort summary

| Item | Effort | Owner | Status |
|---|---|---|---|
| Bot-mode round-trip (Steps 1–4) | 2 h | Morteza | pending |
| Figure 4 composite assembly | 2 h | Hoorieh | depends on Step 4 |
| §2.6 prose two-encoding edit | — | Morteza | **done** |
| §2.6 CogEnv paragraph | — | Morteza | **done** |
| (Optional) human-subject pilot (Step 5) | half-day + ethics wait | Hoorieh + Pedro | decision-gated |

**Total to a submittable §2.6:** ≈ 1 day (bot-mode path) or ≈ 1 week (with human pilot).
