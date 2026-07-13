# Phase 2 Contract - Architectural Design

## ADD Iteration

For each iteration:

1. Select the element to design or refine.
2. Select a cohesive group of approved ASRs and drivers affecting it.
3. Compare at most three viable tactics, patterns, technologies, services, frameworks, or other concepts.
4. Instantiate elements, responsibilities, data ownership, trust boundaries, and allocation.
5. Define collaborations and interfaces; create only views needed to answer the iteration question.
6. Record material ADRs, alternatives, consequences, review triggers, status, and pending checks.
7. Review coverage and inventory remaining ASRs.

For Evolution and Integration contexts, preserve compatibility, migration, existing constraints, and rollback concerns explicitly.

## Hybrid Review

Generate a coherent draft when choices are bounded. Pause for an unresolved irreversible technology choice, critical tradeoff, material ADR, or risk acceptance. The architect may edit the files directly before approval.

## Evidence Semantics

- `Addressed`: an ADR responds to the driver; evidence is pending.
- `Pending`: a decision or check definition is incomplete.
- `Accepted Risk`: the architect explicitly accepts the condition.
- `Verified` / `Failed`: executed evidence exists and the trace row includes `Evidence:` and `Executed:`.

Every primary driver must map to an ADR or Accepted Risk and a `CHECK`. A Lite project may have no ADR only with an explicit architect-approved no-material-decision rationale.
