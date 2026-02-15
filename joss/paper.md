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

Scientific processes are often obscured by free-text descriptions, informal figures, or code artifacts that are difficult to reproduce in later studies. We present **Studyflow**, a BPMN extension providing formal diagrams for scientific research. Studyflow adds experiment-oriented constructs such as cognitive tests, data operators, and assignment logic while maintaining compatibility with familiar BPMN notation. By formalizing experimental studies in a machine-readable, human-understandable format, Studyflow clarifies communication between different stakeholders across the research lifecycle.

Studyflow contributes a process-modeling framework that complements common data standards by making study protocols explicit, reviewable, and machine-validated. The project provides (i) an open language specification, (ii) representative example diagrams that encode common experimental patterns, and (iii) Studyflow Modeler: an open-source web-based modeler that operationalize the specification and lowers the barrier to producing shareable, version controlled workflow diagrams. Together, these artifacts provide a concrete foundation for integrating protocol diagrams into scientific practices and connecting high-level research intent to downstream data products in an interoperable format.

# Statement of need

Reproducibility in science requires more than sharing data and manuscripts; it also requires an explicit description of the process that generated those artifacts. Process models complement data models by documenting the sequence of activities, decision points, and transformations that underlie a scientific study [@sehgal2011].

Existing workflow approaches tend to split across two needs: execution-focused tooling (e.g., orchestration frameworks and pipeline languages) that encodes study logic implicitly in code, and domain-generic process modeling (e.g., BPMN) that is readable and standardized but lacks scientific-study concepts such as participant assignment, inclusion/exclusion logic, and explicit links between workflow steps and research datasets. Domain-specific workflow engines improve executable reproducibility in particular communities, yet they often require programming expertise and do not provide a shared modeling layer interpretable by non-technical stakeholders (e.g., ethics boards, clinicians, and collaborators). Studyflow addresses this gap by extending BPMN with study-specific constructs—experimental task types, branching gateways, and data-aware annotations aligned with community standards (e.g., BIDS/BDM/Psych-DS [@bids; @bdm; @psychds])—so a single diagram can serve as both a human-readable protocol and a machine-readable specification to validate, version, and integrate downstream tooling across the study lifecycle.

## State of the field

Scientific workflows are supported by a broad ecosystem of tools spanning custom scripts, graphical pipeline builders, DAG-based engines, portable workflow languages, and protocol registries. User-friendly platforms such as KNIME, RapidMiner, and Galaxy [@thegalaxycommunity2024] democratized pipeline composition through graphical interfaces, while domain-specific frameworks (e.g., PsychoPy for psychology, scikit-learn and Tidymodels for machine learning) lowered the barrier within individual communities. Modern workflow management systems treat processes as directed acyclic graphs: general-purpose orchestrators (e.g., Apache Airflow, Kedro, CI workflows like GitHub Actions) and science-focused engines (e.g., Nextflow, Pegasus) automate task scheduling, dependency management, and scalable execution [@airflow; @kedro; @ci_workflows, @nextflow]. Workflow languages such as CWL and WDL further improve cross-platform execution and provenance for computations [@cwl; @wdl; @cromwell], and domain-specific ecosystems (e.g., NiPype/Pydra for neuroimaging) provide powerful analysis pipelines within their communities [@nipype; @pydra]. Complementing execution-focused tools, protocol registries and methodological standards address documentation and reporting: platforms like protocols.io support narrative sharing of methods [@protocolsio], reporting guidelines such as CONSORT and STARD enforce structured disclosure at the publication stage, and data standards and ontologies such as SchemaOrg, BIDS and Psych-DS prescribe consistent dataset organization [@schemorg; @bids; @psychds]. Notations like SBGN provide visual conventions for specific scientific contexts (e.g., systems biology) [@sbgn], and emerging tools such as Viash wrap scripts into containerized, pipeline-ready modules. On the process-modeling side, BPMN offers a widely adopted graphical notation with standard serialization and an explicit extension mechanism [@bpmn_spec; @white2004introduction], and recent LLM-assisted authoring tools (e.g., ProMoAI, BPMN-ChatBot) can accelerate diagram creation from informal text [@khourani2024; @kopke2024]. Other general formalisms such as UML Activity Diagrams and Petri nets provide alternative foundations [@uml_activity; @petri] but typically do not offer a domain-aligned vocabulary for experimental studies and can be cumbersome as a shared communication artifact across heterogeneous stakeholders.

Despite this progress, current tools exhibit recurring limitations. Workflow representations defined in code, YAML, or domain-specific DSLs remain opaque to non-technical stakeholders; even languages designed for human readability (e.g., WDL) require familiarity with software patterns, leaving protocols split between text descriptions and code artifacts (they largely encode researcher's intent in code/configuration). Outside computational pipelines, experimental procedures are typically documented in free-form text or ad hoc lab conventions, with no formal, unifying structure that spans design, collection, analysis, and reporting. Several checklists enforce structure but only at the publication stage, not during planning and execution. Provenance systems track computational lineage well but rarely capture the full experimental context (e.g., manual human annotations, randomization decisions, protocol deviations), creating a boundary between the well-tracked computational graph and the partially represented experimental documentations. Most critically, no single representation serves all stakeholders: execution specifications target developers and platforms, while collaborators, ethics boards, and reviewers rely on separate, potentially inconsistent narrative documents.

BPMN's graphical clarity, formal execution semantics, and proven extensibility (e.g., BPMN4CP for clinical pathways, extensions for human-AI collaboration) make it a strong foundation for bridging this gap, yet its generic semantics do not natively represent experiment-specific concepts such as randomization, counterbalancing, inclusion/exclusion pathways, or structured links between protocol steps and research datasets.

Recent LLM-assisted BPMN authoring tools can accelerate diagram creation from text (e.g., ProMoAI, BPMN-ChatBot) [@khourani2024; @kopke2024], but they do not resolve the absence of domain semantics and validation rules needed to represent scientific studies. Studyflow builds on BPMN's familiarity and ecosystem while adding a science-oriented profile and schema, so that a single diagram can serve as both a human-understandable protocol and a machine-readable specification across the study lifecycle.


<!-- Existing workflow engines and data standards provide important building blocks, but they often emphasize one aspect of research (data, execution, or reporting) rather than a shared, human-readable protocol that can be communicated across scientists, engineers, ethics boards, and other stakeholders with diverse expertise and responsibilities. -->

<!-- Just like ERD or UML for data or code, one widely used solution for process modeling is BPMN. BPMN (Business Process Model and Notation) is a general-purpose process modeling in industry and business domains. BPMN provides a well adopted process modeling standard [@white2004introduction], yet it lacks constructs tailored to the needs of experimental sciences. Studyflow extends BPMN and targets researchers who need a formal, shareable way to describe study protocols while keeping them compatible with established notations. -->

# Software design

Studyflow is designed around three principles: **interoperability**, **schema-first**, and **stakeholder readability**.

**Interoperability via BPMN extension.** Rather than introducing a new notation, Studyflow leverages BPMN’s extension points to introduce a `studyflow:` namespace for additional element types and attributes [@bpmn_spec]. This keeps diagrams compatible with BPMN editors/parsers at the base level while enabling domain-specific semantics (e.g., randomization gateways, study activities, and data annotations).

**Schema-first specification.** Studyflow’s language surface is specified as a machine-checkable schema (see `assets/schemas/studyflow.yaml`) that defines allowable element types, required attributes, and validation rules. Keeping the core specification text-based supports version control, review diffs, and long-term provenance tracking, and enables automated checks (e.g., diagram completeness constraints, branch labeling, and data input/output consistency).

**Separation of language and tooling.** The Studyflow specification is independent of any particular UI implementation. The accompanying **Studyflow Modeler** is a reference editor that operationalizes the schema through interactive validation and export. The modeler is implemented as a web application using TypeScript/React and `bpmn-js` for BPMN rendering/editing, extended with Studyflow-specific palettes, properties, and validators [@bpmnjs]. This separation allows other tooling (e.g., CLI validators, converters, or execution adapters) to be implemented against the same spec. The modeler is available at https://behaverse.github.io/studyflow-modeler/.

The specifications, example diagrams, and tools are open source at https://github.com/behaverse/studyflow-modeler under the MIT license. A versioned release will be archived at <DOI>. 

Studyflow is formally specified to support unambiguous interpretation, validation, and interoperability, but the full grammar and schema are maintained in the project documentation. The complete schema and serialization rules are provided in the repository under `assets/` (and accompanying specification documentation), together with example diagrams and the modeler implementation.


## Functionality

It extends BPMN with a profile that includes:

- **Core BPMN elements**: events, activities, gateways, and data-related artifacts.
- **Domain-specific elements** for experiments in cognitive sciences (e.g., tests, video games, questionnaires, instructions, data elements and operators).
- **Study-aware gateways** to encode participant assignment and branching (e.g., random assignment, inclusion/exclusion criteria).
- **Data-aware annotations** declaring which steps consume or produce datasets for traceability across the lifecycle.
- **A schema-driven interchange format** using BPMN XML augmented with `studyflow:` extensions, enabling validation, version control, and integration with BPMN tooling. Studyflow diagrams are serialized as BPMN 2.0 XML augmented with Studyflow-specific elements in a dedicated namespace, preserving compatibility with standard BPMN parsers while adding study semantics.

The language specification is provided as a LinkML schema (see `assets/studyflow.linkml.yaml`), and example diagrams are included in the repository.

# Example

Common established research patterns can be naturally represented using Studyflow diagrams. For example, a CONSORT-style randomized controlled trial flow can be expressed with explicit randomization and exclusion pathways while preserving BPMN readability (Figure 1). Similarly, cognitive task designs can capture trial structure, instructions, branching logic, and data outputs as explicit workflow steps, supporting clearer protocol communication and replication.


![Example Studyflow diagram showing randomization, exclusion pathways, and data annotations.](figures/figure1_consort_studyflow.png)

Another example is cognitive task design, where trial structures, instructions, and data outputs are captured as explicit workflow steps, making experimental procedures easier to understand and replicate.

# AI usage disclosure

Generative AI tools were used to assist with language refinement of portions of this paper. All AI-assisted text was reviewed, edited, and validated by the authors. No AI tool was used as an author, and the authors take full responsibility for the content and any errors.

# Acknowledgements
We thank collaborators and early users for feedback on the Studyflow specification and editor.

# References
