---
title: "gbrain-exam-plan"
doc-id: "mb-85164f9c"
updated: "2026-10-04"
---
# GBrain — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager before
each run from: [[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) (spec), the last [[[mybizz-config-docs:gbrain/gbrain-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-exam-report.md),
[[[mybizz-config-docs:gbrain/gbrain-log|Log]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-log.md) (events since last run), [[[mybizz-config-docs:gbrain/gbrain-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-learnings.md). Consumed by the
skill at run time; rewritten at the start of the following cycle. The file is
live; its contents are transient.

**This first plan is hand-written** (emulation of the PostgreSQL architecture): it
also serves as the format template — the standing-checks section below is the
complete, authoritative enumeration of every check the exam performs. Once
verified by a run, it graduates into the skill, and future plans carry
run-specifics + references instead.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (pilot 2026-09-12 was detection-only, pre-architecture) |
| Run date | set at execution |
| Prior report | [[[mybizz-config-docs:gbrain/gbrain-exam-report\|Exam Report]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-exam-report.md) (2026-09-12, pilot) |
| Step-0 result | recorded at execution |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request) | (a) `~/.gbrain/config.json` content checks (sensitive-data guard blocks agent reads — proven 2026-09-12); (b) any check whose command text the guards deny |
| Expected-value source of truth | [[[mybizz-config-docs:gbrain/gbrain-config\|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) — read fresh at run start; never rely on remembered values |
| Scope boundary | DB-level checks (tables/RLS/roles/extensions/coverage) belong to `mb-config-postgresql` — this exam cross-references its current report, never re-probes |

## 2. Carried-forward items (from pilot report, 2026-09-12)

| # | Item | Why deferred | This run's action |
|---|---|---|---|
| CF-1 | Finding 1 — new 14th source `pdlf` vs spec's 13 | docs-governance flag | Verify whether governance approved + applied; re-inventory and compare |
| CF-2 | Finding 2 — page-count table stale + **273-page accounting gap** (sources sum < identity total) | docs-governance flag + open question | Re-compute both sums; investigate attribution per-source if queryable |
| CF-3 | Finding 3 — legacy `brain.pglite` absent vs spec "present (stale)" | docs-governance flag | Confirm absence; re-flag until spec refreshed |
| CF-4 | Finding 4 — skills bundle evolved (65 entries, no `skillify`, 4 underscore files vs spec "60 + skillify = 61") | docs-governance flag | Re-inventory; compare |
| CF-5 | Finding 5 — `config.json` content checks | sensitive-data guard blocks agent | Bundle into the developer-run request |

## 3. Erred last run (distinct from deferred)

| # | What erred | This run's action |
|---|---|---|
| ER-1 | `jq`/`cat` on `~/.gbrain/config.json` denied (sensitive-data guard) | Config-content probes are permanently developer-run; agent verifies existence/permissions only |
| ER-2 | Pilot used remembered DB facts for gbrain-specific conformance | This run: cross-reference the postgres module's current report instead of re-probing (scope boundary) |

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-09-13 sync+embed runs (post-commit): 54 + 2 pages added, brain grew to ~1,880 | Count growth is expected-at-sync (learning: counts drift by design); coverage % is the durable check |
| LG-2 | No crashes/incidents logged | If a new log row exists at synthesis time, derive a targeted probe from it |

## 5. Learnings-driven items

| # | Learning | Check |
|---|---|---|
| LE-1 | Count-type values drift by design at every sync (established on postgres run #2) | Coverage % + growth explainability checked; exact count equality never asserted |

## 6. Standing checks — the complete enumeration (Tiers 0-3)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass rule.
This enumeration graduates into the skill after a verified run; future plans carry
run-specific deltas only.

### Tier 0 — Liveness (run first; any failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| G0-1 | A | Binary resolves: `/home/dev-p/.bun/bin/gbrain` exists; `/home/dev-p/gbrain/VERSION` readable | Both present; VERSION matches spec |
| G0-2 | A | Engine responds: brain identity call (MCP) returns version + counters without error | 0.46.1.0, engine postgres, counters sane |
| G0-3 | A | DB ping on `gbrain` database | `SELECT 1` returns 1 (same probe as postgres Tier 0) |

### Tier 1 — Health

| ID | Runner | Check | Expected |
|---|---|---|---|
| G1-1 | A | `sources list` — every registered source's path exists on disk; page counts sane (growth-at-sync expected; only zero-count or missing-path = anomaly) | 14 live (spec 13 + `pdlf` until spec refreshed) |
| G1-2 | A | Sync machinery: `~/.gbrain/sync-failures.jsonl` empty; crontab holds no gbrain entries | Both clean (any cron reappearance = finding) |
| G1-3 | A | Embedding coverage — cross-reference the postgres module's current exam report (never re-probe) | 100% |
| G1-4 | A | Legacy artifact `~/.gbrain/brain.pglite` — record presence or absence | Absence expected (documented stale artifact; spec-drift flag until refreshed) |
| G1-5 | A | `~/.gbrain/` directory integrity — listing only (names/metadata; **never read `config.json`**) | Structure matches spec's config-file inventory; config.json present with restrictive permissions |

### Tier 2 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| G2-1 | A | Version | live 0.46.1.0; upstream gap recorded, **never upgraded on newness** (upgrade only on check failure) |
| G2-2 | A | Schema pack (MCP) | `gbrain-everything@1.0.0+7021205a`, 30 page types / 12 link types |
| G2-3 | A | MCP integration entry | `opencode.jsonc` → `mcp.gbrain`: local, `["/home/dev-p/.bun/bin/gbrain", "serve"]`, enabled true, env names OPENAI_API_KEY + ZEROENTROPY_API_KEY |
| G2-4 | A | Models (via DB `config` table — agent-safe, unlike `config.json`) | embedding `openai:text-embedding-3-large`, dims 1536 |
| G2-5 | A | Skills bundle at `/mnt/c/dev/dev-mb-3-cs/mb-3-cs/.opencode/skills/` | re-inventory vs spec (bundle-evolved drift class — flag until spec refreshed) |
| G2-6 | A | Page accounting — identity total vs sources-list sum | sums reconcile or the gap is explained (the 273 question, CF-2) |
| G2-7 | A | Registered source paths all exist | 14/14 present on disk |

### Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| G3-1 | D | `config.json` content: `self_upgrade_mode: notify`; no API keys inside; DB URL present | as spec |
| G3-2 | D | Full sync verification on a sample source (writes — content-changing) | clean sync, no failures |
| G3-3 | D | MCP server restart behavior (config changes need full process restart) | documented behavior holds |
| G3-4 | D | Upgrade decision (0.46.1.0 → 0.50.0.0) | policy question — developer's, never agent-initiated |

## 7. Report requirements

The run writes [[[mybizz-config-docs:gbrain/gbrain-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-exam-report.md): verdict line; per-tier tables (check ID,
expected, actual, result); findings with class + evidence + recommended repair;
runner attribution for every deferred item (guard-forbidden vs unlock-gated);
overwritten in full each run (write-then-replace). Then: one run row appended to
[[[mybizz-config-docs:gbrain/gbrain-log|Log]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-log.md) (run-row format per [[[mybizz-config-docs:mb-config-manager/config-manager-reference|Reference: Commands, Procedures]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-reference.md)); new learnings
filed.

## 8. Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No live-system heals defined for gbrain** — sync, schema changes, upgrades,
  source registration are all state changes to a memory system governed elsewhere;
  diagnosis + proposal only
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): `~/.gbrain/config.json` (never hand-edited,
  never printed) · the live install at `/home/dev-p/gbrain` · the source clone's
  staleness question (never resolve unilaterally) · env-managed API keys · the MCP
  entry in `opencode.jsonc` (self-governing config) · any `gbrain sync`/`embed`
  execution without explicit developer go
- Credentials: variable names only, never printed
