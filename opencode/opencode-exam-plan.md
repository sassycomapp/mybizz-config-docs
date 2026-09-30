---
title: "opencode-exam-plan"
doc-id: "mb-21046eca"
---
# OpenCode — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager before
each run from: [[opencode-config|OpenCode Configuration]] (spec), the last [[opencode-exam-report|Exam Report]],
[[opencode-log|Log]] (events since last run), [[opencode-learnings|Learnings]]. Consumed by the
skill at run time; rewritten at the start of the following cycle. The file is live;
its contents are transient.

**This first plan is hand-written** (emulation of the PostgreSQL architecture): it
also serves as the format template. The **standing check inventory lives in the
skill** ([[opencode-skill|Opencode Skill]], born-with-inventory); this plan carries run-specifics
and references. Once verified by a run, future plans carry run-specifics +
references only.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap) |
| Run date | set at execution |
| Prior report | none — placeholder present; missing prior report = expected, not silence |
| Step-0 result | recorded at execution |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request) | (a) any probe whose command text the guards deny; (b) `opencode debug config` **if** guard-denied (sensitive-data class — the resolved config may carry env/value references); (c) the WSL default-distro confirmation if the `wsl.exe` probe is denied; (d) the full-restart-disable (OC3-1) — inherently developer-run and run-with-developer's-schedule, never agent-run |
| Expected-value source of truth | [[opencode-config|OpenCode Configuration]] — read fresh at run start; never rely on remembered values |
| Scope boundary | OpenCode **is the harness this exam runs inside** — the config-manager itself lives under `~/.config/opencode/` (skills, plugin). Self-referential by nature: config-manager self-health is step-0 (register↔skill↔source), never this exam. Cupcake **enforcement** (rules compile + fire) belongs to `mb-config-cupcake`; this exam owns the plugin's **discoverability/dedup mechanics** (exactly one path). GBrain **server** liveness belongs to `mb-config-gbrain`; this exam owns the `mcp.gbrain` **config entry**. The **session database** and its cleanup belong to [[opencode-project-session-data-integrity|Project & Session Data Integrity]] (agent content reads guard-denied — presence-only, via listing). Full skill **inventory** belongs to [[skills-register|Skill Register]] (docs-managed) — this exam checks discovery **mechanics**, never re-audits the inventory |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). Recorded spec states kept under watch
(observations, not findings):

| # | Watch item (spec / doc claims) | This run's action |
|---|---|---|
| W-1 | Version 1.15.12 (verified live 2026-09-09) | Re-read live; if changed, flag spec refresh to governance (an upgrade is not a defect — policy: never on newness) |
| W-2 | Config **merge** semantics (deep merge verified 2026-09-09) | Functional proof attempted via `opencode debug config` (OC2-1); do not re-derive the whole merge experiment |
| W-3 | No native session-start hook; no skill-identity field reaches any plugin (known scope limitations) | Verify the limitations are still **honestly stated and true** — a mechanism's sudden appearance = DRIFT to flag, not to fix |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-09-01 dual-global-config incident (two files, ambiguous precedence) | OC0-2 executes the single-file check (exactly one global config; `.jsonc` only) |
| LG-2 | 2026-09-06/08 plugin changes required full restart (load-once) | Restart procedure presence in reference (knowledge); plugin single-load probe OC2-2; restart itself is Tier 3 / developer-run |
| LG-3 | 2026-09-08 four skill-discovery mechanisms found (plain/symlink/hybrid/two-hop) | Mechanics still resolve (spot evidence via the installed `mb-config-*` skills — step-0 overlaps here harmlessly; full inventory = skill-index) |
| LG-4 | 2026-09-09 deny-list proven live (command text matching `rm -rf *` refused; file survived) | OC2-3 re-verifies the deny patterns are actually **present** in the resolved config (text match, not a fresh firing); do not construct a deny-matching command to re-prove it |
| LG-5 | No crashes/incidents logged since suite build-out | New rows at synthesis time → derive a targeted probe from them |

## 5. Learnings-driven items

| # | Learning | Check |
|---|---|---|
| LE-1 | (seeded: none yet — table is empty at bootstrap) | Carry-forward any entry filed after run #1 into the next plan |

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in [[opencode-skill|Opencode Skill]] (Tiers 0–3). Summary:

- **Tier 0 (A) — invocability:** OC0-1 version 1.15.12 · OC0-2 single global config file (`.jsonc` only) · OC0-3 global `AGENTS.md` present + readable
- **Tier 1 (A/D) — state conformance:** OC1-1 resolved `default_agent` = `plan` · OC1-2 `instructions` pointer resolves · OC1-3 permission posture (edit ask + `**/anvil.yaml` deny; webfetch ask; bash ask + standard deny set; external-directory allow on the three roots; `agent.plan` edit deny) · OC1-4 `mcp.gbrain` entry present · OC1-5 cupcake plugin active at exactly one discoverable path · OC1-6 suite completeness (seven files) · OC1-7 Active Project Standard holds (makepdlf present; mb-3-cs present/retained; mb4ecom/mb5pdlf absent; project-template literal)
- **Tier 2 (A/D) — functional, present ≠ working:** OC2-1 `opencode debug config` executes and returns the resolved merged map · OC2-2 plugin load-once log probe (exactly one "loading plugin" line per real plugin in the latest session) · OC2-3 deny pattern **presence** in resolved config (text match; no fresh firing)
- **Tier 3 (D, locked):** OC3-1 full restart + single-load regression (developer-run, on the developer's schedule — the exam runs inside this harness; a restart interrupts the run itself) · OC3-2 WSL default-distro confirmation (`wsl.exe -l -v` — Windows-side read) · OC3-3 upgrade-policy decision (never on newness; only on check failure)

## 7. Report requirements

The run writes [[opencode-exam-report|Exam Report]]: verdict line; per-tier tables (check ID,
expected, actual, result); findings with class + evidence + recommended repair +
risk; runner attribution for every deferred item (guard-forbidden vs unlock-gated);
overwritten in full each run (write-then-replace; failed runs never touch the prior
report; written before any pruning). Then: one run row appended to [[opencode-log|Log]]
(run-row format per [[config-manager-reference|Reference: Commands, Procedures]]); new learnings filed.

## 8. Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items** — OpenCode is the working harness; every repair is
  developer-run or proposed. The exam never edits its own config, its own skill, or
  the plugin tree.
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): `~/.config/opencode/opencode.jsonc` content
  (agent content reads guard-denied by class; use `opencode debug config` only) · the
  session-data doc (agent content reads denied) · any plugin path (never create,
  move, or remove a discoverable copy) · any restart of the running harness
  (developer-run, on the developer's schedule) · `wsl.exe` without explicit
  `-d Ubuntu -u dev-p` · any command whose text matches a deny pattern, even for
  inspection — the match is incidental? then rephrase; the action is forbidden?
  then stop
- Credentials: variable names only, never printed
