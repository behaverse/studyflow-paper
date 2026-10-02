"""Give fig-consort and fig-overview the state and records of the current planted pipeline-check run
(`../study/pipeline-check/run-planted/planted.studyflow.yaml`), so they show the run fig-combined draws.

fig-consort takes the run's `state:` block as it is. fig-overview takes it too, each of its elements takes the run's
records of the element with the same id, and each flow its compaction draws takes the count of the path it stands
for. Both are then written in the modeler's own spelling.

Run it from the figures folder, with these scripts restored in `src/`, then re-render both figures:

    python3 src/overview-history.py ../study/pipeline-check/run-planted/planted.studyflow.yaml src

It replaces the two-run merge it used to be (the 2026-09-29 run and its faulty re-run).
"""
import copy, subprocess, sys, tempfile
from pathlib import Path
import yaml

CLI = str(Path(__import__("os").environ.get("MODELER", "../../studyflow-modeler")) / "packages/cli/dist/studyflow.mjs")
PROV = "prov:Activity"
# fig-overview's compact flows, each with the run's flow it stands for (its first one, where it stands for a path)
COMPACT = {
    "Flow_Enroll_Screening": "SF_Start_Screening", "Flow_Screening_Eligibility": "SF_Screening_Eligibility",
    "Flow_Cautious_Interference": "SF_Cautious_Merge", "Flow_Impulsive_Interference": "SF_Impulsive_Merge",
    "Flow_Interference_WorkingMemory": "SF_Interference_WorkingMemory", "Flow_Failed_Interference": "SF_Failed_Interference",
    "Flow_Failed_WorkingMemory": "SF_Failed_WorkingMemory", "Flow_WorkingMemory_End": "SF_WorkingMemory_Debrief",
}


def elements(node, found=None):
    found = {} if found is None else found
    for key, value in (node.items() if isinstance(node, dict) else enumerate(node) if isinstance(node, list) else []):
        if key in ("layout", "state"):
            continue
        if isinstance(value, dict) and "type" in value:
            found.setdefault(key, value)
        elements(value, found)
    return found


def records(element):
    return [e for e in element.get("extensionElements") or [] if isinstance(e, dict) and e.get("type") == PROV]


def write(path, data):
    with tempfile.TemporaryDirectory() as tmp:
        raw, canon = f"{tmp}/raw.studyflow.yaml", f"{tmp}/canon.studyflow.yaml"
        yaml.safe_dump(data, open(raw, "w"), sort_keys=False, allow_unicode=True, width=120)
        subprocess.run(["node", CLI, "convert", raw, canon], check=True, capture_output=True)
        assert yaml.safe_load(open(canon)) == data, path
        Path(path).write_text(Path(canon).read_text())


run = yaml.safe_load(open(sys.argv[1]))
src = Path(sys.argv[2])

consort = yaml.safe_load(open(src / "fig-consort.studyflow.yaml"))
consort["state"] = copy.deepcopy(run["state"])
write(src / "fig-consort.studyflow.yaml", consort)

overview = yaml.safe_load(open(src / "fig-overview.studyflow.yaml"))
ran = elements(run)
for key, element in elements(overview).items():
    kept = [e for e in element.get("extensionElements") or [] if not (isinstance(e, dict) and e.get("type") == PROV)]
    taken = records(ran.get(key, {}))
    if kept or taken:
        element["extensionElements"] = kept + copy.deepcopy(taken)
    elif "extensionElements" in element:
        del element["extensionElements"]
overview["state"] = copy.deepcopy(run["state"])
reached = overview["state"]["_meta"]["reached"]
for flow, stands_for in COMPACT.items():
    if reached.get(stands_for):
        reached[flow] = reached[stands_for]
write(src / "fig-overview.studyflow.yaml", overview)
print("carried", run["state"]["_meta"]["prov"][-1]["run"], "into fig-consort and fig-overview")
