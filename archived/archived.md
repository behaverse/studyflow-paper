# **\# Introduction**

## **\#\# Context**

Trusting science at large requires rigor and reproducibility, hence clear communication of the experiments has become one of the cornerstones of good scientific practices. Following this, many scientific projects rely on detailed description of data and protocols in manuscripts, visual diagrams, reporting guidelines, checklists, and more-or-less standard softwares; all to provide enough details to reproduce the findings.

In parallel, as we increasingly rely on machines to facilitate research, trust in code and data are becoming more and more critical. The need for reproducibility of science has become essential for building trust in automated processes, especially at scale using various large models.

The context of this paper is how scientific workflows and everything related to that (study protocols, experimental designs, data, analysis, etc) can be communicated for rigor and reproducibility in modern days. We specifically propose Studyflow, a formal language to represent research processes and data for the various stakeholders involved in a scientific project in a single cohesive visual diagram.

## **\#\# Problem statement**

As with everything else, trust and understanding requires a complete description of systems. And a complete description of a computing system requires both 1\) a data model and 2\) a process model \[@sehgal2011\]. The data model describes the structure and semantics of the data, while the process model describes the workflow of generating and making sense of the data. Cognitive science is no exception to this requirement. Yet, most efforts are focused on standardized data (which is good in isolation), while formalizing the processes that generate the data are often neglected. Consequently, the common practice for process models rely on reusing common software and codes (see for example, REF, REF, REF), and more recently language models that encapsulate the implicit knowledge of experimental designs (REF).  
 The lack of rigor process models is particularly problematic in cognitive science, probably because the complexity of the experiments and the multidisciplinary diversity of the stakeholders make it difficult to communicate and effectively share the experiments and findings with everyone.

## **\#\# Current approach and its limitations**

Current strategies to define and communicate experimental workflows are either informal as plain textual descriptions in manuscripts accompanied by codes and figures in arbitrary formats. Some of the strategies researchers use to compensate for the lack of clarity in natural language or diversity of codes are as follows:

- \*\*Box and arrow figures\*\* explain the workflow and the data in a more abstract way. These are limited because of the medium, or task-specific formats. There are efforts like UML in software engineering, or CONSORT in experimental sciences, but they are limited and inefficient to capture the complexity of modern data and softwares (e.g., MLOps). Given the fact that several stakeholders in scientific research each requires different kinds of communication, those diagramming are required to be separately tailored for each stakeholder; making it impossible to share via common scientific communication outlets such as manuscripts. At the end they are just arbitrary description of what actually happened during the scientific experiment, neither the texts nor the visual diagrams are executable for engineers to re-use.  
  \- \*\*Checklists\*\*, and pre-defined forms (e.g., pre-registration) address the need for structured text descriptions but they do not directly address the need for exploration required by rigorous science (e.g., by keeping track of changes or promoting version control). Keeping history is difficult because of the inherent unstructured-ness of natural language descriptions, and the way they are stored: formatted texts in proprietary PDF, DOCX, and on data silos that will never change.  
  \- \*\*Schemas, standards, ontologies, and custom packages\*\* make decisions and designs machine-readable, but they do not capture the two different aspects of modern science: domain-specific (as in asking the right question) and technical (as in using the right software architecture). They are either tailored for domain experts (e.g., NiBabel), or technical experts (e.g., UML). The technical solutions are also often specific to particular use cases, e.g., MLOps or GitHub actions, and do not address the need for several levels of expertise that a scientific project requires, from funding agencies and public audiences, to software engineers and non-expert assistants who develop the tools, collect the data, and manage the process. Recent efforts in cognitive science have mainly focused on data models, such as BIDS \[@gorgolewski2016bids\] and Psych-DS \[@REF\], which provide a structured way to describe the data collected during experiments. However, data models do not address the need for an end-to-end description of the workflows that generate, analyze, and report the data. Recent paradigm shifts in how data is managed (@REF) and how software is implemented (e.g., @REF) requires more flexible and adaptable workflows that can handle multi-modal data and changing environments.   
  \- \*\*Codes\*\* (source code, scripts, MLOps packages, CI jobs, etc) make pipeline definitions clear, but requires a lot of effort to be readable and shareable which is a luxury for scientists whose main task is to address research questions. They also often include terminologies and require environments which are not tailored for other non-expert stakeholders with whom they like to communicate with. Sharing those codes is also a limiting factor, as it requires intellectual property management or open sourcing the project which is not always feasible for human-involved scientific projects.  
  


However, these formats are not always easy to share or execute, specifically given the multitude of expertise required for experimental sciences (as in scientists, data collectors, analysts, funding agencies, etc). The situation is even worse when the methods are described in a language that is not the native language of the reader or a programming language that is proprietary or outdated. Interpreting those texts and supporting diagrams also require specialized knowledge that is not always available to all the stakeholders, making them inaccessible to non-experts and hindering the reproducibility of the experiments. We can however leverage practices in safety-critical disciplines that require trust (e.g., finance or healthcare) and apply them to experimental cognitive sciences.

## **\#\# Our contributions**

To address this, our contribution is two-fold:

- A formal language to describe processes in scientific studies that can be interpreted and executed by both humans (at different levels of expertise) and machines (for different purposes).  
- A proof-of-concept interface to model and run the experiments without the need for specialized knowledge.


To this end we propose Studyflow, a formal language to describe cognitive experiments, and Studyflow Modeler, a tool to design and test cognitive experiments using the Studyflow language.

Studyflow is based on BPMN \[Business Process Model and Notation; @white2004introduction\], a standard for process modeling that is widely used in the industry. Just like its counterparts to model data, BPMN is a graphical language to formally describe workflows, making them easy to understand (by human) and execute (by machine). Studyflow extends BPMN with additional elements to describe scientific experiments, such as elements for data collection, data transformation, modeling, checklists, and other patterns common in an experimental study.

Additionally, Studyflow Modeler is a web-based tool that demonstrates how to design, test, and run cognitive experiments using the Studyflow language. It provides a graphical interface to create and edit Studyflow diagrams, as well as a simulator to run the workflow before deployment. The tool is designed to be easy to use, even for domain experts with no specialized technical experience.

## **\#\# Benefits**

In section X, several use cases of applying studyflow for common patterns in research will be presented to demonstrate the benefits of using studyflows in practice. But generally, using studyflow for scientific research workflows will benefit experimental research because:

Data models are not sufficient to reproduce the experiments. Full reproducibility requires an explicit process model to accompany the data model. Studyflow provides domain-specific elements for 1\) activities including cognitive tests, questionnaires, instructions, and 2\) data including specialized datasets that align with best practices like BDM (Behaverse Data Model), BIDS, Psych-DS, and Kedro to name a few.

- Help all stakeholders understand complex research protocols using easily readable diagrams.  
- Provide a natural basis for collaboration between researchers, ethics committees, data scientists, software engineers, and other stakeholders through a coherent visual representation.  
- Reduce the effort and risk of experimental design through graphical decomposition of research workflows into well-defined activities, events, and gateways, and simulation of the workflow before deployment.  
- Allow study protocols to be defined simply and unambiguously using a formal machine-readable format that supports version control.  
- Simplify reproducibility of studies using specifications that can be automatically validated, shared, and executed.  
- Support the FAIR principles by making processes such as experimental protocols findable, accessible, interoperable, and reusable.  
- Enable the development of a library of reusable research components across cognitive tests, questionnaires, instructions, and data processing pipelines.  
    



## **\# Related Works**

Numerous approaches to model scientific workflows exist, each with its own strengths and weaknesses. The workflow ecosystem can be understood along two dimensions: 1\) definition vs. execution, and 2\) domain-specificity (generic vs. specific; see Figure YXY).  
Within the domain-generic definition space, there are formal models that aim to make complex processes understandable for machines and humans. Prominent among them is BPMN (Business Process Model and Notation), a widely adopted standard for process modeling that offers both graphical representation and executable semantics in XML format. BPMN has been noted in particular for its readability (enabling communication across technical and non-technical stakeholders), but it lacks built-in support for specific domains like scientific experiments. To address this limitation, BPMN provides an extension mechanism which can be used to adapt the underlying meta-model for specific domains.

With the advent of large language models, BPMN, known for its clarity and its ability to connect design with execution of processes, has recently been adapted for automated development. For example, ProMoAI \[@khourani2024\] and BPMN-ChatBot \[@kopke2024\] use large language models to create BPMN models from text. These tools allow for automated BPMN modeling but don't inherently understand domain-specific semantics.

UML Activity Diagrams and Petri nets also reside in the general-purpose space, focusing on formal definitions of workflows rather than domain relevance or executability. Their application however can be cumbersome and an impediment for complex workflows for scientific experiments with specific terminologies and methods.

On the opposite end, execution-focused generic tools like LONI, Apache Airflow, Kedro \[REF\], and CI pipelines (e.g., Taskfile, Make, CI, Jenkins, GitHub Actions) provide powerful orchestration engines to run workflows, yet they lack rigorous formal specifications, broad applicability, and require specific knowledge and custom codes to develop end-to-end pipelines for experiments.

The other end is domain-specific tools. Systems biology relies on SBGN (Systems Biology Graphical Notation) as a visual guide. The protocols.io is a platform for developing and sharing reproducible protocols, which describe the background, rationale, objectives, design, methodology, statistical considerations, and organization of a clinical research project. Within the cognitive sciences, neuroscience has a rich toolkit for domain-specific workflows. Tools such as Nipype (flexible Python-based engine for neuroimaging analyses), NeuroManager (automates neuroscience simulation workflows across diverse compute resources), Pydra (an emerging lightweight dataflow successor to NiPype), Cromwell/WDL (scalable, reproducible pipelines), and CWL (Common Workflow Language, an open standard for portable, command-line-driven pipelines) fill the gap for executable domain-specific scientific workflows. Other key tools include the LONI Pipeline, NeuroHub, Pydpiper, neuropype, Porcupine, labvanced, and BIDS-based tools like the BIDS Manager-Pipeline. These tools are useful for execution and reproducibility, but they often demand programming skills or significant upfront effort to adapt to specific needs, and often lack a visual or formal modeling layer interpretable by non-technical stakeholders.

**TODO**: limitations of DAG for scientific discovery (@ghareeb2025).  
Beyond usability and accessibility challenges, a more fundamental limitation shared by many execution oriented workflow tools such as Nextflow, CWL, Apache Airflow, and CI pipelines lies in their reliance on directed acyclic graphs (DAGs) as the underlying computational model. DAGs are effective for representing data processing pipelines with well defined inputs and outputs, and they are widely used to enable scalable and reproducible execution. However, scientific inquiry itself is inherently iterative and non linear. For example, recent systems for AI driven scientific discovery implement iterative cycles of hypothesis generation, experimentation, and analysis within a continuous feedback loop \[@ghareeb2025\]. Such processes involve repeated refinement steps, including parameter tuning, conditional branching based on intermediate results, and revisiting earlier stages of analysis. In contrast, DAG based representations do not natively support cycles, which limits their ability to directly represent these iterative patterns. In practice, such behaviors are often implemented through external control logic, repeated workflow executions, or manual intervention, which can obscure the high level structure of the process and reduce transparency. This reveals a mismatch between execution oriented workflow abstractions and the need to represent scientific reasoning in a more expressive and interpretable way.

Studyflow occupies a unique space: grounded in BPMN, it extends the language with constructs for the communication and execution of scientific experiments: data collection, transformation, and experimental tasks. Moreover, studyflows align with community standards like BIDS, BDM, and Psych-DS. This allows studyflow to operate across both axes: it enables interpretable, formal workflow definitions tailored for scientific communication that can be executed directly, without requiring implicit knowledge.

\#\# Notes

- Other general formalisms include UML for data modeling and UML Activity Diagrams for basic processes.  
- While BPMN is extendible, and has been adapted in works like XXXX \[@REF\], its generic semantics requires extension for specialized domains like experimental cognitive science.  
- Simpler tools like make and taskfile, alongside CI pipelines, also represent general workflow automation but often lack the rich modeling capabilities required for complex scientific experiments.  
- In scientific domains, several specialized workflow tools have been developed. For instance, Nextflow, Common Workflow Language (CWL), and Apache Airflow facilitate the execution of command-line tools and complex data-processing directed acyclic graphs (DAGs). Biology benefits from SBGN (Systems Biology Graphical Notation). Neuroscience, in particular, has seen tools like NiPype, Pydra, NeuroHub, NeuroManager, Cromwell, Pydpiper, neuropype, Porcupine, labvanced, the LONI Pipeline, and BIDS tools like BIDS Manager-Pipeline, each addressing specific aspects of neuroimaging or electrophysiology data analysis. More recent efforts like ProMoAI \[@khourani2024\] and POWL also target specific research workflow needs. While these tools provide significant value in their respective domains, a gap remains for a comprehensive, formally defined language that integrates the entire scientific study lifecycle from experimental design and data collection (including cognitive tests and questionnaires) to data formatting and analysis while being accessible to different stakeholders with or without specialized knowledge.  
    
- BPMN is a standard language to define business processes, widely used in healthcare, finance, and logistics to model workflows. BPMN provides 1\) a graphical representation of workflows, allowing various stakeholders to understand and communicate complex processes, and 2\) a formal XML-based semantics that enables the execution of BPMN models in various environments.  
    
- However, despite its versatile nature, BPMN is designed for general use cases and does not specifically capture domain-specific semantics like those needed for cognitive science or machine learning. It is extendible though: its elements can be extended to model specific concepts in data-driven scientific experiments, such as experimental design, data collection, data cleaning and transformation, training models, versioning and deployment, and so on. 

- Petri nets are a mathematical modeling language used to represent processes as bipartite graphs of places (states) and transitions (events).  
    
- Domain specific: Nextflow, SBGN (Systems Biology Graphical Notation), Common Workflow Language (CWL) is an open standard for describing how to run command line tools and connect them to create workflows.  
- Apache Airflow helps with scheduling and monitoring complex DAGs, often in large data-processing contexts.  
- POWL  
- Pydra  
- NeuroHub  
- NeuroManager  
- Cromwell [https://cromwell.readthedocs.io/en/stable/](https://cromwell.readthedocs.io/en/stable/)  
- Pydpiper  
- neuropype  
- Porcupine  
- labvanced  
- NiPype is a Python-based engine that wraps popular neuroimaging softwares to build and execute pipelines as directed graphs of processing "nodes".  
- With LONI Pipeline, researchers can create workflow protocols to run multiple computational tools, monitor their progress and quickly interpret results.  
- GitHub CI. Its workflow engine enforces unique node names, cycle-free graphs, and supports hierarchical workflows for modular reuse   
- BIDS tools  
- Nipype  
- BIDS Manager-Pipeline: A framework for multi-subject analysis in electrophysiology \[link\](https://www.sciencedirect.com/science/article/pii/S2772528622000346)  
    
  