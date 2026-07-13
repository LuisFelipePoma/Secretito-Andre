---
name: sam
description: Run the three-phase SAM software architecture workflow and optional delivery handoff. Use when a user invokes @sam/$sam, wants architect-led AI drafting, needs approved architecture memory under docs/architecture, or asks for SAM status, drivers, ADD design, documentation, approval, reopening, handoff, or implementation slices.
---

# SAM Workflow

Use the user's language for conversation. Keep canonical filenames, stable IDs, metadata fields, and generated artifacts in English.

## Core Rules

- Treat SAM as three architecture phases: requirements, design, and documentation.
- Treat delivery planning as an optional handoff, never as phase 4.
- Let the agent draft and analyze; require the architect to approve drivers, material tradeoffs, ADRs, and accepted risks.
- Treat Draft and In Review artifacts as proposals. Only Approved artifacts constrain implementation.
- Write architecture artifacts under `docs/architecture/`; additionally maintain only the managed SAM block in root `AGENTS.md`.
- Preserve existing user content and stop on ambiguous migrations.
- Use `REQ`, `QA`, `CON`, `DRV`, `ADR`, `STORY`, `SLICE`, and `CHECK` identifiers.
- Use `Addressed`, `Pending`, or `Accepted Risk` during design. Use `Verified` or `Failed` only with executed evidence metadata.
- Ask only when an unresolved answer would change a primary driver, hard constraint, irreversible decision, or critical risk.

## State Helper

Resolve `../../scripts/sam_state.py` relative to this file. Use it for deterministic state, scaffolding, source hashes, migration, validation, drift, and approval.

```bash
python ../../scripts/sam_state.py init --name "Project"
python ../../scripts/sam_state.py status
python ../../scripts/sam_state.py next
python ../../scripts/sam_state.py can-run step-one
python ../../scripts/sam_state.py mark-draft phase-1-drivers
python ../../scripts/sam_state.py approve phase-1-drivers --approved-by "Architect"
python ../../scripts/sam_state.py reopen phase-2-design --reason "Driver changed"
python ../../scripts/sam_state.py handoff
```

If the helper cannot be resolved, follow the same contract manually in `docs/architecture/.sam/state.json`; never bypass a gate.

## Commands

### `@sam init NAME="project"`

Run `init`. It creates the three-phase base files, `docs/architecture/README.md`, state v3, and an idempotent SAM block in root `AGENTS.md`. Ask the user to complete and review `project-brief.md`; its blank scaffold cannot be approved.

### `@sam status` and `@sam next`

Run the matching helper command. Report drift, artifact authority, current core gate, optional delivery status, and one concrete next action. Never treat Superseded or drifted content as current.

### `@sam step-one`

Run `can-run step-one`. Read `references/phase-one.md` and the generated base files. Produce a complete driver proposal without architecture choices, update `architecture-drivers.md`, then run `mark-draft phase-1-drivers`.

### `@sam step-two`

Run `can-run step-two`. Read `references/phase-two.md`. Update the iteration plan and design decisions with bounded alternatives, instantiation, useful provisional views, ADR proposals, risks, and checks. Pause for material authority decisions; otherwise complete the coherent draft. Mark both artifacts Draft.

### `@sam step-three`

Run `can-run step-three`. Read `references/phase-three.md`. Select views from stakeholder questions, consolidate approved design information, complete traceability and agent guidance, then mark the architecture document Draft.

### `@sam approve GATE="..."`

Run helper approval only after the named human explicitly approves. Supported gates are `brief`, `phase-1-drivers`, `phase-2-design`, `phase-3-document`, optional `delivery`, and optional `design-system`. Validation, source hashes, order, and drift can block approval.

### `@sam reopen GATE="..." REASON="..."`

Run helper reopen. Preserve the reason, set the selected artifact Draft, and make dependent artifacts Superseded. Never edit an approved artifact silently.

### `@sam handoff`

Require phase 3 approval, run `handoff`, then read `references/delivery.md`. Generate the optional delivery plan. Create `design-system.md` from its asset only when a user interface needs shared design guidance and product/design ownership is known.

### `@sam step-four`

Treat as a deprecated alias for `@sam handoff`. Tell the user it is no longer a fourth architecture phase, then follow the handoff behavior.

### `@sam slice N`

Require an Approved delivery plan. Emit only the requested slice prompt with authoritative sources, boundaries, criteria, checks, tests, risks, and rollback. Do not implement it.

## Resources

- Read `references/phase-one.md`, `phase-two.md`, `phase-three.md`, or `delivery.md` only for the active workflow.
- Use `assets/templates/` as executable artifact scaffolds. Do not invent alternate required sections.
