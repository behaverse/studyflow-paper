# ToDo

## Deferred: the seed-42 experiment run, then populate the manuscript

The paper now reads as a collected study. The actual run, analysis, and figure
rendering are deferred to here; the data-dependent numbers are marked in
`paper.qmd` with `[FILL: ...]` tokens (grep for `[FILL`).

Prerequisites (checked on this machine):

- Modeler deps installed; Unity WebGL build present at `../assessment-unity/Build/WebGL`.
- `claude` CLI present: authenticate, then start the proxy (`node tools/claude-proxy`).
- `ollama` running, but no model pulled yet: `ollama pull <vision model>`. The bot
  diagrams reference `gemma4:e2b-mlx`; pull it or swap to e.g. `llama3.2-vision`.
- `python3` present (pandas, matplotlib). `Rscript` is NOT installed; do the analysis
  in Python (the dplyr block stays the illustrative panel of Figure 8).

Run the panel (matches §2.6: model x trait x task at seed 42):

- [ ] Start the dev server: `npm run dev` (serves `run.html` at :5173).
- [ ] Drive `run.html?studyflow_url=...&seed=42` headlessly via Playwright over
      `bot_external.studyflow` (random baseline), `bot_ollama.studyflow` (open-weight),
      `bot_claude.studyflow` (commercial), and the full `example.studyflow`.
- [ ] Capture trials: there is no local CSV export, so intercept the `.../events` POST
      payloads and write a trials CSV (BDM trials schema).
- [ ] Capture the runner walkthrough screenshots for Figure 4 (consent -> instruction ->
      questionnaire -> task -> end).

Analyze and render figures (drop into `figures/` at 88 mm / 180 mm):

- [ ] Python (pandas): accuracy (mean `correct`), median RT, and random-fallback rate by
      model x trait x task -> Table 3 + Figure 13.
- [ ] Figure 8 left panel: export SVG from `elife/rt_analysis.studyflow` (open in the
      modeler, *File > Export*); pair with the dplyr block (right panel). The diagram was
      authored in this pass.
- [ ] Figures 6 (CONSORT), 7 (n-back slide / Studyflow / XML), 12 (three runtimes): export
      SVG from `consort2025.studyflow` / `example.studyflow` and compose.

Populate the `[FILL: ...]` tokens in `paper.qmd`:

- [ ] §2.3: Figure 4 runner screenshots.
- [ ] §2.6: the trait set and the prior studies it is grounded in; Table 3 values; Figure 13;
      the observed open- vs closed-weight pattern.
- [ ] §2.7: summary RT values.
- [ ] Finalize the AI roster: the model set (Claude + chosen open-weight Ollama models) and
      the trait/persona set grounded in prior cognitive-science / psychology work.
- [ ] Reconcile the human arm with the real dataset (`P500_9subjects`; the text currently
      says "ten participants" and the six-task Behaverse battery).

## Other (pre-existing)

- [ ] Add the CONSORT 2025 checklist to `example.studyflow`.
- [ ] Data and code availability statement: link to repo URLs.
- [ ] Decision figure (optional): a diagram or decision tree to pick the right element via
      three orthogonal questions.
- [ ] Zotero: verify the 19 `%!VERIFY` entries.
- [ ] Reporting-guideline templates beyond CONSORT/SPIRIT (the Table 2 "Roadmap" rows);
      STROBE and PRISMA next.
