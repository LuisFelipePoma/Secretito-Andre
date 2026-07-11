---
name: sam
description: Run the SAM workflow commands (@sam init/status/next/step-one/step-two/step-three/step-four/approve/reopen/slice) and keep validated artifacts under docs/architecture.
---

# SAM Workflow

Use this skill when the user invokes `@sam`, `$sam`, or asks to run SAM step by step.

## Core Rules

- Write project artifacts only under `docs/architecture/`.
- Keep method/source files untouched unless the user asks to change the method itself.
- Do not mark an artifact approved unless the architect explicitly uses `approve`.
- Treat generated artifacts as drafts.
- Refuse phase advancement when the previous gate is not approved.
- Use stable `REQ`, `QA`, `CON`, `DRV`, `ADR`, `STORY`, `SLICE`, and `CHECK` identifiers.
- Never use `Verified` without executed evidence; a design decision only makes a driver `Addressed`.
- Validate artifacts before approval and synchronize Markdown metadata with state.
- Do not create custom `/sam` slash prompts in v1.

## State Helper

Use the helper script at `../../scripts/sam_state.py`, resolved relative to this `SKILL.md`.

Commands:

```bash
python ../../scripts/sam_state.py init --name "Project Name"
python ../../scripts/sam_state.py status
python ../../scripts/sam_state.py next
python ../../scripts/sam_state.py can-run step-two
python ../../scripts/sam_state.py mark-draft phase-1-drivers
python ../../scripts/sam_state.py approve phase-1-drivers --approved-by "Architect"
python ../../scripts/sam_state.py validate phase-1-drivers
python ../../scripts/sam_state.py reopen phase-2-design --reason "Driver changed"
```

If the script path cannot be resolved, follow the same state contract manually in `docs/architecture/.sam/state.json`.

## Supported Commands

### `@sam init NAME="project-name"`

Run `sam_state.py init`. This creates:

```text
docs/architecture/
  project-brief.md
  01-architectural-requirements/input.md
  02-architectural-design/input.md
  03-architectural-documentation/input.md
  04-architectural-implementation/input.md
  .sam/state.json
```

Then tell the user to fill or review `docs/architecture/project-brief.md`.
Existing `docs/arquitecture/` workspaces are migrated only when the canonical root does not exist; conflicting roots require manual reconciliation.

### `@sam status`

Run `sam_state.py status` and report the current gate, artifact statuses, and next action.

### `@sam next`

Run `sam_state.py next`. Execute only the returned next action when it is unblocked.

### `@sam step-one`

Run `sam_state.py can-run step-one`. Read:

- `docs/architecture/project-brief.md`
- `docs/architecture/01-architectural-requirements/input.md`
- `references/templates.md`

Generate or update the drivers artifact using the template. Include tailoring profile, versioned sources, stable IDs, measurable scenarios, driver proposal, tradeoffs, open questions, and a completed exit checklist. Then mark it draft.

### `@sam step-two`

Run `sam_state.py can-run step-two`. Read approved phase 1 output and phase 2 input. Create or update:

- `docs/architecture/02-architectural-design/iteration-plan.md`
- `docs/architecture/02-architectural-design/design-decisions.md`

Use ADD with at most 3 concepts per driver group. Store provisional views in `design-decisions.md`, not in phase 3. Link primary drivers to ADRs and pending checks; use `Addressed`, `Pending`, or `Accepted Risk`, never `Verified`. Complete exit checklists and mark both artifacts draft.

### `@sam step-three`

Run `sam_state.py can-run step-three`. Consolidate approved provisional views into the architecture document. Include only question-driven optional views, profile-required security/data/operations material, interfaces/events, stable stories, full traceability, evidence status, governance, and exit checklist. Then mark it draft.

### `@sam step-four`

Run `sam_state.py can-run step-four`. Generate the plan with stable slices, dependencies, affected boundaries, functional criteria, separate checks/evidence, tests, risks, rollback, and exit checklist. Generate `design-system.md` only for a frontend and record product/design approval separately. Then mark drafts.

### `@sam approve GATE="phase-1-drivers"`

Run `sam_state.py approve <gate> --approved-by "<name>"`.

The helper blocks out-of-order approval, incomplete artifacts, unchecked exit criteria, missing IDs, and ambiguous design-validation statuses.

Supported gates:

- `brief`
- `phase-1-drivers`
- `phase-2-design`
- `phase-3-document`
- `phase-4-implementation`

### `@sam reopen GATE="phase-2-design" REASON="driver changed"`

Run `sam_state.py reopen <gate> --reason "<reason>"`. The selected gate becomes Draft and later dependent artifacts become Superseded.

### `@sam slice N`

Require the phase 4 plan to be approved, then emit only the prompt for Slice N. Do not implement the slice.

## Templates

Read `references/templates.md` before generating phase artifacts.
