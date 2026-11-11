# Studyflow paper: supplementary materials

Materials of the paper "Studyflow: an executable visual notation for designing, running, and reporting experimental studies".

| Folder | What it holds |
| --- | --- |
| `studyflows/yaml/` | The example study, one Studyflow file per agent (Gemma 4 E2B, Gemma 4 E4B, d1 3B, simulated). The history of a file shows what its run added. |
| `studyflows/png/` | The same diagrams as images, each carrying its Studyflow file. |
| `runs/` | The run of each model cohort: the executed diagram, the run's record and log, the trial data and the results. |
| `replays/` | A second run of the two Gemma cohorts. |
| `tests/` | `checks/`: the example study run with simulated agents whose outcomes are known in advance, each with its run and its replay. `faults/`: a small study and twelve copies of it, each with one planted deviation. |
| `paper/` | The Quarto source of the manuscript. |
