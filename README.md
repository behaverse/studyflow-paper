# studyflow-paper

Studyflow Paper


## Setup

You can use [uv](https://docs.astral.sh/uv/) to automatically set up the environment and generate the pdf file:

```
uv run quarto render . --to pdf
```

The output will be saved as `_manuscript/studyflow_modeler_paper.pdf`.


To preview the paper in HTML format, you can run:

```
uv run quarto preview .
```

## JOSS

There is an alternative, and shorter, version of the paper that is formatted for the Journal of Open Source Software (JOSS). This version includes additional metadata and is structured to meet JOSS requirements.

To build the JOSS version, you need to install Docker and run the following command in the root of the project:

```
docker run --rm --volume $PWD/joss:/data --env JOURNAL=joss openjournals/inara
```

Output will be saved as `joss/paper.pdf`.