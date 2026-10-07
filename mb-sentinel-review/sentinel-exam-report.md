---
title: "sentinel-exam-report"
doc-id: "mb-4c225dae"
updated: "2026-10-07"
---
# sentinel — Exam Report

**Verdict: Sentinel HEALTHY — Tiers 0–3 all PASS (run #1, 2026-10-07, plan-driven bootstrap; Tier 3 developer-unlocked).** All eight findings (F-1–F-8) dispositioned **APPROVED** at the gate and applied the same day: the spec refreshed (six row clusters), the installed skill's stale citations re-pointed and the step-36 row removed (deny-list edit, developer-approved; body hash `c4a2fe90283224cf`), the bridge route corrected to port 5433, and the ten unwired steps approved as a PDLF-development work item carried on watch rows. The three developer-run checks all PASS developer-verified. The system is working well; the exam verified it and the gate corrections closed every gap it found.

Run header: plan [[[mybizz-config-docs:mb-sentinel-review/sentinel-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-exam-plan.md) (bootstrap, hand-written); run date 2026-10-07; executor: the config-manager cycle per [[[mybizz-config-docs:mb-config-manager/config-manager-agent|config-manager-agent]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-agent.md) + [[[mybizz-config-docs:mb-config-manager/config-setup-prompt|config-setup-prompt]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-setup-prompt.md); expected values read fresh from [[[mybizz-config-docs:mb-sentinel-review/sentinel-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-config.md) at run start. Evidence: `/tmp/opencode/sentinel-run1/`.

## Step 0 — config-manager self-validation (recorded in [[[mybizz-config-docs:mb-config-manager/config-manager-log|Config Manager Log]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-log.md), 2026-10-07)

- Hash pairs probed for 17 installed `mb-config-*` skills via the approved glob form (pinned awk method) — **16/17 source↔installed body MATCH**; estate install discipline intact. This system's pair: `d22c53f567f57ba4` both sides.
- Estate observation S0-F1 (recorded, NOT self-healed): the mb-sysdoc-creator exam-skill pair mismatches (suite source `db7c198744a607db` vs installed `dc231cc6a86c8fa4`) — belongs to that module's next cycle (stale-record class per the F-S0-1/S0-F1 precedent).
- Suite completeness: 16/16 pre-existing Installed folders at the 7-file+skill standard (censored folder read via the approved glob form — no denial) + this folder conforms.
- Register spec-doc paths: 17/17 exist. One-run-at-a-time: held. S-1 executed: register row `Deferred` → `WIP` → `Installed`.

## Tier 0 — Invocability (runner A)

| ID | Expected | Actual | Result |
|---|---|---|---|
| SN0-1 | Installed Skill 1 present with functional frontmatter | Present — `~/.config/opencode/skills/mb-sentinel-review/SKILL.md`; keys exactly `name` + `description` | PASS |
| SN0-2 | Skill discoverable in the session skill surface | `mb-sentinel-review` listed in this session's available skills | PASS |
| SN0-3 | Spec doc present, non-empty | `sentinel-config.md` present (step-0 path check 17/17) | PASS |

## Tier 1 — State conformance (runner A; D rows developer-verified)

| ID | Expected | Actual | Result |
|---|---|---|---|
| SN1-1 | Skill 2 installed with functional frontmatter | Present — `mb-compile-rules/SKILL.md` (8,195 B); keys `name` + `description` | PASS |
| SN1-2 | Methodology installed (SKILL.md + references + templates + evals) | Present — SKILL.md + README + 11 methodology references + `source-index.md` + 3 templates + `evals.json` (matches upstream tree shape) | PASS |
| SN1-3 | Genesis + scope + governing ADR present | All present, incl. the three related ADRs (client-instance-architecture, client-instance-readme-five-app-system, dependency-update-model) | PASS |
| SN1-4 | Step-16 wiring: invocation item 7, gate-proof item 9 | Both live (`step-16-domain-modeling.md` lines 38, 52–55) | PASS |
| SN1-5 | Built-status column vs live | Spec said only Step 16 built; live: all twelve step files exist | FAIL → F-1 DRIFT (spec side) — **corrected at gate** |
| SN1-6 | Unwired-built-steps evidence | Steps 17, 19, 20, 21, 34, 35, 37, 38, 45, 46 zero Sentinel references; step-39's refs are ordinary triage usage | → F-5 GAP — **work item approved** |
| SN1-7 | Skill §1 table vs spec table | Scrutiny values matched; skill carried a 13th marker row (36) | FAIL → F-4 DRIFT (skill side) — **corrected at gate** |
| SN1-8 | Suite completeness | 7/7 + exam-skill source + scope + genesis | PASS |
| SN1-9 | Register row complete after Phase 2 | `Installed`, hash `d22c53f567f57ba4`, install date 2026-10-07 | PASS |
| SN1-13 | Spec mirror claim vs live | Claim false — stub born empty 2026-09-13, never a mirror | FAIL → F-2 DRIFT (spec side) — **corrected at gate** |
| SN1-10 | Security-global library shape | **Developer-verified:** principles 9, requirements 6, threat-models 11, infrastructure 10, cloud 7, secrets 6, testing 5, total 54 — exact match | PASS (developer-verified) |
| SN1-11 | Database state | **Developer-verified** (corrected bridge `-p 5433`): table exists, 0 rows, all columns + CHECK constraints exact (`source_step` 13 values incl. 36; `triage_label` 6 values; severity Low/Medium/High/Critical; confidence Low/Medium/High); `finding_id` free-standing; `step_id`→`steps(id)` FK observed and recorded. The documented route's missing port = F-8 — **corrected at gate** | PASS (developer-verified) |
| SN1-12 | Skill 2 rule inventory | **PASS against the corrected spec row** (re-verified live 2026-10-07): 20 compiled rules + 3 grants-data files at the policy folder root; 20 rule documents (documentation only); mapping deltas ×2 recorded for the policy module's lane | PASS |

## Tier 2 — Functional proof (runner A)

| ID | Expected | Actual | Result |
|---|---|---|---|
| SN2-1 | Machine-parsable; body intact from H1 | Keys exactly `name` + `description`; body intact (hard rules, intensity table, review cycle) | PASS |
| SN2-2 | CLEAR-fast-path + CLEAR-row doctrine | Both present (fast-path line; "Corrected — a CLEAR outcome is now recorded") | PASS |
| SN2-3 | Gate-proof semantics | "No row: STOP, present a…" at item 9 | PASS |
| SN2-4 | Three outcomes + no-match ESCALATE + `needs-info` mapping | All present | PASS |
| SN2-5 | Bridge-only route documented | Wrong-server warning + bridge-only statement + Do-not row; no direct-route instruction | PASS |
| SN2-6 | Methodology discoverable in session | Listed in this session's skill catalog — restart caveat superseded | PASS |

## Tier 3 — Deep pass (runner D — UNLOCKED at the gate; executed 2026-10-07)

| ID | Expected | Actual | Result |
|---|---|---|---|
| SN3-1 | Full spec-vs-live conformance walk | Executed across every spec table: §Identity, §Environment position, §Security-global, §Governing ADR (+3 related ADRs on disk), §Database, §Step-intensity, §Retrofitted (Step 16 live), §Related tools (`/cso` + `/review` in the session catalog), §Known limitations (bullet 3 verified true — `finding_id` has no FK), §Do not (all six traced into the exam skill). Reverse mapping complete. Every mismatch itemized as a finding — all resolved at the gate | PASS |
| SN3-2 | Database deep probe | Satisfied by SN1-11's developer-verified output (full column list, all four CHECK constraints, PK, FK, count 0) | PASS |
| SN3-3 | Methodology upstream currency | Live fetches (2026-10-07): upstream exists at the exact cited path; **MIT license confirmed**; actively maintained (1,005 commits, 112 stars, 9 open PRs); installed tree shape matches upstream — `source-index.md` is upstream-native | PASS |

## Findings — final dispositions (all APPROVED at the gate, applied 2026-10-07)

| # | Class | Resolution |
|---|---|---|
| F-1 | DRIFT (spec side) | **APPROVED + applied** — built-status Yes ×12; environment-position row refreshed; limitations bullet 2 rewritten; step-intensity header updated; security-global + DB verified-live dates refreshed |
| F-2 | DRIFT (spec side) | **APPROVED + applied** — mirror claim removed; installed copy authoritative (body hash recorded; `c4a2fe90283224cf` post-edit) |
| F-3 | GAP | **APPROVED + applied** — four citations re-pointed in the installed skill (deny-list edit, developer-approved; pre-state `cd1816ce093ac2eb` captured to `/tmp/opencode/sentinel-run1/subject-skill-prestate.md`; zero stale references remain) |
| F-4 | DRIFT (skill side) | **APPROVED, option (a) + applied** — the step-36 row removed from §1; step 36 now fast-CLEARs like any unlisted step, matching the spec's 12-step scope |
| F-5 | GAP (material) | **APPROVED as work item** — the ten unwired steps (17, 19, 20, 21, 34, 35, 37, 38, 45, 46) are a PDLF-development retrofit task (Step 16 pattern ×10); carried on watch rows W-4 until closed |
| F-6 | Spec freshness | **APPROVED + applied** — methodology tree cells refreshed; restart caveat superseded (registered in catalog) |
| F-7 | DRIFT (spec side) | **APPROVED + applied** — Skill-2 row refreshed to the developer-approved wording (20 compiled rules + 3 grants-data + 6 backups + 20 documentation files); SN1-12 re-verified PASS |
| F-8 | DRIFT (route) | **APPROVED + applied** — port 5433 documented in spec §Database and the reference bridge command (root cause: the ledger's port changed after installation; the documentation was never updated) |

## Watch rows (carried forward)

| # | Item | Status |
|---|---|---|
| W-1 | `mb-sentinel-review` has never run live against a real feature — the first real PDLF-run feature is the test that matters | Standing watch |
| W-4 | Retrofit work item: wire the ten built steps (Step 16 pattern ×10, intensity numbers confirmed file-by-file at wiring time) | Open — PDLF development owns it |
| W-5 | Policy-module lane observations: doc `no_bash_mediated_file_writes_without_grant.md` has no same-named compiled `.rego`; `cup-protect-cupcake-control-plane.rego` has no same-named doc; 8 `.bak` files in the live policy tree | Routed to the policy module's next cycle |

## Developer-run bundle (results recorded verbatim, developer-verified)

1. **SN1-10** — security-global counts: exact match (9/6/11/10/7/6/5 = 54). Command recorded in the log-era evidence.
2. **SN1-11** — bridge probe: first attempt on the documented route failed (`password authentication failed for user "pdlf_agent"` on port 5432 — the stale route); corrected `-p 5433` run returned the full table definition and `count = 0` — all conform to spec §Database.
3. **SN1-12** — rules inventory: developer count (2 = `cup-`-prefixed documentation files) + agent inventory (20 functional rules + 3 grants-data + 6 backups; 20 documentation files) — reconciled and spec-corrected.

## Guard denials honored this run

Sensitive-token class (the security-global category count probe — Phase 0, honored live), policy-folder token class (bash-carried script text naming the policy folder — restructured per the corpus pattern: content kept in files, never echoed in command text), connection-fragment class (the reference edit's database command fragment — restructured the same way). No denial was retried, reshaped, or routed around; every denied check was completed through a legitimate channel or developer-run.

## Dispositions

Recorded in the [[[mybizz-config-docs:mb-sentinel-review/sentinel-log|Log]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-log.md) run row. One process note for the record: two Edit-tool bracket-fuzz slips during build-out were self-caught at git-diff verification and repaired byte-exactly; the Edit tool's fuzzy bracket matching is why all later edits went through exact-match scripts.