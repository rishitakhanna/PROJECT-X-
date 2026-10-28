# Telemetry schema and health classification

This reference defines the CSV contract consumed by `linkscope.py`. It intentionally separates the interface contract (field names and units) from the task-based procedure in the [quick start](../guide/quickstart.md).

## CSV contract

The input must be UTF-8 CSV with a header row. Each data row is a single link snapshot.

| Field | Type | Unit / allowed value | Description |
| --- | --- | --- | --- |
| `link_id` | string | stable identifier | Identifier displayed in the report. |
| `endpoint_a` | string | sanitized label | First endpoint of the observed path. |
| `endpoint_b` | string | sanitized label | Second endpoint of the observed path. |
| `protocol` | string | descriptive label | Link technology label, for example `PCIe/CXL`. |
| `negotiated_rate_gts` | decimal | GT/s | Negotiated signaling rate at sample time. Stored for traceability. |
| `lane_width` | integer | lane count | Active link width at sample time. Stored for traceability. |
| `corrected_errors` | integer | count | Errors corrected by the link’s applicable mechanism during the sample window. |
| `uncorrected_errors` | integer | count | Errors not corrected during the sample window. |
| `minimum_margin_mv` | decimal | mV | Lowest observed voltage-margin value for the sample. |
| `temperature_c` | decimal | °C | Relevant local temperature measurement. |
| `ber_estimate` | decimal | unitless | Estimated bit-error rate in scientific notation, for example `2.0e-15`. |

### Input rules

- Every field in the table is required.
- Numeric fields must parse as ordinary decimal or scientific-notation values.
- `link_id` should be unique within one report. LinkScope does not merge repeated IDs.
- Counters should use a consistent observation window across all rows; include that window in the case notes outside this CSV.

## Health classification

The limits below are **illustrative portfolio logic**, not product specifications. They are deliberately located in one source file and documented here so a subject-matter expert can review, change, and approve them.

| Signal | Condition | Score adjustment | Reader-facing evidence |
| --- | --- | ---: | --- |
| Uncorrected errors | greater than 0 | −55 | `N uncorrected error(s) recorded` |
| Corrected errors | 1–99 | −8 | `corrected errors present` |
| Corrected errors | 100 or more | −20 | `corrected errors elevated` |
| Minimum margin | below 20 mV | −10 | `minimum margin is reduced` |
| Minimum margin | below 12 mV | −25 | `minimum margin is low` |
| Temperature | 85 °C or higher | −15 | `temperature is high` |
| Estimated BER | above 1e-12 | −20 | `estimated BER exceeds 1e-12` |

The score starts at 100 and is never lower than 0.
For the nested margin conditions, only the most severe matching row applies; a
10.8 mV value receives the −25 adjustment, not both adjustments.

| Status | Rule | Intended response |
| --- | --- | --- |
| Healthy | score 91–100, no uncorrected errors | Retain as a baseline. |
| Observe | score 65–90, no uncorrected errors | Re-sample after the next workload cycle and compare trend. |
| Investigate | score below 65 **or** one or more uncorrected errors | Capture supporting evidence and follow the troubleshooting flow. |

An uncorrected error always produces **Investigate**, even when the computed score might otherwise be higher. This makes the safety-critical exception obvious to a reviewer.

## Output contract

The generator creates both a Markdown and a self-contained HTML report. Both contain the same findings in this order:

1. Status summary
2. Per-link findings: path, status, score, evidence, next action
3. Escalation bundle
4. Interpretation note

The HTML is intentionally dependency-free and can be attached to a ticket or opened locally. It uses no external analytics, fonts, or network requests.
