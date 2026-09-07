# Figure sources

Hand-written `.studyflow` files for the manuscript figures, and the scripts
that turn them into the `fig-*.studyflow.png` files one level up.

| Source | Figure | Notes |
|---|---|---|
| `fig-step1-design.studyflow` | `@fig-step1-design` | Enrolment and allocation lanes; counted exits declare `count` properties; `state:` deposited at zero |
| `fig-step2-run.studyflow` | `@fig-step2-run` | Collaboration: the runner's battery exchanges observation/response messages with four actor pools (`cognitive:Actor`) |
| `fig-step2-nback.studyflow` | `@fig-step2-nback` panel b | Trial subprocess with loop marker, boundary timer, ISI timer, `Parameters`; the same block as one `BehaverseTask` |
| `fig-step3-pipeline.studyflow` | `@fig-step3-pipeline` | Service tasks with `implementation`, typed tables between them, `Parameters` for thresholds |
| `fig-step3-analyze.studyflow` | `@fig-step3-analyze` | Analysis phase: counted analysis exclusion, gateway over the three analyses |
| `fig-step4-report.studyflow` | `@fig-step4-report` | Render, debrief, completion end event with `redirectTo` |
| `fig-combined.studyflow` | `@fig-combined`; panel a of `@fig-views` | The whole study with `state:` after a run (`{count}`, `{reached}`, `_meta.prov`) |
| `fig-consort.studyflow` | `@fig-consort` panel b; panel e of `@fig-views` | The combined study with both subprocesses collapsed |
| `figS1-multimodal.studyflow` | `@fig-s1-multimodal` | Extracted from the old PNG; still uses the retired `functional:` namespace and needs redrawing against `eeg` |

`@fig-elements` is the modeler's own `kitchensink.studyflow.png` re-rendered;
`@fig-views` panels b to d are captures of the modeler's Gantt, Checklist and
Provenance dialogs (`views.mjs`), composed by `compose_views.py`.

## Conventions

- Nodes carry absolute `bounds`. Flows may omit `waypoint`; `layout.py` fills in an orthogonal route (a hand-written `waypoint` wins). `A -> B` shorthand is fine.
- Attrition exits: `fill: "#f1d0cd"`, `stroke: "#ac5a54"`, and `stroke` on their flows.
- Labels are auto-placed unless a `label:` box is given; give one where the default collides.
- Post-run figures carry a `state:` block; deposited figures carry the same block at zero, so labels read `n=0` rather than `n={count}`.

## Rendering

```sh
MODELER=~/workspace/behaverse/studyflow-modeler ./render.sh fig-step1-design
```

`render.sh` needs the modeler checkout with `npm ci`, `npx playwright install chromium`
and the CLI built. It writes the PNG (studyflow embedded) and an SVG next to it.
Icons are served from the local `@iconify/json` package, so no network is needed.
