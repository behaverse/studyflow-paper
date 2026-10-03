# Backup: Limitations and Future work if wave 2 does not land (2026-10-02)

These are ready-to-paste replacements for the `# Limitations` and `# Future work` sections of `paper-v3.qmd`. They answer the eight objections in `adoption-objections-plan.md` as limitations and future work, without any tool change. They are true of studyflow-modeler main at 2aff980c and of the example study as it stands. Nothing has been applied to the manuscript.

Each paragraph is tagged: **[kept]** is the current text unchanged, **[revised]** is current text with additions (shown in full), **[new]** is a new paragraph. The tag also names the objection the paragraph answers. Option A is the full version, about 700 words more than the current Limitations, plus about 175 for the new Future work paragraph. Option B is one compact paragraph of about 200 words. The paper's main text is about 7,900 words now, so Option A suits a version that trims elsewhere, and Option B one that does not.

Citations use only keys already in `references.bib`. No new keys are needed.

---

## Option A: full replacement

# Limitations

**[revised; objections 4 and 7]** BPMN is heavyweight, and asking researchers to learn one more notation is a real cost, paid before any benefit arrives. Comprehension of a process model also degrades as the model grows [@reijers2011understandability; @bogale2024]; the usual mitigation, which Studyflow inherits from BPMN, is hierarchical decomposition into subprocesses that expand and collapse. The example study shows the scale: a pilot with two tasks is a file of more than a thousand lines. We hold the cost down with a small vocabulary specific to cognitive science over a domain-neutral core. Conceptually, a Studyflow diagram is a flowchart carrying extra attributes, one that can also be checked automatically, tracked line by line under version control, embedded in an image, and run. Like any domain-specific notation, Studyflow's core vocabulary is designed to cover common experimental workflows rather than every possible experimental paradigm. Some common designs are described by the notation but not yet run by its reference runtimes: stratified allocation and minimization, sessions that participants return to days later, and EEG acquisition. Adaptive procedures such as staircases run only by delegating to external code, outside what the validator checks (@tbl-scope). Specialized use cases are expected to extend the core schema with additional elements where needed, while preserving compatibility with the underlying notation.

**[new; objection 2]** The notation coordinates tasks; it does not describe their trials. What happens within a task (the order of its trials, their timing, and how its conditions are drawn) is registered only when the author writes it into the settings wired to the task (@tbl-scope). In the example study much of it is not. The file fixes the number of Simon trials, but the task draws each trial's congruency with a generator of its own, so the order participants saw is recorded in the trial data after the run rather than registered before it. Some of the values that @tbl-encoded finds unstated in published Methods, such as the order of trials and the proportion of congruent ones, are therefore absent from our own file as well. Registering a task's trial list as data, with its content inside the protocol's fingerprint, would close that gap without turning Studyflow into a language for authoring trials, which tools such as jsPsych and SweetPea already are [@deleeuw2015jspsych; @musslick2022sweetpea].

**[new; objection 3]** The registered analysis names a published library function at every step, so that each operation can be read in the diagram and checked against the data dictionary. The price is length. The example study's congruency test, a one-sided paired *t* test, takes twelve library calls, most of them reshaping the table of trials, where a script would take a few lines. The reference implementation also runs only Python steps. R, in which much of cognitive science analyzes its data, and the mixed-effects models the field often fits are not demonstrated, and response times are not analyzed in the example. The claim states are decided here by *p* values, but the notation does not require it: a decision gateway reads any result, so a rule on a Bayes factor or on an interval is drawn the same way.

**[revised; objection 6]** An executable figure shifts where trust in a study rests. Running a Studyflow diagram asks the reader to trust two things: the external code it references, and the correspondence between the rendered diagram and its source file. Both yield to ordinary software engineering and security remedies: fingerprinting the source, recording the version of the external code, and restricting each external call to its declared operation, for example through containers. The reference implementation provides the first two but not the third (@tbl-claims). Running someone else's file therefore runs their code with the reader's permissions, and it deserves the care given to any downloaded script. A run also keeps its history under version control, every exchange included. With people as participants that history would hold their responses, so a human study needs data-protection measures, such as pseudonymised identifiers and raw data kept outside the history, which the reference implementation does not yet provide.

**[kept]** Validation checks form, not science. A file that passes validation is well-formed, its counts balance, and its protocol is the one its runs recorded; the validator cannot tell a difference test from an equivalence test, or an inequality flipped in every branch from an intended one (@tbl-faults). A passing check read as an endorsement would discourage exactly the reading those faults need.

**[revised; objection 1]** A human cohort taking the same file is a design goal that this paper does not demonstrate: the example study ran only with artificial agents, in the reference implementation's local runtime (Appendix 1). The browser runtime presents every step to a participant, but at this release it keeps a session's record in the browser, to be downloaded at the end or sent to the Behaverse data server. It does not send data to the platforms laboratories use to host online studies, does not resume an interrupted session, and does not write the counts of a human cohort back into the file. Until it does, the participant flow of a human study would be assembled from session records by hand, which is the step the notation exists to remove.

**[revised; objection 5]** A single source of truth also concentrates risk, so the design keeps the notation independent of any one tool: the schema is versioned apart from the code that reads it, and the exported BPMN 2.0 XML opens in any compliant BPMN tool, which ignores the Studyflow extensions it does not recognize [@bpmnspec; @magnani2009bpdmn]. A project that no longer uses our toolkits is left with a valid, standard file that no single tool owns and any BPMN tool can draw. Running it again, however, needs a runtime that follows the Studyflow specification, since a generic BPMN engine does not read the extensions and few engines run BPMN's own execution semantics [@geiger2016bpmn]. What has to outlive our implementation is therefore the specification, and at present one group maintains both.

The single source is also not yet complete:
- The labels drawn on the diagram repeat some values as text for the reader, such as the 20% of a discontinuation exit. The run does not read those copies, so nothing yet stops them drifting from the values they describe (@tbl-copies).
- The ethics application, the registry entry, and the manuscript are still written as prose. The file reduces the copies a study keeps by hand rather than removing them.
- The fingerprint shows that a protocol changed, not when it was registered. That date still comes from where the file was sent before the run.

**[kept]** We have not measured whether Studyflow diagrams are easier to read than the protocol PDFs, figures, and scripts they replace, and the classic flowchart-versus-text comparisons are mixed [@scanlan1989flowcharts; @shneiderman1977flowcharts]. Diagrams can make explicit the relations that a text leaves the reader to infer [@larkin1987diagram], and we designed every feature with comprehension in mind, but we treat the benefit as a hypothesis awaiting a usability study [@figl2017comprehension].

**[revised; objection 8]** Finally, the language models in the example study stand in for participants only to exercise the protocol. We chose them because they are the cheapest actor that fails in some of the ways people do, answering outside the allowed responses or not in time, so the exits fire on failures that were not planted. They are not replacements for humans, and treating their data as human evidence invites documented misinterpretations [@dillion2023replace; @lin2025fallacies; @messeri2024illusions]. The cohorts are also small, enough to walk every path of the protocol rather than to estimate an effect. Our claim in the example study stays at the level of the notation: the pilot shows that the protocol ran as registered, not what the models can do. Whether the tasks measure the same constructs in artificial agents as in humans is an open question that the shared protocol makes testable rather than resolves [@bean2025construct].

# Future work

**[new; objections 1, 2, 3, 4, 6]** The first direction is a human cohort, and the evidence only people can give. Two studies would provide it.
- A replication of the example study's tasks with online participants, run from the same file, would exercise the path this paper designs for but does not demonstrate: data sent to the platforms laboratories use, sessions resumed after an interruption, and the participant flow counted as it runs.
- A comprehension study, itself written in Studyflow, would measure what the Limitations leave as a hypothesis: whether the notation is easier to read and to check. Researchers would be allocated at random to read the same study either as a diagram or as prose and code.

Both need what the reference implementation lacks today (@tbl-scope):
- trial lists registered with the protocol;
- analysis steps in R, and in scripts pinned by their content;
- data-protection measures for human records.

**[revised: "The first" → "The second"]** The second direction is machine authorship. *(rest of the current paragraph unchanged)*

**[revised: "The second" → "The third"; one optional sentence added]** The third direction is to standardize experimental science. *(current paragraph unchanged, then optionally:)* One file run unchanged at several sites is also what a multi-site replication needs, and each site's executed copy would differ from the others only in its records.

---

## Option B: one compact paragraph

Insert after the "human cohort" paragraph of the current Limitations. Add the Option A Future work paragraph only if space allows.

**[new; objections 1, 2, 3, 5, 6, 7]** The reference implementation also leaves parts of a study outside the file or outside what runs (@tbl-scope):
- **Trials.** What happens within a task is registered only when written into the settings wired to it. In the example study the Simon task draws each trial's congruency with its own generator, so the order of trials is recorded after the run but not registered before it.
- **Analysis.** It runs only as Python library calls, which makes it long: one paired *t* test takes twelve calls. R and mixed-effects models are not demonstrated.
- **Human data.** The browser runtime keeps a session's record in the browser rather than sending it to the platforms laboratories use, and does not resume an interrupted session.
- **Labels.** The labels on the diagram repeat some values as text that nothing checks.
- **Data protection.** A run's version-controlled history holds every exchange, so a human study needs data protection that is not yet built in.
- **Other designs.** Stratified allocation, minimization, return visits and EEG acquisition are described but not run.

Each is a matter of tooling rather than of the notation, and each is future work.

---

## Facts behind the text (modeler main, 2aff980c)

| Claim in the text | Evidence |
|:--|:--|
| Simon congruency is drawn by the task's own generator | paper-v3 Methods, Reproducibility paragraph; `Simon_Timeline` overrides only `ExitRules: Trials: 30` |
| Twelve library calls for the congruency test | six upstream (`pivot_table`, `reset_index`, `dropna`, `query`, `astype`, `merge`) plus five in "Accuracy cost per subject" (`pivot_table` ×2, `get` ×2, `Series.sub`) plus `ttest_1samp` |
| Python steps only | `skills/python` has a local runner only; no `r://` runner exists (an `r://` reference only appears as "a scheme no runner knows" in a test) |
| Browser keeps the record in the session | `packages/runtime-browser/src/session.ts` ("never written back"); "Download the run's record" button in `Runner.tsx`; Behaverse data server only when "Record events" is on; no resume |
| Containers not provided | `tbl-claims`: "External calls run in containers: not implemented" |
| Run history holds every exchange | `packages/runtime-local/src/prov.ts` commits the whole run directory; `events.jsonl` carries sent messages and replies |
| Stratification and minimization not applied | `packages/core/src/engine/allocation.ts` "unapplied" warning |
| EEG not run | `skills/eeg/SKILL.md`: "Nothing executes these elements yet" |
| Labels repeat values | `example_study.studyflow.yaml`: "> 20% unanswered" beside `max_unanswered: 0.2` |
