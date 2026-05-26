# Studyflow: a BPMN-based notation, modeler, and runner for end-to-end specification of experimental research workflows in cognitive sciences

**Authors:**
Morteza Ansarinia^1,\*^ (ORCID 0000-0001-8335-6704),
Hoorieh Afkari Roshan^1^ (ORCID 0000-0003-4787-8331),
Pedro Cardoso-Leite^1^ (ORCID 0000-0002-2848-5527)

^1^ University of Luxembourg, Luxembourg
^\*^ Corresponding author: morteza.ansarinia@uni.lu

## Abstract

A scientific study passes through many hands — designer, ethics reviewer, participant, data engineer, analyst, reviewer, replicator — and each typically receives a different artifact: a protocol PDF, an experiment script, a preprocessing notebook, a manuscript figure, a CONSORT diagram. These artifacts drift apart, and no single representation describes the study as it was actually run. We present **Studyflow**, a notation, modeler, and runner that closes this gap by extending Business Process Model and Notation (BPMN) with elements specific to experimental cognitive science: domain-specific activities (cognitive task, questionnaire, instruction), gateways for randomization and eligibility, data operations (map, filter, reduce, group), and data elements bound to community schemas (BIDS, Psych-DS, BDM, CSVW). A single `.studyflow` file serves as protocol, specification, publication figure, and participant-facing runtime. We describe the language, an open-source modeler, and a client-side runner, and demonstrate end-to-end use on a CONSORT-style trial, an N-back task, and a reproducible analysis pipeline.

## Impact statement

Studyflow turns a scientific study into a single source-of-truth diagram that can be reviewed, executed, and published, replacing the divergent artifacts (protocols, scripts, pipeline configs, reporting diagrams) that currently fragment experimental research across stakeholders.

## Keywords

scientific workflows; BPMN; reproducibility; experimental design; cognitive science; MLOps; process modeling


---

# 1. Introduction

## 1.1 The reproducibility gap is in *processes*, not just data

A scientific study touches many people and systems. A researcher designs it; an ethics reviewer approves it; a participant runs it; a data pipeline ingests it; a model trains on it; a reviewer reads it in a manuscript; a replicator tries to rebuild it. Reproducing the study after the fact requires more than the data and the manuscript: it requires an explicit, complete description of the *processes* that generated them [@aguilar2022experiments; @momeni2026guidelines]. A complete description of any computing system needs both a data model and a process model [@Sehgal2011]; in the life sciences and cognitive sciences, however, most standardization effort has gone into data, leaving the processes that produce the data documented in narrative prose, ad-hoc lab conventions, or code repositories that drift apart from the prose they accompany [@bell2021perspectives; @osc2015].

The cost of this asymmetry is visible whenever a study has to be re-read by anyone other than its author. The researcher's protocol PDF, the ethics application, the experiment script, the preprocessing notebook, the model card, the manuscript figure, and the CONSORT diagram begin as different views of the same study and end as inconsistent ones. By the end, no single thing describes the study *as it was actually run*. Trust in research, and increasingly trust in code and data on which research depends, is built or lost at exactly that junction.

We argue that reproducibility should be a property of the artifact itself rather than a separate documentation effort maintained alongside the work — *trust by construction*. A single, machine-readable, human-understandable representation of a study, shared across its audiences, would force the process model and the data model to stay aligned. The contribution of this paper is one concrete realization of that idea, grounded in a standard process notation and a working open-source toolchain.

## 1.2 Current practice fragments the study across artifacts

Today, the audiences listed above each receive a different artifact, and each artifact drifts from the others. We can sort current approaches into four overlapping families.

**Box-and-arrow figures** in manuscripts and protocols communicate study logic at a glance but are not standardized, not machine-checkable, and rarely connect to the code that runs the study. They are tailored to each stakeholder (a CONSORT flow for a journal, a slide deck for a funder, a sketch on a whiteboard for an engineer) and so are difficult to keep mutually consistent [@visualmodelinglanguagesscopingreview]. **Checklists and pre-registration forms** address the need for structured text but encode it in free-form fields, in proprietary PDF or DOCX, on data silos that resist version control [@barrowman2020vtree]. **Data standards, ontologies, and packages** (BIDS, Psych-DS, the Behaverse Data Model, CSVW [@bids; @psychds; @bdm; @csvw]) make the data side machine-readable but say little about the procedure that produced the data, and ontology-based process models, while numerous, demand high upfront effort and are rarely reused [@norouzi2025semantic_processes]. **Code and configuration** (analysis scripts, GitHub Actions, Nextflow [@kinsman2021], protocol registries such as protocols.io [@teytelman2016]) make pipelines precise but require programming literacy that excludes ethics boards, reviewers, and many collaborators.

The recurring pattern is a split between **execution** and **communication**: tools that execute the study (scripts, workflow engines, CI pipelines) target developers and machines; tools that communicate the study (protocol PDFs, narrative platforms, reporting checklists) target humans. Provenance systems track the computational graph well but rarely capture the full experimental context — randomization decisions, manual annotations, protocol deviations — creating a boundary between a well-tracked computational graph and a partially represented experimental graph [@souza2020provenance; @simmons2018provenance_sport]. No single representation currently spans the full lifecycle of a study in a form that scientists, engineers, ethics boards, and journal editors can all read, validate, and execute (Figure 1).

## 1.3 BPMN as a foundation

Business Process Model and Notation (BPMN) is a mature ISO-standard graphical language for processes [@white2004introduction]. It already provides what scientific workflows need at the structural level: events, activities, sub-processes, exclusive/parallel/inclusive gateways, data objects and stores, sequence and message flows, and choreography between participants. It has an established tooling ecosystem (editors and renderers such as `bpmn-js` and Camunda Modeler, drawing libraries such as diagrams.net) and a body of accumulated practice in industries where process clarity is not optional. Building on BPMN gives any domain-specific extension a shape vocabulary that engineers and analysts already recognize, plus a serialization (BPMN 2.0 XML) that survives outside any single tool.

BPMN's extension mechanism — `extensionElements` and namespaced attributes — is the bridge we use. The standard permits domain-specific elements and attributes to be added inside a vendor namespace; a BPMN-only parser ignores them gracefully, while a domain-aware tool can validate and render them [@magnani2009bpdmn]. Existing BPMN extensions in adjacent domains demonstrate the pattern: BPMN4CP for clinical pathways [@braun2014], BPMN4sML for serverless machine-learning pipelines [@tetzlaff2022bpmn4sml], extensions for human–AI collaboration [@ait2024bpmn_humanagent], and applications to healthcare more broadly [@pufahl2022]. A systematic review identifies dozens more profiles across domains [@zarour2019]. Cognitive and behavioural research is conspicuously absent from this list.

Recent large-language-model-assisted BPMN authoring tools (ProMoAI, BPMN-ChatBot, and related work [@kourani2024promoai; @kourani2024process_modeling_llm]) accelerate diagram authoring from text, but evaluations show that competitive syntactic quality does not translate into domain-specific semantics or domain-specific validation [@lauer2026assessing]. Authoring help is welcome; it is not a substitute for a profile that defines what *cognitive task*, *random assignment*, or *eligibility check* mean inside a process model. That profile is the gap Studyflow fills.

## 1.4 Contributions and roadmap

We contribute five artifacts, each independently usable:

1. **A versioned language specification** for Studyflow, authored as a LinkML schema [@moxon2025linkml] that serves as the single source of truth for element types, attribute constraints, and validation rules. LinkML is a schema-modeling framework increasingly adopted across biology, biomedicine, and ontology engineering, and provides FAIR-aligned [@fair] serialization plus tooling for documentation, validator, and downstream-converter generation. The Studyflow LinkML schema is independent of any particular implementation: a third party can target it directly without depending on the modeler's code.

2. **A layered set of runtime schemas** mirroring the LinkML specification as moddle YAML — the format `bpmn-moddle` consumes — comprising the language core (`studyflow`), a companion cognitive schema (`cognitive`), and four optional domain extensions (`behaverse`, `omniprocess`, `datatrove`, `galea`). New domain semantics plug in without touching the core.

3. **A library of worked example diagrams** that ship with the modeler, including a 423-line CONSORT-2025 randomized trial, a 378-line SPIRIT-2025 protocol schedule, and patterns for cognitive tasks, data collection, analysis pipelines, MLOps, multi-agent choreography, and reporting guidelines.

4. **The Studyflow Modeler**, an open-source client-side web application (React with `bpmn-js`; MIT-licensed) for authoring, inspecting, simulating, validating, and publishing `.studyflow` diagrams. Its inspector and palette are generated from the schemas, so the language and the editor stay in sync.

5. **The Studyflow Runner**, a separate client-side application that parses, validates, and walks a `.studyflow` file participant-by-participant. It ships with built-in renderers for consents, instructions, questionnaire instruments (PHQ-9, GAD-7, BDI-II), generic tasks, and embedded Behaverse cognitive-task runtimes, and supports seeded determinism for reproducible random branches.

The remainder of the paper is organised as follows. §2 describes the language, modeler, and runner, and demonstrates them end-to-end on a CONSORT-style randomized controlled trial (§2.5), an N-back cognitive task authored, published, and run on the runner (§2.6), and a reproducible reaction-time analysis pipeline (§2.7). §2 also examines how Studyflow covers existing reporting guidelines (§2.8), how process and data fit in one diagram (§2.9), how MLOps workflows can be expressed in the same notation (§2.10), and how multi-agent studies are modelled via BPMN choreography (§2.11). §3 discusses what Studyflow changes for the field, its relationship to neighbouring ecosystems, current limitations, and directions for community-led extension. §M (Methods) details the LinkML schema and its moddle YAML runtime mirror, the BPMN extension mechanism, and the architectures of the modeler and runner.


---

# 2. Results

§2 is organized in three movements. The first (§2.1–§2.4) describes Studyflow's working artifacts — the language, the modeler, and the runner — together with the three rendering views (Study, Timeline, Checklist) that let one source file serve readers with different needs. The second (§2.5–§2.7) demonstrates the language end-to-end on three workflows: a CONSORT-style randomized controlled trial, an N-back cognitive task authored, published, and run on the runner, and a reproducible reaction-time analysis pipeline. The third (§2.8–§2.11) maps Studyflow onto adjacent territory: coverage of reporting guidelines beyond CONSORT, the integration of process and data in one diagram, the application to MLOps workflows, and multi-agent studies via BPMN choreography.

## 2.1 The Studyflow language

Studyflow is a domain-specific profile of Business Process Model and Notation (BPMN) 2.0 [@white2004introduction] tailored to experimental research in cognitive sciences. We adopted BPMN as the host notation rather than inventing a new language for three reasons. First, Studyflow diagrams remain valid BPMN 2.0 XML and open in any compliant tool (Camunda Modeler, bpmn.io, diagrams.net), with Studyflow-specific elements degrading gracefully. Second, BPMN's flowchart-like visual grammar is already familiar to many researchers, lowering adoption barriers. Third, BPMN provides a formal extension mechanism (`extensionElements`, namespaced attributes) for adding domain semantics without breaking the base standard [@stroppi2011; @magnani2009bpdmn].

**What Studyflow inherits.** Studyflow reuses BPMN's full vocabulary for control flow and structure: start, end, intermediate, boundary, timer, and error *events*; tasks, sub-processes, and call activities; exclusive, parallel, inclusive, event-based, and complex *gateways*; sequence flows and message flows; data objects and data stores with their associations; pools and lanes; and choreography for multi-agent interactions. These elements render with standard BPMN shapes and behave exactly as specified by the OMG.

**What Studyflow adds.** Four areas extend BPMN with vocabulary that experimental research routinely needs. (i) A top-level **`Study`** container element extends `bpmn:Process` and carries study-level metadata (name, version, authors, runtime). (ii) **Domain-specific activity types** specialize the generic BPMN task into `CognitiveTask`, `Questionnaire`, `Instruction`, `Rest`, `VideoGame`, `BehaverseTask`, `Script`, and `Manual`, each rendering with a distinctive icon while remaining a normal BPMN task underneath. (iii) **Research-specific data elements** — `Dataset`, `Table`, `Array`, `Schema`, `DataCatalog`, `Snapshot` — augment BPMN's generic `DataObject`/`DataStore` with bindings to community standards (BIDS [@bids], Psych-DS [@psychds], Behaverse Data Model, CSVW). A small **data-operations vocabulary** (`Map`, `Filter`, `Reduce`, `Group`, `FlatMap`, `Transform`, `Compose`) renders as a task marker, making *how* data is transformed explicit. (iv) **Research gateways** — `RandomGateway`, `StratifiedAllocationGateway`, `EligibilityGateway` (inclusion/exclusion criteria as markdown lists) — encode the branching patterns specific to experimental design. **Temporal attributes** (start/end time, duration, progress, resource allocation) attached to activities let trial timelines and Gantt views be derived from the same diagram (§2.4).

**What Studyflow deliberately leaves alone.** Studyflow does not redefine BPMN's serialization conventions: XML namespaces, element IDs, and the base shape vocabulary are untouched. Extensions live in a `studyflow:` (and per-extension) namespace inside `<extensionElements>`, so a generic BPMN renderer ignores them gracefully while a Studyflow-aware tool validates and renders them consistently.

**A layered set of schemas.** The vocabulary is partitioned into a small core and optional domain extensions that can be loaded on demand (Figure 2). The core comprises **`studyflow`** (`Study`, events, sequence flows, base activity, data infrastructure) and **`cognitive`** (cognitive tasks, questionnaires, instructions, rest, video games, and the three research gateways). Four optional schemas — **`behaverse`** (Behaverse Unity tasks), **`omniprocess`** (process-orchestration primitives), **`datatrove`** (large-scale data transformation operators), and **`galea`** (EEG/eye-tracking acquisition) — can be enabled per diagram, and new domains plug in by authoring a moddle YAML schema without modifying the core. The complete element catalog is provided in Supplementary Table S1.

## 2.2 The Studyflow Modeler

The **Studyflow Modeler** is an open-source web application (React 19, `bpmn-js` 18, MIT license) that operationalizes the Studyflow language for authoring, inspecting, simulating, and publishing diagrams. It is a client-side application without a server dependency, continuously deployed at <https://behaverse.org/studyflow-modeler/>. Two design choices shape the modeler. First, the language specification is maintained as a versioned LinkML schema [@moxon2025linkml] independent of the modeler codebase, so third-party tools (linters, converters, execution engines) can target the same specification. The modeler tracks the schema rather than owning it. Second, the user interface is **schema-driven**: palette entries, the inspector panel, and validation rules are generated from the layered moddle schemas (§2.1). Adding an element type or attribute to a schema updates the UI without manual UI work, which has so far kept the modeler lightweight while the notation evolves with community feedback.

The authoring workflow (Figure 3) proceeds in seven steps. (1) **Sign in.** Users open the modeler at `app.html`. A Behaverse API key unlocks publish; guest mode supports draft-only authoring. (2) **Drag from the palette.** The left palette exposes the BPMN base vocabulary alongside the Studyflow-specific elements (cognitive task, questionnaire, instruction, random gateway, eligibility gateway, dataset, etc.); optional schemas can be toggled from the palette settings. (3) **Edit in the inspector.** Selecting an element opens a right-hand inspector sidebar whose fields are derived from the element's schema entry: required attributes are flagged, enumerated values become dropdowns, markdown fields render with a preview, and conditional attributes appear only when their predicate holds. (4) **Connect elements.** The connect tool wires sequence flows, data associations, and message flows; the modeler picks the appropriate edge type from the source/target pair. (5) **Save and export.** Diagrams persist as `.studyflow` files — BPMN 2.0 XML with Studyflow extensions in named namespaces — so they diff cleanly in Git and remain valid BPMN. Export to PNG and SVG produces publication-ready figures; SVGs can embed the source XML for one-file commits. (6) **Simulate.** A simulation mode steps through the diagram interactively, exercising gateway logic and showing the next admissible elements, which is useful for catching dead branches and missing conditions before a study runs. (7) **Publish.** *File → Publish* uploads the diagram to the Behaverse Data Server [@bds], which renders its own participant-facing UI from the diagram structure (Local layout in the modeler is for human readers; the server ignores it.) Each publish creates a new server-side version, so studies already in the field do not break when authors push updates.

This separation between specification (the LinkML schema), authoring tool (the modeler), runtime UI (the data server), and visual layout (export artifacts) lets each component evolve independently while a single `.studyflow` source ties them together.

## 2.3 The Studyflow Runner

The **Studyflow Runner** is a distinct client-side application that takes a `.studyflow` file and walks a participant through it node by node. It lives at `run.html` alongside the modeler. Three entry paths bring a diagram in: clicking *Run* in the modeler toolbar (the diagram is serialized to local storage and the runner opens in a new tab), appending `?studyflow_url=<URL>` to fetch a hosted file, or opening `run.html` directly and uploading a `.studyflow`/`.bpmn`/`.xml` file from disk. An optional `?seed=N` integer makes random branches deterministic, supporting reproducible pilot runs and regression tests.

After loading, the runner **parses** the XML using the bundled `studyflow` and `cognitive` schemas plus any optional extensions the diagram declares; **pre-fetches** the Behaverse runtime manifest only when the diagram contains a `BehaverseTask`; **validates** the diagram (each node kind contributes its own validator for missing required attributes, unsupported types, malformed conditions; issues appear in a logs panel and the run aborts with `phase=invalid`); and **traverses** the flow from the `StartEvent`. Each visited node yields a *job*; the runner renders the corresponding React component and waits for the participant to complete or skip the step. On reaching the `EndEvent`, the run finishes with `phase=done`.

**Gateway semantics.** `RandomGateway` selects an outgoing branch uniformly at random, seeded by `?seed`. `StratifiedAllocationGateway` currently falls back to the same uniform pick; stratification logic is reserved for future work. Exclusive and inclusive gateways evaluate `conditionExpression` against a runtime *variable bag* (nodes write to it via `setVariable(name, value)`); the first truthy flow wins, with fallback to the `default` flow then to the first unconditioned flow. `ParallelGateway` is not yet supported.

**Built-in node kinds.** Six kinds ship with the runner: **Start** (consent screen if `consentFormUri` is set, otherwise immediate advance), **End** (issues a `none`/`static`/`dynamic` completion code and redirects via `redirectTo`), **Instruction** (markdown content + Continue), **Questionnaire** (renders the chosen `instrument`; PHQ-9, GAD-7, BDI-II ship as built-ins), **Behaverse Task** (embeds the Behaverse Unity runtime in an iframe and bridges messages), and a **Generic Task** fallback for any plain `bpmn:Task`/`UserTask`/`ServiceTask`. Other element kinds (data references, sub-processes not traversed inline) are skipped at run time — they affect modeling and analysis, not execution.

**Runtime extensibility.** New node kinds plug in by adding a folder under `src/runner/nodes/<kind>/` with a `match` predicate (typically keyed on `extensionType: '<schema>:<Type>'`), a `toJob(node)` mapper, and a React `Component`; a `registerNode(...)` call at module load wires it in. A domain group can thus ship a custom step (e.g. an eye-tracking calibration) without forking the runner.

Figure 4 [GAP: a four-to-six-panel walkthrough of a participant moving from consent through an instruction, a questionnaire, and a Behaverse cognitive task to the end screen, on the same diagram authored in §2.2.]

## 2.4 The three views: Study / Timeline / Checklist

A single `.studyflow` source is rendered three ways, each tuned to a different stakeholder need (Figure 5). The three views read the same file, so changes propagate automatically.

**Study view.** The default rendering: a BPMN-like graph showing every element and connection. The Study view is *structural* — it shows what happens and in what order but does not commit to wall-clock timing. It is the canonical view for Methods sections, for reviewers checking logical structure, and for pipeline authors wiring up data flow.

**Timeline view.** A Gantt-style rendering that places time-sensitive elements along a temporal axis. BPMN has timer events but no native way to express activity duration, scheduled start/end, or progress. Studyflow attaches these as optional element attributes: **start/end time**, **duration**, **progress** (percentage or label), and **resource allocation** (personnel, equipment, budget — expressed as lanes or pools). When these attributes are present, the Timeline view renders the diagram as a Gantt chart automatically. The same mechanism scales from trial-level timing (stimulus duration, ITI, response window) to study-level timing (visit schedule, follow-ups). Milestones are the special case where start and end coincide, and hierarchical Gantt structures map directly onto BPMN sub-processes. Timeline views are particularly useful for longitudinal studies and SPIRIT-style schedules of enrolment and assessment [@spirit2013].

**Checklist view.** A task-oriented view that flattens the diagram into a list of activities with their associated items and status. Every Studyflow element carries an optional `checklist` attribute — a markdown list — that the Checklist view extracts and aggregates. The view supports two uses: *running studies day-to-day* (what is next, what is done) and *adhering to reporting guidelines* (CONSORT, SPIRIT, STROBE, PRISMA, CARE), where guideline items are mapped to the diagram elements that satisfy them so a study can be audited without leaving the diagram. Checklists ship with the `.studyflow` file and can be exported to JSON or Markdown for external task managers (§2.8 returns to reporting-guideline coverage).

| If you need to communicate… | Use |
|---|---|
| Procedural structure, branching, data flow | Study view |
| Wall-clock timing, schedules, durations | Timeline view |
| Coverage against a reporting checklist or protocol | Checklist view |

A single `.studyflow` source thus underwrites three reading paths — a methods diagram, a project schedule, a reporting audit — without forcing authors to maintain three artifacts that drift apart.


## 2.5 Demonstration I — CONSORT-style randomized controlled trial

CONSORT (Consolidated Standards of Reporting Trials) prescribes a checklist plus a flow diagram for documenting randomized controlled trials [@moher2012; @rennie2001]. The flow diagram, in particular, is a participant-tracking schematic with enrollment, allocation, follow-up, and analysis as the four canonical rows, and with attrition counts annotating each transition. In current practice this diagram is drawn at write-up time, typically in a presentation or drawing program, and bears no machine-readable connection to the protocol that was registered, to the data collection system that recruited the participants, or to the analysis code that produced the published estimates. The diagram is a *document* about the trial, not the *spec* that drove it.

Studyflow inverts this relationship. We ship a 423-line CONSORT 2025 reference diagram (`src/assets/examples/consort2025.studyflow`) that authors can fork, parameterize, and run as the actual protocol of a new trial. Figure 6 contrasts three artifacts: (a) the canonical CONSORT 2025 reference flow as published by the CONSORT group, (b) a Studyflow reproduction encoded with the same labels and pathways, and (c) an annotated comparison whose left path uses Studyflow boundary error events and whose right path uses the traditional text-and-box treatment.

The crucial mechanical difference is how attrition is represented. In the traditional figure, each "Excluded / Did not receive / Lost to follow-up / Discontinued" box is an unconnected annotation sitting next to the column of follow-up activities; readers infer that these counts subtract from the main flow. In the Studyflow diagram, attrition is encoded as a *boundary error event* attached to the activity from which participants departed. `Excluded_Pre` hangs off the eligibility gateway, `DidNotReceive_A/B` off the two allocation tasks, `LostFollowup_A/B` and `Discontinued_A/B` off the follow-up tasks, and `ExcludedFromAnalysis_A/B` off the analysis tasks. Each event terminates in an error end event with a labeled count. This has three consequences. The topology of the diagram now matches the topology of the trial: a participant lost during follow-up exits along an edge whose origin is the follow-up activity itself, not along an arrow drawn from a side annotation. Summing attrition becomes a graph operation rather than a manual exercise — a Studyflow-aware validator can verify that no row's outbound counts exceed its inbound count. And the boundary error event is the same primitive BPMN uses to model interrupts in any business process, so the diagram remains valid BPMN 2.0 and inherits the standard execution semantics for error handling [@stroppi2011; @ait2024bpmn_humanagent].

The shipped CONSORT diagram carries domain semantics in `studyflow:` extension elements alongside the BPMN scaffolding. The enrollment start event sets `studyflow:consentFormUri` to a participant-facing consent PDF, so a runner that hits this node renders the consent screen automatically before any randomization happens. The screening task carries a `studyflow:checklist` attribute whose value is a markdown checklist (demographic intake, medical history, vital signs, baseline cognitive screen); this checklist also drives the Checklist view (§2.4). The eligibility gateway is tagged with `cognitive:eligibilityGateway`, the randomization gateway with `cognitive:randomGateway`, and the follow-up tasks carry `cognitive:cognitiveTask` with an instrument hint (`jspsych`) and an inline parameter block (n-back duration, n-back levels, trials per block). Allocation, follow-up, and analysis tasks each carry their own checklists describing protocol obligations.

This means a single `.studyflow` file simultaneously serves four readers. The trial registry sees a registered protocol with explicit randomization and eligibility criteria. The ethics board sees the consent screen content and the per-task checklists. The data collection platform sees the embedded cognitive task instrument and parameters. The journal sees the CONSORT-compatible figure with attrition flows already wired. The mechanism that makes this work is not new: it is the standard BPMN extension protocol [@stroppi2011], and the four readers' interpretive layers are the four `studyflow:` and `cognitive:` namespaces. What is new is that the union of these layers, rendered together, *is* a CONSORT diagram.

[GAP: coverage table mapping CONSORT 2025 items to machine-checked / encoded-as-attribute / author-discipline categories, derived by inspecting the 25-item CONSORT 2025 checklist against the shipping `consort2025.studyflow` artifact.]

The reverse direction is also supported: starting from a `.studyflow` file that already encodes the protocol, the modeler renders the CONSORT-style figure as a publication asset without any redrawing. The figure that appears in the paper is the file that ran the trial. This is the strongest single rebuttal to the "different artifacts drift" failure pattern described in §1.2.

## 2.6 Demonstration II — A cognitive task end-to-end: N-back

To validate the round-trip from authored diagram to running experiment, we walk through an N-back working-memory task encoded as a Studyflow. The N-back is a near-universal probe of working memory [@bell2021perspectives] and is normally documented as a slide-style schematic showing one or two example trials, annotated with stimulus duration, inter-trial interval, and the target-match rule. The slide is intuitive but underdetermined: timing values often live only in the figure caption, the boundary between trial and block is implicit, and decisions like "what counts as a correct match" are buried in the analysis code. Figure 7 places the traditional slide-style figure next to the Studyflow equivalent.

The Studyflow N-back authors the trial as an explicit subgraph. Each trial begins with a stimulus activity (a task carrying `studyflow:url="behaverse://show_stimulus"`); a boundary timer event (`bpmn:boundaryEvent` with a `timerEventDefinition` of duration `1s`) defines the response window; a second boundary timer encodes the inter-trial interval; text annotations attached to the response branches label them as `target` and `non-target` matches. The trial-by-trial encoding in Figure 7 is pedagogical; for execution beyond a handful of trials, the same logic is expressed as a single `behaverse:behaverseTask` whose inline YAML block declares the N level, stream specification, trial count, stimulus duration, and inter-trial interval — and which the runner expands into individual trials via the Behaverse Unity runtime. Trial sequence flows compose into a block, blocks loop until a counter reaches the target trial count, and the loop's exit edge transitions to the next block of a different N level. The XML fragment in Figure 7c shows the relevant primitives: `studyflow:url` resolves to a behavioral primitive in the runner; the boundary timer event terminates the stimulus activity at the response deadline; the text annotation supplies the human-readable label that anchors the icon in the rendered diagram.

The empirical anchor of this section is the round-trip itself. We authored the N-back in the Studyflow Modeler (§2.2), serialized it as a `.studyflow` file, then loaded that file into the Studyflow Runner (§2.3). The runner parses the file with the bundled studyflow and cognitive moddle schemas, validates that every required attribute is present (response window, stimulus duration, N level, target rule), then traverses the diagram one node at a time. The N-back's primitives are covered by the runner's built-in node kinds: `cognitive:Instruction` renders markdown instructions; trial-level execution is delegated to a `behaverse:behaverseTask` whose Behaverse Unity bridge expands the inline block into ordered trials with their declared timing; the questionnaire that precedes the task renders through `cognitive:Questionnaire`, which ships with PHQ-9, GAD-7, and BDI-II built-in instruments and accepts custom instruments via inline schema. Seeded randomization through the `?seed=N` URL parameter makes the within-task sequence deterministic, which is the property that lets a pilot dataset be reproduced exactly from the same `.studyflow` source.

The trial data the runner emits is itself a small artifact: a per-participant log of node entries and exits, the seed, the resolved branch at each gateway, the participant's response and reaction time at each trial, and the start and end timestamps. This log is structured to fit the Behaverse Data Model trials-level schema [@bdm], which is in turn Psych-DS-compatible [@psychds]. A Studyflow-encoded N-back therefore produces a CSV of trials whose columns are predetermined by the schema and whose semantic content is determined by the diagram. The trials CSV is reviewable side by side with the diagram, and a third party with only those two files can reconstruct what each row means without running the modeler.

This closes the "single diagram, many audiences" loop from §1. The same file is reviewable by an ethics board (consent and instructions are first-class elements), executable by the runner (each element has a node renderer or is gracefully skipped), generative of standards-compliant data (the trials CSV is Psych-DS-conformant), and a publication figure as-is (no redrawing). Three concrete artifacts make this tangible in the supplementary materials: the N-back `.studyflow` source committed alongside the paper; a short walkthrough showing the runner stepping through trials; and the resulting trials CSV from a pilot run.

[GAP: actual pilot data (n participants, seed, summary accuracy and median RT) and runner-state screenshots; the runner ships and the .studyflow primitives are in place — execution is the remaining piece.]

The same `.studyflow` source also extends to a second audience: artificial agents. **CogEnv** [@ansarinia2022cogenv] is a configurable environment that administers Behaverse cognitive tests to reinforcement-learning agents through DeepMind's AndroidEnv interaction layer, exposing them to the same screenshots, response options, and time constraints that human participants see and logging each trial under the Behaverse Data Model [@defossez2020bdm]. A planned extension would add adapters for large-language-model and other generative-AI agents — translating symbolic task state into natural-language or screenshot-based prompts and mapping the agent's discrete outputs back to response actions (via the Model Context Protocol or comparable interfaces). In either form, a Studyflow encoding of the N-back is simultaneously the human protocol and the agent test specification: the diagram declares the trial structure, instrument parameters, and response schema; CogEnv's adapter handles the modality bridge. The same `.studyflow` source therefore drives three distinct executions from one source — bot-mode validation in the runner (§2.3), human pilot via the Behaverse Data Server (§M.6), and systematic agent profiling via CogEnv — each consuming the same diagram, none requiring a protocol redesign. This is what enables a "few models, many items" benchmarking regime: profiling selected agents across hundreds of parametrically varied items rather than ranking many models on a small fixed set [@ansarinia2022cogtext].

The N-back case also clarifies what Studyflow does *not* do. It is not a stimulus-presentation library: rendering letters at a fixed retinal angle still requires either the bundled Behaverse Unity runtime (via `BehaverseTask`) or an external presentation framework reached through `studyflow:url`. The diagram describes which stimulus to show, in what order, under what timing constraint, and what to record — not the pixel-level mechanics of showing it.

## 2.7 Demonstration III — A reproducible analysis pipeline

The third demonstration moves past data collection into data analysis, where the dominant artifact is a script — an R or Python notebook with implicit dependencies, comments instead of types, and no machine-readable pre-registration of its steps. Studyflow's data operations (§2.1) give every script-style operation a typed marker: `Map` (1→1 element-wise), `Filter` (N→subset(N) row drop), `Group` (N→G groups), `Reduce` (N→1 per group), `FlatMap` (1→N), `Transform` (generic), and `Compose` (bundled pipeline). Combined with `Dataset`, `DataStorage`, and `Schema` data elements, the diagram is a complete pre-registration of the analysis.

We illustrate with a response-time analysis of a two-alternative forced-choice task. The pipeline is nine steps: read raw trial data from a `Dataset`; `Filter` invalid trials (RT < 100 ms, missing data, flagged-as-bad rows); `Map` to derived measures (log-RT and condition codes); branch on data type at an exclusive gateway (within-subject down one path, between-subject down another); `Group` by participant and condition; `Reduce` to per-group means, standard errors, and accuracy; route through a `Manual` review task where the analyst inspects outliers and optionally re-runs with adjusted criteria; `Transform` into a publication-ready summary; write to a `Table` whose CSVW schema declares every column the downstream figure-generation task can rely on. Three properties are not optional: the conditional branch on within-vs-between design is visible in the topology rather than buried inside an `if` statement; the manual review activity has an explicit place in the diagram, making it harder to skip; and the schema attached to the output `Table` is part of the spec rather than implicit in the column names.

Figure 8 shows the RT-analysis subprocess side by side with equivalent dplyr code. The diagram encodes the same chained pipeline that a tidyverse user writes as `trials_raw |> filter(correct == 1) |> mutate(log_rt = log(rt), rt_z = (rt - mean(rt)) / sd(rt)) |> group_by(agent_id, condition) |> summarize(rt_mean = mean(rt), rt_sd = sd(rt))`, but with two additional commitments. First, typed inputs and outputs: `trials_raw` and `trials_summary` are `Dataset` elements with `format = bdm`, at `bdmDataLevel = trials` and `models` respectively, both registered in a `behaverse` `DataCatalog` and physically stored in a `DataStorage` (here a DuckDB+Parquet `ducklake`). Second, an explicit `Compose` marker on the analysis task lists `transform`, `filter`, `map`, `group`, `reduce` as the primitive operations the task is allowed to perform. Tooling can therefore reject any implementation that touches a column the schema does not declare, or that performs a join the marker does not authorize.

Pre-registration of analysis is the diagram itself. A pre-registered analysis plan in current practice is a free-text narrative on a registry website, with no machine-checkable correspondence to the code the analyst eventually runs. Under the Studyflow encoding, the diagram is the spec, the dplyr pipeline is one valid implementation, and any divergence between the two is detectable by inspection of the data-operation markers and the input/output schemas.

[GAP: specific Pedro-group RT dataset to use for the demonstration; the analysis subprocess is in place but the worked dataset needs picking.]

## 2.8 Coverage across reporting guidelines

The CONSORT case in §2.5 and the SPIRIT 2025 protocol case (which ships as `src/assets/examples/spirit2025.studyflow`, 378 lines) are two instances of a broader pattern. Reporting guidelines structure the way a study is written up across roughly a dozen study types in biomedicine and the social sciences. The Equator network catalogs the standards; Table 2 lists the eleven most widely used.

| Topic | Guideline | Template ships? | Checklist view? |
|---|---|---|---|
| Randomized trials | CONSORT | Yes (`consort2025.studyflow`) | Yes |
| Study protocols | SPIRIT | Yes (`spirit2025.studyflow`) | Yes |
| Observational studies | STROBE | [GAP, small] | [GAP, small] |
| Systematic reviews | PRISMA | [GAP, small] | [GAP, small] |
| Diagnostic/prognostic | STARD | [GAP, small] | [GAP, small] |
| Case reports | CARE | [GAP, small] | [GAP, small] |
| Clinical practice | AGREE | [GAP, small] | [GAP, small] |
| Qualitative research | SRQR | [GAP, small] | [GAP, small] |
| Animal pre-clinical | ARRIVE | [GAP, small] | [GAP, small] |
| Quality improvement | SQUIRE | [GAP, small] | [GAP, small] |
| Economic evaluations | CHEERS | [GAP, small] | [GAP, small] |

Each guideline is structurally a controlled vocabulary plus a checklist plus (sometimes) a flow diagram. Studyflow's mechanism is identical across the eleven: checklist items become entries in the `studyflow:checklist` attribute on the relevant element; flow diagrams become Studyflow renderings with boundary error events for attrition (where applicable); vocabulary becomes labels on activities, gateways, and data elements. Because the checklist attribute is machine-readable, the Checklist view (§2.4) automatically projects items as a markdown list, with each item linked back to the element it documents. SPIRIT 2025 is the most demanding shipped template: its 34 items across 9 topics map to a Timeline view (Figure 9) that simultaneously serves as the study schedule and the SPIRIT checklist.

The two guidelines that currently ship as worked templates are CONSORT 2025 and SPIRIT 2025. The other nine are roadmap items rather than gaps in the mechanism: the elements, attributes, and Checklist view are in place; what remains per guideline is roughly a half-day of authoring. STROBE and PRISMA are next.

The deeper point: reporting guidelines and execution specifications need not be different artifacts. A SPIRIT protocol is a *plan*; a CONSORT diagram is a *report*. In current practice the two are written by different people at different times into different files. Encoded as a Studyflow, they are the same file at two points in its lifecycle — the SPIRIT view before randomization, and the CONSORT view with attrition counts written into the labels of the boundary error events.

## 2.9 Process and data: one diagram

Most workflow tools separate *process* (what runs, in what order) from *data* (what tables, columns, files, and units the process consumes and produces). UML splits the two into activity diagrams and class diagrams [@cuevasvicenttin2013workflows]. DAG-based execution engines describe the process in code and rely on convention for data layout. Reporting guidelines describe the process in prose and the data in a separate supplementary file. The split is convenient for tool builders and inconvenient for researchers: the two artifacts drift, and an analyst cannot tell from the process figure alone whether a downstream task is consuming the column the upstream task produced.

Studyflow puts process and data in the same diagram. Activities sit on the sequence-flow graph; `Dataset`, `DataStorage`, `DataCatalog`, `Schema`, `Array`, and `Snapshot` sit on a parallel data-flow graph; the two are connected by BPMN data associations rendered as dashed edges. A `Dataset` carries a `format` attribute (`bdm`, `bids`, `psych-ds`, `kedro`, `undefined`) and a `schema` reference, inline or external. The `Schema` element is first-class: tabular data uses CSVW [@hoytO3GuidelinesOpen2024] body or a `schemaRef` URL; non-tabular data (the `Array` element) documents tensor dimensions, dtypes, and units. Bindings to BIDS [@bids], Psych-DS [@psychds], the Behaverse Data Model [@bdm], and CSVW are typed attributes the modeler validates and the runner respects — not comments.

Figure 10 shows a minimal example: a `Record EEG` task whose data output is bound to a `Dataset` with `format = bids` and `bidsDataType = eeg`. A downstream preprocessing task on the same diagram declares a data input from the same `Dataset`, and the dataset's schema is the contract both tasks share — verifiable at modeling time and at validation time against the declared BIDS layout.

[GAP, small: small EEG/BIDS example diagram to be authored; the data elements and associations are in place — what remains is a one-page exemplar.]

The trade-off is visual density. The modeler manages this through collapsible views (§2.2): the high-level protocol toggles the data layer off; the full dependency graph toggles it on. The single source remains the same `.studyflow` file.

## 2.10 Beyond data collection: multimodal preprocessing and foundation-model training

ML pipelines for behavioral and neural prediction face the same fragmentation that experimental protocols face: model card in one repository, feature engineering in another, training script in a third, deployment configuration in a fourth, and retraining triggers living (if at all) as cron jobs nobody can find. Studyflow's data operations, gateways, and schema-bound data elements apply to ML pipelines as cleanly as to behavioral analyses. We illustrate this with **OmniProcess**, a use case sketched as an automated multimodal preprocessing pipeline that harmonises EEG, fMRI, and behavioral recordings across heterogeneous public datasets. The deployed pipeline is forthcoming; the encoding shown here is the Studyflow diagram that would specify it.

OmniProcess instantiates the abstract `DataOperationActivity` vocabulary (§M.3.4) with concrete neuroimaging primitives. The `omniprocess` schema layer adds two domain-specific activity types — `PreprocessfMRI` and `PreprocessEEG` — on top of the generic `Transform`, `Map`, `Reduce`, and `Filter` operators. A canonical OmniProcess Studyflow proceeds in four movements (Figure 11). (1) **Ingest** loads raw recordings as `Dataset` elements with `format = bids` from a `DataCatalog` (e.g. OpenNeuro, TUH EEG, UK Biobank, ABCD), each registered against a canonical `omni://` address whose query API would lazily materialize derivatives on demand. (2) **Modality-specific preprocessing** runs as parallel subprocesses: `PreprocessfMRI` chains brain extraction, motion correction, MNI152 registration, and confound removal through fMRIPrep, ANTsPyNet, and Nilearn; `PreprocessEEG` chains layout normalization, channel selection, filtering, artifact removal, re-referencing, and source localization through MNE and EEGPrep; behavioral data is converted to BDM trials [@defossez2020bdm] with original stimuli, raw responses, and evaluation scores retained. (3) **Multiverse expansion** captures the multiple defensible analytical paths each preprocessing step admits — high-pass cutoff at 0.1 Hz versus 0.5 Hz, alternative re-referencing schemes, different brain atlases — as explicit branches off a `Compose` operator, so downstream models can compare across choices rather than committing to one [@steegen2016multiverse]. (4) **Harmonised corpus output** writes the preprocessed derivatives back to the catalog under their canonical addresses with schema-bound metadata; downstream model-training, fine-tuning, or analysis workflows then consume those derivatives by reading specific addresses, without needing to know how they were produced.

Three properties become explicit in this encoding that are hard to recover from prose. **Provenance is the diagram**: every derived artifact would trace back to its raw source through the Studyflow nodes that produced it, including the specific parameterization captured in inline configurations. **Multiverse is first-class**: alternative preprocessing paths are explicit branches rather than version-controlled forks of a script, and cross-pipeline disagreement reduces to a structured comparison instead of a discovery exercise [@steegen2016multiverse]. **Cross-dataset interoperability is a schema decision**: every `Dataset` declares its `format` (BIDS, BDM, Psych-DS, etc.) and binding schema, so a preprocessing subprocess defined once can target every dataset whose recordings honour the same format — turning per-dataset engineering effort into a one-time schema commitment.

The same encoding extends naturally to HPC settings, where subprocesses would be containerized via Docker/Apptainer and scheduled on a SLURM cluster, and to downstream stages: a `Script` activity that consumes the harmonised corpus and emits a model `Snapshot` is a straightforward continuation of the same diagram, as are fine-tuning, evaluation, and monitoring subprocesses [@kourani2024promoai]. Planned governance operations (`anonymize`, `validate`, `controlAccess`) would make data-governance steps first-class diagram elements rather than annotations [@ghosh2025reproducible_digital_health]. The layered schemas (§2.1) allow domain-specific extensions like `galea` for VR-multimodal recording sessions or `datatrove` for large-scale corpora to plug in without touching the core. ML pipelines and behavioral analyses look different in code; in a Studyflow they are the same notation with different operators [@tetzlaff2022bpmn4sml].

## 2.11 Multi-agent / choreography

Some studies cannot be described as one participant walking through one flow. Dyadic decision experiments, parent–child developmental protocols, two-player economic games, and experimenter-administered protocols all involve interactions between two or more agents whose *interaction* is itself the unit of analysis. BPMN 2.0 introduced the **choreography task** for exactly this case — a specialized task representing a directed exchange between participants with an explicit initiator [@pufahl2022]. Studyflow inherits the construct unchanged.

Three patterns recur. The **dyadic decision pattern** uses one choreography task per round, listing two `ParticipantRef`s and rotating which one is `InitiatingParticipant` across rounds; this is the right encoding when each round's content depends on the previous round's exchange. The **experimenter-driven protocol pattern** is simpler: pools and lanes usually suffice, with choreography reserved for when the experimenter's next choice depends on the subject's mid-trial responses. The **parent–child pattern** models developmental studies with separate `StartEvent`s per family member (indicating independent recruitment) and choreography tasks for joint sessions.

The decision rule is to use choreography only when the *interaction itself* is the unit of analysis; otherwise the additional notational complexity is unwarranted. The runner does not yet traverse choreography tasks (a roadmap item; §3.4), but the diagram is fully expressive at modeling time and validates against the BPMN 2.0 choreography schema [@stroppi2011].


---

# 3. Discussion

## 3.1 What Studyflow changes

The recurring failure mode in current practice is that the *protocol*, the *pipeline*, and the *figure* are three separate artifacts that begin in agreement and end in drift. The demonstrations in §2 are intended to show that a single `.studyflow` file can carry all three: the CONSORT diagram in §2.5 is, simultaneously, the participant-flow figure for the paper, the spec a reviewer can audit against the CONSORT-2025 checklist, and a runnable artifact that the runner can step through; the N-back in §2.6 is the protocol text, the trial-loop logic, and the executable task on the runner; the reaction-time pipeline in §2.7 is the analysis section of the paper and the actual transformation script. Drift across these views is no longer possible by construction, because there is only one source.

Several concrete benefits follow. **Stakeholder alignment**: an ethics reviewer, a collaborator, and an engineer read the same diagram at different zoom levels (Study, Timeline, Checklist) rather than three documents that disagree subtly (§2.4). **Versionability**: a `.studyflow` file is BPMN 2.0 XML with stable element IDs, diffs cleanly in Git, and can be embedded inside an SVG so that the figure in the manuscript carries its own machine-readable source. **Reusability**: because the language is independent of the modeler, third-party tools — linters, converters, alternative renderers — can target the specification directly. **Process–data coupling**: data artifacts (datasets, tables, schemas, snapshots) and data operations (map, filter, reduce, group) live on the same diagram as the procedure that produced them (§2.9), so a CSVW or BIDS or Psych-DS schema can be bound to a specific task and the binding survives review.

The deepest claim is **trust by construction**: reproducibility becomes a property of the artifact rather than an add-on documentation effort. The same diagram that an ethics board approved is the one the participants ran is the one the figures were generated from. That is a stronger guarantee than current practice can offer, and it is the basis on which we expect Studyflow to compose with — rather than compete against — existing reproducibility infrastructure.

## 3.2 Relationship to existing ecosystems

Studyflow sits at the intersection of four ecosystems and does not aim to replace any of them.

**Execution stacks.** Nextflow, the Common Workflow Language (CWL), the Workflow Description Language (WDL), Pegasus, Apache Airflow, Kedro, and domain-specific engines such as NiPype and Pydra solve a problem Studyflow does not: scalable, reproducible execution on heterogeneous compute [@zhao2008scientific_workflows; @cuevasvicenttin2013workflows; @nextflow; @cwl; @pydra]. Their representations are optimised for machines and developers, not for ethics boards or journal reviewers. A more fundamental limitation many of these stacks share is their reliance on directed acyclic graphs (DAGs) as the underlying computational model: DAGs are well-suited to data pipelines with fixed inputs and outputs, but scientific inquiry itself is inherently iterative — hypothesis generation, experimentation, and revisited analysis form continuous feedback loops that AI-driven discovery systems are beginning to operationalise [@ghareeb2025]. BPMN's sequence flows, boundary events, and choreography express these cycles natively; a DAG-based stack must emulate them through external control logic or repeated workflow executions. Studyflow sits *above* such systems: a Studyflow task can reference an external script (a Nextflow process, a Kedro node, a NiPype workflow) and a downstream tool can compile the protocol-level diagram into an executable graph for one of these engines. The boundary is deliberate — we have prioritised communication over execution [@ghosh2025reproducible_digital_health].

**Data standards.** BIDS, Psych-DS, the Behaverse Data Model, and CSVW prescribe how datasets are structured [@bids; @psychds; @bdm; @csvw]; they say nothing about the process that produced them. Studyflow describes the process and references the data standards via schema-bound `Dataset`, `Table`, and `Schema` elements. The two are complementary: a Studyflow diagram with a `bids:Dataset` linked to a "Record EEG" task tells the reader (and the machine) both *what* was collected and *how*.

**Reporting guidelines.** CONSORT, SPIRIT, STROBE, STARD, and their siblings [@moher2012; @spirit2013; @strobe; @stard] enforce structure at the publication stage. Today, conformance is checked by hand against PDF supplementary materials. Studyflow can be the carrier for these guidelines: §2.5 shows a CONSORT diagram authored as Studyflow with the checklist items as elements; §2.8 shows the same idea for SPIRIT. Conformance becomes a property the diagram can be checked against, not a checklist tacked on afterwards.

**Other BPMN profiles.** BPMN4CP for clinical pathways [@braun2014], BPMN4sML for serverless ML [@tetzlaff2022bpmn4sml], and the human–agent extension [@ait2024bpmn_humanagent] are sibling profiles in adjacent domains. Studyflow's layered moddle schemas (core plus `cognitive`, `behaverse`, `omniprocess`, `datatrove`, `galea`) follow the same pattern at the schema level, and we expect future extensions for neuroimaging, clinical neurology, or developmental research to layer in similarly without modifying the core. Visual modeling languages already used in life-sciences-adjacent fields, such as Systems Biology Graphical Notation [@novere2009], confirm both the appetite for graphical formalisation and the importance of domain-specific vocabulary [@norouzi2025semantic_processes].

A final positioning point: Studyflow is not an ontology of experimental design. Ontologies developed for processes are numerous but suffer from high upfront cost and low reuse [@norouzi2025semantic_processes]; we have aimed instead for a profile that is small enough to learn from one worked example and a glossary, and that is enforced by tooling rather than by inspection.

## 3.3 Limitations

Studyflow inherits BPMN's visual grammar; readers with no prior exposure to flowchart notation still face a small learning curve, even if the curve is shallower than learning a domain-specific language from scratch. The modeler's schema-driven inspector reduces this cost during authoring but cannot eliminate it for readers.

Representing process and data within a single diagram is the design's central trade-off (§2.9). For large multi-session studies the visual density can suffer despite collapsible sub-processes, swimlanes, and the alternative Timeline and Checklist views (§2.4). We have not benchmarked the legibility of large diagrams against the alternatives they replace; this is an empirical question we leave for future readability and comprehension studies.

Studyflow prioritises communication over execution. A `.studyflow` file is a specification; making it executable requires integration with external systems. The Studyflow Runner provides a participant-facing runtime for a curated set of node kinds (consents, instructions, questionnaires, generic tasks, embedded Behaverse cognitive tasks), but it is not a general-purpose orchestrator. Parallel gateways are not yet supported by the runner; `StratifiedAllocationGateway` currently behaves identically to `RandomGateway` (uniform-at-random); choreography traversal across pools is not implemented in the runner. These are scope choices rather than language limitations, and they map directly to the roadmap below.

Some experimental designs are intrinsically awkward to express as directed graphs. Adaptive trials, certain Bayesian sequential designs, and ABAB single-subject designs need representations of feedback, dynamic re-allocation, or open-ended replay loops that exceed what BPMN sequence flow encodes naturally [@ghareeb2025]. The Choreography and message-flow elements can express some of this; the rest is current research.

Finally, Studyflow is an emerging specification, and adoption beyond our group is still limited. Long-term sustainability depends on community uptake. We have tried to lower that bar — MIT-licensed, browser-only deployment, BPMN 2.0 XML as the on-disk format, LinkML as the schema source of truth, no server dependency — but the bar exists nonetheless.

## 3.4 Future directions

The language has near-term extensions queued in the roadmap. `Timeseries` and `Event` data structures will round out the data taxonomy for physiological and behavioural recordings; explicit storage operations (`loadData`, `saveData`, `exportData`) will separate pure transformations from I/O; data-governance operations (`anonymizeData`, `validateData`, `controlAccess`) will encode regulatory steps as first-class elements rather than annotations; stochastic operations and a tidyverse-mirrored vocabulary (`splitData`, `cleanData`, `joinTables`, `pivot`, `selectColumns`, `mutate`, `summarize`) will close the gap with everyday analysis idioms.

Tooling will follow the same path. A dedicated schema editor for data stores is in progress, as are improved inspector ergonomics, additional worked examples (data collection, MLOps, analysis), and a published specification for the data elements. On the runner side, support for parallel gateways, true stratified allocation, and choreography traversal across pools is planned, alongside broader runtime integrations beyond the Behaverse Data Server so that a Studyflow diagram can drive heterogeneous downstream stacks (Kedro, Nextflow, NiPype) [@ghareeb2025].

A larger question is community formation. Sibling BPMN profiles in clinical pathways and serverless ML emerged because a small number of groups committed to the same notation; Studyflow's layered moddle design is deliberately set up to make new domain extensions cheap (each is one YAML file plus optional renderer code). External adoption signals are the goal: forks of the modeler for adjacent domains, third-party validators against the LinkML schema, and re-use of the SPIRIT and CONSORT templates in registered reports and journal supplements. [GAP: community-adoption signals — fork counts, external `behaverse/data-server` deployments, or third-party Studyflow files in the wild — to be added when available.]

Two lines of empirical work will sharpen the evidence base for the claims we make here. First, a readability and comprehension study with 5–10 cognitive scientists comparing Studyflow diagrams against the artifacts they replace (protocol PDFs, manuscript flow figures, analysis scripts) would test the *trust by construction* claim against measured reviewer effort. Second, end-to-end demonstrations beyond the three reported here — a multi-session longitudinal study, an ABAB single-subject design, an MLOps pipeline with a fairness audit and retraining loop (§2.10) — would map the boundaries of what the current vocabulary covers. Both are realistic for a follow-up applications paper once Studyflow has been picked up by groups outside our own.


---

# 4. Methods

## M.1 LinkML schema as the single source of truth

A recurring failure mode in scientific tooling is to couple a notation to a single application: when the tool is abandoned, the notation becomes unreadable. Studyflow avoids this by maintaining the language as an independent, machine-readable LinkML schema [@moxon2025linkml] that serves as the single source of truth for element types, attribute constraints, and validation rules. LinkML is an open schema-modeling framework increasingly adopted across biology, biomedicine, and ontology engineering for FAIR-aligned [@fair] data and process descriptions; we adopt it for Studyflow so the language sits in a notation life-sciences readers are likely to encounter rather than in a BPMN-tooling-specific dialect. The accompanying modeler is a reference implementation that tracks the schema; it does not own the language.

Formally, a Studyflow diagram is a tuple $S = (N, E, T, \tau, \lambda)$ where $N$ is a finite set of nodes, $E \subseteq N \times N$ is a set of directed sequence flows, $T$ is the set of node types, $\tau: N \rightarrow T$ assigns a type to each node, and $\lambda$ attaches domain attributes (metadata, triggers, gateway logic, implementation links) to nodes. $N$ partitions into $N_E$ (events), $N_A$ (activities), $N_G$ (gateways), and $N_D$ (data objects). Studyflow refines this base in four places: $N_A$ adds cognitive-task, questionnaire, instruction, rest, video-game, and Behaverse-task types, plus an abstract `DataOperationActivity` that augments any BPMN activity with a data-operation marker and input/output variable lists; $N_G$ adds `RandomGateway`, `StratifiedAllocationGateway`, and `EligibilityGateway`; $N_D$ adds `DataCatalog`, `DataStorage`, `Dataset`, `Schema`, `Array`, and `Snapshot`; and $\lambda$ adds attributes such as consent forms, completion codes, randomization probabilities, and bindings to community data standards (BIDS, Psych-DS, BDM [@bids; @psychds; @bdm], CSVW, Kedro). Edges in $E$ remain BPMN `SequenceFlow`s and may carry an optional `conditionExpression` for gated branches.

The LinkML schema is versioned and drives documentation, validators, and downstream tools. Because `bpmn-js` and `bpmn-moddle` cannot consume LinkML directly, a parallel moddle YAML mirror lives alongside the modeler at `studyflow-modeler/src/assets/schemas/` and carries the same definitions in the format the BPMN runtime expects [@bpmnmoddle]. The mirror is partitioned into a small core (`studyflow.moddle.yaml`, 507 lines) and a companion cognitive schema (`cognitive.moddle.yaml`, 318 lines), with four optional domain extensions (`behaverse`, `omniprocess`, `datatrove`, `galea`) loaded on demand. The two representations are kept aligned by maintaining the LinkML schema as the authoritative spec and treating the moddle YAML as a runtime materialization; a changelog records breaking and additive changes between releases.

**Listing 1.** Excerpt from the Studyflow LinkML schema showing one enum and one class with a conditional attribute. `class_uri: bpmn:ExclusiveGateway` declares that the new element inherits from a BPMN base, and `annotations.condition` encodes a visibility predicate that the modeler honors at inspection time.

```yaml
enums:
  AssignmentAlgorithmEnum:
    description: The scheduling algorithm used for the assignment.
    permissible_values:
      probabilistic:
        title: Probabilistic
      round-robin:
        title: Round Robin

classes:
  RandomGateway:
    class_uri: bpmn:ExclusiveGateway
    mixins:
      - Element
    attributes:
      algorithm:
        range: AssignmentAlgorithmEnum
        ifabsent: string(probabilistic)
        description: Algorithm used for the assignment.
      probabilityFunction:
        range: string
        ifabsent: string(uniform)
        description: Probability mass function over the outgoing branches.
        annotations:
          condition:
            language: json
            body: '{"studyflow:algorithm": "probabilistic"}'
```

## M.2 BPMN extension mechanism

Studyflow uses BPMN's native extension mechanism rather than a parallel notation, so that diagrams remain valid BPMN 2.0 XML and degrade gracefully in any compliant editor (e.g. Camunda Modeler, bpmn.io) [@bpmnspec; @stroppi2011]. Domain elements live in two XML namespaces. The `studyflow` namespace (`http://behaverse.org/schemas/studyflow`) holds the core extensions (`Study`, `StartEvent`, `EndEvent` augmentations, data-infrastructure types). The `cognitive` namespace (`http://behaverse.org/schemas/studyflow/cognitive`) holds activity and gateway types specific to behavioral research. IDs, sequence flows, and BPMN diagram interchange (BPMN-DI) layout information are left untouched.

The moddle YAML schemas compose types through two distinct relationships [@bpmnmoddle]. `extends` is a pure mixin that adds attributes onto an existing BPMN class without creating a new visual element; we use it, for example, to augment `bpmn:StartEvent` with `consentFormUri` and `requiresConsent`. `superClass` declares class inheritance and is used when introducing a new concrete element; we pair `superClass` (listing the BPMN base such as `bpmn:Task` or `bpmn:ExclusiveGateway`, plus `bpmn:BaseElement`) with `meta.bpmnType` so the modeler renders the correct BPMN shape. Each property carries moddle modifiers (`isAttr` for XML attributes, `isBody` for the element's text body, `isMany` for repeated lists, `default` for initial values, `redefines` to override an inherited property's type or default, `replaces` to swap one entirely) and an additional `meta` block that drives Studyflow-specific behavior in the inspector: `meta.pinned` keeps a property visible in the summary panel; `meta.optional` exposes a checkbox to opt the property in; `meta.editable` lets enum-typed properties accept free-text values; `meta.categories` groups properties under inspector tabs; and `meta.condition` declares a JSON visibility predicate so attributes only appear when sibling fields take specific values.

**Listing 2.** XML serialization of two extension elements. The `studyflow:study` marker declares the process as a Studyflow study; `cognitive:randomGateway` and `cognitive:questionnaire` nest inside `bpmn2:extensionElements` so generic BPMN parsers can ignore them while Studyflow-aware tools render and validate them. Round-tripping through `bpmn-moddle` preserves the XML losslessly.

```xml
<bpmn2:definitions
  xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL"
  xmlns:studyflow="http://behaverse.org/schemas/studyflow"
  xmlns:cognitive="http://behaverse.org/schemas/studyflow/cognitive"
  id="example-diagram">
  <bpmn2:process id="exampleStudy" isExecutable="true">
    <bpmn2:extensionElements>
      <studyflow:study />
    </bpmn2:extensionElements>
    <bpmn2:startEvent id="s">
      <bpmn2:extensionElements>
        <studyflow:startEvent consentFormUri="https://ex.org/consent.pdf" />
      </bpmn2:extensionElements>
    </bpmn2:startEvent>
    <bpmn2:task id="qs">
      <bpmn2:extensionElements>
        <cognitive:questionnaire instrument="phq-9" />
      </bpmn2:extensionElements>
    </bpmn2:task>
    <bpmn2:exclusiveGateway id="gw">
      <bpmn2:extensionElements>
        <cognitive:randomGateway algorithm="probabilistic"
          probabilityFunction="uniform" />
      </bpmn2:extensionElements>
    </bpmn2:exclusiveGateway>
  </bpmn2:process>
</bpmn2:definitions>
```

## M.3 Domain-specific extensions

Six moddle YAML schemas ship with the modeler under `src/assets/schemas/`. The core (`studyflow.moddle.yaml`, 507 lines) defines `Study`, `StartEvent`, `EndEvent`, `SequenceFlow`, the abstract `BaseElement`/`Activity`/`DataOperationActivity` bases, the data-infrastructure types, and the shared enumerations (`DatasetFormatEnum`, `BDMDataLevelEnum`, `BIDSDataTypeEnum`, `DataOperationTypeEnum`, `CompletionCodeTypeEnum`, `RuntimeEnum`, `AssignmentAlgorithmEnum`, `ProbabilityDistributionEnum`). The cognitive layer (`cognitive.moddle.yaml`, 318 lines) is split from the core so adopters in adjacent fields can swap or omit it without touching the base. Four further schemas (`behaverse.moddle.yaml`, `omniprocess.moddle.yaml`, `datatrove.moddle.yaml`, `galea.moddle.yaml`) extend the modeler's schema palette with domain-specific vocabularies and are enabled per diagram.

### M.3.1 Activity types

`CognitiveTask` (`superClass: bpmn:Task`) carries an `instrument` attribute drawn from an editable enum (PsychoPy, jsPsych, lab.js, OpenSesame, or a custom identifier) and an `isBody` `configurations` block in YAML whose shape depends on the instrument. `VideoGame`, `Rest`, `Instruction` (markdown `content`), and `Questionnaire` (with `QuestionnaireInstrumentEnum` covering PHQ-9, GAD-7, BDI-II, STAI, PSS, WHO-5, BFI, DASS-21, PANAS, plus a free-text option) follow the same pattern. `BehaverseTask` references the curated `BehaverseTaskEnum` of validated paradigms (N-Back, SART, Digit Span, Multiple Object Tracking, Useful Field of View, and others). Every activity inherits `documentation` and `checklist` from `BaseElement`.

### M.3.2 Event types

Studyflow adds `consentFormUri` and `requiresConsent` to `bpmn:StartEvent` (via `extends`, since no new visual shape is introduced) and adds `redirectTo`, `completionCodeType` (none/static/dynamic), and `completionCode` to `bpmn:EndEvent`. Intermediate, boundary, timer, error, message, signal, and conditional events remain standard BPMN and inherit Studyflow's `documentation` and `checklist` attributes through the `BaseElement` mixin.

### M.3.3 Gateways

`RandomGateway` (`superClass: bpmn:ExclusiveGateway`) picks one outgoing branch via an `algorithm` (probabilistic or round-robin) and a `probabilityFunction` (uniform, normal, exponential, poisson, custom). `StratifiedAllocationGateway` adds a `stratificationVariable` to balance allocation across covariate strata; in the current runner it falls back to uniform-at-random pending the full stratification logic. `EligibilityGateway` encodes inclusion/exclusion criteria as typed predicates. Standard BPMN `Exclusive`, `Parallel`, `Inclusive`, and `Complex` gateways remain available, with `conditionExpression` evaluated against the runtime variable bag.

### M.3.4 Data elements and data operations

The data infrastructure layer (`DataCatalog`, `DataStorage`, `Dataset`, `Schema`, `Array`, `Snapshot`) maps where appropriate to standard BPMN `DataStoreReference` and `DataObjectReference` shapes, augmented with format bindings to BIDS, Psych-DS, BDM, CSVW, and Kedro through `DatasetFormatEnum` and conditional sub-attributes (e.g. `bdmDataLevel` of events/trials/models when `datasetFormat=bdm`; `bidsDataType` of anat/func/eeg/meg/etc. when `datasetFormat=bids`). The data-operation vocabulary is closed: `DataOperationTypeEnum` permits `Transform`, `Map`, `Filter`, `FlatMap`, `Reduce`, `Group`, and `Compose`, mirroring tidyverse-style data manipulation. Each operation is a BPMN task carrying the abstract `DataOperationActivity` marker plus `dataInput`/`dataOutput` references; the operator name appears as a task marker icon. `Compose` takes a sequence of primitive operations.

### M.3.5 Iconography and styling

Element icons are drawn from the Iconify catalog (`iconify <set>--<name>`), so the modeler resolves them at runtime without bundling raster assets. Each `types[].meta.icon` declares a default; schemas may override icons per enumeration value (e.g. a dedicated `bids-dataset-icon` for the BIDS format). Color coding signals role (events green/red, gateways yellow, data blue), and the modeler's color picker writes to `bpmn-js-color-picker`-compatible attributes so colors round-trip through any BPMN-aware tool.

## M.4 Modeler architecture

The Studyflow Modeler is a client-side, browser-only React 19 application built on `bpmn-js` 18 [@bpmnjs] and `bpmn-moddle` 10. It compiles to a static bundle with Vite 7 and deploys without a server. Additional dependencies include `@xyflow/react` 12 (Timeline and Checklist views), `zustand` 5 (application state), `js-yaml` 4 (schema loading), Tailwind CSS 4 (styling), `bpmn-js-color-picker`, `bpmn-js-create-append-anything`, and `diagram-js-grid` (canvas extensions), Iconify (icons), and Playwright (end-to-end tests).

The source tree separates a shared core library from the two apps it serves (`src/modeler/` and `src/runner/`). The library at `src/lib/core/` is responsible for the bridge between schemas and the live BPMN model. `parsers/moddle-schema.ts` loads moddle YAML files and registers them with `bpmn-moddle`; `parsers/studyflow.ts` parses `.studyflow` XML; `schemas.ts` exposes the schema registry; `flow.ts` exposes the abstract flow-node type used by both apps. The `extensions/` directory contains the six modules that resolve domain attributes against the live diagram: `attributeDefinitions.ts` enumerates declared attributes; `attrs.ts` reads and writes them; `defaults.ts` applies default values; `extensionType.ts` resolves the active extension type for a BPMN base element; `resolve.ts` walks the extension hierarchy; and `wrapper.ts` exposes a uniform read/write API to consumers.

The modeler app at `src/modeler/` is organized into UI packages around `bpmn-js`. `palette/` and `contextpad/` generate drag-to-canvas controls from schema entries; `inspector/` generates the right-side attribute panel from `meta` annotations; `render/` overlays Studyflow icons and styling on the standard BPMN renderer; `simulation/` provides token-based diagram traversal for previewing flow without actually running tasks; `commands/` wraps user actions into undoable `bpmn-js` commands; `moddle/templates/` ships seed objects for the create/append menus; and `navbar/`, `dialogs/`, and `settings/` cover save/load, publish, and configuration. The whole UI is regenerated on schema reload, so when a contributor adds an attribute to a moddle file the inspector, palette, contextpad, and constraint checks all update without manual UI work. Figure M-1 [GAP] shows the architecture as a block diagram with schemas (left) feeding the core library (centre), which in turn drives the modeler and runner apps (right) and uploads to the Behaverse Data Server (off-page).

## M.5 Runner architecture

The Studyflow Runner is a separate single-page app deployed alongside the modeler at `run.html`. It accepts a diagram through one of three entry paths: a *Run* button in the modeler (which serializes the current diagram to local storage and opens the runner in a new tab), a `?studyflow_url=<url>` query parameter that fetches a hosted `.studyflow` file, or a direct file upload. A `?seed=<integer>` parameter makes random branches deterministic, which is essential for pilot runs and reproducibility audits.

The runner operates as a four-step state machine: it **parses** the XML using the bundled `studyflow` and `cognitive` schemas (plus any extension schemas the diagram references), **pre-fetches** the Behaverse runtime manifest only if the diagram contains a `BehaverseTask`, **validates** the diagram (each node kind contributes its own validator; failures abort with `phase=invalid` and surface in a logs panel), and **traverses** the diagram from the `StartEvent`. Each visited node yields a *job* descriptor; the registry maps the descriptor to a React component which the runner renders and waits to complete. Phases observable from the URL and header are `loading`, `running`, `job:<kind>`, `done`, `aborted`, `invalid`, and `error`.

Gateway semantics are deterministic given the seed. `RandomGateway` and `StratifiedAllocationGateway` pick one outgoing branch uniformly at random (the stratified variant currently behaves identically to random; balanced stratification is reserved for future work). `Exclusive` and `Inclusive` gateways evaluate the `conditionExpression` on each outgoing flow against a runtime variable bag (`setVariable(name, value)` writes; conditions read); the first truthy branch wins, falling back to the gateway's `default` flow. `ParallelGateway` is not yet supported and aborts the run. Six built-in node kinds ship with the runner: `Start` (consent screen when `consentFormUri` is set), `End` (issues a completion code and redirects), `Instruction` (markdown content), `Questionnaire` (PHQ-9, GAD-7, BDI-II and others, storing responses), `BehaverseTask` (embeds the Behaverse Unity runtime in an iframe), and a generic `Task` fallback. Adding a node kind is a single folder under `src/runner/nodes/<kind>/index.tsx` that calls `registerNode({ kind, match, toJob, Component, validate? })`; an `import.meta.glob` auto-discovers the module at startup so no other file needs editing.

## M.6 Validation and publishing

Validation is layered. The schema layer enforces type-level constraints (required attributes, enum membership, conditional attribute visibility, redefinition compatibility) at load time through `bpmn-moddle`. The modeler layer enforces structural constraints (every start event has an outgoing flow, every end event has an incoming flow, every gateway is fully wired, sequence flows have valid source/target references) and surfaces issues in the inspector. The runner layer adds per-node validators that run before traversal begins (e.g. a `Questionnaire` requires an instrument; a `BehaverseTask` requires a task identifier from the curated enum). The same per-node validators are exposed to the modeler's lint pass, so authors see the same errors they would see at run time.

Publishing flows through the Behaverse Data Server [@bds]. After signing in with an API key, the author selects *File → Publish*; the modeler uploads the `.studyflow` file (element definitions, attributes, control flow, embedded data schemas) to the user's data-server account, which returns a participant-facing URL. The rendered SVG and PNG are not transferred; the data server renders its own participant UI from the diagram structure. Local stimuli must be referenced by URL or uploaded separately. Each publish creates a new version on the server; earlier versions remain reachable by ID so running studies do not break when authors push updates, and authors tag the local source with a study version attribute on the `Study` element to keep the file in sync with the published artifact.

A `.studyflow` file is plain BPMN 2.0 XML. It diffs in Git, opens in any BPMN-aware tool, and embeds inside an SVG export so that one committed file is both the diagram and the source. We recommend committing the `.studyflow.svg` (with the XML embedded) and giving elements stable IDs (`taskNBackBlock1` rather than the modeler's random `Task_0a1b2c3`) for clean diffs.

## M.7 Three views: rendering the same source three ways

Studyflow renders one `.studyflow` source three ways. The **Study view** is the canonical BPMN-like graph that the modeler displays and that publications embed; it is structural and shows what happens in what order without committing to wall-clock timing. The **Timeline view** is a Gantt-style projection that places elements along a temporal axis when the relevant attributes are present. The four temporal attributes that drive Timeline rendering are `startTime`/`endTime` (when the activity is scheduled to begin and end), `duration` (the allocated time, or the difference between start and end), `progress` (completion as a percentage or label), and `resourceAllocation` (personnel, equipment, or budget, expressed as BPMN lanes or pools). Trial-level timing (stimulus duration, ITI, response window) and study-level timing (visit schedule, follow-ups) share the same mechanism at different zoom levels; the Timeline renderer automatically adapts the axis. The **Checklist view** flattens the diagram into a list of activities, each annotated with the markdown items declared in `checklist.items` on the corresponding `BaseElement`, plus a status flag derived from the runner's logs (pending, running, done, error). Because all elements may carry a `checklist`, the view maps directly onto reporting-guideline items (CONSORT, SPIRIT, STROBE), so coverage against a guideline becomes a property of the diagram rather than a parallel document. The three views share the same source, so changes propagate automatically.

## M.8 EBNF grammar

The grammar below specifies the structure of a Studyflow diagram in EBNF and is provided as a reference companion to the schema; it covers the same elements but is independent of XML and YAML serialization. We include it for readers who want a syntactic summary without inspecting the LinkML schema or its moddle YAML mirror, and as a reference target for third-party parsers that prefer not to depend on a BPMN library. The grammar covers the top-level `Study`/`SubProcess` containers, the event/activity/gateway/data element types, the closed `DataOperation` vocabulary, sequence-flow edges with optional conditions, and the choreography forms used in multi-agent diagrams. Section M.8 can be moved to Supplementary Information without loss.

**Listing 3.** Studyflow EBNF grammar (excerpt; full grammar in `studyflow-modeler/docs/reference/spec.qmd`).

```ebnf
Definitions      ::= Study*
Study            ::= 'Study' Identifier Attribute* (Element | SequenceFlow)*
SubProcess       ::= 'SubProcess' Identifier Attribute*
                     (Element | SequenceFlow | DataAssociation)*
Element          ::= Event | Activity | Gateway | SubProcess
                   | DataObject | DataCatalog | DataStorage | Dataset
                   | Schema | Array | Snapshot
Event            ::= StartEvent | EndEvent
StartEvent       ::= 'StartEvent' Identifier Attribute*
EndEvent         ::= 'EndEvent' Identifier Attribute*
Activity         ::= 'Activity' Identifier ActivityAttributeList Choreography?
ActivityType     ::= '@type' ('CognitiveTask' | 'Questionnaire' | 'Instruction'
                            | 'Rest' | 'VideoGame' | 'BehaverseTask'
                            | 'Script' | 'Manual')
DataOperation    ::= OpClause+
OpClause         ::= '@op' (PrimitiveOp | CompositeOp) DataInput+ DataOutput+
PrimitiveOp      ::= 'Transform' | 'Map' | 'Filter' | 'FlatMap'
                   | 'Reduce' | 'Group'
CompositeOp      ::= 'Compose' PrimitiveOp+
Gateway          ::= 'Gateway' Identifier GatewayAttribute*
GatewayType      ::= '@type' ('Random' | 'StratifiedAllocation' | 'Eligibility'
                            | 'Exclusive' | 'Parallel' | 'Inclusive' | 'Complex')
SequenceFlow     ::= 'SequenceFlow' Identifier Attribute* NodeRef '->' NodeRef
Attribute        ::= Identifier Value
Identifier       ::= [A-Za-z] [A-Za-z0-9_]*
```

## M.9 Reproducibility statement

All artifacts are open source under the MIT license and run in the browser without installation. The hosted modeler is at <https://behaverse.org/studyflow-modeler/app>, the hosted runner at <https://behaverse.org/studyflow-modeler/run.html>, and the documentation at <https://behaverse.org/studyflow-modeler/docs/>. The modeler, runner, the six moddle YAML runtime schemas, the example diagrams, and the documentation all live in `github.com/behaverse/studyflow-modeler`; the canonical LinkML schema is versioned separately at `github.com/behaverse/schemas`.

The versions used in this paper are modeler `v26.0505.dev2` (per `package.json`) and LinkML schema `v25.1217.dev` (per the schema-file header); the schema-file header is authoritative, and a stable release will be tagged at camera-ready time. Pinned dependencies include React 19.2, `bpmn-js` 18.15, `bpmn-moddle` 10.0, `@xyflow/react` 12.10, `zustand` 5.0, `js-yaml` 4.1, Tailwind CSS 4.2, and Vite 7.3. Playwright end-to-end tests cover the create/inspect/save/load/run round-trip for each example diagram.

Example diagrams referenced in the paper ship under `src/assets/examples/`: `consort2025.studyflow` (CONSORT 2025-style randomized trial), `spirit2025.studyflow` (SPIRIT 2025 schedule of enrolment and assessment), and `demo0.studyflow`/`demo1.studyflow`/`demo2.studyflow`. Reproducing every figure requires opening the corresponding `.studyflow` file in the hosted modeler and exporting SVG; runner figures are reproduced by loading the same files in `run.html` with seed 42. Permanent links to the exact source commits will be added to the camera-ready version.
