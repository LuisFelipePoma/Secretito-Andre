# SAM - Software Architecture Method

SAM moves from a client problem to approved, usable architecture while preserving decision authority, traceability, and project memory.

## Operating Model

The AI agent performs the expensive drafting work: it extracts information, finds gaps, proposes bounded alternatives, updates artifacts, and checks traceability. The architect reviews, modifies, and explicitly approves drivers, tradeoffs, accepted risks, and decisions.

The workflow is hybrid. Generate a coherent phase draft when inputs are sufficient, but stop for a question when an unresolved issue would materially change the architecture. Do not require approval for mechanical drafting steps; do require it at governed gates.

## Initial Input

Every project starts with `project-brief.md`. It describes the problem and context without prescribing a final architecture. Use [project-brief-template.md](project-brief-template.md).

## Main Flow

1. [Architectural Requirements](01-architectural-requirements/README.md) turns the brief into prioritized ASRs, measurable quality scenarios, constraints, assumptions, and drivers.
2. [Architectural Design](02-architectural-design/README.md) applies ADD iteratively and records alternatives, instantiated elements, interfaces, ADRs, provisional views, and checks.
3. [Architectural Documentation](03-architectural-documentation/README.md) selects and consolidates the views and cross-view information required by stakeholders, implementers, operators, and agents.

Architecture documentation begins during design; phase 3 packages and validates it rather than postponing documentation until design is finished.

[Delivery Handoff](delivery/README.md) is optional after phase 3 approval. It prepares slices and code-agent context without becoming a fourth architecture gate.

## Artifact Chain

```text
project-brief.md
  -> 01-architectural-requirements/input.md
  -> 01-architectural-requirements/architecture-drivers.md
  -> 02-architectural-design/input.md
  -> 02-architectural-design/iteration-plan.md + design-decisions.md
  -> 03-architectural-documentation/input.md
  -> 03-architectural-documentation/architecture-document.md
  -> delivery/implementation-plan.md (optional)
```

## Tailoring

Record both axes in every governed artifact.

| Axis | Values | Effect |
| --- | --- | --- |
| Rigor | Lite / Standard / High Assurance | Controls review depth, evidence, and assurance. |
| System context | Greenfield / Evolution / Integration | Controls discovery, compatibility, migration, and boundary concerns. |

| Rigor | Typical use | Minimum depth |
| --- | --- | --- |
| Lite | Low criticality, small scope, reversible decisions | Essential drivers, explicit assumptions, only material decisions, question-driven views, and lightweight checks. |
| Standard | Material business risk, integrations, moderate uncertainty | Lite plus operational/security concerns, runtime or deployment views as needed, and executable architecture checks. |
| High Assurance | Regulatory, safety, privacy, financial, or high cost of failure | Standard plus formal reviews, resilience/recovery evidence, migration/rollback, and independent approvals where required. |

The profile controls depth, not approval integrity. Project type never forces a diagram or pattern.

## Artifact Contract

Governed artifacts use `Draft`, `In Review`, `Approved`, or `Superseded`. Record approver, UTC approval date, rigor profile, system context, and source hashes. An approved source changed outside the workflow is drift; dependent approvals remain blocked until it is reopened.

Stable identifiers use `REQ`, `QA`, `CON`, `DRV`, `ADR`, `STORY`, `SLICE`, and `CHECK`. A primary driver traces to an approved ADR or an explicitly accepted risk and an evidence-producing check. `Verified` and `Failed` require executed evidence; design coverage uses `Addressed`, `Pending`, or `Accepted Risk`.

## Living Architecture Memory

`docs/architecture/README.md` is the generated entry point for humans and agents. It lists the current gate, authoritative artifacts, constraints, and reading order. Approved artifacts constrain implementation. Draft artifacts may inform discussion but must not silently override approved content.

When a driver, constraint, or decision changes, reopen the relevant gate. Mark dependent artifacts Superseded, preserve history in version control, and review downstream effects before implementation continues.

## Minimum Outcome

- Sufficient intake or explicit unresolved risks.
- Prioritized architectural drivers and measurable scenarios where material.
- ADD iterations proportional to architectural significance.
- Approved ADRs or an explicit statement that no material decision is required.
- Stakeholder-relevant views and cross-view rationale.
- Traceability from primary drivers to decisions or accepted risks and checks.
- Optional delivery slices when a team or code agent needs them.
