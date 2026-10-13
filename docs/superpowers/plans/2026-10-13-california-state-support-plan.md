# California State Support — Implementation Plan

Spec: `docs/superpowers/specs/2026-10-13-california-state-support-design.md` (approved).
Rules: all synthetic data only; run `python -I scripts/check_private_data.py` before every commit and push; stage files by explicit path.

## Phase 1 — References (done)
- `reference/curated/ca/*.md` with `.source.txt` stubs; FTB PDFs and extracted text gitignored.
- Spec open questions resolved.

## Phase 2 — Scripts and tests
1. `skills/tax-cheatsheet/scripts/ca_540nr.py`
   - Input: one JSON string. Output: one JSON object. `Decimal` only. Errors as `{"error": ...}`.
   - Inputs: `filing_status`, `federal_agi`, `ca_wages`, `lines` (Schedule CA rows with columns A, B, C and column E split into resident-period and California-source nonresident-period amounts), `exemptions`, `credits`, `payments`, optional `scenarios` (alternate row values for judgment calls).
   - Steps: Schedule CA columns D and E, Part IV proration, Form 540NR lines 13-19, tax (Tax Table via range midpoint at or below $100,000, Rate Schedule above), lines 31-40 with AGI limitation worksheet, line 72, lines 63-74, payments, refund or balance due, scenario dollar effects.
   - Tests (`tests/test_ca_540nr.py`): FTB's printed example ($125,000 on Schedule Y = $4,768), Tax Table midpoint rule against printed rows, hand-computed part-year MFJ case, AGI-limitation case, error cases, CLI run.
2. `skills/tax-audit/scripts/ca_cross_check.py`
   - Independent recomputation (separate code path using a closed-form bracket formula and different rounding order checks), comparison with the user's filed form values, tolerance reporting, flags for unverified items.
   - Tests (`tests/test_ca_cross_check.py`).

## Phase 3 — Skill integration
- `/tax-prep`: California CSV rows and residency prompts writing `analysis/ca-residency.json`; template and validator updated.
- `/tax-cheatsheet`: Form 540NR and Schedule CA (540NR) walkthrough.
- `/tax-audit`: California section; new pitfalls in `docs/KNOWN-PITFALLS.md`.
- Every rule cites `reference/curated/ca/`.

## Phase 4 — Maintainer's real return
Not run here (private folders are absent from the cloud clone).

## Phase 5 — Docs and release
- `CLAUDE.md` (after tests pass), `README.md`, `.claude-plugin/plugin.json` (description, version), `docs/ARCHITECTURE.md`, `docs/PRIVATE-DATA.md`.
- Final guard run, push, pull request with unverified items, judgment calls and dollar effects.
