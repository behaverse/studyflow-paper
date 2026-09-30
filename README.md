# studyflow paper

This repository contains the files for the paper describing the [studyflow notation and tools](https://behaverse.org/studyflow-modeler). The paper is formatted for submission to eLife as a Tools and Resources article. An earlier, shorter version formatted for JOSS is kept in `joss/`, but JOSS is no longer a target venue.


## eLife

To generate the elife-formatted pdf using Quarto, run the following in the root of the project:

```
quarto render elife
```

This renders the manuscript that `elife/_quarto.yml` names, `elife/paper-v3.qmd`. The output will be saved as `elife/_manuscript/` folder.

## JOSS

There is an earlier, shorter version of the paper that is formatted for the Journal of Open Source Software (JOSS). JOSS was dropped as a venue on 2026-09-26 (`SUBMISSION.md`), so this version is kept for reference and no longer follows the eLife manuscript.

To build the JOSS version, you need to install Docker and run the following command in the root of the project:

```
docker run --rm --volume $PWD/joss:/data --env JOURNAL=joss openjournals/inara
```

Output will be saved as `joss/paper.pdf`.