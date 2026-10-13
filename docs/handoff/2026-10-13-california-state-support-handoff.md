# Handoff: California State Tax Support (cloud session)

Date: 2026-10-13
Audience: a Claude Code cloud session that will finish the plan and implement
the work without supervision.
Read order: this file, then `CLAUDE.md`, then
`docs/superpowers/specs/2026-10-13-california-state-support-design.md`.

## 0. The vital rule: never leak private tax data

The maintainer's source documents and generated analysis are secret. They are
never committed, pushed, quoted, summarized or reproduced anywhere in the repo.

Protected folders (all gitignored, all absent from a cloud clone):

- `my-tax-docs/`
- `my tax files/`
- `analysis/`

Hard requirements:

1. **Never edit `.gitignore` in a way that removes or weakens** the entries
   `my-tax-docs/`, `my tax files/` and `analysis/`. Adding entries is fine.
2. **Never use `git add -f`, `git add -A` from a directory that could hold
   private files, or any option that overrides ignore rules.** Stage files by
   explicit path.
3. **Run `python -I scripts/check_private_data.py` before every commit and
   before every push.** It must print "Private data check passed." If it fails,
   stop and fix the cause. Do not commit or push until it passes.
4. **No personal data in any tracked file**, including docs, tests, skill files,
   examples, commit messages and PR text: no names, SSNs, addresses, employer
   names, real dollar amounts from a real return, account numbers or dates of
   residency changes. All test inputs and examples must be synthetic. Use
   obviously fake values (for example a made-up filer with round-number wages).
5. If you ever find private data already in a tracked file or in git history,
   stop immediately, do not push, and record the finding in the PR description
   or final report without repeating the data.

The cloud clone will not contain the private folders. That is expected and
correct. Do not recreate them, fabricate files in them, or try to obtain their
contents.

## 1. What this project is

A Claude Code plugin (a fork of an upstream open-source plugin) that helps a
filer prepare a U.S. federal tax return for tax year 2025 from their own
documents. Pipeline: `/tax-prep` (extract document values to a CSV) →
`/tax-cheatsheet` (line-by-line form help) → `/tax-audit` (pre-filing
cross-check) → `/tax-advisor` (next-year planning). The upstream version
shipped a state-tax module (Maryland) that was removed in this fork; state
support is now being added back, starting with California.

Repo rules from `CLAUDE.md` (read the file itself; these are the essentials):

1. Every tax rule must cite a file in `reference/curated/`.
2. If a rule cannot be verified: say "I cannot verify this — check IRS.gov"
   (for California: check ftb.ca.gov).
3. All math runs in Python scripts using `Decimal`. No arithmetic in model text.
4. No personal information in skill files.
5. Saved forms leave SSN, bank and signature fields blank.

Script pattern (from `docs/ARCHITECTURE.md`): a script takes one JSON string as
its CLI argument and prints one JSON object to stdout; arithmetic uses
`Decimal`; errors are returned as `{"error": ...}`.

## 2. What has been decided

The design is approved by the maintainer. The spec is the source of truth; this
section records why.

| Decision | Choice | Rejected |
|----------|--------|----------|
| Structure | A `state: CA` layer inside the four existing skills; CA references under `reference/curated/ca/` | Separate `/ca-*` skills; one `/tax-state-ca` skill |
| Residency | Part-year support from the start (Form 540NR with Schedule CA (540NR)); full-year Form 540 is the simpler subset | Full-year only |
| Test case | A married-filing-jointly return where one spouse was a full-year California resident and the other became a resident partway through 2025 | |
| Build order | References, then scripts with tests, then skill integration, then verification | Scripts first |
| Unverifiable rules | Flag them; never assume California conforms to federal | Assume conformity |
| Judgment calls | Conservative default (report more tax) and show the dollar effect of the alternative | Aggressive default |

Maintainer preferences to carry forward:

- On unsettled judgment calls, take the conservative position: overpaying and
  amending later is preferred to underpaying.
- In accuracy-first documents (references, fact sheets), record only the
  corrected fact, not the history of the correction. Decision records such as
  specs, handoffs and change logs do keep history.
- Keep communication short and direct.

Already written:

- `docs/superpowers/specs/2026-10-13-california-state-support-design.md`
  (approved design; contains three open questions to resolve in phase 1).
- `scripts/check_private_data.py` (the privacy guard from section 0).

## 3. Your task

Finish the plan and implement the spec. Work on a branch named
`ca-state-support`, commit after each phase, and open a pull request against
the fork's `main` at the end. Do not push to `main` directly.

### Step 1 — Prepare

1. Read the three documents listed at the top.
2. Run `python -I scripts/check_private_data.py` and confirm it passes.
3. Add a stdlib `unittest` test for `scripts/check_private_data.py` (temporary
   git repo in a temp directory; cases: passes on a clean repo, fails when an
   ignore entry is missing, fails when a private path is force-added). Use no
   new dependencies. Put tests in a top-level `tests/` folder.

### Step 2 — Curate California references (phase 1)

Fetch the 2025 FTB sources and write `reference/curated/ca/*.md` in the same
format as the existing curated files (Source, Applicable To, Rules, citations).
Suggested sources (verify each URL; I could not):

- 2025 Form 540NR booklet (California Nonresident or Part-Year Resident Income
  Tax Return) and Schedule CA (540NR) instructions
- FTB Publication 1031, Guidelines for Determining Resident Status
- 2025 California tax rate schedules, standard deduction and exemption credit
  amounts
- FTB guidance on federal conformity (depreciation, state refund, rollovers)

For each source add a `<name>.source.txt` stub: title on the first line, URL on
the second, then `Local copy: <name>.pdf (gitignored)`. Download PDFs only to
gitignored paths; extend `.gitignore` with `reference/curated/ca/*.pdf` (adding
is allowed; see section 0).

Resolve the spec's three open questions from these sources and edit the spec's
"Open questions" section into a "Resolved questions" section stating the
answer and citing the reference file.

If a source cannot be fetched, do not guess. Write the affected rule as
"I cannot verify this from provided FTB materials — check ftb.ca.gov", list it
in the PR description under "Unverified items", and continue.

### Step 3 — Write the implementation plan

Use the `superpowers:writing-plans` skill. Save the plan as
`docs/superpowers/plans/2026-10-13-california-state-support-plan.md` and commit
it. The spec is already approved, so do not wait for further approval; proceed
to execution.

### Step 4 — Implement (phases 2 and 3)

1. `skills/tax-cheatsheet/scripts/ca_540nr.py` — Form 540NR calculation, with
   tests in `tests/`. Use hand-checkable synthetic inputs; verify the tax
   against the FTB rate schedule in the curated reference.
2. `skills/tax-audit/scripts/ca_cross_check.py` — independent recomputation and
   comparison, with tests.
3. Skill integration:
   - `/tax-prep`: California CSV rows (W-2 state wages, state tax withheld,
     SDI, 1099-G state refund) and residency date prompts that write to
     `analysis/ca-residency.json` (gitignored).
   - `/tax-cheatsheet`: Form 540NR and Schedule CA (540NR) walkthroughs.
   - `/tax-audit`: California section and new pitfalls in
     `docs/KNOWN-PITFALLS.md`.
4. Follow the way the existing `SKILL.md` files reference their scripts. Keep
   scripts and docs free of machine-specific absolute paths and OS-specific
   code (the maintainer develops on Windows; you run on Linux).
5. Every rule in a skill or script comment cites a file in
   `reference/curated/ca/`.

### Step 5 — Test

1. Run the full test suite (`python -m unittest discover -s tests`). All tests
   must pass.
2. Run each new script from the command line with a synthetic JSON input and
   confirm the output is valid JSON and matches hand calculations.
3. Verify every California number in the examples against the FTB rate
   schedule. Use the `adversarial-verification` skill on the calculation
   outputs if it is available.
4. Run `python -I scripts/check_private_data.py`.

The maintainer will run the real return through the finished flow locally
(spec phase 4). You cannot do this because the private folders are not in the
clone. Do not attempt it.

### Step 6 — Update `CLAUDE.md` (after testing)

After the tests pass, update the repo's `CLAUDE.md` to capture everything
added or changed in this work. At minimum:

- the project now covers federal and California (state support, Form 540NR
  and Schedule CA (540NR)), not federal only
- the new folder `reference/curated/ca/` in the file-locations table
- the new scripts and tests (`ca_540nr.py`, `ca_cross_check.py`, `tests/`,
  `scripts/check_private_data.py`)
- the new residency input (`analysis/ca-residency.json`) in setup steps
- the privacy rule from section 0, stated as a numbered rule: the three
  protected folders, never weaken their gitignore entries, run the guard
  before every commit and push
- the rule that California rules cite `reference/curated/ca/` and unverified
  items say "check ftb.ca.gov"

Write `CLAUDE.md` as a current-state document: describe how things are now,
not the history of the change.

### Step 7 — Finish

1. Update `README.md`, `.claude-plugin/plugin.json` (description and version
   bump), `docs/ARCHITECTURE.md` (new scripts, references, data flow) and
   `docs/PRIVATE-DATA.md` (mention `analysis/ca-residency.json`).
2. Run `python -I scripts/check_private_data.py` one last time.
3. Push the branch and open a pull request. The PR description must include:
   what was built, test results, the list of "Unverified items", every
   judgment call with its conservative default and the dollar effect of the
   alternative, and the statement that the real-return verification (spec
   phase 4) remains for the maintainer to run locally.

## 4. Stop conditions

Stop and report instead of continuing if:

- the privacy check fails and you cannot fix the cause
- you find private data in a tracked file or in history
- an FTB source contradicts the spec's design (for example a different
  part-year method); record the contradiction in the PR description and the
  spec rather than silently diverging
- the tests cannot be made to pass

## 5. Done means

- All tests pass and the privacy check passes.
- Every California rule in references, skills and scripts cites a curated file.
- Unverifiable rules are flagged, not assumed.
- `CLAUDE.md` is updated as described in step 6.
- A pull request is open with the description required in step 7.
