---
name: mb-config-graphify
description: Graphify configuration exam — verifies the installed Graphify toolchain (CLI/package identity, OpenCode skill surface, mb-3-cs scope configuration, graph artifact provenance and shape, OpenCode MCP entry, AGENTS.md guidance-block markers, plugin surface) against graphify-config.md and proves the query surfaces functionally execute; detection and verification only — Graphify is working well and this module changes nothing; catches silent failures and proposes gated repairs. Use when asked to "exam graphify", "check graphify health", or as part of a full mb-config-manager run.
---

# mb-config-graphify — Exam Skill

Exams Graphify's configuration state against its spec. This skill holds the
**procedure** only — expected values live in the spec doc and are read fresh
at the start of every run. Graphify is working well; this exam verifies that
and repairs nothing.

- Spec: `graphify/graphify-config.md` — read it first, every run
- **Exam plan: `graphify/graphify-exam-plan.md` — read second, every run.**
  The plan-driven cycle: the config-manager synthesizes this plan fresh before
  each run (from spec + last report + log + learnings) and this skill executes
  it in hand. The plan carries run-specifics and deltas; the **standing check
  inventory lives in this skill** (below) — permanent occurrences graduate
  here, never into plans
- Reference: `graphify/graphify-reference.md` — commands, procedures, the
  Do-not list
- Report: `graphify/graphify-exam-report.md` — one file, overwritten each run
  (write-then-replace)
- Log: `graphify/graphify-log.md` — one run row per exam; free rows for
  notable events witnessed between runs
- Learnings: `graphify/graphify-learnings.md` — file new patterns/nuances;
  delete entries once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **Graphify**: installed toolchain identity (CLI, package,
  OpenCode skill surface), the mb-3-cs scope configuration (`.graphifyignore`,
  build-state sidecars, repo `.gitignore` lines), the graph artifact
  (provenance, shape, counts), and the integration surfaces (project-root
  `opencode.json` MCP entry, AGENTS.md block markers, plugin files).
- **GBrain-side conformance** belongs to `mb-config-gbrain` — cross-reference
  its current report, never re-probe.
- **The AGENTS.md block's content** (single shared GBrain+Graphify guidance
  block) is owned by `mybizz-os-docs/memory-master-explainer.md` — this module
  verifies marker presence only, never reads content as authority, never edits.
- **OpenCode global configuration** belongs to `mb-config-opencode` (when
  built) — the repo-local `opencode.json` here is examined only as Graphify's
  integration surface.
- **Database-level checks** belong to `mb-config-postgresql` — the
  `--postgres` extraction path is unused in this environment.
- **mb-3-cs project health** (its code, its tests, its deployment state) is
  nobody's exam here — only Graphify's footprint in that repo is examinable.

## Credential discipline (hard rule)

The code-only configuration has **no API key**: AST extraction needs none,
none is configured, none is needed. Never prompt for one. If any check
appears to require a key, that is itself a DRIFT finding (the
semantic-backend state changed) — report it, never satisfy it. No credential
values are ever printed, logged, or copied into reports, outputs, or
learnings.

## Hard behavioral rules (from the suite's own Do-not list)

- Never run `graphify install` outside the target repo root — and never run
  it at all from this exam (registration-writing).
- Never trust a `path` result without `--undirected` for cross-file
  relationships (the stored graph is undirected; the directed default returns
  "no path found" on real edges).
- Never run a shrink rebuild without `--force` — it refuses and writes
  nothing — and never run any rebuild from this exam (Tier 3,
  developer-unlocked only).
- Never assume `extract`/`update` produce `GRAPH_REPORT.md`/`graph.html` —
  `cluster-only` makes those.
- Never treat INFERRED edges as settled fact; EXTRACTED edges are read,
  INFERRED/AMBIGUOUS need verification.
- Never add or change any `mcp.*` entry and expect tools without a full
  OpenCode process restart (quit and relaunch, not a new chat session).
- Never install hooks or the merge driver without re-examining the gitignore
  premise — the standing decision is "not installed" (tripwire, not closed).
- Never track `graphify-out/` without a fresh credential-shaped scan
  (`sk-`, `AKIA`, `ghp_`, `xoxb`, PEM headers) — the standing decision is
  "gitignored".
- Never prompt for an API key for code-only work — none exists, none is
  needed.
- **Never run `graphify extract` or `cluster-only` from any directory other
  than the target repo root** (run #1 F-4, proven live 2026-09-14): extract
  stamps `built_at_commit` from the invoking working directory's git repo,
  not the scanned path — a rebuild run from another repo mis-stamps
  provenance onto the graph.
- Read-only probes only: the exam never writes to the mb-3-cs repo, the
  graph artifact, or any registration surface.
- Before trusting any current-state answer from the graph (in this exam or
  any other context), `built_at_commit` must equal `git rev-parse HEAD`.

## Run #1 lessons graduated (2026-09-14)

- **F-4 cwd provenance (above):** the rebuild procedure's step-4 provenance
  confirmation (`built_at_commit` == `git rev-parse HEAD`) is mandatory,
  never optional — it is what caught the mis-stamp.
- **`check-update` semantics:** silent on success — the verdict comes from
  the exit code, never stdout; its silence is not a currency claim.
  Currency truth stays with `built_at_commit` vs HEAD (GF1-4).
- **Count-delta discipline:** after any update/rebuild, the count change
  must be explained against the actual commits (or the code-only semantics:
  a fresh build carries no document-derived concept nodes) before
  acceptance — the 2026-09-14 shrink 574→562 (removed document) and
  562→537 (code-only fresh baseline, matching the 2026-08-15 era) were both
  explained, not assumed.

## Tier 0 — Invocability (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| GF0-1 | A | `graphify --version` | `0.9.40` (config §Identity). The available upgrade is a recorded open item — **never upgraded on newness**; upgrade only on check failure (GF3-2) |
| GF0-2 | A | `pip show graphifyy` | Name `graphifyy` (double-y; other `graphify*` packages unaffiliated), Version `0.9.40` — CLI and package agree (config §Identity) |
| GF0-3 | A | Executable + module paths: `command -v graphify` → `/home/dev-p/.local/bin/graphify`; module directory exists at `/home/dev-p/.local/lib/python3.12/site-packages/graphify/` | Both exact (config §Identity) |
| GF0-4 | A | OpenCode skill surface: `~/.config/opencode/skills/graphify/` holds `SKILL.md` + `references/`; `.graphify_version` marker reads `0.9.40` | All present; marker agrees with the CLI (config §Identity — Skill) |

## Tier 1 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| GF1-1 | A→D | Upstream lag state: `pip index versions graphifyy` (outbound network — agent-attempted; guard denial → developer bundle) | Installed behind latest (spec records `0.9.56` as of 2026-09-08); a newer upstream number = spec-refresh flag, never an upgrade trigger |
| GF1-2 | A | Scope config: `$MB/.graphifyignore` exactly two lines (`.opencode/`, `opencode.json`); `$MB/graphify-out/.graphify_build.json` = `{"gitignore": false}`; `$MB/graphify-out/.graphify_root` = `/mnt/c/dev/dev-mb-3-cs/mb-3-cs` | All exact (config §Scope configuration). `$MB` = `/mnt/c/dev/dev-mb-3-cs/mb-3-cs` |
| GF1-3 | A | Repo `.gitignore` graphify-relevant lines: `graphify-out/`, `.opencode/`, `agents.md`, `opencode.json`, `tests/` | All present (config §Scope configuration — repo `.gitignore`) |
| GF1-4 | A | Graph provenance + shape: `built_at_commit` vs live `git -C $MB rev-parse HEAD`; nodes/edges/communities/confidence/ghost counts vs the spec's recorded values (574 / 468 / 158 / 451 EXTRACTED + 17 INFERRED + 0 AMBIGUOUS / 95 ghost template nodes); `directed` = `false`; artifact `$MB/graphify-out/graph.json` exists | **Provenance equality is the hard check — mismatch = DRIFT** (authority model §7.3: a stale graph describes code that no longer exists). Counts are point-in-time (LE-1): movement vs the 2026-09-08 recording is explainable, exact equality never asserted; `directed: false` is structural, mismatch = DRIFT |
| GF1-5 | A | MCP entry in the **project-root** `opencode.json` (the gitignored one — not `.opencode/opencode.json`, which is plugin registration): `mcp.graphify` type `local`, enabled `true`, command `["/usr/bin/python3", "-m", "graphify.serve", "/mnt/c/dev/dev-mb-3-cs/mb-3-cs/graphify-out/graph.json"]`, no API-key field | Exact (config §OpenCode MCP integration). Config-file read class: proven agent-readable 2026-09-14; a guard denial → developer bundle, never an alternate path |
| GF1-6 | A | AGENTS.md guidance block: `<!-- BEGIN GRAPH MEMORY GUIDANCE -->` … `<!-- END GRAPH MEMORY GUIDANCE -->` markers present in `$MB/AGENTS.md` | Both present (config §Related integration facts). Position may move — the markers are the invariant, never line numbers. Markers only; block content owned by `memory-master-explainer.md` |
| GF1-7 | A | Plugin surface: `$MB/.opencode/plugins/graphify.js` exists (bash-reminder hook; writes no files of its own); `$MB/.opencode/node_modules/` exists | Both present (config §Install surface — repo-local scope) |
| GF1-8 | A | Suite completeness: eight files in `graphify/` (config, exam-plan, exam-report, log, learnings, explainer, reference, skill) | All present (missing file = GAP) |
| GF1-9 | A | Labeling state: `pip show anthropic` absent from site-packages (community labels are deterministic representative-node names — accepted state) | Absent (config §Related integration facts). Presence = labeling state changed → spec-refresh flag, not a defect |

## Tier 2 — Functional proof (present ≠ working; read-only reporting surfaces — no mutation from detection)

| ID | Runner | Check | Expected |
|---|---|---|---|
| GF2-1 | A | Safe read-only execution probe: `graphify god-nodes --top 3 --json --graph $MB/graphify-out/graph.json` | Runs to completion and returns JSON — proves the graph artifact loads and a query surface executes for real |
| GF2-2 | A | Discipline probe: `graphify check-update $MB` | Runs to completion with an explicit needs-update verdict. On a provenance-lagged graph, `needs update = true` is **the tool working correctly**, not a second defect — the state finding lives in GF1-4; the two must never be conflated |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| GF3-1 | D | Graph realign/rebuild: `graphify update $MB` (realign after new commits) or the full documented rebuild (`graphify extract $MB --force --code-only`, then `cluster-only` when report/HTML are wanted) + provenance confirmation | Executes only on developer unlock; content-changing to the derived artifact (gitignored, reproducible at zero API cost). Procedure per reference §Procedures |
| GF3-2 | D | Upgrade execution (0.9.40 → upstream latest) | Developer decision, open (W-2); policy: **never on newness — only on check failure**. Upstream features conflict with standing decisions (committed-graph team model, PR-triage, HTTP MCP) — each needs a deliberate re-decision. Requires fresh security-scan posture |

## Report

Write `graphify-exam-report.md`: verdict line; per-tier tables (check ID,
expected, actual, result); findings with class + evidence + recommended
repair + risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace: failed runs
never touch the prior report; written before any pruning). Then: one run row
appended to `graphify-log.md` (run-row format per
`config-manager-reference.md`); new learnings filed.

## Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items** — Graphify lives in user site-packages and
  external repos; every repair is developer-run or proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch from this exam): anything
  content-changing (`extract`, `update`, `watch`, `install`, `uninstall`,
  `hook install`, `global add/remove`) without developer unlock · the mb-3-cs
  repo itself (no file writes of any kind) · the AGENTS.md block **content**
  (markers verified, content owned elsewhere) · any `mcp.*` entry (never
  added or changed by the exam) · the tracking status of `graphify-out/`
  (standing decision: gitignored; a change re-opens the hooks tripwire) ·
  no API key — never prompt
- Credentials: none configured for this system's code-only posture; a check
  that appears to require a key is itself a DRIFT finding
