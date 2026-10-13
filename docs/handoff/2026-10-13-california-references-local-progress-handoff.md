# Handoff: California references added locally; next steps for the cloud session

Date: 2026-10-13
Audience: a Claude Code cloud session continuing California state support.
Read order: this file, then `CLAUDE.md`, then
`docs/handoff/2026-10-13-california-state-support-handoff.md` (original task,
still valid for the rules in its section 0), then
`docs/superpowers/plans/2026-10-13-california-state-support-plan.md`.

## 0. The vital rule: never leak private tax data

Same as the original handoff. Protected folders: `my-tax-docs/`,
`my tax files/`, `analysis/` (all gitignored, all absent from a cloud clone).
Never weaken their `.gitignore` entries, never `git add -f` or `git add -A`,
stage by explicit path, and run `python -I scripts/check_private_data.py`
before every commit and push. Do not record facts from the private folders in
any tracked file, including this one.

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

## 4. Environment notes

- The GitHub MCP server failed to connect locally; `gh` CLI is authenticated
  locally and can read and edit the PR. In the cloud use the GitHub MCP tools.
- Regenerating extracted text needs poppler, not Xpdf:
  `pdftotext -layout -enc UTF-8 <file>.pdf <file>.txt`.
- Never use `git add -A`; stage by explicit path.

## 5. Stop conditions

Same as the original handoff: stop and report if the privacy check fails, if
private data appears in a tracked file or history, if an FTB source contradicts
the design, or if tests cannot be made to pass.

## 6. Done means

- All tests and the privacy check pass.
- Every California rule in references, skills and scripts cites a file in
  `reference/curated/ca/`.
- The skills reference the new curated files.
- The PR description is current and the real-return verification (spec
  phase 4) is stated as remaining for the maintainer.
