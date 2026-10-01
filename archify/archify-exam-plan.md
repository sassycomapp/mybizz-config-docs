---
title: "archify-exam-plan"
doc-id: "mb-b496f764"
updated: "2026-10-01"
---
# Archify — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager before
each run from: [[[mybizz-config-docs:archify/archify-config|Configuration]]](C:/mybizz/mybizz-config-docs/archify/archify-config.md) (spec), the last [[[mybizz-config-docs:archify/archify-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/archify/archify-exam-report.md),
[[[mybizz-config-docs:archify/archify-log|Log]]](C:/mybizz/mybizz-config-docs/archify/archify-log.md) (events since last run), [[[mybizz-config-docs:archify/archify-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/archify/archify-learnings.md). Consumed by the
skill at run time; rewritten at the start of the following cycle. The file is
live; its contents are transient.

**This first plan is hand-written** (emulation of the established architecture):
it also serves as the format template. The **standing check inventory lives in the
skill** ([[[mybizz-config-docs:archify/archify-skill|Archify Skill]]](C:/mybizz/mybizz-config-docs/archify/archify-skill.md), born-with-inventory); this plan carries run-specifics
and references. Once verified by a run, future plans carry run-specifics +
references only.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap). **EXECUTED 2026-09-16; verdict HEALTHY in [[[mybizz-config-docs:archify/archify-exam-report\|Exam Report]]](C:/mybizz/mybizz-config-docs/archify/archify-exam-report.md). This plan remains as the run record for the cycle; the next cycle rewrites it.** |
| Run date | 2026-09-16 (executed) |
| Prior report | none — placeholder present; missing prior report = expected, not silence |
| Step-0 result | PASS — 12/12 hash pairs, suite 8/8 + scope-skill, spec-doc paths 19/19, bootstrap disposition clear |
| Tier 3 unlock state | **Unlocked at gate 2026-09-16 (developer-approved)** — AR3-1, AR3-2, AR3-5 executed agent-side with evidence; AR3-3/AR3-4 dispositions recorded |
| Developer-run requests this run (bundled into ONE request) | (a) any check whose command text the guards deny (expected classes: reads of `~/.config/opencode/skills/archify` — cross-project; token-literal command text naming sibling skills); denied anyway → bundled, honored absolutely; (b) Tier 3 items if unlocked — AR3-2 functional-ability acceptance (live bounded render proof) and AR3-3 open-item dispositions are developer-run by nature |
| Expected-value source of truth | [[[mybizz-config-docs:archify/archify-config\|Configuration]]](C:/mybizz/mybizz-config-docs/archify/archify-config.md) — read fresh at run start; never rely on remembered values |
| Developer instructions this run | (2026-09-16) Full config-management rerun for Archify, Tiers 0–3; the scoping skill (`mb-archify-scope` / [[[mybizz-config-docs:archify/archify-scope-skill\|Scoping Skill Specification]]](C:/mybizz/mybizz-config-docs/archify/archify-scope-skill.md)) is retained and **built into the configuration documentation** (config, explainer, reference) — it is a permanent component of this suite, not transient; prior memory-ecosystem run is **not** used as exam evidence (the pipeline was proven there, but this run verifies the installation independently); Archify-canonical facts recorded in the memory-ecosystem run-learnings are graduated into the explainer/reference permanent homes |
| Scope boundary | This module exams **the Archify tool installation + lifecycle + its documented front-of-pipe scoping discipline**: the discovery symlink, the clone/package, the schemas/references/renderers inventory, the update-notice contract, the scoping skill (`mb-archify-scope`) as an integrated suite component, and the runtime output structure. What it does **not** probe: the upstream repository's content beyond the recorded version identity; `gbrain sync` state (gbrain module); the memory ecosystem diagram's authoring quality (a prior subject, not this module's scope — this run's Tier 3 performs its own bounded functional proof); Graphify / GStack design-HTML domains (related, different-domain, no dependency) |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). Recorded spec open items kept under
watch (observations, not findings):

| # | Watch item (config §Open items) | This run's action | Disposition (run #1, 2026-09-16) |
|---|---|---|---|
| W-1 | Symlink creation method for this specific link (WSL-side vs Windows-side `mklink /D`) — unverified | Confirm the link resolves (AR1-2); Windows-side readability is unprovable from WSL — recorded as an open item with disposition, candidate Tier 3 (AR3-3) | **Retained** (AR3-3) — WSL-visible symlink resolves, doctor passes, OpenCode resolves it; Windows-side readability unprovable from WSL; spec unchanged, watch row continues |
| W-2 | Windows Explorer visibility of the skill through the symlink — unverified | Same as W-1; doctor passes so OpenCode resolves it; recorded, candidate Tier 3 (AR3-3) | **Retained** (AR3-3) — same evidence as W-1; watch row continues |
| W-3 | Update-check manifest URL — claimed by README as one fixed trusted URL; not fetched/verified | Out of scope for local documentation; update-notice contract (notification-only + disable flag) is what this module verifies (AR1-5); manifest URL fetch recorded as deliberately out of scope | **Deliberately out of scope** (AR3-3) — recorded; no fetch performed, by design |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-08-31/09-01 Archify tool discovered and symlinked into OpenCode discovery (`~/.config/opencode/skills/archify` → `/mnt/c/mybizz/archify/archify`) | AR0-1 / AR1-2 topology still holds |
| LG-2 | 2026-09-06 config/explainer/reference suite created; doctor verified 15/15 "Archify is ready" | AR1-1/AR1-3 identity + package structure; AR2-1 doctor re-probe |
| LG-3 | 2026-09-15 scoping skill `mb-archify-scope` built (front-of-pipe) + integrated into suite | AR1-5 suite completeness incl. scope-skill; scope skill installed copy present |
| LG-4 | 2026-09-15 memory-ecosystem run completed (scope → header → probe → render → visual-check) | NOT exam evidence this run (developer instruction); its canonical learnings graduate into explainer/reference |
| LG-5 | 2026-09-16 suite build-out (this run) + output reorganized by project slug under `output/` | AR1-5; verification record for the slug-folder convention |

## 5. Learnings-driven items

| # | Learning | Check |
|---|---|---|
| — | none (learnings file empty at bootstrap) | — |

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in [[[mybizz-config-docs:archify/archify-skill|Archify Skill]]](C:/mybizz/mybizz-config-docs/archify/archify-skill.md) (Tiers 0–3). Summary:

- **Tier 0 (A) — invocability:** AR0-1 discovery symlink resolves (`archify` → `/mnt/c/mybizz/archify/archify`) · AR0-2 CLI entry executable (`node bin/archify.mjs --help`). Failure = DOWN, stop.
- **Tier 1 (A) — state conformance:** AR1-1 version identity (package.json 2.16.0 · SKILL.md frontmatter "2.16") · AR1-2 install architecture (symlink topology, discovery path) · AR1-3 package structure (schemas/ 6 + README · references/ 4 · renderers per type + shared · `bin/archify.mjs`) · AR1-4 suite completeness (8 files + scope-skill) · AR1-5 update-notice contract (notification-only; `ARCHIFY_UPDATE_CHECK_DISABLED=1`) · AR1-6 integration facts (OpenCode /archify · GBrain no page · not a memory writer · Cupcake no rule — provisional per [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md))
- **Tier 2 (A) — functional, present ≠ working:** AR2-1 doctor 15/15 PASS ("Archify is ready") · AR2-2 skill frontmatter resolves through the discovery path (invocable as `/archify`) · AR2-3 scoping skill installed copy present + in sync with [[[mybizz-config-docs:archify/archify-scope-skill|Scoping Skill Specification]]](C:/mybizz/mybizz-config-docs/archify/archify-scope-skill.md) (byte-identity) · a live bounded non-content-changing render proof scheduled for Tier 3 (developer-unlocked)
- **Tier 3 (D, locked):** AR3-1 full mechanical integrity audit (key files byte-count + sha256; clone trees clean) · AR3-2 functional-ability acceptance — live bounded proof the tool renders (doctor + a `validate` of a representative example at showcase), recorded as demonstrated ability · AR3-3 open-item dispositions (symlink method / Windows visibility / update URL) · AR3-4 supply-chain/adoption review performed + recorded · AR3-5 update-notice + integration discipline re-confirmed

## 7. Report requirements

The run writes [[[mybizz-config-docs:archify/archify-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/archify/archify-exam-report.md): verdict line; per-tier tables (check ID,
expected, actual, result); findings with class + evidence + recommended repair +
risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace; failed runs never
touch the prior report; written before any pruning). Then: one run row appended to
[[[mybizz-config-docs:archify/archify-log|Log]]](C:/mybizz/mybizz-config-docs/archify/archify-log.md) (run-row format per [[[mybizz-config-docs:mb-config-manager/config-manager-reference|Reference: Commands, Procedures]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-reference.md)); new learnings
filed.

## 8. Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items expected** — the tool install is developer-owned; every
  repair/decision is developer-run or proposed (update discipline, open-item
  dispositions, spec corrections)
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the Archify source clone/package
  (`/mnt/c/mybizz/archify/`) — never fetched/pulled/reset by an agent · the
  discovery symlink `~/.config/opencode/skills/archify` (never a second path) ·
  the installed scope-skill copy (never modified without resyncing the spec) ·
  any Memory-Governor submission of skill content (permanent ordinary-`gbrain`
  bypass) · `output/` artifacts of prior runs (never deleted by this exam)
- Credentials: variable names only, never printed
