---
name: sam
description: Run the SAM architecture workflow commands (@sam init/status/next/step-one/step-two/step-three/step-four/approve/slice) and keep artifacts under docs/arquitecture with architect approval gates.
---

# SAM Workflow

Use this skill when the user invokes `@sam`, `$sam`, or asks to run SAM step by step.

## Core Rules

- Write project artifacts only under `docs/arquitecture/`.
- Keep method/source files untouched unless the user asks to change the method itself.
- Do not mark an artifact approved unless the architect explicitly uses `approve`.
- Treat generated artifacts as drafts.
- Refuse phase advancement when the previous gate is not approved.
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
```

If the script path cannot be resolved, follow the same state contract manually in `docs/arquitecture/.sam/state.json`.

## Supported Commands

### `@sam init NAME="project-name"`

Run `sam_state.py init`. This creates:

```text
docs/arquitecture/
  project-brief.md
  01-architectural-requirements/input.md
  02-architectural-design/input.md
  03-architectural-documentation/input.md
  04-architectural-implementation/input.md
  .sam/state.json
```

Then tell the user to fill or review `docs/arquitecture/project-brief.md`.

### `@sam status`

Run `sam_state.py status` and report the current gate, artifact statuses, and next action.

### `@sam next`

Run `sam_state.py next`. Execute only the returned next action when it is unblocked.

### `@sam step-one`

Run `sam_state.py can-run step-one`. Read:

- `docs/arquitecture/project-brief.md`
- `docs/arquitecture/01-architectural-requirements/input.md`
- `references/templates.md`

Generate or update `docs/arquitecture/01-architectural-requirements/architecture-drivers.md` using the Architectural Requirements template. Include status metadata as Draft, ASR classification, measurable scenarios, utility tree, driver proposal, tradeoffs, and open questions. Then run `sam_state.py mark-draft phase-1-drivers`.

### `@sam step-two`

Run `sam_state.py can-run step-two`. Read approved phase 1 output and phase 2 input. Create or update:

- `docs/arquitecture/02-architectural-design/iteration-plan.md`
- `docs/arquitecture/02-architectural-design/design-decisions.md`

Use ADD. Keep alternatives bounded to at most 3 concepts per driver group. Mark both artifacts as draft with `mark-draft phase-2-iteration-plan` and `mark-draft phase-2-decisions`.

### `@sam step-three`

Run `sam_state.py can-run step-three`. Read approved phase 2 artifacts and phase 3 input. Generate or update `docs/arquitecture/03-architectural-documentation/architecture-document.md` with C4 views, decisions, interfaces/events, Scrum handoff, traceability, and governance checks. Then run `sam_state.py mark-draft phase-3-document`.

### `@sam step-four`

Run `sam_state.py can-run step-four`. Read approved phase 3 output, phase 2 decisions, and phase 4 input. Generate `docs/arquitecture/04-architectural-implementation/implementation-plan.md`. Generate `design-system.md` only when the project has a frontend. Then mark drafts in state.

### `@sam approve GATE="phase-1-drivers"`

Run `sam_state.py approve <gate> --approved-by "<name>"`.

Supported gates:

- `brief`
- `phase-1-drivers`
- `phase-2-design`
- `phase-3-document`
- `phase-4-implementation`

### `@sam slice N`

Read `docs/arquitecture/04-architectural-implementation/implementation-plan.md` and emit only the prompt for Slice N. Do not implement the slice.

## Templates

Read `references/templates.md` before generating phase artifacts.
