"""Tests for skills/tax-audit/scripts/ca_cross_check.py (synthetic inputs only)."""
import json
import os
import random
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "skills", "tax-audit", "scripts", "ca_cross_check.py")
CALC_DIR = os.path.join(ROOT, "skills", "tax-cheatsheet", "scripts")
sys.path.insert(0, os.path.dirname(CHECK))
sys.path.insert(0, CALC_DIR)
import ca_cross_check as cc  # noqa: E402
import ca_540nr as calc  # noqa: E402

INPUTS = {
    "filing_status": "MFJ",
    "federal_agi": 180000,
    "rows": [
        {"id": "w-a", "kind": "income", "federal": 120000, "resident": 120000},
        {"id": "w-b", "kind": "income", "federal": 60000, "resident": 30000},
    ],
    "payments": {"line81": 9000},
}
# Hand-calculated values (see test_ca_540nr.py)
FILED = {"line13": 180000, "line17": 180000, "line19": 168588, "line31": 8556,
         "line35": 140490, "line36": "0.0508", "line37": 7137, "line38": "0.8333",
         "line39": 255, "line40": 6882, "line74": 6882, "line88": 9000,
         "line101_overpaid": 2118, "line104_tax_due": 0, "line81": 9000, "line12": 180000}


class CrossCheckTests(unittest.TestCase):
    def test_hand_values_pass(self):
        r = cc.check({"inputs": INPUTS, "filed": FILED})
        self.assertEqual(r["verdict"], "READY TO FILE", r)
        self.assertTrue(all(c["status"] in ("MATCH", "SKIPPED") for c in r["line_checks"]))
        self.assertTrue(r["unverified_items"])

    def test_mixed_scenario_hand_values_pass(self):
        # Rental add-back, IRA and gain rows; hand values in test_ca_540nr.MixedScenarioTests
        inputs = {
            "filing_status": "MFJ", "federal_agi": 161000,
            "rows": [
                {"id": "w-a", "kind": "income", "federal": 100000, "resident": 100000},
                {"id": "w-b", "kind": "income", "federal": 50000, "resident": 20000},
                {"id": "rental", "kind": "income", "federal": -6000, "addition": 10000, "resident": 2000},
                {"id": "ira", "kind": "income", "federal": 9000, "resident": 3000},
                {"id": "gain", "kind": "income", "federal": 8000, "resident": 5000},
            ],
        }
        filed = {"line13": 161000, "line16": 10000, "line17": 171000, "line19": 159588,
                 "line31": 7719, "line35": 121325, "line36": "0.0484", "line37": 5872,
                 "line38": "0.7602", "line39": 233, "line40": 5639, "line74": 5639}
        r = cc.check({"inputs": inputs, "filed": filed})
        self.assertEqual(r["verdict"], "READY TO FILE", r)

    def test_isr_penalty_agrees_with_calculator(self):
        inputs = dict(INPUTS, payments={"line81": 9000, "line91": 750})
        res = calc.calculate(inputs)["form_540nr"]
        filed = dict(FILED, line101_overpaid=int(res["line101_overpaid"]),
                     line104_tax_due=int(res["line104_tax_due"]), line88=9000)
        r = cc.check({"inputs": inputs, "filed": filed})
        self.assertNotIn("STOP", r["verdict"], r)

    def test_wrong_tax_stops(self):
        filed = dict(FILED, line74=6000, line40=6000)
        r = cc.check({"inputs": INPUTS, "filed": filed})
        self.assertEqual(r["verdict"], "STOP")

    def test_one_dollar_is_rounding(self):
        filed = dict(FILED, line37=7138)
        r = cc.check({"inputs": INPUTS, "filed": filed})
        row = [c for c in r["line_checks"] if c["line"] == "line37"][0]
        self.assertEqual(row["status"], "ROUNDING")

    def test_document_checks(self):
        docs = {"w2_ca_withholding": 9000, "w2_box16_wages": 179000, "w2_sdi": 1000}
        r = cc.check({"inputs": INPUTS, "filed": FILED, "documents": docs})
        by = {d["check"]: d for d in r["document_checks"]}
        self.assertEqual(by["line81 vs W-2 box 17 total"]["status"], "MATCH")
        self.assertEqual(by["line12 vs W-2 box 16 total"]["status"], "DIFFERENT")
        self.assertEqual(r["verdict"], "REVIEW THESE ITEMS")

    def test_state_refund_check(self):
        inp = json.loads(json.dumps(INPUTS))
        inp["rows"].append({"id": "state_refund", "kind": "income", "federal": 500, "subtraction": 500, "resident": 0})
        inp["federal_agi"] = 180500
        filed = dict(FILED, line13=180500)
        r = cc.check({"inputs": inp, "filed": filed, "documents": {"state_refund_1099g": 500}})
        self.assertEqual(r["document_checks"][0]["status"], "MATCH")

    def test_errors(self):
        self.assertIn("error", cc.check({}))
        self.assertIn("error", cc.check({"inputs": INPUTS}))
        self.assertIn("error", cc.check({"inputs": dict(INPUTS, filing_status="ZZ"), "filed": FILED}))

    def test_independent_implementation_agrees_with_calculator(self):
        # Randomised agreement on synthetic returns. Above ~$370,000 the FTB's printed base
        # amounts are rounded to cents, so line 31 can differ by $1 between the two methods.
        rng = random.Random(7)
        for _ in range(400):
            status = rng.choice(list(calc.STATUS))
            wages = rng.randint(0, 400000)
            resident = rng.randint(0, wages)
            inp = {"filing_status": status, "federal_agi": wages,
                   "rows": [{"id": "w", "kind": "income", "federal": wages, "resident": resident}],
                   "exemptions": {"senior": rng.randint(0, 2), "dependents": rng.randint(0, 3)}}
            mine = cc.recompute(inp)
            theirs = calc.calculate(inp)["form_540nr"]
            for line, val in mine.items():
                self.assertLessEqual(abs(int(theirs[line]) - val) if line not in ("line36", "line38")
                                     else abs(float(theirs[line]) - float(val)), 1 if line not in ("line36", "line38") else 0.0002,
                                     (status, wages, line))

    def test_cli(self):
        out = subprocess.run([sys.executable, "-I", CHECK, json.dumps({"inputs": INPUTS, "filed": FILED})],
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(json.loads(out.stdout)["verdict"], "READY TO FILE")


if __name__ == "__main__":
    unittest.main()
