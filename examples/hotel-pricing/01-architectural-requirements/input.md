# Phase 1 Input - Architectural Requirements

Human-prepared minimum briefing. The architect prepares or validates this file; the agent uses it with `project-brief.md` to generate `architecture-drivers.md`.

## Source

- `examples/hotel-pricing/input/project-brief.md`

## Input

| Item | Value |
| --- | --- |
| Business problem | Legacy pricing system causes financial loss and modernization risk. |
| Objective | Replace pricing with a cloud-ready HPS for price changes, calculation, publication and queries. |
| Scope/MVP | Login, price changes, price queries, hotel/rate management and CMS publication. |
| Stakeholders | Sales managers, commercial representatives, administrators, operators, external systems and internal stakeholders. |
| Main functions | HPS-1 through HPS-6. |
| Expected quality attributes | Performance, reliability, availability, scalability, security, modifiability, deployability, monitorability and testability. |
| Constraints | Browser UI, cloud identity/hosting, company Git platform, MVP/release deadlines, REST first, cloud-native, Java/Angular knowledge. |
| External systems | User Identity Service, CMS, PMS, Commercial Analysis System and other consumers. |
| Customer priorities | HPS-2, HPS-3, HPS-4, QA-1, QA-2, QA-3, QA-4 and QA-5. |
