# California Credits, SDI and Withholding

## Source
- 2025 Form 540NR Booklet, lines 50-61 and 81-83, What's New (State Disability Insurance) — 2025-540nr-booklet.source.txt

## Applicable To
- **Forms:** Form 540NR lines 50-63, 81-83
- **Workflow Steps:** /tax-prep California rows, California tax computation, /tax-audit

---

## Rules

### Withholding (line 81)
- Line 81 is California income tax withheld from W-2 box 17, W-2G box 15, 1099-DIV box 16, 1099-INT box 17, 1099-K box 8, 1099-MISC box 16, 1099-NEC box 5, 1099-OID box 14 and 1099-R box 14. [2025 Form 540NR Booklet, Line 81]
- Do not include city, local or county tax, tax withheld by other states, or nonresident/real estate withholding from Forms 592-B or 593 (use line 83 for those). [2025 Form 540NR Booklet, Lines 81 and 83]
- Estimated tax payments and extension payments go on line 82. [2025 Form 540NR Booklet, Line 82]

### SDI
- Beginning in 2024 California removed the taxable wage limit and maximum withholding for SDI; all wages are subject to SDI. The excess SDI line was removed from the return (the line is "reserved for future use"). Because of this, SDI shown on W-2 (box 14) is not a credit on Form 540NR. [2025 Form 540NR Booklet, What's New, State Disability Insurance]
- SDI is not entered anywhere on Form 540NR; the plugin records it only to cross-check W-2 box 14 and does not credit it. [2025 Form 540NR Booklet, What's New, State Disability Insurance]

### Credits Supported
- Exemption credits: see ca-2025-numbers.md. [2025 Form 540NR Booklet, Lines 7-11 and 39]
- Credits on lines 50-61 are otherwise entered by the filer from the matching form. Nonrefundable child and dependent care credit requires federal AGI of $100,000 or less and care provided in California (line 50). [2025 Form 540NR Booklet, Line 50]
- Joint custody head of household and dependent parent credits (maximum $610) and senior head of household credit (maximum $1,860) are prorated by the line 38 percentage. [2025 Form 540NR Booklet, Lines 51-55]
- Other credits: I cannot verify this from provided FTB materials — check ftb.ca.gov. The plugin accepts a total credits amount (line 62) as a filer-supplied input.
- Credits cannot reduce line 63 below zero. [2025 Form 540NR Booklet, Line 63]
