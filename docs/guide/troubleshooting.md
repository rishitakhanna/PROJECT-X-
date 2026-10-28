# Troubleshooting high-speed link-health findings

Use this guide after LinkScope marks a path **Observe** or **Investigate**. The steps are ordered to preserve evidence first and change configuration second.

## Safety and evidence boundaries

- Follow your lab’s electrical-safety, ESD, and maintenance procedures.
- Record timestamps, workload state, and any physical intervention.
- Do not include customer payloads, secrets, or personally identifying information in a case bundle.
- This guide is a generic portfolio example, not a replacement for a vendor’s product documentation or support direction.

## Symptom: uncorrected errors

**Report clue:** Status is **Investigate** and the evidence lists one or more uncorrected errors.

1. Preserve the report and capture the training/initialization log before restarting or reseating hardware.
2. Confirm that the sample window overlaps the reported workload or failure time.
3. Check system event logs for a correlated reset, thermal event, or endpoint availability change.
4. During an approved maintenance window, inspect seating, retention, and cooling. Record any change made.
5. Re-run the same workload and generate a second report with the same observation window.
6. Escalate both reports and the supporting logs if the condition repeats.

**Avoid:** assuming that a single corrected or uncorrected event identifies the failing component. The report is evidence for a structured investigation, not a component-level diagnosis.

## Symptom: corrected errors trend upward

**Report clue:** The report shows `corrected errors present` or `corrected errors elevated` without uncorrected errors.

1. Collect at least one comparable sample after the next workload cycle.
2. Compare counter rate, margin, and temperature—not only the absolute counter total.
3. Check whether a workload, firmware, topology, or environmental change occurred between samples.
4. If the rate rises or other signals degrade, treat the path as an investigation candidate and collect a training log.

## Symptom: low or reduced margin

**Report clue:** Minimum margin is below 20 mV.

1. Confirm the measurement source and the operating condition under which it was captured.
2. Compare the result with a known-good path running under an equivalent workload.
3. Check for concurrent temperature rise or error growth.
4. Capture a repeated sample before and after any approved physical inspection.

## Symptom: high temperature

**Report clue:** Temperature is 85 °C or higher.

1. Verify the temperature sensor location and sample time.
2. Check for fan, airflow, power, or workload changes that overlap the reading.
3. Return the system to its documented thermal operating condition.
4. Re-sample; if temperature remains high or errors appear, attach both the telemetry and environmental observations to the escalation bundle.

## Information to include in a support case

| Include | Why it helps |
| --- | --- |
| Generated report(s) | Shows classification and the exact input-derived evidence. |
| Timestamp and observation window | Makes logs and workload events correlatable. |
| Sanitized training/event logs | Adds state transitions that a summary CSV cannot show. |
| System and topology summary | Gives engineers context without customer payload data. |
| Changes made and re-test results | Prevents duplicate checks and makes the case reproducible. |
