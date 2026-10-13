# California State Tax Support — Design

Date: 2026-10-13
Status: Draft for review

## Purpose

Extend the plugin from federal-only (Form 1040) to also prepare a California
income tax return for tax year 2025. The first real filing used to validate it
is a married-filing-jointly return where one spouse was a full-year California
resident and the other became a resident partway through the year. That return
uses Form 540NR with Schedule CA (540NR), not the plain Form 540. The plugin
must support this case, and the full-year-resident Form 540 case as the simpler
subset.

## Success criteria

- A filer can go from source documents to complete Form 540NR / Schedule CA
  (540NR) values using the same four-skill pipeline as the federal return.
- Every California rule cites a curated file in `reference/curated/ca/`.
- All arithmetic runs in Python (`Decimal`), never in model text.
- California tax computed by the script matches the FTB rate schedule to the
  dollar for the test inputs.
- No personal data in any tracked file.

## Decisions

| Decision | Choice | Alternatives rejected |
|----------|--------|-----------------------|
| Structure | State layer inside the existing four skills (`state: CA` branch) | Separate `/ca-*` skills (duplicates CSV and audit logic); one `/tax-state-ca` skill (no structure for a second state) |
| Residency | Part-year support is in scope from day one | Full-year Form 540 only |
| Build order | References first, then scripts, then skill integration, then a real return | Scripts first (rules would be unsourced) |
| Unverifiable rules | Flag "I cannot verify this from provided FTB materials — check ftb.ca.gov" | Assume California conforms to federal |
| Judgment calls | Conservative position by default; show the dollar effect of the alternative | Aggressive default |

## Layout

New files:

- `reference/curated/ca/` — CA rule files, each citing FTB sources, plus
  `*.source.txt` stubs (title and URL) for each FTB booklet. FTB PDFs are
  gitignored like the IRS PDFs. Initial topics:
  - residency and part-year proration
  - Form 540NR line by line
  - Schedule CA (540NR) federal-to-California adjustments
  - 2025 California numbers (rate schedule, standard deduction, exemption
    credits)
  - credits, SDI and withholding
- `skills/tax-cheatsheet/scripts/ca_540nr.py` — Form 540NR calculation.
- `skills/tax-audit/scripts/ca_cross_check.py` — independent recomputation and
  comparison against federal values and source documents.

Changed files:

- `/tax-prep` — extracts California rows (W-2 state wages, state tax withheld,
  SDI, 1099-G state refund) into the existing CSV and prompts for residency
  dates.
- `/tax-cheatsheet` — Form 540NR and Schedule CA (540NR) walkthroughs.
- `/tax-audit` — California section; new California pitfalls in
  `docs/KNOWN-PITFALLS.md`.
- `/tax-advisor` — unchanged in this phase.
- `README.md`, `CLAUDE.md`, `.claude-plugin/plugin.json`,
  `docs/ARCHITECTURE.md` — describe state support instead of "federal only".

## Data flow

Inputs, all kept outside tracked skill files:

- `analysis/tax-doc-summary.csv` — gains California rows.
- `analysis/federal-return.json` (gitignored) — the filer's final federal line
  values, so California starts from the return as filed.
- `analysis/ca-residency.json` (gitignored) — each spouse's California
  residency start and end dates.

Calculation (`ca_540nr.py`):

1. Build Schedule CA (540NR): column A federal amounts, column B subtractions,
   column C additions, giving California-taxable income.
2. Apply the California tax rate method for part-year filers: tax on
   all-source income divided by that income, applied to California-source
   taxable income. This must be confirmed against the FTB booklet during
   reference curation before it is implemented.
3. Apply the California standard deduction, prorated exemption credits,
   withholding and SDI to produce a refund or balance due.

Outputs:

- `/tax-cheatsheet` writes `analysis/cheatsheet-540NR.md` and
  `analysis/cheatsheet-ScheduleCA.md` with each line's value and source.
- `/tax-audit` recomputes the same lines independently and compares.

Judgment items are surfaced explicitly, each with a conservative default and
the dollar effect of the alternative: rental depreciation conformity, rental
income earned before California residency began, rollovers, and the state
refund received in the year.

## Error handling

- Missing inputs: scripts return `{"error": ...}` naming the missing key.
- Unsourced rule: flagged "I cannot verify this from provided FTB materials —
  check ftb.ca.gov". Never silently assumed.
- Rounding: `Decimal` math; whole-dollar rounding only where the filed form
  rounds. Differences against the filed form are reported.

## Testing

- Unit tests for `ca_540nr.py` and `ca_cross_check.py` with inputs checkable by
  hand against FTB examples.
- Integration: a real return run end to end, tax checked against the FTB rate
  schedule.
- Adversarial verification of every California line before filing.

## Build phases

Each phase is committed separately.

1. Curate California references and source stubs.
2. `ca_540nr.py` and `ca_cross_check.py` with tests.
3. Skill integration (`/tax-prep`, `/tax-cheatsheet`, `/tax-audit`) and
   pitfalls.
4. Run a real return through the flow and verify each line.
5. Update docs and manifest; push.

## Out of scope

- California what-ifs in `/tax-advisor`.
- Itemized deductions on the California return.
- Other states.
- 2026 California estimated-tax calculation.

## Open questions

- Part-year California tax rate method and Schedule CA (540NR) column
  definitions: confirm from the 2025 FTB booklets during phase 1.
- Whether California conforms to the federal special depreciation allowance
  for the rental property: confirm from FTB sources in phase 1.
- Whether the residency start date for the part-year spouse needs more than a
  single date (for example, income earned before and after the move): confirm
  from FTB Publication 1031.
