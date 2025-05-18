# studyflow-modeler-paper

Studyflow Modeler Paper


## Setup

You need to install the following dependencies:
- [Quarto](https://quarto.org/docs/get-started/installation/)
- librsvg (only for SVG export)
- PlanetUML (only for EBNF figures)

If you don't have them installed, you can use pixi to install them:
```
pixi shell
quarto preview .
```

## JOSS

To build the JOSS paper, you need to install Docker and run the following command in the root of the project:

```
docker run --rm \
    --volume $PWD/joss:/data \
    --user $(id -u):$(id -g) \
    --env JOURNAL=joss \
    openjournals/inara
```

Output will be saved as `joss/paper.pdf`.