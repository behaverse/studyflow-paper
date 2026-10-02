# eLife manuscript

`quarto render elife` (from the repository root) builds `paper-v3.qmd` into `_manuscript/`, as `_quarto.yml` says.

| Path | What |
|:--|:--|
| `paper-v3.qmd` | the manuscript |
| `cover-letter.md` | the cover letter |
| `UBIQUITOUS_LANGUAGE.md` | the terms the paper uses, one meaning each |
| `references.bib` | the bibliography |
| `figures/` | the cited figures, each with the Studyflow diagram it shows ([README](figures/README.md)) |
| `study/` | the example study, its runs and the material the Results report ([README](study/README.md)) |
| `_extensions/elife/` | the eLife template, class and bibliography style |

The rewrite `paper-v4.qmd`, the Google Doc mirror scripts, the figure-building scripts and the uncited figures are in
`../archived/elife/`.
