# Ubiquitous Language

Working vocabulary for the Studyflow paper (`elife/paper-v4.qmd`). This is guidance, not law: write naturally, and reach for these terms when precision matters or when one of the collisions at the end is in play.

## Core terms

| Term | Meaning |
| --- | --- |
| Studyflow | The notation, a BPMN 2.0 profile for experimental cognitive research. Capitalized everywhere except the `studyflow:` namespace prefix and the `.studyflow` file extension. |
| Study (S) | The formal object, a typed attributed directed multigraph. A Studyflow diagram is a study; the `.studyflow` YAML file is its serialization; the `.bpmn` XML is its interoperability projection. |
| Element | Any typed node or edge; each specializes a BPMN base type. |
| Language schema (Sigma) | The versioned LinkML schema defining element types, attributes, and validation rules, independent of any tool. |
| Coordination language | What Studyflow is in Gelernter and Carriero's terms. The notation carries the coordination (ordering, dependencies, data passing between stages) while the computations stay in the tools built for them. |

## Graphs and execution

| Term | Meaning |
| --- | --- |
| Sequence flow, G_ctrl | Control-flow edges and the directed (deliberately not acyclic) graph they induce; execution walks it. |
| Data association, G_data | Data-flow edges and the graph they induce; an analysis pipeline is a path through it. |
| Well-formed | Passing the four validity conditions (language schema, typed endpoints, sound control flow, valid BPMN XML). |
| Run | One administration of the whole protocol to one subject. |
| Study seed (s) | Combined with a subject identifier i, fixes the path, task order, stimulus order, and every branch draw. |
| Prospective and retrospective provenance | W3C PROV's names for the plan versus the executed record. A Studyflow file is prospective provenance at deposit and accumulates retrospective provenance (execution environment, seeds, attrition counts) as it runs; the deviation report is the diff between the two states. |

## Actors

| Term | Meaning |
| --- | --- |
| Actor | Anything implementing the observation-to-response exchange; the umbrella over humans and machines. |
| Participant | A human enrollee, in the CONSORT sense. |
| Subject | One enrolled instance walking the protocol (the i in the execution semantics), human or artificial. |
| Artificial agent | A non-human actor (a language model, a vision-language model, or a random baseline). |
| Runner, Modeler | The reference apps that execute and author diagrams, respectively. Any conforming engine is an executor; the runner is one executor among possible others. |
| Executor configuration | The pinned setup of an artificial actor (model id, digest, sampling parameters, trait prompt). |

## Views

| Term | Meaning |
| --- | --- |
| Projection | The operation pi_p(S). It discards elements, never adds or rewrites. |
| View | The result of a projection (Study, Gantt, Checklist, Figure). |

## Collisions worth avoiding

Only a few words genuinely bite when left bare; qualify them and move on.

- "schema": say language schema (validates diagrams) or data schema (validates datasets).
- "agent": say artificial agent for the umbrella term; bare `agent` is the specific actorType enum value.
- "marker": say marker analysis (the Flanker congruency anchor) or operation marker (the icon on a data operation).
- "runner" vs "executor": the runner is the reference app; an executor is any conforming engine.
- "view" vs "projection": the projection is the operation, the view is its result.

Everything beyond this (the long alias ban-lists and worked dialogues of earlier versions) proved more constraint than help. Trust context; consult the collision list when in doubt.
