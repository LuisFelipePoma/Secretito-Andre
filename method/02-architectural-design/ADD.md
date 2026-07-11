# Attribute Driven Design

Attribute Driven Design is an iterative process to design software architectures. Use it after the Architectural Requirements phase has produced approved drivers.

## Step 1: Review Inputs

Review the approved drivers, phase input, existing provisional design views, and `iteration-plan.md`.

Confirm that the iteration has:

- Functional drivers, quality attribute scenarios, constraints, and concerns.
- A prioritized list of drivers approved by the architect.
- Enough context to choose design concepts without inventing requirements.

If critical information is missing, answer with questions and wait for review.

## Step 2: Establish goal for the iteration by selecting drivers

The goal of the iteration has been defined in `iteration-plan.md`. Review the goal and associated drivers.

## Step 3: Choose one or more elements of the system to refine

Consider the provisional views in `design-decisions.md` and identify elements that need refinement. The living architecture document does not exist until phase 3.
Refinement can mean decomposition into finer-grained elements (top-down approach), combination of elements into coarser-grained elements (bottom-up approach), or improvement of previously identified elements. For greenfield development, in the first iteration, the only element to refine is the whole system.

Answer with the list of elements to be refined and wait for user review.

## Step 4: Choose One or More Design Concepts That Satisfy the Selected Drivers

In this step, design concepts are selected to achieve the iteration goal, these design concepts may include:

- Design patterns, reference architectures, architectural patterns, design patterns, and deployment patterns.
- Externally developed components, frameworks, or specific cloud resources.
- Tactics that address particular quality attributes.

Use an existing pattern or technology catalog when available. Do not brainstorm unlimited options. Answer with the selected design concepts, pros, cons, and discarded alternatives. Show this in a Markdown table and wait for review.

| Design concept | Pros | Cons | Discarded alternatives |
| -------------- | ---- | ---- | ---------------------- |
|                |      |      |                        |

## Step 5: Instantiate Architectural Elements, sketch views, allocate Responsibilities, and Define Interfaces

In this step, the selected design concepts are adapted to address the drivers that compose the goal of the iteration, that is the meaning of instantiation. This may result in new elements created or existing elements changed.

Create or modify provisional Mermaid views in `design-decisions.md`.

For the definition of interfaces, first create sequence diagrams that illustrate how the instantiated elements collaborate to support the selected stories or scenarios. Add them to the provisional views section; phase 3 later consolidates approved views.

Answer with instantiation decisions in a table:

| Instantiation decision | Rationale |
| ---------------------- | --------- |

Wait for user review.

## Step 6: Record Design Decisions

Design decisions are documented in the Architectural Decisions section using a table like the following one:

| ID | Driver | Decision | Rationale | Discarded alternatives | Consequences |
| -- | ------ | -------- | --------- | ---------------------- | ------------ |

Record only decisions that affect structure, quality attributes, deployment, integration, data ownership, or expensive-to-change technology choices. Wait for user review.

## Step 7: Perform Analysis of Current Design and Review Iteration Goal and Achievement of Design Purpose

For this step, you must analyze if the design decisions made during the iteration were sufficient to address the drivers associated with the iteration goal. Answer with a table like the following:

| Driver | Coverage status | Decision | Pending evidence/check | Next action |
| ------ | --------------- | -------- | ---------------------- | ----------- |

Coverage status has these meanings:

- Addressed: an approved decision responds to the driver; verification is pending.
- Verified: executed evidence meets the measure. This is recorded only after execution, never inferred during design.
- Failed: executed evidence does not meet the measure.
- Pending: the decision or evidence definition is incomplete.
- Accepted Risk: the architect explicitly accepts the uncovered or failed condition.

Update only the driver-decision-pending-evidence table in this phase. Phase 3 creates the complete traceability matrix.
