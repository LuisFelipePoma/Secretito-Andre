# Phase 2 Input - Architectural Design

## Source

- `examples/hotel-pricing/01-architectural-requirements/architecture-drivers.md`

## Approved Drivers

| Driver | Priority |
| --- | --- |
| QA-1 Performance | Primary |
| QA-2 Reliability | Primary |
| QA-3 Availability | Primary |
| QA-4 Scalability | Primary |
| QA-5 Security | Primary |
| QA-6 Modifiability | Supporting |
| QA-7 Deployability | Supporting |
| QA-8 Monitorability | Supporting |
| QA-9 Testability | Supporting |

## Measurable Scenarios

Use the quality scenarios from Phase 1, especially:

- QA-1: price publication in less than 100 ms.
- QA-2: 100% of accepted changes become queryable and reach CMS.
- QA-3: 99.9% query uptime outside maintenance windows.
- QA-4: 100k/day initially and 1M/day with less than 20% latency degradation.
- QA-5: authenticated users only see and execute authorized functions/hotels.

## Constraints And Risks

- MVP in 2 months creates delivery risk.
- Existing integrations can propagate failures.
- Shared database integration must be avoided.
- Query growth can overload command-side persistence.
- CMS delivery failures cannot lose accepted changes.

## Allowed Design Catalog

- Modular monolith.
- Ports and adapters.
- Transactional outbox.
- Message broker.
- Read-optimized query store/cache.
- Managed identity.
- Externalized configuration.
- Metrics/tracing.
