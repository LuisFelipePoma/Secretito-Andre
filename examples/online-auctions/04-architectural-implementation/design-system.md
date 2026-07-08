# Online Auctions - Design System

## 1. Product / UI Principles

- Live-auction UI for bidders, clerks and operations.
- Current lot, current bid, bidder eligibility and connection state must be immediately visible.
- Bid actions must be fast, explicit and hard to trigger accidentally.
- Clerk views optimize for rapid room-bid entry and correction visibility.
- Audit and operations views optimize for scanability and incident response.

## 2. Design Tokens

| Token | Value | Usage |
| --- | --- | --- |
| `space-1` | 4px | Compact labels and feed metadata. |
| `space-2` | 8px | Default gap. |
| `space-3` | 12px | Bid controls and form fields. |
| `space-4` | 16px | Panels and live-room sections. |
| `radius-sm` | 4px | Inputs/buttons. |
| `radius-md` | 8px | Panels/cards max radius. |

## 3. Color Palette

| Role | Value | Usage |
| --- | --- | --- |
| Primary | `#0F766E` | Main bid and join actions. |
| Accent | `#C2410C` | Current winning bid and live state. |
| Surface | `#F7F7F4` | App background. |
| Panel | `#FFFFFF` | Live room panels and forms. |
| Border | `#D6D3C8` | Field, table and feed separators. |
| Success | `#15803D` | Accepted bid, paid state. |
| Warning | `#B45309` | Pending charge, stream delay or reputation warning. |
| Danger | `#B42318` | Rejected bid, payment failure or disconnected state. |

## 4. Typography

| Role | Size | Weight | Usage |
| --- | --- | --- | --- |
| Page title | 24px | 600 | Auction or operations page header. |
| Lot title | 20px | 600 | Current lot name. |
| Current bid | 28px | 700 | Live current price. |
| Body | 14px | 400 | Forms, lists and feed rows. |
| Caption | 12px | 400 | Bid metadata, sequence and timestamps. |

## 5. Spacing / Radius / Elevation

- Use compact spacing in live rooms and operations dashboards.
- Keep cards and panels at max 8px radius.
- Prefer bordered panels over heavy shadows.
- Reserve high-contrast emphasis for current bid, bid status and connection/payment errors.

## 6. Component Rules

- Buttons: primary for bid/join; secondary for watchlist and navigation; danger for irreversible clerk/admin actions.
- Bid control: fixed-size amount display, increment controls and explicit confirm action.
- Bid feed: show sequence, amount, source, status and timestamp.
- Clerk entry: support fast room-bid amount entry with visible accepted/rejected result.
- Reputation: show score and eligibility state near bidder identity.
- Connection state: always show realtime and video status separately.

## 7. Form Patterns

- Registration forms require bidder identity, payment token status and terms acknowledgement.
- Bid confirmations show amount, lot and bidder before submit.
- Rejected bid errors must explain stale amount, closed lot or eligibility issue.
- Payment failures must show retry/pending state without exposing card data.

## 8. Table / List Patterns

- Auction list supports status, category, start time and auction house filters.
- Bid feed is append-first with newest accepted bid easy to identify.
- Operations tables show auction, participant count, bid latency, stream state and payment failures.
- Audit tables support correlation ID, lot, bidder, source, sequence and action filters.

## 9. Feedback States

- Loading: skeleton auction rows and bid feed rows.
- Live: visible live indicator with last event time.
- Success: accepted bid and payment charged.
- Warning: stream delay, payment pending or reputation caution.
- Error: disconnected, bid rejected, lot closed or payment failed.

## 10. Accessibility Rules

- Bid controls must be keyboard accessible and screen-reader labeled.
- Bid status cannot rely on color only.
- Video controls must expose captions/support provider accessibility when available.
- Focus order follows live room: lot, current bid, bid controls, feed, video.

## 11. Responsive Behavior

- Desktop: video, current lot and bid feed visible in one live-room layout.
- Tablet: video above bid/feed columns.
- Mobile: current bid and bid action remain visible above scrollable feed/video.

## 12. Icon / Library Policy

- Use existing icon set if present.
- Do not add component libraries without approval.
- Prefer standard icons for live, bid, clock, card, user, warning, success and disconnect states.
