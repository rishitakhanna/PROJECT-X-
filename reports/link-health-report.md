# Link health report

> Generated from fictional portfolio telemetry. See `docs/reference/telemetry-schema.md` for illustrative scoring limits.

## Executive summary

- **1** healthy link(s)
- **1** link(s) to observe
- **2** link(s) requiring investigation

## Findings

| Link | Path | Protocol | Status | Score | Evidence | Next action |
| --- | --- | --- | --- | ---: | --- | --- |
| FAB-01 | Accelerator-01 → Switch-01 | PCIe/CXL | **Healthy** | 100 | no threshold exceptions | No action required; retain as a baseline. |
| FAB-02 | Accelerator-02 → Switch-01 | PCIe/CXL | **Observe** | 82 | corrected errors present (14); minimum margin is reduced (18.6 mV) | Re-sample after the next workload cycle; compare corrected errors and margin against this baseline. |
| FAB-03 | Accelerator-03 → Switch-02 | PCIe/CXL | **Investigate** | 35 | corrected errors elevated (184); minimum margin is low (10.8 mV); estimated BER exceeds 1e-12 (3.0e-12) | Capture the link training log, verify seating and cooling, then attach this report to the support case. |
| FAB-04 | Accelerator-04 → Switch-02 | PCIe/CXL | **Investigate** | 22 | 1 uncorrected error(s) recorded; corrected errors present (7); temperature is high (87.3 °C) | Capture the link training log, verify seating and cooling, then attach this report to the support case. |

## Suggested escalation bundle

For each **Investigate** result, attach this report, the link-training log, a timestamped workload description, and before/after reseat observations. Do not include customer payload data.

## Interpretation note

A single sample is a triage signal, not a root-cause diagnosis. Compare repeated samples under equivalent workload and environmental conditions before deciding whether the condition is persistent.
