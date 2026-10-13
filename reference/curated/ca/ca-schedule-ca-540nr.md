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
- HSA: California does not conform. Employer contributions in W-2 box 12 code W are added to column C line 1h; the deduction taken for HSA contributions is added back in column C on the adjustment line (Part II line 13 column B in Pub. 1001); interest and dividends earned in the HSA are added in column C. [FTB Pub. 1001 (2025), Health Savings Account (HSA)]
- Rollover from an Archer MSA to an HSA is a taxable distribution for California. [FTB Pub. 1001 (2025), Archer MSA to an HSA]
- 529-to-Roth IRA rollover: California does not conform to the federal provision. The rollover distribution is included in California taxable income and is subject to an additional 2.5% tax. [Schedule CA (540NR) Instructions, Special Rules for Certain Distributions from Qualified IRC Section 529 Tuition Plans]

### Depreciation (rental and business property)
- California does not conform to the federal additional first-year (bonus) depreciation, including the OBBBA 100% allowance for property acquired and placed in service after January 19, 2025. [FTB Pub. 1001 (2025), Additional depreciation (IRC Section 168(k))]
- Use form FTB 3885A to figure the adjustment (column B or C on line 3 for business, line 5 for rental and pass-through). Passive loss limits for rentals use form FTB 3801. [FTB Pub. 1001 (2025); Schedule CA (540NR) Instructions, Line 5]
- The California depreciation amount for a specific asset is an FTB 3885A computation: the plugin takes the resulting adjustment as an input and does not derive it.

### Capital Gains
- California taxes long-term and short-term capital gains as regular income; there is no special rate. [Schedule CA (540NR) Instructions, Line 7a]

### OBBBA Non-Conformity
- In general California does not conform to the One Big Beautiful Bill Act. Specific adjustments exist; check each Schedule CA (540NR) line instruction (the increased SALT cap is relevant only when itemizing; see Out of Scope in the design spec). [Schedule CA (540NR) Instructions, General Information]
- Federal deductions and exclusions created by the OBBBA that appear as federal return lines (such as Schedule 1-A items) have no California equivalent unless a Schedule CA (540NR) line says so: I cannot verify this from provided FTB materials — check ftb.ca.gov.

### Column E Items Used Here
- Wages: resident-period wages plus wages for services performed in California while a nonresident. [FTB Pub. 1031 (2025), Wages and Salaries]
- Rental, interest, dividends, gains: see ca-residency-part-year.md.
- Adjustments to income (Section C): self-employment tax and self-employed health insurance deductions are limited by the ratio of self-employment income in column E to column D. [Schedule CA (540NR) Instructions, Lines 15 and 17]
