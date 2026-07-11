# 04 - Architectural Implementation

Goal: convert approved architecture into packages ready for a code agent or Scrum team.

## Input

- Phase `input.md`, derived from Architectural Documentation.
- `architecture-document.md`, decisions, traceability, and Scrum handoff.
- Interfaces, events, governance checks, and driver status.
- Stack, allowed/prohibited libraries, and UI constraints when applicable.

## Process

1. Confirm stack, libraries, and constraints that cannot be broken.
2. Divide implementation into small, testable slices.
3. Associate each slice with driver, ADR, story/use case, and architectural check.
4. Define acceptance criteria and minimum tests per slice.
5. Create `design-system.md` when the project has a frontend.
6. Define dependencies, risks, rollback, affected boundaries, and expected architecture evidence per slice.

## Output

- `implementation-plan.md`.
- `design-system.md` when there is a frontend.
- Ordered implementation slices.
- Acceptance criteria, minimum tests, and constraints per slice.

## Approval Gate

The architect or tech lead approves that each slice respects drivers/ADRs and has minimum tests before passing it to the code agent. Product/design approves the optional design system; its absence never blocks a backend-only project.

### Exit checklist

- Every primary driver links to at least one `SLICE` and `CHECK`.
- Functional acceptance criteria and architecture checks are separate.
- Dependencies, risks, rollback, and affected boundaries are explicit.
- The design system exists only when applicable and records product/design approval.

## AI Agent Role

The agent prepares the implementation plan, design system, and prompts per slice. It does not write code in this phase.
