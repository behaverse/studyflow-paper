---
title: 'Studyflow Modeler: Formal Diagrams and Tools to Define and Execute Cognitive Science Workflows'
tags:
  - BPMN
  - cognitive science
  - workflow
  - scientific computing
authors:
  - name: Morteza Ansarinia
    orcid: https://orcid.org/0000-0001-8335-6704
    affiliation: 1
  - name: Pedro Cardoso-Leite
    affiliation: 1
affiliations:
 - name: University of Luxembourg, Luxembourg
   index: 1
date: 15 May 2025
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
# aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
# aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary

Clarity and reproducibility of experimental workflows in scientific manuscripts are often compromised by informal description or custom codes. Studyflow addresses this by providing a formal diagramming language based on BPMN (Business Process Model and Notation) for specifying end-to-end scientific workflows. Studyflow encodes workflows as self-contained, machine-readable diagrams, including experimental design, data collection, preprocessing, analysis, and deployment. These diagrams can be version-controlled and used for automated execution, enabling reproducibility and validation. Studyflow promotes transparent, reusable research processes, and the additional Studyflow Modeler tool supports editing, simulation, and visualization of workflows.

# Statement of need

Despite the importance of reproducibility in experimental science and related fields, most descriptions of methodologies are either informal (textual descriptions) or embedded in custom code, making replication and communication difficult. Existing solutions often focus on data and analysis models, neglecting the process model that generate them. Studyflow provides a formal, visual, and machine-readable language for describing scientific workflows, bridging the gap between human and machine interpretation, and supporting collaboration among diverse stakeholders.

# Area of need

# Related Software

The Studyflow Modeler builds upon and extends several existing approaches for workflow and process modeling in scientific and cognitive research. BPMN (Business Process Model and Notation) provides a widely adopted standard for business process modeling, which Studyflow adapts for scientific workflows. Tools such as POWL, ProMoAI (Khourani2024), and BPMN-ChatBot (Kopke2024) offer various interfaces and enhancements for process modeling and automation.

In the broader landscape, general workflow management tools like Make, Taskfile, and CI pipelines facilitate automation but lack domain-specific constructs for experimental science. Domain-specific workflow engines such as Pydra and Pydpiper address scientific data processing, while BIDS tools (e.g., Nipype, BIDS Manager-Pipeline) focus on neuroimaging and electrophysiology data analysis. However, these solutions often emphasize data and analysis pipelines rather than the explicit modeling of experimental processes. Studyflow complements these tools by providing a formal, visual, and machine-readable language for specifying, sharing, and executing end-to-end scientific workflows.

# Related Research

Workflow modeling has a long history in both business process management and scientific computing. The Business Process Model and Notation (BPMN) standard [REF] has become a widely adopted approach for representing complex processes in healthcare, finance, and other business domains as a formal, visual, and machine-readable manner. In scientific domains, workflow systems such as Apache Taverna [REF], Kepler [REF], and Galaxy [REF] have enabled researchers to design, execute, and share computational pipelines, promoting reproducibility and collaboration.

Recent research has highlighted the importance of formal workflow representations for ensuring transparency and repeatability in scientific studies [REF]. Scientific pipeline management systems like Nextflow [REF], Snakemake [REF], vetiver, and Airflow [REF] provide automation and scalability for data analysis pipelines, but often focus on computational tasks rather than the full experimental process, including design, data collection, and deployment.

Efforts to bridge the gap between human-readable process models and executable workflows have led to the development of domain-specific languages and tools that integrate process logic with metadata and provenance. Studyflow builds on these advances by adapting BPMN for scientific research, enabling the explicit modeling of experimental protocols, data flows, and analysis steps in a unified framework.

# Mathematical Formulation

A workflow is a (N, E, T, $\tau$, $\lambda$) tuple, where N is a finite set of elements (activities, gateways, events), $E\subseteq N\times N$ represents sequence flows (edges), T is a set of pre-defined node types (Activity, Event, Gateway), $\tau: N \rightarrow T$ is a typing function that assigned types (Activity, Event, Gateway) to the nodes, and $\lambda$ is a labeling function that assigns additional attributes to the nodes (e.g., event triggers, gateway logic, implementations). The elements are connected by directed edges, forming a directed acyclic graph (DAG) that represents the flow of the study.

Studyflow extends this formulation by introducing additional type hierarchies and attributes to the elements, allowing for a more detailed representation of the workflow, tailored to the specific needs of scientific research. Metadata and constraints are encoded using BPMN extension mechanisms, supporting modular workflow design. The formal grammar of Studyflow is specified as EBNF in Figure 2.

Example use cases include a CONSORT, data preprocessing, and experimental design (see Figure 3).

# Grammar

Studyflow extends the BPMN 2.1 specification (including the addition of choreography tasks) and has been adapted to fit the needs of our specific use case. Studyflow diagrams can be described as a domain-specific language to model processes along with data produced or needed by those processes. The following EBNF grammar describes the formal structure of a Studyflow diagram:

```ebnf
Definitions      = { Process }-;

Process         = "process", Identifier, { Node | SequenceFlow }-;

Node    = (StartEvent | Task | Gateway | EndEvent);

StartEvent      = "startEvent", Identifier;
EndEvent        = "endEvent", Identifier;

Task            = 'task', Identifier, TaskType, [Choreography];

TaskType        = "cognitive-test" | "questionnaire" | "instruction" | "rest" | "script" | "manual";
Choreography = "choreography", ParticipantList, [InitiatingParticipant];

Gateway         = 'gateway', Identifier, GatewayType;
GatewayType     = 'random-assignment' | 'exclusive' | 'complex';

SequenceFlow = "sequenceFlow", Identifier, NodeRef, ?→?, NodeRef;

MessageFlowList  = { "messageFlow", Identifier, ParticipantRef, ?→?, ParticipantRef };

ProcessRef = Identifier;
NodeRef = Identifier;
ParticipantRef = ProcessRef;
InitiatingParticipant = ParticipantRef;

Identifier = ? [a-zA-Z_][a-zA-Z0-9_]* ?;
```

# Acknowledgements

We acknowledge contributions from X, Y, and Z.

# References
