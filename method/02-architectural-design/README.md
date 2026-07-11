# 02 - Architectural Design

Goal: design the architecture with ADD from approved drivers.

## Input

- Phase `input.md`, derived from the approved Architectural Requirements output.
- Prioritized driver list.
- Measurable quality scenarios.
- Constraints, concerns, risks, and priorities.
- Allowed catalog of patterns, technologies, and architectures.

## Process

1. Define the iteration goal.
2. Choose elements to refine.
3. Select design concepts: patterns, tactics, technologies, or architectures.
4. Instantiate elements, responsibilities, interfaces, and collaborations.
5. Record decisions and tradeoffs.
6. Classify design coverage as `Addressed`, `Pending`, or `Accepted Risk`; reserve `Verified` and `Failed` for executed evidence.

## Output

- Iteration plan ADD.
- Selected concepts.
- Architectural decisions.
- ADD analysis.
- Provisional design views embedded in `design-decisions.md`; phase 3 consolidates them into the living architecture document.
- Driver-decision-pending-evidence traceability.

## Approval Gate

The architect approves decisions, discarded alternatives, and covered drivers before moving to Architectural Documentation.

### Exit checklist

- Every primary driver is `Addressed`, `Pending`, or `Accepted Risk`; design work never marks a driver `Verified`.
- Each `Addressed` driver links to an ADR and a pending `CHECK` that can verify its measure.
- Provisional views describe affected boundaries and collaborations without consuming the phase 3 document.
- Iteration, instantiation, consequences, and review triggers are recorded.

Missing items block approval.

## Scenario Format

| Field | Question |
| --- | --- |
| Source of stimulus | Who or what triggers the event? |
| Stimulus | What happens? |
| Artifact | Which part of the system receives the stimulus? |
| Environment | Under what conditions does it happen? |
| Response | What must the system do? |
| Measure | How is the result validated? |

## AI Agent Role

The agent runs ADD step by step, proposes bounded alternatives, and prepares tradeoff tables. The architect approves each step before moving forward.
