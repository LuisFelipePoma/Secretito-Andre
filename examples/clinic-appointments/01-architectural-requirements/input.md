# Phase 1 Input - Architectural Requirements

Human-prepared minimum briefing. The architect prepares or validates this file; the agent uses it with `project-brief.md` to generate `architecture-drivers.md`.

## Source

- `examples/clinic-appointments/input/project-brief.md`

## Input

| Item | Value |
| --- | --- |
| Business problem | Manual scheduling causes double-bookings, missed appointments and poor visibility. |
| Objective | Create a web appointment system for patients, receptionists, doctors and managers. |
| Scope/MVP | Login, availability search, booking, reschedule/cancel, receptionist management, doctor schedule, notification request. |
| Stakeholders | Patients, receptionists, doctors, clinic managers and IT operations. |
| Main functions | CA-1 through CA-7. |
| Expected quality attributes | Consistency, availability, performance, security/privacy, modifiability and monitorability. |
| Constraints | Browser UI, MVP in 10 weeks, external notification provider, cloud preferred, small team. |
| External systems | Email/SMS provider. |
| Customer priorities | Prevent double-booking, fast booking, protect patient data, ship MVP. |
