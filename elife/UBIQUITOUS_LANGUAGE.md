# Ubiquitous Language

Working vocabulary for the Studyflow paper (`elife/paper-v3.qmd`). This is guidance, not law: write naturally, and reach for these terms when precision matters or when one of the collisions at the end is in play.

## Core terms

| Term | Meaning |
| --- | --- |
| Studyflow | The notation, a BPMN 2.0 profile for experimental cognitive research. Capitalized everywhere except the `studyflow:` namespace prefix and the `.studyflow.yaml` file extension. |
| Study (S) | The formal object, a typed attributed directed multigraph. A Studyflow diagram is a study as drawn; the `.studyflow.yaml` file is its serialization and what is sealed, deposited, diffed, validated and run; BPMN 2.0 XML is its export, not a projection. |
| Element | Any typed node or edge; each specializes a BPMN base type. |
| Language schema (Sigma) | The versioned schemas defining element types, attributes, and validation rules, independent of any tool: one or more per skill, each with its own prefix, the core one required. |
| Coordination language | What Studyflow is in Gelernter and Carriero's terms. The notation carries the coordination (ordering, dependencies, data passing between stages) while the computations stay in the tools built for them. |
| FEEL | The expression language of DMN, BPMN's sibling OMG standard. Every condition and data selection a file writes is FEEL; the validator rejects one that is not, and both reference runtimes evaluate the same subset. |

## Graphs and execution

| Term | Meaning |
| --- | --- |
| Sequence flow, G_ctrl | Control-flow edges and the directed (deliberately not acyclic) graph they induce; execution walks it. |
| Data association, G_data | Data-flow edges and the graph they induce; an analysis pipeline is a path through it. |
| Well-formed | Passing the four validity conditions (language schema and FEEL, typed endpoints, connected control flow, valid BPMN XML export). |
| Run | One administration of the whole protocol to one subject. |
| Study seed (sigma) | Fixes every random draw: a gateway's from the seed, the gateway, the participant and that participant's visit; a timeline's from the seed and the step; a simulated participant's from the seed and each message's identity. A language model's responses are sampled, not seeded. |
| Prospective and retrospective provenance | W3C PROV's names for the plan versus the executed record. A Studyflow file is prospective provenance at deposit and accumulates retrospective provenance (the tool, the seed, the protocol digest, attrition counts) as it runs; the deviation report is the diff between the two states. |
| Sealed, deposited | Sealed: the file's protocol digest is recorded, so any later change to the protocol shows. Deposited: archived where a timestamp proves when it was registered. The example study was sealed and run, not deposited first. |
| Fingerprint | The main text's word for the protocol digest (Methods keeps "digest"). |
| Discontinuation rule | The main text's word for a task's conditional boundary event that sends a subject to the Discontinued exit. |
| Data dictionary | The main text's word for a dataset's data schema (a CSVW schema in the example study). |
| Claim state | The end event a registered question reaches: Supported, Not supported, or Not testable, decided by a rule drawn in the file before any run. |

## Actors

| Term | Meaning |
| --- | --- |
| Actor | Anything implementing the observation-to-response exchange; the umbrella over humans and machines. |
| Participant | A human enrollee, in the CONSORT sense. |
| Subject | One enrolled instance walking the protocol (one instance of the subjects' pool), human or artificial. |
| Simulated participant | A runner-only actor of the `simulate` skill (`simulate://planted`, `simulate://null`) that answers each trial correctly with a set probability; the example study's cohort, not a participant in the CONSORT sense. |
| Planted truth | An effect built into simulated participants, so the correct outcome of each registered question is known before the run; the null twin plants nothing. |
| Artificial agent | A non-human actor (a simulated participant or a language model); the umbrella term. |
| Instruction condition | The main text's name for the two arms (cautious, impulsive); the study file's labels call them dispositions. |
| Pilot | What the example study's run is: artificial agents take every element of the protocol so that it can be checked as registered; its questions exercise the registered analysis, not hypotheses about the subjects. |
| Modeler, reference runtimes | The modeler authors diagrams. The two reference runtimes execute them: the local runtime (`studyflow run --runtime local`) walks the whole study and writes its record into the executed copy; the browser runner walks one process, one screen at a time, and keeps its record in the session. |
| Executor configuration | What a language model's runner records with every exchange (model digest and quantization, sampling parameters, server version, request and reply); the file names the model but cannot set its sampling. |

## Views

| Term | Meaning |
| --- | --- |
| Projection | The mapping pi_p(S) from the study to what one audience reads. It discards elements, never adds or rewrites. |
| View | What a projection renders (Study, Gantt, Checklist, Provenance, Manuscript Figure). |

## Collisions worth avoiding

Only a few words genuinely bite when left bare; qualify them and move on.

- "schema": say language schema (validates diagrams) or data schema (validates datasets).
- "agent": say artificial agent for the umbrella term; `actorType` names an actor's kind (`human`, `software`, `hardware`, `llm`).
- "marker": say loop or multi-instance marker (BPMN's) or operation marker (the icon on a data operation).
- "runner" vs "runtime": the local runtime and the browser runner are the reference runtimes; a skill's runner executes the elements that skill claims; any conforming engine is an executor.
- "view" vs "projection": the projection is the mapping, the view is what it renders.
- "sound": the third validity condition is *connected* (every flow node on a path from a start to an end event), weaker than the soundness of workflow nets.
- "draw": depicting on the diagram; sampling is a random draw.

Everything beyond this (the long alias ban-lists and worked dialogues of earlier versions) proved more constraint than help. Trust context; consult the collision list when in doubt.
