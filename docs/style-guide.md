# LinkScope documentation style guide

## Write for a decision

Each section should help a reader make one decision or complete one task. Lead with what the reader should do, then explain why. Prefer **“Capture the training log before reseating hardware”** to **“Training logs are important.”**

## Use terms consistently

| Preferred term | Do not alternate with | Reason |
| --- | --- | --- |
| link-health report | health dashboard, diagnostic output | Names the published artifact. |
| Observe | warning, amber | Matches a report status. |
| Investigate | critical, error state | Describes the requested human action. |
| corrected error | recoverable error | Matches the input-field name. |
| endpoint | port, device side | Works across topology levels. |

## Keep conditions inspectable

- State units with values: `18.6 mV`, `85 °C`, `1e-12`.
- Put product limits and illustrative limits in tables.
- Flag an exception explicitly; do not bury it in a paragraph.
- Distinguish a measurement, an inference, and an action.

## Make content safe to share

Use fictional or sanitized examples. Do not include customer identifiers, credentials, payloads, unannounced product details, or proprietary register definitions. Add an explicit scope note when a guide is generic.
