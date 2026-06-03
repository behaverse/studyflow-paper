# studyflow paper

This repository contains the files for the paper describing the [studyflow notation and tools](https://behaverse.org/studyflow-modeler). The paper is formatted for submission to eLife, with an alternative version formatted for JOSS.


## eLife

To generate the elife-formatted pdf using Quarto, run the following in the root of the project:

```
quarto render elife
```

The output will be saved as `elife/_manuscript/` folder.

## JOSS

There is an alternative, shorter version of the paper that is formatted for the Journal of Open Source Software (JOSS). This version is structured to meet JOSS requirements.

To build the JOSS version, you need to install Docker and run the following command in the root of the project:

```
docker run --rm --volume $PWD/joss:/data --env JOURNAL=joss openjournals/inara
```

Output will be saved as `joss/paper.pdf`.