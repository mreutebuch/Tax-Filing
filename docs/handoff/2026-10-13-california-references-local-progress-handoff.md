# Handoff: California references added locally; next steps for the cloud session

Date: 2026-10-13
Audience: a Claude Code cloud session continuing California state support.
Read order: this file, then `CLAUDE.md`, then
`docs/handoff/2026-10-13-california-state-support-handoff.md` (original task
and build phases), then
`docs/superpowers/plans/2026-10-13-california-state-support-plan.md`.

## 0. Privacy: no real tax data in any tracked file

Never write real tax data into a tracked file, commit message, PR text, test,
example or report: no names, SSNs, addresses, employers, account numbers, real
dollar amounts or real dates. Use synthetic inputs only.

- Keep the `.gitignore` entries for `my-tax-docs/`, `my tax files/` and
  `analysis/`; never weaken them.
- Stage files by explicit path; never `git add -A` or `git add -f`.
- Run `python -I scripts/check_private_data.py` before every commit and push.
- If private data is ever found in a tracked file or in history, stop, do not
  push, and report it without repeating the data.

## 1. State of the work

- Branch: `claude/california-state-support-m941pv`, pull request #1 against
  `main` (open). Everything below is pushed.
- Tests: `python -m unittest discover -s tests` runs 28 tests, all passing.
- Privacy check passes.
- The cloud session built phases 1-3 (references, `ca_540nr.py`,
  `ca_cross_check.py`, skill integration, docs). Phase 4 (the maintainer's
  real return) is still the maintainer's to run locally.

## 2. Progress since the session moved to the maintainer's machine

1. **More FTB publications downloaded** into `reference/curated/ca/`
   (2025 versions): Pub. 1005 (pensions and IRAs), Pub. 1100 (nonresident and
   change-of-residency method), FTB 3885A and 3801 (forms and instructions),
   FTB 3805P instructions, Schedule D (540NR) and Schedule D (540)
   instructions, Schedule P (540NR) instructions, Schedule CA (540NR)
   instructions, and the Form 540 booklet. Each has a `*.source.txt` stub.
   FTB 3519 instructions returned a 404 and were not fetched.
2. **Four new curated rule files**, each rule citing its FTB source:
   - `ca-retirement-distributions.md` (nonresident-period retirement income,
     part-year pension split, IRA basis after moving in, Roth IRA, the 2½%
     early-distribution tax on FTB 3805P)
   - `ca-rental-depreciation-passive.md` (no bonus-depreciation conformity,
     $25,000 Section 179 cap, all rentals passive, part-year allocation of
     suspended losses)
   - `ca-capital-gains-part-year.md` (Schedule D (540NR) worksheet, carryover
     proration by days)
   - `ca-filing-deadlines-extension.md` (April 15 payment, October 15 filing,
     FTB 3519)
   They were chosen from the document types in the private folders. The files
   are generic and contain no personal facts.
3. **Repository policy changed:** only `reference/curated/ca/*.pdf` is
   gitignored. HTML instruction pages and extracted `.txt` files are tracked.
4. **Extracted text regenerated.** The text for each PDF is now produced by
   poppler 26.09.0 `pdftotext -layout`; HTML pages are converted with table
   rows preserved. Git for Windows ships Xpdf 4.00 as `pdftotext`, which splits
   table cells across lines and must not be used for the Tax Table.
5. **Test portability fix:** `test_every_printed_row` decodes `pdftotext`
   output as UTF-8 and skips (with a message) when fewer than 1,001 rows are
   read. With poppler it passes and checks the calculator against every printed
   Tax Table range.

## 3. What is left (suggested order)

1. **Wire the new references into the skills.** They are curated but no skill
   cites them yet.
   - `/tax-prep`: add 1099-R rows (Box 1, 2a, 2b, 7 distribution code) and a
     prompt for each distribution's date; add 1099-B transaction dates; add
     the 1099-MISC rents row. Cite `ca-retirement-distributions.md` and
     `ca-capital-gains-part-year.md`.
   - `/tax-cheatsheet`: add rows to the California reference table for the
     four new files; add the Schedule CA lines 4a-4b, 5a-5b, 7a, and
     Schedule D (540NR) worksheet steps; add FTB 3885A and 3801 as inputs to
     the Schedule CA line 5 row.
   - `/tax-audit`: add pitfalls 13-15 to `docs/KNOWN-PITFALLS.md`
     (retirement income during a nonresident period; 2½% tax and Box 7 codes;
     rental passive loss restated for a part-year resident) and a short
     California deadline check.
2. **Extend `ca_540nr.py` only if needed.** The FTB 3805P additional tax
   goes in `other_tax.line73` today; add a documented input and a test if the
   skills need it. Keep arithmetic in `Decimal` and tests synthetic.
3. **Update `CLAUDE.md` file-locations** to say that extracted text and HTML
   pages under `reference/curated/ca/` are tracked and PDFs are not. Write it
   as current state, not history.
4. **Update the PR description** if more changes land, and keep the list of
   unverified items in it accurate.
5. **Resolve the open unverified items where an FTB source exists**, otherwise
   leave them flagged: community-property treatment of a part-year spouse's
   pre-move income, whether a federal Form 4868 changes any California
   requirement, and California exceptions to the early-distribution tax by
   code.

## 4. Scenarios the curated references must support (generalized, no private data)

Intent: the references in `reference/curated/ca/` were collected for one
class of return. The scenarios below describe that class in general terms
only. They do not describe any real filer, and nothing here may be refined
with real facts. Use them to judge whether each reference is sufficient,
correct and complete for its purpose.

| # | Generalized scenario | Curated files that should answer it |
|---|----------------------|--------------------------------------|
| 1 | Married filing jointly; one spouse a California resident all year, the other becoming a California resident partway through the year (Form 540NR with Schedule CA (540NR)). | `ca-residency-part-year.md`, `ca-form-540nr-line-by-line.md`, `ca-schedule-ca-540nr.md`, `ca-2025-numbers.md` |
| 2 | The part-year spouse earned wages from an employer outside California before the move and from the same or another employer after it; wages and withholding appear on W-2s. | `ca-residency-part-year.md`, `ca-credits-withholding.md` |
| 3 | A residential property located outside California, owned before the move and converted from personal use to a rental during the year, with federal bonus (additional first-year) depreciation, repairs and improvements, prepaid contracts, and a rent statement on Form 1099-MISC. | `ca-rental-depreciation-passive.md`, `ca-schedule-ca-540nr.md` |
| 4 | Retirement distributions during the year from both a traditional and a Roth account on Forms 1099-R, some received before the move and some after. | `ca-retirement-distributions.md`, `ca-schedule-ca-540nr.md` |
| 5 | A taxable brokerage account with a consolidated Form 1099 (interest, dividends, sales), some activity before the move and some after. | `ca-capital-gains-part-year.md`, `ca-residency-part-year.md` |
| 6 | Interest income on a Form 1099-INT; student loan interest on a Form 1098-E; an employer tip and other compensation report attached to the W-2. | `ca-schedule-ca-540nr.md` (student loan interest, OBBBA non-conformity), `ca-residency-part-year.md` |
| 7 | Federal AGI is the starting point; federal below-the-line deductions created by the One Big Beautiful Bill Act do not flow into Form 540NR line 13. | `ca-form-540nr-line-by-line.md`, `ca-schedule-ca-540nr.md` |
| 8 | A federal extension was requested; California payment and filing dates must be stated correctly. | `ca-filing-deadlines-extension.md` |
| 9 | Health coverage offered by an employer (Form 1095-C style statement) is on file; check whether the return needs any California coverage reporting. | `ca-form-540nr-line-by-line.md` (line 91 text in the booklet) |

Known gaps relative to these scenarios (keep flagged, do not guess):
- Community-property treatment of the part-year spouse's pre-move income.
- Whether a federal extension request changes any California requirement.
- California exceptions to the 2½% early-distribution tax by distribution code.
- California treatment of expenses paid before a converted property was
  available for rent (follows the federal characterization).
- Scenarios 6 (tip report) and 9 (coverage reporting) have thin coverage; if
  the booklet or Pub. 1001 text settles them, add a rule with its citation,
  otherwise say "I cannot verify this from provided FTB materials — check
  ftb.ca.gov".

## 5. Validation requested before the maintainer runs the plugin

The maintainer intends to run the plugin on the real return later the same
day, so the cloud session should first validate the downloaded documents and
the curated files against each other. Do this with synthetic data only.

1. Run the `adversarial-verification` skill on the curated files, one file at
   a time, with the extracted text beside each (`*.txt` next to the PDF or HTML
   it came from). For each rule check:
   - the cited source file and section exist and say what the rule says;
   - every number (dollar amount, percentage, threshold, date, line number)
     matches the extracted text exactly;
   - no rule goes beyond its source (conformity assumed, a federal rule
     imported, a California rule stated without a citation);
   - each unverified item uses the exact wording
     "I cannot verify this from provided FTB materials — check ftb.ca.gov".
2. Check that every scenario in section 4 has a curated rule or an explicit
   unverified flag, and report any scenario with neither.
3. Re-run `ca_540nr.py` and `ca_cross_check.py` on synthetic inputs that
   exercise scenarios 1-5 in general terms (part-year wages, a rental-style
   row with a depreciation add-back, a retirement row split by period, a gain
   split by period) and confirm the line values against hand calculations.
4. Confirm the extracted text is a faithful copy of each source (page counts,
   table rows intact, no empty files). The text was produced with poppler
   26.09; regenerate with poppler, never with Xpdf.
5. Record the findings in a short report under `docs/` (no private data),
   fix errors in the curated files, and list anything unresolved in the pull
   request description under "Unverified items".
## 6. Environment notes

- The GitHub MCP server failed to connect locally; `gh` CLI is authenticated
  locally and can read and edit the PR. In the cloud use the GitHub MCP tools.
- Regenerating extracted text needs poppler, not Xpdf:
  `pdftotext -layout -enc UTF-8 <file>.pdf <file>.txt`.
- Never use `git add -A`; stage by explicit path.

## 7. Stop conditions

Same as the original handoff: stop and report if the privacy check fails, if
private data appears in a tracked file or history, if an FTB source contradicts
the design, or if tests cannot be made to pass.

## 8. Done means

- All tests and the privacy check pass.
- Every California rule in references, skills and scripts cites a file in
  `reference/curated/ca/`.
- The skills reference the new curated files.
- The validation in section 5 has been run and its report committed.
- The PR description is current and the real-return verification (spec
  phase 4) is stated as remaining for the maintainer.
