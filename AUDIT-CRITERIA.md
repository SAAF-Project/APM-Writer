# AUDIT-CRITERIA.md — APM Writing Assistant

> What this agent must be judged against as an auditee: its control objectives, testable acceptance criteria, and known limits. The [README](README.md) separates current skeleton behavior from the proposed workflow. This document follows the SAAF A2 standard (`docs/conventions/audit-criteria-template.md` in the main SAAF-Project repo).

---

## Metadata

| Field | Value |
|---|---|
| **Agent** | APM Writing Assistant |
| **Repository** | https://github.com/SAAF-Project/APM-Writer |
| **Maintainer(s)** | Junhan Wen |
| **Last reviewed** | 2026-10-05 |
| **Status** | Draft |

**Sources used to draft this document:** the README and `scripts/run.py` in this repository, and the plan `plans/hackathon-2/junhan-wen-apm-writing-assistant.md` (SAAF-Project/SAAF-Project#135). The original design mapping has not been accepted as a new standard. A technical review of the skeleton does not validate these framework mappings or their legal applicability.

**Implementation state:** `scripts/run.py` is a skeleton. The agent is designed to make model calls at runtime, so AI-specific frameworks apply to the criteria below, but none of the steps is implemented yet. CO-1 to CO-5 remain design targets, not verified workflow behavior. A small, separate status/refusal contract is implemented and tested below.

## 1. What the agent is designed to do

The agent helps an auditor draft one section of an Audit Planning Memorandum (APM) per session. The auditor selects a section, and the agent runs a fixed intake process: audit scoping, document intake and validation, iterative clarification of the scope, and then synthesis and writing in the structure defined for that section. The finished section is saved to a local file and the path is shown to the auditor. The output is a draft for the auditor to review.

## 2. Control objectives & framework mapping

These are control objectives **for the agent itself**: what must be true of its behaviour for an auditor to rely on its output as a working draft.

| Control objective | Framework + clause/area | Why relevant |
|---|---|---|
| CO-1 — The intake cannot be skipped: no section text is produced until the audit scope and the documents have been confirmed by the auditor. | EU AI Act Art. 14 (human oversight) | The scope of an audit is the auditor's decision. A draft written before the scope is confirmed bakes in the model's assumptions. |
| CO-2 — Content is restricted to the evidence and traceable to it: the section uses only the provided documents and the auditor's explicit input, and key statements name their source. | IIA Global Internal Audit Standards 14.1 (Gathering Information for Analyses and Evaluation) and EU AI Act Art. 13 (transparency) | Planning conclusions drawn from invented or unattributed content would misdirect the audit. |
| CO-3 — Scope discipline: every part of the section concludes what belongs in the audit scope, and material outside the confirmed scope is not used. | IIA Global Internal Audit Standards 13.3 (Engagement Objectives and Scope) | The purpose of the APM sections is to support scoping decisions. |
| CO-4 — The auditor stays in control of the conversation: one question at a time, structured options when an answer is vague, and a confirmed recap after each phase. | IIA Global Internal Audit Standards 13.2 (Engagement Risk Assessment) | The intake only works if the auditor can follow and correct what the agent has understood at each step. |
| CO-5 — Confidential inputs and outputs are protected: no credentials in code, and no audit evidence, personal data or generated sections in the repository. | ISO/IEC 27001 Annex A (protection of information) and GDPR Art. 5 (data minimisation, confidentiality) | The inputs can include HR data, incident records and fraud cases. |

## 3. Acceptance criteria (testable, pass/fail)

### CO-1 — The intake cannot be skipped

- Given a new session, the agent first shows the available sections and asks which one to write; it accepts only a section listed in `available_sections`.
- Given a request to "just write the section" before scoping is confirmed, the agent does not draft; it continues with the next scoping question.
- Given uploaded documents, the agent summarises each document and its relevance and waits for confirmation before any analysis.
- Given a missing mandatory document for the selected section, the agent asks for it and does not draft without it or without the auditor's explicit decision to proceed.

### CO-2 — Evidence-restricted and traceable

- Given a finished section, every key statement refers to a provided document and its period.
- Given a topic for which the documents contain nothing, the section states that no information was provided; it does not fill the gap.
- Given a matter whose classification the source leaves open (for example, issue or incident), the section says the source does not make it clear.
- Given sources that use different terminology, the section does not harmonise it and notes the difference.

### CO-3 — Scope discipline

- Given a finished section, each part ends with a conclusion on what should be included in the audit scope and why.
- Given a document or case outside the confirmed scope, the section does not use it, not even for trend analysis.
- Given each scope refinement, the agent's update separates in scope, out of scope, and unclear.

### CO-4 — Auditor in control

- Given any turn of the intake, the agent asks exactly one question.
- Given a vague or incomplete answer, the agent proposes two or three structured options and asks the auditor to confirm or adjust one.
- Given the end of a phase, the agent gives a short recap and waits for confirmation before the next phase.

### CO-5 — Protection of inputs and outputs

- Given the repository, no file contains a credential, real audit evidence, personal data or a generated section.
- Given a finished session, only the written section is saved, locally, and the path is shown to the auditor.

## 4. Good output / never do

| A correct output MUST contain | The agent must NEVER |
|---|---|
| ✓ The section in the structure defined for it, in at most 8 short paragraphs | ✕ Draft before scope and documents are confirmed |
| ✓ A scope conclusion at the end of each part | ✕ Invent facts, risks, root causes or severity |
| ✓ Source and period for key statements | ✕ Use material outside the confirmed scope |
| ✓ An explicit statement where information is missing or classification is unclear | ✕ Replace the auditor's judgement or risk assessment |
| ✓ The local path of the saved section | ✕ Hard-code credentials, or commit audit evidence or generated sections |

The output is narrative text for an APM, not findings, so `outputs/schemas/finding-schema.json` does not apply to it.

## 5. Coverage gaps

- **Audit workflow not implemented.** `scripts/run.py` retains the workflow comments and placeholders. It reports static status or explicitly exits 2 without performing an intake, model call or draft. It no longer imports the unused proposed dependencies.
- **Content tests still missing.** Five public offline tests cover only the skeleton boundary. A synthetic planning-document set with expected source references, missing-input cases and rejected drafts is needed to test the future content workflow; confidential company documents are not required for public regression tests.
- **Section definitions are not in the repository.** The mandatory documents and the output structure per section are not yet defined in code; `available_sections` only lists section numbers.
- **One section per session.** Writing several sections from one shared scoping conversation is not designed yet.
- **No check of the draft against the documents.** Traceability is asked of the model; nothing verifies that a cited source actually contains the statement.

## 6. Status / validation

| Acceptance criterion | Verified? | Evidence |
|---|---|---|
| CO-1 to CO-4 — all criteria | ☐ | Not implemented; design targets only |
| CO-5 — no credentials, evidence or generated sections in the repository | Historical only | Original tracked-file review dated 2026-10-05; not a new full-history or current content assessment |
| CO-5 — only the section is saved locally | ☐ | Not implemented |

### Implemented skeleton contract (separate from CO-1 to CO-5)

The following checks describe current code, not additions to the approved SAAF
standards. Run `python3 -I -S -m unittest discover -s tests -v`; CI repeats the same
five synthetic tests on Python 3.9 and 3.12. Results belong to the tested commit
and run, not permanently to this file.

| Criterion | Type | Evidence / limit |
|---|---|---|
| APM-SK-01 — A normal invocation cannot report a completed intake or draft. | `[code]` | `test_default_invocation_reports_unimplemented_instead_of_success`: exit 2, explicit stderr and no draft stdout. |
| APM-SK-02 — A status query explicitly identifies a skeleton with `can_draft: false` and no model provider. | `[code]` | `test_status_is_explicit_design_metadata_not_a_draft`; successful metadata is not a successful audit run. |
| APM-SK-03 — Unsupported section, draft and positional arguments cannot silently succeed. | `[code]` | `test_unknown_section_or_draft_options_are_not_silently_accepted`: exit 2. |
| APM-SK-04 — The documented isolated invocation requires no site packages and leaves the synthetic working directory unchanged. | `[code]` | `test_isolated_cli_needs_no_site_packages_and_ignores_local_env_and_modules` plus status open/subprocess mocks. This is a bounded fixture, not a production sandbox. |
| CO-2/CO-3/CO-4 — Draft grounding, scope quality and conversational behavior. | `[llm]` | **Not assessed:** there is no implementation, chosen model, evaluation set or provider run. |

## 7. Observability

The current CLI writes only status JSON to stdout or a refusal to stderr; it creates no log or evidence dossier. No workflow step is implemented. The design saves only the finished section. A record of the confirmed scope, the documents used and the prompts sent to the model would be needed to trace a section back to its inputs.
