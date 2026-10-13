"""
ca_cross_check.py — Independent recomputation of a California Form 540NR.

Usage:
    python ca_cross_check.py '{"inputs": {...ca_540nr.py input...}, "filed": {"line19": 168588, ...}, "documents": {...}}'

"inputs" uses the same keys as skills/tax-cheatsheet/scripts/ca_540nr.py.
"filed" holds the values the filer entered on Form 540NR (keys line13 ... line104).
"documents" (optional): {"w2_ca_withholding": x, "w2_box16_wages": x,
                         "state_refund_1099g": x, "w2_sdi": x}

This script does NOT import ca_540nr.py. It rebuilds the tax from marginal
rates only (rate x slice of income per bracket) instead of base amounts, and
uses a closed-form Tax Table lookup, so a typo in either implementation shows
up as a difference. Rules cite reference/curated/ca/:
- Marginal brackets, Tax Table, standard deduction, exemptions:
  ca-2025-numbers.md
- Lines 13-74: ca-form-540nr-line-by-line.md
- Part IV proration: ca-schedule-ca-540nr.md
- Withholding and SDI: ca-credits-withholding.md
Differences of $1 or less are reported as rounding (the form rounds each line).
"""

import json
import math
import sys
from decimal import Decimal, ROUND_HALF_UP

D = Decimal

# (floor, marginal rate) per schedule — ca-2025-numbers.md
MARGINAL = {
    "X": [(0, "0.01"), (11079, "0.02"), (26264, "0.04"), (41452, "0.06"), (57542, "0.08"),
          (72724, "0.093"), (371479, "0.103"), (445771, "0.113"), (742953, "0.123")],
    "Y": [(0, "0.01"), (22158, "0.02"), (52528, "0.04"), (82904, "0.06"), (115084, "0.08"),
          (145448, "0.093"), (742958, "0.103"), (891542, "0.113"), (1485906, "0.123")],
    "Z": [(0, "0.01"), (22173, "0.02"), (52530, "0.04"), (67716, "0.06"), (83805, "0.08"),
          (98990, "0.093"), (505208, "0.103"), (606251, "0.113"), (1010417, "0.123")],
}
STATUS = {
    "Single": ("X", 5706, 1, 252203, 2500), "MFS": ("X", 5706, 1, 252203, 1250),
    "MFJ": ("Y", 11412, 2, 504411, 2500), "QSS": ("Y", 11412, 2, 504411, 2500),
    "HoH": ("Z", 11412, 1, 378310, 2500),
}
# Items the FTB materials in reference/curated/ca/ did not let us verify
UNVERIFIED = [
    "Community property effect of the move on the part-year spouse's pre-move income "
    "(I cannot verify this from provided FTB materials — check ftb.ca.gov)",
    "Credits other than exemption credits are filer-supplied "
    "(I cannot verify this from provided FTB materials — check ftb.ca.gov)",
    "Alternative minimum tax (Schedule P (540NR)) is not computed; verify Boxes A-C in the 540NR booklet",
    "Credit limits (tentative minimum tax) and the Credit Chart are not applied; line 62 is filer-supplied "
    "(I cannot verify this from provided FTB materials — check ftb.ca.gov)",
    "Mapping of 1099-R Box 7 codes to California early-distribution exceptions (FTB 3805P Line 2 uses "
    "exception numbers) (I cannot verify this from provided FTB materials — check ftb.ca.gov)",
    "California treatment of OBBBA federal items with no stated Schedule CA (540NR) line, such as "
    "Schedule 1-A deductions (I cannot verify this from provided FTB materials — check ftb.ca.gov)",
    "Daily pro-rata allocation of a direct rental and expenses paid before a property was available "
    "for rent (I cannot verify this from provided FTB materials — check ftb.ca.gov)",
]


def num(x):
    return D(str(x if x not in (None, "") else 0).replace(",", ""))


def whole(x):
    return x.quantize(D(1), rounding=ROUND_HALF_UP)


def marginal_tax(income, sched):
    """Sum of rate x slice for each bracket, rounded to whole dollars."""
    rows = MARGINAL[sched]
    total = D(0)
    for i, (floor, rate) in enumerate(rows):
        top = D(rows[i + 1][0]) if i + 1 < len(rows) else None
        if income <= floor:
            break
        upper = income if top is None or income < top else top
        total += (upper - D(floor)) * D(rate)
    return whole(total.quantize(D("0.01"), rounding=ROUND_HALF_UP))


def tax_for_line19(line19, sched):
    if line19 <= 0:
        return D(0)
    if line19 <= 100000:
        if line19 <= 50:
            return D(0)
        if line19 > 99950:
            return marginal_tax(D(99975), sched)
        # range number k covers (100k-49 .. 100k+50); table uses 100k
        k = math.ceil((int(line19) - 50) / 100)
        return marginal_tax(D(100 * k), sched)
    return marginal_tax(line19, sched)


def recompute(inp):
    sched, std, personal, limit, step = STATUS[inp["filing_status"]]
    agi = whole(num(inp["federal_agi"]))
    sa = sb = sc = sd = se = D(0)
    for r in inp["rows"]:
        sign = 1 if r["kind"] == "income" else -1
        a, b, c = num(r.get("federal")), num(r.get("subtraction")), num(r.get("addition"))
        sa += sign * a
        sb += sign * b
        sc += sign * c
        sd += sign * (a - b + c)
        se += sign * (num(r.get("resident")) + num(r.get("nonresident_ca_source")))
    nb, nc = whole(sb), whole(sc)
    l14 = max(nb, D(0)) + max(-nc, D(0))
    l16 = max(nc, D(0)) + max(-nb, D(0))
    l17 = agi - l14 + l16
    l19 = max(l17 - std, D(0))
    l31 = tax_for_line19(l19, sched)
    l36 = (l31 / l19).quantize(D("0.0001"), rounding=ROUND_HALF_UP) if l19 else D(0)
    col_d, col_e = whole(sd), whole(se)
    pct = D(0) if col_d <= 0 or col_e <= 0 else min((col_e / col_d).quantize(D("0.0001"), rounding=ROUND_HALF_UP), D(1))
    l35 = max(col_e - whole(D(std) * pct), D(0))
    l37 = whole(l35 * l36)
    l38 = min((l35 / l19).quantize(D("0.0001"), rounding=ROUND_HALF_UP), D(1)) if l19 else D(0)
    ex = inp.get("exemptions") or {}
    blind, senior, deps = int(num(ex.get("blind"))), int(num(ex.get("senior"))), int(num(ex.get("dependents")))
    per = D(153)
    pbs_boxes = personal + blind + senior
    if agi > limit:
        e = D(math.ceil((agi - limit) / D(step))) * 6
        base = max(pbs_boxes * per - e * pbs_boxes, D(0)) + max(deps * D(475) - e * deps, D(0))
    else:
        base = pbs_boxes * per + deps * D(475)
    l39 = whole(base * l38)
    l40 = max(l37 - l39, D(0))
    ot = inp.get("other_tax") or {}
    l42 = l40 + whole(num(ot.get("line41")))
    l63 = max(l42 - whole(num(inp.get("credits_total"))), D(0))
    l72 = whole(max(l35 - 1000000, D(0)) * D("0.01"))
    l74 = l63 + whole(num(ot.get("line71"))) + l72 + whole(num(ot.get("line73")))
    pay = inp.get("payments") or {}
    l91 = whole(num(pay.get("line91")))
    l88 = sum((whole(num(pay.get(k))) for k in ("line81", "line82", "line83", "other")), D(0))
    return {
        "line13": agi, "line14": l14, "line16": l16, "line17": l17, "line19": l19,
        "line31": l31, "line35": l35, "line36": l36, "line37": l37,
        "line38": l38, "line39": l39, "line40": l40, "line63": l63, "line72": l72,
        "line74": l74, "line88": l88,
        "line92": max(l88 - l91, D(0)), "line93": max(l91 - l88, D(0)),
        "line101_overpaid": max(max(l88 - l91, D(0)) - l74, D(0)),
        "line104_tax_due": max(l74 - max(l88 - l91, D(0)), D(0)),
    }


def check(data):
    inp = data.get("inputs")
    filed = data.get("filed")
    if not inp or "filing_status" not in inp or "rows" not in inp or "federal_agi" not in inp:
        return {"error": "Missing key: inputs (needs filing_status, federal_agi, rows)"}
    if inp["filing_status"] not in STATUS:
        return {"error": f"Unknown filing_status: {inp['filing_status']}"}
    if not filed:
        return {"error": "Missing key: filed"}
    try:
        mine = recompute(inp)
        checks = []
        worst = "PASS"
        for line, val in mine.items():
            if line not in filed:
                checks.append({"line": line, "status": "SKIPPED", "detail": "not in filed values"})
                continue
            diff = num(filed[line]) - val
            tol = D("0.0001") if line in ("line36", "line38") else D(1)
            if diff == 0:
                st = "MATCH"
            elif abs(diff) <= tol:
                st = "ROUNDING"
            else:
                st = "DIFFERENT"
                worst = "STOP" if abs(diff) > 5 or line in ("line74", "line104_tax_due", "line101_overpaid") else "REVIEW"
            checks.append({"line": line, "status": st, "recomputed": str(val),
                           "filed": str(num(filed[line])), "difference": str(diff)})
        if worst == "PASS" and any(c["status"] == "DIFFERENT" for c in checks):
            worst = "REVIEW"
        docs = data.get("documents") or {}
        doc_checks = []
        if "w2_ca_withholding" in docs and "line81" in filed:
            diff = num(filed["line81"]) - num(docs["w2_ca_withholding"]) - num((inp.get("payments") or {}).get("other_withholding_docs"))
            doc_checks.append({"check": "line81 vs W-2 box 17 total", "difference": str(diff),
                               "status": "MATCH" if abs(diff) <= 1 else "DIFFERENT"})
        if "w2_box16_wages" in docs and "line12" in filed:
            diff = num(filed["line12"]) - num(docs["w2_box16_wages"])
            doc_checks.append({"check": "line12 vs W-2 box 16 total", "difference": str(diff),
                               "status": "MATCH" if abs(diff) <= 1 else "DIFFERENT"})
        if "state_refund_1099g" in docs:
            sub = sum(num(r.get("subtraction")) for r in inp["rows"] if r.get("id") == "state_refund")
            diff = sub - num(docs["state_refund_1099g"])
            doc_checks.append({"check": "state refund subtracted in column B vs 1099-G", "difference": str(diff),
                               "status": "MATCH" if diff == 0 else "DIFFERENT"})
        if "w2_sdi" in docs:
            doc_checks.append({"check": "SDI (W-2 box 14) is not a credit on Form 540NR", "status": "INFO",
                               "detail": "Not entered on line 81 (ca-credits-withholding.md)"})
        if any(c["status"] == "DIFFERENT" for c in doc_checks) and worst == "PASS":
            worst = "REVIEW"
        verdict = {"PASS": "READY TO FILE", "REVIEW": "REVIEW THESE ITEMS", "STOP": "STOP"}[worst]
        return {"verdict": verdict, "line_checks": checks, "document_checks": doc_checks,
                "unverified_items": UNVERIFIED}
    except (KeyError, ValueError, ArithmeticError) as e:
        return {"error": f"Bad input: {e}"}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: ca_cross_check.py '<json>' (see module docstring)"}))
        sys.exit(1)
    try:
        data = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)
    result = check(data)
    print(json.dumps(result, indent=2))
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
