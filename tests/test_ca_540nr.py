"""Tests for skills/tax-cheatsheet/scripts/ca_540nr.py (synthetic inputs only)."""
import json
import os
import re
import shutil
import subprocess
import sys
import unittest
from decimal import Decimal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "skills", "tax-cheatsheet", "scripts", "ca_540nr.py")
sys.path.insert(0, os.path.dirname(SCRIPT))
import ca_540nr as ca  # noqa: E402

BOOKLET_PDF = os.path.join(ROOT, "reference", "curated", "ca", "2025-540nr-booklet.pdf")


def part_year_case(**over):
    data = {
        "filing_status": "MFJ",
        "federal_agi": 180000,
        "rows": [
            {"id": "w-a", "kind": "income", "federal": 120000, "resident": 120000},
            {"id": "w-b", "kind": "income", "federal": 60000,
             "resident": 30000, "nonresident_ca_source": 0},
        ],
        "payments": {"line81": 9000},
    }
    data.update(over)
    return data


class RateScheduleTests(unittest.TestCase):
    def test_ftb_printed_example(self):
        # FTB example: Schedule Y, $125,000 -> $4,768.10 -> $4,768
        self.assertEqual(ca.schedule_tax(Decimal("125000"), "Y"), Decimal("4768.10"))
        self.assertEqual(ca.california_tax(Decimal("125000"), "Y"), Decimal("4768"))

    def test_bracket_base_amounts_are_continuous(self):
        for name, brackets in ca.SCHEDULES.items():
            for (f0, b0, r0), (f1, b1, _) in zip(brackets, brackets[1:]):
                expected = Decimal(b0) + Decimal(r0) * (Decimal(f1) - Decimal(f0))
                self.assertAlmostEqual(float(expected), float(Decimal(b1)), delta=0.02,
                                       msg=f"schedule {name} at {f1}")

    def test_hand_checked_over_100k(self):
        # Schedule X: 72,724 base 3,201.97 + 9.3% x (200,000 - 72,724) = 15,038.65
        self.assertEqual(ca.california_tax(Decimal("200000"), "X"), Decimal("15039"))
        # Schedule Z top bracket: 97,472.91 + 12.3% x 100,000 = 109,772.91
        self.assertEqual(ca.california_tax(Decimal("1110417"), "Z"), Decimal("109773"))


class TaxTableTests(unittest.TestCase):
    def test_printed_rows(self):
        # (income, Single, MFJ, HoH) from the printed 2025 table
        for inc, s, j, h in [(13000, 149, 130, 130), (6500, 65, 65, 65),
                             (45800, 1283, 694, 694), (100000, 5736, 3068, 3708)]:
            income = Decimal(inc)
            self.assertEqual(ca.california_tax(income, "X"), s, inc)
            self.assertEqual(ca.california_tax(income, "Y"), j, inc)
            self.assertEqual(ca.california_tax(income, "Z"), h, inc)

    def test_zero_and_tiny_income(self):
        self.assertEqual(ca.california_tax(Decimal("0"), "X"), 0)
        self.assertEqual(ca.california_tax(Decimal("50"), "X"), 0)
        self.assertEqual(ca.california_tax(Decimal("51"), "X"), 1)

    @unittest.skipUnless(shutil.which("pdftotext") and os.path.exists(BOOKLET_PDF),
                         "needs pdftotext and the gitignored FTB booklet PDF")
    def test_every_printed_row(self):
        text = subprocess.run(["pdftotext", "-layout", BOOKLET_PDF, "-"],
                              capture_output=True, text=True,
                              encoding="utf-8", errors="replace").stdout.splitlines()
        start = [i for i, l in enumerate(text) if l.strip() == "2025 California Tax Table"][0]
        rows = set()
        for line in text[start:]:
            nums = re.findall(r"\d+", re.split(r"[A-Za-z]", line)[0].replace("$", "").replace(",", ""))
            if len(nums) >= 5 and len(nums) % 5 == 0:
                for k in range(0, len(nums), 5):
                    row = tuple(map(int, nums[k:k + 5]))
                    if row[1] - row[0] in (49, 99) and (row[0] in (1, 99951) or (row[0] - 51) % 100 == 0):
                        rows.add(row)
        if len(rows) != 1001:
            self.skipTest(f"pdftotext read {len(rows)} of 1001 Tax Table rows; this version splits table cells across lines (use a newer poppler)")
        for lo, hi, s, j, h in rows:
            for sched, want in (("X", s), ("Y", j), ("Z", h)):
                self.assertEqual(ca.california_tax(Decimal(hi), sched), want, (lo, hi, sched))


class FormCalculationTests(unittest.TestCase):
    def test_part_year_mfj_hand_calculation(self):
        # Hand calculation:
        #  line 19 = 180,000 - 11,412 = 168,588; Schedule Y tax = 6,403.94 + 9.3% x 23,140 = 8,555.96 -> 8,556
        #  rate = 8,556 / 168,588 = 0.0508; column E / D = 150,000 / 180,000 = 0.8333
        #  deduction = 11,412 x 0.8333 = 9,510; line 35 = 140,490; line 37 = 7,137
        #  exemption = 306 x 0.8333 = 255; line 40 = 6,882; refund = 9,000 - 6,882
        f = ca.calculate(part_year_case())["form_540nr"]
        self.assertEqual(f["line19"], "168588")
        self.assertEqual(f["line31"], "8556")
        self.assertEqual(f["line36"], "0.0508")
        self.assertEqual(f["line35"], "140490")
        self.assertEqual(f["line37"], "7137")
        self.assertEqual(f["line38"], "0.8333")
        self.assertEqual(f["line39"], "255")
        self.assertEqual(f["line74"], "6882")
        self.assertEqual(f["line101_overpaid"], "2118")
        self.assertEqual(f["line104_tax_due"], "0")

    def test_full_year_resident_uses_full_amounts(self):
        data = part_year_case()
        data["rows"][1].update(resident=60000)
        r = ca.calculate(data)
        self.assertEqual(r["schedule_ca"]["part_iv_line3_deduction_percentage"], "1.0000")
        self.assertEqual(r["form_540nr"]["line35"], "168588")
        self.assertEqual(r["form_540nr"]["line38"], "1.0000")
        self.assertEqual(r["form_540nr"]["line39"], "306")
        # line 37 = 168,588 x 0.0508 (rate rounded to 4 places, per the form) = 8,564; less 306 = 8,258
        self.assertEqual(r["form_540nr"]["line37"], "8564")
        self.assertEqual(r["form_540nr"]["line74"], "8258")

    def test_table_method_used_at_or_below_100k(self):
        r = ca.calculate({"filing_status": "Single", "federal_agi": 60000,
                          "rows": [{"id": "w", "kind": "income", "federal": 60000, "resident": 60000}]})
        self.assertEqual(r["tax_method"], "Tax Table")
        # taxable 54,294 -> range 54,251-54,350 midpoint 54,300
        # 1,022.01 + 6% x (54,300 - 41,452) = 1,792.89 -> 1,793
        # rate = 1,793 / 54,294 = 0.0330; line 37 = 54,294 x 0.0330 = 1,791.7 -> 1,792; less 153 = 1,639
        self.assertEqual(r["form_540nr"]["line31"], "1793")
        self.assertEqual(r["form_540nr"]["line36"], "0.0330")
        self.assertEqual(r["form_540nr"]["line74"], "1639")

    def test_agi_limitation_worksheet(self):
        # MFJ AGI 600,000: excess 95,589 / 2,500 -> 39 steps; 39 x 6 = 234 per box; 2 boxes -> 306 - 468 -> 0
        r = ca.calculate({"filing_status": "MFJ", "federal_agi": 600000,
                          "rows": [{"id": "w", "kind": "income", "federal": 600000, "resident": 600000}]})
        self.assertEqual(r["form_540nr"]["line39"], "0")
        self.assertIn("AGI Limitation", " ".join(r["notes"]))

    def test_dependents_and_senior(self):
        r = ca.calculate(part_year_case(exemptions={"senior": 1, "dependents": 2}))
        self.assertEqual(r["form_540nr"]["line11"], str(306 + 153 + 950))

    def test_behavioral_health_services_tax(self):
        r = ca.calculate({"filing_status": "Single", "federal_agi": 1200000,
                          "rows": [{"id": "w", "kind": "income", "federal": 1200000, "resident": 1200000}]})
        # line 35 = 1,200,000 - 5,706 = 1,194,294 -> 1% x 194,294 = 1,943
        self.assertEqual(r["form_540nr"]["line72"], "1943")

    def test_subtraction_and_negative_column_moves(self):
        data = part_year_case()
        data["rows"].append({"id": "refund", "kind": "income", "federal": 1000,
                             "subtraction": 1000, "resident": 0})
        data["federal_agi"] = 181000
        f = ca.calculate(data)["form_540nr"]
        self.assertEqual(f["line14"], "1000")
        self.assertEqual(f["line17"], "180000")

    def test_scenario_dollar_effect(self):
        data = part_year_case(scenarios=[{"label": "half of pre-move wages", "rows": {"w-b": {"nonresident_ca_source": 15000}}}])
        r = ca.calculate(data)
        self.assertEqual(len(r["scenarios"]), 1)
        self.assertGreater(Decimal(r["scenarios"][0]["change_in_total_tax"]), 0)

    def test_errors(self):
        self.assertIn("error", ca.calculate({"filing_status": "XX", "federal_agi": 1, "rows": [{}]}))
        self.assertIn("federal_agi", ca.calculate({"filing_status": "MFJ", "rows": [{}]})["error"])
        bad = part_year_case()
        bad["rows"][0]["kind"] = "oops"
        self.assertIn("kind", ca.calculate(bad)["error"])


class MixedScenarioTests(unittest.TestCase):
    """Synthetic MFJ return covering part-year wages, a rental row with a bonus
    depreciation add-back, a retirement row and a gain, each split by period."""

    CASE = {
        "filing_status": "MFJ",
        "federal_agi": 161000,
        "rows": [
            {"id": "w-a", "kind": "income", "federal": 100000, "resident": 100000},
            {"id": "w-b", "kind": "income", "federal": 50000, "resident": 20000},
            # federal loss after bonus depreciation; add-back makes column D +4,000
            {"id": "rental", "kind": "income", "federal": -6000, "addition": 10000,
             "resident": 2000},
            {"id": "ira", "kind": "income", "federal": 9000, "resident": 3000},
            {"id": "gain", "kind": "income", "federal": 8000, "resident": 5000},
        ],
    }

    def test_hand_calculation(self):
        # Hand calculation (Decimal, independent of the script):
        #  D = 161,000 + 10,000 = 171,000; E = 100,000+20,000+2,000+3,000+5,000 = 130,000
        #  line 19 = 171,000 - 11,412 = 159,588
        #  Schedule Y: 6,403.94 + 9.3% x (159,588 - 145,448) = 7,718.96 -> 7,719
        #  rate = 7,719 / 159,588 = 0.0484; Part IV % = 130,000 / 171,000 = 0.7602
        #  deduction = 11,412 x 0.7602 = 8,675; line 35 = 121,325; line 37 = 5,872
        #  line 38 = 121,325 / 159,588 = 0.7602; line 39 = 306 x 0.7602 = 233; line 40 = 5,639
        r = ca.calculate(self.CASE)
        self.assertNotIn("error", r)
        f = r["form_540nr"]
        self.assertEqual(r["schedule_ca"]["column_D"], "171000")
        self.assertEqual(r["schedule_ca"]["column_E"], "130000")
        self.assertEqual(r["notes"], [])
        for line, want in (("line16", "10000"), ("line17", "171000"), ("line19", "159588"),
                           ("line31", "7719"), ("line36", "0.0484"), ("line35", "121325"),
                           ("line37", "5872"), ("line38", "0.7602"), ("line39", "233"),
                           ("line40", "5639"), ("line74", "5639")):
            self.assertEqual(f[line], want, line)

    def test_ftb_3805p_additional_tax_goes_to_line_73(self):
        # 2.5% x 2,000 early taxable distribution = 50 (filer-supplied from FTB 3805P)
        base = ca.calculate(self.CASE)["form_540nr"]
        case = dict(self.CASE, other_tax={"line73": 50})
        f = ca.calculate(case)["form_540nr"]
        self.assertEqual(f["line73"], "50")
        self.assertEqual(f["line74"], str(int(base["line74"]) + 50))

    def test_addback_scenario_lowers_tax(self):
        case = dict(self.CASE, scenarios=[{
            "label": "no bonus add-back",
            "rows": {"rental": {"addition": 0, "resident": -3000}}}])
        sc = ca.calculate(case)["scenarios"][0]
        self.assertLess(Decimal(sc["change_in_total_tax"]), 0)

    def test_retirement_nonresident_period_is_excluded(self):
        # All distributions taken while a nonresident: column E has none of the IRA row
        case = json.loads(json.dumps(self.CASE))
        case["rows"][3]["resident"] = 0
        r = ca.calculate(case)
        self.assertEqual(r["schedule_ca"]["column_E"], "127000")
        self.assertEqual(r["schedule_ca"]["column_D"], "171000")


class CommandLineTests(unittest.TestCase):
    def test_cli_outputs_json(self):
        out = subprocess.run([sys.executable, "-I", SCRIPT, json.dumps(part_year_case())],
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(json.loads(out.stdout)["form_540nr"]["line74"], "6882")

    def test_cli_invalid_json(self):
        out = subprocess.run([sys.executable, "-I", SCRIPT, "{bad"], capture_output=True, text=True)
        self.assertEqual(out.returncode, 1)
        self.assertIn("error", json.loads(out.stdout))


if __name__ == "__main__":
    unittest.main()
