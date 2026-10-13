# Tax Filing Skills 2025

Skills for preparing, filing, and optimizing a U.S. federal (Form 1040) and
California (Form 540NR with Schedule CA (540NR), including part-year
residents) tax return using Claude Code. Built for tax year 2025.

## Setup
1. Place your tax documents in the `my-tax-docs/` folder
2. Point Claude Code at this project
3. Start with /tax-prep to extract your document values (for California it also asks for residency dates and writes `analysis/ca-residency.json`)
4. Use /tax-cheatsheet as you fill each form (federal first, then Form 540NR and Schedule CA (540NR))
5. Run /tax-audit before submitting (includes the California cross-check)
6. After filing, use /tax-advisor for next-year planning (federal only)

## File Locations
| What | Where |
|------|-------|
| Curated IRS references | reference/curated/ |
| Curated California (FTB) references (rule files `ca-*.md`; extracted text `*.txt` and HTML instruction pages are tracked; source PDFs are gitignored and fetched from the URL in each `*.source.txt`) | reference/curated/ca/ |
| Reference curation guide | reference/HOW-TO-CURATE.md |
| Known pitfalls | docs/KNOWN-PITFALLS.md |
| Example outputs | examples/ |
| California calculation script | skills/tax-cheatsheet/scripts/ca_540nr.py |
| California cross-check script | skills/tax-audit/scripts/ca_cross_check.py |
| Tests (`python -m unittest discover -s tests`) | tests/ |
| Privacy guard | scripts/check_private_data.py |
| Your tax documents | my-tax-docs/ and my tax files/ (gitignored) |
| Generated analysis, including analysis/ca-residency.json | analysis/ (gitignored) |

## Rules
1. Every tax rule must cite a file in reference/curated/ (California rules cite reference/curated/ca/)
2. If unverifiable: "I cannot verify this — check IRS.gov" (California: "I cannot verify this from provided FTB materials — check ftb.ca.gov"). Never assume California conforms to federal law
3. All math via Python scripts — no LLM arithmetic
4. No personal information stored in skill files
5. Forms must leave SSN, bank, and signature fields blank
6. Private data never leaves the maintainer's machine. The protected folders are `my-tax-docs/`, `my tax files/` and `analysis/`. Never weaken or remove their `.gitignore` entries, never use `git add -f` or `git add -A` where private files could exist (stage by explicit path), and run `python -I scripts/check_private_data.py` before every commit and every push. All test inputs and examples must be synthetic
7. On unsettled judgment calls take the conservative position (report more tax) and show the dollar effect of the alternative

## Disclaimer
These skills assist with tax return preparation. They do not constitute tax advice. Verify all numbers against source documents. Consult a qualified tax professional for your specific situation.
