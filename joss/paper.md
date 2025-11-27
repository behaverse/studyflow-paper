---
title: 'Studyflow: Formal Diagrams to Define and Execute Scientific Workflows'
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
Scientific experiments include so much implicit knowledge in their design that they require rigorous and detailed communication for other scientists to trust and reproduce the findings. However, methodologies in manuscripts are often described informally or insufficiently, making them difficult to communicate, reproduce, or automate.

We introduce a formal diagramming language called Studyflow to address the need for clarity. Based on Business Process Model and Notation (BPMN), studyflow specifies scientific experiments end-to-end. Studyflow diagrams represent research workflows as machine-readable, self-contained visual diagrams that capture all stages of the research: experimental design, data collection, preprocessing, analysis, publication, and deployment. These diagrams can be version-controlled or executed; promoting provenance tracking, reproducibility, and transparent research practices.

Specifically, Studyflow Modeler is a proof-of-concept editor where researchers draw studyflow diagrams of their studies using simple building blocks for events, tasks, decision gateways, and data. These diagrams are both human-readable figures and machine-readable specifications that can be saved with a project, executed for data collection or analysis, shared with collaborators, and linked to the underlying data and code. In practice, a researcher can sketch and simulate the full lifecycle of a study from recruitment and consent, through task presentation and data preprocessing, to analysis and reporting. It further lowers the barrier for formalized, executable research workflows that improve trust and reproducibility.

Studyflow specifications and tools are available as open-source software at https//github.com/behaverse/studyflow-modeler under the MIT license. A versioned release will be archived at <DOI>.

# Statement of need

Despite the importance of reproducibility in experimental sciences and related fields, most methods sections are either informal (textual descriptions) or embedded in custom softwares, making replication and communication difficult. Existing solutions often focus on standardized data, partly neglecting the diversity of processes that generate the data (especially if the processes are not computational, e.g., subject recruitment or random assignment procedures). A formal, visual, and machine-readable language for describing a wide range of scientific workflows (hence a process model), may bridge the gap between human and machine interpretation, and support collaboration among diverse stakeholders.

# Area of need
- reproducible research
- manuscripts and publications
- clarity and machine-readability

# Related Software

The Studyflow builds upon and extends several existing approaches for workflow and process modeling in scientific and cognitive research. BPMN (Business Process Model and Notation) provides a widely adopted standard for business process modeling, which Studyflow extends for scientific workflows. Tools such as POWL, ProMoAI (Khourani2024), and BPMN-ChatBot (Kopke2024) offer various interfaces and enhancements for process modeling and automation.

In the broader landscape, general workflow management tools like Make, Snakemake, Taskfile, and CI pipelines facilitate automation but are sometimes arbitrary and lack domain-specific constructs for experimental sciences. Domain-specific workflow engines such as Pydra and Pydpiper address scientific data processing, and BIDS tools (e.g., Nipype, BIDS Manager-Pipeline) focus on neuroimaging and electrophysiology data analysis. However, these solutions often emphasize data rather than the explicit modeling of the processes. Studyflow complements these tools by providing a formal, visual, and machine-readable language for specifying, sharing, and executing end-to-end scientific workflows.

# Related Research

Workflow modeling has a long history in both business process management and scientific computing. The Business Process Model and Notation (BPMN) standard [REF] has become a widely adopted approach for representing complex processes in healthcare, finance, and other business domains in a formal, visual, and machine-readable way. In scientific domains, workflow systems such as Apache Taverna [REF], Kepler [REF], and Galaxy [REF] have enabled researchers to design, execute, and share computational pipelines, promoting reproducibility and collaboration.

Recent research has highlighted the importance of formal workflow representations for ensuring transparency and repeatability in scientific studies [REF]. Scientific pipeline management systems like Nextflow [REF], taskfile [REF], Snakemake [REF], vetiver, and Airflow [REF] provide automation and scalability for data analysis pipelines, but often focus on computational tasks rather than the full experimental process, including design, data collection, and deployment.

Efforts to bridge the gap between human-readable process descriptions and machine-readable executable workflows have led to the development of domain-specific languages and tools that integrate process logic with metadata, provenance, and tools. Studyflow builds on these advances by adapting BPMN for scientific research, enabling the explicit modeling of experimental protocols, data flows, and analysis steps in a unified framework.

# Mathematical Formulation

A workflow is a (N, E, T, $\tau$, $\lambda$) tuple, where N is a finite set of elements (activities, gateways, events), $E\subseteq N\times N$ represents sequence flows (edges), T is a set of pre-defined node types (Activity, Event, Gateway), $\tau: N \rightarrow T$ is a typing function that assigns types (Activity, Event, Gateway) to the nodes, and $\lambda$ is a labeling function that assigns additional attributes to the nodes (e.g., event triggers, gateway logic, implementations). The elements are connected by directed edges, forming a graph that represents the flow of the study. The graph has two critical execution points marked by a bpmn2:StartEvent and bpmn2:EndEvent.

Studyflow extends this formulation by introducing additional type hierarchies and attributes for a more detailed representation tailored to the specific needs of scientific research workflows. For a modular design, those additional metadata and constraints are encoded using BPMN extension mechanisms. The formal grammar of Studyflow is specified as EBNF in the next section.

# Grammar

Studyflow extends the BPMN 2.1 specification (including the addition of choreography tasks) to fit the needs of our specific use case (experimental sciences). Studyflow diagrams can be described by a domain-specific language to model processes along with data produced or needed by those processes. The following EBNF grammar describes the formal structure of a Studyflow diagram:

```
Definitions       ::= Study*
Study             ::= 'Study' Identifier Attribute* (Element | SequenceFlow)*
Element           ::= Event | Activity | Gateway

Event             ::= StartEvent | EndEvent
StartEvent        ::= 'StartEvent' Identifier Attribute*
EndEvent          ::= 'EndEvent' Identifier Attribute*

Activity          ::= 'Activity' Identifier ActivityAttributeList Choreography?
ActivityAttributeList ::= ActivityType ActivityAttribute*
ActivityType      ::= '@type' ('CognitiveTest' | 'Questionnaire' | 'Instruction' | 'Rest' | 'VideoGame' | 'Script' | 'Manual')
ActivityAttribute ::= Attribute | DataOperation

Choreography     ::= 'Choreography' Attribute* ParticipantRef+ InitiatingParticipant? MessageFlowList
ParticipantRef   ::= ProcessRef
InitiatingParticipant ::= ParticipantRef
MessageFlowList  ::= MessageFlow*
MessageFlow      ::= 'MessageFlow' Identifier Attribute* ParticipantRef '→' ParticipantRef

/* Gateway definitions */
Gateway          ::= 'Gateway' Identifier GatewayAttribute*
GatewayAttribute ::= GatewayType | Attribute
GatewayType      ::= '@type' ('Random' | 'Exclusive' | 'Complex')
SequenceFlow     ::= 'SequenceFlow' Identifier Attribute* NodeRef '→' NodeRef

/* Common definitions */
Attribute  ::= Identifier Value
ProcessRef ::= Identifier
NodeRef    ::= Identifier

/* Basic value types */
Boolean    ::= 'true' | 'false'
Value      ::= String | Number | Boolean | Identifier
Number     ::= '-'? ( [0-9]+ ('.' [0-9]*)? | '.' [0-9]+ )
String     ::= '"' [^"]* '"'
Identifier ::= [A-Za-z] [A-Za-z0-9_]*

/* data transformations */
DataOperation ::= DataOpClause+
DataOpClause  ::= DataOperator DataInput+ DataOutput+
DataOperator  ::= '@op' ('Transform' | 'TransformTables'
                        | 'Map' | 'Filter' | 'FlatMap'
                        | 'Reduce' | 'Group')
DataInput     ::= '@in' NodeRef
DataOutput    ::= '@out' NodeRef
```

# Example Use Cases

Example use cases include a CONSORT, data preprocessing, and experimental design (see Figure 3).

Further examples and documentations are available at https://behaverse.github.io/studyflow

# Acknowledgements
We acknowledge contributions from X, Y, and Z.

# References

