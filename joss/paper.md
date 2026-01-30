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
Scientific workflows are often communicated through free-text descriptions in scientific manuscripts, informal box-and-arrow figures, and code artifacts that are difficult to reconcile across stakeholders and to reproduce in later studies. Studyflow is a BPMN extension that provides formal, machine-readable diagrams for end-to-end scientific workflows, covering study design, data collection, preprocessing, analysis, and reporting. The language adds domain-specific elements (e.g., study steps, experimental tasks, and randomization gateways) while retaining BPMN's familiar notation and XML-based interchange format [@white2004introduction]. Studyflow diagrams are human-friendly, machine-readable, and executable; they can support experiment design, protocol documentation, methodology communication, workflow automation, reproducibility, and reporting.

Additionally, *Studyflow Modeler* is a proof-of-concept web editor for creating and simulating studyflows, and the documentation also describes an experimental Runner for deployment and execution. The specifications, example diagrams, and tools are open source at https://github.com/behaverse/studyflow-modeler under the MIT license. A versioned release will be archived at <DOI>.

# Statement of need
Reproducibility requires more than sharing data and analysis code: it also requires an explicit description of the processes that generated those artifacts. Process models complement data models by documenting the sequence of activities, decision points, and data transformations that underlie a study [@sehgal2011]. Existing workflow engines and data standards provide important building blocks, but they often emphasize execution or data structure rather than a shared, human-readable protocol that can be communicated across scientists, engineers, ethics boards, and other stakeholders. BPMN provides a widely adopted and readable process modeling standard [@white2004introduction], yet it lacks constructs tailored to the needs of experimental science. Studyflow targets researchers and research teams who need a formal, shareable way to describe study protocols while keeping them compatible with established workflow notations.

# Functionality
Studyflow extends BPMN with a scientific workflow profile that includes:

- **Core flow elements** for scientific workflows: events, activities, decisions, and data.
- **Domain-specific activities** to represent common scientific actions (e.g., experimental tasks, questionnaires, instructions, and data collection phases).
- **Decision gateways** to encode participant assignment and experimental branching.
- **Data-aware workflow elements** that annotate which tasks consume or produce datasets, enabling traceability across the study lifecycle.
- **A structured schema and interchange format** that serialize the extended elements in BPMN XML using a Studyflow namespace, enabling version control and integration with existing BPMN tooling.

Studyflow Modeler provides a visual editor for creating and simulating Studyflow diagrams and exporting the resulting specification for use in documentation, collaboration, or downstream tooling.

# Example
Studyflow diagrams can be used to formalize common research patterns. For instance, randomized controlled trial reporting can be represented as a CONSORT-style flow with explicit randomization and exclusion pathways, while still remaining compact and readable. Another example is cognitive task design, where trial structures, instructions, and data outputs are captured as explicit workflow steps, making experimental procedures easier to review and replicate.

# Implementation details
Studyflow diagrams are serialized as BPMN 2.0 XML with Studyflow-specific extensions, preserving compatibility with standard BPMN parsers while adding scientific semantics. The language specification is provided as a schema (see `assets/schemas/studyflow.yaml`), and example diagrams are included in the repository. The Modeler is implemented as a web-based proof-of-concept to demonstrate diagram authoring and export in this format. These choices keep the artifacts text-based and diffable, which supports collaborative editing and long-term provenance tracking.

# Acknowledgements
We thank collaborators and early users for feedback on the Studyflow specification and editor.

# References
