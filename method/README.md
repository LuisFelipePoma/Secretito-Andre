# SAM - Software Architecture Method

Practical method to move from a client problem to implementable architecture without losing control of information, decisions, and traceability.

## Initial Input

Every project starts with a `project-brief.md`. This file is delivered by the client/team and must not contain final technical design.

Use [project-brief-template.md](project-brief-template.md) as the base format.

## Main Flow

1. [Architectural Requirements](01-architectural-requirements/README.md): categorize quality attributes, prioritize tradeoffs, and obtain a prioritized driver list.
2. [Architectural Design](02-architectural-design/README.md): run ADD with approved drivers and select patterns, tactics, technologies, and architectures.
3. [Architectural Documentation](03-architectural-documentation/README.md): document views, decisions, interfaces, events, traceability, and Scrum handoff.
4. [Architectural Implementation](04-architectural-implementation/README.md): convert approved architecture into implementable slices, stack/libraries, tests, and design system.

## Input Chain

```text
project-brief.md
  -> 01-architectural-requirements/input.md
  -> 02-architectural-design/input.md
  -> 03-architectural-documentation/input.md
  -> 04-architectural-implementation/input.md
```

## SAM Rule

The agent does not decide architecture. The agent prepares information, alternatives, and artifacts; the architect approves drivers, tradeoffs, and decisions.

## Tailoring Profile

Select one profile during intake and record it in every phase input.

| Profile | Use when | Required depth |
| --- | --- | --- |
| Lite | Low criticality, small team, reversible decisions | Drivers, bounded decisions, context/container views, traceability, and slices. |
| Standard | Material business risk, integrations, or moderate uncertainty | Lite plus component/sequence views where needed, operational scenarios, threat review, and fitness checks. |
| High Assurance | Safety, financial, regulatory, privacy, or high cost of failure | Standard plus formal security/data review, resilience and recovery evidence, migration/rollback, and independent approvals. |

The profile controls depth, not whether approval and traceability are required. Add a diagram only when it answers a stakeholder or implementation question.

## Artifact Contract

All governed artifacts use `Draft`, `In Review`, `Approved`, or `Superseded`. Approval records the approver, UTC date, and source artifact versions (Git commit or content hash). A gate is blocked when required sections, stable IDs, unresolved critical questions, or its exit checklist are missing. Revisions to an approved source mark dependent artifacts for review.

Stable identifiers use `REQ`, `QA`, `CON`, `DRV`, `ADR`, `STORY`, `SLICE`, and `CHECK`. A primary driver must trace to at least one decision, implementation slice, and evidence-producing check.

## Minimum Output

- Prioritized drivers.
- ADD iteration plan.
- 3 to 7 initial architectural decisions.
- Basic C4 views and necessary diagrams.
- Initial backlog with epics/stories linked to drivers or decisions.
- Implementation plan with slices, criteria, tests, and constraints.
- Design system when the project has a frontend.
