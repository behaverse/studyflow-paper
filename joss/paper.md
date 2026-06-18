---
title: 'Studyflow: BPMN-based diagrams for experimental workflows in cognitive sciences'
tags:
  - scientific workflows
  - BPMN
  - reproducibility
  - process modeling
authors:
  - name: Morteza Ansarinia
    orcid: https://orcid.org/0000-0001-8335-6704
    affiliation: 1
  - name: Hoorieh Afkari Roshan
    orcid: https://orcid.org/0000-0003-4787-8331
    affiliation: 1
  - name: Pedro Cardoso-Leite
    orcid: https://orcid.org/0000-0002-2848-5527
    affiliation: 1
affiliations:
 - name: University of Luxembourg, Luxembourg
   index: 1
date: 12 February 2026
bibliography: joss_references.bib
---

# Summary

Experimental design in cognitive science research is typically described using free-text descriptions, idiosyncratic diagrams, or code artifacts that can be difficult to understand and may thus negatively impact subsequent studies (e.g., replication studies). Here we present *Studyflow*, a notation based on Business Process Model and Notation (BPMN) for developing diagrams that describe research workflows, particularly experimental studies in cognitive sciences. Studyflow provides experiment-oriented elements such as cognitive tests, participant flow, and data operations by extending the tried-and-tested, widely used BPMN standard. By formalizing experimental research design in a machine-readable, human-understandable format, Studyflow diagrams aim to clarify communication and reduce ambiguity between stakeholders across the research lifecycle, from study design to implementation and publication.

The main goal of Studyflow is to have a single diagram that stays consistent from study planning through execution and reporting, serving as both a protocol description and a structured specification. Its primary users are cognitive science researchers and their collaborators (including technical and non-technical stakeholders: engineers, data scientists, ethics boards, reviewers, and publishers).

The accompanying *\*Studyflow Modeler\** app is a reference implementation of a graphical interface that operationalizes the Studyflow specification for editing, previewing, validating, deploying, and publishing diagrams to support different phases of a scientific study in cognitive sciences.

# Statement of need

The reproducibility crisis in psychology and related fields has shown that insufficient documentation of experimental procedures is a major contributor to non-replicable findings \[@bell2021; @REF/benjamini2020\]. Reproducibility requires more than sharing data and manuscripts; it also requires an explicit, complete description of the *processes* that generated those artifacts \[@aguilar2022; @momeni2026\]. Process models (i.e., workflows) complement data models by documenting the sequence of activities, decision points, and transformations that underlie a scientific study \[@sehgal2011\].

Current workflow approaches seem to split along two needs: 1\) execution which encodes study logic in code or configuration (e.g., GitHub Actions \[@Kinsman2021\]), and 2\) communication which prioritizes human-readable formats (e.g., Protocols.io \[@teytelman2015\]). Neither alone is sufficient to serve all stakeholders. Execution tools remain opaque to non-technical collaborators such as ethics boards and reviewers, while narrative platforms lack the formal structure needed for developers, machine validation, or automation. Domain-specific workflow engines can improve reusability within particular communities, but they typically require specialized programming expertise that limits accessibility. Other approaches target specific aspects of research (data organization, computational execution, or reporting) and constitute important building blocks, but no single representation currently spans the full lifecycle of scientific research in a form that scientists, engineers, ethics boards, and journal editors can all read and use.

Studyflow addresses this gap by extending BPMN, a widely used standard for process modeling, with elements specific to experimental cognitive science: activity types for cognitive tests, questionnaires, and instructions; gateways to encode branching such as random assignment, stratified allocation, and inclusion/exclusion criteria; and data elements aligned with community standards (BIDS, Psych-DS, BDM \[@bids; @psychds; @bdm\]). A single Studyflow diagram serves as both a human-readable protocol and a machine-readable specification that can be shared, validated, versioned, and integrated with downstream tooling across the study lifecycle (from initial design through data collection, analysis, and publication).

# **State of the field**

Scientific workflows are supported by a broad ecosystem of tools spanning custom scripts, graphical pipeline builders, directed acyclic graph (DAG)-based engines, portable workflow languages, and protocol registries \[@zhao2008; @cuevasvicenttin2013\]. User-friendly platforms such as KNIME \[@berthold2009\], RapidMiner \[[@mierswa2026](https://doi.org/10.1145/1150402.1150531)\], and Galaxy \[@galaxy2024\] have democratized pipeline composition through graphical interfaces, while domain-specific frameworks (e.g., PsychoPy for psychology, scikit-learn and Tidymodels for machine learning) lowered the barrier within individual communities.

Many modern workflow management systems treat processes as directed acyclic graphs. General-purpose orchestrators (e.g., Apache Airflow, Kedro, GitHub Actions) and science-focused engines (e.g., Nextflow, Pegasus) automate task scheduling, dependency management, and scalable execution \[@airflow; @kedro; @ciworkflows; @nextflow\].

Workflow languages such as the Common Workflow Language (CWL) and Workflow Description Language (WDL) further improve cross-platform execution and provenance for computations \[@cwl; @wdl; @cromwell\]. Domain-specific ecosystems (e.g., NiPype/Pydra for neuroimaging) provide powerful analysis pipelines within their communities \[@nipype; @pydra\].

Complementing execution-focused tools, protocol registries and methodological standards address documentation and reporting. Platforms like protocols.io support narrative sharing of methods \[@teytelman2015\], and reporting guidelines such as CONSORT (Consolidated Standards of Reporting Trials) and STARD (Standards for Reporting Diagnostic Accuracy Studies) enforce structured disclosure at the publication stage. Data standards and ontologies such as Schema.org, BIDS, Psych-DS and the Behaverse data model prescribe consistent dataset organization \[@schemaorg; @bids; @psychds\].

Notations like Systems Biology Graphical Notation (SBGN) provide visual conventions for specific scientific contexts (e.g., systems biology) \[@sbgn\], and emerging tools such as Viash wrap scripts into containerized, pipeline-ready modules. On the process-modeling side, BPMN offers a widely adopted graphical notation with standard serialization and an explicit extension mechanism \[@bpmnspec; @white2004\]. Its extensibility has been demonstrated in domains such as machine learning workflows \[@tetzlaff2022bpmn4sml\], human-AI collaboration \[@ait2024\], and healthcare ([@pufahl2022](https://www.sciencedirect.com/science/article/pii/S0306437922000217); most notably BPMN4CP for clinical pathways \[[@braun2014](https://ieeexplore.ieee.org/document/6999261/)\]. For a systematic review of BPMN extensions, see \[[@zarour2020](https://laas.hal.science/hal-02419886v1/file/Article%20Lit%20Rev%20BPMN%20ext.pdf)\].

Other general formalisms such as Unified Modeling Language (UML) Activity Diagrams and Petri nets provide alternative foundations \[@uml\_activity; @petri\] but typically do not offer a domain-aligned vocabulary for experimental studies and can be cumbersome as a shared communication artifact across heterogeneous stakeholders.

Despite their many benefits, current tools exhibit important limitations for our purposes. Workflow representations defined in code, YAML, or domain-specific DSLs remain opaque to non-technical stakeholders. Even languages designed for human readability (e.g., WDL) require familiarity with software patterns, leaving protocols split between text descriptions and code artifacts (these languages mostly encode researchers' intent in code/configuration). Outside computational pipelines, experimental procedures are typically documented in free-form text or ad hoc lab conventions, with no formal, unifying structure that spans design, data collection, analysis, and reporting. Several checklists enforce structure but only at the publication stage, not during planning and execution \[@barrowman2020vtree\]. Provenance systems track computational lineage well but rarely capture the full experimental context (e.g., manual human annotations, randomization decisions, protocol deviations), creating a boundary between the well-tracked computational graph and the partially represented experimental documentation \[@souza2020provenance; @simmons2018provenance\_sport\]. Indeed, recent work has shown that one-size-fits-all provenance and workflow systems perform poorly in practice and that their notation needs to be optimized for the domain of use \[@simmons2018provenance\_sport\]. Similarly, ontologies developed for process modeling, while numerous, require substantial upfront effort and are often too complex to reuse effectively \[@norouzi2025semantic\_processes\]. Most critically, no single representation serves all stakeholders: execution specifications target developers and platforms, while collaborators, ethics boards, and reviewers rely on separate, potentially inconsistent narrative documents.

BPMN's graphical clarity, formal execution semantics, and proven extensibility (e.g., BPMN4CP for clinical pathways, extensions for human-AI collaboration \[@ait2024bpmn\_humanagent\], and ML workflow extensions \[@tetzlaff2022bpmn4sml\]) make it a strong foundation for bridging this gap. BPMN's data representation capabilities have also been extended through mechanisms such as extensionElements or vendor namespaces so existing BPMN parsers ignore them gracefully \[@magnani2009bpdmn\]. Yet its generic semantics do not natively represent experiment-specific concepts such as randomization, counterbalancing, inclusion/exclusion pathways, or structured links between protocol steps and research datasets, highlighting the need for domain-specific extensions.

Recent large language model (LLM)-assisted BPMN authoring tools can accelerate diagram creation from text (e.g., ProMoAI, BPMN-ChatBot) \[@khourani2024; @kopke2024; @kourani2024promoai\], but evaluations show that while LLMs achieve competitive syntactic quality, they still fall short in semantic fidelity and domain-specific validation \[@lauer2026assessing\]. They also do not resolve the absence of domain semantics and validation rules needed to represent scientific studies. Studyflow builds on BPMN's familiarity and ecosystem while adding a science-oriented profile and schema, so that a single diagram can serve as both a human-understandable protocol and a machine-readable specification across the study lifecycle.

# **Software design**

Designing a process notation for experimental cognitive science requires balancing competing demands: formal precision for machine validation versus visual simplicity for non-technical stakeholders, domain-specificity versus interoperability with existing tooling, and a stable language specification versus rapid iteration on features. The architecture of Studyflow reflects deliberate trade-offs among these requirements to support both usability and long-term adoption.

## **Extend BPMN rather than invent a new notation**

The central design decision was whether to create a standalone domain-specific language (DSL) or to extend an existing standard. A standalone DSL would offer maximum expressiveness for experimental constructs (e.g., task parametrization, variable naming) but would require building parsers, renderers, and an ecosystem from scratch, and would impose yet another notation on a community already fragmented across tools. Adopting BPMN as the host notation trades some expressiveness for three practical advantages: (i) Studyflow diagrams remain valid BPMN and can be opened and versioned with any BPMN-compliant tool; (ii) researchers already exposed to flowchart-like notations can read diagrams without learning a new visual grammar, lowering adoption barriers; and (iii) BPMN's formal extension mechanism (\`extensionElements\` and extended attributes) provides a constrained way to add domain semantics without breaking the base standard \[@stroppi2011\]. Studyflow introduces its domain-specific elements in a \`studyflow:\` namespace, so that a generic BPMN parser gracefully ignores study-specific metadata while a Studyflow-aware tool can validate and render it consistently.

## **Separate the specification from tooling**

A recurring failure pattern in scientific projects is coupling the notation to a single application: when the tool is abandoned, the notation becomes unreadable. Studyflow addresses this by maintaining the language as an independent, machine-readable LinkML schema \[@moxon2025\] that serves as the single source of truth for definitions and rules, and enables compliance with FAIR principles (Findable, Accessible, Interoperable, Reusable; \[@fair\]). This separation has several practical implications: i) the schema can generate documentation, validation rules, and independent utilities, ii) third-party tools (e.g., linters, execution engines, or converters) can target the same specification without depending on specific software, and iii) the language can evolve independently of any particular software implementation.

The schema defines a process as a (N, E, T, $\\tau$, $\\lambda$) tuple, where N is a finite set of elements (activities, gateways, events), $E\\subseteq N\\times N$ represents sequence flows (edges), T is a set of pre-defined node types (Activity, Event, Gateway), $\\tau: N \\rightarrow T$ is a typing function that assigns types (Activity, Event, Gateway) to the nodes, and $\\lambda$ is a labeling function that assigns additional attributes to the nodes (e.g., event triggers, gateway logic, implementations). The elements are connected by directed edges, forming a graph that represents the flow of the study. The schema also introduces additional type hierarchies and attributes to the elements, allowing for a more detailed representation of the workflow, tailored to the specific needs of experimental cognitive sciences while remaining compatible with BPMN structure.

The accompanying \*\*Studyflow Modeler\*\* application is explicitly positioned as a working example that demonstrates how a compliant tool can read, write, and validate diagrams, not the canonical definition of the language. The language is defined by the schema (studyflow.schema.yaml), which is versioned independently and serves as the single source of truth; the modeler tracks the schema but does not own it. This separation has practical consequences: the schema can generate documentation and utilities independently of the editor, and third-party tools (e.g., linters or execution engines) can target the same specification without depending on the modeler's codebase. The trade-off is added overhead, but this cost is justified by the longevity and portability it provides as a community-oriented standard.

## **Prioritize communication over execution**

Workflow systems typically optimize for one of two audiences: developers who need executable pipelines, or domain experts who need readable protocols \[@zhao2008; @ghosh2025\]. Studyflow deliberately prioritizes the latter to improve accessibility and shared understanding. Diagrams are designed so that a single artifact can be reviewed by an ethics board, shared with collaborators, and attached to a publication without requiring any programming knowledge. This means Studyflow intentionally hides execution semantics (e.g., orchestration, scheduling policies) that would add complexity without serving the communication goal. Where execution is needed, the schema-driven interchange format allows downstream tools to consume Studyflow diagrams and map them onto executable pipelines, preserving a clean boundary between protocol description and runtime concerns. To demonstrate this, the modeler also includes a "publish" tool that deploys diagrams as an executable study to the Behaverse Data Server \[@bds\], which can then be used for data collection.

## **Combine process and data in one diagram**

Most workflow tools separate process logic from data descriptions (e.g., UML): the pipeline defines what runs (e.g., UML activity diagram), while a separate data model defines what is produced (e.g., UML class diagram). This split forces researchers to maintain two representations that can drift apart over time. Studyflow's notation allows data artifacts (datasets consumed, transformed, or produced by each activity) to be annotated directly on the process diagram through data elements and operations to maintain alignment between process and data. The trade-off is increased visual density. To manage this, the visual representations support \*collapsible views\* so that researchers can toggle between a process-only view and a full process-data view depending on their needs. This dual representation supports traceability from high-level protocol design to data products and enables validation of both process logic and data dependencies within a single reviewable artifact.

## **Use schema-driven tooling for incremental development**

The modeler's user interface is generated from the LinkML schema rather than being hard-coded. When a new element type or attribute is added to the schema, the inspector panel, palette entries, and constraints update accordingly without manual UI work. This design choice reduces the cost of evolving the notation (which is critical during early adoption when community feedback drives frequent schema changes). But it constrains the UI to patterns that can be generalized from schema. Moreover, highly specialized interactions (e.g., drag gestures, visual alignments, colors) require additional custom implementation in the tools. In practice, the schema-driven approach has so far proven sufficient for the current element set while keeping the modeler lightweight (only React and \`bpmn-js\`) and deployable as a webapp with no server dependency.

##    **Define domain-specific extensions for cognitive experiment**

Beyond core BPMN elements (events, activities, gateways, data artifacts), cognitive science experiments have specific concepts that are not natively represented in BPMN (e.g., tests, consents, participant inclusion/exclusion criteria, data formats). Studyflow introduces a set of domain-specific extensions to capture these concepts while maintaining the underlying BPMN structure and ensuring compatibility with existing tools. These include: \*\*new activity types\*\* as BPMN tasks (e.g., cognitive tests, questionnaires, instructions, video games, rest), \*\*new attributes\*\* for annotating experimental parameters (e.g., cognitive test parameters, documentations, checklists, data formats), \*\*new gateways\*\* encoding participant branching such as random assignment, stratified allocation, and inclusion criteria, and \*\*data elements and operations\*\* for annotating which (and how) elements consume data, aligned with community standards (e.g., BIDS, Psych-DS, BDM).

| ![][image1] |
| :---- |
| **Figure 1\.** Additional domain-specific elements for experimental cognitive sciences in the studyflow visual notation (for a complete list see documentations). |

#  **Contributions**

Studyflow contributes three open, independently usable artifacts to the scientific workflow ecosystem:

1\. **\*\*An open language specification\*\*** maintained as a versioned LinkML schema (\`studyflow.linkml.yaml\`). The schema defines element types, attribute constraints, and validation rules for experimental workflow diagrams. The specification is independent of any particular implementation.

2\. **\*\*A set of representative example diagrams\*\*** that encode common experimental patterns (e.g., CONSORT-style randomized controlled trial, within-subject crossover designs, and multi-session cognitive testing protocols) as standard BPMN 2.0 XML with \`studyflow:\` extensions. These examples serve as reusable templates and as regression tests for the specification itself facilitating adoption and validation. Because diagrams are valid BPMN 2.0 XML (i.e., extra elements gracefully degrade to standard BPMN), they can be opened in any compliant editor (e.g., Camunda Modeler, bpmn.io) and stored in version-control systems with meaningful diffs.

3\. **\*\*Studyflow Modeler\*\***, an open-source web application (React \+ \`bpmn-js\` \[@bpmnjs\], MIT license) that operationalizes the specification through a schema-driven graphical editor and enables creation, validation, and sharing of Studyflow diagrams. The modeler is a client-side app without any server and continuously deployed at https://behaverse.org/studyflow-modeler/.

All artifacts are publicly available under permissive MIT licenses.

## **\#\# Examples**

Established experimental design patterns can be directly represented as Studyflow diagrams. Figure 2 shows a CONSORT-style randomized controlled trial (RCT). The logic is encoded with explicit randomization gateways, inclusion/exclusion pathways, events, and annotations.

| ![][image2]  | ![][image3]  |
| ----- | :---- |
| **Figure 2\.** A randomized controlled trial with randomization, pathways, and annotations. (A) Original CONSORT 2025 diagram. (B) The same CONSORT diagram reproduced using studyflow as a human/machine-readable diagram. The studyflow diagram can be further customized to convey more details via symbols or metadata. |  |

A second use case, Figure 3, is a simple cognitive task design, where trial sequences, instruction screens, logic, and data are captured as explicit elements rather than buried in scripts.

| ![][image4] | ![][image5] |
| :---- | :---- |
| `<?xml version="1.0" encoding="UTF-8"?> <bpmn2:definitions ...>   <bpmn2:process id="NBack"  ...>     <bpmn2:extensionElements>       <studyflow:study />     </bpmn2:extensionElements>     <bpmn2:task id="Trial1" name="b" documentation="Display a letter on screen" studyflow:url="behaverse://show_stimulus">     <bpmn2:boundaryEvent id="ISI" name="1s" attachedToRef="Trial1">     </bpmn2:endEvent> ...     <bpmn2:association id="Association1" associationDirection="None" sourceRef="Trial3" targetRef="TextAnnotation1" />     <bpmn2:textAnnotation id="TextAnnotation1">       <bpmn2:text>Non-target</bpmn2:text>     </bpmn2:textAnnotation> ...` |  |
| **Figure3.** (A) Common visualization of an N-back task. (B) A Studyflow diagram of an N-back task; sequence flow is shown using start, end, and directed lines, interrupting timer events manage timing, and annotations describe the elements. (C) XML representation of the studyflow diagram also contains additional information to communicate and execute the workflow (for brevity, only part of the XML is shown). |  |

# **Limitations**

While Studyflow aims to provide a unified and accessible representation of experimental workflows, it has several limitations. First, although BPMN improves familiarity for some users already exposed to flowchart notations, it may still introduce a learning curve for researchers without prior exposure to process modeling notations. 

Second, representing both process and data within a single diagram can increase visual complexity, particularly for large or multi-session studies, which may affect readability despite the use of collapsible views and layered representations. 

Third, Studyflow focuses on communication and specification rather than execution, and therefore requires integration with external systems for full automation of experimental workflows, a deliberate design choice that prioritizes stakeholder alignment over one-click execution.

Finally, as an emerging specification, the current ecosystem of tools and community adoption is still limited, which may constrain immediate interoperability and long-term sustainability without broader community uptake.

# **AI usage disclosure**

Generative AI tools were used to assist with language refinement of portions of this paper. All AI-assisted text was reviewed, edited, and validated by the authors. No AI tool was used as an author, and the authors take full responsibility for the content and any errors.

# **Acknowledgements**

We thank collaborators and early users for feedback on the specification and modeler.
