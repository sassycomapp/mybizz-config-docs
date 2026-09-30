---
title: "opencode-skill"
doc-id: "mb-c861757a"
---
# mb-config-opencode — Exam Skill

Exams OpenCode's configuration state against its spec. This skill holds the
**procedure** only — expected values live in the spec doc and are read fresh at
the start of every run. OpenCode is working well; this exam verifies that and
repairs nothing.

- Spec: [[opencode-config|OpenCode Configuration]] — read it first, every run
- **Exam plan: [[opencode-exam-plan|Exam Plan]] — read second, every run.**
  The plan-driven cycle: the config-manager synthesizes this plan fresh before
  each run (from spec + last report + log + learnings) and this skill executes it
  in hand. The plan carries run-specifics and deltas; the **standing check
  inventory lives in this skill** (below) — permanent occurrences graduate here,
  never into plans
- Reference: [[opencode-reference|Commands, Verification, Troubleshooting]] — restart, verification,
  troubleshooting, deny-list behavior
- Report: [[opencode-exam-report|Exam Report]] — one file, overwritten each run
  (write-then-replace)
- Log: [[opencode-log|Log]] — one run row per exam; free rows for notable
  events witnessed between runs
- Learnings: [[opencode-learnings|Learnings]] — file new patterns/nuances; delete
  entries once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **the harness itself**: version, global-config consolidation,
  merge semantics, permission posture, plugin discoverability, MCP config entry,
  and the Active Project Standard.
- **Cupcake enforcement** (rules compile + firing) belongs to `mb-config-cupcake`
  — this exam owns the plugin's **discoverability/dedup mechanics** (exactly one
  discoverable path), never its policy behavior.
- **GBrain server liveness** belongs to `mb-config-gbrain` — this exam owns the
  `mcp.gbrain` **config entry only** (present, local server), never server state.
- **Session database** and its cleanup belong to
  [[opencode-project-session-data-integrity|Project & Session Data Integrity]] — agent content reads are
  guard-denied; this exam checks presence only (directory listing), never content.
- **Full skill inventory** belongs to [[skills-register|Skill Register]] (docs-managed) — this exam
  checks discovery **mechanics** (that the documented real install methods still
  resolve for the installed `mb-config-*` set), never re-audits the inventory.
- **PostgreSQL/data-model state** belongs to `mb-config-postgresql` — OpenCode's
  own session DB is local app data, not a managed PG instance.

## Credential discipline (hard rule)

The only credential surface is `mcp.gbrain`'s environment-passed API keys passing
through OpenCode's resolved config. Reference them **by variable name only** —
never print, log, or copy values into reports, outputs, or learnings. When
running `opencode debug config`, **select only the needed fields**; never dump a
raw resolved config (or its environment sections) into any report or output, and
**delete any captured resolved-config file at once** — the capture itself carries
the sensitive sections. Field extraction from the capture is **guard-denied by
class**: treat it as developer-run (runner D). If a guard denies a probe, it
becomes a developer-run request — honored absolutely, never retried through an
alternate path.

## Hard behavioral rules (from the suite's own Do-not list)

- Never edit a plugin's code and expect it to take effect without a **full
  process restart** — changes are read only at process start; no reload exists.
- Never create a second discoverable path for any plugin — even a symlink to the
  identical file causes double-loading (the proven Cupcake double-decrement
  incident).
- Never create a **WSL-side** symlink pointing at a Windows-drive target —
  confirmed unreadable by Windows Explorer; create from the Windows side with
  `mklink /D` (Developer Mode required).
- Never invoke `wsl.exe` from a Windows-triggered command without explicit
  `-d Ubuntu -u dev-p` — two distros exist; the working one is not the default.
- Never treat a "Paused" project's existing config as stale — only "Never
  started" projects default to zero configuration.
- Never assume project config replaces global config — they **merge**; project
  wins only on conflicting keys (verified 2026-09-09).
- Never construct a command whose text matches a deny pattern, even to "prove"
  the deny is live — a match refuses before execution (text-matching behavior,
  verified live 2026-09-09). The intact deny-list is verified by **presence** in
  the resolved config, not by a fresh firing. **This includes argument literals:**
  the exec-protection guard matches the `cupcake` token even inside a grep/sed
  search argument (run #1, 2026-09-15) — write no token into any command text,
  including read-only inspection args; use path/token-free glob forms instead.
- Never read `~/.config/opencode/opencode.jsonc` or
  [[opencode-project-session-data-integrity|Project & Session Data Integrity]] raw — sensitive-data guard class;
  use `opencode debug config` for resolved state, presence checks for files.

## Run #1 lessons graduated (2026-09-15)

- **Config-content field extraction is permanently developer-run.** The
  executable config command (`opencode debug config`) runs fine, but extracting
  fields from its capture is guard-denied (sensitive-data class — the resolved
  config carries `mcp.gbrain` env sections). The probe's PASS is execution-only;
  field values come from the developer bundle. Never retain a captured resolved
  config. Hence OC1-2, OC1-4…10, OC2-3, OC1-11 are runner **D** (below).
- **The exec-protection guard matches tokens inside argument literals, not just
  paths** — a read-only grep for a token-named string is refused. No token in
  any command text; glob/path-free forms only (the hard rule above was extended).

## Tier 0 — Invocability (run first; non-execution = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| OC0-1 | A | `opencode --version` executes and reports | `1.15.12` (config §Identity — version, verified live 2026-09-09). Non-execution = DOWN. A version **drift** from spec = DRIFT finding (upgrade observation, never auto-accepted; policy: never on newness) |
| OC0-2 | A | Global config single source: `~/.config/opencode/opencode.jsonc` exists; no `opencode.json` sibling at the global level | `.jsonc` only (config §Identity — "the only global config file"; consolidated 2026-09-01). A second global file = DRIFT (the 2026-09-01 incident class) |
| OC0-3 | A | Global AGENTS.md present and readable: `~/.config/opencode/AGENTS.md` | Present, non-trivial (~14.4 KB — config §The global AGENTS.md). Missing = DRIFT |

## Tier 1 — State conformance (each probe vs the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| OC1-1 | A | Resolved-config inspection runs: `opencode debug config` (from any project root) exits 0, output non-empty | Runs and prints the merged map (reference §RESOLVED configuration; verified live 2026-09-09). Output captures the config layer's own machinery working |
| OC1-2 | D | `default_agent` from resolved config (field extraction — sensitive-data guard class; agent-denied) | `plan` (config §Global config). Extract selected keys only — never the full dump |
| OC1-3 | A | `instructions` pointer resolves: `C:/dev/project-library-global/register-global/register-global.md` exists (WSL: `/mnt/c/dev/project-library-global/register-global/register-global.md`) | File exists (config §Global config; corrected 2026-09-01 from four deleted INDEX files). Missing = DRIFT |
| OC1-4 | D | `permission.edit` (field extraction — sensitive-data guard class) | `ask` by default; `**/anvil.yaml` explicitly `deny` (config §Global config) |
| OC1-5 | D | `permission.webfetch` (field extraction — sensitive-data guard class) | `ask` (config §Global config) |
| OC1-6 | D | `permission.bash` (field extraction — sensitive-data guard class) | `ask` by default; explicit `deny` on destructive git, `DROP`/`TRUNCATE` SQL patterns, `curl`/`wget` piped to a shell (config §Global config) |
| OC1-7 | D | `permission.task` (field extraction — sensitive-data guard class) | `deny` (config §Global config — Layer 1 of the three-layer task-denial) |
| OC1-8 | D | `permission.external_directory` (field extraction — sensitive-data guard class) | `allow` for `C:\mybizz\**`, `C:\dev\**`, `C:\pdlf\**` (config §Global config) |
| OC1-9 | D | `agent.plan.permission.edit` (field extraction — sensitive-data guard class) | `deny` (config §Global config — Plan cannot write, by design) |
| OC1-10 | D | `mcp.gbrain` entry present, local server (field extraction — sensitive-data guard class) | Present — local MCP server, `gbrain serve`, keys env-passed (config §Global config; entry-only — server liveness belongs to `mb-config-gbrain`). Never print environment sections |
| OC1-11 | D | `opencode.jsonc` content key-by-key vs config §Global config table (raw content read — sensitive-data guard class; agent-denied) | Exact match (permission-model doc verified 2026-09-09). Guard denial → developer bundle |
| OC1-12 | A | Plugin state: `cupcake.js` discoverable from **exactly one** path (plugin dir listing) | Active, exactly one discoverable copy (config §Plugin state; dedup by discovery path) |
| OC1-13 | A | Suite completeness: the seven suite files in `opencode/` | All present (config, exam-plan, exam-report, log, learnings, explainer, reference — missing = GAP; skill source + the two sister scope docs extra, not required by the 7-file standard) |
| OC1-14 | A | Active Project Standard: per-project config states per config §Active Project Standard | `makepdlf-project-library` — present (Active); `mb-3-cs` — present, retained (Paused); `mb4ecom`/`mb5pdlf` — **absent** (scaffolding-only, correct); `project-template` — literal `{SLUG}` placeholders (template, not a project). A Paused config misread as stale, or a scaffolding project gaining config, = DRIFT |
| OC1-15 | A | Known scope limitations veracity | No native session-start hook · no skill-identity field reaches any plugin · plugin dedup by discovery path (config §Known scope limitations). If any limitation is found silently "fixed" without governance → DRIFT flag, never a silent acceptance |

## Tier 2 — Functional proof (present ≠ working; read-only execution probes — nothing content-changing)

| ID | Runner | Check | Expected |
|---|---|---|---|
| OC2-1 | A | Functional resolve probe: `opencode debug config` from a project root, exit 0, output contains `default_agent` | Runs to completion and returns the resolved map — the merge machinery works, not merely that the file exists (reference §RESOLVED; the deep-merge proof was live-verified 2026-09-09). Empty/failure = UNHEALTHY |
| OC2-2 | A | Plugin loaded exactly once: `grep -ia 'loading plugin' ~/.local/share/opencode/log/*.log | tail -5` — exactly one line per real plugin file in the latest session's timestamp block | Exactly one line per plugin (reference §Confirming a plugin is loaded exactly once). Two lines for cupcake.js in one session = double-discovery DRIFT (the proven double-decrement class). Guard denial on log read → developer bundle |
| OC2-3 | D | Deny-list live posture: deny patterns present in the resolved config (text match, no construct/fire — field extraction is sensitive-data guard class) | Present — the `ask` default + deny patterns survive merge (config §Global config; reference §deny-list is live). Absence = DRIFT. **Never build a deny-matching command to re-prove** |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| OC3-1 | D | Full restart + plugin single-load regression: restart per reference §Restarting (`pkill -f "opencode web"` + relaunch), then re-run the OC2-2 log probe | Loads exactly once post-restart. **Disruptive — this exam runs inside the harness; a restart interrupts the run itself** → developer-run, on the developer's schedule |
| OC3-2 | D | WSL default-distro confirmation: `wsl.exe -l -v` (Windows-triggered read) | Default distro = `Ubuntu-22.04` (stopped); working env = `Ubuntu`; real commands use `-d Ubuntu -u dev-p` (config §Identity) |
| OC3-3 | D | Upgrade decision (only if OC0-1 observed version drift) | Policy: **never on newness — only on check failure**. A drifted version with no failed check → stay; flag spec refresh. The upgrade decision is the developer's |

## Report

Write [[opencode-exam-report|Exam Report]]: verdict line; per-tier tables (check ID,
expected, actual, result); findings with class + evidence + recommended repair +
risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace: failed runs
never touch the prior report; written before any pruning). Then: one run row
appended to [[opencode-log|Log]] (run-row format per [[config-manager-reference|Reference: Commands, Procedures]]);
new learnings filed.

## Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items** — OpenCode is the working harness; the exam never
  edits its own config, its own skill, or the plugin tree. Every repair is
  developer-run or proposed.
- Spec-doc corrections → flagged to docs governance, never applied here (e.g. a
  version drift, or the [[opencode-config|OpenCode Configuration]] five-part suite table if the suite
  set changes).
- Deny-list (never heal, never touch): `~/.config/opencode/opencode.jsonc`
  content (sensitive-data class — agent never reads) · the session-data doc
  content (proven denial) · any plugin path (never create, move, or remove a
  discoverable copy) · the running process (never restart — OC3-1 is
  developer-run) · `wsl.exe` without explicit `-d Ubuntu -u dev-p` · any
  command text matching a deny pattern (even for inspection — rephrase only when
  the match is incidental; stop when the action itself is forbidden)
- Credentials: variable names only, never printed
