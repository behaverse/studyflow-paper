# Cover letter (draft)

[date]

Dear Editors,

We submit "Studyflow, a visual notation for coordinating experiments in the cognitive sciences, from design to publication" as a Tools and Resources article.

A cognitive science study's data have shared standards such as BIDS; its process has no shared machine-readable form. The process is spread across a protocol, scripts, analysis code and figures; each keeps its own copy of the study's parameters, free to drift, and none fully records what was done.

Studyflow gives that process one machine-readable representation, a `.studyflow.yaml` file that is at once the protocol, the runnable study, the analysis specification and the publication figure, each a view for a different audience, so there is no second copy to drift. Formally, a study is a typed directed multigraph with validity conditions and execution semantics, realized as a profile of the ISO standard BPMN 2.0. Two records follow that current practice lacks: the deviation report is the diff between the file before and after execution, and every registered question ends in a claim state (Supported, Not supported or Not testable) decided by a rule drawn before any run.

The example study runs end to end from one file on cohorts of open-weight language models, three models one line apart, that are enrolled, screened, allocated, administered two cognitive tasks, and analyzed. Before those runs, the registered analysis was checked on simulated participants with a planted effect, which it recovered, and on a null copy, which it rejected; that check exposed a fault in the classifier before the file was sealed. A human cohort would take the same protocol through the same interface, as a pool of its own, which this paper designs for but does not yet demonstrate. In the supplement, two published studies encoded from their Methods sections each leave about ten run-critical parameters unstated.

Our own fault library catches ten of twelve faults we seeded, but authors seed what their checks were designed to catch. Of twelve deviations seeded by an agent that never saw the checks, the validator reports one, and the protocol digest flags all twelve. Validation checks form, not science.

The reference tools and the schema are open source under the MIT license, on GitHub (https://github.com/behaverse/studyflow-modeler, https://github.com/behaverse/schemas), with archived releases at [modeler DOI] and [schemas DOI], and the example study's files and runs at [deposit DOI]. The modeler runs in the browser without installation (https://behaverse.org/studyflow-modeler/app), where a researcher draws a study from domain elements such as consent, randomization and cognitive tasks; the command-line tool validates and runs it.

Tools and Resources fits because the paper reports a resource, not a finding about cognition, and verifies it against a planted effect; eLife reaches the researchers who design, preregister and replicate experiments. The manuscript is not under consideration elsewhere, all authors have approved its submission, and the preprint is at [preprint DOI]. We declare no competing interests; as the manuscript states, we also develop the Behaverse data model, whose trial-level shape the example study's records follow.

Sincerely,

Morteza Ansarinia, corresponding author, on behalf of all authors
University of Luxembourg
morteza.ansarinia@uni.lu

# Suggested reviewers and editors (to fill)

No names are proposed here. For each slot, give a name, affiliation and email, and say whether the person is suggested as a Reviewing Editor (from eLife's board) or as a reviewer.

1. [Name, affiliation, email; Reviewing Editor or reviewer]: BPMN and process modeling, to assess the profile, the formal object and its execution semantics.
2. [Name, affiliation, email; Reviewing Editor or reviewer]: reproducibility and preregistration in psychology, to assess the protocol digest, the claim states and the deviation report.
3. [Name, affiliation, email; Reviewing Editor or reviewer]: experiment builders such as jsPsych or PsychoPy, to assess the actor interface and how Studyflow composes with existing builders.
4. [Name, affiliation, email; Reviewing Editor or reviewer]: machine psychology and the evaluation of language models, to assess the simulated and language-model cohorts and the records kept for each model exchange.

# Author contributions (CRediT), proposal to confirm

These roles are placeholders, not a record of who did what. They are inferred only from the author order (first author as lead, last author as senior author) and from the example study file, which lists all three as its authors (hence Methodology for each). Each author must confirm or correct their own roles before submission.

- Morteza Ansarinia: Conceptualization, Methodology, Software, Formal analysis, Investigation, Data curation, Visualization, Writing – original draft, Writing – review and editing
- Hoorieh Afkari Roshan: Methodology, [Software or Validation], Writing – review and editing
- Pedro Cardoso-Leite: Conceptualization, Methodology, Supervision, [Funding acquisition], [Project administration], Writing – review and editing
