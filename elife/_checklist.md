# ToDo

## Deferred: the seed-42 experiment run, then populate the manuscript

The paper is framework-forward; the worked study (§3) is a *demonstration*. The actual
run, analysis, and figure rendering are deferred to here; the data-dependent numbers are
marked in `paper.qmd` with `[FILL: ...]` tokens (grep for `[FILL`; 12 of them).

Prerequisites (checked on this machine):

- Modeler deps installed; Unity WebGL build present at `../assessment-unity/Build/WebGL`.
- `claude` CLI present: authenticate, then start the proxy (`node tools/claude-proxy`).
- `ollama` running, but no model pulled yet: `ollama pull <vision model>`. The bot
  diagrams reference `gemma4:e2b-mlx`; pull it or swap to e.g. `llama3.2-vision`.
- `python3` present (pandas, matplotlib). `Rscript` is NOT installed; do the analysis
  in Python (the dplyr block stays the illustrative panel of Figure 10).

Run the cohort (§3.2: model x trait x task at seed 42):

- [ ] Start the dev server: `npm run dev` (serves `run.html` at :5173).
- [ ] Drive `run.html?studyflow_url=...&seed=42` headlessly via Playwright over
      `bot_external.studyflow` (random baseline), `bot_ollama.studyflow` (open-weight),
      `bot_claude.studyflow` (commercial), and the full `example.studyflow`.
- [ ] Capture trials: there is no local CSV export, so intercept the `.../events` POST
      payloads and write a trials CSV (BDM trials schema).
- [ ] Capture the runner walkthrough screenshots for Figure 4 (consent -> instruction ->
      questionnaire -> task -> end).

Analyze and render figures (drop into `figures/` at 88 mm / 180 mm):

- [ ] Python (pandas): accuracy (mean `correct`), median RT, and out-of-set fallback rate by
      model x trait x task -> `@tbl-agents` + Figure 9.
- [ ] Figure 10 left panel: export SVG from `elife/rt_analysis.studyflow` (open in the
      modeler, *File > Export*); pair with the dplyr block (right panel).
- [ ] Figures 6 (CONSORT), 7 (n-back slide / Studyflow / XML), 12 (SPIRIT three views): export
      SVG from `consort2025.studyflow` / `example.studyflow` / `spirit2025.studyflow` and compose.
      (Figure 8, the executor schematic, is hand-drawn and already drafted.)

Populate the `[FILL: ...]` tokens in `paper.qmd`:

- [ ] §2.3: Figure 4 runner screenshots.
- [ ] §3.2: `@tbl-agents` values (accuracy, median RT, out-of-set fallback rate per cell);
      Figure 9; the observed open- vs closed-weight pattern.
- [ ] §3.3: summary RT values and per-construct agreement.
- [ ] Finalize the AI roster: the model set (Claude + chosen open-weight Ollama models) and
      the trait/persona set grounded in prior cognitive-science / psychology work.
- [ ] Reconcile the human arm with the real dataset (`P500_9subjects`; the text currently
      says "ten participants" and the six-task Behaverse battery).

## Other (pre-existing)

- [ ] Add the CONSORT 2025 checklist to `example.studyflow`.
- [ ] Code and data availability: confirm repo URLs and tagged versions.
- [ ] MIT LICENSE file on the `studyflow-modeler` repo (claimed in §1.5 / Code-and-data).
- [ ] Prune the 8 now-unused references after the §3.2 "Beyond one participant" shrink
      (`sebanz2006joint`, `babiloni2014hyperscanning`, `hakim2023interbrain`, `kothe2025lsl`,
      `dahlback1993woz`, `aher2023llms`, `binz2023gpt3`, `park2023agents`).
- [ ] Zotero: verify the `%!VERIFY` entries in `references.bib`.
- [ ] Reporting-guideline templates beyond CONSORT/SPIRIT (the `@tbl-guidelines` "Roadmap" rows);
      STROBE and PRISMA next.
