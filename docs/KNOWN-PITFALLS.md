# Known Pitfalls — Common Tax Filing Mistakes

Reference document for the `/tax-audit` skill. Each pitfall includes
a description, how to verify, and a citation to the relevant curated
reference file.

---

## Pitfall 1: AGI Breakdown Must Include ALL Income

- **Mistake:** When splitting AGI between spouses (or reconciling it
  to source documents), only including W-2 wages and forgetting
  interest, dividends, capital gains, and Schedule C income.
- **How to verify:** Sum each spouse's W-2 wages + their share of
  investment income + Schedule C income. The total must equal federal AGI
  (1040 Line 11).
- **Citation:** *(Source: 1040-line-by-line.md, Income Section)*

## Pitfall 2: All Math Must Be Verified Through Python

- **Mistake:** Eyeballing numbers or doing mental arithmetic instead
  of running values through the calculation scripts.
- **How to verify:** Every computed value on the return should have a
  corresponding script output. Use `cross_check.py` for verification.
- **Citation:** *(Source: CLAUDE.md, Rules)*

## Pitfall 3: Cross-Form References Must Pull From Completed Forms

- **Mistake:** Entering a value on Form 1040 Line 7 that does not
  match Schedule D Line 21 (or using an estimate instead of the
  actual computed value).
- **How to verify:** For each line that references another form,
  trace the value back to the source form and confirm they match.
- **Citation:** *(Source: 1040-line-by-line.md, Income Section)*

## Pitfall 4: W-2 Box 5 (Medicare Wages) >= Box 1 (Wages)

- **Mistake:** Not noticing when Medicare wages are less than regular
  wages, which can indicate pre-tax benefits were applied differently.
  This affects Additional Medicare Tax calculations on Form 8959.
- **How to verify:** For each W-2, confirm Box 5 >= Box 1. If not,
  verify pre-tax benefit treatment is correct.
- **Citation:** *(Source: additional-medicare-tax.md, Form 8959
  Line-by-Line)*

## Pitfall 5: SALT Cap Must Be Applied on Schedule A

- **Mistake:** Deducting state/local taxes and property taxes on
  Schedule A without applying the $40,000 SALT cap (or its MAGI
  phase-out).
- **How to verify:** Confirm Schedule A Line 5e respects the SALT cap
  and any MAGI phase-out.
- **Citation:** *(Source: salt-deduction-2025.md, Overall SALT Cap)*

## Pitfall 6: Student Loan Interest May Be $0 Despite Having 1098-E

- **Mistake:** Claiming a student loan interest deduction when MAGI
  exceeds the phase-out range. Having a 1098-E does not guarantee
  you get the deduction — it depends on MAGI.
- **How to verify:** Check MAGI against the $170,000–$200,000 MFJ
  phase-out range. If MAGI >= $200,000, deduction is $0 regardless
  of the 1098-E amount.
- **Citation:** *(Source: student-loan-interest.md, MAGI Phase-Out)*

## Pitfall 7: QBI Deduction Is $0 if Schedule C Shows a Net Loss

- **Mistake:** Entering a QBI deduction when the business had a loss.
  Negative QBI produces $0 deduction (but the loss carries forward
  to future years).
- **How to verify:** If Schedule C Line 31 is negative, Form 8995
  Line 15 must be $0. File Form 8995 anyway to establish the
  carryforward on Line 16.
- **Citation:** *(Source: self-employment-qbi.md, QBI Loss
  Carryforward)*

## Pitfall 8: Additional Medicare Tax Threshold Mismatch

- **Mistake:** Assuming that because neither spouse individually
  exceeds $200,000 in wages, no Additional Medicare Tax is due. The
  employer withholds at $200,000 per individual employee, but the MFJ
  threshold is $250,000 on combined wages. Combined wages over $250,000
  trigger the tax even if neither spouse alone triggers employer
  withholding.
- **How to verify:** Sum both spouses' W-2 Box 5. If total > $250,000
  (MFJ), Form 8959 is required. Check whether the withholding credit
  (Form 8959 Line 22) covers the liability or leaves a balance due.
- **Citation:** *(Source: additional-medicare-tax.md, How Employer
  Withholding Works)*

## Pitfall 9: Part-Year Filers Must Split Income by Residency Period (California)

- **Mistake:** Putting all income in Schedule CA (540NR) column E, or
  dropping all income earned before a move. California taxes everything
  earned while a resident and only California-source income while a
  nonresident.
- **How to verify:** For each Schedule CA (540NR) row, confirm the
  column E amount equals the resident-period amount plus the
  California-source nonresident-period amount, and that column D still
  holds the all-year total.
- **Citation:** *(Source: ca-residency-part-year.md, How Part-Year
  Residents Are Taxed)*

## Pitfall 10: California Does Not Tax the State Refund (California)

- **Mistake:** Leaving a 1099-G state income tax refund in California
  income because it is on the federal return.
- **How to verify:** The refund amount appears in column A and again in
  column B of Schedule CA (540NR) Part II Section B line 1, and matches
  1099-G Box 2.
- **Citation:** *(Source: ca-schedule-ca-540nr.md, Adjustments Included
  in This Plugin)*

## Pitfall 11: Bonus Depreciation and HSA Do Not Carry Over (California)

- **Mistake:** Copying federal rental depreciation (including bonus
  depreciation) or federal HSA treatment to the California return.
- **How to verify:** Confirm an FTB 3885A adjustment exists for any
  property with bonus depreciation, and that HSA contributions and
  earnings are added back in column C.
- **Citation:** *(Source: ca-schedule-ca-540nr.md, Depreciation; HSA)*

## Pitfall 12: SDI Is Not a Credit and Withholding Excludes Other States (California)

- **Mistake:** Adding SDI (W-2 Box 14) or tax withheld by another state
  to Form 540NR line 81.
- **How to verify:** Line 81 equals the sum of California income tax
  withheld shown on W-2 Box 17 and the listed 1099 boxes only.
- **Citation:** *(Source: ca-credits-withholding.md, Withholding; SDI)*

## Pitfall 13: Retirement Income Received While a Nonresident (California)

- **Mistake:** Leaving a nonresident-period IRA or pension distribution
  in Schedule CA (540NR) column E because the 1099-R total is on the
  federal return.
- **How to verify:** Each 1099-R distribution has a date. Only amounts
  received on or after the first day of California residency are in
  column E (lines 4a-4b, 5a-5b). If any distribution has no date, the
  split is unverified: ask for the date.
- **Citation:** *(Source: ca-retirement-distributions.md, Nonresident
  Period; Part-Year Residents)*

## Pitfall 14: Early-Distribution Tax and Box 7 Codes (California)

- **Mistake:** Ignoring the 2.5% California additional tax on an early
  taxable distribution received as a resident, or assuming every federal
  exception applies in California.
- **How to verify:** For each taxable distribution received as a
  resident before age 59½, read 1099-R Box 7. FTB 3805P is needed for a
  code other than 2, 3 or 4, for an exception code that is wrong when tax
  is owed, and when an exception applies but code 2, 3 or 4 is missing or
  incorrect. The result is entered as the filer-supplied `other_tax.line73`.
  A distribution received while a nonresident has no California additional
  tax. The FTB 3805P exception list is by exception number, not Box 7
  code, so a code-to-exception mapping is unverified.
- **Citation:** *(Source: ca-retirement-distributions.md, Additional Tax
  on Early Distributions)*

## Pitfall 15: Rental Loss Restated for a Part-Year Resident (California)

- **Mistake:** Carrying the federal rental result to column E, or
  treating the rental as non-passive because federal law allows it.
- **How to verify:** The rental has a California depreciation figure
  (FTB 3885A, no bonus depreciation, Section 179 at most $25,000). All
  rentals are passive for California, so a loss is limited by FTB 3801,
  and suspended losses from prior years are prorated between the
  resident and nonresident periods. Column E holds only the
  resident-period part for property outside California.
- **Citation:** *(Source: ca-rental-depreciation-passive.md, Depreciation
  Differences; Passive Activity Rules; Part-Year Residents and Rental
  Property)*
