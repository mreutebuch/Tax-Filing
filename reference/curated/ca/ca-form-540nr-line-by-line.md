# Form 540NR Line by Line (2025)

## Source
- 2025 Form 540NR Booklet, Form 540NR and its line instructions — 2025-540nr-booklet.source.txt
- 2025 California Tax Rate Schedules — 2025-540-tax-rate-schedules.source.txt

## Applicable To
- **Forms:** Form 540NR
- **Workflow Steps:** /tax-cheatsheet California walkthrough, /tax-audit California section

---

## Rules

### Exemptions (lines 6-11)
- Line 7 personal x $153 (1 box for Single/MFS/HoH, 2 for MFJ); line 8 blind x $153; line 9 senior x $153; line 10 dependents x $475; line 11 is their sum. If line 6 (someone can claim you) is checked, line 7 follows the booklet table. [2025 Form 540NR Booklet, Lines 6-11]
- Numbers: see ca-2025-numbers.md.

### Total Taxable Income (lines 12-19)
- Line 12: California wages from W-2 box 16. [2025 Form 540NR Booklet, Line 12]
- Line 13: federal AGI from Form 1040 line 11b. [2025 Form 540NR Booklet, Line 13]
- Line 14: Schedule CA (540NR) Part II line 27 column B (subtractions). Line 15: line 13 minus line 14. Line 16: Part II line 27 column C (additions). Line 17: line 15 plus line 16, which must equal Part II line 27 column D. [2025 Form 540NR Booklet, Lines 14-17]
- If column B or C is negative, move it as a positive number to the other line. [2025 Form 540NR Booklet, Lines 14 and 16]
- Line 18: larger of California itemized deductions (Schedule CA (540NR) Part III line 30) or the California standard deduction. Line 19: line 17 minus line 18, not less than zero. [2025 Form 540NR Booklet, Lines 18-19]

### California Taxable Income (lines 31-40)
- Line 31: tax on line 19 from the Tax Table (line 19 of $100,000 or less) or Tax Rate Schedule (over $100,000). [2025 Form 540NR Booklet, Line 31]
- Line 32: Schedule CA (540NR) Part IV line 1 (California AGI, column E). Line 35: Part IV line 5 (California taxable income). [2025 Form 540NR Booklet, Lines 32 and 35]
- Line 36: California tax rate = line 31 divided by line 19, rounded to four decimals. [2025 Form 540NR Booklet, Line 36]
- Line 37: line 35 times line 36. Line 38: exemption credit percentage = line 35 divided by line 19, capped at 1.0000, four decimals. Line 39: line 11 times line 38 (or the AGI Limitation Worksheet result when AGI exceeds the threshold). Line 40: line 37 minus line 39, not less than zero. [2025 Form 540NR Booklet, Lines 37-40]
- Line 41: tax from Schedule G-1 or FTB 5870A (not computed here). Line 42: line 40 plus line 41. [2025 Form 540NR Booklet, Lines 41-42]

### Credits and Total Tax (lines 50-74)
- Line 62: add line 50 and lines 55 through 61. Line 63: line 42 minus line 62, not less than zero. [2025 Form 540NR Booklet, Lines 62-63]
- Line 72: Behavioral Health Services Tax, see ca-2025-numbers.md. Line 74: line 63 plus lines 71, 72 and 73. [2025 Form 540NR Booklet, Lines 72-74]
- Special credits on lines 51-53 are prorated by the line 38 percentage. [2025 Form 540NR Booklet, Lines 54-55]
- Credits and limits other than the above (child and dependent care, renter's credit, other state tax credit): see ca-credits-withholding.md.

### Payments, Refund, Balance Due (lines 81-104)
- Line 81 California income tax withheld, line 82 estimated tax and other payments, line 83 Form 592-B/593 withholding; line 88 total payments is line 81 through line 87. [2025 Form 540NR Booklet, Lines 81-88]
- Overpaid tax (line 101) is line 92 minus line 74 when positive; tax due (line 104) is line 74 minus line 92 when positive. [2025 Form 540NR Booklet, Lines 101 and 104]
- Use tax (line 91 of Form 540; not on Form 540NR's payment block) and voluntary contributions are not computed here: I cannot verify this from provided FTB materials — check ftb.ca.gov.

### Form Handling
- Leave SSN, bank account and signature fields blank on any saved form (repo rule 5 in CLAUDE.md).
