# Clinic Appointments - Project Brief

## 1. Business Problem

A private clinic chain manages patient appointments through phone calls, spreadsheets and isolated calendars. This causes double-bookings, missed appointments, slow rescheduling and poor visibility for clinic managers.

## 2. System Goal

Create a web system for patients, receptionists and doctors to schedule, reschedule, cancel and monitor medical appointments across clinics.

## 3. Initial Scope / MVP

Included:

- Patient registration and login.
- Search doctor availability by specialty, location and date.
- Book, reschedule and cancel appointments.
- Receptionist appointment management.
- Doctor daily schedule view.
- Email/SMS notification request to an external provider.

Out of initial scope:

- Payments.
- Electronic medical records.
- Insurance authorization.
- Telemedicine video calls.

## 4. Stakeholders

| Stakeholder | Interest |
| --- | --- |
| Patients | Book appointments quickly and receive reminders. |
| Receptionists | Manage schedules without double-booking. |
| Doctors | See an accurate daily schedule. |
| Clinic managers | Monitor appointment volume and no-shows. |
| IT operations | Deploy and monitor the system with low support effort. |

## 5. Main Features

- REQ-001: Register and log in.
- REQ-002: Search availability.
- REQ-003: Book appointment.
- REQ-004: Reschedule/cancel appointment.
- REQ-005: Receptionist manages doctor calendars.
- REQ-006: Doctor views daily schedule.
- REQ-007: Send notification request.

## 6. Expected Quality Attributes

- Consistency: avoid double-booking.
- Availability: booking must remain available during business hours.
- Performance: availability search must be fast.
- Security/privacy: protect patient personal data.
- Modifiability: support future payment and telemedicine modules.
- Monitorability: track booking failures and notification failures.

## 7. Constraints

- Web app for desktop and mobile browsers.
- MVP in 10 weeks.
- Existing clinic identity provider is not available; email/password login is acceptable for MVP.
- SMS/email delivery must use an external provider.
- Cloud deployment is preferred.
- Small team: 2 backend, 1 frontend, 1 QA.

## 8. Current Context

Each clinic has different scheduling practices. Doctor availability changes frequently. Managers need consolidated appointment visibility but do not need medical record data in MVP.

## 9. Environments And Operations

- Development: local.
- QA: cloud test environment.
- Production: cloud production environment.
- Basic monitoring and error alerts are required.

## 10. Customer Priorities

Highest priority:

- Prevent double-booking.
- Book appointments quickly.
- Protect patient data.
- Ship MVP in 10 weeks.

## 11. Risk And Tailoring Inputs

Standard profile: confidential patient data, concurrent booking risk, external notifications, and moderate change cost require more than Lite, without High Assurance evidence for this illustrative MVP.

## 12. Data, Security And Recovery

Patient and appointment data are confidential. API authorization is a trust boundary; booking recovery must prevent confirmed double-bookings, and deployments require reversible schema changes.
