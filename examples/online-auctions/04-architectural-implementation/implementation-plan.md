# Online Auctions - Implementation Plan

## 1. Source Artifacts

- Architecture document: `../03-architectural-documentation/architecture-document.md`
- Design decisions: `../02-architectural-design/design-decisions.md`
- Traceability matrix: Architecture document section 11.
- Scrum handoff: Architecture document section 10.

## 2. Stack And Libraries

| Area | Choice | Constraint |
| --- | --- | --- |
| Frontend | Browser web app | Follow `design-system.md`; support bidder and clerk flows. |
| Realtime | WebSocket gateway | Ordered bid updates per auction. |
| Backend | Auction API and bidding workers | Bid ordering enforced server-side. |
| Database | Append-only bid ledger and read models | Immutable bid/payment audit records. |
| Payments | Tokenized provider adapter | Charge requests run through outbox. |
| Video | Managed streaming/CDN provider | Streaming isolated from bid command path. |
| Tests | Unit + integration + load checks | Include sequencer, fanout and payment outbox checks. |
| Observability | Logs/metrics/traces/audit | Per-auction health and correlation IDs are required. |

## 3. Implementation Order

| Order | Slice | Why now |
| --- | --- | --- |
| 1 | Platform skeleton | Establish module/service boundaries and local run path. |
| 2 | Bidder registration and payment token | Required before bidding and charging. |
| 3 | Auction catalog and live room | Gives users auctions, lots and room entry. |
| 4 | Bid sequencer and ledger | Highest risk driver: ordered bid acceptance. |
| 5 | Real-time bid feed and video integration | Makes live participation usable at scale. |
| 6 | Lot close, payment outbox and reputation | Completes winner charge and participant tracking. |
| 7 | Audit, operations and tenant onboarding | Supports fraud review and mergers. |

## 4. Implementation Slices

### Slice 1 - Platform Skeleton

| Field | Value |
| --- | --- |
| Goal | Create web app, auction API, realtime gateway and worker boundaries. |
| Related drivers / ADRs | ADR-001, ADR-002, ADR-006 |
| Story/use case | Initial system skeleton. |
| Modules/files expected | web shell, API app, bidding worker, realtime gateway, config module. |
| Acceptance criteria | App/API/gateway start locally; health endpoints work. |
| Minimum tests | API startup test; gateway startup test; web build test. |
| Architecture constraints | Keep video and bidding as separate integration paths. |
| Done when | Later slices can be added without restructuring. |

### Slice 2 - Bidder Registration And Payment Token

| Field | Value |
| --- | --- |
| Goal | Register bidders and store payment-provider token references. |
| Related drivers / ADRs | QA-5, ADR-004 |
| Story/use case | OA-2 Register bidder with credit card. |
| Modules/files expected | bidder model, registration API, payment provider adapter, token storage. |
| Acceptance criteria | Bidder can register with a tokenized card; raw card data is never persisted. |
| Minimum tests | Registration succeeds; raw card fields rejected/not stored; provider failure handled. |
| Architecture constraints | Payment data crosses only provider adapter boundary. |
| Done when | Registered bidder can join an auction with payment token on file. |

### Slice 3 - Auction Catalog And Live Room

| Field | Value |
| --- | --- |
| Goal | Implement auctions, lots and live room entry. |
| Related drivers / ADRs | QA-7, ADR-003, ADR-006 |
| Story/use case | OA-1 Browse auctions, OA-3 Join live auction room, OA-4 Watch live video stream. |
| Modules/files expected | auction catalog, lot model, join endpoint, stream token integration, tenant config. |
| Acceptance criteria | Bidder can find auction, join room and receive event/video connection data. |
| Minimum tests | Browse live auctions; join allowed auction; invalid tenant config rejected. |
| Architecture constraints | Video provider token is issued separately from bid command APIs. |
| Done when | Users can enter a live auction room before bidding is enabled. |

### Slice 4 - Bid Sequencer And Ledger

| Field | Value |
| --- | --- |
| Goal | Implement ordered bid acceptance for online and room bids. |
| Related drivers / ADRs | QA-1, QA-2, QA-6, ADR-001 |
| Story/use case | OA-5 Place online bid, OA-6 Enter live room bid. |
| Modules/files expected | bid command API, clerk live-bid API, sequencer worker, append-only ledger, audit entry writer. |
| Acceptance criteria | Online and room bids for the same auction receive monotonic sequence numbers from one path. |
| Minimum tests | Online bid accepted; room bid accepted; concurrent bids receive ordered sequence; rejected bid is audited. |
| Architecture constraints | No separate persistence path for room bids. |
| Done when | Accepted/rejected bid history can be reconstructed from the ledger. |

### Slice 5 - Real-Time Bid Feed And Video Integration

| Field | Value |
| --- | --- |
| Goal | Publish ordered bid events and display video in the live room. |
| Related drivers / ADRs | QA-1, QA-3, QA-4, ADR-002, ADR-003 |
| Story/use case | OA-4 Watch live video stream, OA-7 Publish bid feed. |
| Modules/files expected | WebSocket event stream, pub/sub consumer, bid feed UI, video player embed, per-auction metrics. |
| Acceptance criteria | Participants receive bid events in sequence order; video failure does not block bidding. |
| Minimum tests | WebSocket receives ordered events; reconnect resumes latest state; video unavailable state shown. |
| Architecture constraints | Clients do not read bid ledger directly for live updates. |
| Done when | Live room shows video and bid feed from separate paths. |

### Slice 6 - Lot Close, Payment Outbox And Reputation

| Field | Value |
| --- | --- |
| Goal | Close lots, charge winners and update reputation. |
| Related drivers / ADRs | QA-5, QA-6, ADR-004, ADR-005 |
| Story/use case | OA-8 Close lot and charge winner, OA-9 Track participant reputation. |
| Modules/files expected | lot close command, winner selection, payment outbox, payment worker, reputation projection. |
| Acceptance criteria | Highest accepted bid wins; charge request is queued; provider result updates reputation and audit trail. |
| Minimum tests | Winner selected by accepted sequence/amount rules; payment queued; provider failure retried; reputation changes recorded. |
| Architecture constraints | Charge call must not run inside the lot-close transaction. |
| Done when | Lot close can be audited through bid, payment and reputation records. |

### Slice 7 - Audit, Operations And Tenant Onboarding

| Field | Value |
| --- | --- |
| Goal | Add dispute review, operational dashboards and auction-house configuration. |
| Related drivers / ADRs | QA-6, QA-7, QA-8, ADR-005, ADR-006 |
| Story/use case | OA-10 Preserve audit trail and onboard acquired auction houses. |
| Modules/files expected | audit query API, operations dashboard, tenant config validation, per-auction alerts. |
| Acceptance criteria | Operator can review ordered bids and payment actions by correlation ID; new auction house config is validated. |
| Minimum tests | Audit reconstruction test; missing correlation ID rejected; invalid tenant config rejected. |
| Architecture constraints | Audit view reads immutable records, not reconstructed mutable state only. |
| Done when | Compliance and operations can inspect live and completed auctions. |

## 5. Code Agent Prompt

```text
Implement only the selected slice from this file.
Use related drivers/ADRs and architecture constraints.
Do not implement unrelated slices.
Run the minimum tests listed for the slice.
```
