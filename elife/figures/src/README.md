# Figure sources

Hand-written `.studyflow.yaml` files for the manuscript figures, and the scripts
that turn them into the `fig-*.studyflow.png` files one level up.

| Source | Figure | Notes |
|---|---|---|
| `fig-step1-design.studyflow.yaml` | `@fig-step1-design` | Enrolment and allocation lanes; the arms are the two dispositions (cautious, impulsive) as `cognitive:Instruction` tasks; counted exits declare `count` properties; `state:` deposited at zero |
| `fig-step2-run.studyflow.yaml` | `@fig-step2-run` | Collaboration: the runner's battery exchanges `behaverse:Trial`/`behaverse:Response` messages with four actor pools (`studyflow:Actor`, named by model: Llama 3.3 via `ollama://`, Claude Opus 4.8 via `claude://`); the trait prompt (`agentic:Prompt`) wired into the battery; the N-back Parameters label shows the values (N=2, 40 trials, ISI 1.5 s) |
| `fig-step2-nback.studyflow.yaml` | `@fig-step2-nback` panel b | Trial subprocess with loop marker, boundary timer, ISI timer, `Parameters`; the same block as one `behaverse:Task` with its `Parameters` wired in |
| `fig-step3-analyze.studyflow.yaml` | `@fig-step3-analyze` | Analysis phase in three rows: service tasks with `implementation`, typed tables between them (raw, valid, derived, per-run, group), `Parameters` for thresholds, the filter's exclusion checklist, counted analysis exclusion, gateway over the three analyses |
| `fig-step4-report.studyflow.yaml` | `@fig-step4-report` | Render (with its export checklist), debrief, completion end event with `redirectTo` |
| `fig-combined.studyflow.yaml` | `@fig-combined`; the study `views.mjs` captures for `@fig-views` | The whole study with `state:` after a run (`{count}`, `{reached}`, `_meta.prov` naming the authors, the CLI version and the run repository) |
| `fig-consort.studyflow.yaml` | `@fig-consort` panel b | The combined study with both subprocesses collapsed, on one centre line with the exits in a column, 580 units wide for its 62% panel |
| `fig-consort-reference.svg` | `@fig-consort` panel a | The CONSORT 2025 flow template, hand-drawn; `render.sh` rasterizes it at 0.185 mm/unit |
| `fig-step2-nback-classic.svg` | `@fig-step2-nback` panel a | The slide-style N-back figure, hand-drawn; `render.sh` rasterizes it at 0.185 mm/unit |
| `figS1-multimodal.studyflow.yaml` | `@fig-s1-multimodal` | EEGPrep and fMRIPrep as the `eeg` skill's service-task templates, BDM datasets as `behaverse:BDMDataset` |

`@fig-elements` is the modeler's own `skills/studyflow/examples/kitchensink.studyflow.yaml` rendered with `render.mjs` (`MM_PER_UNIT=0.115`).
`@fig-views` is `views.mjs`'s captures of the modeler's Gantt, Checklist and Provenance dialogs for `fig-combined`,
composed by `compose_views.py`: the Gantt chart across the page, the provenance log under it, the checklist cards
in two columns. `@fig-s2-modeler` is `modeler.mjs`'s annotated screenshot of Step 2.

## Conventions

- Cognitive tasks are choreography tasks (`type: ChoreographyTask` with a `behaverse:Task` or `cognitive:CognitiveTask` inside); their settings are a `studyflow:Parameters` data object wired into them. `seed` sits on `studyflow:Study`.
- Lay a figure out for the one print scale, 1 unit = 0.2 mm: at most 900 units wide (the 180 mm figure width) and short enough to leave its caption room on the page (about 950 units). Labels are 11–12 units, so they print at 6.2–6.8 pt. Give a task room for its name clear of its boundary events (140 × 80 holds three lines; 170 × 80 keeps a two-line name above a bottom-corner boundary event).
- Nodes carry absolute `bounds`. Flows may omit `waypoint`; `layout.py` fills in an orthogonal route (a hand-written `waypoint` wins). `A -> B` shorthand is fine.
- Colour by step (`colorize.py <file> <design|run|analyze|report|by-id> [--pools]`, idempotent): flow nodes get their step's `fill`/`stroke`, an expanded subprocess the lighter container fill; data objects, stores, boundary events, pools and groups stay plain. `by-id` is for the combined study and its CONSORT view, where the step follows the element id and its nesting.
- Attrition exits: `fill: "#f1d0cd"`, `stroke: "#ac5a54"`, and `stroke` on their flows.
- Labels are auto-placed unless a `label:` box is given; give one where the default collides. An external label takes its element's stroke colour.
- Post-run figures carry a `state:` block; deposited figures carry the same block at zero, so labels read `n=0` rather than `n={count}`.

## Rendering

```sh
MODELER=~/workspace/behaverse/studyflow-modeler ./render.sh fig-step1-design
MM_PER_UNIT=0.185 MODELER=… ./render.sh fig-consort-reference   # a hand-drawn .svg panel
```

`render.sh` needs the modeler checkout with `npm ci`, `npx playwright install chromium`
and the CLI built. It writes the PNG, the studyflow embedded in it as the modeler spells it, with a `pHYs` chunk giving its print size. A figure that fills a page at a scale of its own sets `MM_PER_UNIT` (`fig-combined`: 0.155).
Icons are served from the local `@iconify/json` package, so no network is needed.

The views composite, from the modeler checkout with `views.mjs` copied next to its `package.json`:

```sh
python3 layout.py fig-combined.studyflow.yaml /tmp/studyflow-figs/fig-combined.studyflow.yaml
node views.mjs /tmp/studyflow-figs/fig-combined.studyflow.yaml /tmp/views && python3 compose_views.py /tmp/views ../fig-views.studyflow.png
```
