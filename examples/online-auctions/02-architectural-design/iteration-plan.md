# Online Auctions - Architectural Design

| Iteration | Goal | Drivers | Elements to refine |
| --- | --- | --- | --- |
| 1 | Establish auction platform structure. | CON-4, CON-6, QA-7 | Web app, auction API, tenants, catalog, identity and payments. |
| 2 | Preserve bid order. | QA-2, OA-5, OA-6, QA-6 | Bid command path, per-auction sequencer, bid ledger and audit records. |
| 3 | Make live updates scale. | QA-1, QA-3, OA-7 | WebSocket gateway, pub/sub fanout, bid read model and active auction partitioning. |
| 4 | Keep video separate from bidding. | QA-1, QA-4, OA-4 | Managed streaming provider, stream tokens and auction-room UI. |
| 5 | Close lots safely. | QA-5, OA-8, OA-9 | Winner detection, payment outbox, reputation updates and failure handling. |

## Execution Summary

| Iteration | Result |
| --- | --- |
| 1 | Use a service-oriented platform with auction, bidding, payment, reputation and operations boundaries. |
| 2 | Route online and room bids through a single per-auction sequencer and append-only ledger. |
| 3 | Use WebSocket gateway and pub/sub fanout for bid updates. |
| 4 | Use managed video streaming/CDN so video failures do not block bids. |
| 5 | Use tokenized payment workflow, outbox and reputation projection after lot close. |
