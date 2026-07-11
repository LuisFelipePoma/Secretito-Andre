# 03 - Architectural Documentation

Goal: leave enough evidence to build, review, and maintain the architecture.

## Input

- Phase `input.md`, derived from the approved Architectural Design output.
- Approved decisions.
- Instantiated elements.
- Interfaces, events, and responsibilities.
- Addressed, pending, verified, failed, or accepted-risk drivers, with evidence where applicable.
- Initial stories/epics.

## Process

1. Document minimum C4 views: context, containers, and components when applicable.
2. Add 4+1, database, or class diagram views only when they answer a real question.
3. Record ADRs or a decision table with alternatives and consequences.
4. Link requirement, scenario, driver, decision, view, story, and check.
5. Translate decisions into epics/stories and define governance checks.
6. Record data classification, trust boundaries, threat review, SLO/SLI, recovery, deployment, migration, and rollback when required by the selected profile or drivers.

## Output

- Living architecture document.
- Architectural decisions.
- Relevant interfaces and events.
- Traceability matrix.
- Handoff a Scrum.

## Approval Gate

Each critical story must link to a driver or decision. Decisions must have an associated view/diagram and check.

The approved output from this phase feeds Architectural Implementation.

### Exit checklist

- Approved provisional views are consolidated; optional views state the question they answer.
- Every primary driver traces to a decision, story, and evidence-producing `CHECK`.
- Security, data, operations, recovery, migration, and rollback concerns required by the profile are addressed or accepted as risks.
- ADR review triggers and supersession status are visible.

Missing items block approval.

## AI Agent Role

The agent keeps documents consistent, generates diagrams, detects decisions without traceability, and reviews architecture-code drift. The architect validates the final version.
