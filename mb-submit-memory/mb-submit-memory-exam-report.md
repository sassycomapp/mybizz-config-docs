---
title: "mb-submit-memory-exam-report"
doc-id: "mb-aae27791"
updated: "2026-10-01"
---
# mb-submit-memory — Exam Report

**Run #1 formal — 2026-09-15. Verdict: HEALTHY.** Tier 0–2 all PASS, zero live
defects. Three spec/governance flags carried to the gate (F-A, F-B, F-C); one
cross-reference observation (Obs-1). Tier 3 Locked — unlock decision at the
gate. The system is working well; this exam changes nothing.

## Step-0 self-validation (config-manager)

| Check | Result |
|---|---|
| Hash pairs, every Installed skill (approved glob form `mb-config-*/SKILL.md`) | **7/7 MATCH** — postgresql `b41a3e117dee1809` · cupcake `f5e8489cf60a8abc` · gbrain `58dc0b52cbc86d72` · memory-governor `c40df342d523aa59` · gbrain-dream-cycle `a4872e9d61f1c32f` · graphify `1ca73897a2023741` · mb-submit-memory `5306a5e64d43e613` |
| Suite completeness, Installed systems | 7/7 at 8/8 files |
| Register The use of registers has been discontinued. Please review spec-doc paths | 19/19 exist |
| Target's last log run-row disposition | Present (11 rows; last row disposed) |
| Guard denials | 1 — exec-protection on token-literal step-0 command text (documented class). Honored absolutely; the approved glob form used instead. Recorded in [[[mybizz-config-docs:mb-config-manager/config-manager-log\|Log]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-log.md) |

## Tier 0 — Invocability (runner A)

| ID | Expected | Actual | Result |
|---|---|---|---|
| SM0-1 | Installed skill present, frontmatter name `mb-submit-memory` | Present; `name: mb-submit-memory` | **PASS** |
| SM0-2 | 13,502 B (spec §Identity fingerprint) | 13,502 B | **PASS** |

## Tier 1 — State conformance (runner A)

| ID | Expected | Actual | Result |
|---|---|---|---|
| SM1-1 | Suite completeness — 8 files | 8/8 present | **PASS** |
| SM1-2 | `gbrain config get mcp_surface` → `verbs` (spec §Governance chain) | `verbs` (source: db plane) | **PASS** — matches this spec; cross-spec flag F-C (W-6) |
| SM1-3 | Governor API listening on `127.0.0.1:8321` | LISTENING (python, pid 14623) | **PASS** |
| SM1-4 | Run-logs lane present per spec §Logs | 2 run logs + learnings.md (8 entries) | **PASS with flag F-A** — live growth vs spec's "one + 6" = spec progress → governance |
| SM1-5 | Spec §Identity mirror claim vs reality | No repo-side mirror — [[[mybizz-config-docs:mb-submit-memory/submit-memory-skill\|Submit Memory Skill]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/submit-memory-skill.md) is the exam-skill source (developer instruction 2026-09-15) | **PASS with flag F-B** — spec claim superseded → governance; hash anchor = spec fingerprint (SM0-2) |

## Tier 2 — Functional proof (runner A)

| ID | Expected | Actual | Result |
|---|---|---|---|
| SM2-1 | Unauthenticated probe → `422` | `422` | **PASS** — auth posture intact; never probed with a credential |
| SM2-2 | Detect surface: `gbrain call recall '{"grep": "<real phrase>"}'` succeeds | Clean envelope (protocol_version 1, exit 0); `total: 0` on the world-fact phrase | **PASS with note** — surface proven functional; zero consistent with the all-private fact inventory (operational learning #7: project_local facts not recallable in 0.46.1.0). Noted for graduation (L-2) |

## Findings (classified; decisions at the gate)

| # | Class | Finding | Evidence | Recommended repair | Risk |
|---|---|---|---|---|---|
| F-A | DRIFT (spec-progress) | Spec §Logs stale: records one run log + 6 learnings (verified 2026-09-08); live = two run logs (2026-08-27, 2026-09-14) + 8 learnings | SM1-4 output | Flag to docs governance: update the Logs row counts + verified-live date | Low — normal operation recorded late in the spec |
| F-B | GAP (spec claim superseded) | Spec §Identity "byte-identical mirror" claim no longer matches reality: the slot is the exam-skill source (developer instruction 2026-09-15); the subject skill has no repo-side copy | SM1-5 output; 0 B file pre-build; 11,594 B exam skill post-build | Flag to docs governance: correct the Identity row + resolve the "Dual SKILL.md copies" open item (it dissolves — no dual copies exist) | Low-medium — the subject skill's only repo-side anchor is the spec fingerprint until the developer decides otherwise |
| F-C | DRIFT (cross-spec contradiction) | This spec records `mcp_surface` → `verbs` (2026-09-08, live-confirmed today); the dream-cycle spec records "no `mcp_surface` key, verbs in default surface" (reconciled 2026-09-06) — both cannot describe the current config | SM1-2 output | Flag to docs governance: the dream-cycle spec's MEMORY_VERBS row is stale; parent `mb-config-gbrain` re-verifies config state at its next run | Low — expectation values disagree between suites, not between spec and live |
| Obs-1 | Observation (cross-reference) | gbrain upgrade available: 0.46.1.0 → 0.50.0.0 (banner on `config get` and `call recall` stdout) | SM1-2 / SM2-2 output | None here — version policy belongs to `mb-config-gbrain` (DC3-2: never on newness, only on check failure) | None for this module |

## Runner attribution

All Tier 0–2 rows agent-run (A). Tier 3 rows (SM3-1, SM3-2, SM3-3) are
developer-run and Locked — unlock decision requested at the gate. No checks
were guard-denied except the step-0 token-literal form (honored; approved
glob form used).

## Learnings filed this run

- L-1: the gbrain CLI emits an `UPGRADE_AVAILABLE 0.46.1.0 0.50.0.0` banner on
  stdout ahead of real output on several commands — probe consumers must
  expect and skip it. Destination: skill.
- L-2: recall's grep arm returning `total: 0` on a world-fact phrase can
  reflect an all-private fact inventory (learning #7 corollary) — the surface
  is proven by the clean envelope, not by a nonzero count. Destination: skill.
  (Both graduated into the skill at gate close-out; re-installed, re-hash
  `88a71641d03f1997`.)

## Tier 3 — deep pass (unlocked at the gate; developer-executed, 2026-09-15)

| ID | Check | Result |
|---|---|---|
| SM3-1 | Credentialed review-queue check (developer-executed; credential by variable name `MEMORY_GOVERNOR_WRITER_MANUAL_SUBMISSION` — name only, value never exposed) | Credential **accepted**; queue **empty** — zero pending `owning_project` records; the three 2026-09-14 visibility-correction items resolved upstream. Every evidenced `owning_project` (`mybizz-config-docs`, `makepdlf-project-library`) matches a registered gbrain source exactly. Boundary recorded: no documented API endpoint enumerates all project rows — full enumeration would require a new read endpoint (developer feature decision) or a credentialed DB query; stated, not silently dropped |
| SM3-2 | Permanent auto-start (systemd migration) | **EXECUTED + VERIFIED 2026-09-15 (session 005)** — systemd enabled (`systemd=true` under `[boot]`, boot command preserved); both units enabled and active under the user manager (api pid 2607, worker pid 2608, Restart=on-failure); PostgreSQL auto-started (5432); port 8321 held by the service; auth-gate 422. Boot-script idempotency proof lands at the next natural restart (standing check, not an open item) |
| SM3-3 | Stray `0.48.2.0` deletion | **Resolved** — file verified absent 2026-09-15 (`ls: cannot access … No such file or directory`); nothing to delete |

Gate dispositions (2026-09-15): F-A approved → spec §Logs corrected; F-B
approved → spec §Identity corrected and the dual-copies open item dissolved;
F-C resolved by developer directive (correct, do not flag) → dream-cycle spec
MEMORY_VERBS row corrected. All three applied and verified.
[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) updated to current verified state (its own
commit, standing authorization).
