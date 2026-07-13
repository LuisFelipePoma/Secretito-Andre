# 03 - Architectural Documentation

Goal: turn approved design work into living architecture memory that stakeholders, implementers, operators, and agents can use.

## Inputs

- Approved iteration plan and design decisions.
- Instantiated elements, interfaces, behavior, provisional views, risks, checks, and phase `input.md` delta.
- Stakeholders, their concerns, and the intended uses of the documentation.

## Process

1. Identify documentation audiences, questions, and uses.
2. Select the smallest set of views that answers those questions.
3. Consolidate approved provisional views and document each view's elements, relations, legend, rationale, and known limitations.
4. Add cross-view information: scope, drivers, scenarios, ADRs, interfaces, behavior, security/data/operations concerns, glossary, and risks.
5. Trace primary drivers to decisions or accepted risks, views when relevant, and evidence-producing checks.
6. Define governance, review triggers, drift handling, and reading guidance for humans and agents.

C4, module, runtime, deployment, data, security, class, sequence, or other views are optional. Select notation after selecting the question; never add a diagram only to satisfy a template.

## Output

`architecture-document.md` is the governed living architecture package. The generated `docs/architecture/README.md` points agents to its approved version and related sources.

## Approval Gate

The architect approves documentation sufficiency, view selection, cross-view consistency, risks, and traceability. Phase 3 approval completes the core SAM method. Delivery planning remains optional.

## Agent Behavior

Preserve decision rationale and uncertainty. Detect contradictions between views and ADRs. Keep implementation detail only when it constrains architecture or is needed to use an interface. Do not turn Draft content into authoritative guidance.
