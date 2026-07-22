# Ubiquitous Language

Domain glossary for the eLife paper *"Studyflow: an executable visual notation for experimental workflows in the cognitive sciences, from protocol to publication"* (`elife/paper-v2.qmd`). Use these terms consistently in the manuscript, figures, listings, and supplementary materials. Terms are grouped by subdomain; **flagged ambiguities** at the end record the collisions to guard against.

## The notation and the artifact

| Term | Definition | Aliases to avoid |
| --- | --- | --- |
| **Studyflow** | The domain-specific visual notation itself: a BPMN 2.0 profile for experimental cognitive research. | "the notation" / "the language" used bare where precision matters; lowercase *studyflow* as a noun |
| **`.studyflow` file** | The on-disk YAML serialization of a study; the file of record and the single source of truth. | "the file", "the artifact", "the source" used without antecedent |
| **Studyflow diagram** | A study as a typed graph, whatever its rendering (YAML, XML, or drawn figure). | "the diagram" used to mean a specific rendered view |
| **BPMN 2.0** | Business Process Model and Notation, the ISO/OMG host standard Studyflow specializes. | "BPMN" without the version on first use |
| **`.bpmn` projection** | The lossless BPMN 2.0 XML form of a `.studyflow` file, for generic-tool interoperability. | "the XML" |
| **Language schema (Σ)** | The versioned LinkML schema that defines Studyflow's element types, attributes, and validation rules independently of any tool. | bare "schema" (collides with *data schema* — see ambiguities); "the spec" |
| **Element** | Any typed node or edge in a diagram, each specializing a BPMN base type. | "box", "typed box", "component" |
| **Studyflow extension** | A schema `Σ'` that subclasses core types to add a domain, leaving the diagram valid BPMN 2.0. | "plugin", "fork" |

## The formal object

| Term | Definition | Aliases to avoid |
| --- | --- | --- |
| **Study (S)** | The formal object: a typed, attributed directed multigraph over the language schema. | "graph" unqualified |
| **Node** | A vertex of the study graph (event, activity, gateway, actor, or data element). | "step" (reserve for the execution transition) |
| **Edge** | A directed connection between nodes, either a sequence flow or a data association. | "arrow", "link" |
| **Sequence flow** | A control-flow edge; the set of them induces the control flow graph `G_ctrl`. | "flow" unqualified |
| **Data association** | A typed edge joining a data element to a flow node; induces the data flow graph `G_data`. | "dashed edge" in prose (use in captions only) |
| **Well-formed** | A diagram satisfying the four validity conditions (schema, typed endpoints, sound control flow, valid BPMN XML). | "valid" used loosely, "correct" |
| **Control flow (`G_ctrl`)** | The directed (not acyclic) graph of sequence flows that execution walks. | "the DAG" (it is deliberately *not* a DAG) |

## Study lifecycle and design

| Term | Definition | Aliases to avoid |
| --- | --- | --- |
| **Protocol** | The study seen as a registered plan, before the run. | "the file" (a protocol is a role a file plays, not the file itself) |
| **Example study** | The single demonstration study that exercises the notation end to end. | "the example study", "the experiment" |
| **Battery** | The ordered set of cognitive tasks administered to each actor. | "cognitive tests" |
| **Task** | One instrument node in the battery (a cognitive task, questionnaire, instruction, rest, or video game). | bare "task" for a BPMN base type — say *`bpmn:Task`* |
| **Trial** | One stimulus–response exchange within a task. | "item", "round" |
| **Run** | One administration of the whole protocol to one subject (k = 30 runs per condition). | "session" (reserve for humans), "participant" |
| **Session** | A single human sitting through the battery (~45 min). | "run" |
| **Condition** | One cell of the factorial (a model × trait × task × path combination). | "cell", "arm", "group" used interchangeably |
| **Trait** | The disposition manipulation on an actor (baseline vs. a careful persona). | "persona" as the manipulation name (a persona is one *value* of the trait) |
| **Attrition** | Participants leaving the flow, encoded as boundary error events. | "dropout" and "loss to follow-up" as separate concepts (they are the same edge) |
| **Amendment** | An edit from a registered file `F` to a revised file `F'`. | "revision", "change" used loosely |

## Actors and execution

| Term | Definition | Aliases to avoid |
| --- | --- | --- |
| **Actor** | Anything that implements the observation→response function; the umbrella abstraction over human and artificial performers. | "user", "player" |
| **Participant** | A *human* enrollee in the CONSORT sense. | using "participant" for artificial actors or for the BPMN pool |
| **Subject** | One enrolled instance walking the protocol, identified by `i` in the execution semantics. | "participant" (subject spans humans and agents), "user" |
| **Artificial agent** | A non-human actor (a language model, a vision-language model, or a random baseline). | bare "agent" where the `agent` actorType is also in play (see ambiguities); "AI", "bot" |
| **Runner** | The reference browser application that executes a diagram node by node. | "player", "engine", "interpreter" |
| **Modeler** | The reference browser application that authors, validates, simulates, and publishes diagrams. | "editor", "designer" |
| **Executor** | Any conforming agent or engine that runs a `.studyflow` file (the property R7 "executor agnostic" names). | conflating with *runner* (the runner is one executor) |
| **Executor configuration** | The pinned record of an artificial actor's setup (model id, digest, sampling params, trait prompt, context policy). | "model config", "settings" |
| **Executor interface** | The single message-passing (observation/response) interface through which the runner administers every actor. | "API", "harness" |
| **Observation** | The per-trial message to an actor (stimulus, allowed responses, timing, and rendered frame where needed). | "prompt" (a prompt is one encoding of an observation), "input" |
| **Response** | What an actor returns for a trial, optionally with a response time. | "answer", "output" |
| **Actor pool** | The BPMN `Participant` element typed `human`, `llm`, `agent`, or `instrument`. | "lane", "swimlane" |

## Analysis and data

| Term | Definition | Aliases to avoid |
| --- | --- | --- |
| **Analysis pipeline** | The typed nodes inside the diagram that specify the analysis; the pipeline *is* the preregistration. | "script", "notebook", "code" |
| **Data operation** | A pipeline step typed by its transformation (read, filter, map, branch, reduce, render/write). | "function", "stage" |
| **Operation marker** | The icon on an activity naming the data operation it performs. | "marker" bare (collides with the *marker analysis* — see ambiguities) |
| **Marker analysis** | The Flanker congruency-effect analysis used as a within-task validity anchor. | "marker" bare; "the congruency test" as if a hypothesis test |
| **Agreement (analysis)** | The TOST equivalence test on the accuracy difference between two conditions. | "equivalence" unqualified |
| **Divergence (analysis)** | The AUC-of-a-classifier test of whether two conditions are distinguishable. | "difference test", "separability" |
| **Data contract** | The typed schema binding on a dataset that lets a downstream step's column use be validated against upstream production. | "interface", "type check" |
| **Dataset** | A typed data node declaring a format (BDM, BIDS, Psych-DS, CSVW) and a data schema. | "data", "file" |
| **Data schema** | A CSVW (or LinkML/JSONSchema) schema bound to a dataset or table — the `Schema` element. | bare "schema" (collides with *language schema* — see ambiguities) |
| **Trials table** | The per-trial behavioral record; the release format itself, not a summary of it. | "results", "the data", "log" |

## Views

| Term | Definition | Aliases to avoid |
| --- | --- | --- |
| **View** | A projection of the study that discards elements but never adds or rewrites (Study, Gantt, Checklist, Figure). | "rendering", "output", "export" as a synonym for *view* |
| **Projection** | The operation `π_p(S)` that produces a view from a predicate over elements. | "filter", "transform" |
| **Study view** | The view that keeps every element. | "full diagram" |
| **Gantt view** | The view placing elements with an onset or duration on a time axis (the SPIRIT schedule). | "timeline", "schedule" unqualified |
| **Checklist view** | The view flattening the diagram into items and status for running and guideline audits. | "audit", "report" |
| **Figure view** | The view rendering a visible subset whose exported SVG embeds the source. | "the figure", "publication export" |

## Reproducibility guarantees

| Term | Definition | Aliases to avoid |
| --- | --- | --- |
| **Determinism** | The property that `(F, s, i)` plus the input sequence fixes the entire visited-node walk. | "reproducibility" unqualified |
| **Amendment stability** | The property that an edit leaves the random draws of every untouched element bit-identical at the same seed, because draws are keyed by element identifier. | "stability", "seed stability" |
| **Study seed (s)** | The seed that, combined with a subject identifier `i`, derives each subject's path, task order, stimulus order, and branch draws. | "the seed" without saying which |
| **Deviation report** | The diff between the registered `.studyflow` file and the as-run file. | "changelog", "amendment log" |

## Relationships

- A **Studyflow diagram** *is* a **study (S)**; a **`.studyflow` file** is its serialization, and a **`.bpmn` projection** is its interoperability form.
- A **study** is validated against the **language schema (Σ)**; a **dataset** is validated against a **data schema**. These are two different "schemas."
- A **study** contains one **battery**; a **battery** contains many **tasks**; a **task** contains many **trials**.
- A **run** administers the whole protocol to one **subject**; a **subject** is either a **participant** (human) or an **artificial agent**.
- The **runner** administers every **actor** through the one **executor interface**; the **runner** is one **executor** among possible others.
- Every **view** is a **projection** of the one **study**; a projection only discards, so views cannot drift.
- **Attrition** is one **boundary error event** per exit; the **deviation report** is the diff of the registered vs. as-run file.
- The **analysis pipeline** is typed **nodes** inside the **study**, so the pipeline is the preregistration.

## Example dialogue

> **Reviewer:** "You call the whole thing a *schema* in two places — is the thing that validates the diagram the same thing that validates a dataset?"
>
> **Author:** "No, and that is the one collision to fix. The **language schema** is the LinkML `Σ` that defines what elements and attributes a diagram may contain. A **data schema** is the CSVW schema bound to a **dataset** — the `Schema` element on the data flow graph. Different objects, different validators."
>
> **Reviewer:** "And an *actor* versus a *participant* — the N-back is administered to both?"
>
> **Author:** "The **actor** is the abstraction: anything implementing observation→response. A **participant** is specifically a human enrollee, the CONSORT sense. When I need the executing instance regardless of kind, I say **subject** — that is the `i` in the walk. A language model is an **artificial agent**, never a *participant*."
>
> **Reviewer:** "The congruency *marker* and the operation *marker* — same word, same figure panel."
>
> **Author:** "Right. The **marker analysis** is the Flanker congruency effect, a validity anchor. The **operation marker** is the icon on a **data operation** node. I will always qualify both so *marker* never stands alone."
>
> **Reviewer:** "One diagram is the protocol *and* the report?"
>
> **Author:** "One **study**, projected. The **Gantt view** is the SPIRIT plan, the **Checklist view** is the audit, and the **Figure view** is the CONSORT flow after the run. The **deviation report** is just the diff between the registered file and the as-run file — the attrition counts the **runner** wrote onto the **boundary error events**."

## Flagged ambiguities

- **"schema" is overloaded** — it names both the **language schema (Σ)** that defines Studyflow (LinkML, one per notation version) and a **data schema** (CSVW/LinkML/JSONSchema) bound to an individual **dataset** (the `Schema` element). These are distinct concepts on distinct graphs. Recommendation: never write bare "schema"; qualify as *language schema* or *data schema* on every use. Currently the manuscript relies on context (e.g., "a versioned schema defines the language" in the abstract vs. "declares its format … and a schema" in Data contracts).

- **"agent" is overloaded** — in prose it is the umbrella term for any non-human actor (LLMs and VLMs included: "artificial agents", "agent cohort"), but in the `actorType` enum `human | llm | agent | instrument` it is a *specific* value distinct from `llm`. A reader cannot tell whether "the agents" includes the language models or excludes them. Recommendation: use **artificial agent** for the umbrella in prose, and reserve bare `agent` for the actorType value (an autonomous, tool-using actor as opposed to a plain `llm`). Consider renaming the enum value to something like `autonomous-agent` if the distinction matters.

- **"marker" is overloaded** — the **marker analysis** (Flanker congruency effect, a validity anchor) and the **operation marker** (the icon typing a data operation) appear in the same Results/Figure 6 context. Recommendation: always qualify — *marker analysis* and *operation marker* — never bare "marker".

- **"actor" vs. "participant" vs. "subject"** — the manuscript uses "participant" for humans, for the BPMN `Participant` pool, and inside "participant flow" (CONSORT), while "actor" is the human-or-artificial abstraction and "subject" (`i`) is the walking instance. Recommendation: **actor** = the abstraction, **participant** = human enrollee only, **subject** = one enrolled instance in the execution semantics, **actor pool** = the BPMN `Participant` element. Keep "participant flow" as the fixed CONSORT term of art.

- **"Studyflow" vs. "studyflow" casing** — the proper-noun notation is capitalized (*Studyflow*), but the manuscript frequently lowercases it as an adjective ("studyflow diagram", "studyflow notation", "the studyflow file", and typos "studlofw"/"studfylow"). The namespace prefix `studyflow:` is correctly lowercase. Recommendation: capitalize **Studyflow** everywhere except the `studyflow:` namespace prefix and the `.studyflow` extension; fix the typos.

- **"runner" vs. "executor" vs. "runtime"** — **runner** is the reference application, **executor** is any conforming execution agent (R7), **executor configuration** is a model's pinned setup, and `runtime` is a study-container attribute. These are close enough to blur. Recommendation: keep the four distinct and never use "executor" to mean the reference app (that is the **runner**).

- **"view" vs. "projection" vs. "rendering"** — used interchangeably ("Every rendering of the study is a projection"). Recommendation: **projection** = the operation, **view** = its result; avoid "rendering" as a synonym (reserve it for the literal drawing a runner or GUI paints).
