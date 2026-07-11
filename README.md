# SAM - Software Architecture Method

Lightweight method to standardize architecture work in software projects with tight timelines.

SAM follows 4 phases: requirements, design, documentation, and architectural implementation to prepare work for a code agent or delivery team.

1. [Architectural Requirements](method/01-architectural-requirements/README.md)
2. [Architectural Design](method/02-architectural-design/README.md)
3. [Architectural Documentation](method/03-architectural-documentation/README.md)
4. [Architectural Implementation](method/04-architectural-implementation/README.md)

The full SAM entry point is [method/README.md](method/README.md).

Every project starts with a `project-brief.md`; use [method/project-brief-template.md](method/project-brief-template.md).

## AI Agent Role

The agent is an approved copilot: it prepares artifacts, questions, alternatives, diagrams, ADRs, and the initial backlog. The architect sets priorities, accepts tradeoffs, and approves decisions.

## Codex Plugin

SAM includes a Codex plugin under `plugins/sam/`.

Install it from this repository:

```powershell
git clone https://github.com/LuisFelipePoma/SAM.git
cd SAM
codex plugin marketplace add .\.agents\plugins
codex plugin add sam@local-repository
```

Open a new Codex thread after installing so the plugin is loaded.

Use the workflow commands:

```text
@sam init NAME="Project Name"
@sam status
@sam next
@sam approve GATE="phase-1-drivers"
@sam slice 1
```

The plugin writes project artifacts under `docs/architecture/` and keeps approval gates in `docs/architecture/.sam/state.json`. Existing `docs/arquitecture/` workspaces are detected and migrated compatibly.

## Structure

| Path | Use |
| --- | --- |
| `method/` | 4-phase SAM method. |
| `method/project-brief-template.md` | Initial input delivered by the client/team. |
| `method/01-architectural-requirements/` | Quality attributes, ASRs, QAW-lite, utility tree, and prioritized list. |
| `method/02-architectural-design/` | ADD and selection of patterns, tactics, technologies, and architectures. |
| `method/03-architectural-documentation/` | C4, database view, 4+1, class diagrams, ADRs, interfaces, events, and traceability. |
| `method/04-architectural-implementation/` | Implementation slices, stack, libraries, tests, and design system. |

## Examples

| Path | Use |
| --- | --- |
| `examples/hotel-pricing/` | AD&D Hotels example. |
| `examples/clinic-appointments/` | Clinic appointment scheduling example to validate another domain. |
| `examples/online-auctions/` | Nationwide online auction example with real-time bidding. |

## Acceptance Criteria

In 1 or 2 sessions, SAM should produce prioritized drivers, 3 to 7 architectural decisions, basic C4 views, an initial backlog, and risks. Each critical story must link to a driver or decision.

SAM supports Lite, Standard, and High Assurance tailoring. In every profile, primary drivers retain end-to-end links to decisions, implementation slices, and evidence-producing architecture checks.

## Base Sources

ADD/SEI, QAW-lite, Views and Beyond, C4, ADRs, enterprise architecture patterns, and evolutionary architecture.
