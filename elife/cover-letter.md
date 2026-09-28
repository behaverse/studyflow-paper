# Cover letter (draft)

[date]

Dear Editors,

We submit "Studyflow, an executable visual notation for experimental workflows in the cognitive sciences, from design to publication" as a Tools and Resources article.

A cognitive science study's data have shared standards such as BIDS; its process has no shared machine-readable form. The process is spread across a protocol, scripts, analysis code and figures; each keeps its own copy of the study's parameters, free to drift, and none fully records what was done.

Studyflow gives that process one machine-readable representation, a `.studyflow.yaml` file that is at once the protocol, the runnable study, the analysis specification and the publication figure, each a view for a different audience, so there is no second copy to drift. Formally, a study is a typed directed multigraph over a profile of the ISO-standard BPMN 2.0, with validity conditions and execution semantics defined on it. To our knowledge, no existing approach is at once a readable definition and an executable specification of a whole study.

Our example study runs end to end from one file on an artificial cohort of open-weight language models. Each analysis question ends in a claim state (Supported, Not supported or Not testable) decided by a rule fixed before any run, and the deviation report is the diff between the deposited file and its executed copy. A human cohort would take the same protocol through the same interface.

To calibrate the validator, we seeded twelve faults one at a time into a small study: ten were caught, eight by the validator and two when the affected step ran. The two missed faults are scientific rather than formal (a flipped inequality in a decision rule, and a difference test where the question asks for equivalence). Validation checks form, not science.

The schema and reference tools are open source under the MIT license, on GitHub (https://github.com/behaverse/studyflow-modeler, https://github.com/behaverse/schemas), with archived releases at [modeler DOI] and [schemas DOI], and the deposited example study at [deposit DOI]. The modeler runs in the browser without installation (https://behaverse.org/studyflow-modeler/app): a researcher draws a study from domain elements (consent, randomization, cognitive tasks), validates and runs it, and exports its views.

Tools and Resources fits because the paper reports a resource, not a finding about cognition, and shows its use in a proof-of-concept study; eLife reaches the researchers who design, preregister and replicate experiments. The manuscript is not under consideration elsewhere, all authors have approved its submission, and the preprint is at [preprint DOI]. We declare no competing interests; as the manuscript states, we also develop the Behaverse tasks and data model the demonstration uses.

Sincerely,

Morteza Ansarinia, corresponding author, on behalf of all authors
University of Luxembourg
morteza.ansarinia@uni.lu

# Suggested reviewers and editors (to fill)

No names are proposed here. For each slot, give a name, affiliation and email, and say whether the person is suggested as a Reviewing Editor (from eLife's board) or as a reviewer.

1. [Name, affiliation, email; Reviewing Editor or reviewer]: BPMN and process modeling, to assess the profile, the formal object and its execution semantics.
2. [Name, affiliation, email; Reviewing Editor or reviewer]: reproducibility and preregistration in psychology, to assess the deposit, the claim states and the deviation report.
3. [Name, affiliation, email; Reviewing Editor or reviewer]: experiment builders such as jsPsych or PsychoPy, to assess the actor interface and how Studyflow composes with existing builders.
4. [Name, affiliation, email; Reviewing Editor or reviewer]: machine psychology and the evaluation of language models, to assess the artificial cohort and the records kept for each model exchange.

# Author contributions (CRediT), proposal to confirm

These roles are placeholders, not a record of who did what. They are inferred only from the author order (first author as lead, last author as senior author) and from the example study file, which lists all three as its authors (hence Methodology for each). Each author must confirm or correct their own roles before submission.

- Morteza Ansarinia: Conceptualization, Methodology, Software, Formal analysis, Investigation, Data curation, Visualization, Writing – original draft, Writing – review and editing
- Hoorieh Afkari Roshan: Methodology, [Software or Validation], Writing – review and editing
- Pedro Cardoso-Leite: Conceptualization, Methodology, Supervision, [Funding acquisition], [Project administration], Writing – review and editing
