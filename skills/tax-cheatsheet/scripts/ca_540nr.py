"""
ca_540nr.py — California Form 540NR / Schedule CA (540NR) calculation for 2025.

Usage:
    python ca_540nr.py '{"filing_status": "MFJ", "federal_agi": 180000, "rows": [...], ...}'

Input keys (all amounts in dollars):
    filing_status      Single | MFJ | MFS | HoH | QSS
    federal_agi        Form 1040 line 11b (Form 540NR line 13)
    rows               Schedule CA (540NR) Part II rows. Each row:
                         id, label, kind ("income" or "adjustment"),
                         federal (col A), subtraction (col B), addition (col C),
                         resident (col E amount earned/received as a resident),
                         nonresident_ca_source (col E amount from California
                         sources while a nonresident)
    exemptions         {"blind": n, "senior": n, "dependents": n}
    credits_total      Form 540NR line 62 (filer-supplied)
    other_tax          {"line41": x, "line71": x, "line73": x}
    payments           {"line81": x, "line82": x, "line83": x, "other": x}
    scenarios          Optional list of {"label": str, "rows": {row_id: {field: value}}}
                       to show the dollar effect of a judgment call.

Rules (all cite reference/curated/ca/):
- Schedule CA columns D and E, Part IV proration: ca-schedule-ca-540nr.md
- Form 540NR lines 7-74, 101, 104: ca-form-540nr-line-by-line.md
- Rate schedules, Tax Table, standard deduction, exemption credits, AGI
  limitation, Behavioral Health Services Tax: ca-2025-numbers.md
- Part-year column E split: ca-residency-part-year.md
- Withholding lines: ca-credits-withholding.md
Whole-dollar rounding (half up) is applied at each form line.
"""

import copy
import json
import sys
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING

ZERO = Decimal("0")
ONE = Decimal("1")

# Source: ca-2025-numbers.md, Tax Rate Schedules X, Y, Z
# (floor, base tax, rate); each bracket runs to the next floor.
SCHEDULES = {
    "X": [
        ("0", "0.00", "0.01"), ("11079", "110.79", "0.02"),
        ("26264", "414.49", "0.04"), ("41452", "1022.01", "0.06"),
        ("57542", "1987.41", "0.08"), ("72724", "3201.97", "0.093"),
        ("371479", "30986.19", "0.103"), ("445771", "38638.27", "0.113"),
        ("742953", "72219.84", "0.123"),
    ],
    "Y": [
        ("0", "0.00", "0.01"), ("22158", "221.58", "0.02"),
        ("52528", "828.98", "0.04"), ("82904", "2044.02", "0.06"),
        ("115084", "3974.82", "0.08"), ("145448", "6403.94", "0.093"),
        ("742958", "61972.37", "0.103"), ("891542", "77276.52", "0.113"),
        ("1485906", "144439.65", "0.123"),
    ],
    "Z": [
        ("0", "0.00", "0.01"), ("22173", "221.73", "0.02"),
        ("52530", "828.87", "0.04"), ("67716", "1436.31", "0.06"),
        ("83805", "2401.65", "0.08"), ("98990", "3616.45", "0.093"),
        ("505208", "41394.72", "0.103"), ("606251", "51802.15", "0.113"),
        ("1010417", "97472.91", "0.123"),
    ],
}

# Source: ca-2025-numbers.md, Filing Status Schedules and Standard Deduction
STATUS = {
    "Single": {"schedule": "X", "std": 5706, "personal": 1, "agi_limit": 252203, "step": 2500},
    "MFS": {"schedule": "X", "std": 5706, "personal": 1, "agi_limit": 252203, "step": 1250},
    "MFJ": {"schedule": "Y", "std": 11412, "personal": 2, "agi_limit": 504411, "step": 2500},
    "QSS": {"schedule": "Y", "std": 11412, "personal": 2, "agi_limit": 504411, "step": 2500},
    "HoH": {"schedule": "Z", "std": 11412, "personal": 1, "agi_limit": 378310, "step": 2500},
}

# Source: ca-2025-numbers.md, Exemption Credits
PERSONAL_CREDIT = Decimal("153")
DEPENDENT_CREDIT = Decimal("475")
TAX_TABLE_LIMIT = Decimal("100000")  # Form 540NR line 31
BHST_THRESHOLD = Decimal("1000000")  # ca-2025-numbers.md, line 72


def d(val):
    """Convert to Decimal. Returns Decimal('0') for None/empty."""
    if val is None or val == "":
        return ZERO
    try:
        return Decimal(str(val).replace(",", "").strip())
    except Exception:
        raise ValueError(f"Not a number: {val!r}")


def dollars(val):
    """Whole-dollar rounding, half up (forms are filed in whole dollars)."""
    return val.quantize(ONE, rounding=ROUND_HALF_UP)


def pct4(val):
    return val.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def schedule_tax(income, schedule):
    """Tax Rate Schedule result rounded to cents (ca-2025-numbers.md)."""
    brackets = SCHEDULES[schedule]
    floor, base, rate = brackets[0]
    for b in brackets:
        if income > Decimal(b[0]):
            floor, base, rate = b
    tax = Decimal(base) + Decimal(rate) * (income - Decimal(floor))
    return tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def tax_table_midpoint(income):
    """Income the Tax Table uses for the range containing income.

    Ranges are $51-$150, $151-$250, ... and the table amount is the Rate
    Schedule tax at the range's round-hundred midpoint (100, 200, ...). The
    last range, $99,951-$100,000, uses 99,975. Verified against all printed
    rows (ca-2025-numbers.md, Tax Table).
    """
    if income <= 50:
        return Decimal("0")
    if income > 99950:
        return Decimal("99975")
    k = ((income - 50) / Decimal(100)).to_integral_value(rounding=ROUND_CEILING)
    return k * 100


def california_tax(taxable_income, schedule):
    """Form 540NR line 31 tax in whole dollars."""
    if taxable_income <= 0:
        return ZERO
    if taxable_income <= TAX_TABLE_LIMIT:
        return dollars(schedule_tax(tax_table_midpoint(taxable_income), schedule))
    return dollars(schedule_tax(taxable_income, schedule))


def build_rows(rows):
    """Schedule CA (540NR) Part II: columns D and E per row."""
    out = []
    for r in rows:
        if r.get("kind") not in ("income", "adjustment"):
            raise ValueError(f"Row {r.get('id')}: kind must be 'income' or 'adjustment'")
        a, b, c = d(r.get("federal")), d(r.get("subtraction")), d(r.get("addition"))
        res, non = d(r.get("resident")), d(r.get("nonresident_ca_source"))
        out.append({
            "id": r.get("id"), "label": r.get("label", ""), "kind": r["kind"],
            "A": a, "B": b, "C": c, "D": a - b + c, "E": res + non,
        })
    return out


def calculate(data):
    status = data.get("filing_status")
    if status not in STATUS:
        return {"error": f"Unknown filing_status: {status}. Use Single, MFJ, MFS, HoH or QSS."}
    if "federal_agi" not in data:
        return {"error": "Missing key: federal_agi"}
    if not data.get("rows"):
        return {"error": "Missing key: rows"}
    if data.get("claimed_as_dependent"):
        return {"error": "Filer can be claimed as a dependent: use the California Standard Deduction Worksheet for Dependents (not supported)."}
    try:
        return _calculate(data, status)
    except ValueError as e:
        return {"error": str(e)}


def _calculate(data, status):
    p = STATUS[status]
    notes = []
    rows = build_rows(data["rows"])

    def total(col, kind):
        return sum((r[col] for r in rows if r["kind"] == kind), ZERO)

    # Schedule CA (540NR) Part II line 27 (income less adjustments)
    sums = {c: total(c, "income") - total(c, "adjustment") for c in "ABCDE"}
    line13 = dollars(d(data["federal_agi"]))
    if dollars(sums["A"]) != line13:
        notes.append(f"Column A total {dollars(sums['A'])} differs from federal AGI {line13}; check the rows.")

    # Form 540NR lines 14-17 (negative column totals move to the other line)
    net_b, net_c = dollars(sums["B"]), dollars(sums["C"])
    line14 = max(net_b, ZERO) + max(-net_c, ZERO)
    line16 = max(net_c, ZERO) + max(-net_b, ZERO)
    line15 = line13 - line14
    line17 = line15 + line16
    col_d = dollars(sums["D"])
    col_e = dollars(sums["E"])
    if line17 != col_d:
        notes.append(f"Line 17 {line17} differs from column D total {col_d}; check the rows.")

    # Lines 7-11 exemptions
    ex = data.get("exemptions") or {}
    blind, senior, deps = int(d(ex.get("blind"))), int(d(ex.get("senior"))), int(d(ex.get("dependents")))
    line7 = Decimal(p["personal"]) * PERSONAL_CREDIT
    line8, line9 = blind * PERSONAL_CREDIT, senior * PERSONAL_CREDIT
    line10 = deps * DEPENDENT_CREDIT
    line11 = line7 + line8 + line9 + line10

    # Lines 18-19
    line18 = Decimal(p["std"])
    line19 = max(line17 - line18, ZERO)

    # Line 31 and 36
    line31 = california_tax(line19, p["schedule"])
    line36 = pct4(line31 / line19) if line19 > 0 else ZERO

    # Schedule CA (540NR) Part IV
    deduction_pct = ZERO
    if col_d > 0:
        deduction_pct = min(pct4(col_e / col_d), ONE) if col_e > 0 else ZERO
    part4_line4 = dollars(line18 * deduction_pct)
    line32 = col_e
    line35 = max(line32 - part4_line4, ZERO)

    line37 = dollars(line35 * line36)
    line38 = min(pct4(line35 / line19), ONE) if line19 > 0 else ZERO

    # Line 39 (AGI Limitation Worksheet when line 13 exceeds the threshold)
    limit = Decimal(p["agi_limit"])
    if line13 > limit:
        steps = ((line13 - limit) / Decimal(p["step"])).to_integral_value(rounding=ROUND_CEILING)
        e = steps * 6
        boxes_pbs = Decimal(p["personal"]) + blind + senior
        i = max(line7 + line8 + line9 - e * boxes_pbs, ZERO)
        m = max(line10 - e * deps, ZERO)
        line39 = dollars((i + m) * line38)
        notes.append("Exemption credits reduced by the AGI Limitation Worksheet.")
    else:
        line39 = dollars(line11 * line38)
    line40 = max(line37 - line39, ZERO)

    ot = data.get("other_tax") or {}
    line41, line71, line73 = dollars(d(ot.get("line41"))), dollars(d(ot.get("line71"))), dollars(d(ot.get("line73")))
    line42 = line40 + line41
    line62 = dollars(d(data.get("credits_total")))
    line63 = max(line42 - line62, ZERO)
    line72 = dollars(max(line35 - BHST_THRESHOLD, ZERO) * Decimal("0.01"))
    line74 = line63 + line71 + line72 + line73

    pay = data.get("payments") or {}
    line81, line82, line83 = (dollars(d(pay.get(k))) for k in ("line81", "line82", "line83"))
    line88 = line81 + line82 + line83 + dollars(d(pay.get("other")))
    overpaid = max(line88 - line74, ZERO)
    due = max(line74 - line88, ZERO)

    result = {
        "filing_status": status,
        "schedule_ca": {
            "column_A": str(dollars(sums["A"])), "column_B": str(net_b),
            "column_C": str(net_c), "column_D": str(col_d), "column_E": str(col_e),
            "part_iv_line3_deduction_percentage": str(deduction_pct),
            "part_iv_line4_deduction": str(part4_line4),
        },
        "form_540nr": {
            "line7": str(line7), "line8": str(line8), "line9": str(line9),
            "line10": str(line10), "line11": str(line11),
            "line13": str(line13), "line14": str(line14), "line15": str(line15),
            "line16": str(line16), "line17": str(line17), "line18": str(line18),
            "line19": str(line19), "line31": str(line31), "line32": str(line32),
            "line35": str(line35), "line36": str(line36), "line37": str(line37),
            "line38": str(line38), "line39": str(line39), "line40": str(line40),
            "line41": str(line41), "line42": str(line42), "line62": str(line62),
            "line63": str(line63), "line71": str(line71), "line72": str(line72),
            "line73": str(line73), "line74": str(line74), "line81": str(line81),
            "line82": str(line82), "line83": str(line83), "line88": str(line88),
            "line101_overpaid": str(overpaid), "line104_tax_due": str(due),
        },
        "tax_method": "Tax Table" if line19 <= TAX_TABLE_LIMIT else "Tax Rate Schedule " + p["schedule"],
        "notes": notes,
    }

    scenarios = data.get("scenarios")
    if scenarios:
        result["scenarios"] = []
        for sc in scenarios:
            alt = copy.deepcopy({k: v for k, v in data.items() if k != "scenarios"})
            for row in alt["rows"]:
                row.update((sc.get("rows") or {}).get(row.get("id"), {}))
            r2 = calculate(alt)
            if "error" in r2:
                result["scenarios"].append({"label": sc.get("label"), "error": r2["error"]})
                continue
            t2 = d(r2["form_540nr"]["line74"])
            result["scenarios"].append({
                "label": sc.get("label"),
                "total_tax_line74": str(t2),
                "change_in_total_tax": str(t2 - line74),
            })
    return result


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: ca_540nr.py '<json>' (see module docstring)"}))
        sys.exit(1)
    try:
        data = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)
    result = calculate(data)
    print(json.dumps(result, indent=2))
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
