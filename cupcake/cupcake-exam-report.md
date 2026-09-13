---
document: "Cupcake — Exam Report"
doc-id: cupcake-exam-report
state: Live
date-created: 2026-09-12
---

# Cupcake — Exam Report

First verification run of the `mb-config-cupcake` module (2026-09-12).
Detection only — Tiers 0–2. Tier 3 (developer-run eval + test sheets) not unlocked.
Spec: `cupcake-config.md` (verified live 2026-09-12).

## Verdict: ACTIVE & HEALTHY — enforcement proven live, 0 compile failures

## Tier 0 — Liveness: PASS

| Check | Expected | Actual | Result |
|---|---|---|---|
| Binaries resolve | cupcake real file + symlink; opa 1.19.1 | exact match | PASS |
| Enforcement firing | deny on known-blocked probe | **outbound-network deny received** (curl to non-allowlisted domain) | PASS |
| Enforcement firing (natural) | denies received during exam | exec-protection denied `which cupcake`; batch block ×2 | PASS |

Three independent live enforcement proofs this run — the silent-failure class
(rule present, not firing) is demonstrably absent right now.

## Tier 1 — Health: PASS

| Check | Expected | Actual | Result |
|---|---|---|---|
| `opa check` all deployed + builtins + system | 0 failures | 0 failures | PASS |
| Scaffold files | none (`example.rego` absent) | none | PASS |
| Plugin single copy | one live `cupcake.js` | one live copy | PASS |
| Backups non-loadable | `.bak` suffixes (never `.rego`/`.js`) | all correct | PASS |
| Grants data file | generated-form, present | `GLOBAL-GRANTS-DATA` header | PASS |
| Plugin cwd fix (same-day follow-up) | `cwd: event.cwd` in Bun.spawn | present (1 match) | PASS |
| failMode (same-day follow-up) | configurable; project file exists | `.cupcake/opencode.json` → `"open"` — matches documented fail-open posture | PASS |

## Tier 2 — State conformance: PASS with two minor drift flags

| Check | Expected (spec) | Actual | Result |
|---|---|---|---|
| Custom rules | 19 | 19 live `.rego` (20th glob match = generated grants file) | PASS |
| Builtins | 3 | 3 (system_protection, sensitive_data_protection, cupcake_exec_protection) | PASS |
| Aggregator | `system/evaluate.rego` | present, compiles | PASS |
| Task denial layer 1 | `"task": "deny"` | present (in `opencode.jsonc`) | PASS |
| `spawn-tools-denylist.json` | task, delegate, call_omo_agent, agent_session_create | exact match | PASS |
| Grant tooling | mg-grant, mg-revoke on PATH | present | PASS |
| Source↔deployed sync | 20 sources ↔ 19 deployed | see finding 1 | MATCH-WITH-NOTE |
| Backups documented | `.bak-20260912` (plugin) | 2 plugin backups + 5 rego backups exist | DRIFT (minor) |

## Findings

0. **Guard false-positive class confirmed (exec-protection breadth).** The guard
   denies any command whose argument text contains the token `cupcake` — including
   non-execution operations (`which cupcake`, `mkdir .../mb-config-cupcake`,
   `mv ... cupcake-skill.md`). Proven live twice this run. Consequence: cupcake-named
   path operations (skill install included) are **developer-run**. This is the guard
   being broad, not broken — no repair proposed unless the developer wants the
   matcher narrowed.
1. **Source↔deployed correspondence (match, with note).** 20 rule sources, 19 deployed
   files. `no_bash_mediated_file_writes_without_grant.md` has no standalone deployed
   file — per the spec's 2026-09-12 entry its bash-write-shapes are compiled into
   `cup-no_cross_project_filesystem_access_by_default.rego` (same file/package, own
   rule id). Verified: 4 bash-shape indicator groups found in that rego. Future runs
   must expect this fold-in and not report it as a missing deployment.
2. **DRIFT (minor) — backup inventory vs spec.** Spec documents one plugin backup;
   two exist (`bak-20260912`, `bak-2026-08-31T095850+0200`), plus 5 `.rego.bak-*`
   files in the policy folder. All correctly suffixed (not loaded) — no risk.
   Recommended: spec lists the full backup set on next approved doc pass → docs
   governance.
3. **Config filename drift (minor).** Spec says task-deny verified in
   `opencode.json`; the live file is `opencode.jsonc`. Content confirmed correct.
   → docs governance naming fix.

## Guard layers

Three denials received mid-exam, each clean and correctly attributed — guard layers
armed and firing. All denials honored; nothing retried through alternate paths.

## Not run this cycle

Tier 3: authoritative developer-run eval check, live test sheet, grant lifecycle,
version corroboration. Instance-A-equivalent: none (single-host system).