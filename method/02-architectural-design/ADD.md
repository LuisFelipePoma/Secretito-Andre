# Attribute-Driven Design In SAM

Use ADD after the Architectural Requirements gate is approved. Treat design and its working documentation as one activity: decisions and provisional views are recorded during each iteration, then consolidated in phase 3.

## Preconditions

Confirm that significant functionality, quality scenarios, constraints, assumptions, and prioritized drivers are sufficient for the intended iteration. If a missing answer would materially change the design, record the question and stop. Otherwise record the assumption and risk.

## Iteration 1: Select The Target

Choose one element that needs design or refinement. In a greenfield first iteration, this is normally the whole system. In Evolution or Integration work, it may be an existing boundary, integration, deployment unit, or change area.

Record the iteration goal, selected element, and expected decision or view output.

## Iteration 2: Select Relevant ASRs

Choose a cohesive, prioritized subset of approved drivers, significant functionality, constraints, concerns, and assumptions that affect the selected element. Do not introduce requirements that are absent from approved sources.

## Iteration 3: Choose Design Concepts

Evaluate no more than three viable concepts. Concepts may include tactics, architectural or design patterns, reference architectures, frameworks, managed services, existing components, or deployment approaches.

Compare how each concept addresses the selected ASRs, its negative effects on other qualities, constraints, operational cost, delivery risk, and reversibility. Mark alternatives as discarded only with rationale.

## Iteration 4: Instantiate Elements And Responsibilities

Adapt selected concepts to the project. Identify new or changed elements, responsibilities, data ownership, trust boundaries, dependencies, and allocation decisions. Preserve existing constraints and migration needs for Evolution and Integration contexts.

## Iteration 5: Define Collaborations And Interfaces

Define the interactions needed by the selected stories or scenarios. Use a sequence, runtime, data-flow, module, deployment, or other provisional view only when it answers the iteration question. Record the audience, question, elements, relations, and legend for every view.

## Iteration 6: Record Decisions And Checks

Create ADRs only for decisions that affect structure, quality attributes, integration, deployment, data ownership, trust boundaries, or expensive-to-change technology. Record rationale, consequences, discarded alternatives, review triggers, and supersession status.

Define a `CHECK` for each quantitative or otherwise testable primary driver. A design decision makes coverage `Addressed`; only executed evidence can make it `Verified` or `Failed`.

## Iteration 7: Review And Continue

Assess whether the selected drivers are Addressed, Pending, or Accepted Risk. Inventory remaining ASRs and select the next element or stop when further design would not reduce material risk.

Update `iteration-plan.md` and `design-decisions.md` after every iteration. Architect approval is required for material tradeoffs, ADRs, and accepted risks, not for clerical updates.
