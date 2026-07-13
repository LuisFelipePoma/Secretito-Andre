# Online Auctions - Project Brief

## 1. Business Problem

An auction company wants to move room-based auctions online at nationwide scale. Customers need to choose an auction, wait until it begins, watch the auctioneer, and bid as if they are physically in the room.

The company is expanding aggressively by merging with smaller competitors. It also recently settled a lawsuit alleging fraud, so the online platform must make bid handling transparent and auditable.

## 2. System Goal

Create a web auction platform that supports live video, real-time bid updates, online and room bids in the same ordered flow, automatic winner charging, participant reputation, and operational growth across many auction houses.

## 3. Initial Scope / MVP

Included:

- Auction discovery and registration.
- Bidder registration with tokenized credit card.
- Live auction room with video stream and bid feed.
- Online bid placement.
- Live room bid entry by auction staff.
- Ordered bid processing for online and live bids.
- Winner detection and automatic payment charge.
- Participant reputation index.
- Auditable bid and payment history.

Out of initial scope:

- Native mobile apps.
- In-house video encoding platform.
- Custom payment gateway.
- Full migration tooling for every acquired competitor.

## 4. Stakeholders

| Stakeholder | Interest |
| --- | --- |
| Online bidders | Watch auctions and place bids with minimal delay. |
| Auctioneers | Run auctions without losing room rhythm. |
| Auction clerks | Enter room bids accurately and quickly. |
| Auction operations | Monitor live auctions and resolve disputes. |
| Finance | Charge winning bidders reliably. |
| Compliance/legal | Prove bid order, bidder identity and payment actions. |
| Acquired auction houses | Onboard auctions, catalogs and staff practices. |

## 5. Main Features

- REQ-001: Browse and choose auctions.
- REQ-002: Register bidder with credit card.
- REQ-003: Join live auction room.
- REQ-004: Watch live video stream.
- REQ-005: Place online bid.
- REQ-006: Enter live room bid.
- REQ-007: Publish bid feed to participants.
- REQ-008: Close lot, detect winner and charge card.
- REQ-009: Track participant reputation.
- REQ-010: Preserve audit trail for bid and payment activity.

## 6. Expected Quality Attributes

- Low latency: auctions must feel as real-time as possible.
- Ordering/consistency: online and room bids must be accepted in placement order.
- Scalability: hundreds to thousands of participants per auction and many simultaneous auctions.
- Availability: live bidding must remain available during active auctions.
- Security/compliance: protect payment and participant data.
- Auditability: bid history must support dispute and fraud investigation.
- Modifiability: support onboarding acquired auction houses.
- Observability: operators must see live auction health and bid/payment failures.

## 7. Constraints

- Browser-based participant experience.
- Credit cards must be tokenized through an external payment provider.
- Budget is not constrained; this is a strategic direction.
- The platform must support nationwide scale.
- Fraud lawsuit history raises audit and compliance priority.
- Acquired competitors may have different catalog and operating practices.

## 8. Current Context

Existing auctions are run in physical rooms with auctioneers and live bidders. The online platform must integrate staff-entered room bids with online bids and keep all participants seeing the same bid state.

## 9. Environments And Operations

- Development: local and shared integration environments.
- QA: load-test environment with simulated auctions and bidders.
- Staging: production-like streaming, payment sandbox and auction operations rehearsal.
- Production: monitored live auction environment with incident response during auctions.

## 10. Customer Priorities

Highest priority:

- Preserve ordered bid acceptance across online and room participants.
- Keep bid updates low-latency.
- Scale active auctions without blocking growth.
- Prove bid and payment history after disputes.
- Charge winning bidders reliably.

## 11. Risk, Rigor And System Context

Rigor profile: Standard. System context: Integration. Real-time ordering, disputed transactions, nationwide fanout, payment integration, and high incident cost require explicit audit, recovery, and capacity evidence.

## 12. Data, Security And Recovery

Payment tokens and bidder identity are confidential; bid order is integrity-critical. Trust boundaries include clients, live-room staff, payment, and streaming providers. Sequencer recovery and rollback must preserve the append-only ledger.

## 13. Assumptions And Open Questions

Managed video and payment providers can satisfy regional needs. Retention, dispute, and sequencer failover rules require explicit review.
