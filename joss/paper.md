---
title: 'Studyflow: BPMN-based diagrams for scientific workflows'
tags:
  - scientific workflows
  - BPMN
  - reproducibility
  - workflow modeling
authors:
  - name: Morteza Ansarinia
    orcid: https://orcid.org/0000-0001-8335-6704
    affiliation: 1
  - name: Pedro Cardoso-Leite
    affiliation: 1
affiliations:
 - name: University of Luxembourg, Luxembourg
   index: 1
date: 30 January 2026
bibliography: references.bib
---

# Summary

Scientific workflows are often communicated through free-text descriptions in manuscripts, informal box-and-arrow figures, or code artifacts that are difficult to reconcile across stakeholders and to reproduce in later studies. We present **Studyflow**, a BPMN extension that provides formal, machine-readable diagrams for end-to-end scientific workflows spanning experimental design, data collection, analysis, and reporting. Studyflow adds domain-specific elements (e.g., experimental tasks, questionnaires, and group assignment logic) while remaining compatible with familiar BPMN notation. complement standard data models with process models in a human-friendly, machine-readable, and executable way.

# Statement of need

Reproducibility in science requires more than sharing data and manuscripts; it also requires an explicit description of the process that generated those artifacts. Process models complement data models by documenting the sequence of activities, decision points, and transformations that underlie a scientific study [@sehgal2011].

Existing workflow approaches tend to split across two needs: execution-focused tooling (e.g., orchestration frameworks and pipeline languages) that encodes study logic implicitly in code, and domain-generic process modeling (e.g., BPMN) that is readable and standardized but lacks scientific-study concepts such as participant assignment, inclusion/exclusion logic, and explicit links between workflow steps and research datasets. Domain-specific workflow engines improve executable reproducibility in particular communities, yet they often require programming expertise and do not provide a shared modeling layer interpretable by non-technical stakeholders (e.g., ethics boards, clinicians, and collaborators). Studyflow addresses this gap by extending BPMN with study-specific constructs—experimental task types, randomization and branching gateways, and data-aware annotations aligned with community standards (e.g., BIDS/BDM/Psych-DS)—so a single diagram can serve as both a human-readable protocol and a machine-readable specification for validation, versioning, and downstream tooling across the study lifecycle.

<!-- Existing workflow engines and data standards provide important building blocks, but they often emphasize one aspect of research (data, execution, or reporting) rather than a shared, human-readable protocol that can be communicated across scientists, engineers, ethics boards, and other stakeholders with diverse expertise and responsibilities. -->

<!-- Just like ERD or UML for data or code, one widely used solution for process modeling is BPMN. BPMN (Business Process Model and Notation) is a general-purpose process modeling in industry and business domains. BPMN provides a well adopted process modeling standard [@white2004introduction], yet it lacks constructs tailored to the needs of experimental sciences. Studyflow extends BPMN and targets researchers who need a formal, shareable way to describe study protocols while keeping them compatible with established notations. -->

# Functionality

Studyflow extends BPMN with a profile that includes:

- **Core BPMN elements**: events, activities, gateways, and data-related artifacts.
- **Domain-specific activities** for common scientific actions (e.g., experimental tasks, questionnaires, instructions, data collection phases).
- **Study-aware gateways** to encode participant assignment and experimental branching (e.g., random assignment, inclusion/exclusion criteria).
- **Data-aware annotations** to declare which steps consume or produce datasets, enabling traceability across the study lifecycle.
- **A schema-driven interchange format** using Studyflow extensions within BPMN XML (via a `studyflow:` namespace), enabling validation, version control, and integration with BPMN tooling.


# Example
Common established research patterns can be naturally represented using Studyflow diagrams. For example, a CONSORT-style randomized controlled trial flow can be expressed with explicit randomization and exclusion pathways while preserving BPMN readability (Figure 1). Similarly, cognitive task designs can capture trial structure, instructions, branching logic, and data outputs as explicit workflow steps, supporting clearer protocol communication and replication.

- [ ] CONSORT FIGURE

Another example is cognitive task design, where trial structures, instructions, and data outputs are captured as explicit workflow steps, making experimental procedures easier to understand and replicate.

# Implementation details
Studyflow diagrams are serialized as BPMN 2.0 XML augmented with Studyflow-specific elements in a dedicated namespace, preserving compatibility with standard BPMN parsers while adding study semantics. The language specification is provided as a schema (see `assets/schemas/studyflow.yaml`), and representative diagrams are included in the repository to support validation and regression testing.

- [ ] UML
- [ ] GRAMMAR + MATHEMATICAL FORMALIZATION

## Modeler

As a proof-of-concept, we also developed *Studyflow Modeler*, a schema-based visual editor for creating, simulating, and deployment of studyflows. The specifications, example diagrams, and tools are open source at https://github.com/behaverse/studyflow-modeler under the MIT license. A versioned release will be archived at <DOI>.

Studyflow Modeler is a web-based editor for authoring Studyflow diagrams and exporting them for documentation and downstream use (e.g., simulation or integration with data collection and analysis tooling). The modeler is available at https://behaverse.github.io/studyflow-modeler/ and is implemented using TypeScript/React and `bpmn-js`, with Studyflow-specific UI components and validation rules.

## Grammar and formalization

Studyflow is formally specified to support unambiguous interpretation, validation, and interoperability, but the full grammar and schema are maintained in the project documentation. The complete schema and serialization rules are provided in the repository under `assets/` (and accompanying specification documentation), together with example diagrams and the modeler implementation.

# Acknowledgements
We thank collaborators and early users for feedback on the Studyflow specification and editor.

# References
