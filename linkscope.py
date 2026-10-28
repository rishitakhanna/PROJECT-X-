#!/usr/bin/env python3
"""Build a readable link-health report from fictional rack telemetry.

This portfolio utility deliberately uses only the Python standard library so a
reviewer can clone, run, and inspect the reporting logic without setup work.
"""

from __future__ import annotations

import argparse
import csv
import html
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class LinkSample:
    """One point-in-time summary for a fictional high-speed fabric link."""

    link_id: str
    endpoint_a: str
    endpoint_b: str
    protocol: str
    negotiated_rate_gts: float
    lane_width: int
    corrected_errors: int
    uncorrected_errors: int
    minimum_margin_mv: float
    temperature_c: float
    ber_estimate: float


@dataclass(frozen=True)
class Finding:
    """A customer-readable result with transparent scoring evidence."""

    sample: LinkSample
    status: str
    score: int
    observations: tuple[str, ...]
    next_action: str


def read_samples(path: Path) -> list[LinkSample]:
    """Read and validate the supported CSV shape.

    The raised messages are intentionally specific because data-import failures
    are documentation failures too: users need to know how to recover.
    """
    required = {field.name for field in LinkSample.__dataclass_fields__.values()}
    with path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        fields = set(reader.fieldnames or [])
        missing = sorted(required - fields)
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(missing))
        samples = []
        for line, row in enumerate(reader, start=2):
            try:
                samples.append(
                    LinkSample(
                        link_id=row["link_id"],
                        endpoint_a=row["endpoint_a"],
                        endpoint_b=row["endpoint_b"],
                        protocol=row["protocol"],
                        negotiated_rate_gts=float(row["negotiated_rate_gts"]),
                        lane_width=int(row["lane_width"]),
                        corrected_errors=int(row["corrected_errors"]),
                        uncorrected_errors=int(row["uncorrected_errors"]),
                        minimum_margin_mv=float(row["minimum_margin_mv"]),
                        temperature_c=float(row["temperature_c"]),
                        ber_estimate=float(row["ber_estimate"]),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid value on CSV line {line}: {exc}") from exc
    if not samples:
        raise ValueError("The input CSV has no data rows.")
    return samples


def evaluate(sample: LinkSample) -> Finding:
    """Classify a sample using illustrative, documented thresholds.

    Score starts at 100. Severe uncorrected errors immediately create an
    Investigate status, even if the remaining signal indicators look healthy.
    """
    score = 100
    observations: list[str] = []

    if sample.uncorrected_errors > 0:
        score -= 55
        observations.append(f"{sample.uncorrected_errors} uncorrected error(s) recorded")
    if sample.corrected_errors >= 100:
        score -= 20
        observations.append(f"corrected errors elevated ({sample.corrected_errors})")
    elif sample.corrected_errors > 0:
        score -= 8
        observations.append(f"corrected errors present ({sample.corrected_errors})")
    if sample.minimum_margin_mv < 12:
        score -= 25
        observations.append(f"minimum margin is low ({sample.minimum_margin_mv:.1f} mV)")
    elif sample.minimum_margin_mv < 20:
        score -= 10
        observations.append(f"minimum margin is reduced ({sample.minimum_margin_mv:.1f} mV)")
    if sample.temperature_c >= 85:
        score -= 15
        observations.append(f"temperature is high ({sample.temperature_c:.1f} °C)")
    if sample.ber_estimate > 1e-12:
        score -= 20
        observations.append(f"estimated BER exceeds 1e-12 ({sample.ber_estimate:.1e})")

    score = max(0, score)
    if sample.uncorrected_errors > 0 or score < 65:
        return Finding(
            sample, "Investigate", score, tuple(observations),
            "Capture the link training log, verify seating and cooling, then attach this report to the support case.",
        )
    # A score of 90 means one material indicator crossed its observe limit;
    # reserve Healthy for an entirely clean sample or only minor correction.
    if score <= 90:
        return Finding(
            sample, "Observe", score, tuple(observations),
            "Re-sample after the next workload cycle; compare corrected errors and margin against this baseline.",
        )
    return Finding(sample, "Healthy", score, tuple(observations) or ("no threshold exceptions",), "No action required; retain as a baseline.")


def status_summary(findings: Iterable[Finding]) -> dict[str, int]:
    summary = {"Healthy": 0, "Observe": 0, "Investigate": 0}
    for finding in findings:
        summary[finding.status] += 1
    return summary


def report_markdown(findings: list[Finding]) -> str:
    summary = status_summary(findings)
    lines = [
        "# Link health report",
        "",
        "> Generated from fictional portfolio telemetry. See `docs/reference/telemetry-schema.md` for illustrative scoring limits.",
        "",
        "## Executive summary",
        "",
        f"- **{summary['Healthy']}** healthy link(s)",
        f"- **{summary['Observe']}** link(s) to observe",
        f"- **{summary['Investigate']}** link(s) requiring investigation",
        "",
        "## Findings",
        "",
        "| Link | Path | Protocol | Status | Score | Evidence | Next action |",
        "| --- | --- | --- | --- | ---: | --- | --- |",
    ]
    for item in findings:
        s = item.sample
        evidence = "; ".join(item.observations)
        lines.append(
            f"| {s.link_id} | {s.endpoint_a} → {s.endpoint_b} | {s.protocol} | **{item.status}** | {item.score} | {evidence} | {item.next_action} |"
        )
    lines += [
        "",
        "## Suggested escalation bundle",
        "",
        "For each **Investigate** result, attach this report, the link-training log, a timestamped workload description, and before/after reseat observations. Do not include customer payload data.",
        "",
        "## Interpretation note",
        "",
        "A single sample is a triage signal, not a root-cause diagnosis. Compare repeated samples under equivalent workload and environmental conditions before deciding whether the condition is persistent.",
        "",
    ]
    return "\n".join(lines)


def report_html(findings: list[Finding]) -> str:
    summary = status_summary(findings)
    def esc(value: object) -> str:
        return html.escape(str(value))

    rows = []
    for item in findings:
        s = item.sample
        rows.append(
            "<tr>"
            f"<td>{esc(s.link_id)}</td><td>{esc(s.endpoint_a)} → {esc(s.endpoint_b)}</td>"
            f"<td>{esc(s.protocol)}</td><td><span class='status {item.status.lower()}'>{item.status}</span></td>"
            f"<td>{item.score}</td><td>{esc('; '.join(item.observations))}</td><td>{esc(item.next_action)}</td>"
            "</tr>"
        )
    return f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>LinkScope — Link health report</title>
<style>
  :root {{ color-scheme: light; --ink:#172235; --muted:#617085; --line:#dbe3ed; --accent:#5c39c8; --bg:#f7f9fc; }}
  * {{ box-sizing:border-box }} body {{ margin:0; font:16px/1.55 Inter, ui-sans-serif, system-ui, sans-serif; color:var(--ink); background:var(--bg) }}
  main {{ max-width:1180px; margin:auto; padding:48px 24px 72px }} h1 {{ margin:0; font-size:2.25rem; letter-spacing:-.04em }}
  .eyebrow {{ color:var(--accent); font-weight:700; text-transform:uppercase; letter-spacing:.08em; font-size:.78rem }}
  .lede {{ color:var(--muted); max-width:760px }} .cards {{ display:flex; gap:16px; flex-wrap:wrap; margin:28px 0 }}
  .card {{ min-width:160px; flex:1; background:white; border:1px solid var(--line); border-radius:12px; padding:16px 20px }} .number {{ font-size:2rem; font-weight:750 }}
  section {{ background:white; border:1px solid var(--line); border-radius:12px; padding:24px; margin-top:20px; overflow-x:auto }}
  table {{ width:100%; border-collapse:collapse; min-width:900px }} th,td {{ padding:13px 10px; text-align:left; vertical-align:top; border-bottom:1px solid var(--line) }} th {{ color:var(--muted); font-size:.78rem; text-transform:uppercase; letter-spacing:.04em }}
  .status {{ display:inline-block; font-weight:700; border-radius:999px; padding:2px 9px; font-size:.82rem }} .healthy {{ color:#176d3d; background:#e7f7ed }} .observe {{ color:#925b00; background:#fff3da }} .investigate {{ color:#a82626; background:#ffebeb }}
  footer {{ color:var(--muted); font-size:.88rem; margin-top:24px }}
</style></head><body><main>
<p class=\"eyebrow\">LinkScope · portfolio report</p><h1>Link health report</h1>
<p class=\"lede\">A customer-readable interpretation of fictional high-speed fabric telemetry. Classification thresholds are illustrative and documented in the accompanying reference.</p>
<div class=\"cards\"><div class=\"card\"><div class=\"number\">{summary['Healthy']}</div>Healthy</div><div class=\"card\"><div class=\"number\">{summary['Observe']}</div>Observe</div><div class=\"card\"><div class=\"number\">{summary['Investigate']}</div>Investigate</div></div>
<section><h2>Findings</h2><table><thead><tr><th>Link</th><th>Path</th><th>Protocol</th><th>Status</th><th>Score</th><th>Evidence</th><th>Next action</th></tr></thead><tbody>{''.join(rows)}</tbody></table></section>
<section><h2>Suggested escalation bundle</h2><p>For each <strong>Investigate</strong> result, attach this report, the link-training log, a timestamped workload description, and before/after reseat observations. Do not include customer payload data.</p><h2>Interpretation note</h2><p>A single sample is a triage signal, not a root-cause diagnosis. Compare repeated samples under equivalent workload and environmental conditions before deciding whether the condition is persistent.</p></section>
<footer>Generated by LinkScope from fictional portfolio telemetry. Not associated with or endorsed by any hardware vendor.</footer>
</main></body></html>"""


def build(input_path: Path, output_dir: Path) -> list[Finding]:
    findings = [evaluate(sample) for sample in read_samples(input_path)]
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "link-health-report.md").write_text(report_markdown(findings), encoding="utf-8")
    (output_dir / "link-health-report.html").write_text(report_html(findings), encoding="utf-8")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an explainable link-health report.")
    parser.add_argument("--input", type=Path, required=True, help="CSV telemetry input")
    parser.add_argument("--output", type=Path, required=True, help="Directory for report artifacts")
    args = parser.parse_args()
    findings = build(args.input, args.output)
    print(f"Generated reports for {len(findings)} link(s) in {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
