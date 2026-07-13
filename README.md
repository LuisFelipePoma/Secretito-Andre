# SAM - Software Architecture Method

SAM is a lightweight, architect-led method for turning a software problem into approved, traceable architecture without losing delivery speed or project memory.

It is designed for senior software architects and senior software engineers working on anything from a landing page or internal tool to an integration-heavy or distributed system. The amount of architecture work changes with risk and context; the architect's decision authority does not.

## Three-Phase Method

1. [Architectural Requirements](method/01-architectural-requirements/README.md): identify and prioritize architecturally significant requirements, constraints, quality scenarios, and assumptions.
2. [Architectural Design](method/02-architectural-design/README.md): apply ADD iteratively, compare bounded alternatives, and record decisions, tradeoffs, and pending evidence.
3. [Architectural Documentation](method/03-architectural-documentation/README.md): package stakeholder-relevant views and cross-view information as living architecture memory.

[Delivery Handoff](method/delivery/README.md) is an optional extension that converts approved architecture into implementation slices. It is not a fourth architecture phase.

Every project starts with a `project-brief.md`; use [method/project-brief-template.md](method/project-brief-template.md). The complete flow is in [method/README.md](method/README.md), and [method/foundations.md](method/foundations.md) maps SAM practices to their intellectual sources.

## AI Agent Role

The agent prepares drafts, questions, alternatives, diagrams, ADR proposals, checks, and optional delivery slices. The architect edits and approves drivers, tradeoffs, risks, and architectural decisions. Draft or generated content is never final without explicit approval.

Approved artifacts under `docs/architecture/` become living guidance for delivery teams and future agents. Draft and In Review artifacts remain proposals. Source drift blocks dependent approvals until the architect reopens and reviews them.

## Codex Plugin

SAM includes a Codex plugin under `plugins/sam/`.

```powershell
git clone https://github.com/LuisFelipePoma/SAM.git
cd SAM
codex plugin marketplace add .
codex plugin add sam@local-repository
```

Open a new Codex thread after installation or reinstall so the plugin is reloaded.

```text
@sam init NAME="Project Name"
@sam status
@sam next
@sam approve GATE="phase-1-drivers"
@sam handoff
@sam slice 1
```

The plugin creates three-phase artifacts under `docs/architecture/`, maintains a generated architecture index, and records approvals in `docs/architecture/.sam/state.json`. Existing `docs/arquitecture/` workspaces and legacy `04-architectural-implementation/` handoffs are migrated conservatively.

## Tailoring

SAM tailors on two axes:

- Rigor: `Lite`, `Standard`, or `High Assurance`.
- System context: `Greenfield`, `Evolution`, or `Integration`.

Views, ADRs, checks, and delivery artifacts are included only when justified by stakeholder questions, architectural significance, risk, or the selected profile. A Lite project may legitimately need no optional diagrams or material ADRs if that conclusion is recorded explicitly.

## Examples

| Path | Purpose |
| --- | --- |
| `examples/hotel-pricing/` | ADD-style pricing system with integrations and quality drivers. |
| `examples/clinic-appointments/` | Transactional scheduling system in another business domain. |
| `examples/online-auctions/` | Real-time, auditable auction platform. |
| `examples/product-landing/` | Lite landing page showing proportional architecture work. |

## Acceptance Criteria

SAM succeeds when an architect can reach a sufficiently documented, explicitly approved architecture in proportion to the project's risk. Primary drivers must remain traceable to decisions or accepted risks and evidence-producing checks. Optional delivery handoffs additionally connect drivers and decisions to implementable slices.
