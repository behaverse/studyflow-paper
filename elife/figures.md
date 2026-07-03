# Figure briefs for the Studyflow paper (eLife)

Instructions for a graphic designer. No knowledge of the paper's subject is needed:
every figure is built from the small shape vocabulary below, plus ordinary
flowcharts, charts, and screenshots. Read the "Shared visual vocabulary" and
"Global style" sections first; they apply to all figures.

The paper is about a diagram language for describing scientific studies. Its core
message, which the figures must carry visually: **one diagram file can be shown in
many different ways (a flowchart, a timeline, a checklist, a published figure),
and all of these are views of the same single source.**

---

## Shared visual vocabulary (use identically in every figure)

These shapes come from a standard called BPMN. Draw them consistently:

| Shape | How to draw it | Meaning (for your reference only) |
|---|---|---|
| Start event | Small circle, thin single stroke | where a participant enters |
| End event | Small circle, thick single stroke | where a participant exits normally |
| Error end event | Thick circle containing a small lightning-bolt icon | an exit through failure/dropout |
| Boundary event | Small double-stroked circle sitting ON the border of a box (half in, half out) | an interruption attached to a step |
| Timer icon | Tiny clock face inside a boundary event circle | a time limit |
| Task | Rectangle with rounded corners, name centered | one step someone performs |
| Sub-process | Rounded rectangle with a small `[+]` marker at bottom center | a step that contains its own diagram |
| Gateway | Diamond (square rotated 45 degrees) | a decision point |
| Randomization gateway | Diamond with a small dice icon | random assignment |
| Eligibility gateway | Diamond with a small funnel icon | include/exclude decision |
| Dataset / data store | Cylinder (database symbol) | stored data |
| Schema / document | Page with folded top-right corner | a data description or document |
| Sequence flow | Solid arrow with filled arrowhead | "then" (order of steps) |
| Data association | Dashed arrow, thin, open arrowhead | data moving in or out of a step |
| Task-type icons | Small icon in the top-left corner of a task box: brain = cognitive task, clipboard = questionnaire, "i" = instruction, gears = data operation, person = manual step | what kind of step it is |

## Global style

- Vector output: SVG and PDF per figure.
- Sizes: full width = 174 mm, single column = 85 mm (marked per figure). Text
  legible at print size (>= 6.5 pt).
- One sans-serif family throughout (Helvetica/Arial class).
- Grayscale base + ONE accent color used sparingly for "the single source file"
  and callouts. Use a color-blind-safe accent (e.g., Okabe-Ito blue #0072B2 or
  orange #E69F00). Figures must still read in pure grayscale.
- The same shape vocabulary, stroke widths, and corner radii in every figure —
  the repetition is intentional and load-bearing.
- Labels: use the exact strings given below; do not paraphrase.
- Where a caption below says "(n=...)", draw the literal text `n = ...`.

---

## Figure 1 — "Unlike data, the process has no shared artifact"
**Full width. Drawn from scratch. Conceptual map.**

Purpose: show that a study's life passes through many hands, each holding a
DIFFERENT document, and that existing tools each cover only a slice; an empty
highlighted band shows the missing whole-span artifact.

Layout, top to bottom:

1. **Lifecycle bar** (top): a horizontal arrow divided into 7 stages, left to
   right: `Design` → `Ethics` → `Registration` → `Data collection` → `Analysis`
   → `Publication` → `Replication`.
2. **Audience row**: under each stage, a small person icon with a label and the
   document they hold (page icon + text):
   - Design: `Researcher` — `protocol PDF`
   - Ethics: `Ethics board` — `ethics application`
   - Registration: `Reviewer` — `registry entry`
   - Data collection: `Participant / Engineer` — `experiment script`
   - Analysis: `Analyst` — `analysis notebook`
   - Publication: `Reviewer` — `checklists, figures`
   - Replication: `Replicator` — `the published paper`
   Draw the document icons visibly DIFFERENT from one another (different
   proportions/corners) — the point is that no two are the same artifact.
3. **Tool-coverage brackets**: below the audience row, 5 horizontal brackets,
   each spanning only part of the lifecycle bar, labeled:
   - `Experiment builders` (spanning Data collection)
   - `Workflow engines` (spanning Analysis)
   - `Evaluation harnesses` (spanning Analysis)
   - `Reporting guidelines` (spanning Publication)
   - `Data standards` (spanning Data collection → Analysis)
4. **The gap** (bottom): one empty band spanning the ENTIRE lifecycle, drawn as
   a dashed outline filled with the accent color at ~15% opacity, labeled:
   `? — one artifact every audience can read, validate, and execute`.

## Figure 2 — "The example study, whole"
**Full width. Assembled: we supply a machine-exported diagram (SVG); you add callouts.**

Purpose: the complete example study as one big diagram, with seven numbered
callouts naming what each region is. Source: `example_study.studyflow`
(exported from the modeler; we supply the SVG).

We will provide the diagram export. Your work: place it full-width, then add
seven numbered callout chips (accent-colored circles with white numerals, thin
leader lines to the region). Callout labels, placed in a legend strip below the
diagram:

1. `Consent at the start event`
2. `Eligibility and randomization gateways`
3. `The task battery`
4. `Boundary error events accumulate attrition`
5. `The typed analysis subprocess`
6. `Actor pools joined to the battery by message flows`
7. `The trials dataset bound to its schema`

Keep leader lines horizontal/vertical only, never crossing each other.

## Figure 3 — "The CONSORT flow"
**Full width, three panels: (a), (b), (c).**

Purpose: a standard medical-trial flowchart (a) next to the same flowchart in
our shape vocabulary (b), plus a small inset (c) contrasting how dropouts are
drawn.

**(a) Classic flowchart** (redraw; reference: the CONSORT 2025 participant flow
diagram, a well-known template — plain rectangles and arrows, NO rounded
corners, deliberately generic):
- Vertical spine of boxes: `Assessed for eligibility (n = ...)` →
  `Randomized (n = ...)` → two parallel columns:
  `Allocated to self-paced (n = ...)` and `Allocated to time-pressured (n = ...)`,
  each followed by `Lost to follow-up (n = ...)` then `Analysed (n = ...)`.
- One box hanging off to the side of the spine between the first two:
  `Excluded (n = ...)` — connected by a plain horizontal line.

**(b) Same flow in our vocabulary** (use the shared shapes):
- Thin-stroke start circle → task `Screening` with a boundary lightning circle
  on its edge; from that boundary circle an arrow to a thick error-end circle
  labeled `Excluded (n = ...)`.
- Then a dice-icon diamond `Randomize` splitting into two columns of task boxes
  (`Self-paced battery`, `Time-pressured battery`), each with a boundary
  lightning circle → error-end circle `Dropped out (n = ...)`.
- Each column ends in a task `Analyze` (gears icon) with boundary →
  `Excluded from analysis (n = ...)`, then a thick end circle.
- Same labels and left-right arrangement as (a), so (a) and (b) mirror each other.

**(c) Small inset, two mini-drawings side by side:**
- Left, captioned `attrition as a connected edge`: a task box with a boundary
  lightning circle wired by an arrow into a counted error-end circle
  (`n = 12` inside a small tag).
- Right, captioned `attrition as a floating annotation`: a plain box with a
  detached side box `Excluded (n = 12)` connected by NOTHING (leave visible gap).
- Put a subtle check mark near the left mini-drawing and nothing on the right —
  no cross/X (keep it undramatic).

## Figure 4 — "The trial is an explicit subgraph"
**Full width. Left panel, right panel, bottom strip.**

Purpose: an informal "slide-style" sketch of a memory task (left) versus the
same thing as a formal diagram (right), plus the compressed one-box form below.

**Left panel — deliberately informal** (like a PowerPoint slide):
- A diagonal cascade of 4-5 overlapping screen frames, each showing one large
  digit (`3`, `1`, `2`, `1`...). Between frames, small arrows annotated
  `0.5 s` and `1.5 s`. A keyboard-key icon under one frame labeled
  `match?`. Use a hand-drawn/loose visual tone (but still vector).

**Right panel — formal, shared vocabulary:**
- A sub-process rounded rectangle titled `N-back trial` containing:
  task `Show stimulus` (brain icon) with TWO boundary clock circles on its edge,
  labeled `response window` and `inter-trial interval`; an arrow to a plain
  diamond with two exits labeled `target` and `non-target`, both looping back to
  `Show stimulus`; one exit arrow leaving the sub-process.

**Bottom strip — compression:**
- A single task box `N-back (digits)` (brain icon) with a small attached
  parameter card (folded-corner page) listing, in monospace:
  `N: 2 · ISI: 1.5 s · stimulus: 0.5 s · trials/block: 12`.
- A wide arrow from the right panel to this box labeled `compresses to`, and a
  thin arrow back labeled `the runner expands`.

## Figure 5 — "Agent profiles across the battery, against chance and human"
**Full width. Data chart: generated from data by us; you style it (fonts, colors, spacing) only.**

For orientation: dot-and-error-bar chart, two column facets (`N-back`,
`Flanker`); x-axis = accuracy 0-1; rows = model × trait conditions
(`Random baseline`, `Open-weight LLM (baseline)`, `Open-weight LLM (careful)`,
`Commercial VLM (baseline)`, `Commercial VLM (careful)`). A dashed vertical line
at 0.5 labeled `chance`; a shaded vertical band (accent at ~15%) spanning the
human participants' scores, labeled `human anchor`. A second, smaller facet pair
shows response time only for rows where it is meaningful (humans); other rows
grayed out with the note `elapsed latency, excluded`.

## Figure 6 — "The analysis pipeline is the preregistration"
**Full width. Two aligned columns.**

Purpose: a pipeline drawn as diagram steps (left) lines up, step by step, with
the code that implements it (right).

**Left column** (shared vocabulary, vertical chain of gears-icon tasks):
`Read raw trials` → `Filter invalid trials` → `Map to derived measures` →
plain diamond `Branch by comparison` → `Reduce: subject summaries` →
`Reduce: group statistics` → person-icon task `Manual outlier review` →
`Render and write`.
- A cylinder `trials (BDM)` connects INTO `Read` with a dashed arrow; a cylinder
  `results` receives a dashed arrow FROM `Render and write`.

**Right column**: a monospace code panel (we supply the snippet text), visually
split into horizontal bands; each band vertically aligned with its diagram step.
Connect each step to its band with a very light horizontal rule or shared
alternating background stripes — no arrows.

## Figure 7 — "SPIRIT as plan, CONSORT as report, CHART for the agents, one file"
**Full width. One source, three projections.**

Purpose: THE key figure for the paper's message. One file on the left; three
different renderings of it fan out to the right.

- **Left**: one folded-corner document icon, accent-colored, labeled
  `study.studyflow` — the only accent-filled object in the figure.
- Three arrows fan out right to three stacked panels:
  1. **Top panel** `Schedule (plan, before the run)`: a Gantt chart — rows =
     `Consent`, `Screening`, `Battery`, `Follow-up`, `Analysis`; horizontal bars
     across a week/session axis.
  2. **Middle panel** `Checklist (audit)`: 6-7 checklist lines with check marks
     and one empty checkbox; text can be greeked except three real items:
     `Eligibility criteria — declared`, `Allocation rule — declared`, and
     `Model version — pinned`.
  3. **Bottom panel** `Participant flow (report, after the run)`: a miniature of
     Figure 3(b) WITH counts filled in (`n = 1`, `n = 9`, `n = 3` on the error
     ends).
- Under the top and bottom panels add small tags: `before the run` / `after the
  run`, and between them a tiny diff badge: `only the counts changed`.

## Figure 8 — "A complete core, extensible by schema"
**Single column. Architecture diagram.**

Purpose: a complete core with optional plug-ins.

- Center: a large solid rounded rectangle labeled `Core vocabulary`, containing
  two-column micro-text of its contents (small, greeked-acceptable except these
  words): `study container · events · flows · activities · data elements ·
  cognitive tasks · questionnaires · instructions · gateways`.
- Around its right edge: three smaller rounded rectangles docked like sockets
  (draw a notch where they attach), dashed outlines, labeled `omniprocess`,
  `datatrove`, `galea`, each with a one-word subtitle:
  `orchestration`, `data transforms`, `EEG/eye-tracking`.
- Footer line, small text: `extensions subclass core types; the file stays
  valid BPMN 2.0`.
- Visual emphasis: the core looks finished and self-sufficient (solid, heavy
  stroke); extensions look optional (dashed, lighter).

---

## Supplementary figures

## Figure S1 — "A multimodal pipeline in the same notation"
**Full width. We supply the diagram export; minimal styling only.**
A pipeline harmonizing EEG, fMRI, and behavioral recordings: three cylinders
(`EEG`, `fMRI`, `behavior`) feeding gears-icon tasks into one cylinder
(`harmonized dataset`), then a training chain. Treat like Figure 2: place the
export, keep labels legible.

## Figure S2 — "The Studyflow modeler"
**Full width. Annotated screenshot; we supply the screenshot.**
Add four callout chips (same style as Figure 2): `1 Palette (generated from the
schema)`, `2 Canvas`, `3 Inspector (element attributes)`, `4 Validation`.

## Figure S3 — "The runner walks the diagram a participant sees"
**Full width. Five paired rows; we supply the GUI screenshots.**
Left column: five diagram nodes (shared vocabulary): thin start circle
(`Consent`), "i"-icon task (`Instruction`), clipboard task (`Questionnaire`),
brain task (`N-back trial`), thick end circle (`Completion`). Right column: the
matching five browser-window screenshots. Connect each pair with one horizontal
accent arrow. Align rows strictly; equal heights.

---

## Delivery checklist

- [ ] SVG + PDF per figure, fonts embedded or outlined
- [ ] Figures 1, 3, 4, 6, 7, 8 drawn from scratch; 2, S1, S2, S3 assembled from
      supplied exports/screenshots; 5 styled from a supplied chart
- [ ] Identical shape vocabulary, stroke widths, and icon set across all figures
- [ ] One accent color; readable in grayscale; color-blind-safe
- [ ] Exact label strings as specified above
