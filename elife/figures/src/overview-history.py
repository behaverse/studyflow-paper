#!/usr/bin/env python3
"""Give `fig-overview.studyflow.yaml` the run history its Provenance view shows: the reported run, then a re-run after
its `Analysis` record was invalidated, which branches there.

The re-run is `../../study/run-2026-10-02-rerun/`: a copy of `../../study/run/` (which stays as the run left it) with
an `invalidated` marker on `Analysis`, run again by the CLI that made the reported run (studyflow-modeler at 39314fe9,
`studyflow-cli/26.9.29`). Its subjects are simulated, so it called no model. That CLI keeps only a re-executed step's
latest record, so each element here gets the records of both repositories, oldest first; `_meta.prov` (the timeline
of runs) is the re-run's, and the counts stay the reported run's, as in `fig-combined` and `fig-consort`. Re-spell
the result with `studyflow convert` afterwards.

    python3 src/overview-history.py && node $MODELER/packages/cli/dist/studyflow.mjs convert \\
        src/fig-overview.studyflow.yaml src/fig-overview.studyflow.yaml
"""
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
STUDY = HERE.parents[1] / 'study'
TARGET = HERE / 'fig-overview.studyflow.yaml'
PROV = 'prov:Activity'


def elements(node, found=None):
    """Every element of a study by id, outside its drawing and its state."""
    found = {} if found is None else found
    for key, value in (node.items() if isinstance(node, dict) else enumerate(node) if isinstance(node, list) else []):
        if key in ('layout', 'state'):
            continue
        if isinstance(value, dict) and 'type' in value:
            found.setdefault(key, value)
        elements(value, found)
    return found


def records(element):
    return [e for e in element.get('extensionElements') or [] if isinstance(e, dict) and e.get('type') == PROV]


run = yaml.safe_load((STUDY / 'run' / 'example_study.studyflow.yaml').read_text())
rerun = yaml.safe_load((STUDY / 'run-2026-10-02-rerun' / 'example_study.studyflow.yaml').read_text())
study = yaml.safe_load(TARGET.read_text())
sources = [elements(run), elements(rerun)]
for key, element in elements(study).items():
    merged = {}
    for source in sources:
        for record in records(source.get(key, {})):
            merged.setdefault((record.get('action'), str(record.get('when')), record.get('run')), record)
    if not merged:
        continue
    kept = [e for e in element.get('extensionElements') or [] if not (isinstance(e, dict) and e.get('type') == PROV)]
    element['extensionElements'] = kept + sorted(merged.values(), key=lambda record: str(record.get('when')))
study['state'] = run['state']
study['state']['_meta']['prov'] = rerun['state']['_meta']['prov']
TARGET.write_text(yaml.safe_dump(study, sort_keys=False, allow_unicode=True, width=120))
print(f'wrote {TARGET.name}')
