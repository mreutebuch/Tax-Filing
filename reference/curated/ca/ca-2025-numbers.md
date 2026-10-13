# California 2025 Numbers

## Source
- 2025 California Tax Rate Schedules (Schedules X, Y, Z) — 2025-540-tax-rate-schedules.source.txt
- 2025 Form 540NR Booklet — 2025-540nr-booklet.source.txt (Form 540NR lines 7-11, 18, 31, 39; Schedule CA (540NR) Part III line 30; 2025 California Tax Table)

## Applicable To
- **Forms:** Form 540NR lines 7-11, 18, 31, 36-40; Schedule CA (540NR) Part IV
- **Workflow Steps:** California tax computation (`ca_540nr.py`), California audit (`ca_cross_check.py`)

---

## Rules

### Filing Status Schedules
- Schedule X: Single and Married/RDP Filing Separately. Schedule Y: Married/RDP Filing Jointly and Qualifying Surviving Spouse/RDP. Schedule Z: Head of Household. [2025 California Tax Rate Schedules]
- Use the Tax Table if Form 540NR line 19 is $100,000 or less; use the Tax Rate Schedule if it is over $100,000. [2025 Form 540NR Booklet, Line 31]

### Tax Rate Schedule Y (MFJ / Qualifying Surviving Spouse)

| Over | But not over | Base tax | Rate | Of the amount over |
|------|--------------|----------|------|--------------------|
| $0 | $22,158 | $0.00 | 1.00% | $0 |
| $22,158 | $52,528 | $221.58 | 2.00% | $22,158 |
| $52,528 | $82,904 | $828.98 | 4.00% | $52,528 |
| $82,904 | $115,084 | $2,044.02 | 6.00% | $82,904 |
| $115,084 | $145,448 | $3,974.82 | 8.00% | $115,084 |
| $145,448 | $742,958 | $6,403.94 | 9.30% | $145,448 |
| $742,958 | $891,542 | $61,972.37 | 10.30% | $742,958 |
| $891,542 | $1,485,906 | $77,276.52 | 11.30% | $891,542 |
| $1,485,906 | and over | $144,439.65 | 12.30% | $1,485,906 |

[2025 California Tax Rate Schedules, Schedule Y]

### Tax Rate Schedule X (Single / MFS)

| Over | But not over | Base tax | Rate | Of the amount over |
|------|--------------|----------|------|--------------------|
| $0 | $11,079 | $0.00 | 1.00% | $0 |
| $11,079 | $26,264 | $110.79 | 2.00% | $11,079 |
| $26,264 | $41,452 | $414.49 | 4.00% | $26,264 |
| $41,452 | $57,542 | $1,022.01 | 6.00% | $41,452 |
| $57,542 | $72,724 | $1,987.41 | 8.00% | $57,542 |
| $72,724 | $371,479 | $3,201.97 | 9.30% | $72,724 |
| $371,479 | $445,771 | $30,986.19 | 10.30% | $371,479 |
| $445,771 | $742,953 | $38,638.27 | 11.30% | $445,771 |
| $742,953 | and over | $72,219.84 | 12.30% | $742,953 |

[2025 California Tax Rate Schedules, Schedule X]

### Tax Rate Schedule Z (Head of Household)

| Over | But not over | Base tax | Rate | Of the amount over |
|------|--------------|----------|------|--------------------|
| $0 | $22,173 | $0.00 | 1.00% | $0 |
| $22,173 | $52,530 | $221.73 | 2.00% | $22,173 |
| $52,530 | $67,716 | $828.87 | 4.00% | $52,530 |
| $67,716 | $83,805 | $1,436.31 | 6.00% | $67,716 |
| $83,805 | $98,990 | $2,401.65 | 8.00% | $83,805 |
| $98,990 | $505,208 | $3,616.45 | 9.30% | $98,990 |
| $505,208 | $606,251 | $41,394.72 | 10.30% | $505,208 |
| $606,251 | $1,010,417 | $51,802.15 | 11.30% | $606,251 |
| $1,010,417 | and over | $97,472.91 | 12.30% | $1,010,417 |

[2025 California Tax Rate Schedules, Schedule Z]

### Rounding the Schedule Result
- Compute base tax plus rate times the excess over the bracket floor, round that to two decimals, then round the final tax to whole dollars. Example from the FTB: taxable income $125,000 on Schedule Y gives $3,974.82 + $793.28 = $4,768.10, entered as $4,768. [2025 California Tax Rate Schedules, How to Figure Tax]

### Tax Table (line 19 of $100,000 or less)
- The Tax Table lists $100 ranges (the first range is $1-$50, then $51-$150, $151-$250 and so on). Filing statuses 1 and 3 use the Single/MFS column, 2 and 5 use the joint column, 4 uses the Head of Household column. [2025 Form 540NR Booklet, 2025 California Tax Table]
- The table amount equals the Rate Schedule tax at the midpoint of the range (the round hundred: 100, 200, ...; the last range $99,951-$100,000 uses $99,975), rounded to whole dollars (for example, range $12,951-$13,050 for Single is $149 = $110.79 + 2% x ($13,000 - $11,079), rounded; the same range for joint is $130 = 1% x $13,000). [2025 Form 540NR Booklet, 2025 California Tax Table; all 1,001 printed ranges checked in all three filing-status columns]

### Standard Deduction
- Single or Married/RDP filing separately: $5,706. Married/RDP filing jointly, Head of household, Qualifying surviving spouse/RDP: $11,412. [2025 Form 540NR Booklet, Line 18]
- If someone can claim you as a dependent, use the California Standard Deduction Worksheet for Dependents (minimum $1,350). [2025 Form 540NR Booklet, Line 18]

### Exemption Credits (Form 540NR lines 7-10)
- Personal: $153 per box (1 for Single, MFS, HoH; 2 for MFJ and Qualifying surviving spouse/RDP). Blind: $153 each. Senior (65 or older by December 31, 2025; a January 1, 2026 birthday counts as 65 on December 31, 2025): $153 each. Do not claim the senior credit if someone else can claim you as a dependent. Dependent: $475 each. [2025 Form 540NR Booklet, Form 540NR lines 7-10]
- Line 11 exemption amount is the sum of lines 7 through 10. [2025 Form 540NR Booklet, Line 11]

### Exemption Credit Phase-Out (Form 540NR line 39)
- If Form 540NR line 13 (federal AGI) is more than $252,203 (Single, MFS), $504,411 (MFJ, Qualifying surviving spouse/RDP) or $378,310 (HoH), complete the AGI Limitation Worksheet. [2025 Form 540NR Booklet, Line 39]
- Worksheet: excess = line 13 minus threshold; d = excess divided by $2,500 ($1,250 if MFS), rounded up to the next whole number; e = d x $6; credits for lines 7, 8, 9 are reduced by e per box (not below zero); credits for line 10 are reduced by e per dependent (not below zero); the sum is then multiplied by the line 38 percentage. [2025 Form 540NR Booklet, Line 39 AGI Limitation Worksheet]

### Alternative Minimum Tax
- Alternative minimum tax (line 71) is not computed by this plugin. You may owe AMT if total income is more than $123,667 (MFJ, Qualifying surviving spouse/RDP), $92,749 (Single, HoH) or $61,830 (MFS). [2025 Form 540NR Booklet, Line 71]
- Schedule P (540NR) is also needed when the Box A, B or C tests in the booklet apply; they test whether credits are limited by tentative minimum tax. Box C thresholds for line 17 are $347,808 (Single, HoH), $463,745 (MFJ, Qualifying surviving spouse/RDP), $231,868 (MFS). [2025 Form 540NR Booklet, Special Credits, Boxes A-C]

### Behavioral Health Services Tax (line 72)
- If California taxable income (line 35) is more than $1,000,000, the tax is 1% of (line 35 minus $1,000,000), in whole dollars. [2025 Form 540NR Booklet, Line 72]
