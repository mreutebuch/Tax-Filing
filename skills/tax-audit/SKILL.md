---
name: tax-audit
description: "After all forms are filled, performs a comprehensive cross-check of the entire tax return against source documents before submission. Catches cross-form errors, math mistakes, withholding mismatches, and missing documents that session-by-session filing misses. Triggers on: 'audit my return', 'final check', 'am I ready to file', 'check everything', 'cross-check my forms', 'verify my return', 'pre-filing review', 'review before I file', 'double check my taxes', 'did I miss anything'."
---

# tax-audit

Comprehensive pre-filing audit — cross-checks the entire completed tax return against source documents in `analysis/tax-doc-summary.csv`. Verifies all math through Python scripts, checks for missing forms and common pitfalls. This should be the **last step before filing**, run after all forms are filled using `/tax-cheatsheet`.

## Session Handoff

Every conversation starts here:

1. Check if `analysis/tax-doc-summary.csv` exists
2. If it exists:
   - Count distinct documents and total rows
   - Report: "I have your extracted tax data (N documents, M values). Ready to audit your completed return."
3. If it does NOT exist:
   - Tell the user: "No extracted tax data found. Run `/tax-prep` first to extract your document values, then fill your forms with `/tax-cheatsheet`, and come back here for the final audit."
   - Stop — do not proceed without the CSV
4. Collect the user's completed form values. Accept them in any of these ways:
   - The user provides values directly — for example:
     ```
     1040 Line 1 wages: $85,000
     1040 Line 2b interest: $1,200
     1040 Line 11 AGI: $98,500
     1040 Line 15 taxable income: $67,000
     1040 Line 16 tax: $7,582
     1040 Line 25a withholding: $12,400
     ```
   - The user references completed form files
   - The user reads values from their filled forms
5. Ask for **filing status** if not already known (MFJ, Single, MFS, HoH)
6. Ask which **forms they have completed** (list of form names, e.g., "1040, Schedule A, Schedule D")
7. Build the `federal_values` dict from the user's input (see Input Schema Reference below)

## Audit Checks Table

| # | Category | What It Verifies | Script | Reference File(s) |
|---|----------|-----------------|--------|--------------------|
| 1 | Internal Consistency | Wages, interest, dividends match source docs | `cross_check.py` | `1040-line-by-line.md` |
| 2 | Internal Consistency | Total income = sum of income lines | `cross_check.py` | `1040-line-by-line.md` |
| 3 | Internal Consistency | AGI = total income - adjustments | `cross_check.py` | `1040-line-by-line.md` |
| 4 | Internal Consistency | Taxable income = AGI - deductions | `cross_check.py` | `1040-line-by-line.md` |
| 5 | Math Verification | Tax computed correctly for bracket and filing status | `cross_check.py` | `2025-tax-numbers.md` |
| 6 | Withholding Match | Federal withholding on 1040 = sum of W-2 Box 2 | `cross_check.py` | `1040-line-by-line.md` |
| 7 | Document Completeness | Every CSV document reflected in filed forms | `completeness_check.py` | All |
| 8 | Missing Forms | Required schedules filed based on income types | `completeness_check.py` | `investment-income.md`, `schedule-c-guide.md`, `additional-medicare-tax.md` |
| 9 | Common Mistakes | 8 known pitfalls verified | Manual review | `docs/KNOWN-PITFALLS.md` |
| 10 | Estimated Payments | Entered amounts match actual payments | Manual review | `1040-line-by-line.md` |

## Audit Workflow

### Step 1 — Gather Inputs

Load `analysis/tax-doc-summary.csv` and count documents. Collect the user's federal form values (`federal_values` dict), filing status, and list of completed forms. See Input Schema Reference for the exact keys needed.

### Step 2 — Run Cross-Check Script

Invoke `cross_check.py` to verify internal consistency, withholding match, and tax bracket verification.

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/tax-audit/scripts/cross_check.py" '{"csv_path": "analysis/tax-doc-summary.csv", "federal_values": {...}, "filing_status": "MFJ"}'
```

Parse the JSON output. Each check returns: `check_name`, `status` (pass/fail/warning), `expected`, `actual`, `difference`, and `detail`.

### Step 3 — Run Completeness Check Script

Invoke `completeness_check.py` to verify document coverage and required forms.

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/tax-audit/scripts/completeness_check.py" '{"csv_path": "analysis/tax-doc-summary.csv", "forms_filed": ["1040", "Schedule A", ...], "filing_status": "MFJ"}'
```

Parse the JSON output. Check `document_coverage` for unmapped documents, `required_forms` for missing schedules, and `orphaned_documents` for unrecognized types.

### Step 4 — Manual Pitfall Review

Read `docs/KNOWN-PITFALLS.md` and walk through each of the 8 federal pitfalls (and, for a California return, pitfalls 9-12 in the California section) against the user's values:

1. **AGI includes ALL income** — Verify AGI accounts for wages + interest + dividends + capital gains + Schedule C, not just W-2 wages. *(Source: 1040-line-by-line.md, Income Section)*
2. **Math verified through Python** — Confirm all computed values came from script output, not manual arithmetic. *(Source: CLAUDE.md, Rules)*
3. **Cross-form references match** — Verify 1040 Line 7 matches Schedule D Line 21, 1040 Line 8 matches Schedule 1 Line 10, etc. *(Source: 1040-line-by-line.md, Income Section)*
4. **W-2 Box 5 >= Box 1** — For each W-2 in CSV, confirm Medicare wages >= regular wages. *(Source: additional-medicare-tax.md, Form 8959 Line-by-Line)*
5. **SALT cap applied correctly** — Confirm the SALT cap ($40K MFJ, subject to MAGI phase-out) is applied to Schedule A. *(Source: salt-deduction-2025.md, Overall SALT Cap)*
6. **Student loan interest phase-out** — If 1098-E exists but MAGI >= $200K (MFJ), deduction must be $0. *(Source: student-loan-interest.md, MAGI Phase-Out)*
7. **QBI = $0 if Schedule C loss** — If Schedule C Line 31 is negative, Form 8995 Line 15 must be $0. *(Source: self-employment-qbi.md, QBI Loss Carryforward)*
8. **Additional Medicare Tax threshold** — Combined W-2 Box 5 > $250K (MFJ) triggers Form 8959 even if neither spouse individually exceeds $200K. *(Source: additional-medicare-tax.md, How Employer Withholding Works)*

For each pitfall, determine: **PASS** (verified correct), **WARNING** (could not verify — needs user confirmation), or **FAIL** (confirmed incorrect).

### Step 5 — Estimated Payments Check

Ask the user: "Did you make estimated tax payments during the year?"

- If **no**: Mark this section as N/A
- If **yes**: Ask for the amounts paid and compare to:
  - 1040 Line 26 (federal estimated payments)
  - Flag any discrepancy as WARNING

### Step 6 — Compile Results

Merge all results from Steps 2–5 into the output format below. Apply the verdict logic:

- Any **FAIL** anywhere → **STOP — DO NOT FILE**
- Any **WARNING** (no FAILs) → **REVIEW THESE ITEMS**
- All **PASS** → **READY TO FILE**

## Output Template

Present the audit results in this format:

```markdown
## Tax Audit Report

Audited against `analysis/tax-doc-summary.csv` (N documents, M values).
Filing status: [status]. Forms reviewed: [list].

### 1. Internal Consistency

| Check | Status | Expected | Actual | Diff | Detail |
|-------|--------|----------|--------|------|--------|
| Wages match W-2 | PASS/FAIL | $X | $Y | $Z | ... |
| Interest match 1099-INT | ... | ... | ... | ... | ... |
| Dividends match 1099-DIV | ... | ... | ... | ... | ... |
| Total income sum | ... | ... | ... | ... | ... |
| AGI calculation | ... | ... | ... | ... | ... |
| Taxable income | ... | ... | ... | ... | ... |

### 2. Math Verification

| Check | Status | Expected | Actual | Diff | Detail |
|-------|--------|----------|--------|------|--------|
| Tax bracket verify | PASS/FAIL/WARN | $X | $Y | $Z | ... |

### 3. Withholding Match

| Check | Status | Expected | Actual | Diff | Detail |
|-------|--------|----------|--------|------|--------|
| Federal withholding | ... | ... | ... | ... | ... |

### 4. Document Completeness

| Document | Type | Status | Maps To |
|----------|------|--------|---------|
| W-2 (Name - Employer) | W-2 | Mapped | 1040, Schedule A |
| ... | ... | ... | ... |

### 5. Missing Forms

| Form | Status | Reason | Filed? |
|------|--------|--------|--------|
| Schedule B | Required | Interest > $1,500 | Yes/No |
| ... | ... | ... | ... |

### 6. Common Mistakes Review

| # | Pitfall | Status | Detail |
|---|---------|--------|--------|
| 1 | AGI includes all income | PASS | Verified: AGI = wages + interest + dividends + ... |
| ... | ... | ... | ... |

### 7. Estimated Payments

| Check | Status | Detail |
|-------|--------|--------|
| Federal estimated (Line 26) | PASS/N/A | ... |

---

### Verdict

**[VERDICT]**

[Summary paragraph]

- Total checks: N
- Passed: N
- Warnings: N
- Failed: N

---
*Disclaimer: This audit assists with tax return preparation. It does not constitute tax advice. Verify all results against source documents. Consult a qualified tax professional for your specific situation.*
```

**Verdict values:**
- **READY TO FILE** — All checks passed. Return appears consistent and complete.
- **REVIEW THESE ITEMS** — N items need review before filing. See WARNING items above.
- **STOP — DO NOT FILE** — N critical errors found. Do NOT file until resolved.

## California Section (`state: CA`)

Run after the federal audit when a California return exists. Source files: `reference/curated/ca/`.

1. Gather the filer's Form 540NR values (`line12` ... `line104`) and the inputs given to `ca_540nr.py` (rows, filing status, exemptions, payments).
2. Run the independent recomputation:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/tax-audit/scripts/ca_cross_check.py" '{"inputs": {...}, "filed": {"line19": 168588, "line74": 6882}, "documents": {"w2_ca_withholding": 9000, "w2_box16_wages": 180000, "state_refund_1099g": 0}}'
```

3. Report each line check (`MATCH`, `ROUNDING`, `DIFFERENT`), the document checks, and the verdict (READY TO FILE, REVIEW THESE ITEMS, STOP). A difference of $1 or less is rounding because the form rounds each line. *(Source: ca-2025-numbers.md, Rounding the Schedule Result)*
4. Walk through California pitfalls 9-12 in `docs/KNOWN-PITFALLS.md`.
5. List the `unverified_items` from the script in the report. Never mark an unverified item as passed.
6. Confirm that SDI was not claimed as a credit and that withholding on line 81 matches W-2 box 17 only. *(Source: ca-credits-withholding.md)*

## Input Schema Reference

### federal_values

Collect these key 1040 line values from the user:

| Key | Form Line | Description |
|-----|-----------|-------------|
| `line_1_wages` | 1040 Line 1 | Total wages from all W-2s |
| `line_2b_interest` | 1040 Line 2b | Taxable interest |
| `line_3b_dividends` | 1040 Line 3b | Ordinary dividends |
| `line_7_capital_gain` | 1040 Line 7 | Capital gain or loss |
| `line_8_other_income` | 1040 Line 8 | Other income (Schedule 1) |
| `line_9_total_income` | 1040 Line 9 | Total income |
| `line_10_adjustments` | 1040 Line 10 | Adjustments to income |
| `line_11_agi` | 1040 Line 11 | Adjusted gross income |
| `line_12a_deduction` | 1040 Line 12a | Standard or itemized deduction |
| `line_13a_qbi` | 1040 Line 13a | QBI deduction |
| `line_13b_sched1a` | 1040 Line 13b | Schedule 1-A deductions |
| `line_14_total_deductions` | 1040 Line 14 | Total deductions |
| `line_15_taxable_income` | 1040 Line 15 | Taxable income |
| `line_16_tax` | 1040 Line 16 | Tax |
| `line_25a_w2_withholding` | 1040 Line 25a | W-2 withholding |

### forms_filed

A list of form names the user has completed. Common values:

`["1040", "Schedule A", "Schedule B", "Schedule C", "Schedule D", "Form 8949", "Schedule 1", "Schedule 1-A", "Schedule 2", "Form 8959", "Form 8995"]`

## Mandatory Rules

1. **Never** attempt to reconstruct redacted SSNs or other PII
2. **All calculations** run through Python scripts — never do arithmetic in natural language
3. Every tax rule **must cite** a file in `reference/curated/` — format: *(Source: filename.md, section)*
4. If a rule cannot be verified from curated references: "I cannot verify this from provided IRS materials — check IRS.gov"
5. Any saved forms must leave SSN, bank routing, account number, and signature fields **blank**
6. No personal information stored in skill files

## Script Reference

| Script | Purpose | Location |
|--------|---------|----------|
| `cross_check.py` | Source-document match, withholding vs W-2, AGI math, tax bracket verification | `${CLAUDE_PLUGIN_ROOT}/skills/tax-audit/scripts/` |
| `completeness_check.py` | Document coverage, required forms, orphaned documents | `${CLAUDE_PLUGIN_ROOT}/skills/tax-audit/scripts/` |
| `ca_cross_check.py` | Independent California recomputation and comparison with filed Form 540NR values | `${CLAUDE_PLUGIN_ROOT}/skills/tax-audit/scripts/` |

Also available from `/tax-cheatsheet` (do not modify):

| Script | Purpose | Location |
|--------|---------|----------|
| `form_line_lookup.py` | Query CSV by document type and box | `${CLAUDE_PLUGIN_ROOT}/skills/tax-cheatsheet/scripts/` |
| `standard_vs_itemized.py` | Compare standard vs itemized deduction | `${CLAUDE_PLUGIN_ROOT}/skills/tax-cheatsheet/scripts/` |
| `salt_cap_calculator.py` | SALT cap with MAGI phase-out | `${CLAUDE_PLUGIN_ROOT}/skills/tax-cheatsheet/scripts/` |

## Related Skills

- `/tax-prep` — Extract document values into CSV (run **first**)
- `/tax-cheatsheet` — Line-by-line form filling help (run **before** this skill)
- `/tax-advisor` — Next-year tax planning based on this year's data (run **after** filing)
