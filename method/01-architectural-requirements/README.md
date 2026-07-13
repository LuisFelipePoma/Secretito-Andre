# 01 - Architectural Requirements

Goal: turn the project problem into a sufficient, prioritized set of architectural drivers without proposing a final design.

## Inputs

- `project-brief.md` and the phase `input.md` delta.
- Selected rigor profile and system context with rationale.
- Business goals, scope, stakeholders, significant functionality, quality expectations, constraints, existing systems, assumptions, and concerns.

`architecture-drivers.md` is an agent-generated proposal reviewed and approved by the architect.

## Process

1. Check intake sufficiency. Stop when a missing answer would materially change the architecture; otherwise record the gap as an assumption or risk.
2. Separate significant functionality, quality attributes, constraints, concerns, and assumptions.
3. Refine material quality attributes into six-part scenarios with measures or explicit measurement gaps.
4. Prioritize scenarios and concerns using QAW-lite and a utility tree.
5. Propose primary and supporting drivers with sources, rationale, tradeoffs, and risks.

## Output

`architecture-drivers.md` contains the intake summary, ASR classification, quality scenarios, assumptions, utility tree, driver proposal, questions, and risks.

## Approval Gate

The architect approves or corrects the profile, context, metrics, priorities, assumptions, tradeoffs, accepted gaps, and driver list. Approval is blocked when the brief is only a scaffold, a primary driver lacks a measurable scenario or accepted gap, source hashes are stale, or a critical question remains unowned.

## Agent Behavior

Generate a coherent draft when inputs are sufficient. Ask only questions whose answers would change scope, a primary driver, a hard constraint, or a high-risk tradeoff. Never propose technologies or architecture in this phase.
