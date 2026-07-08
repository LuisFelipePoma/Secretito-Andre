# Phase 2 Input - Architectural Design

## Source

- `examples/online-auctions/01-architectural-requirements/architecture-drivers.md`

## Approved Drivers

| Driver | Priority |
| --- | --- |
| QA-2 Ordering/consistency | Primary |
| QA-1 Low latency | Primary |
| QA-6 Auditability | Primary |
| QA-3 Scalability | Primary |
| QA-5 Security/compliance | Supporting |
| QA-4 Availability | Supporting |
| QA-7 Modifiability | Supporting |
| QA-8 Observability | Supporting |

## Constraints And Risks

- Online and live room bids must enter the same ordered command path.
- Bid feed latency is critical, but the video stream must not block bidding.
- Fraud history requires immutable audit records, not mutable status-only rows.
- Participant and payment data must stay out of the browser trust boundary.
- Acquired auction houses need configuration boundaries without changing the bid ordering core.

## Allowed Design Catalog

- Per-auction bid sequencer.
- Append-only bid ledger.
- WebSocket real-time gateway with pub/sub fanout.
- Managed video streaming/CDN provider.
- Tokenized payment provider and payment outbox.
- Reputation read model.
- Tenant and auction-house configuration.
- Metrics/logging/tracing with audit correlation IDs.
