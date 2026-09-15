# Figure sources

Hand-written `.studyflow.yaml` files for the manuscript figures, and the scripts
that turn them into the `fig-*.studyflow.png` files one level up.

| Source | Figure | Notes |
|---|---|---|
| `fig-step1-design.studyflow.yaml` | `@fig-step1-design` | Enrolment and allocation lanes; counted exits declare `count` properties; `state:` deposited at zero |
| `fig-step2-run.studyflow.yaml` | `@fig-step2-run` | Collaboration: the runner's battery exchanges `behaverse:Trial`/`behaverse:Response` messages with four actor pools (`studyflow:Actor`); a trait prompt (`agentic:Prompt`) wired into the battery |
| `fig-step2-nback.studyflow.yaml` | `@fig-step2-nback` panel b | Trial subprocess with loop marker, boundary timer, ISI timer, `Parameters`; the same block as one `behaverse:Task` with its `Parameters` wired in |
| `fig-step3-analyze.studyflow.yaml` | `@fig-step3-analyze` | Analysis phase in three rows: service tasks with `implementation`, typed tables between them, `Parameters` for thresholds, counted analysis exclusion, gateway over the three analyses |
| `fig-step4-report.studyflow.yaml` | `@fig-step4-report` | Render, debrief, completion end event with `redirectTo` |
| `fig-combined.studyflow.yaml` | `@fig-combined`; panel a of `@fig-views` | The whole study with `state:` after a run (`{count}`, `{reached}`, `_meta.prov`) |
| `fig-consort.studyflow.yaml` | `@fig-consort` panel b; panel e of `@fig-views` | The combined study with both subprocesses collapsed, on one centre line with the exits in a column |
| `fig-consort-reference.svg` | `@fig-consort` panel a | The CONSORT 2025 flow template, hand-drawn; `panel.py` rasterizes it |
| `fig-step2-nback-classic.svg` | `@fig-step2-nback` panel a | The slide-style N-back figure, hand-drawn; `panel.py` rasterizes it |
| `figS1-multimodal.studyflow.yaml` | `@fig-s1-multimodal` | EEGPrep and fMRIPrep as the `eeg` skill's service-task templates, BDM datasets as `behaverse:BDMDataset` |

`@fig-elements` is the modeler's own `skills/studyflow/examples/kitchensink.studyflow.yaml` rendered with `render.mjs`;
`@fig-views` panels b to d are captures of the modeler's Gantt, Checklist and
Provenance dialogs (`views.mjs`), composed by `compose_views.py` with panel a, the battery cropped from
`fig-combined`, and panel e, `fig-consort`. `@fig-s2-modeler` is `modeler.mjs`'s annotated screenshot.

## Conventions

- Cognitive tasks are choreography tasks (`type: ChoreographyTask` with a `behaverse:Task` or `cognitive:CognitiveTask` inside); their settings are a `studyflow:Parameters` data object wired into them. `seed` sits on `studyflow:Study`.
- Lay a figure out for the one print scale, 1 unit = 0.175 mm: at most about 1030 units wide (the 180 mm column) and short enough to leave its caption room. Labels are 11–12 units, so they print at 5.5–6 pt. Give a task room for its name clear of its boundary events (140 × 80 holds three lines).
- Nodes carry absolute `bounds`. Flows may omit `waypoint`; `layout.py` fills in an orthogonal route (a hand-written `waypoint` wins). `A -> B` shorthand is fine.
- Attrition exits: `fill: "#f1d0cd"`, `stroke: "#ac5a54"`, and `stroke` on their flows.
- Labels are auto-placed unless a `label:` box is given; give one where the default collides.
- Post-run figures carry a `state:` block; deposited figures carry the same block at zero, so labels read `n=0` rather than `n={count}`.

## Rendering

```sh
MODELER=~/workspace/behaverse/studyflow-modeler ./render.sh fig-step1-design
```

`render.sh` needs the modeler checkout with `npm ci`, `npx playwright install chromium`
and the CLI built. It writes the PNG, the studyflow embedded in it as the modeler spells it, with a `pHYs` chunk giving its print size. A figure that fills a page at a scale of its own sets `MM_PER_UNIT` (`fig-combined`: 0.154).
Icons are served from the local `@iconify/json` package, so no network is needed.
