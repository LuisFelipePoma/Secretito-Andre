# Online Auctions - ADD Design Decisions

## Selected Concepts

| Driver | Selected concept | Why | Discarded alternatives |
| --- | --- | --- | --- |
| QA-2, QA-6 | Per-auction bid sequencer with append-only ledger. | Gives one ordered source of truth for online and room bids. | Client timestamps; separate online/live bid stores. |
| QA-1, QA-3 | WebSocket gateway with pub/sub fanout by auction. | Pushes bid updates quickly and scales readers away from command processing. | Polling; direct DB reads by clients. |
| QA-1, QA-4 | Managed video streaming/CDN outside the bid command path. | Keeps video bandwidth and failures from affecting bid ordering. | Self-hosted video in bidding service. |
| QA-5 | Tokenized payment provider with payment outbox. | Avoids raw card storage and keeps charge retries auditable. | Store cards directly; synchronous charge inside lot-close transaction. |
| QA-6, CON-5 | Immutable audit records with correlation IDs. | Supports fraud investigation and dispute reconstruction. | Mutable bid status table only. |
| QA-7, CON-6 | Tenant and auction-house configuration boundary. | Supports mergers without changing bidding core. | Hard-coded auction-house behavior. |

## ADD Analysis

| Driver | Result | Evidence | Next action |
| --- | --- | --- | --- |
| QA-2 | Satisfied for design | Single sequencer per auction assigns monotonic sequence numbers. | Define sequence conflict and failover rules. |
| QA-1 | Partially satisfied | WebSocket fanout and short bid path selected. | Validate latency under load test. |
| QA-3 | Partially satisfied | Partitioning by auction and fanout support horizontal scale. | Define active-auction capacity targets. |
| QA-6 | Satisfied for design | Append-only ledger and audit records selected. | Define retention and access policy. |
| QA-5 | Satisfied for design | Tokenization and payment outbox selected. | Confirm provider and PCI scope. |
| QA-7 | Partially satisfied | Tenant configuration boundary selected. | Define onboarding configuration model. |
