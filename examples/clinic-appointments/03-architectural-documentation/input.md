# Phase 3 Input - Architectural Documentation

## Source

- `examples/clinic-appointments/02-architectural-design/iteration-plan.md`
- `examples/clinic-appointments/02-architectural-design/design-decisions.md`

## Approved Decisions

| ID | Decision |
| --- | --- |
| ADR-001 | Use a modular monolith. |
| ADR-002 | Prevent double-booking with a transactional booking flow and unique slot constraint. |
| ADR-003 | Use a read-optimized availability projection. |
| ADR-004 | Enforce role/ownership authorization in the API and audit access. |
| ADR-005 | Send notification requests through an outbox and provider adapter. |

## Elements To Document

- Web App.
- Clinic Appointments API.
- Appointment DB.
- Availability Projection.
- Notification Outbox.
- Email/SMS Provider.
- Metrics/Logging.

## Interfaces And Events

- `POST /appointments`
- `PATCH /appointments/{id}`
- `GET /availability`
- `GET /doctor-schedule`
- `AppointmentBooked`
- `NotificationRequested`

## Initial Stories

- Search availability.
- Book appointment.
- Reschedule/cancel appointment.
- Doctor daily schedule.
- Notification request.
- Booking failure monitoring.
