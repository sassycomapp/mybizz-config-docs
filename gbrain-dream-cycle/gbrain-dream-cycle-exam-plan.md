---
title: "gbrain-dream-cycle-exam-plan"
doc-id: "gbrain-dream-cycle-exam-plan"
---
# GBrain Dream Cycle — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager before
each run from: [[gbrain-dream-cycle-config|Configuration]] (spec), the last
[[gbrain-dream-cycle-exam-report|Exam Report]], [[gbrain-dream-cycle-log|Log]] (events since last
run), [[gbrain-dream-cycle-learnings|Learnings]]. Consumed by the skill at run time;
rewritten at the start of the following cycle. The file is live; its contents are
transient.

**This first plan is hand-written** (emulation of the PostgreSQL architecture): it
also serves as the format template. The **standing check inventory lives in the
skill** ([[gbrain-dream-cycle-skill|Gbrain Dream Cycle Skill]], born-with-inventory); this plan carries
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
| Developer-run requests this run (bundled into ONE request) | (a) `~/.gbrain/config.json` content check — `mcp_surface` key absence (sensitive-data guard blocks agent reads — proven class); (b) ANTHROPIC_API_KEY validity curl, if the guard denies the agent attempt; (c) any check whose command text the guards deny |
| Expected-value source of truth | [[gbrain-dream-cycle-config|Configuration]] — read fresh at run start; never rely on remembered values |
| Scope boundary | Parent `mb-config-gbrain` owns binary/version/config/schema-pack/sources/models/MCP/sync conformance — this exam cross-references its current report, never re-probes (version echo DC0-1 is the one permitted overlap); DB-level checks belong to `mb-config-postgresql`; resolved call-graph belongs to Graphify |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). Recorded spec states kept under watch
(observations, not findings):

| # | Watch item (config open items) | This run's action |
|---|---|---|
| W-1 | Upstream `dream.*` config surface (triage cascade, oneshot synthesis, spend telemetry) unverified against 0.46.1.0; no such keys exist locally | Confirm no local keys exist (via the developer bundle's config check); do not probe upstream |
| W-2 | Orphan backlog: 1,177 of 1,755 pages with no inbound links (2026-09-06) | Re-count via the orphans probe; growth expected (LE-1); content-hygiene backlog, not a defect |
| W-3 | Doctor `cycle_freshness` FAIL on a freshly-synced, just-dreamed brain — stamp updates only when the cycle's sync phase processes real new commits | Verify mechanism matches the documented behavior; a FAIL here is **not** a defect |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-08-16 gstack `--dream` source-overlap trap | Knowledge check only — reference's bypass guidance present; no live probe |
| LG-2 | 2026-09-05/06 autopilot found inert and removed | DC0-2 executes the absence check |
| LG-3 | 2026-09-06 silent `extract_atoms` outage (expired key behind a bare failure count) | Credential-first doctrine embedded in DC1-1; per-phase JSON rule embedded in DC2-1 |
| LG-4 | No crashes/incidents logged since | If a new log row exists at synthesis time, derive a targeted probe from it |

## 5. Learnings-driven items

| # | Learning | Check |
|---|---|---|
| LE-1 | All dream-cycle counters are point-in-time (pages/orphans/atoms move with content; a purge decrease is work done) | Compare vs last recorded + explainability; exact equality never asserted |

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in [[gbrain-dream-cycle-skill|Gbrain Dream Cycle Skill]] (Tiers 0–3). Summary:

- **Tier 0 (A) — invocability:** DC0-1 version 0.46.1.0 · DC0-2 autopilot absent (crontab + script + log) · DC0-3 schema pack `gbrain-everything@1.0.0` (`7021205a`) unchanged
- **Tier 1 (A/D) — state conformance:** DC1-1 Anthropic credential present, env-only (validity curl agent-attempted → developer bundle on denial) · DC1-2 trigger surfaces exist · DC1-3 no `mcp_surface` key (D — config content) · DC1-4 `code` `extractable: false` intact · DC1-5 suite completeness (7 files)
- **Tier 2 (A) — functional, present ≠ working:** DC2-1 safe single-phase probe `--phase orphans --json` (expected ok/warn-with-count) · DC2-2 suspected-contradictions probe with a real query (bare syntax fails exit 2 — query required)
- **Tier 3 (D, locked):** DC3-1 full dream cycle + complete post-run verification procedure · DC3-2 upgrade execution (developer decision; policy: only on check failure)

## 7. Report requirements

The run writes [[gbrain-dream-cycle-exam-report|Exam Report]]: verdict line; per-tier tables
(check ID, expected, actual, result); findings with class + evidence + recommended
repair + risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace; failed runs never
touch the prior report; written before any pruning). Then: one run row appended to
[[gbrain-dream-cycle-log|Log]] (run-row format per [[config-manager-reference|Reference: Commands, Procedures]]);
new learnings filed.

## 8. Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items** — the Dream Cycle is part of GBrain (a memory
  system governed elsewhere); every repair is developer-run or proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): `~/.gbrain/config.json` (never read by the
  agent, never printed) · env-managed API keys (name only) · the autopilot
  schedule (re-enabling it or any scheduler contradicts the deliberate design) ·
  any `gbrain sync` execution · any full dream cycle without explicit developer
  go (content-changing, LLM spend)
- Credentials: variable names only, never printed
