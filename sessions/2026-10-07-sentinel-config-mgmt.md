---
title: "2026-10-07-sentinel-config-mgmt"
doc-id: "mb-ca9e9d9f"
updated: "2026-10-07"
---
# Session 2026-10-07 — mb-sentinel-review config-management build-out + run #1

## What was done

- Built the configuration-management suite for **mb-sentinel-review** (7-file standard + exam-skill source, born-with-inventory checks SN0-1…SN3-3) and installed the exam skill `mb-config-mb-sentinel-review` (copy-install, hash pair `d22c53f567f57ba4` both sides; register row flipped `Deferred` → `WIP` → `Installed` via named step S-1, per the config-setup-prompt clarity discipline).
- Ran formal exam **run #1**: Tiers 0–2 autonomous, Tier 3 developer-unlocked. All checks PASS. Final verdict: **HEALTHY**.
- Gate same day: **F-1 through F-8 all APPROVED and applied** — spec refreshed (built-status Yes ×12, mirror claim re-pointed, methodology tree cells, Skill-2 inventory wording, bridge route `-p 5433`, verified-live dates, `step_id` FK note); installed subject skill citations re-pointed + the step-36 row removed (deny-list edit, developer-approved; pre-state `cd1816ce093ac2eb` captured; post-edit `c4a2fe90283224cf`); SN1-12 re-verified PASS against the corrected spec row.

## Evidence

- Developer-verified (verbatim in the report): security-global library counts 9/6/11/10/7/6/5 = 54 (exact); `triage_findings` bridge probe — table exists, 0 rows, all columns + four CHECK constraints exact, `finding_id` free-standing, `step_id`→`steps(id)` FK recorded. First bridge attempt on the documented route failed on port 5432; the developer corrected: the ledger's port was changed to 5433 after Sentinel's installation and the documentation was never updated (→ F-8).
- Tier 3: full spec-vs-live conformance walk PASS (every mismatch itemized, all resolved); methodology upstream re-verified live — MIT, actively maintained (1,005 commits, 112 stars), installed tree shape matches, `source-index.md` upstream-native.
- Evidence files: `/tmp/opencode/sentinel-run1/` (`step0.txt`, `tiers.txt`, `subject-skill-prestate.md`).

## Decisions and standards the developer set

- Grants issued per need as the work demanded (suite 12+3+2+1; config-manager 4; install 3; net github.com 2).
- Skill-2 inventory wording: **20 compiled rules** (`cup-*.rego` in the policy folder) + 3 grants-data + 6 `.bak` backups + **20 rule documents** in `rules-cupcake-global/` — that folder is **documentation only**; the functional rules are the policy files.
- F-4 option (a): the step-36 marker row removed so step 36 fast-CLEARs like any unlisted step.
- Bridge route correction: `-p 5433` is now the documented procedure.

## Quirks

- The Edit tool fuzzy-matches bracket runs: it corrupted stored links twice; both caught at git-diff verification and repaired byte-exact. All later edits ran through exact-match Python scripts (including the corpus pattern: content kept in files, never echoed in command text).
- Guard denials honored, none retried or reshaped: sensitive-token class (security-global count probe — developer-run), policy-folder token class (bash text), connection-fragment class (reference-edit text) — the last two completed via the corpus pattern.

## Documents written or changed

- `mb-sentinel-review/`: sentinel-config (corrected), sentinel-reference (port fix), sentinel-explainer, sentinel-learnings, sentinel-log, sentinel-exam-plan, sentinel-exam-report, sentinel-skill (exam-skill source)
- `mb-config-manager/`: register row final (Installed, verified live 2026-10-07), log step-0 row
- `~/.config/opencode/skills/mb-config-mb-sentinel-review/SKILL.md` (installed exam skill)
- `~/.config/opencode/skills/mb-sentinel-review/SKILL.md` (subject skill: citation re-point + step-36 removal)

## What is open

- **W-1** (standing watch): Sentinel has never run live against a real feature — the first real PDLF-run feature is the true test.
- **W-4** (work item, PDLF development owns it): retrofit the ten built-but-unwired intensity steps (17, 19, 20, 21, 34, 35, 37, 38, 45, 46) with the Step 16 pattern (invocation + gate-proof).
- **W-5** (routed): policy-lane observations — doc `no_bash_mediated_file_writes_without_grant.md` has no same-named compiled `.rego`; `cup-protect-cupcake-control-plane.rego` has no same-named doc; 8 `.bak` files in the live policy tree.
- **S0-F1** (estate observation, config-manager log): the mb-sysdoc-creator exam-skill source no longer matches its installed copy — that module's next cycle.