# Repository Guidelines

## Project Structure & Module Organization

This repository documents SAM, a four-phase Software Architecture Method. The root `README.md` is the entry point. Core method content lives in `method/`, with one folder per phase:

- `01-architectural-requirements/`
- `02-architectural-design/`
- `03-architectural-documentation/`
- `04-architectural-implementation/`

Shared starting material is in `method/project-brief-template.md`. Worked examples live under `examples/<domain>/` and mirror the phase structure, for example `examples/hotel-pricing/03-architectural-documentation/architecture-document.md`.

## Build, Test, and Development Commands

There is no build system or package manager in this repo; changes are markdown-only.

- `rg --files`: list tracked documentation files quickly.
- `rg -n "TODO|TBD|FIXME" method examples`: find unfinished content before review.
- `git diff --check`: catch trailing whitespace and common diff formatting issues.
- `git diff -- README.md method examples`: review documentation changes before committing.

## Coding Style & Naming Conventions

Use Markdown with concise headings, short paragraphs, and tables where comparison matters. Keep phase artifact names stable: `input.md`, `architecture-drivers.md`, `design-decisions.md`, `architecture-document.md`, `implementation-plan.md`, and `design-system.md`. Use lowercase kebab-case for new directories and descriptive markdown filenames, matching existing examples. Keep terminology consistent: SAM, ADD, ASR, ADR, C4, drivers, decisions, and traceability.

## Testing Guidelines

No automated test framework is configured. Validate documentation by checking flow and traceability: each phase input should derive from the previous phase output, critical stories should link to drivers or ADRs, and examples should match the templates in `method/`. When updating templates, update at least one example or explicitly note why examples do not change.

## Commit & Pull Request Guidelines

Recent commits use imperative, sentence-style summaries such as `Refactor README files...`, `Remove output expectations...`, and `Add Architectural Implementation phase...`. Follow that style and keep commits scoped to one documentation change.

Pull requests should include the changed phase or example, the reason for the change, and any traceability impact. For example updates, mention which template or method rule was validated.

## Agent-Specific Instructions

Agents prepare artifacts, questions, alternatives, diagrams, ADRs, and backlog drafts. The architect approves drivers, tradeoffs, and architectural decisions; do not present generated architecture as final without that approval.
