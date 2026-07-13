# 02 - Architectural Design

Goal: design enough architecture to address approved drivers and expose remaining risk, using iterative Attribute-Driven Design.

## Inputs

- Approved `architecture-drivers.md` and phase `input.md` delta.
- Rigor profile, system context, constraints, assumptions, accepted risks, and existing architecture when applicable.
- Project-approved pattern, technology, or platform catalogs when they exist.

## Process

1. Plan iterations by element and cohesive groups of ASRs.
2. Select an element and the relevant approved drivers for one iteration.
3. Compare at most three viable patterns, tactics, technologies, or other design concepts.
4. Instantiate elements, responsibilities, data ownership, collaborations, and interfaces.
5. Sketch only the provisional views required to reason about the iteration.
6. Record material ADRs, consequences, discarded alternatives, review triggers, and pending checks.
7. Review the iteration goal and inventory remaining ASRs before continuing.

Use `Addressed`, `Pending`, or `Accepted Risk` for design coverage. Reserve `Verified` and `Failed` for executed evidence.

## Outputs

- `iteration-plan.md`: intended and completed ADD iterations.
- `design-decisions.md`: selected concepts, instantiation, ADRs, provisional views, risks, and driver/check coverage.

## Approval Gate

The architect approves material concepts, tradeoffs, ADRs, accepted risks, and the sufficiency of remaining checks. A phase can contain zero ADRs only when the architect approves the explicit conclusion that no material, expensive-to-change decision is required.

## Agent Behavior

Draft a complete proposal when constraints and drivers make the choices bounded. Pause when a critical tradeoff, irreversible technology choice, risk acceptance, or requirement ambiguity needs architect authority. Do not turn a design choice into Verified evidence.
