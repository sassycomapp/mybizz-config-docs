---
title: "magdoub-wireframe-exam-plan"
doc-id: "mb-1626420d"
---
# Magdoub Wireframe — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager before
each run from: [[magdoub-wireframe-config|Configuration]] (spec), the last
[[magdoub-wireframe-exam-report|Exam Report]], [[magdoub-wireframe-log|Log]] (events since last
run), [[magdoub-wireframe-learnings|Learnings]]. Consumed by the skill at run time;
rewritten at the start of the following cycle. The file is live; its contents are
transient.

**This first plan is hand-written** (emulation of the established architecture):
it also serves as the format template. The **standing check inventory lives in the
skill** ([[magdoub-wireframe-skill|Magdoub Wireframe Skill]], born-with-inventory); this plan carries
run-specifics and references. Once verified by a run, future plans carry
run-specifics + references only.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap) |
| Run date | set at execution |
| Prior report | none — placeholder present; missing prior report = expected, not silence |
| Step-0 result | recorded at execution |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request) | (a) any check whose command text the guards deny (expected classes: cross-project reads of `~/.claude/skills/wireframe/` and `~/.config/opencode/skills/wireframe/`; denied anyway → bundled, honored absolutely); (b) Tier 3 items if unlocked — MW3-1 (network probe against the upstream repo) and MW3-3 (update-policy re-confirmation) are developer-run by nature |
| Expected-value source of truth | [[magdoub-wireframe-config|Configuration]] — read fresh at run start; never rely on remembered values |
| Scope boundary | This module exams **the magdoub-wireframe skill installation and lifecycle**: the real clone, the OpenCode discovery symlink, the bundled file set, the runtime output structure, and the settled sync/update policy. What it does **not** probe: PDLF's step 22/26 usage of the skill and the [[adr-design-rules|Wireframe Design Rules]] ADR interplay (belong to the PDLF / project-library-global docs domain — open item 4, resolved 2026-09-16 via ADR §A); the `task`-tool guard layer itself (belongs to the cupcake/opencode modules — referenced, never re-verified); the upstream repository's content beyond the recorded HEAD match; gbrain's sync state (belongs to the gbrain module) |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). Recorded spec open items kept under
watch (observations, not findings):

| # | Watch item (config §Open items) | This run's action |
|---|---|---|
| W-1 | Phase 2 execution mechanism unresolved — SKILL.md instructs 5 parallel Task agents; sub-agent creation is prohibited standing policy (three-layer denial). How Phase 2 actually executes here is undecided | Confirm the constraint still holds (task tool absent — MW2-3). No mechanism decided unasked; option set surfaces at the gate (Tier 3 / open item) |
| W-2 | No confirmed real run of the skill anywhere in this environment | Confirm no-run state stands (MW1-4): no `wireframe/` output dirs, no `design-context.md` |
| W-3 | No security supply-chain review record at adoption (2026-07-02), per [[sec-dependency-skill-supply-chain|Dependency and Skill Supply Chain]] / [[sec-review-before-trust|Review Before Trust]] | Candidate Tier 3 item (MW3-2): perform + record the review, or record a deliberate deferral |
| W-4 | [[adr-design-rules|Wireframe Design Rules]] ADR vs the skill's fixed output format — reconciliation undocumented | **RESOLVED 2026-09-16** — ADR gained Section A (Magdoub-skill exemption); open item 4 closed. No action this run |
| W-5 | Old single-file reference doc retirement | Candidate gate item (MW3-2): retired or retained, developer decides |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-07-02 adoption + install (clone + symlink) | MW0-1 / MW0-2 topology still holds |
| LG-2 | 2026-08-12 old single-file reference created | MW1-7 presence check (open item 5) |
| LG-3 | 2026-09-06 suite created; settled policy set (gbrain ordinary sync; update developer-run only) | MW1-5 suite completeness (7 files + skill source); MW3-3 re-confirms update discipline |
| LG-4 | 2026-09-16 suite build-out | MW1-5 suite completeness (8 files); run #1 is the closure |

## 5. Learnings-driven items

| # | Learning | Check |
|---|---|---|
| — | none (learnings file empty at bootstrap) | — |

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in [[magdoub-wireframe-skill|Magdoub Wireframe Skill]] (Tiers 0–3). Summary:

- **Tier 0 (A) — invocability:** MW0-1 real clone present + pinned at recorded HEAD · MW0-2 discovery symlink resolves into the clone. Failure = DOWN, stop.
- **Tier 1 (A) — state conformance:** MW1-1 SKILL.md frontmatter identity (name `wireframe`, no version field) · MW1-2 install architecture (remote URL, branch, clean tree) · MW1-3 bundled files live-counted (line counts) · MW1-4 runtime output structure (no `design-context.md`, no output dirs — no-confirmed-run state) · MW1-5 suite completeness (8 files) · MW1-6 single discovery path (no double-load) · MW1-7 old single-file reference state
- **Tier 2 (A) — functional, present ≠ working:** MW2-1 symlink resolves + frontmatter real + skill invocable (`/wireframe`) · MW2-2 template files resolve at bundled paths with recorded line counts · MW2-3 discipline probe — `task` tool absent, Phase 2 not executed (open item 1 intact)
- **Tier 3 (D, locked):** MW3-1 full mechanical integrity audit (all bundled files byte-count + hash, tree clean) · MW3-2 open-item decisions (supply-chain review, reference-doc retirement) · MW3-3 update discipline re-confirmation (developer-run only, never AI-invoked)

## 7. Report requirements

The run writes [[magdoub-wireframe-exam-report|Exam Report]]: verdict line; per-tier tables
(check ID, expected, actual, result); findings with class + evidence + recommended
repair + risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace; failed runs never
touch the prior report; written before any pruning). Then: one run row appended to
[[magdoub-wireframe-log|Log]] (run-row format per [[config-manager-reference|Reference: Commands, Procedures]]);
new learnings filed.

## 8. Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items expected** — the clone is developer-owned (update
  developer-run only, standing policy); every repair/decision is developer-run or
  proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the real clone `~/.claude/skills/wireframe/`
  (never fetch/pull/reset by an agent — update command is developer-run only per
  settled policy) · the OpenCode discovery symlink (never a second discovery path —
  double-load) · Phase 2 Task-agent spawning (standing three-layer denial; execute
  Phase-1-only or proposed alternatives, never improvised sub-agents) · any
  Memory-Governor submission of skill content (permanent ordinary-`gbrain sync`
  bypass per settled policy)
- Credentials: variable names only, never printed
