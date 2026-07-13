# Hotel Pricing System - Project Brief

## 1. Business Problem

AD&D Hotels needs to replace a legacy pricing system that has reliability, performance, availability and maintainability issues. These issues have caused financial losses and make modernization harder.

## 2. System Goal

Create a new Hotel Pricing System that lets authorized users manage hotel prices, calculate derived rates, publish prices to external systems and serve price queries reliably.

## 3. Initial Scope / MVP

Included:

- Login and authorization.
- Change prices for hotels and dates.
- Query prices through UI/API.
- Manage hotels and rates.
- Publish accepted prices to the Channel Management System.

Out of initial scope:

- Full replacement of every external system.
- Non-REST query protocols in the MVP.
- Advanced revenue-management optimization.

## 4. Stakeholders

| Stakeholder | Interest |
| --- | --- |
| Sales managers | Change prices quickly and safely. |
| Commercial representatives | Query and manage prices for authorized hotels. |
| Administrators | Manage hotels, rates and user permissions. |
| Operators | Monitor publication and system reliability. |
| External systems | Consume current prices. |
| Internal stakeholders | See an MVP in 2 months and release in 6 months. |

## 5. Main Features

- REQ-001: Log In.
- REQ-002: Change Prices.
- REQ-003: Query Prices.
- REQ-004: Manage Hotels.
- REQ-005: Manage Rates.
- REQ-006: Manage Users.

## 6. Expected Quality Attributes

- Performance for price publication.
- Reliability for accepted price changes and CMS delivery.
- Availability for price queries.
- Scalability for query volume growth.
- Security for identity and authorization.
- Modifiability for future protocols.
- Deployability across environments.
- Monitorability for publication operations.
- Testability without real external systems.

## 7. Constraints

- Browser-based UI across common platforms/devices.
- Managed cloud identity service and cloud hosting.
- Code hosted on the company's Git platform.
- MVP demo in 2 months and initial release in 6 months.
- Initial external integration through REST APIs.
- Cloud-native approach preferred.
- Team knowledge favors Java and Angular.

## 8. Current Context

The company has multiple systems around hotel operations and commercial analysis. Existing integrations use REST/SOAP request-response endpoints and shared database integration anti-patterns. Enterprise architecture principles now require a more decoupled model.

## 9. Environments And Operations

- Development: local developer machines.
- Integration: cloud environment with mocks for unavailable systems.
- Staging: cloud environment connected to test versions of external systems.
- Production: real operation.

## 10. Customer Priorities

Highest priority:

- REQ-002 Change Prices.
- REQ-003 Query Prices.
- REQ-004 Manage Hotels.
- QA-001 Performance.
- QA-002 Reliability.
- QA-003 Availability.
- QA-004 Scalability.
- QA-005 Security.

## 11. Risk, Rigor And System Context

Rigor profile: Standard. System context: Evolution. Revenue-impacting pricing, high query growth, identity/CMS integrations, and material delivery risk require explicit operational and security evidence.

## 12. Data, Security And Recovery

Prices are internal business data and identity claims are confidential. API/identity and API/CMS boundaries require protection; publication recovery, reversible migrations, and rollback of query projections are required.

## 13. Assumptions And Open Questions

Managed identity and cloud hosting remain available. CMS retry limits, price retention, and regional hosting requirements require confirmation.
