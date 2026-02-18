---
title: 'Studyflow: BPMN-based diagrams for scientific workflows'
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

Experimental workflows in cognitive sciences are often obscured by free-text descriptions, informal figures, or code artifacts that are difficult to reproduce in later studies [@aguilar2022experiments; @bell2021perspectives]. We present **Studyflow**, a BPMN-based notation to develop formal diagrams for research, in particular in experimental cognitive studies. Studyflow provides experiment-oriented elements such as cognitive tests, data operators, and flow of participants while maintaining familiarity with the widely known BPMN standard. By formalizing experimental studies in a machine-readable, human-understandable format, studyflow diagrams clarify communication between different stakeholders across the research lifecycle.

The accompanying **Studyflow Modeler** is a reference implementation of an editor that operationalizes the studyflow specification through an interactive user interface. It uses React and `bpmn-js` [@bpmnjs] for rendering, editing, simulating, and deploying studyflow diagrams.

# Statement of need

Reproducibility in cognitive sciences requires more than sharing data and manuscripts; it also requires an explicit description of the process that generated that artifacts [@aguilar2022experiments; @momeni2026guidelines]. Process models, i.e., workflows, complement data models by documenting the sequence of activities, decision points, and transformations that underlie a scientific study [@sehgal2011]. The reproducibility crisis in psychology and related fields has demonstrated that insufficient documentation of experimental procedures is a major contributor to non-replicable findings [@bell2021perspectives; @zeevi2020time]. Existing workflow approaches tend to split across two needs: execution (e.g., orchestration as in GitHub Actions [@Kinsman2021]) that encodes study logic implicitly in code, and communication (e.g., Protocols.io [@teytelman2015]) that is readable and standardized but lacks extendability, a particular set of concepts, and explicit links between implementation and researcher's intent. Further domain-specific workflow engines improve reproducibility in particular communities, but they often require rare programming expertise and do not provide interoperability to non-technical stakeholders (e.g., ethics boards, clinicians, funding agencies, and collaborators).

Studyflow addresses this gap by extending BPMN, a widely used standard language for process modeling, with elements for conducting experiments in cognitive sciences (such as experimental task types, branching gateways, data-aware annotations aligned with community data standards such as BIDS, Psych-DS, Behaverse Data Model [@bids; @psychds; @bdm]). A single studyflow diagram can serve as both a human-readable protocol and a machine-readable specification to validate, version, and integrate downstream tooling across the study lifecycle.

## State of the field

Scientific workflows are supported by a broad ecosystem of tools spanning custom scripts, graphical pipeline builders, DAG-based engines, portable workflow languages, and protocol registries [@zhao2008scientific_workflows; @cuevasvicenttin2013]. User-friendly platforms such as KNIME, RapidMiner, and Galaxy [@thegalaxycommunity2024] democratized pipeline composition through graphical interfaces, while domain-specific frameworks (e.g., PsychoPy for psychology, scikit-learn and Tidymodels for machine learning) lowered the barrier within individual communities. Modern workflow management systems treat processes as directed acyclic graphs: general-purpose orchestrators (e.g., Apache Airflow, Kedro, CI workflows like GitHub Actions) and science-focused engines (e.g., Nextflow, Pegasus) automate task scheduling, dependency management, and scalable execution [@airflow; @kedro; @ci_workflows; @nextflow]. Workflow languages such as CWL and WDL further improve cross-platform execution and provenance for computations [@cwl; @wdl; @cromwell], and domain-specific ecosystems (e.g., NiPype/Pydra for neuroimaging) provide powerful analysis pipelines within their communities [@nipype; @pydra].

Complementing execution-focused tools, protocol registries and methodological standards address documentation and reporting: platforms like protocols.io support narrative sharing of methods [@teytelman2015], reporting guidelines such as CONSORT and STARD enforce structured disclosure at the publication stage, and data standards and ontologies such as SchemaOrg, BIDS and Psych-DS prescribe consistent dataset organization [@schemaorg; @bids; @psychds]. Notations like SBGN provide visual conventions for specific scientific contexts (e.g., systems biology) [@sbgn], and emerging tools such as Viash wrap scripts into containerized, pipeline-ready modules. On the process-modeling side, BPMN offers a widely adopted graphical notation with standard serialization and an explicit extension mechanism [@bpmn_spec; @white2004introduction], and its extensibility has been demonstrated in domains such as machine learning workflows [@tetzlaff2022bpmn4sml] and human-AI collaboration [@ait2024bpmn_humanagent]. Other general formalisms such as UML Activity Diagrams and Petri nets provide alternative foundations [@uml_activity; @petri] but typically do not offer a domain-aligned vocabulary for experimental studies and can be cumbersome as a shared communication artifact across heterogeneous stakeholders.

Despite this progress, current tools exhibit recurring limitations. Workflow representations defined in code, YAML, or domain-specific DSLs remain opaque to non-technical stakeholders; even languages designed for human readability (e.g., WDL) require familiarity with software patterns, leaving protocols split between text descriptions and code artifacts (they largely encode researcher's intent in code/configuration). Outside computational pipelines, experimental procedures are typically documented in free-form text or ad hoc lab conventions, with no formal, unifying structure that spans design, collection, analysis, and reporting. Several checklists enforce structure but only at the publication stage, not during planning and execution [@barrowman2020vtree]. Provenance systems track computational lineage well but rarely capture the full experimental context (e.g., manual human annotations, randomization decisions, protocol deviations), creating a boundary between the well-tracked computational graph and the partially represented experimental documentation [@souza2020provenance; @simmons2018provenance_sport]. Indeed, recent work has shown that one-size-fits-all provenance and workflow systems perform poorly in practice and their notation needs to be optimized for the domain of use [@simmons2018provenance_sport]. Similarly, ontologies developed for process modeling, while numerous, require substantial upfront effort and are often too complex to reuse effectively [@norouzi2025semantic_processes]. Most critically, no single representation serves all stakeholders: execution specifications target developers and platforms, while collaborators, ethics boards, and reviewers rely on separate, potentially inconsistent narrative documents.

BPMN's graphical clarity, formal execution semantics, and proven extensibility (e.g., BPMN4CP for clinical pathways, extensions for human-AI collaboration [@ait2024bpmn_humanagent], and ML workflow extensions [@tetzlaff2022bpmn4sml]) make it a strong foundation for bridging this gap. BPMN's data representation capabilities have also been extended through conservative additions that blend gracefully into the existing notation [@magnani2009bpdmn]. Yet its generic semantics do not natively represent experiment-specific concepts such as randomization, counterbalancing, inclusion/exclusion pathways, or structured links between protocol steps and research datasets.

Recent LLM-assisted BPMN authoring tools can accelerate diagram creation from text (e.g., ProMoAI, BPMN-ChatBot) [@khourani2024; @kopke2024; @kourani2024promoai], but evaluations show that while LLMs achieve competitive syntactic quality, they still fall short in semantic fidelity and domain-specific validation [@lauer2026assessing], and they do not resolve the absence of domain semantics and validation rules needed to represent scientific studies. Studyflow builds on BPMN's familiarity and ecosystem while adding a science-oriented profile and schema, so that a single diagram can serve as both a human-understandable protocol and a machine-readable specification across the study lifecycle.

# Software design

Designing a process notation for experimental cognitive science requires balancing competing demands: formal precision for machine validation versus visual simplicity for non-technical stakeholders, domain-specificity versus interoperability with existing tooling, and a stable language specification versus rapid iteration on features. The architecture of studyflow reflects deliberate trade-offs among these tensions.

## Extend BPMN rather than invent a new notation

The central design decision was whether to create a standalone domain-specific language (DSL) or to extend an existing standard. A standalone DSL would offer maximum expressiveness for experimental constructs (e.g., trial sequences, task parametrization, variable naming) but would require building parsers, renderers, and an ecosystem from scratch, and would impose yet another notation on a community already fragmented across tools. Adopting BPMN as the host notation trades some syntactic features for three concrete benefits: (i) studyflow diagrams remain valid BPMN and can be opened, diffed, and versioned with any BPMN-compliant tool; (ii) researchers already exposed to flowchart-like notations can read diagrams without learning a new visual grammar; and (iii) BPMN's formal extension mechanism (`extensionElements` and typed attributes) provides a constrained way to add domain semantics without breaking the base standard [@bpmn_spec]. Studyflow introduces its constructs through a `studyflow:` namespace, so that a generic BPMN parser gracefully ignores study-specific metadata while a studyflow-aware tool can validate and render it.

## Separate the language specification from tooling

A recurring failure mode in scientific workflow projects is coupling the notation to a single application: when the tool is abandoned, the notation becomes unreadable. Studyflow counters this by maintaining the language as an independent, machine-readable LinkML schema [@moxon2025linkml] that serves as the single source of truth for element definitions, attribute constraints, and validation rules. LinkML is an open data modeling framework that simplifies schema authoring, validation, and sharing while enabling compliance with FAIR data standards; it has seen increasing adoption across biology, chemistry, biomedicine, and other fields [@moxon2025linkml]. The accompanying **Studyflow Modeler** application is explicitly positioned as one reference implementation of this schema, not the canonical artifact. This separation has practical consequences: the schema can generate JSON Schema validators, documentation, and conversion utilities independently of the editor, and third-party tools (e.g., CLI linters or execution engines) can target the same specification without depending on the modeler's codebase. The trade-off is the added overhead, but this cost is justified by the longevity and portability it affords a community standard.

## Prioritize communication over execution

Workflow systems typically optimize for one of two audiences: developers who need executable pipelines, or domain experts who need readable protocols [@zhao2008scientific_workflows; @ghosh2025reproducible_digital_health]. Studyflow deliberately prioritizes the latter. Diagrams are designed so that a single artifact can be reviewed by an ethics board, shared with collaborators, and attached to a publication without requiring any programming knowledge. This means studyflow intentionally hides execution semantics (e.g., container orchestration, scheduling policies, retry logic) that would add complexity without serving the communication goal. Where execution is needed, the schema-driven interchange format allows downstream tools to consume studyflow diagrams and map them onto executable pipelines, preserving a clean boundary between protocol description and runtime concerns.

## Process and data in a joint diagram

Most workflow tools separate process logic from data descriptions: the pipeline defines what runs, while a separate data standard (e.g., BIDS, Psych-DS) defines what is produced. This split forces researchers to maintain two representations that can drift apart. Studyflow's architecture allows data artifacts (datasets consumed, transformed, or produced by each step) to be annotated directly on the process diagram through data elements and operators. The trade-off is increased visual density. To manage this, the modeler supports collapsible views so that researchers can toggle between a process-only view and a full process-and-data view. This dual representation supports traceability from high-level protocol design to downstream data products and enables validation of both process logic and data dependencies within a single reviewable artifact.

## Schema-driven tooling for incremental evolution

The modeler's user interface is generated from the LinkML schema rather than hard-coded. When a new element type or attribute is added to the schema, the property panels, palette entries, and validation rules update accordingly without manual UI work. This design choice reduces the cost of evolving the notation—critical during early adoption when community feedback drives frequent schema changes. But it constrains the UI to patterns that can be generalized from schema metadata (forms, palettes, and context menus). Highly specialized interactions (e.g., drag gestures or icons) require specialized code in the tools. In practice, the schema-driven approach has so far proven sufficient for the current element set while keeping the modeler lightweight (React + `bpmn-js`) and deployable as a static web application with no server dependency.

## Functionality

Beyond core BPMN elements (events, activities, gateways, data artifacts), studyflow adds:

- **Domain-specific activity types** for cognitive science experiments (e.g., cognitive tests, video games, questionnaires, instructions), introduced as BPMN task specializations.
- **Study-aware gateways** encoding participant-level branching such as random assignment, stratified allocation, and inclusion/exclusion criteria.
- **Data elements and operators** for annotating which steps consume or produce datasets, aligned with community data standards (e.g., BIDS, Psych-DS).

# Research impact

## Contributions

Studyflow contributes three open, independently usable artifacts to the scientific workflow ecosystem:

1. **An open language specification** maintained as a versioned LinkML schema (`assets/studyflow.linkml.yaml`). The schema defines element types, attribute constraints, and validation rules for experimental workflow diagrams. The specification is independent of any particular implementation.

2. **A set of representative example diagrams** that encode common experimental patterns (e.g., CONSORT-style randomized controlled trial, within-subject crossover designs, and multi-session cognitive testing protocols) as standard BPMN 2.0 XML with `studyflow:` extensions. These examples serve as reusable templates and as regression tests for the specification itself.

3. **Studyflow Modeler**, an open-source, client-side web application (React + `bpmn-js` [@bpmnjs], MIT license) that operationalizes the specification through a schema-driven graphical editor. The modeler is continuously deployed at https://behaverse.github.io/studyflow-modeler/.

All artifacts are publicly available under permissive licenses. Because diagrams are valid BPMN 2.0 XML, they can be opened in any compliant editor (e.g., Camunda Modeler, bpmn.io) and stored in version-control systems with meaningful diffs.

## Example

Established experimental patterns can be directly represented as studyflow diagrams. Figure 1 shows a CONSORT-style randomized controlled trial (RCT). The logic is encoded with explicit randomization gateways, inclusion/exclusion pathways, and data annotations.

![Example studyflow showing a CONSORT trial with randomization, exclusion pathways, and annotations. See documentation website for comparison against the original CONSORT diagram.](figures/consort2025.studyflow.png)

A second use case, Figure 2, is cognitive task design, where trial sequences, instruction screens, branching logic, and data are captured as explicit elements rather than buried in scripts.

![(A) Common visualization of an N-back task. (B) A studyflow diagram showing N-back cognitive task. Timer events are used to manage timing, and data elements link task steps to output datasets.](figures/nback.both.png)

# AI usage disclosure

Generative AI tools were used to assist with language refinement of portions of this paper. All AI-assisted text was reviewed, edited, and validated by the authors. No AI tool was used as an author, and the authors take full responsibility for the content and any errors.

# Acknowledgements
We thank collaborators and early users for feedback on the studyflow specification and editor.

# References
