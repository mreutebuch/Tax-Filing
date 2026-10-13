# California References Validation Report

Date: 2026-10-13. Scope: the nine curated rule files in `reference/curated/ca/`
against the extracted FTB text beside them. Synthetic data only; no private
data was used.

## Method

- Four independent verifier subagents received only the claims (each rule
  bullet, with its bracketed citation) and the instruction to disprove them
  using only the files in `reference/curated/ca/`. Each verdict carries a file
  location and a quote. I opened the locators for every REFUTED and REFUTED AS
  WORDED verdict I acted on.
- Arithmetic (tax tables, examples, ratios) was recomputed in Python with
  `Decimal`.
- Network access to ftb.ca.gov worked, so the five PDFs missing from this clone
  were downloaded from their `*.source.txt` URLs and compared with the tracked
  text (see Extracted text below).

## Results by file

| Files | Claims | Confirmed | Refuted as worded | Weak / inconclusive | Refuted |
|-------|-------:|----------:|------------------:|--------------------:|--------:|
| ca-2025-numbers, ca-form-540nr-line-by-line, ca-credits-withholding | 70 | 61 | 7 | 2 | 0 |
| ca-residency-part-year, ca-schedule-ca-540nr | 35 | 24 | 8 | 2 | 1 |
| ca-retirement-distributions, ca-rental-depreciation-passive | 28 | 13 | 12 | 3 | 0 |
| ca-capital-gains-part-year, ca-filing-deadlines-extension | 19 | 13 | 3 | 3 | 0 |

No number in the rate schedules, Tax Table, standard deduction, exemption
credit, phase-out or BHST rules was wrong: all 27 bracket rows match, and all
1,001 printed Tax Table ranges in all three columns equal the Rate Schedule
tax at the midpoint, rounded.

## Errors fixed (highest impact first)

1. Schedule CA HSA: the deduction is reversed in column B (line 13), not column
   C (the one outright refutation).
2. Sale of out-of-state real property: the rule said only that California taxes
   real property where it is located; residents are taxed on all income
   regardless of source, so a gain realized as a resident is taxable.
3. Passive-loss allowance: the $25,000 figure had lost its conditions (active
   participation, income phase-out, filing-status limits).
4. Rental allocation: the actual-date and daily pro-rata rule is sourced for
   partnership, S corporation and trust income, not for direct rentals. The
   conservative default is now rents by period earned and expenses by period
   incurred; daily pro-rata is flagged unverified.
5. Rental depreciation adjustment: routes through FTB 3885A to FTB 3801 for a
   passive rental; the list of depreciation differences is not exhaustive.
6. Early-distribution tax: added the 6% SIMPLE rate, the missing "incorrect
   exception code" filing trigger, and that FTB 3805P lists exceptions by
   number, not by Box 7 code.
7. Retirement: nonresident exclusion is for qualified retirement distributions
   and listed plan types, not all pensions; Worksheet I is pre-1987 basis only.
8. Self-employment tax ratio (line 15) uses column A income; line 17 uses
   column E over column D.
9. Line 91 on Form 540NR is the Individual Shared Responsibility penalty, with
   lines 92-93 between payments and overpaid/due tax; use tax is paid to the
   CDTFA. The rule file previously said the opposite.
10. SDI: not a credit or payment, but not deductible; itemizers enter it on
    Schedule CA (540NR) line 5a, column B.
11. AMT thresholds for line 71 added; Box A-C heading corrected; credits on
    lines 58-60, the Credit Chart and the TMT limit described.
12. Qualifying surviving spouse gets two personal exemption boxes in both files;
    senior credit rules (January 1, 2026 birthday; not if claimable as a
    dependent) added; dependent standard deduction worksheet named correctly.
13. Part-year capital gains: worksheet columns described correctly; the
    carryover worksheet applies only when the year-end column shows a loss.
14. FTB 3519 mailing and credit-card wording corrected; wash-sale statement
    reworded as unverified.
15. Residency: filing-status exception for joint filers; start and end dates;
    the nonresident interest and dividend rule includes accounts pledged for a
    business loan; community property wording split into what Pub. 1031 says
    and what remains unverified.

The `ca_540nr.py` and `ca_cross_check.py` scripts gained an optional
`payments.line91` input (ISR penalty from FTB 3853, default 0) so lines 92, 93,
101 and 104 follow the form.

## Scenario coverage (handoff section 4)

| # | Scenario | Rule file(s) or flag |
|---|----------|----------------------|
| 1 | MFJ, one part-year spouse | ca-residency-part-year, ca-form-540nr-line-by-line, ca-schedule-ca-540nr, ca-2025-numbers |
| 2 | Part-year wages and withholding | ca-residency-part-year, ca-credits-withholding. Community property effect flagged unverified |
| 3 | Converted rental, bonus depreciation, 1099-MISC | ca-rental-depreciation-passive. Pre-conversion expenses and direct-rental daily pro-rata flagged unverified |
| 4 | Traditional and Roth distributions | ca-retirement-distributions. Box 7 code to exception mapping flagged unverified |
| 5 | Brokerage, mixed dates | ca-capital-gains-part-year. Wash sale and non-installment stock sourcing flagged unverified |
| 6 | 1099-INT, 1098-E, tip report | ca-schedule-ca-540nr: student loan interest conforms (rule added); tip income reported separately flagged unverified |
| 7 | OBBBA federal deductions | ca-schedule-ca-540nr: general non-conformity; Schedule 1-A items flagged unverified |
| 8 | Federal extension | ca-filing-deadlines-extension: California dates; effect of a federal extension flagged unverified (no provided source mentions Form 4868) |
| 9 | Employer coverage statement | ca-form-540nr-line-by-line: line 91 box and FTB 3853 rule added; the sources do not say whether the requirement reaches nonresident months, flagged |

Every scenario has a rule or an explicit unverified flag.

## Extracted text

- PDF-sourced text: page counts match the form-feed counts for all nine PDFs
  (`2025-3801` 4, `2025-3885a` 1, `2025-540-booklet` 80, `2025-540nr-booklet`
  80, rate schedules 1, Pub. 1001 26, Pub. 1005 15, Pub. 1031 14, Pub. 1100
  17). Regenerated with poppler 24.02: identical for seven files; the two
  booklets differ only in whitespace layout of a few non-tax lines (poppler
  version difference). No file is empty.
- HTML-sourced text (seven instruction pages): every table cell appears in the
  extracted text; paragraph differences are list formatting only.
- The Tax Table in the 540NR booklet extracts with all 1,001 rows intact.

## Limits

- Only the extracted FTB text was used; no live ftb.ca.gov page was consulted
  beyond downloading the PDFs.
- The verifiers cited Pub. 1005 and 1100 PDFs only through the tracked text.
- Unresolved items are listed in the pull request description under
  "Unverified items".
- Real-return verification (spec phase 4) remains for the maintainer.
