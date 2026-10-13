# California Residency and Part-Year Proration

## Source
- FTB Publication 1031 (2025), Guidelines for Determining Resident Status — p1031.source.txt
- 2025 Form 540NR Booklet, "How Nonresidents and Part-Year Residents Are Taxed" and Schedule CA (540NR) instructions (Column E, Part-Year Resident Worksheet) — 2025-540nr-booklet.source.txt

## Applicable To
- **Forms:** Form 540NR; Schedule CA (540NR) column E and Part IV
- **Workflow Steps:** /tax-prep residency prompts (`analysis/ca-residency.json`), California tax computation, California audit

---

## Rules

### Who Files Which Form
- A full-year resident files Form 540 or 540 2EZ. If a joint return is filed and either spouse/RDP was a nonresident or part-year resident, file Form 540NR. [FTB Pub. 1031 (2025), Section C]
- Use the same filing status for California as for the federal return (except RDPs). [FTB Pub. 1031 (2025), Section D]

### Resident, Nonresident, Part-Year Resident
- A resident is present in California for other than a temporary or transitory purpose, or is domiciled in California but outside it for a temporary or transitory purpose. A nonresident is anyone who is not a resident. A part-year resident is a resident for part of the year and a nonresident for part. [FTB Pub. 1031 (2025), Section E]
- You are presumed a California resident for any taxable year in which you spend more than nine months in California. [FTB Pub. 1031 (2025), Section H]
- Residency is decided on facts and circumstances (closest connections: home, family, work, social ties, property, registrations). [FTB Pub. 1031 (2025), Sections G and H]

### How Part-Year Residents Are Taxed
- A part-year resident is taxed on all income received while a resident and only on income from California sources while a nonresident. [FTB Pub. 1031 (2025), Income Taxable by California; 2025 Form 540NR Booklet, General Information]
- Column A through column D of Schedule CA (540NR) are computed as if resident for the whole year. Column E holds the income taxable by California. [2025 Form 540NR Booklet, General Information; Schedule CA (540NR) Instructions, Column E]
- Use the Part-Year Resident Worksheet: for each income line, column A holds the amount earned or received while a California resident (from the column D amount); column B holds the amount from California sources while a nonresident; column C (A plus B) transfers to Schedule CA (540NR) column E. [Schedule CA (540NR) Instructions, Part-Year Resident Worksheet]

### Residency Dates Are Not Enough on Their Own
- One residency start date is the input for dividing wages and other dated income, but the worksheet needs separate resident-period and nonresident-period amounts for every income line, so the filer's records must show the date each item was earned or received. [Schedule CA (540NR) Instructions, Part-Year Resident Worksheet]
- Wages have their source where the services were performed. A part-year resident includes in column E all wages earned while a resident regardless of where performed; as a nonresident, only wages for services performed in California. [FTB Pub. 1031 (2025), Wages and Salaries]
- Partnership, S corporation and certain trust income is allocated by actual date of realization. Without that information, allocate the annual amount between the two periods by a daily pro-rata method. [Schedule CA (540NR) Instructions, Line 5, part-year resident amounts]
- Rental real estate: resident amounts are the profit or loss that accrued while a California resident. Nonresident amounts are profit or loss related to property located in California. Rent on property outside California earned before residency began is therefore not California-source income. [Schedule CA (540NR) Instructions, Line 5]
- Capital gains and losses: resident amounts are those from all sources while a resident; nonresident amounts come from California sources, using the Schedule D (540NR) Worksheet. [Schedule CA (540NR) Instructions, Line 7a]
- Interest and dividends: resident amounts are those received while a resident. Nonresident amounts are only interest or dividends from accounts used in a California trade or business. [Schedule CA (540NR) Instructions, Lines 2 and 3]

### Community Property
- California is a community property state. On a joint Form 540NR the chart in Pub. 1031 shows that Schedule CA (540NR) columns A-D carry all income and columns E carries all income taxable by California. [FTB Pub. 1031 (2025), How To Split Income on Form 540NR]
- Pub. 1031 example: a California-domiciled spouse working overseas under the 546-day safe harbor (nonresident) and a spouse who is a California resident file jointly; half of the overseas spouse's wages are taxable to California because California is a community property state and the other spouse is a resident. [FTB Pub. 1031 (2025), Section E, Example 3 tables]
- How domicile in a community or separate property state before the move applies to the part-year spouse's pre-move income: I cannot verify this from provided FTB materials — check ftb.ca.gov.
