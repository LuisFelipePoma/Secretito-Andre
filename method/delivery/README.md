# Optional Delivery Handoff

Goal: convert approved architecture into bounded, testable implementation guidance for a delivery team or code agent.

This workflow is optional and begins only after phase 3 approval. It is not a fourth architecture phase and does not change core SAM completion.

## Inputs

- Approved `architecture-document.md` and design decisions.
- Delivery constraints, repository context, allowed/prohibited libraries, interfaces, checks, and risks.
- Product/design ownership and UI constraints when a user interface exists.

## Process

1. Confirm delivery constraints and repository state without reopening architectural choices implicitly.
2. Divide work into small, testable slices.
3. Link each slice to drivers, ADRs or accepted risks, affected boundaries, and checks.
4. Separate functional acceptance criteria from architecture evidence.
5. Define dependencies, tests, risks, rollback, and done conditions.
6. Generate `design-system.md` only for a user interface that needs one; record product/design approval separately.

## Outputs

- `implementation-plan.md`.
- Ordered implementation slices and one-slice code-agent prompts.
- Optional `design-system.md`.

## Approval

The architect or tech lead approves the delivery plan before `@sam slice N` emits a prompt. Product/design separately approves an optional design system. A missing design system never blocks a non-UI project.

## Agent Behavior

Do not implement code in this workflow. Do not expand a slice beyond its approved boundaries. If implementation planning reveals an architectural contradiction, reopen the relevant core gate instead of hiding the change in a slice.
