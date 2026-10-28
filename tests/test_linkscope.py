import tempfile
import unittest
from pathlib import Path

from linkscope import LinkSample, build, evaluate, read_samples


class LinkScopeTests(unittest.TestCase):
    def sample(self, **overrides):
        values = dict(
            link_id="L-1", endpoint_a="A", endpoint_b="B", protocol="PCIe/CXL",
            negotiated_rate_gts=64.0, lane_width=16, corrected_errors=0,
            uncorrected_errors=0, minimum_margin_mv=30.0, temperature_c=65.0,
            ber_estimate=1e-15,
        )
        values.update(overrides)
        return LinkSample(**values)

    def test_nominal_link_is_healthy(self):
        result = evaluate(self.sample())
        self.assertEqual((result.status, result.score), ("Healthy", 100))

    def test_uncorrected_error_requires_investigation(self):
        result = evaluate(self.sample(uncorrected_errors=1))
        self.assertEqual(result.status, "Investigate")
        self.assertLess(result.score, 65)

    def test_reduced_margin_is_observed(self):
        result = evaluate(self.sample(minimum_margin_mv=18.0))
        self.assertEqual(result.status, "Observe")

    def test_build_writes_both_publication_formats(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "reports"
            findings = build(root / "samples/link_telemetry.csv", output)
            self.assertEqual(len(findings), 4)
            self.assertIn("Investigate", (output / "link-health-report.md").read_text())
            self.assertIn("Link health report", (output / "link-health-report.html").read_text())

    def test_missing_columns_explains_the_problem(self):
        with tempfile.TemporaryDirectory() as temporary:
            bad_file = Path(temporary) / "bad.csv"
            bad_file.write_text("link_id\nL-1\n")
            with self.assertRaisesRegex(ValueError, "Missing required columns"):
                read_samples(bad_file)


if __name__ == "__main__":
    unittest.main()
