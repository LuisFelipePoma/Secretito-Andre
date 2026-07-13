# Agent Prompts - Optional Delivery Handoff

## Implementation Plan

```text
Using the approved architecture document, design decisions, and delivery input, generate implementation-plan.md. Divide work into small slices with stable SLICE IDs. Include related drivers/ADRs, dependencies, affected boundaries, functional criteria, separate CHECK/evidence expectations, minimum tests, risks, rollback, and done conditions.
```

## Design System

```text
Only when the project has a user interface and product/design ownership is identified, generate design-system.md. Record product/design approval separately from architecture approval. Do not create this artifact for a non-UI project.
```

## Code Agent Slice Prompt

```text
Emit context for exactly one approved slice. Include authoritative artifacts, drivers/ADRs, affected boundaries, criteria, checks, tests, risks, and rollback. Mention concrete files only after inspecting an existing repository. Forbid unrelated work and silent architecture changes.
```
