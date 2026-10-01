---
title: "graphify-exam-plan"
doc-id: "mb-282b3d7f"
updated: "2026-10-01"
---
# Graphify — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager before
each run from: [[[mybizz-config-docs:graphify/graphify-config|Graphify Configuration]]](C:/mybizz/mybizz-config-docs/graphify/graphify-config.md) (spec), the last [[[mybizz-config-docs:graphify/graphify-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/graphify/graphify-exam-report.md),
[[[mybizz-config-docs:graphify/graphify-log|Log]]](C:/mybizz/mybizz-config-docs/graphify/graphify-log.md) (events since last run), [[[mybizz-config-docs:graphify/graphify-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/graphify/graphify-learnings.md). Consumed by the
skill at run time; rewritten at the start of the following cycle. The file is live;
its contents are transient.

**This first plan is hand-written** (emulation of the gbrain-dream-cycle
architecture): it also serves as the format template. The **standing check
inventory lives in the skill** ([[[mybizz-config-docs:graphify/graphify-skill|Graphify Skill]]](C:/mybizz/mybizz-config-docs/graphify/graphify-skill.md), born-with-inventory); this
plan carries run-specifics and references. Once verified by a run, future plans
carry run-specifics + references only.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap) |
| Run date | set at execution |
| Prior report | none — placeholder present; missing prior report = expected, not silence |
| Step-0 result | recorded at execution |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request) | (a) upstream version check via PyPI (`pip index versions graphifyy`) if the outbound-network guard denies the agent attempt (proven class); (b) any check whose command text or target file the guards deny (config-file reads are proven agent-readable for this suite as of 2026-09-14, but a denial is always honored) |
| Expected-value source of truth | [[[mybizz-config-docs:graphify/graphify-config\|Graphify Configuration]]](C:/mybizz/mybizz-config-docs/graphify/graphify-config.md) — read fresh at run start; never rely on remembered values |
| Scope boundary | GBrain-side conformance belongs to `mb-config-gbrain`; the shared AGENTS.md block's **content** is owned by [[[mybizz-os-docs:os-reference-docs/memory-master-explainer\|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) (this exam verifies marker presence only); OpenCode global configuration belongs to `mb-config-opencode` (when built); PostgreSQL-level checks belong to `mb-config-postgresql` (the `--postgres` extraction path is unused here); **mb-3-cs project health is nobody's exam here** — only graphify's footprint in that repo (scope files, graph artifact, plugin files, MCP entry, block markers) is examinable |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). Recorded spec states kept under watch
(observations, not findings):

| # | Watch item (config open items) | This run's action |
|---|---|---|
| W-1 | `--exclude` flag: absent from 0.9.40 help; a prior suite claimed it functional — unverified in this version | Confirm continued absence from `graphify --help` output (read-only); do not probe upstream |
| W-2 | Upgrade decision open: installed 0.9.40 vs upstream 0.9.56 (repo `v8`); upstream features conflict with standing decisions (committed-graph team model, PR-triage dashboards, HTTP MCP transport) | Never an upgrade trigger — GF3-2 developer decision only; policy: never on newness, only on check failure |
| W-3 | mb-3-cs project paused (deployment waits on PDLF completion); HEAD observed ahead of graph provenance 2026-09-14 (log row) | GF1-4 provenance equality is the hard check; weigh any DRIFT finding against paused status at the gate — the state is reportable even when the repair is deferrable |
| W-4 | Community labels are deterministic representative-node names (LLM labeling package `anthropic` not installed — accepted state) | GF1-9 confirms the state; presence of the package = labeling state changed → spec-refresh flag |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-08-15 manual backup of prior graph state | Verify `graphify-out/2026-08-15/` still present and untracked (state observation, not a requirement) |
| LG-2 | 2026-09-08 full spec verification baseline | Expected values read fresh from the spec; counters treated point-in-time (LE-1) |
| LG-3 | 2026-09-14 HEAD-movement observation + suite build-out rows | GF1-4 provenance check is the designated decision point; W-3 context applies |

## 5. Learnings-driven items

| # | Learning | Check |
|---|---|---|
| LE-1 | All graph counters are point-in-time (nodes/edges/communities/ghosts move with the codebase; the project is paused but not frozen) | Compare vs the 2026-09-08 recorded values + explainability; exact equality never asserted; provenance equality (`built_at_commit` vs HEAD) is the hard check, not the counts |

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in [[[mybizz-config-docs:graphify/graphify-skill|Graphify Skill]]](C:/mybizz/mybizz-config-docs/graphify/graphify-skill.md) (Tiers 0–3). Summary:

- **Tier 0 (A) — invocability:** GF0-1 CLI version 0.9.40 · GF0-2 package `graphifyy` 0.9.40 (CLI and package agree) · GF0-3 executable + module paths · GF0-4 OpenCode skill surface + `.graphify_version` marker
- **Tier 1 (A/D) — state conformance:** GF1-1 upstream lag state (agent-attempted → developer bundle on denial) · GF1-2 scope config (`.graphifyignore`, `.graphify_build.json`, `.graphify_root`) · GF1-3 repo `.gitignore` lines · GF1-4 graph provenance + shape vs spec · GF1-5 MCP entry (project-root `opencode.json`) · GF1-6 AGENTS.md block markers · GF1-7 plugin surface · GF1-8 suite completeness (8 files) · GF1-9 labeling state (`anthropic` absent)
- **Tier 2 (A) — functional, present ≠ working:** GF2-1 safe read-only execution probe (`god-nodes --json`) · GF2-2 discipline probe (`check-update` — verdict output distinguishes tool health from graph state)
- **Tier 3 (D, locked):** GF3-1 graph realign/rebuild (content-changing) · GF3-2 upgrade execution (developer decision; policy: only on check failure)

## 7. Report requirements

The run writes [[[mybizz-config-docs:graphify/graphify-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/graphify/graphify-exam-report.md): verdict line; per-tier tables (check
ID, expected, actual, result); findings with class + evidence + recommended
repair + risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace; failed runs
never touch the prior report; written before any pruning). Then: one run row
appended to [[[mybizz-config-docs:graphify/graphify-log|Log]]](C:/mybizz/mybizz-config-docs/graphify/graphify-log.md) (run-row format per [[[mybizz-config-docs:mb-config-manager/config-manager-reference|Reference: Commands, Procedures]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-reference.md));
new learnings filed.

## 8. Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items** — graphify lives in user site-packages and external
  repos; every repair is developer-run or proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch from this exam): anything content-changing
  (`extract`, `update`, `watch`, `install`, `uninstall`, `hook install`,
  `global add/remove`) without developer unlock · the mb-3-cs repo itself (no
  file writes of any kind) · the AGENTS.md block **content** (markers verified,
  content owned by [[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md)) · any `mcp.*` entry (never
  added or changed by the exam; a full OpenCode process restart is required for
  any legitimate change, developer-run) · the tracking status of `graphify-out/`
  (standing decision: gitignored — a change re-opens the hooks tripwire) ·
  no API key exists for code-only work — never prompt for one
- Credentials: none configured for this system's code-only posture; if a check
  appears to require a key, that is itself a DRIFT finding (the semantic-backend
  state changed)
