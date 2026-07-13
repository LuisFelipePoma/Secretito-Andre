# Optional Delivery Handoff Contract

Use this workflow only after phase 3 approval and only when implementation slices are useful.

## Plan Rules

- Use Approved architecture sources and current hashes.
- Define small `SLICE` outcomes, dependencies, affected boundaries, functional criteria, minimum tests, architecture checks/evidence, risks, rollback, and done conditions.
- Trace each primary driver needed for delivery to a slice and CHECK.
- Separate functional acceptance from architecture evidence.
- If planning reveals an architectural contradiction, reopen the relevant core gate.
- Do not implement code while creating the handoff.

Generate `design-system.md` only for a user interface needing shared tokens/components and when product/design ownership is identified. Its approval is independent from architecture and delivery approval.

`@sam slice N` emits one bounded prompt. It must list authoritative sources and prohibit unrelated slices or silent ADR changes.
