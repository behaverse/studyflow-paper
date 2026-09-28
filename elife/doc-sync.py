#!/usr/bin/env python3
"""Write the text of paper-v3.qmd as the coauthors' Google Doc holds it: one Markdown file per Doc tab.

    python3 elife/doc-sync.py            # writes elife/_manuscript/doc-mirror/{main-text,supplementary,figures,code-listings,tables}.md

The Doc "Studyflow Paper (eLife)" has five tabs: Main Text, Supplementary, Figures, Code Listings, Tables. Each file
here is that tab's new content, ready to paste over the tab (Edit > Paste from Markdown keeps headings, emphasis and
tables). HTML comments (the qmd's private notes) are left out; Quarto's fenced divs (`:::`) are dropped and image
lines become a bracketed file name above the caption, since a paste carries no images. Everything else is the qmd
text as written, which is what the Doc has always held.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
qmd = (ROOT / "paper-v3.qmd").read_text()
out = ROOT / "_manuscript" / "doc-mirror"; out.mkdir(parents=True, exist_ok=True)

# front matter
fm_end = qmd.index("\n---\n", 4); fm = qmd[4:fm_end]; body = qmd[fm_end + 5:]
def fm_block(key):
    m = re.search(rf"^{key}: \|\n((?:  .*\n?)+)", fm, re.M)
    return re.sub(r"^  ", "", m.group(1), flags=re.M).strip() if m else ""
title = re.search(r'^title: "(.*)"', fm, re.M).group(1)
keywords = re.findall(r"^  - (.+)$", fm[fm.index("keywords:"):fm.index("bibliography:")], re.M)

body = re.sub(r"<!--.*?-->\n?", "", body, flags=re.S)          # private notes
body = re.sub(r"^:::.*\n", "", body, flags=re.M)               # fenced divs
body = re.sub(r"^!\[(.*)\]\((figures/[^)]+)\)(\{[^}]*\})?\s*$", r"[\2]\n\1", body, flags=re.M)  # images

# split at H1 headings
parts = re.split(r"^(?=# )", body, flags=re.M)
sections = {}
order = []
for part in parts:
    if not part.strip(): continue
    head = part.split("\n", 1)[0]
    name = re.sub(r"\s*\{#.*\}\s*$", "", head[2:]).strip()
    sections[name] = part; order.append(name)

tabs = {"figures": ["Figures"], "code-listings": ["Code listings"], "tables": ["Tables"], "supplementary": ["Supplementary materials"]}
taken = {n for names in tabs.values() for n in names} | {"References"}
main = [n for n in order if n not in taken]

front = (f"# {title}\n\n# Abstract\n\n{fm_block('abstract')}\n\n**Keywords.** {', '.join(keywords)}\n\n"
         f"**Impact statement.** {fm_block('impact-statement')}\n\n")
(out / "main-text.md").write_text(front + "".join(sections[n] for n in main))
for file, names in tabs.items():
    (out / f"{file}.md").write_text("".join(sections[n] for n in names if n in sections))
for f in sorted(out.glob("*.md")):
    print(f"{f.name}: {len(f.read_text().split())} words")
