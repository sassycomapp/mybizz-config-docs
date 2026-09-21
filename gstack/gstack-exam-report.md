---
document: "GStack — Exam Report"
doc-id: gstack-exam-report
state: Live
date-created: 2026-09-16
---

# GStack — Exam Report

**Verdict: HEALTHY — all Tier 0–2 checks PASS, zero live defects.** Formal run #1
(emulation, via `config-setup-prompt.md`). No open findings requiring repair; the
released report carries two developer-run items (guard-denied classes) and Tier 3
(watch rows / unlock-gated), all recorded as deferrals below.

## Tier 0 — Invocability (all PASS)

| ID | Runner | Check | Expected | Actual | Result |
|---|---|---|---|---|---|
| GS0-1 | A | Clone version/HEAD | `c7ae632`; VERSION = package.json = `1.58.1.0` | HEAD `c7ae6320`; VERSION `1.58.1.0`; package.json `1.58.1.0` | PASS |
| GS0-2 | A | Discovery topology | per-host tree + both link generations + aggregate present | per-host 54 entries; 53 prefixed links; aggregate `~/.config/opencode/skills/gstack` present; legacy `~/.claude/skills/gstack` present | PASS |
| GS0-3 | A | `GSTACK_BIN` + legacy resolve | `gstack/bin` → `/mnt/c/mybizz/gstack/bin`; `~/.claude/skills/gstack` → clone | both symlinks resolve into the clone | PASS |

## Tier 1 — State conformance (all PASS)

| ID | Runner | Check | Expected | Actual | Result |
|---|---|---|---|---|---|
| GS1-1 | A | Per-host skill tree | 54 entries (53 `gstack-*` + aggregate) | 54 | PASS |
| GS1-2 | A | Binary tree | 74 scripts | 74 | PASS |
| GS1-3 | A | Broken discovery entries | 3 dead (retired `/mnt/c/mybizz/skills/`) | all 3 dead | PASS |
| GS1-4 | A | `~/.gstack/config.yaml` live values | `artifacts_sync_mode: full` · `telemetry: community` · `question_tuning: true` · `user_slug_at_local: dev-p` | all four exact | PASS |
| GS1-5 | A | gbrain-detection.json + repo-policy.json | detection: postgres, doctor ok, mcp none, sync full, remote `""`; 8 repos read-write sassycomapp | all exact (see note N-1 for version field format) | PASS |
| GS1-6 | A | GBrain worktree + remote | worktree exists, git-backed, `.brain-allowlist`/`.brain-privacy-map.json`/analytics/sessions; remote file **absent** | present; remote absent | PASS |
| GS1-7 | A | `~/.gstack/last-update-check` | `UPGRADE_AVAILABLE 1.58.1.0 1.61.0.0` (stale = documented) | exact string | PASS |
| GS1-8 | A/D | `.env` absence; `.env.example` content | `.env` absent; one template line | `.env` absent (clone listing); `.env.example` content = **D** (guard-denied) | PASS (partial → see D-1) |
| GS1-9 | A | Generation discipline: `SKILL.md.tmpl` + `gen:skill-docs` + slop config | all present, values match | tmpl present; `gen:skill-docs` ×2 in package.json; slop config `{"ignores":["**/vendor/**"]}` | PASS |
| GS1-10 | A | Suite completeness (7 files + skill source) | all present | 8/8 | PASS |

**N-1 (note, not a defect):** `gbrain-detection.json` stores the version as `"gbrain0.46.1.0"` (no space after `gbrain`); the spec writes `gbrain 0.46.1.0`. Cosmetic field-format variance in the JSON record; records the same value. Flagged to docs governance as a possible spec rendering nit — not a live-state mismatch.

## Tier 2 — Functional proof (present ≠ working; all PASS)

| ID | Runner | Check | Expected | Actual | Result |
|---|---|---|---|---|---|
| GS2-1 | A | Deterministic bin invocation | script executes, exit 0 | `gstack-gbrain-detect` (also `gstack-brain-sync --status`) both EXIT 0 with valid JSON/`{"status":"idle","queue_depth":0}` | PASS |
| GS2-2 | A | Generation discipline probe — frontmatter `name:` matches command convention | `gstack-qa` → `name: qa`; aggregate → `name: gstack`; exception → `name: gstack-upgrade` | all three exact | PASS |

## Tier 3 — Deep pass (unlock-gated; EXECUTED 2026-09-16 per developer unlock)

| ID | Runner | Check | Expected | Actual | Result |
|---|---|---|---|---|---|
| GS3-1 | D | Full functional lifecycle: agent-visible invocation of a real GStack skill in a live session (plan→review flow or one browser/QA skill) | Skill runs to completion per its documented exit condition | Two real skills invoked in-session from the installed per-host tree: `/plan-ceo-review` and `/review` — both loaded full instructions through the discovery symlinks and executed their documented workflows; run-time preamble binaries (`gstack-update-check`, [[gstack-config|GStack Configuration]], `gstack-slug`) resolved via the OpenCode-host root `~/.config/opencode/skills/gstack/bin` and each exited 0. `/review` reached its documented base-branch stop condition ("Nothing to review — on base branch"). Nuance: the auto-generated SKILL.md preamble hardcodes the OpenClaw/Claude host root (`~/.openclaw/...` — absent here), degrading to `|| true`; this host's correct runtime root is OpenCode's aggregate bin, per the global AGENTS.md GStack-binary-path rule — a documented host variance, not a defect | PASS (with nuance noted as N-2) |
| GS3-2 | D | Upgrade execution (`1.58.1.0` → newer) | developer decision; never on newness, only on check failure | **STAY on `1.58.1.0`** — zero check failures this run; policy forbids upgrading on newness. Upgrade remains open W-1 (developer-owned re-decision, `1.81.0.0` Aside-first is a behavior change) | PASS (policy applied — no upgrade) |

**N-2 (note, not a defect):** generated SKILL.md preambles default their runtime-path detection to `~/.openclaw/skills/gstack/bin` / `~/.claude/skills/gstack/bin`. On this OpenCode host that path is absent (`~/.claude/...` symlink exists and resolves into the clone, but the global AGENTS.md explicitly prefers `~/.config/opencode/skills/gstack/bin`). Preamble code already protects itself with `|| true` fallbacks, so skills run — but the path detection does not resolve to the OpenCode host root at skill-load time. Flagged to docs governance as a candidate addition to `gstack-reference.md` (§bin-tree note): pair with LE-1's mixed-interpreter note.

**N-3 (resolved — developer correction applied):** [[gstack-config|GStack Configuration]] §Integration facts stated GStack is "one of the six closely-related memory-system components in [[memory-master-explainer|Master Explainer]]." The current master explainer (checked live 2026-09-16) lists **no GStack row** — its family is GBrain, Dream Cycle, Memory Governor, mb-submit-memory, Graphify, PostgreSQL, Cupcake — and GStack is the workflow layer, not a memory mechanism. **Developer correction 2026-09-16:** GStack is **not** a memory-family member; it is related only through its close relation to GBrain. Spec row corrected in this run to match; no [[memory-master-explainer|Master Explainer]] edit made (GStack was never a listed member there).

## Watch rows (observations carried forward to next plan)

- W-1 upgrade decision (`1.81.0.0` Aside-first) — remains an open re-decision, never a routine bump. Confirmed standing this run (GS3-2).

## Learnings filed

- LE-1 (→ graduate to [[gstack-reference|GStack Reference]] on acceptance): the `bin/` tree is **mixed-interpreter** — most scripts are bash, but `gstack-gbrain-detect` (and likely other gbrain-facing diagnostics) were rewritten to TypeScript/Bun (shebang `#!/usr/bin/env -S bun run`). Invocation must follow the individual script's shebang; `bash <name` on a Bun script yields confusing multi-line errors (observed; the script comment documents the rewrite). Reference documents `bash .../gstack-brain-sync` — verified still bash, correct.

## Gate protocol

- Findings: none requiring repair. All remediation proposed = deferred (Tier 3) or developer-run (D-1).
- No agent-healable items — GStack is verified working; the module changes nothing.
- Tier 3 unlock decision asked at the gate, never assumed.
- Spec-doc corrections: N-1 rendered to docs governance as a candidate wording nit.
