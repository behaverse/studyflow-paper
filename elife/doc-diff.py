#!/usr/bin/env python3
"""Show what pasting the Doc mirror would change: an HTML diff, tab by tab, between the Google Doc's current text
and the mirror files doc-sync.py wrote.

    python3 elife/doc-diff.py <doc-export.txt>     # writes elife/_manuscript/doc-mirror/diff.html and diff.txt

<doc-export.txt> is the Doc's text as the Drive connector returns it (read_file_content), with its five tabs as
`# Main Text`, `# Supplementary`, `# Figures`, `# Code Listings`, `# Tables`. Both sides are normalized before the
comparison (the export's backslash escapes and comment anchors removed, bold headings unbolded, smart quotes
straightened, whitespace collapsed), paragraphs are aligned, and changed paragraphs are shown word by word.
"""
import difflib, html, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "_manuscript" / "doc-mirror"
TABS = [("Main Text", "main-text.md"), ("Supplementary", "supplementary.md"), ("Figures", "figures.md"),
        ("Code Listings", "code-listings.md"), ("Tables", "tables.md")]

def norm(text):
    text = re.sub(r"<comment_(start|end)[^>]*>", "", text)
    text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!>|<@$])", r"\1", text)      # the export's escapes
    text = re.sub(r"^(#+) \*\*(.*?)\*\*\s*$", r"\1 \2", text, flags=re.M)   # bold headings
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace(" ", " ")
    text = re.sub(r"\s*\{#[^}]*\}", "", text)                                # Quarto labels, which the Doc does not need
    text = re.sub(r"^\|[\s|:\-]*\|\s*$\n?", "", text, flags=re.M)              # table alignment rows and the empty row the export adds
    text = re.sub(r"^(\|.*)$", lambda m: m.group(1).replace("**", ""), text, flags=re.M)   # bold header cells the export adds
    text = re.sub(r"\[(https?://[^\]]+)\]\((https?://[^)]+)\)", r"<\2>", text)          # auto-links the export writes as [url](url)
    text = re.sub(r"^```.*$\n?", "", text, flags=re.M)                               # code fences
    paras = [re.sub(r"\s+", " ", p).strip() for p in text.split("\n")]   # one unit per line, as the qmd and the export both write
    return [p for p in paras if p]

def split_tabs(doc):
    out = {}
    for name, _ in TABS:
        m = re.search(rf"^# \**{re.escape(name)}\**\s*$", doc, re.M)   # the export may bold a tab title
        if not m: continue
        rest = doc[m.end():]
        nxt = [re.search(rf"^# \**{re.escape(n)}\**\s*$", rest, re.M) for n, _ in TABS if n != name]
        ends = [x.start() for x in nxt if x]
        out[name] = rest[:min(ends)] if ends else rest
    return out

def words(p): return re.findall(r"\S+|\s+", p)

def inline(a, b):
    sm = difflib.SequenceMatcher(None, words(a), words(b), autojunk=False); parts = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        x = html.escape("".join(words(a)[i1:i2])); y = html.escape("".join(words(b)[j1:j2]))
        if op == "equal": parts.append(x)
        elif op == "delete": parts.append(f"<del>{x}</del>")
        elif op == "insert": parts.append(f"<ins>{y}</ins>")
        else: parts.append(f"<del>{x}</del><ins>{y}</ins>")
    return "".join(parts)

doc = pathlib.Path(sys.argv[1]).read_text()
tabs = split_tabs(doc)
css = ("body{font:15px/1.5 -apple-system,Helvetica,Arial,sans-serif;max-width:60em;margin:2em auto;padding:0 1em;color:#1c1917}"
       "h2{margin-top:2em;border-bottom:1px solid #ccc}p{white-space:pre-wrap;margin:.6em 0;padding:.3em .5em;border-left:4px solid #e5e5e5}"
       ".same{color:#777;border-color:#eee}.chg{border-color:#d97706;background:#fffbeb}.fmt{border-color:#a3a3a3;background:#fafafa;color:#555}.add{border-color:#16a34a;background:#f0fdf4}"
       ".del{border-color:#dc2626;background:#fef2f2}del{background:#fecaca;text-decoration:line-through}ins{background:#bbf7d0;text-decoration:none}"
       ".sum{font-family:ui-monospace,Menlo,monospace;font-size:13px}details{margin:.4em 0}summary{cursor:pointer;color:#555}")
parts = [f"<!doctype html><meta charset=utf-8><title>Doc mirror diff</title><style>{css}</style>",
         "<h1>What pasting the mirror changes in the Google Doc</h1><p class=sum>Left/red: the Doc as read on the export's date. Green: the mirror from the current qmd. Grey paragraphs are unchanged (folded); light-grey ones differ only in markup characters (bold, escapes), which the paste changes and the eye does not.</p>"]
txt = []
for name, file in TABS:
    old = norm(tabs.get(name, "")); new = norm((OUT / file).read_text())
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    counts = {"equal": 0, "replace": 0, "insert": 0, "delete": 0}
    body = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            counts["equal"] += i2 - i1
            body.append(f"<details><summary>{i2 - i1} unchanged paragraph(s)</summary>" + "".join(f"<p class=same>{html.escape(p)}</p>" for p in old[i1:i2]) + "</details>")
        elif op == "replace":
            n = max(i2 - i1, j2 - j1); counts["replace"] += n
            for k in range(n):
                a = old[i1 + k] if i1 + k < i2 else None; b = new[j1 + k] if j1 + k < j2 else None
                if a and b:
                    fmt = re.sub(r"[*_`\\\s]", "", a) == re.sub(r"[*_`\\\s]", "", b)
                    counts["format"] = counts.get("format", 0) + fmt
                    body.append(f"<p class={'fmt' if fmt else 'chg'}>{inline(a, b)}</p>"); txt.append(f"[{name}] {'FORMATTING' if fmt else 'CHANGED'}\n- {a}\n+ {b}\n")
                elif a: body.append(f"<p class=del><del>{html.escape(a)}</del></p>"); txt.append(f"[{name}] REMOVED\n- {a}\n")
                else: body.append(f"<p class=add><ins>{html.escape(b)}</ins></p>"); txt.append(f"[{name}] ADDED\n+ {b}\n")
        elif op == "insert":
            counts["insert"] += j2 - j1
            for b in new[j1:j2]: body.append(f"<p class=add><ins>{html.escape(b)}</ins></p>"); txt.append(f"[{name}] ADDED\n+ {b}\n")
        else:
            counts["delete"] += i2 - i1
            for a in old[i1:i2]: body.append(f"<p class=del><del>{html.escape(a)}</del></p>"); txt.append(f"[{name}] REMOVED\n- {a}\n")
    f = counts.get("format", 0); w = counts["replace"] - f
    parts.append(f"<h2>{name}</h2><p class=sum>unchanged {counts['equal']} · wording changed {w} · markup only {f} · added {counts['insert']} · removed {counts['delete']}</p>" + "".join(body))
    print(f"{name:14s} unchanged {counts['equal']:4d}  wording {w:3d}  markup-only {f:3d}  added {counts['insert']:3d}  removed {counts['delete']:3d}")
(OUT / "diff.html").write_text("\n".join(parts)); (OUT / "diff.txt").write_text("\n".join(txt))
print("wrote", OUT / "diff.html", "and diff.txt")
