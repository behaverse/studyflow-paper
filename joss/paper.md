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
bibliography: paper.bib
---

# Summary
Scientific workflows are often communicated through free-text descriptions in manuscripts, informal box-and-arrow figures, or code artifacts that are difficult to reconcile across stakeholders and to reproduce in later studies. We propose Studyflow language, a BPMN extension that provides formal, machine-readable diagrams for end-to-end scientific workflows. Studyflow diagrams can be used to describe different stages of scientific workdlows including experimental design, data collection, analysis, and reporting. The language adds domain-specific elements (e.g., activities, tests, group assignments) while retaining familiar notation of BPMN in XML format [@white2004introduction]. Studyflow diagrams complement standard data models with process models in a human-friendly, machine-readable, and executable way. It encapsulates what is needed for research in one unified diagram (including experiment design, protocol documentation, data formats, methodology communication, reproducibility, and reporting).

As a proof-of-concept, we also developed *Studyflow Modeler*, a web editor for creating, simulating, and deployment of studyflows. The specifications, example diagrams, and tools are open source at https://github.com/behaverse/studyflow-modeler under the MIT license. A versioned release will be archived at <DOI>.

# Statement of need

Reproducibility requires more than sharing data and analysis code: it also requires an explicit description of what generated those artifacts: a process model. Process models complement data models by documenting the sequence of activities, decision points, and data transformations that underlie a scientific experiment [@sehgal2011]. Existing workflow engines and data standards provide important building blocks, but they often emphasize one aspect of research (data, execution, or reporting) rather than a shared, human-readable protocol that can be communicated across scientists, engineers, ethics boards, and other stakeholders with diverse expertise and responsibilities.

Just like UML for data or code, one general solution for process modeling is BPMN. BPMN (Business Process Model and Notation) is a general-purpose process modeling language widely used in industry and business domains. BPMN provides a widely adopted and readable process modeling standard [@white2004introduction], yet it lacks constructs tailored to the needs of experimental science. Studyflow targets researchers and teams who need a formal, shareable way to describe study protocols while keeping them compatible with established notations.

# Functionality
Studyflow extends BPMN with a profile that includes:

- **Core flow elements** for scientific workflows: events, activities, decisions, and data.
- **Domain-specific activities** to represent common scientific actions (e.g., experimental tasks, questionnaires, instructions, and data collection phases).
- **Decision gateways** to encode participant assignment and experimental branching (e.g., random assignment, inclusion/exclusion criteria).
- **Data-aware workflow elements** to annotate which tasks consume or produce datasets, enabling traceability across the study lifecycle.
- **A structured schema and interchange format** that serialize the extended elements in BPMN XML using a Studyflow namespace, enabling version control and integration with existing BPMN tooling.

# Example
Common established research patterns can be naturally represented using Studyflow diagrams. For instance, CONSORT-style flow to represent randomized controlled trial reporting can be represented with explicit randomization and exclusion pathways, while still remaining compact and readable.

- [ ] CONSORT FIGURE

Another example is cognitive task design, where trial structures, instructions, and data outputs are captured as explicit workflow steps, making experimental procedures easier to understand and replicate.

# Implementation details
Studyflow diagrams are serialized as BPMN 2.0 XML with Studyflow-specific elements, preserving compatibility with standard BPMN parsers with additional semantics. The language specification is provided as a schema (see `assets/schemas/studyflow.yaml`), and example diagrams are included in the repository.
These choices keep the artifacts text-based and version controllable, and support collaborative editing and long-term provenance tracking.


## Modeler
Studyflow Modeler provides a visual editor for authoring and simulating Studyflow diagrams and exporting them for use in documentation, collaboration, or downstream tooling such as data collection. The modeler is accessible as a web application at https://behaverse.github.io/studyflow-modeler/ and is implemented using TypeScript and React. It leverages the bpmn-js library for rendering and editing BPMN diagrams, extended with Studyflow-specific components and validation logic.


# Acknowledgements
We thank collaborators and early users for feedback on the Studyflow specification and editor.

# References
