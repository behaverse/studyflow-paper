#!/usr/bin/env python3
"""Write the text of paper-v3.qmd as the coauthors' Google Doc holds it: one Markdown file per Doc tab.

    python3 elife/doc-sync.py            # writes elife/_manuscript/doc-mirror/{main-text,supplementary,figures,code-listings,tables}.md

The Doc "Studyflow Paper (eLife)" has five tabs: Main Text, Supplementary, Figures, Code Listings, Tables. Each tab
gets two files: `<tab>.md`, the text, and `<tab>.html`, the same rendered for pasting. To update a tab, open the
.html in a browser, select all, copy, and paste into the tab with a plain paste (Cmd+V): headings, emphasis, tables
and code blocks (monospace, indentation kept as non-breaking spaces) come through, which Docs' "Paste from Markdown"
does not manage for fenced code. Images are not carried; the .html shows each figure's file name in its place. HTML comments (the qmd's private notes) are left out; Quarto's fenced divs (`:::`) are dropped and image
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
body = re.sub(r"^\{\{<.*?>\}\}\n?", "", body, flags=re.M)      # shortcodes (page breaks)
body = re.sub(r"^!\[(.*)\]\((figures/[^)]+)\)(\{[^}]*\})?\s*$", r"[\2]\n\1", body, flags=re.M)  # images

body = re.sub(r"^\\(clearpage|newpage)\s*$\n?", "", body, flags=re.M)         # raw LaTeX page breaks
# a table's caption line (": text {#tbl-x}") becomes a paragraph under the table, which a paste keeps; a <caption> is dropped
body = re.sub(r"^: (.*?)[ \t]*\{#(tbl-[\w-]+)\}[ \t]*$", r"**Table \2.** \1", body, flags=re.M)
# a listing's caption (the fence's lst-cap) likewise, after its code block
def _lst(m):
    head, cap, code = m.group(1), m.group(2), m.group(3)
    lang = re.search(r"\.(\w+)", head); lbl = re.search(r"#(lst-[\w-]+)", head)
    return "```" + (lang.group(1) if lang else "") + "\n" + code + "```\n\n**Listing " + (lbl.group(1) if lbl else "") + ".** " + cap.replace('\\"', '"') + "\n"
body = re.sub(r"^```\{([^}]*?)lst-cap=\"((?:[^\"\\]|\\.)*)\"[^}]*\}\n(.*?)^```\n", _lst, body, flags=re.M | re.S)
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
# the rendered copies, for pasting: pandoc (quarto's) writes the HTML; citations and $math$ stay literal text
import subprocess, html as _html
CSS = ("body{font:11pt/1.5 Arial,sans-serif;max-width:52em;margin:2em auto}h1{font-size:20pt}h2{font-size:16pt}h3{font-size:13pt}"
       "pre,code{font-family:'Roboto Mono','Courier New',monospace;font-size:9pt}pre{white-space:pre-wrap;background:#f6f6f6;padding:.5em}"
       "table{border-collapse:collapse;margin:1em 0}td,th{border:1px solid #999;padding:3px 6px;vertical-align:top;font-size:10pt}th{background:#eee}")
for f in sorted(out.glob("*.md")):
    r = subprocess.run(["quarto", "pandoc", "-f", "markdown-tex_math_dollars-citations-raw_html-raw_tex", "-t", "html", "--wrap=none", "--no-highlight", str(f)], capture_output=True, text=True)
    if r.returncode: print(f.name, "pandoc failed:", r.stderr[:200]); continue
    body = re.sub(r"<pre([^>]*)><code([^>]*)>(.*?)</code></pre>", lambda m: "<pre" + m.group(1) + ">" + re.sub(r"(?m)^( +)", lambda k: "\u00a0" * len(k.group(1)), m.group(3)) + "</pre>", r.stdout, flags=re.S)
    body = re.sub(r"<span class=\"math inline\">\\\((.*?)\\\)</span>", r"$\1$", body)
    (out / (f.stem + ".html")).write_text("<!doctype html><meta charset=utf-8><title>" + f.stem + "</title><style>" + CSS + "</style>\n" + body)
    print(f"{f.name}: {len(f.read_text().split())} words; {f.stem}.html: {body.count('<pre')} code blocks, {body.count('<table')} tables")
