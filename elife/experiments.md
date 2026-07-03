# Experiment runbook for the Studyflow paper (eLife)

Instructions for the experimenter running the example study. Everything the
manuscript ([paper-v2.qmd](paper-v2.qmd)) reports must come out of the work
packages below. Two rules govern all of them:

1. **Every value currently in the manuscript's results is an invented
   placeholder** (the agent table, the human congruency costs, the attrition
   counts 1/9/3). Replace them with what the runs produce. If the data
   disagree with any prose claim, **rewrite the prose to match the data** —
   never the reverse. Placeholders are marked `[TODO]` in the manuscript;
   grep for `TODO` to find them all.
2. **Everything must be produced BY running the deposited `.studyflow` file**,
   not assembled by hand. The paper's central claim is that the protocol, the
   runs, the analysis, and the figures are one artifact; any number that
   bypasses the file breaks that claim.

Work packages are ordered by dependency. WP1 blocks everything.

---

## WP1 — Register the protocol

**Do:** finalize the example study's `.studyflow` file and deposit it (OSF or
equivalent) BEFORE any runs, with attrition counts empty.

- Confirm the registered file carries: consent document reference on the start
  event; eligibility criteria on the eligibility gateway; the allocation rule on
  the randomization gateway; per-task parameters; the analysis nodes with their
  margins, alpha levels, and thresholds; the failed-trial exit threshold; and
  the study seed policy.
- Two design constants appear in the manuscript as registered values —
  **failed-trial exit threshold 20%** and **k = 30 runs per condition**. Either
  make the registered file match, or correct the manuscript (Results, "Run" and
  "Failure is data").
- Also register (as extensions, not results): the larger factorial (further
  open-weight models, fatigued and fast-but-error-prone personas, all six
  battery tasks).
- Export the protocol as SVG with the source embedded.

**Deliverables → manuscript locations:**
- OSF/registry link → Results "Design" `[TODO: OSF link]`
- Registered file + SVG → deposit (WP8)

## WP2 — Agent cohort

**Design (must match the registered file):** 3 agent families × trait × 2 tasks
(N-back, Flanker) × 2 timing paths, k = 30 runs per condition.

- Families: uniform random baseline (no trait); one open-weight LLM served
  locally through Ollama; one commercial vision-language model reading rendered
  screenshots.
- Traits (LLM and VLM only): baseline (no trait prompt) vs "careful" persona.
  Trait prompts name a disposition, never a target accuracy. Version the
  prompts.
- Time pressure: enforced response window is expressed per family (deadline in
  the prompt for language models). Agents run the full factorial (no random
  allocation).
- Each run uses a distinct derived subject identifier under the registered
  study seed. The runner must record the seed log.

**Pin per run (enrollment record):** model identifier and version (content
digest + quantization for the open-weight model; provider snapshot identifier
for the commercial model), sampling parameters, versioned trait prompt, context
policy (accumulation and truncation across trials/tasks), frame resolution for
vision input.

**Record per trial:** observation sent, raw reply, parsed response, failure
mode where parsing failed (invalid / timeout / refusal), latency and its source.
No imputation: out-of-vocabulary replies are stored raw and flagged. Runs
crossing the failed-trial threshold must exit through the boundary error events
(they are attrition, not deletions).

**Deliverables → manuscript locations:**
- Complete agent trials table (BDM / Psych-DS compatible) → deposit
- Per-condition accuracy, median RT, failed-trial rate (self-paced path) →
  Results table `@tbl-agents` (10 rows; all current values are placeholders)
- The time-pressured path's table ships with the deposit
- Executor configurations + trait prompts + seed log → deposit

## WP3 — Human participants

**Do:** human participants (sample size fixed at registration) complete the
full flow in the runner (consent screen from the start event → screening →
allocation → battery), on the same deposited file, same interface.

- Confirm ethics status first: UniLu ERP / UserLab confirmation or documented
  exemption → Ethics statement `[TODO]`.
- Record recruitment channel, compensation (currently written as "word of
  mouth, uncompensated, ~45-minute sessions" — confirm or correct), and
  aggregate demographics → Methods "Human participants" `[TODO]`.
- Consent must include publication of de-identified data. Release only
  de-identified trials; demographics aggregate-only.
- Note: the manuscript's Listing 3 diff currently implies 3 people were
  screened and 1 excluded. That is a placeholder; the real screening/attrition
  numbers replace it (WP6).

**Deliverables:** de-identified human trials table → deposit; per-participant
Flanker congruency costs → WP4.

## WP4 — Prespecified analyses

Run the three analyses AS THE TYPED NODES IN THE FILE (they are the
preregistration); implementations may live behind `studyflow:uses` but the
margins, levels, and thresholds come from the registered nodes.

1. **Marker** — Flanker congruency effect: within-subject accuracy and RT cost,
   incongruent vs congruent, per subject. Fill:
   - each human participant's RT and accuracy costs → Results paragraph
     ([TODO: per-participant estimates])
   - per-family agent estimates and their direction
2. **Agreement** — TOST equivalence of accuracy between two conditions within
   the prespecified margin. Document how the margin was justified from the
   battery's test-retest variability (the manuscript asserts this).
3. **Divergence** — classifier AUC (subject-grouped cross-validation) vs
   permutation chance.

**Integrity check:** the manuscript deliberately reports the analyses as
estimates without characterizing patterns; keep it that way. If you add any
pattern statement, it must come from the executed runs, not expectation.

**Deliverables:** filled Results paragraph + `@tbl-agents`; Figure 5 (generated
chart handed to the designer, see [figures.md](figures.md)); analysis outputs
in the deposit.

## WP5 — Validator demonstrations

**Do:** in a COPY of the deposited file, introduce two faults and capture the
validator's verbatim messages:

1. A participant-flow inconsistency (make inflow != outflow + attrition at one
   activity) → expect a flow-consistency error naming the activity.
2. An analysis node reading a column its upstream schema does not define →
   expect a data-contract error naming the column and the closest match.

Replace the two constructed `ERROR ...` blocks in Results "Amend and report"
with the exact tool output.

## WP6 — Deviation diff (Listing 3 and Figure 7)

**Do:** after all runs, produce the as-run file and generate the diff against
the registered file MECHANICALLY (`git diff` or equivalent).

- Expected content: only run-time values (attrition counts) on elements that
  declared them at registration. If anything else changed, that is a real
  deviation — report it, do not clean it.
- Replace Listing 3's diff (current counts 1/9/3 are placeholders).
- Tell the graphic designer the real counts: Figure 7's bottom panel shows
  them (see [figures.md](figures.md)).

## WP7 — Reproducibility and toolkit checks

1. **Determinism:** run the full walk for a fixed (file, seed, subject) in two
   browsers on two machines; require bit-identical visited-node sequences and
   trial records. Record the release tag and both environments → Methods
   "Reproducibility test" `[TODO]`.
2. **Amendment stability:** insert a node upstream; verify every untouched
   downstream element's draws are bit-identical.
3. **Confirm or correct three tooling claims** (Methods `[TODO]`s):
   runner checkpoint granularity; allocation concealment mechanics for the
   human participants; whether the SVG round-trip test exists.
4. Confirm the runner records the GUIDE-LLM consensus checklist's core items in
   machine-readable form (claimed in the Discussion).

## WP8 — Deposit and identifiers

Assemble the research-object package (RO-Crate):

- registered `.studyflow` + as-run `.studyflow` + the mechanical diff
- exported figure SVGs with embedded sources
- de-identified human trials table; complete agent trials table
- seed log; executor configurations; versioned trait prompts
- time-pressured path results table
- the complete machine-readable guideline mapping (Supplementary Table S2:
  CONSORT/SPIRIT for the human cohort; CHART primary for the agent cohort,
  merged with the overlapping CONSORT-AI/SPIRIT-AI items, numbers verified)

Then mint identifiers and fill the manuscript's remaining `[TODO]`s:
Zenodo DOIs for modeler/runner/schemas releases; deposit DOI; preregistration
template DOI; MDAR Key Resources Table (RRIDs + DOIs); CRediT roles; AI-usage
disclosure; CONSORT 2025 figure redraw license (Figure 3a).

---

## Acceptance checklist (what "done" means)

- [ ] Registered file deposited before any run; OSF link in manuscript
- [ ] 20% threshold and k = 30 verified against the registered file
- [ ] All `@tbl-agents` values, human congruency costs, and the
      agreement/divergence sentence replaced with real estimates
- [ ] Prose claims re-checked against data ("profiles order as expected",
      "ordering preserved" on the timed path) and corrected where wrong
- [ ] Listing 3 diff and Figure 7 counts regenerated mechanically
- [ ] Both validator messages captured verbatim
- [ ] Determinism + amendment-stability checks passed and pinned
- [ ] Human participants' ethics, recruitment, and consent text confirmed
- [ ] Deposit complete, DOIs minted, zero `TODO` left in
      [paper-v2.qmd](paper-v2.qmd)
