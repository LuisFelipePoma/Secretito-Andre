# Phase 1 Input - Architectural Requirements

Human-prepared minimum briefing. The architect prepares or validates this file; the agent uses it with `project-brief.md` to generate `architecture-drivers.md`.

## Source

- `examples/online-auctions/input/project-brief.md`

## Input

| Item | Value |
| --- | --- |
| Business problem | Take room-based auctions online nationwide while preserving live-auction rhythm and trust. |
| Objective | Create a web platform for live video, real-time bids, ordered bid acceptance, automatic winner charging and reputation tracking. |
| Scope/MVP | Auction discovery, bidder registration, credit card token, live room, online bids, live bid entry, bid feed, winner charge, reputation and audit trail. |
| Stakeholders | Online bidders, auctioneers, clerks, operations, finance, compliance/legal and acquired auction houses. |
| Main functions | OA-1 through OA-10. |
| Expected quality attributes | Low latency, ordering/consistency, scalability, availability, security/compliance, auditability, modifiability and observability. |
| Constraints | Browser UI, tokenized payments, nationwide scale, unconstrained budget, fraud lawsuit context and competitor mergers. |
| External systems | Payment provider, live video streaming/CDN and monitoring stack. |
| Customer priorities | Ordered bid acceptance, low-latency bid updates, scale, auditability and reliable winner charging. |
