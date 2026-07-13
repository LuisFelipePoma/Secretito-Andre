# Repository Guidelines

## Purpose And Operating Model

SAM is a three-phase Software Architecture Method for senior software architects and senior software engineers who need to move quickly without losing decision quality or project memory. It applies to software-intensive work of different sizes and shapes, including landing pages, web applications, APIs, internal tools, integrations, and larger distributed systems.

SAM is an architect-led, AI-assisted workflow. The agent analyzes inputs, exposes missing information, proposes bounded alternatives, drafts artifacts, and keeps approved information traceable. The architect reviews and edits those drafts, approves drivers and tradeoffs, accepts risks, and owns every architectural decision. Generated content is never final merely because an agent produced it.

The project-local `docs/architecture/` directory is living architecture memory. Approved artifacts guide delivery teams and future agents; Draft and In Review artifacts are proposals only. Agents must not contradict an approved driver or ADR silently. When an approved source changes, reopen it and review dependent artifacts before treating them as current.

## Method Structure

Core method content lives in `method/` and follows three phases:

- `01-architectural-requirements/`: identify and prioritize architecturally significant requirements and quality scenarios.
- `02-architectural-design/`: apply ADD iteratively and record concepts, tradeoffs, ADRs, provisional views, and pending evidence.
- `03-architectural-documentation/`: package stakeholder-relevant views and cross-view information into living documentation.

`method/delivery/` is an optional post-method handoff. It turns approved architecture into implementation slices and can add a design system for projects with a user interface. It is not a fourth architecture phase and does not block completion of the three-phase method.

The root `README.md` is the repository entry point. Shared intake material is in `method/project-brief-template.md`; intellectual foundations and their mapping to SAM practices are in `method/foundations.md`. Worked examples live under `examples/<domain>/` and mirror the three phases, with optional delivery material under `examples/<domain>/delivery/`.

## Method Invariants

- Tailor on two axes: rigor (`Lite`, `Standard`, `High Assurance`) and system context (`Greenfield`, `Evolution`, `Integration`).
- Use functional requirements, quality attribute scenarios, constraints, concerns, and assumptions as ADD inputs.
- Select views because they answer stakeholder or implementation questions; do not require C4, UML, 4+1, or any other notation by default.
- Give stable IDs to governed information: `REQ`, `QA`, `CON`, `DRV`, `ADR`, `STORY`, `SLICE`, and `CHECK`.
- Trace each primary driver to an approved decision or explicitly accepted risk and to an evidence-producing check. Delivery handoffs additionally trace drivers to slices.
- Use `Addressed` for design coverage. Use `Verified` or `Failed` only when executed evidence is recorded.
- Preserve source versions, approval metadata, consequences, review triggers, and supersession history.
- Do not impose a fixed number of ADRs or diagrams. A Lite project may legitimately record that no material architectural decision or optional view is needed.

## Project Structure And Stable Names

Keep these artifact names stable: `project-brief.md`, `input.md`, `architecture-drivers.md`, `iteration-plan.md`, `design-decisions.md`, `architecture-document.md`, `implementation-plan.md`, and `design-system.md`. Use lowercase kebab-case for new directories and descriptive Markdown filenames.

The Codex plugin lives in `plugins/sam/`. Its state helper owns `docs/architecture/.sam/state.json`, creates an idempotent SAM block in a target project's `AGENTS.md`, and maintains the generated `docs/architecture/README.md` index. Plugin behavior must preserve existing user files and must stop rather than overwrite ambiguous migrations.

## Build, Test, And Development Commands

The method and examples are Markdown; the plugin also contains a Python state helper.

- `rg --files`: list repository files.
- `rg -n "TODO|TBD|FIXME|\[TODO:" README.md method examples plugins --glob '!plugins/sam/scripts/sam_state.py'`: find unfinished content while excluding validator literals.
- `python3 plugins/sam/scripts/sam_state.py self-test`: exercise state, gates, drift, migration, and validation.
- `python3 plugins/sam/scripts/sam_state.py template-parity`: verify public and executable templates are identical.
- `python3 plugins/sam/scripts/sam_state.py validate-examples`: validate every example through synchronized temporary workspaces.
- `git diff --check`: catch trailing whitespace and common formatting errors.
- `git diff -- README.md AGENTS.md method examples plugins`: review method and plugin changes.

Use the skill-creator and plugin-creator validators after editing plugin skills or the manifest. If their environment lacks PyYAML, run them through `uv` with a temporary `pyyaml` dependency rather than adding a runtime dependency to SAM.

## Documentation Style

Write canonical repository content and generated artifacts in English. The agent should converse in the user's language while preserving stable filenames, IDs, and status vocabulary. Use concise headings, short paragraphs, and tables when comparison or traceability matters. Keep terminology consistent: SAM, ADD, ASR, ADR, QAW, drivers, decisions, views, checks, evidence, and traceability.

## Testing And Review Guidelines

Validate both document shape and semantic flow:

- each phase input derives from approved sources;
- critical questions are resolved or explicitly accepted as risks;
- primary drivers reach ADRs or accepted risks and `CHECK` definitions;
- only executed evidence can mark a driver Verified or Failed;
- optional views identify their audience and question;
- approved-source hash drift blocks downstream approval;
- examples conform to current templates and state validation.

When templates or contracts change, update every structurally affected example and the plugin copy, then run the parity and state tests.

## Commit And Pull Request Guidelines

Use imperative, sentence-style summaries and keep commits scoped to one coherent documentation or plugin change. Pull requests should identify the changed phase or workflow, the motivation, compatibility or migration effects, and the traceability impact.

## Intellectual Foundations

SAM synthesizes, without reproducing, practices from Attribute-Driven Design and QAW from the Software Engineering Institute, Views and Beyond, architecture quality-attribute and evaluation literature, enterprise and architectural pattern catalogs, ADR practices, C4 where useful, and evolutionary architecture. `method/foundations.md` records the detailed source-to-practice mapping. These sources inform the workflow; they do not replace architect judgment or project-specific evidence.
