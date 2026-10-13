# Schedule CA (540NR) — California Adjustments

## Source
- 2025 Form 540NR Booklet, Schedule CA (540NR) and its instructions, Part-Year Resident Worksheet — 2025-540nr-booklet.source.txt
- FTB Publication 1001 (2025), Supplemental Guidelines to California Adjustments — p1001.source.txt

## Applicable To
- **Forms:** Schedule CA (540NR) Parts II and IV
- **Workflow Steps:** /tax-cheatsheet Schedule CA walkthrough, /tax-audit

---

## Rules

### Columns
- A: federal amounts. B: subtractions (income taxable federally but not by California). C: additions. D: total amounts using California law as if a resident for the whole year = A minus B plus C. E: California amounts (income earned or received as a resident plus California-source income as a nonresident). [2025 Form 540NR Booklet, Schedule CA (540NR) column headings]
- Do not subtract non-California-source income in columns A-D. [FTB Pub. 1031 (2025), Avoid Common Mistakes on Form 540NR]

### Part IV (California Taxable Income)
- Line 1: California AGI = Part II line 27 column E. Line 2: deduction from Part III line 30 (itemized or standard). Line 3: deduction percentage = column E line 27 divided by column D line 27, four decimals, capped at 1.0000, zero if negative. Line 4: line 2 times line 3. Line 5: line 1 minus line 4, not less than zero; this is Form 540NR line 35. [2025 Form 540NR Booklet, Schedule CA (540NR) Part IV]

### Adjustments Included in This Plugin
- State income tax refund (Part II Section B line 1): California does not tax the state income tax refund; enter in column B the amount in column A. [Schedule CA (540NR) Instructions, Section B line 1]
- Unemployment compensation: enter in column B the amount in column A. [Schedule CA (540NR) Instructions, Section B line 7]
- Social security benefits: enter in column B the federal taxable amount. [FTB Pub. 1001 (2025), Social Security Benefits; Schedule CA (540NR) Instructions, Section A line 6]
- HSA: California does not conform. Employer contributions in W-2 box 12 code W are added to Part II Section A line 1h, column C. The HSA deduction is reversed by entering the line 13 column A amount on line 13, column B. Interest and dividends earned in the HSA are also added in column C on their income lines. [FTB Pub. 1001 (2025), Health Savings Account (HSA); Schedule CA (540NR) Instructions, Line 13]
- Rollover from an Archer MSA to an HSA is a taxable distribution for California. [FTB Pub. 1001 (2025), Archer MSA to an HSA]
- 529-to-Roth IRA rollover: California does not conform to the federal provision. The rollover distribution is included in California taxable income and is subject to an additional 2.5% tax. [Schedule CA (540NR) Instructions, Special Rules for Certain Distributions from Qualified IRC Section 529 Tuition Plans]

### Depreciation (rental and business property)
- California does not conform to the federal additional first-year (bonus) depreciation, including the OBBBA 100% allowance for property acquired and placed in service after January 19, 2025. [FTB Pub. 1001 (2025), Additional depreciation (IRC Section 168(k))]
- For a rental or pass-through with a passive loss, FTB 3801 figures the total adjustment for line 5 (FTB 3885A is an input worksheet to it). FTB 3885A figures the adjustment directly only for nonpassive activities or passive activities with gains. [Schedule CA (540NR) Instructions, Line 5; 2025 FTB 3885A Instructions, Part I Line 1]
- The California depreciation amount for a specific asset is an FTB 3885A computation. This plugin takes the resulting adjustment as an input (a column C addition) and does not derive it.

### Capital Gains
- California taxes long-term and short-term capital gains as regular income; there is no special rate. [Schedule CA (540NR) Instructions, Line 7a]

### OBBBA Non-Conformity
- In general California does not conform to the One Big Beautiful Bill Act. Specific adjustments exist; check each Schedule CA (540NR) line instruction (the increased SALT cap is relevant only when itemizing; see Out of Scope in the design spec). [Schedule CA (540NR) Instructions, General Information]
- In general California does not conform to the OBBBA. No provided FTB material addresses federal Schedule 1-A items (for example tips, overtime or car-loan interest deductions), so whether any has a California equivalent: "I cannot verify this from provided FTB materials — check ftb.ca.gov".

### Student Loan Interest and Tips
- California law conforms to federal law on the student loan interest deduction (Schedule CA (540NR) line 21), except for non-California-domiciled military taxpayers, who use the Student Loan Interest Deduction Worksheet. [Schedule CA (540NR) Instructions, Line 21]
- Wages, salaries, tips and other compensation received while a California resident go in column E on the applicable line; for the nonresident period, only compensation for services performed in California. [Schedule CA (540NR) Instructions, Part-Year Resident Worksheet, California resident amounts and California nonresident amounts]
- Treatment of tip income reported separately from W-2 box 1 (for example unreported tips, or federal deductions for tips created by the OBBBA): I cannot verify this from provided FTB materials — check ftb.ca.gov.

### Column E Items Used Here
- Wages: resident-period wages plus wages for services performed in California while a nonresident. [FTB Pub. 1031 (2025), Wages and Salaries]
- Rental, interest, dividends, gains: see ca-residency-part-year.md.
- Adjustments to income (Section C): the line 15 self-employment tax deduction is the column D amount times a ratio of column A self-employment income (resident-period income from all sources plus California-source income as a nonresident) to total column A self-employment income. The line 17 self-employed health insurance deduction uses column E self-employment income divided by column D. Each ratio is capped at 1.00 and floored at zero. [Schedule CA (540NR) Instructions, Lines 15 and 17]
