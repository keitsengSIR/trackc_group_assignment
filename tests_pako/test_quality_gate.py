"""Tests for the CI gate itself, using isolated synthetic evidence only."""
import json
import tempfile
import unittest
from pathlib import Path
from scripts.pako_quality_gate import evaluate


class QualityGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.policy = self.root / "policy.json"
        self.xml = self.root / "coverage.xml"
        self.mutation = self.root / "mutation.json"
        self.xml.write_text('<coverage line-rate="0.70" branch-rate="0.5"/>', encoding="utf-8")
        self.policy.write_text(json.dumps({"minimum_line_coverage": 50,
                                           "minimum_mutation_score": 60,
                                           "enforce_mutation": False}), encoding="utf-8")

    def test_coverage_passes_without_mutation_enforcement(self):
        good, notes = evaluate(str(self.policy), str(self.xml))
        self.assertTrue(good)
        self.assertTrue(any("NOT YET ENFORCED" in x for x in notes))

    def test_coverage_below_threshold_blocks(self):
        self.xml.write_text('<coverage line-rate="0.49"/>', encoding="utf-8")
        self.assertFalse(evaluate(str(self.policy), str(self.xml))[0])

    def test_missing_mutation_evidence_blocks_when_required(self):
        self.policy.write_text(json.dumps({"minimum_line_coverage": 50,
                                           "minimum_mutation_score": 60,
                                           "enforce_mutation": True}), encoding="utf-8")
        self.assertFalse(evaluate(str(self.policy), str(self.xml))[0])

    def test_stale_commit_blocks_when_mutation_enabled(self):
        self.policy.write_text(json.dumps({"minimum_line_coverage": 50,
                                           "minimum_mutation_score": 60,
                                           "enforce_mutation": True}), encoding="utf-8")
        self.mutation.write_text(json.dumps({"commit_sha": "other", "score": 90,
                                             "tool": "mutmut", "created_at_utc": "2026-10-17T10:00:00Z"}), encoding="utf-8")
        self.assertFalse(evaluate(str(self.policy), str(self.xml), str(self.mutation), "tested")[0])

    def test_mutation_gate_accepts_matching_commit_and_score(self):
        self.policy.write_text(json.dumps({"minimum_line_coverage": 50,
                                           "minimum_mutation_score": 60,
                                           "enforce_mutation": True}), encoding="utf-8")
        self.mutation.write_text(json.dumps({"commit_sha": "tested", "score": 70,
                                             "tool": "mutmut", "created_at_utc": "2026-10-17T10:00:00Z"}), encoding="utf-8")
        self.assertTrue(evaluate(str(self.policy), str(self.xml), str(self.mutation), "tested")[0])


if __name__ == "__main__":
    unittest.main()
