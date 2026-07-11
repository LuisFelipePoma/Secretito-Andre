# Agent Prompts - Architectural Implementation

## Implementation Plan

```text
Using architecture-document.md, design-decisions.md, and phase 4 input, generate implementation-plan.md with the phase template. Divide work into small slices with stable `SLICE` IDs. Each slice must have driver/ADR, story, dependencies, affected boundaries, functional criteria, architecture checks/evidence, minimum tests, risks, and rollback.
```

## Design System

```text
If the project has a frontend and product/design ownership is identified, generate design-system.md using the template. Record product/design approval separately from architecture approval. Do not create it for backend-only work.
```

## Code Agent Slice Prompt

```text
Prepare a prompt to implement only one slice. Include minimum context, related drivers/ADRs, affected boundaries, functional criteria, architecture checks/evidence, tests, risks, and rollback. Mention files only when a repository already exists. Forbid implementing unrequested slices.
```
