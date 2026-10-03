# eLife manuscript

`quarto render elife` (from the repository root) builds `paper-v3.qmd` into `_manuscript/`, as `_quarto.yml` says.

| Path | What |
|:--|:--|
| `paper-v3.qmd` | the manuscript |
| `cover-letter.md` | the cover letter |
| `references.bib` | the bibliography |
| `figures/` | the cited figures, each with the Studyflow diagram it shows ([README](figures/README.md)) |
| `study/` | the example study, its runs and the material the Results report ([README](study/README.md)) |
| `_extensions/elife/` | the eLife template, class and bibliography style |

The rewrite `paper-v4.qmd`, the Google Doc mirror scripts, the figure-building scripts and the uncited figures are in
`../archived/elife/`. The figure-building scripts are still needed to re-render the figures after the language-model
runs (`../archived/elife/figure-tools/render.sh`). The planning notes (submission plan, co-author ledger, reviews,
objections plan, wave log, glossary of terms) are in `../archived/notes/`.
