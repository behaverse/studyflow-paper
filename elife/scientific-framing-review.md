# Making the Studyflow paper read as cognitive science (review, 2026-10-02)

Sources: eLife's author and reviewer guides and the published reviews of 12 eLife tools papers; the guidance of 11 other venues (BRM, AMPPS, JOSS, Nature Methods, PLOS CB, Scientific Data, Neuroinformatics, GigaScience, NHB, Meta-Psychology, eLife); about 20 model tool papers; work on simulated and language-model participants; and a line-by-line audit of `paper-v3.qmd`. Line numbers refer to `paper-v3.qmd` as of today. Nothing in the manuscript was changed.

## 1. Bottom line

1. **eLife does not ask a Tools and Resources paper for a discovery.** It asks the paper to show that the tool *will enable* advances, through proof-of-concept experiments, and to benchmark the tool against existing methods. The evidence rating (Solid, Convincing, Compelling) comes from validation, not from feature coverage. The paper has the validation already, but it sits in Methods and Appendix 3.
2. **The paper reads as technical for two reasons.**
   - The Notation section (2,190 words) is formalism, file format and execution semantics.
   - The Results narrate what the runner does (pools, message flows, `python://` URIs, `n={reached}`, digests) rather than what the researcher gets.
   
   Reviewers of NeuroML, NWB and HSSM said this in so many words: "seems to target software developers", "reads like a press release", and "CLI, YAML" listed as undefined terms.
3. **The paper reads as a study of language models for four reasons.**
   - The Results ask questions about the agents: "Does an agent show the congruency effect?"
   - It uses persona prompts with "silicon samples" citations.
   - It cites CHART, a reporting guideline for studies of *chatbot health advice*.
   - The Discussion spends three paragraphs on AI evaluation (L200–204), and Future work opens with machine authorship.
4. **The fix is mostly to move and rename text, not to do new work.**
   - Promote the evidence you already have (Appendix 3, the planted and null runs) into Results.
   - Recast the language-model run as a pilot that checks the protocol.
   - Push tool and release detail into Methods, a versioned supplement, or the existing JOSS draft (`joss/paper.md`).
5. **Length.** For a Research Article eLife suggests at most about 5,000 words of main text. The current main text, Introduction to Future work, is about 9,000 words. Moving the formalism and the AI-evaluation material frees about 2,000.

## 2. What eLife and similar venues reward

| Pattern | Model papers | Studyflow today |
|---|---|---|
| **Measure the problem first** | Nextflow (the same pipeline gave different genes on Mac and Linux); the timing mega-study; audits of preregistrations | Only cites others' audits. The paper's own measurement, two published Simon and flanker studies encoded with about 10 run-critical values unstated each, is in Appendix 3. |
| **Validate against known answers** | Wilson & Collins 2019 (eLife, "simulate, simulate, simulate"; parameter recovery); jsPsych simulated participants (BRM 2022); SpikeInterface | The planted effect was recovered and the null rejected, but this is one sentence in Results with the detail in Methods. |
| **Reproduce published paradigms** | Gorilla (flanker across settings); lab.js (one Stroop throughout); Neuroscout (replicated known findings); BioCoder (66 protocols encoded, ambiguities exposed) | Appendix 3 does this, on the very tasks of the example study. |
| **Compare with alternatives on one stated criterion** | fMRIPrep vs FEAT; the Nextflow table; pyControl reviewers: "why not roll your own?" | Appendix 2 lists related tools; there is no head-to-head criterion. |
| **Title Results by claim, not by component or stage** | Neuroscout titles Results by scientific aim | Results are "Step 1 Design … Step 4 Report", a tour of the stages. |
| **Keep implementation and version detail out of the main text** | Neuroscout: 17 version numbers, all in Methods; jsPsych split its work into BRM papers and a JOSS paper; BIDS put its specification in a supplement; JOSS bans API docs from papers | CLI names, YAML keys and fault counts tied to a release appear in Results and captions. |
| **Name the users and what each gains on day one** | Spyglass and NWB reviewers asked "who is this for?" | Implicit |

Red flags eLife reviewers raised on comparable papers:
- advertising tone;
- written for developers, or a catalog of features;
- proof of principle with no scientific question (Training Village: "what is more interesting is the scientific question");
- standardization for its own sake (IBL);
- outcomes guaranteed by design (circularity);
- overclaiming "end-to-end" (Neuroscout);
- relying on online docs instead of a self-contained paper (pyControl);
- beta status and future features (HSSM);
- reviewers unable to run the tool (Neuroscout).

**The circularity risk applies to Studyflow.** In Appendix 3 the fingerprint (digest) flags 12 of 12 seeded deviations, but any edit changes a hash. A reviewer can call that guaranteed by design. Its evidential value is elsewhere: the diff shows *which* registered element changed, sorted by Claesen's categories of deviation. Say that, rather than the 12/12.

## 3. The language-model cohort: recommended framing

You decided on 2026-09-30 that the language-model run is the main Results run, and this keeps it. What changes is what the run is *asked*. Precedents that read as "testing the protocol", not as findings:
- jsPsych's simulation mode, for testing "design and analysis pipelines prior to running an experiment";
- oTree bots with `expect()` assertions;
- Wilson & Collins' recovery checks;
- Many Labs 2 piloting its slates to check timing, not effects.

**Recommended (call it A+).**

- **Terms.** Call the actors *artificial participants*; avoid "twins", "silicon" and "agents' cognition". Call the personas *instruction conditions (cautious vs impulsive)*. That is a speed–accuracy emphasis manipulation, standard with human participants (Heitz 2014), and the same instruction text could go to people, which supports "any actor".
- **Pilot checks stated before the results**, each with its expected outcome fixed in advance:
  - P1: did allocation balance the two conditions?
  - P2: did the discontinuation rule fire for exactly the participants with more than 1 in 5 trials unanswered?
  - P3: did both registered decision rules run unchanged on the data that arrived?
  - P4: does the CONSORT figure regenerate from the stored run with a matching fingerprint?
  - P5: did swapping the actor change only one line?
- **One outcomes table:**
  - rows are those checks;
  - columns are the planted, null and three language-model runs;
  - for the planted and null runs the expected value is the ground truth, for the models it is the protocol rule;
  - effect estimates for the models go to a supplementary table, labelled "not interpreted".
- **The two cognitive questions** (Simon congruency, telling the two instruction conditions apart) stay as *example registered questions*. Report only the claim state each rule reached.
- **A short box, "What this run shows / does not show".**
  - It shows that one file produced the allocation, exclusions, analysis, provenance and figure, and that the actor can be replaced.
  - It does not show anything about how language models think, whether they have a Simon effect, whether they can stand in for humans, or timing for humans.
- **Move or cut:**
  - Move to Methods: CHART (at most one sentence: model identifier, decoding parameters, prompts), the latency caveat, the persona texts.
  - Pair Argyle, Aher, Ivanova and Lampinen with the critiques (Crockett & Messeri 2025 TiCS; Lin 2025 AMPPS), and cite them only in Methods or one Discussion paragraph.
  - Cut or send to the supplement the AI-evaluation Discussion (L200–204). Replace it with the cognitive-science counterpart: one protocol given across populations and sites (multi-site replication, measurement invariance).
  - Cut Brain Researcher from five mentions to one or two.
  - Reorder Future work so it leads with a human cohort, multi-site replication and encoding published studies at scale.
- **No per-model comparison figure.** It invites a model-ranking reading.

**Alternative (B):** make the planted and null runs the main Results, with the language-model swap as a short second demonstration. This is the cleanest recovery framing, but it reverses your 30 September decision, so it is your call. Under any option, expect "show it on humans". A small pilot run by the authors (if ethics allows) or reproducing an open human Simon dataset would answer it.

## 4. Turn existing material into evidence (proposed Results order)

Retitle the Results by claim. For example:

1. **"Written methods leave run-critical decisions unstated"**: Appendix 3's `tbl-encoded`, promoted. This is the problem, measured on cognitive tasks. Optional and stronger: encode 5–10 published Simon or n-back studies in BioCoder style and report the categories of what was unstated.
2. **"One file carries the protocol from registration to report"**: the current Steps 1–4, condensed to what the researcher gets. Use one running task (the Simon task, as lab.js did with its Stroop), and keep the `trials: 30` example; it is the clearest illustration of protocol fidelity.
3. **"The registered analysis recovers a planted effect and rejects a null"**: the planted and null runs, in Wilson & Collins' terms.
4. **"Deviations from the registered plan are localized"**: `tbl-blind`, framed by Claesen's categories of deviation and the deviation-reporting template of Willroth & Atherton (2024, AMPPS), not by the 12/12 count.
5. **"The same protocol runs with a different participant"**: the language-model pilot, framed as in section 3.

Add a comparison table on one stated criterion. Proposed criterion: *how many independently maintained copies of each design decision a study keeps* (trial count, exclusion rule, allocation ratio, decision threshold). The alternatives are an OSF preregistration template, a PsychoPy or jsPsych script, an R/Python analysis, a hand-drawn CONSORT figure, and Studyflow. This answers pyControl's "why not roll your own?" and NWB's "no benchmark".

## 5. Vocabulary: developer terms to cognitive-science terms (main text only)

| Now | Replace with |
|---|---|
| coordination model, glue code, pipeline jungles (L51, L55) | step order, decision rules and data hand-offs scattered across scripts and prose (Gelernter and Sculley go to Appendix 2) |
| typed directed graph with validity conditions (L63) | a complete, checkable protocol |
| serialization (L59, L103–109) | file format |
| the runner walks the diagram; message flows between pools (L142) | at each trial the study presents the stimulus and records the response (the BPMN terms go to the caption) |
| conditional boundary event (L136) | preregistered discontinuation rule |
| `n={reached}`, study state $s_n$ (L138) | counts recorded as the study ran |
| digest | fingerprint of the registered protocol |
| read, filter, map, reduce (L156) | read, exclude, summarize per participant, then per group |
| `python://scipy.stats.ttest_1samp`, pins every package (L160) | SciPy's one-sample t test, at a recorded version |
| CSVW schema, dtypes; fails validation before any data moves (L162) | data dictionary; rejected before data collection |
| prompt conditions, dispositions, personas | instruction conditions |
| agents, subjects (for the models) | artificial participants |
| thirteen of fifteen faults were caught (L177) | errors of form are caught, errors of meaning (e.g. a difference test where equivalence is asked) are not |
| projections (functions), views (representations) (L67) | keep "view" only; "projection" moves to Methods (glossary: projection = the mapping) |

## 6. Release-bound statements: one rule

**The main text describes the notation, which is versioned with its schema. Methods names one archived release (a DOI) and holds everything tied to it.** Then move:

- **Notation:** L85 ("checks all four … modeler also enforces"), L97 (departures from OMG), L99 (`python://pkg.fn@1.2`), L105 (`studyflow:exchange`), L107 (`iTXt`), L113, L117 (FEEL, "the validator warns").
- **Results:** L134 "pinned model tag", L160 "pins every package", the fault counts at L177.
- **Limitations:** L226 ("does … does not yet do"), L230 (the browser runner, whole paragraph), L236 (`memory` is `none`).
- **Captions:** identifiers in `fig-overview`, `fig-step2-run`, `fig-step3-analyze`, `fig-views`, `fig-combined`; `studyflow-cli/[TODO]`.
- **Tables:** `tbl-claims`, `tbl-faults`, `tbl-departures` and Appendix 1 become a versioned supplement or move to the JOSS paper, following jsPsych's split. The grammar and element catalog stay as a labelled snapshot of the release, which keeps the paper self-contained, as pyControl's reviewers required.

## 7. Cognitive-science concepts the argument is missing

Seven references already in `references.bib` are never cited:
- `steegen2016multiverse`
- `bridges2020timing`
- `anwylirvine2021timing`
- `morris2019simulation`
- `lakens2017equivalence`
- `larkin1987diagram`
- `redick2013nback`

Where each concept belongs:

- **Analytic flexibility and the multiverse (Steegen):** at L41 (the many-analysts results) and L572 (the multiverse over exclusion thresholds).
- **Reproduction vs replication:** L39–41 use "replicator" beside a reproduction result. The file serves the two differently. Reproduction means re-running on the same data, which the file supports today. Replication means the same protocol with new data, which it is designed for but has not demonstrated.
- **Protocol fidelity and trial timing:**
  - Name trial timing at the N-back paragraph (L148), the strongest cognitive-science passage in the paper, as a known cause of results differing across platforms (Bridges; Anwyl-Irvine).
  - The `trials: 30` example (L183) is protocol fidelity; call it that.
- **Simulation-based validation:** at L154, and in Results item 3 of section 4 (Morris; Wilson & Collins 2019, not yet in the .bib).
- **Researcher degrees of freedom:** at L156; exclusions fixed in advance remove one.
- **Undisclosed deviations from preregistration:** at L175, citing Claesen 2021, Willroth & Atherton 2024 and van den Akker 2023 (52% of 459 preregistrations omitted hypotheses).
- **Equivalence testing:** at L177, the missed fault (Lakens).
- **Diagrams as cognitive aids:** at L234 (Larkin & Simon), framed as a hypothesis.
- **Counterbalancing and allocation concealment:** at L99. Concealment is currently only a hidden TODO at L645.
- **Optional stopping:**
  - L212 says "an analysis can send a researcher back to collect more data". Unplanned, that is optional stopping.
  - Write "a preregistered sequential design" instead.
- **Overclaims to soften:**
  - L177, auditing against CONSORT/SPIRIT/CHART: checklist items are free text and are not scored automatically.
  - L177, "faults a text description is unlikely to catch": no evidence is given.
  - L220, "fundamental rather than fashionable": no evidence is given.

**Positioning.** Clinical trials already have machine-readable protocols:
- ICH M11, adopted November 2025;
- CDISC USDM;
- SPIRIT's SEPTRE.

Studyflow brings that idea to experiments. This argument is stronger for an eLife readership than the comparison with AI evaluation (L47).

## 8. Proposed stages (one kind of change each, each approved before the next)

1. **Framing decision:** A+ or B (section 3). This changes what the Results are about, so it is yours to make.
2. **Cuts and moves, no rewording:**
   - the Notation formalism and file format go to Methods (about 1,700 words leave the main text);
   - the AI-evaluation Discussion and the runtime paragraph at L230 go to the supplement;
   - the release-bound items in section 6 go to Methods.
3. **Reword in domain terms:** the swaps in section 5 and the language-model framing in section 3 (Abstract, L63, L123, L144, L154, L190, captions).
4. **New blocks:**
   - the Results reordered by claim;
   - Appendix 3 and the planted and null runs promoted;
   - the outcomes table;
   - the comparison table;
   - the "shows / does not show" box.
5. **Citations:** the concepts in section 7.
6. **Before submission:**
   - run a one-command reproduction on a clean machine, since eLife reviewers do try to run the tool;
   - write a short paragraph on users and maintenance;
   - archive the release with a DOI.

## 9. Key sources

**eLife guidance**
- Author instructions: https://elife-rp.msubmit.net/html/elife-rp_author_instructions.html
- What an eLife assessment is: https://elifesciences.org/about/elife-assessments

**eLife tools papers and their reviews**
- pyControl: 10.7554/eLife.67846
- IBL behaviour: 10.7554/eLife.63711
- NWB: 10.7554/eLife.78362
- Neuroscout: 10.7554/eLife.79277
- SpikeInterface: 10.7554/eLife.61834
- Brainrender: 10.7554/eLife.65751
- NeuroML: 10.7554/eLife.95135
- Pynapple: reviewed preprint 85786
- Spyglass: reviewed preprint 108089
- HSSM: reviewed preprint 112168
- Training Village: reviewed preprint 111110

**Validation norms**
- Wilson & Collins 2019: 10.7554/eLife.49547
- jsPsych simulation mode: 10.3758/s13428-022-01899-0 and 10.21105/joss.05351
- oTree bots: https://otree.readthedocs.io/en/latest/bots.html

**Tool papers in other venues**
- PsychoPy2: 10.3758/s13428-018-01193-y
- lab.js: 10.3758/s13428-019-01283-5
- Gorilla: 10.3758/s13428-019-01237-x
- Timing mega-study: 10.7717/peerj.9414
- BIDS: 10.1038/sdata.2016.44
- fMRIPrep: 10.1038/s41592-018-0235-4
- Nextflow: 10.1038/nbt.3820
- LabOP: 10.1145/3604568
- BioCoder: 10.1186/1754-1611-4-13

**Deviations from preregistration**
- Claesen 2021: 10.1098/rsos.211037
- van den Akker 2023: 10.1177/25152459231187988
- Willroth & Atherton 2024: 10.1177/25152459231213802

**Language models as participants, and critiques**
- Crockett & Messeri 2025: 10.1016/j.tics.2025.09.012
- Lin 2025: 10.1177/25152459251357566
- CHART: 10.1186/s12916-025-04274-w
- Heitz 2014: 10.3389/fnins.2014.00150

**Not verified.** The research agents saw only the abstract or a search excerpt for these: Crockett & Messeri, Heitz 2014's specific passage, Centaur's "in silico prototyping" phrase, and the Many Labs 2 pilot detail. They did not confirm the article type for Spyglass, HSSM and Training Village. Check these before citing.
