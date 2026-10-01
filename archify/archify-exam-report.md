---
title: "archify-exam-report"
doc-id: "mb-3f68fb7d"
updated: "2026-10-01"
---
# Archify — Exam Report

**Verdict (run #1, Tiers 0–3): HEALTHY — ** all tiers executed, zero DOWN, zero
UNHEALTHY, zero open findings at close. Two findings raised and closed during the
run (F-1 re-sync applied, F-2 config governance refresh applied with gate
approval).

Run date: 2026-09-16 · run #1 — first formal plan-driven run (bootstrap). Plan:
[[[mybizz-config-docs:archify/archify-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/archify/archify-exam-plan.md). Executed by `mb-config-archify` with the plan in hand.
Tier 3 **unlocked at the gate** (developer-approved 2026-09-16).

## Tier 0 — Invocability (A)

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| AR0-1 | Discovery symlink resolves | `archify` → `/mnt/c/mybizz/archify/archify` | readlink → `/mnt/c/mybizz/archify/archify` | PASS |
| AR0-2 | CLI entry executable | `bin/archify.mjs` returns usage | `--help` prints full usage (render/compare/deliver/preview/validate/migrate/inspect) | PASS |

## Tier 1 — State conformance (A)

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| AR1-1 | Version identity | package.json `2.16.0`; SKILL.md `version: "2.16"` | `2.16.0`; frontmatter contains `version: "2.16"` | PASS |
| AR1-2 | Install architecture — single discovery path | exactly one `archify` entry resolving to the clone | one symlink entry; no duplicate path elsewhere | PASS |
| AR1-3 | Package structure | schemas/ 6 `.schema.json` + README; references/ 4; renderers per-type + shared; `bin/archify.mjs` | schemas 6 + README (1); references 4 (authoring-contract, brand-marks, delivery-contract, viewer-runtime); renderers architecture/dataflow/lifecycle/sequence/shared/workflow; bin present | PASS |
| AR1-4 | Suite completeness | 8 regular files + scope-skill spec | 8/8 present + [[[mybizz-config-docs:archify/archify-scope-skill\|Scoping Skill Specification]]](C:/mybizz/mybizz-config-docs/archify/archify-scope-skill.md) | PASS |
| AR1-5 | Update-notice contract | notification-only; `ARCHIFY_UPDATE_CHECK_DISABLED=1` documented | contract text present in SKILL.md; env unset live (disable is optional); manifest URL not fetched (deliberately out of scope) | PASS |
| AR1-6 | Integration facts | OpenCode `/archify`; GBrain no page; not a memory writer; Cupcake provisional | OpenCode recorded; GBrain no-page recorded; no Memory-Governor treatment recorded; **Cupcake re-verified live: no archify-specific rule (only the mg-grant access entry exists); Cupcake status ACTIVE (verified 2026-09-12)** | PASS w/ F-2 sub-note |

## Tier 2 — Functional proof (A; read-only)

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| AR2-1 | Doctor probe | 15/15 checks, "Archify is ready" | 15/15 `[ok]`, final line "Archify is ready", exit 0 | PASS |
| AR2-2 | Skill invocability via discovery | real `name: archify` frontmatter resolves | `name: archify` + description resolve through the symlink | PASS |
| AR2-3 | Scoping-skill component integrity | installed copy byte-identical to [[[mybizz-config-docs:archify/archify-scope-skill\|Scoping Skill Specification]]](C:/mybizz/mybizz-config-docs/archify/archify-scope-skill.md) | **FOUND DRIFT** (installed 278 l vs spec 292 l, missing Phase 9). **Closed this run** — re-copy applied (gate F-1 approved), hash pair now identical `0e40e984ba82a5f6`, "nine phases" present | PASS (after repair) |

## Tier 3 — Deep pass (unlocked; safe rows agent-run with evidence below)

| ID | Runner | Check | Actual | Result |
|---|---|---|---|---|
| AR3-1 | A | Full mechanical integrity audit: `sha256sum` of package.json, `bin/archify.mjs`, SKILL.md, all 6 schemas + schemas README, all 4 references | 15 files hashed stable (e.g. package.json `9be6428b…`, bin `a9e02fa9…`, SKILL.md `5bf0cac8…`, schemas `2630c958…`/`8c96140b…`/…, references `8f2b583d…`/`8010869d…`/`c0af94e2…`/`dc0d9ffe…`). Working tree: only known untracked visual-check sidecars in `examples/` (the reference-calibration PNGs documented in the run-learnings) | PASS |
| AR3-2 | A (read-only render probe) | Functional-ability acceptance: `validate architecture examples/web-app.architecture.json --quality showcase --json` | `ok: true`; all 9 artifact checks pass; `errors: 0`, `warnings: 0`; receipt `schemaVersion 1`; satisfies the showcase gate (9/9, 0 errors, 0 warnings). Completed with the previously-run `doctor` 15/15 — the tool demonstrably renders | PASS |
| AR3-3 | D | Open-item dispositions | W-1 symlink creation method / W-2 Windows Explorer visibility — **disposition: deliberately retained as open items**. Evidence: the link is a WSL-visible symlink `archify → /mnt/c/mybizz/archify/archify`; doctor passes so OpenCode resolves it; Windows-side readability is not provable from WSL. W-3 update-check manifest URL — **disposition: deliberately out of scope** (documented). Spec unchanged — these remain watch items, not commitments | Recorded |
| AR3-4 | D | Supply-chain / adoption review | **Performed + recorded.** Publisher: individual (`tt-a1i`) · License: MIT (package.json confirms) · Based on: Cocoon-AI/architecture-diagram-generator (MIT v1.0) · Maintenance: active (2.16.0; project docs confirmed live) · Spawn-capability: benign in-environment — Archify is a CLI authoring tool; it cannot create an isolated agent session; its only network surface is the optional notification-only update check (disableable). Verdict per [[[default:security-global/principles/sec-review-before-trust\|Review Before Trust]]](C:/dev/project-library-global/security-global/principles/sec-review-before-trust.md)/[[[default:security-global/infrastructure/sec-dependency-skill-supply-chain\|Dependency and Skill Supply Chain]]](C:/dev/project-library-global/security-global/infrastructure/sec-dependency-skill-supply-chain.md): benign on all four axes | Recorded |
| AR3-5 | D | Update-notice + integration discipline re-confirmation | Restated: only network surface is the notification-only checker (transmits IP + timestamp to one fixed manifest URL, nothing else); update decisions stay developer-owned; scope-skill copy stays in sync (now verified identical); content reaches GBrain by ordinary `gbrain sync` only; `ARCHIFY_UPDATE_CHECK_DISABLED=1` remains the documented disable | Recorded |

## Findings

| ID | Class | Evidence | Disposition |
|---|---|---|---|
| F-1 | DRIFT | Installed `mb-archify-scope/SKILL.md` (278 l) stale vs spec (292 l): missing Phase 9 close-out learnings, "eight phases" vs "nine", missing learnings output row. Source edited after install | **Closed 2026-09-16 (gate-approved F-1)** — re-copy applied, hash pair identical `0e40e984ba82a5f6`, Phase 9 + "nine phases" present |
| F-2 | GAP (spec wording) | [[[mybizz-config-docs:archify/archify-config\|Configuration]]](C:/mybizz/mybizz-config-docs/archify/archify-config.md) §Integration Cupcake row framed enforcement as "disabled environment-wide at research time (2026-09-06)" | **Closed 2026-09-16 (gate-approved F-2)** — row refreshed to current ACTIVE status (per [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) 2026-09-12) + confirmed no archify rule (re-verified this run) |

## Step-0 note (estate, not this module)

Step-0 self-validation (recorded in [[[mybizz-config-docs:mb-config-manager/config-manager-log|Log]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-log.md)): 12/12 hash pairs
MATCH. One estate-wide GAP was logged and **closed this session**: anvil-agent-
references source (`a66e0140a39a37e5`, edited in `4aff290`) had not been
re-installed; re-sync executed by the developer, hash pair verified, register The use of registers has been discontinued. Please review
updated. No open estate items remain from this run.
