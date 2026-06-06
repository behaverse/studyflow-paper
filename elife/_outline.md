# eLife Paper — Structure and Status

**Working title:** *Studyflow: a framework for end-to-end specification of experimental research in cognitive sciences, from protocol to publication*

**Status (2026-06):** framework-forward structure; modeler + runner merged into one "toolkit"; ~13,600 body words (down ~17% across revision). 79 cited references, 12 `[FILL]` data-dependent placeholders, figures 1-12, listings 1-4. American English, no em/en-dashes (house style). Prose tuned to Morty's voice (see [`_voice_checklist.md`](_voice_checklist.md)).

---

## Front matter
- **Abstract:** framework + formal object foregrounded; closes on the worked study as a *demonstration* (a CONSORT-style RCT in which human participants and a cohort of artificial agents are co-subjects across a six-task cognitive battery).
- **Impact statement:** framework-focused (single source of truth). Human-AI is the worked example, never the headline.
- **Keywords:** scientific workflows, process modeling, experimental design, cognitive assessment, BPMN, reproducibility.

## §1 Introduction
| § | Title | Summary |
|---|---|---|
| 1.1 | The reproducibility gap is in *processes*, not just data | Process is the missing half; voluntary narrative checklists have empirically failed (7-14% preregistration); a machine-readable, human-understandable process representation is what is needed. |
| 1.2 | Current practice fragments the study across artifacts | Four overlapping families (figures, checklists, data standards, code), each covering one slice; an execution-vs-communication split. |
| 1.3 | BPMN as a foundation | Extend a mature ISO-standard process notation with its extension mechanism rather than invent a language. |
| 1.4 | Desiderata for a study specification language | Seven numbered desiderata R1-R7 + `@tbl-requirements` mapping each to where the framework meets it. |
| 1.5 | Contributions | Four artifacts: (1) LinkML language spec, (2) layered runtime schemas, (3) worked-example library, (4) an open-source *reference toolkit* (modeler + runner, fully working prototypes, not production software). |

## §2 The Studyflow framework
| § | Title | Summary |
|---|---|---|
| 2.1 | Studyflow as a formal object | Typed attributed directed graph (N,E,T,τ,λ); BPMN 2.0 profile; what it inherits / adds / leaves alone; layered schemas; `@tbl-elements`; Listings 1-2. |
| 2.2 | Multiple views: Study / Gantt / Checklist / Figure | Each view a projection of the formal object; one source renders four ways (Figure 5). |
| 2.3 | The Studyflow toolkit: a modeler and a runner | Two open-source, browser-only working-prototype reference implementations on top of the language. Modeler (schema-driven, Figure 3); runner (walks a participant or agent node by node behind one message-passing executor, Figure 4). Architecture detail deferred to §5.4. |

## §3 A complete study, from protocol to publication
The worked demonstration, explicitly subordinate to the framework. One registered human-and-agent agreement trial: ten people + a cohort of artificial agents as co-subjects across a six-task Behaverse battery (n-back, digit span, multiple-object tracking, pattern comparison, matrix reasoning, card sorting).
| § | Title | Summary |
|---|---|---|
| 3.1 | Design: a registered human/agent agreement | CONSORT 2025 / SPIRIT 2025 scaffolding; attrition as boundary error events so the diagram's topology matches the trial's (Figure 6). |
| 3.2 | Enroll and run: one diagram runs the trial for every subject | Six-task battery; n-back worked detail (Figure 7 + Listing 3); one executor behind which four actors stand (human, RL via CogEnv, recurrent via CogPonder, LLM) (Figure 8); agent cohort matrix (`@tbl-agents` + Figure 9). |
| 3.3 | Measure agreement: human-agent comparison and the CONSORT flow | Typed data-operation pipeline as machine-readable pre-registration; RT-analysis subprocess vs dplyr (Figure 10). |
| 3.4 | Model agreement: a human-versus-agent classifier | Same trials feed a classifier; multimodal preprocessing/training pipeline sketched (Figure 11). |
| 3.5 | Report: the file that ran the trial is the CONSORT figure and the benchmark | Figure exported from the protocol that ran; reporting-guideline coverage (`@tbl-guidelines`); SPIRIT Gantt (Figure 12). |

## §4 Discussion
| § | Title |
|---|---|
| 4.1 | What Studyflow changes: from divergent artifacts to one auditable diagram |
| 4.2 | Relationship to existing ecosystems (execution stacks, data standards, reporting guidelines, BPMN profiles; "different planes" of the LinkML/NIDM/BIDS/ARTEM-IS pattern) |
| 4.3 | Objections and alternate views (four skeptic objections, each conceded then answered) |
| 4.4 | Limitations (tooling-scope vs deliberate-boundary; two unvalidated claims) |
| 4.5 | Future directions (closes on a vision-tied beat) |

## §5 Methods
| § | Title |
|---|---|
| 5.1 | The language specification (LinkML single source; six moddle layers) |
| 5.2 | Serialization (BPMN 2.0 XML, namespaced extensions, graceful degradation) |
| 5.3 | The Studyflow grammar (EBNF, Listing 4) |
| 5.4 | The runner interface (NodeDefinition contract; one message-passing executor; actor model) |
| 5.5 | Reproducibility and availability (seed fixes the protocol; responses sampled) |

## Back matter
Code and data availability; Supplementary Table S1 (full element catalog).

---

## Figures, listings, tables
- **Figures 1-12** (inventory + status in [`figures/README.md`](figures/README.md)). Key mapping: executor = Fig 8, agent profiles = Fig 9, RT pipeline = Fig 10, multimodal = Fig 11, SPIRIT = Fig 12.
- **Listings:** 1-2 LinkML/moddle (§2.1), 3 n-back XML (§3.2), 4 EBNF grammar (§5.3).
- **Tables:** `@tbl-requirements` (R1-R7, §2), `@tbl-elements` (representative elements, §2.1), `@tbl-agents` (seed-42 cohort, §3.2, `[FILL]`), `@tbl-guidelines` (11 reporting guidelines, §3.5).

## Open items
- **Seed-42 run still deferred:** 12 `[FILL]` placeholders (agent cohort, RT summaries, runner screenshots). See [`_checklist.md`](_checklist.md).
- **MIT LICENSE** file on the modeler repo (claimed in §1.5 / Code-and-data).
- **`%!VERIFY` refs** in `references.bib` (Zotero double-check).
- **8 now-unused refs** prunable after the §3.2 "Beyond one participant" shrink: `sebanz2006joint`, `babiloni2014hyperscanning`, `hakim2023interbrain`, `kothe2025lsl`, `dahlback1993woz`, `aher2023llms`, `binz2023gpt3`, `park2023agents`.
- **Reporting-guideline templates** beyond CONSORT/SPIRIT (the `@tbl-guidelines` "Roadmap" rows).
