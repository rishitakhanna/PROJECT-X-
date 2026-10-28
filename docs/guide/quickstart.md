# Quick start: create a link-health report

Use this guide when you have exported a point-in-time, link-level telemetry CSV and need a readable triage report for a lab, validation, or support review.

## Before you begin

- Use Python 3.10 or later.
- Start with the supported CSV fields listed in the [telemetry schema](../reference/telemetry-schema.md).
- Remove payload, credentials, and customer-identifying information before sharing a report.

## 1. Validate the workflow with sample data

From the repository root, run:

```bash
python3 linkscope.py --input samples/link_telemetry.csv --output reports
```

Expected result:

```text
Generated reports for 4 link(s) in reports
```

The command writes two equivalent artifacts:

| Artifact | Use it for |
| --- | --- |
| `reports/link-health-report.md` | pull-request review, issue comments, and version-controlled evidence |
| `reports/link-health-report.html` | sharing a scannable report with a lab or support audience |

## 2. Open and read the report

Start with **Executive summary**, then review any rows marked **Investigate**. Each row intentionally combines a status, the underlying evidence, and the next action so that a reader does not have to interpret raw counters alone.

Do not treat a single sample as root-cause proof. A report is a triage aid. Re-sample during an equivalent workload and compare the trend before escalating a condition as persistent.

## 3. Use your own sanitized CSV

Copy the header from the sample file and replace only the data rows. Run the same command with your new path:

```bash
python3 linkscope.py --input ~/Desktop/sanitized_telemetry.csv --output reports/customer-case-042
```

If a column is missing or a numeric field is malformed, LinkScope stops and identifies the failing input rather than silently producing a misleading result.

## 4. Prepare an escalation bundle

For an **Investigate** result, collect:

1. The generated report.
2. A link-training or initialization log covering the same time window.
3. A short workload description and timestamps.
4. Environmental observations such as cooling changes, cable/connector reseat, or system configuration changes.

Do not attach user data or credential-bearing logs. See [Troubleshooting](troubleshooting.md) for symptom-specific guidance.

## Next steps

- Learn the score’s explicit limits in [Health classification](../reference/telemetry-schema.md#health-classification).
- Review common symptoms in [Troubleshooting](troubleshooting.md).
- Suggest a documentation improvement using the [contribution workflow](../../CONTRIBUTING.md).
