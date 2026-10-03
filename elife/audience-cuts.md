# Cuts for Pedro's reader (2026-10-03)

Proposal only; nothing in `paper-v3.qmd` is changed. Line numbers are the working tree of 2026-10-03.

## What his comments say about the reader

His 17 comments and 146 suggestions (July 2026, `coauthor-edits-ledger.md`) fall on the Introduction, the Notation, Step 1 and the figures, the parts that existed then. They ask for six things:

1. **Explain each software term, or leave it out.** He asked what "ISO-standardized", XML, "scheme" and "library" mean, and asked twice for a glossary.
2. **Say what a feature shows in this study, not what it does in general.** On the views paragraph he wrote "say something about what those views show about your specific study".
3. **One word, one meaning.** He flagged step vs operation, fragment vs stage, draw (depict vs sample), projection vs view, and structure vs topology.
4. **Say why it matters**, e.g. reproducibility or quality control.
5. **Stay honest about the demo**, e.g. "for convenience" and "current capabilities".
6. **Conclude on five points:** it works; it covers the whole lifecycle; it replaces what is now drawn by hand (CONSORT); one document avoids drift; it opens new uses without code.

Most of the text added since July is denser than anything he read. It includes the state and scope rules, YAML/XML/Git/PNG, prospective and retrospective provenance, digests, BPMN boundary events and pools, the decision-gateway thresholds, the blind-seeded deviations, the workflow-tool axes, and the wave-1 tooling limits. He never commented on any of it, but by his rules 1 and 2 he would have flagged it. The cuts below follow his six rules. The prose cuts total about 2,050 words: the main text goes from about 7,900 words of prose to about 5,900.

Rules for every stage: material that moves goes verbatim to Methods or an appendix, so nothing is lost from the paper. Each stage is one kind of change and is approved before the next.

## Stage F. The example study's conclusion on his five points (about −100 words)

His outline for the conclusion of the example study (Doc, July 2026):

> * studyflow works
> * supports full lifecycle
> * can replace current practices (CONSORT)
> * avoids the problems of current practices (one document)
> * opens up new opportunities; here we used studyflow as a means to orchestrate artifical agents across a battery of task and automate the analysis of their behavior; all using only the modeler and without having to write any code.

Today the Results end in two subsections. "The pilot ran as registered" (L175–180) covers his point 1. "One file, no second copy" (L182–195) covers points 2 to 5 as "First … Fourth", but it does not use his wording. The proposal merges the two subsections into one that follows his outline, one paragraph per point. The text is reused from L177–L195. `tbl-pilot` and `tbl-copies` stay.

**F1. Draft** (about 420 words, replacing about 520):

> ## One file, no second copy
>
> The example study supports five conclusions.
>
> **Studyflow works.** The registered file fixed in advance what each check should return, and every check held (@tbl-pilot). Permuted blocks of four split a cohort of eight four and four. The counts balance at every node and equal those the run recorded. The discontinuation rule removed exactly the participants whose trials crossed its threshold, and the protocol each run followed is the registered one. Where the answer was known, the registered analysis reached it: *Supported* on both questions when an effect was planted, and *Not supported* on both when none was. [TODO: from the language-model runs: which checks held for each model and the claim state of each question. These are outputs of the pilot, not claims about language models (@supptbl-agents).]
>
> **It supports the full study lifecycle.** Each step is a complete example on its own, and @fig-combined is their composition: at once the protocol as registered, the study as executed, and the record of what happened.
>
> **It can replace current practices.** The artifacts that current practice draws by hand come out of that file. The CONSORT flow, the SPIRIT schedule, the checklist, and the deviation report are views of it, and the counts the CONSORT flow reports are the counts recorded as the study ran.
>
> **It avoids the problems of current practices, because there is one document.** The Simon task's length shows what that provides. It is set in the file exactly once (`Trials: 30`, in the settings wired into the task). The Study view displays it, the task uses it to end the block, the analysis receives the data it produces, and the exported figure renders it. A protocol, a script, a methods paragraph, and a figure cannot disagree about its value, because there is no second copy. Changing it to forty trials is one edit: [the existing two-line diff]. @tbl-copies extends the count to four decisions of the example study. Kept as separate documents, each would be written in three or four places that someone keeps in agreement by hand; in the Studyflow file each is written once.
>
> **It opens up new uses.** Here we used Studyflow to orchestrate artificial agents across the tasks of a battery and to automate the analysis of their responses, without writing any code for the study: the file calls only the task software and the published library functions it names. The same file serves the two kinds of repetition differently [@nosek2022replicability]. Anyone can reproduce the analysis from the executed copy and its data, and a replication can run the deposited protocol on new participants, which this paper designs for but does not demonstrate.

**F2. Where the draft departs from his wording, and why**

- **"using only the modeler"** is left out. The runs used the local runtime (`studyflow run`, Appendix 1), not the modeler, so the claim kept is "without writing any code for the study". If the study was in fact authored only in the modeler, "drawn in the modeler" can go back in.
- **"analysis of their behavior"** becomes "of their responses". This keeps the framing of 2026-10-02: the language-model run says nothing about the agents' cognition.
- **"(CONSORT)"** is widened to the four views, which is what the current text already claims.

**F3. Knock-on cuts**

- Box 1's "Shows" half now repeats point 1. The proposal keeps "Does not show" only (−60 words, optional; you approved Box 1 in stage 3a).
- His five points are also a filter for the Results. Every part maps to one of them: R1 and Step 4's deviations to point 4; Steps 1 and 4 to points 2 and 3; Steps 2 and 3 to points 1, 2 and 5. The detail that maps to none of them is what Stage C cuts: decision thresholds, pingouin and CSVW, and BPMN mechanism terms.

## Stage A. Move developer material out of the main text (about −1,170 words)

| ID | Where | Proposal | Words | His rule | Flag |
|:--|:--|:--|--:|:--|:--|
| A1 | Notation, "Data and state" (L75) | Move to Methods, "The graph and its types". Leave one sentence in "The formal object": data appear as datasets; the values a run accumulates (an allocated condition, a count of failed trials) are the study's state. | −110 | 1, 2 | |
| A2 | "Relation to the BPMN standard" (L83–89) | Move the inherits/adds lists and the extensibility paragraph to Methods. Leave about 70 words: a BPMN profile from the OMG's standard; adds tasks, questionnaires, randomization and eligibility gateways, and data bound to community standards (@fig-elements). | −180 | 1 | **Declined 2026-10-02** for coherence. Lite version: cut only the pools/lanes/choreography list and L89 (−90). Keep "OMG" (his edit). |
| A3 | "File format" and "Execution" (L93–101) | Replace with about 70 words: one plain-text file; version control shows each edit as the lines that changed; an exported image carries the whole file, so "the image *is* the Studyflow file" (his sentence, kept); the same file holds the plan and, after the run, its record, so deviations are the difference between the two (Step 4). YAML/XML, SVG/PNG, prospective/retrospective provenance and "cryptographic digest" go to Methods. | −175 | 1 | **Declined 2026-10-02** with A2. Lite version: cut only the provenance terms in L101 (−50). |
| A4 | Discussion, "Where Studyflow sits among workflow tools" (L215–223) | Move to Appendix 2, which already holds the extended comparison. Leave about 80 words: Studyflow composes the tools it calls (jsPsych, PsychoPy, workflow engines, data standards); none of them expresses the study itself (consent, allocation, a preregistered hypothesis), and that is the layer it adds (@tbl-compare). | −305 | 1 | **Declined 2026-10-02** ("related work to Appendix 2"). Lite version: drop the three-axes opener and the DAG/statecharts paragraph (−150). |
| A5 | Limitations, trust/containers (L234), tooling limits (L240), specification risk (L242) | Replace the three paragraphs with about 90 words: the reference tools do not yet run every design the notation states (@tbl-scope). Trial order is recorded, not registered. Analyses are Python library calls. A human cohort needs data protection beyond what is built in. The file stays readable by any BPMN tool, but running it needs the Studyflow specification. | −310 | 1, 5 | L240 and L242 are **wave 1, uncommitted** (adoption objections). Their content survives in `tbl-scope` and Methods. |
| A6 | Discussion, Brain Researcher comparison (L203, second half) | Keep the preregistration argument. Brain Researcher stays only in Future work. | −90 | 6 | It is in both places by your choice of 2026-10-02. |

## Stage B. Remove repetition (about −455 words)

| ID | Said where | Proposal | Words | His rule |
|:--|:--|:--|--:|:--|
| B1 | The five views are listed twice: Notation L79 (in general) and Step 4 L165 (in this study) | Keep L165, which is what he asked for, and move his sentence "The Study view shows all the information available" there. Cut L79 to his opening sentence plus "consistent by construction". | −130 | 2 |
| B2 | Discontinuation rule explained four times (L109, L133, L147, plus `tbl-rule` and the fig-step2-run caption) | Cut L147 to one sentence: an unanswered trial counts toward the rule, and a discontinued participant leaves by the counted exit. | −75 | — |
| B3 | Form vs meaning of the validator, three times (L173, L209, L236) | Drop L173 and keep the Limitations version. | −45 | — |
| B5 | Results roadmap (L117) restates the subsection titles | Replace it with his five points as the signpost, so the Results open and close on them (his rule: signpost and conclude). | −40 | 6 |
| B6 | Pilot framing (L109) repeats Box 1 "Does not show" and Limitations L246 | Keep "for convenience" (his) and the human-cohort sentence. Drop the "pilot in the sense used for experiment software" clause, which Box 1 covers. | −75 | 5 |
| B7 | Planted/null known-answer check in L151, L177, Box 1, L209 and `tbl-pilot` | Drop it from Step 3 (L151). It stays in point 1 of Stage F. | −70 | — |

## Stage C. Plain wording for mechanism detail in the Results (about −335 words)

| ID | Where | Proposal | Words | His rule |
|:--|:--|:--|--:|:--|
| C1 | Step 1 (L133, L135) | Replace "conditional boundary event" (and its two citations) with "a rule attached to each task". Replace "`n={reached}` in the deposited file" with "the registered figure shows every count as zero; the executed one, the numbers". | −35 | 1 |
| C2 | Step 2 (L139, L145) | Replace "message flows … each drawn as a pool" with "drawn as an exchange between the study and its actor". In the N-back paragraph, drop "explicit subprocess", "boundary timer" and the BDM sentence; the caption keeps them. | −50 | 1 |
| C3 | Step 3 (L155) | The *Not testable* minima (four per arm, three within) and the "two-sided *p*" clause are already in `tbl-rule`. Cut them from the prose. | −60 | 2 |
| C4 | Step 3 (L157, L159) | Merge into one sentence: each operation names the published function it calls and its version, and the trials' data dictionary lets the validator reject an analysis that reads a column the data will not have. This drops pingouin, "dashed edges" and CSVW. | −60 | 1 |
| C5 | Step 4, blind-seeded deviations (L171) | Keep two sentences and `tbl-blind`: twelve deviations of the kinds audits find; every one shows in the diff as the line that changed. The seeding procedure is already in Appendix 3. | −105 | 2 |
| C6 | Introduction (L59, wave 1) | Keep his ISO explanation. Drop "while running it follows the Studyflow specification", which A5 states once. | −25 | 1 |

## Stage D. Display items (pages, not words)

The main text now has 10 figures, 6 code listings and 9 tables.

| ID | Proposal | His rule |
|:--|:--|:--|
| D1 | Move the four YAML listings (`lst-minimal-study`, `lst-step1-design`, `lst-step2-run`, `lst-step3-analyze`, about 170 lines of YAML and 330 words of captions) to the Supplementary listings. Keep `lst-swap` and `lst-diff`, which show "one line" and "the deviation report". His conclusion point "without having to write any code" reads oddly beside four pages of YAML. | 1, 6 |
| D2 | `tbl-requirements`: move the Precedent column (config-as-code, GitOps, Make, Airflow, Dagster, build systems) to Appendix 2. | 1 |
| D3 | Move `tbl-elements` (`bpmn:ChoreographyTask`, `python://pkg.fn@version`, `additionalArguments`) and `fig-elements` to the supplement; `supptbl-catalog` already lists the catalog. | 1 |
| D4 | Drop `fig-step4-report` (one manual task and an end event, both visible in `fig-combined`), or fold it into `fig-views` as a panel. | — |
| D5 | Keep `tbl-glossary`, which he asked for twice. After A–C, trim it to the terms the main text still uses; YAML/XML, Schema and Git may go. | 1 |

## Stage E. His one-word-one-meaning rule (no size change)

| ID | Where | Proposal |
|:--|:--|:--|
| E1 | L205 "the flow becomes the topology of the diagram" | Change "topology" to "structure"; he flagged the pair. |
| E2 | L240 "draws each trial's congruency, but the draw happens" | Change to "samples … the sampling happens". "Draw" means depict elsewhere in the main text (L109, L139, L184). |
| E3 | Captions of fig-step1-design, fig-step4-report, lst-minimal-study and lst-step1-design: "runnable fragment" | Change to "a part of the study that runs on its own"; he flagged fragment vs stage. |
| E4 | "subjects" (18 in the main text) vs "participants" (23) | You prefer "participants" in prose. "Subjects" now names the per-participant process in the Results. Decide whether to keep it only in figure and caption labels. |

## His sentences kept through all stages

- Projections: "the key mechanism …" and "The Study view shows all the information available" (moved in B1).
- "Object Management Group (OMG)" (A2).
- "the image *is* the Studyflow file" (A3).
- "for convenience" (B6).
- "Every element defines information that the study will later consume" (untouched).
- "the artifacts that current practice draws by hand come out of that file" (F, point 3).
- "Both properties serve reproducibility and quality control" (untouched).

## Suggested order

Start with F, which is his own outline, then B, C and E. B, C and E cut repetition and wording and touch no decision you made earlier. Then D, then A. A has three items you declined on 2026-10-02, so pick the full or the lite version for each. F, B, C and E alone save about 890 words (main text to about 7,000). With the lite versions of A2–A4 the total is about 1,700 words; with the full versions, about 2,050.

## Applied (2026-10-03) in `paper-v3p.qmd`

`paper-v3p.qmd` is `paper-v3.qmd` (md5 `1e586948…`, working tree of 2026-10-03) with every stage applied. `paper-v3.qmd` and `_quarto.yml` are unchanged. The main text (Introduction to Future work) goes from 8,281 to 6,707 words. The estimate was −2,050; the actual cut is −1,574, because several short replacements came out longer than planned (A3, B1, C5). Main-text figures go from 10 to 8, code listings from 6 to 2, and tables from 9 to 8. The HTML render has no warnings and no unresolved references. The eLife PDF was not rendered.

Where the result departs from the plan:

- **A2–A4:** the full versions were applied, not the lite ones.
- **Moved text:**
  - A1 went to Methods, "The graph and its types".
  - A2 and A3 went to Methods, "The language specification".
  - A4 opens Appendix 2.
  - A5 went to the end of Methods, "Availability and use". Its tooling paragraph overlaps the scope paragraph and `tbl-scope` there, so trim one of them.
  - A6 went to Appendix 2, after "Implications for AI evaluation".
  - The precedents of D2 went to Appendix 2 as one paragraph, before "Configuration as code".
- **Display items:**
  - D1: the listings are now Supplementary Listings S2–S5.
  - D3: `tbl-elements` was dropped rather than moved, since Supplementary Table S1 lists every element with its BPMN type. `fig-elements` became Supplementary Figure S3.
  - D4: `fig-step4-report` became Supplementary Figure S2 rather than being dropped.
- **Box 1** keeps only "does not show", reworded as full sentences.
- **Fixes found on reading:**
  - "allocation lane" became "allocation phase".
  - "open-weight" was dropped.
  - "any BPMN tool can read" the Studyflow file became "converts without loss to the standard BPMN file that any BPMN tool reads", which keeps the wave-1 correction.
  - The two "Finally," openings in Limitations are now one.
  - Listing S5 is cited from Step 3.
