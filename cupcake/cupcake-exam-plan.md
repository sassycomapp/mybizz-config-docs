---
title: "cupcake-exam-plan"
doc-id: "mb-cd94d069"
updated: "2026-10-04"
---
# Cupcake — Exam Plan

Transient job-spec for this run. Synthesized 2026-10-04 by the config-manager from
[[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) (spec — read fresh at run start), the last
[[[mybizz-config-docs:cupcake/cupcake-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-exam-report.md) (run #1, 2026-09-13), the
[[[mybizz-config-docs:cupcake/cupcake-log|Log]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-log.md) (events since last run), and the
[[[mybizz-config-docs:cupcake/cupcake-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-learnings.md). The standing check inventory (Tiers 0–3, C0-1…C3-4)
lives in the skill ([[[mybizz-config-docs:cupcake/cupcake-skill|Cupcake Skill]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-skill.md) / installed copy); this plan
carries run-specifics, deltas, and the developer-requested item only. Consumed by
the skill at run time; rewritten at the start of the following cycle.

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #2 — second formal plan-driven run (run #1: 2026-09-13) |
| Run date | 2026-10-04 |
| Invocation | single-system cycle per developer instruction: step 0 → plan → skill run → aggregate → report → **STOP at the gate; apply no repair** |
| Prior report | [[[mybizz-config-docs:cupcake/cupcake-exam-report\|Exam Report]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-exam-report.md) (run #1, 2026-09-13) |
| Step-0 result | PASS with estate finding F-S0-1 — recorded in the [[[mybizz-config-docs:mb-config-manager/config-manager-log\|Config Manager Log]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-log.md) 2026-10-04 (15/15 source↔installed body MATCH; register body-hash columns stale ×15 → DRIFT, gate item) |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request) | (a) grant-enforcement write-probes (GR-6) — required by the developer-requested item regardless of Tier 3; (b) any check whose command text a guard denies; (c) Tier-3 items (C3-1…C3-4) only if unlocked |
| Read approvals pending | `C:\dev\project-library-global\rules-cupcake-global\` read (C2-4 source leg) — requested; C2-4 executes deployed-side only until approved |
| Expected-value source of truth | [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) — read fresh at run start; never rely on remembered values |
| Structural constraint | per the skill's structural rule: never execute the enforcement binary; read-only inventory only inside `~/.config/cupcake/`; never write to policy or plugin files; never work around a denial |

## 2. Carried-forward items (from run #1 + log)

| # | Item | Status going in | This run's action |
|---|---|---|---|
| CF-1 | Run #1 open question — bash-mediated writes do not decrement grant counts | Resolved 2026-09-13: developer-accepted as intended design; recorded in the spec's grant-mechanics section; skill C3-3 expected cell updated | Verify spec ↔ skill wording agree; no re-test |
| CF-2 | Guard token class — the token `cupcake` denied in non-execution command text | Standing class, honored | Any new denial recorded as liveness evidence, never worked around |
| CF-3 | Version gap — upstream v0.5.1 vs installed 0.3.0 | Recorded 2026-09-13; policy: upgrade only on check failure | No action unless a check fails (then Tier-3 C3-4, developer-run) |
| CF-4 | Run #1 report closing line stale ("Tier 3 partially open") vs log (C3-3 completed) | Doc artifact | Overwritten by this run's report — no separate action |

## 3. Log-driven items (events since run #1: 2026-09-13 → 2026-10-04)

| # | Event | Check |
|---|---|---|
| LG-1 | 2026-09-22 set-and-forget amendment — second total-evaluation crash fixed permanently (`failMode: open` environment default; skeleton-less sessions fall back to `~/.config/cupcake/fallback`; input-gated placeholder guarantees boot safety; live-verified 10 consecutive clean calls) | Verify live: fallback home exists with the expected skeleton (input-gated `cup-noop-fallback.rego`, `system/evaluate.rego`, `helpers/commands.rego`, `rulebook.yml`, `opencode.json`); placeholder opa-checks clean; plugin backup `.bak-20260922-pre-amendment` present; spec §Identity rows (fallback home, plugin amendment, project-init status) match live state |
| LG-2 | 2026-09-22 WP3 commit-allowance channel (decision G1): amended rules committed to source (24985a3), compiled, deployed; plugin prunes and decrements BOTH grants files; `git-grant` placed by developer; live-verified same day (allow with live grant; publish deny; data-mybizz-mgt write deny) | Verify live: `cup-git-grants-data.rego` present, generated-form, opa-checks clean; `git-grant` on PATH; deployed git rule carries the allowance clause and publish/deploy stay absolute-deny; deployed cross-project rule carries no `skills-collective` always-open entry; plugin backup `.bak-20260922-pre-wp3` present; spec §Commit-allowance rows match live |
| LG-3 | 2026-10-04 developer-reported grant-enforcement evidence — over-writes vs counts (~27 write ops against a count-22 slip on `mybizz-config-docs`; 4 against count 3 on `/mnt/c/mybizz/scripts`) and two ungranted successful writes to `~/.config/opencode/skills`. Free row appended to the [[[mybizz-config-docs:cupcake/cupcake-log\|Log]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-log.md) at plan-synthesis time this run | **Developer-requested item — the GR investigation (§5)** |
| LG-4 | Spec refreshed 2026-10-01 (grant counts row dated 2026-09-21: four active grants — data-mybizz-mgt, dev, pdlf, memory-governor — counts 40–60; WP3 rows added) | Verify the live grants file against the spec's dated statement; flag only structural mismatch, not evolution |

## 4. Learnings-driven items

| # | Learning | Check |
|---|---|---|
| LE-1 | Source↔deployed fold-in: 20 sources ↔ 19 deployed — bash-governance compiled into the cross-project rule (same file/package, own rule id, 4 bash-shape indicator groups) | C2-4 as written; a "missing" bash-governance deployment is NOT a finding. Source leg pending read approval; deployed leg executes regardless |
| LE-2 | `.bak-*` files accumulate by design | C1-3 checks suffix discipline, never backup absence |
| LE-3 | Guard denials are dual-purpose: enforcement proof + reclassification signal | Denied checks → developer-run bundle; the denial logged as liveness evidence |

## 5. Developer-requested item — grant-enforcement investigation

Evidence (2026-10-04, developer report): writes exceeded granted counts (~27 write
ops against a count-22 slip on `mybizz-config-docs`; 4 against count 3 on
`/mnt/c/mybizz/scripts`), and two writes to `~/.config/opencode/skills` succeeded
although no grant for that folder was issued in the session. **Read-only first.**
Checks needing a write, or denied by a guard, are bundled as a developer-run
request with exact commands. Every finding classified DOWN / UNHEALTHY / DRIFT /
GAP.

Recorded facts feeding this item: re-granting a path REPLACES the count
([[[mybizz-config-docs:facts/2026-09-22-regrant-replaces-count]]](C:/mybizz/mybizz-config-docs/facts/2026-09-22-regrant-replaces-count.md)); decrements fire per successful edit op —
a count-26 slip was exhausted across 32 edit ops in the makepdlf run, the same
under-decrement class as today's evidence ([[[mybizz-config-docs:facts/2026-09-23-grant-decrement-per-edit-op]]](C:/mybizz/mybizz-config-docs/facts/2026-09-23-grant-decrement-per-edit-op.md));
`mg-grant` lowercases the granted path ([[[mybizz-config-docs:facts/2026-09-15-mg-grant-lowercase-paths]]](C:/mybizz/mybizz-config-docs/facts/2026-09-15-mg-grant-lowercase-paths.md));
CLI syntax is flag-based, failed attempts consume nothing
([[[mybizz-config-docs:facts/2026-09-23-grant-cli-flag-syntax]]](C:/mybizz/mybizz-config-docs/facts/2026-09-23-grant-cli-flag-syntax.md)).

| ID | Question | Method (read-only unless noted) |
|---|---|---|
| GR-1 | How does `mg-grant` record grants? | Read `~/.config/cupcake/bin/mg-grant` (and `mg-revoke`, `git-grant`): where state lives, full-regeneration vs in-place semantics, path canonicalization (the lowercase fact), count/expiry field handling, opa-check-before-overwrite discipline |
| GR-2 | Do counts decrease, and is the count enforced? | Read the plugin's decrement hook: which tools decrement, how the path key is matched (allow-check vs decrement — same canonicalization?), behavior on lookup miss or write failure (silent skip?), concurrency between simultaneous sessions; correlate with the live grants file, the 2026-10-04 evidence, and the 2026-09-23 under-decrement fact |
| GR-3 | Do grants expire? | Schema `expires_at_ns`; the plugin's before-hook prune; verify live entries' expiry stamps are structurally sane and actually compared against wall-clock |
| GR-4 | Does `mg-revoke` remove entries? | Read `mg-revoke`: what it removes, regeneration safety, behavior on an absent entry |
| GR-5 | Why did ungranted writes to `~/.config/opencode/skills` succeed? | Read the deployed cross-project rule: the always-open list (is `~/.config/opencode/skills` on it?), the project-boundary and grant checks for write-shaped ops; classify: documented always-open (spec GAP) vs allow-check defect (UNHEALTHY/DRIFT) |
| GR-6 | Live probes (write-needing) | Agent-executed only where harmless and clearly permitted; otherwise developer-run bundle with exact commands: issue a test grant → file-tool write → verify decrement → revoke → verify removal; expiry probe via a short-`--minutes` grant if supported |

## 6. Standing checks this run

Full ID'd inventory in the skill (Tiers 0–3, C0-1…C3-4). Execute Tier 0 → Tier 2 in
full, expected values from the spec read fresh. Run-specific deltas:

- C0-1: filesystem listing only, glob forms — never the enforcement binary's name in command text.
- C0-2: one harmless probe — curl to a non-allowlisted `.invalid` hostname; a received deny = liveness confirmed; an executed allow = `UNHEALTHY`, hand to developer.
- C2-4: deployed leg only until the rules-cupcake-global read approval lands.
- GR-1…GR-5 run alongside Tiers 1–2 (same inventory reads).

## 7. Report requirements

Per the skill and the orchestrator MO: verdict line; per-tier tables (check ID,
expected, actual, result); findings with class + evidence + recommended repair +
rollback + risk; runner attribution for every deferred item; liveness evidence
(which denial proved firing); every GR finding classified. **This run stops at the
gate:** the structured report is presented in-chat; the report-file write, the run
row, and any new learnings happen after the gate (per the developer's
stop-at-gate instruction; write-then-replace discipline still applies when the run
resumes).

## 8. Gate protocol

- No agent-healable items by design — all repairs developer-run or proposed through the report.
- Spec-doc corrections → flagged to docs governance, never applied here.
- Deny-list honored absolutely: anything inside `~/.config/cupcake/` or any `.cupcake/`; the plugin (live copy and backups); the binaries; `opencode.jsonc` permission section; `spawn-tools-denylist.json`; rule sources in `rules-cupcake-global/`.
- Every gate outcome recorded per-item (item id → approve/reject/defer) in the run row's disposition field when the run resumes past the gate.
- Credentials by variable name only, never printed.
