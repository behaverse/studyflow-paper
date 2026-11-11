# Studyflow paper: supplementary materials

Supplementary materials of the paper "Studyflow: an executable visual notation for designing, running, and reporting experimental studies".

| Folder | What it holds |
| --- | --- |
| `studyflows/yaml/` | The example study, one Studyflow file per agent (Gemma 4 E2B, Gemma 4 E4B, d1 3B, simulated). The history of a file shows what its run added. |
| `studyflows/png/` | The same diagrams as images, including its Studyflow document as metadata. |
| `runs/` | The run of each model cohort, including the executed diagram, the provenance and log, the trial data and the results. |
| `replays/` | A second run of the two Gemma cohorts with provenance. |
| `tests/` | `checks/`: the example study run with simulated agents, each with its runs. `faults/`: a small study and twelve copies with one  deviation each. |
| `paper/` | The Quarto source of the manuscript. |
