# Phase 2 Input - Architectural Design

## Source

- `examples/clinic-appointments/01-architectural-requirements/architecture-drivers.md`

## Approved Drivers

| Driver | Priority |
| --- | --- |
| QA-1 Consistency | Primary |
| QA-2 Performance | Primary |
| QA-4 Security/privacy | Primary |
| QA-3 Availability | Supporting |
| QA-5 Monitorability | Supporting |
| QA-6 Modifiability | Supporting |

## Constraints And Risks

- MVP in 10 weeks favors a modular monolith.
- Double-booking is the highest architecture risk.
- Availability search must not scan transactional appointment data inefficiently.
- Patient privacy requires API-level authorization and audit logging.
- Notification provider failures must not block confirmed bookings.

## Allowed Design Catalog

- Modular monolith.
- Transactional booking with unique slot constraint.
- Read-optimized availability projection.
- Role/ownership authorization.
- Outbox for notification requests.
- Metrics/logging with correlation IDs.
