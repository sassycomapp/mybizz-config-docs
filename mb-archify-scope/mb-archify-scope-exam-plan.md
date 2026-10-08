---
title: "mb-archify-scope-exam-plan"
doc-id: "mb-840bfc22"
updated: "2026-10-08"
---

# mb-archify-scope — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager
before each run from [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-config]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-config.md) (spec), the last
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-report]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-report.md), [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-log]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-log.md) (events since last
run), and [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-learnings]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-learnings.md). Consumed by the skill at run time;
rewritten at the start of the following cycle. The file is live; its contents
are transient.

**This first plan is hand-written** (bootstrap emulation of the proven
cycle); it also serves as the format template. The **standing check inventory
lives in the skill** ([[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-skill]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-skill.md), born-with-inventory);
this plan carries run-specifics and references.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap) |
| Run date | 2026-10-08 (plan synthesized 2026-10-07; run executes 2026-10-08 — the build-out grants expired mid-run 2026-10-07 ≈18:50 UTC, the session resumed 2026-10-08 08:26 UTC) |
| Prior report | none — placeholder present; missing prior report = expected, not silence |
| Step-0 result | recorded at execution ([[[mybizz-config-docs:mb-config-manager/config-manager-log\|Config Manager Log]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-log.md)) |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request at the gate) | (a) Tier 3 unlock decision (AS3-1 full spec-vs-live conformance walk; AS3-2 Phase-8 contract mechanism deep proof); (b) the one guard-forbidden Tier 1 class — AS1-10 Cupcake component-rule absence (rules path carries the sibling guard's token; exec-protection class proven live, mb-sentinel-review run #1 2026-10-07) — exact commands supplied with the bundle; (c) none else anticipated |
| Expected-value source of truth | [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-config]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-config.md) — read fresh at run start; never rely on remembered values |
| Named state-change steps (procedural conflicts stated, not asked) | **S-1 (2026-10-07):** the config-manager register held **no row** for this system where the build-out expects `WIP` — a row was added, state `WIP`, citing the developer instruction "run config-setup-prompt.md + config-manager-agent.md on target C:\mybizz\mybizz-config-docs\mb-archify-scope" (2026-10-07) and the precedents mb-sentinel-review S-1 / mb-sysdoc-creator S-1 (2026-10-07; original precedent mb-memory-system-diagnostic S-1, 2026-09-28). The spec doc exists — the system is examinable; the row addition (rather than a flip) is the delta from precedent, stated here. The row flips `WIP` → `Installed` at Phase 2 per the setup prompt. **S-2 (2026-10-07/08):** grant discipline — three grants issued by the developer 2026-10-07 (suite 12; config-manager 4; install 3) expired mid-run 2026-10-07 ≈18:50 UTC; one guard denial honored (suite edit refused at 2026-10-08 08:26 UTC — no retry, no reshape); three fresh grants issued 2026-10-08 (suite 6; config-manager 2; install 2); denials are never worked around. **S-3 (2026-10-07):** one guard denial honored at Phase 0 — the session-provenance page read (`sessions/2026-09-15-006-archify-scope-skill.md`) denied, sensitive-file class; not retried, not routed around; log seeded from the spec's Run history + git history instead |
| Scope boundary | This module exams **the `mb-archify-scope` skill system itself**: the subject repo (shape + git state), the installed copy (identity, integrity, frontmatter shape), the GBrain registration row, this suite's documents, the archify suite's documented component facts, and the recorded run artifacts' state. **Sibling-module ownership (anti-duplication):** the Archify tool installation/lifecycle is owned by `mb-config-archify` (its AR2-3 parallels this module's AS1-2 — overlapping detection, no duplicated healing); GBrain's sync engine is owned by `mb-config-gbrain` (this module checks the registration row's shape only); Cupcake internals are owned by `mb-config-cupcake` (AS1-10 is a developer-run read of the spec's recorded absence claim, never a Cupcake probe). **Running the subject skill is out of scope** (interactive scoping session; first write only on approval). Run-artifact content quality is out of scope (Archify's domain). |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). Spec open items kept under watch
(observations, not findings):

| # | Watch item (spec open items) | This run's action |
|---|---|---|
| W-1 | Spec §File conventions (repo spec) reads flat `output/{subject}-*`; the live convention since 2026-09-16 nests under `output/{slug}/` — two path shapes in one contract (spec open item 1; correction developer-owned) | AS3-1 verifies the discrepancy still exists; proposed correction raised at the gate (flagged, never applied) |
| W-2 | Fact ownership — archify-config §Scoping skill component is to be reduced to a cross-reference pointer (developer-run edit, separate task; spec open item 2) | Standing watch; AS1-8 verifies the documented facts still stand until the reduction lands |
| W-3 | mybizz-config-docs has no suite register (flagged, not created; spec open item 3) | Standing watch; no exam action |
| W-4 | Cupcake skills-dir ancestor-cwd case unresolved (carried in the cupcake exam report; spec open item 4); installed-copy writes treated as grant-required from every session | Standing watch; Cupcake internals out of scope; AS2-4 verifies the sync discipline still documents the grant requirement |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-09-16: AR2-3 drift event — the installed copy was found stale (missing Phase 9) after the spec was edited post-install; gate-approved re-copy closed it | AS1-2 + AS1-3 formalize the hash-pair check every run; the class (spec-edited-after-install) is the expected DRIFT direction to flag first on any divergence |
| LG-2 | 2026-10-04: spec body update applied by hand to both files (no mechanical sync exists) | AS1-2 + AS1-4 verify the manual sync discipline held (body identity + frontmatter shapes) |
| LG-3 | 2026-10-07: suite created (commit 09128dd); build-out initiated; S-1/S-2/S-3 executed | AS1-6 + AS1-7 verify the built state; the register flip is verified at Phase 2 |
| LG-4 | 2026-10-07: S-3 guard denial honored (sessions-page read, sensitive-file class) | Recorded class (sensitive-file lane, `sessions/`); no retry; no check depends on that page |

## 5. Learnings-driven items

None — bootstrap (the learnings table is empty at first plan synthesis).

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in the [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-skill]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-skill.md) (Tiers 0–3).
Summary:

- **Tier 0 (A) — invocability:** AS0-1 installed copy present with functional frontmatter · AS0-2 discoverable in the session skill surface · AS0-3 spec doc present (absent = DOWN, stop)
- **Tier 1 (A) — state conformance:** AS1-1 repo shape (`.git/` + spec only) · AS1-2 body-hash pair identical · AS1-3 recorded sizes · AS1-4 frontmatter discipline · AS1-5 GBrain registration row · AS1-6 suite completeness (8 files) · AS1-7 register row · AS1-8 integration mirror-facts · AS1-9 run artifacts present — plus **Tier 1 (D), guard-forbidden class:** AS1-10 Cupcake component-rule absence
- **Tier 2 (A) — functional proof (present ≠ working; read-only only):** AS2-1 machine-parsable + body intact · AS2-2 behavioral discipline intact (read-only-until-Phase-8; hard gate; abort-and-reshape; probe declared-not-executed; sync rule) · AS2-3 repo live (HEAD, clean, GitHub-backed) · AS2-4 sync discipline documented (body-to-body; never plain-copy)
- **Tier 3 (D, locked):** AS3-1 full spec-vs-live conformance walk · AS3-2 Phase-8 contract mechanism deep proof (header schema + card byte-match + render evidence)

## 7. Report requirements

The run writes [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-report]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-report.md): verdict line; per-tier
tables (check ID, expected, actual, result); findings with class + evidence +
recommended repair + risk; runner attribution for every deferred item
(guard-forbidden vs unlock-gated). Overwritten in full each run
(write-then-replace; failed runs never touch the prior report; written before
any pruning). Then: one run row appended to [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-log]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-log.md) (run-row
format per [[[mybizz-config-docs:mb-config-manager/config-manager-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-reference.md)); new learnings filed.

## 8. Gate protocol

- Findings → classify (`DOWN`/`UNHEALTHY`/`DRIFT`/`GAP`) → present with
  evidence + recommended repair + risk — per-item decisions, never batched
- Agent-healable: suite-file repairs only (config-manager standard);
  everything else developer-run or proposed
- Deny-list (never heal, never touch without the developer's explicit
  per-item approval naming the file): the installed subject copy · the repo
  spec · the archify suite's documents · GBrain's engine · Cupcake internals ·
  run artifacts
- Spec-doc corrections → flagged at the gate, never applied here
- Tier 3 unlock decision asked at the gate, never assumed
- Credentials: none in this system — no credential route exists (exam skill
  §Credential discipline)
