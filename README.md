# studyflow-modeler-paper

Studyflow Modeler Paper


## Setup

You need to install the following dependencies:
- [Quarto](https://quarto.org/docs/get-started/installation/)

If you don't have them installed, you can use uv:
```
uv run quarto render . --to pdf
```

The output will be saved as `_manuscript/studyflow_modeler_paper.pdf`.

## JOSS

There is an alternative, and shorter, version of the paper that is formatted for the Journal of Open Source Software (JOSS). This version includes additional metadata and is structured to meet JOSS requirements.

To build the JOSS version, you need to install Docker and run the following command in the root of the project:

```
docker run --rm \
    --volume $PWD/joss:/data \
    --user $(id -u):$(id -g) \
    --env JOURNAL=joss \
    openjournals/inara
```

Output will be saved as `joss/paper.pdf`.