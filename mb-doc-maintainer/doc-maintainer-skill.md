---
title: "doc-maintainer-skill"
doc-id: "doc-maintainer-skill"
---
# mb-config-doc-maintainer — Exam Skill

Exams the `mb-doc-maintainer` system's configuration state against its spec.
This skill holds the **procedure** only — expected values live in the spec doc
and are read fresh at the start of every run. The maintainer is working well;
this exam verifies that and repairs nothing.

- Spec: [[doc-maintainer-config|Configuration]] — read it first, every run
- **Exam plan: [[doc-maintainer-exam-plan|Exam Plan]] — read second, every
  run.** The plan-driven cycle: the config-manager synthesizes this plan fresh
  before each run (spec + last report + log + learnings) and this skill
  executes it in hand. Run-specifics and deltas live in the plan; the
  **standing check inventory lives in this skill** (below) — permanent
  occurrences graduate here, never into plans
- Reference: [[doc-maintainer-reference|Reference]] — invocation, tool syntax,
  watcher management, formats
- Explainer: [[doc-maintainer-explainer|Explainer]] — the whole-system narrative
- Report: [[doc-maintainer-exam-report|Exam Report]] — one file, overwritten
  each run (write-then-replace)
- Log: [[doc-maintainer-log|Log]] — one run row per exam; free rows for
  notable events witnessed between runs
- Learnings: [[doc-maintainer-learnings|Learnings]] — transient; delete
  entries once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **the maintainer system itself**: watcher liveness and
  task settings, event-queue mechanics, tool integrity and test suite, the
  installed skill's identity, run-log discipline, and the GBrain source row's
  recorded state.
- **Parent GBrain conformance** (binary version, models, config file, schema
  pack, MCP entry, sync machinery) belongs to `mb-config-gbrain` — cross-
  reference its current report; the one permitted overlap is the source row's
  existence/federated-state/lag reading (DM1-6), never re-probed further.
- **Database-level checks** belong to `mb-config-postgresql`.
- **Corpus documentation governance** (register membership as a policy,
  corpus-wide register audits, wikilink content) belongs to the
  documentation-management side; this exam verifies registration **mechanics
  only** (does the recorded row exist) — never audits corpus content.
- **The contract's content** (`gbrain/gbrain-doc-contract.md`) is governance —
  the exam verifies its existence, frontmatter, and register row as artifacts;
  its requirements are never re-derived, re-interpreted, or edited here.

## Credential discipline (hard rule)

This system holds no credentials of its own. Any credential encountered
incidentally (env vars, other systems' configs) is referenced **by variable
name only** — never printed, logged, or copied into reports, outputs, or
learnings.

## Hard behavioral rules (from the suite's own Do-not list)

- Expected values are read fresh from the spec every run — never from memory.
- Never expand a check into a corpus-wide investigation — the maintainer's own
  core principle applies to its exam.
- Never treat a queued-but-undrained event as a defect — event accumulation is
  the designed behavior between invocations; only malformed events are findings.
- Never run `gbrain sync` from the exam (content-changing; the sync machinery
  is the parent module's surface) — the source row's recorded lag/coverage is
  read from `sources status` only.
- Never execute the maintainer's drain during detection — content-changing;
  a Tier 3 unlock decision only.
- Never create an `anvil.yaml` fixture for the exclusion test — policy-forbidden;
  DM3-2 is developer-run by design.
- Never edit the subject `SKILL.md`, the contract, or any spec doc — governance
  flags only.
- **Never probe `--phase`-style flags bare on any live system** — the run #1
  Dream Cycle lesson generalizes: only parse-safe forms, capture to a file,
  never pipe live output to a truncating consumer.
- **Never rely on `Stop-ScheduledTask` alone to release the watcher's
  single-instance mutex** — the cmd wrapper's PowerShell child survives the
  task stop and keeps holding the mutex (confirmed live 2026-09-25, DM3-2d);
  kill the orphaned process explicitly before any restart.

## Tier 0 — Invocability (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| DM0-1 | A | Scheduled task state: `Get-ScheduledTask -TaskName "mb-doc-maintainer-save-watcher"` | State `Running` (config §Watcher — always-on; developer decision 2026-09-25). `Ready`/absent = DOWN — the watcher is the system's event source; without it saves go unobserved |
| DM0-2 | A | Watcher process live: `Win32_Process` where CommandLine matches `save-watcher.ps1` | Exactly one process present (mutex single-instance, config §Watcher). Two or more = UNHEALTHY; zero with task `Running` = UNHEALTHY |
| DM0-3 | A | Queue dir and run-log exist at their recorded paths (config §Storage) | Both present. Queue absent = DOWN (event loss); run-log absent = GAP |

## Tier 1 — State conformance (each probe vs the spec's current expected value; mismatch = DRIFT)

| ID | Runner | Check | Expected |
|---|---|---|---|
| DM1-1 | A | Source repo: `git -C C:\mybizz\mb-doc-maintainer remote -v` + `log --oneline -1` + `status --short` | Origin = `https://github.com/sassycomapp/mb-doc-maintainer.git`; HEAD `9dae0db` (root commit); tree clean (config §Identity). Untracked debris = finding |
| DM1-2 | A | Hash pair: installed subject skill `~/.config/opencode/skills/mb-doc-maintainer/SKILL.md` vs source `mb-doc-maintainer-skill.md` (sha256 first 16 hex) | Byte-identical (config §Identity — installed skill). Installed-edited → DRIFT; source-edited-not-reinstalled → stale GAP |
| DM1-3 | A | Tools compile (`python3 -m py_compile` × 3) and the test suite passes (`python3 -m unittest discover -s tests`) | All compile; 40/40 pass (config §Component layout) |
| DM1-4 | A | Scheduled-task settings via `Get-ScheduledTask | Select -Expand Settings/Triggers` | AtLogOn trigger; ExecutionTimeLimit 0; RestartCount 3 / 1-min interval; battery-safe flags (config §Watcher). Any divergence = DRIFT |
| DM1-5 | A | Run-log state: exists, frontmatter two-field compliant (tool check), row present in the config-docs register (`doc-maintainer-run-log`, Live) | All three (config §Storage + §Register usage) |
| DM1-6 | A | GBrain source row: `gbrain sources status mb-doc-maintainer` | Registered, federated no, lag ≈ 0 s, 100% embed coverage, 1 page (config §GBrain integration). Permitted overlap with the parent module |
| DM1-7 | A | Suite completeness: 8 files in `mb-doc-maintainer/` — config, exam-plan, exam-report, log, learnings, explainer, reference, skill source | All present; missing file = GAP |
| DM1-8 | A | Contract artifact: exists at `C:\mybizz\mybizz-config-docs\gbrain\gbrain-doc-contract.md`; frontmatter two-field compliant (tool check); register row in config-docs register | All three (config §Identity — governing contract) |
| DM1-9 | A | Register rows for the three suite docs (config/reference/explainer) in the config-docs register | Rows present. Known absent at build (spec open item #1) → anticipated GAP finding; the maintainer's own next creation-event run is the designed closer |
| DM1-10 | A | Queue well-formedness: every `*.json` in the queue parses and carries `path` + `kind` | Every event well-formed; empty queue also passes (designed state) |

## Tier 2 — Functional proof (present ≠ working; read-only probes only — no drain, no mutation)

| ID | Runner | Check | Expected |
|---|---|---|---|
| DM2-1 | A | Tool execution probe: `frontmatter.py check` on the contract file (or any known-compliant doc) | Exit 0, `ok: true` — the tool executes for real, not merely present |
| DM2-2 | A | Watcher functional proof: queue events (if any) are well-formed and none reference the run-log or `watcher.log` paths | No self-events — the watcher's own exclusion works (config §Watcher exclusions) |
| DM2-3 | A | Discipline probe: `register.py check` on the config-docs register — exit 0, no findings | Schema valid — proves the register tool executes read-only against a real register |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier. Not skimped: every sub-check executes, evidence captured to files, per-event walkthroughs — a summary verdict without per-event evidence is a failed Tier 3)

| ID | Runner | Check | Expected |
|---|---|---|---|
| DM3-1a | D | **Pre-state capture, per queued event:** event JSON copied to the exam evidence folder; for the affected document — frontmatter tool check output, links.py scan output, register row state (grep), file bytes hash — all captured BEFORE any maintenance action | Pre-state recorded for every event; a missing pre-state row invalidates the sub-check (no pre-state, no heal discipline applies to the exam too) |
| DM3-1b | D | **Per-event walkthrough, one at a time:** each event processed individually through the full SKILL.md §11 loop — tool checks run live, repairs applied where the automation boundary allows, §9 summary emitted per event | Every event gets its own walkthrough: per-event tool evidence + the standard summary block. No batch processing, no per-event summary = fail |
| DM3-1c | D | **§20 definition-of-done checklist per event, item by item** (not rubber-stamped): affected docs satisfy applicable requirements · frontmatter exactly two-field · affected links resolve · applicable references are wikilinks · register current · safe mechanical problems repaired automatically · genuine ambiguity surfaced · concise summary · detail on request · zero corpus-wide work | Every checklist item individually verified with evidence; an item marked pass without evidence fails the tier |
| DM3-1d | D | **Register four-event discipline under live load:** creation adds its row; rename updates doc-id/title in place; deletion sets `state: Retired` (row survives); content edits leave the register byte-identical | Register diff/byte-compare before vs after: only the rows the four-event model permits changed; any other register change = UNHEALTHY |
| DM3-1e | D | **Run-log append-only proof:** byte-compare the run-log before vs after | Only appended lines added; no existing row altered or removed; one correct-format line per event |
| DM3-1f | D | **Queue drain verification:** event files removed; no event processed twice; no phantom events created by the run itself | Queue empty (or only events that arrived during the run); run-log carries no duplicates |
| DM3-1g | D | **Termination discipline:** the invocation ends — no follow-up work items created, "can wait" findings reported not queued, no rescans | Post-drain queue empty; no new work queues created; findings classified and reported only |
| DM3-2a | D | **Watcher exclusion suite, live fixtures** (developer builds the fixture tree — the agent cannot create `anvil.yaml`): in-scope `.md` (expect event) · WIP folder (none) · `temp-*` folder (none) · `tmp-` prefixed file (none) · dotfolder (none) · `.git` folder (none) · zero-content `.md` (none) · non-`.md` file (none) · folder containing `anvil.yaml` (none — O3/D6 class rule, the code-inspection-only path finally live-tested) | Exactly one event for the in-scope file; every excluded class silent. Any event from an excluded class = UNHEALTHY |
| DM3-2b | D | **Coalescing under load:** ≥5 rapid saves of one file inside the debounce window | Exactly one event, kind correct (creation or modification per final state) |
| DM3-2c | D | **Lifecycle churn:** create → rename → rename back → delete within one debounce window | Final state classifies correctly (deletion or nothing) — no phantom events for intermediate states |
| DM3-2d | D | **Crash-restart resilience:** kill the watcher process mid-run; verify scheduled-task restart (or manual restart) and that the abandoned mutex does not block it; confirm exactly one instance afterwards | Watcher running again within the restart window; single instance; events queued during the gap are not lost (queue files persist) |
| DM3-2e | D | **Scope authority is read live:** add a temporary exception to the scope authority, restart the watcher, save in the excepted path (no event), revert | Scope change honored at start (D6) — the watcher carries no scope list of its own |

## Report

Write [[doc-maintainer-exam-report|Exam Report]]: verdict line; per-tier tables
(check ID, expected, actual, result); findings with class + evidence +
recommended repair + risk; runner attribution for every deferred item
(guard-forbidden vs unlock-gated). Overwritten in full each run
(write-then-replace; failed runs never touch the prior report; written before
any pruning). Then: one run row appended to [[doc-maintainer-log|Log]]; new
learnings filed in [[doc-maintainer-learnings|Learnings]].

## Gate protocol

- Findings → classify (`DOWN`/`UNHEALTHY`/`DRIFT`/`GAP`) → present with
  evidence + recommended repair + risk
- **Agent-healable items: none by default** — this system's artifacts are
  governed documents and a runtime install; repairs are developer-run or
  proposed, except suite-file repairs (the one agent-healable class per the
  config-manager standard: exam-suite file repairs in `mb-doc-maintainer/`)
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the subject `SKILL.md` and its source ·
  `gbrain-doc-contract.md` · `anvil.yaml` (never created, read, or touched) ·
  env credentials (name only) · any `gbrain sync` execution · the watcher's
  scheduled task (mutation only via developer gate) · `~/.gbrain/config.json`
  and all credential values
- Grants: `mg-grant --path <folder> --count N` per the developer's standing
  session instruction (batched; 1 slip per write)