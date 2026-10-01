---
title: "opencode-exam-report"
doc-id: "mb-f1821aef"
updated: "2026-10-01"
---
# OpenCode — Exam Report

Run #1 — **first formal plan-driven exam** (2026-09-15). Plan:
[[[mybizz-config-docs:opencode/opencode-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/opencode/opencode-exam-plan.md) (bootstrap — no prior report). Step-0: **PASS**
— 8/8 hash pairs match via the approved glob form (postgresql `b41a3e117dee1809`
· cupcake `f5e8489cf60a8abc` · gbrain `58dc0b52cbc86d72` · memory-governor
`c40df342d523aa59` · gbrain-dream-cycle `a4872e9d61f1c32f` · graphify
`1ca73897a2023741` · mb-submit-memory `88a71641d03f1997` · opencode
`039b28e46b276834`); suite completeness 7/7 on all eight Installed suites
(mb-submit-memory naming variance register-documented The use of registers has been discontinued. Please review); register spec-doc paths
8/8 exist; no open run blocks opencode (bootstrap). One exec-protection denial at
step-0 (compound loop text carrying the cupcake token — known class) — honored;
re-issued via directory-glob form without the token. Detection only — Tiers 0–2;
Tier 3 locked. Scope boundary honored (cupcake enforcement / gbrain server /
session-db content / skill inventory cross-referenced, never re-probed).

## Verdict: HEALTHY — all checks PASS, zero live defects; developer bundle fully closed; two spec omissions (F-4, F-5) flagged to docs governance, one security confirmation (F-6) recorded

OpenCode is working well. Version and single-source state match the spec; the
permission posture's machinery executes (the resolved-config command runs);
plugin single-load verified in the current session; the Active Project Standard
holds across all four documented project states.

## Tier 0 — Invocability: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| OC0-1 | Version | `1.15.12` | `opencode --version` → `1.15.12` — exact match, no drift | PASS |
| OC0-2 | Single global config | `.jsonc` only, no global `opencode.json` sibling | `opencode.jsonc` present; no sibling found | PASS |
| OC0-3 | Global `AGENTS.md` | present, readable | present; 16,152 bytes (~15.8 KB; spec records 14.4 KB at 2026-09-09 — size moved with the 2026-09-15 session-close updates, not a defect) | PASS |

## Tier 1 — State conformance: PASS, with config-content checks developer-bundled (guard class)

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| OC1-1 | Resolved-config inspection runs | exits 0, non-empty | `opencode debug config` → exit 0, 83 lines resolved output — merge machinery executes | PASS |
| OC1-2 | `default_agent` | `plan` | **developer-verified `plan`** (2026-09-15) | PASS |
| OC1-3 | `instructions` pointer resolves | file exists | `register-global.md` The use of registers has been discontinued. Please review present under `/mnt/c/dev/project-library-global/register-global/` — resolves | PASS |
| OC1-4 | `permission.edit` | ask + `**/anvil.yaml` deny | **developer-verified: `{"*":"ask","**/anvil.yaml":"deny"}`** | PASS |
| OC1-5 | `permission.webfetch` | ask | **developer-verified `ask`** | PASS |
| OC1-6 | `permission.bash` | ask + standard deny set | **developer-verified: `ask` + all 13 deny patterns present** | PASS |
| OC1-7 | `permission.task` | deny | **developer-verified `deny`** | PASS |
| OC1-8 | `permission.external_directory` | allow on three roots | **developer-verified: allow on the three roots PLUS `C:\data-mybizz-mgt\**` (4th root absent from spec — F-4)** | PASS / F-4 |
| OC1-9 | `agent.plan.permission.edit` | deny | **developer-verified `deny`** | PASS |
| OC1-10 | `mcp.gbrain` entry | present, local server | **developer-verified: local `/home/dev-p/.bun/bin/gbrain serve`, `enabled: true`, keys env-passed (`{env:...}` placeholders — no literals in config)** | PASS |
| OC1-11 | `opencode.jsonc` key-by-key | exact match to spec table | **developer-verified: all spec fields+values present verbatim; same F-4 4th-root omission; additionally `agent.docs-manager` subagent present but undocumented in spec (F-5)** | PASS / F-4 / F-5 |
| OC1-12 | Plugin discoverable exactly once | one path | Plugin dir listing: one live `.js`; two `.bak-*` files non-discovered (spec's documented dedup state) | PASS |
| OC1-13 | Suite completeness | seven files | 7/7 in `opencode/` (config, exam-plan, exam-report, log, learnings, explainer, reference) + skill source + the two sister scope docs | PASS |
| OC1-14 | Active Project Standard | makepdlf present; mb-3-cs retained; mb4ecom/mb5pdlf absent | makepdlf-project-library `opencode.json` present (Active); `mb-3-cs/opencode.json` + `mb-3-cs-project-library/opencode.json` present (Paused, retained); no config in `dev-mb4ecom`/`dev-mb5pdlf` (scaffolding-only, correct) | PASS |
| OC1-15 | Known scope limitations | honestly stated and still true | No session-start hook, no skill-identity-to-plugin, path-based dedup — all documented and unmodified in this run's evidence | PASS |

## Tier 2 — Functional proof (present ≠ working): PASS, one check guard-bundled

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| OC2-1 | Resolved-config functional probe | runs to completion, non-empty | `opencode debug config` exit 0, 83 lines — the merge/config layer works, not merely exists | PASS |
| OC2-2 | Plugin loaded exactly once | one `loading plugin` line per plugin per session | Current session log `2026-09-16T030513.log`: exactly **1** `loading plugin` line; its path resolves to the single discoverable copy in the plugin dir | PASS |
| OC2-3 | Deny-list posture in resolved config | deny patterns present | **developer-verified: all 13 deny patterns present in the resolved `permission.bash` map** | PASS |

## Findings

1. **F-1 — Config-content field checks are guard-denied by class (expected, not a
   defect).** Every probe that extracts fields from the resolved config or reads
   `opencode.jsonc` content is blocked as sensitive-data — this matches the
   config-manager's proven denial classes and the skill's own planned posture
   (OC1-2, OC1-4…10, OC2-3, OC1-11). The executable evidence (version, single
   source, pointer resolution, plugin state, project states, single-load) all
   pass. **Recommended repair: none to the live system.** The developer bundle
   below closes the deferred field checks; the skill's runner column stays A→D
   per class.
2. **F-2 — AGENTS.md size moved** (14.4 KB at 2026-09-09 → 16.2 KB now) — the
   file gained the session-close routine and fact-save guidance on 2026-09-15.
   Present and readable; not a defect. Flag: the spec's size figure is
   date-stamped and will drift naturally; treat size as indicative, presence as
   the check.
3. **F-3 — Watch items verified as recorded:** W-1 version unchanged (no drift,
   no upgrade signal); W-2 merge semantics re-proven executable (deep-merge
   re-derivation not repeated — the 2026-09-09 live proof stands, and the
   resolved-config command confirms the layer is live); W-3 limitations honestly
   stated and true.
4. **F-4 — Spec omission: `external_directory` carries a fourth allow root.**
   Developer-verified live (2026-09-15): the resolved config and `opencode.jsonc`
   both allow `C:\data-mybizz-mgt\**` in addition to the three roots the spec
   table records (`mybizz`, `dev`, `pdlf`). The config **deliberately and
   legitimately** grants the management folder; the spec lags reality. **Resolved
   at gate: approved — spec updated 2026-09-15** to list the fourth root.
5. **F-5 — Spec omission: `agent.docs-manager` subagent is undocumented.**
   Developer-verified live (2026-09-15): the resolved config carries a
   `docs-manager` subagent (mode `subagent`, model `openrouter/qwen/qwen3.6-plus`,
   `permission.edit` deny, `permission.bash` deny — read-only by design). The
   spec's §Global config table records `agent.plan` only. Its read-only posture
   is consistent with the plan/build split philosophy; the spec lags reality.
   **Resolved at gate: approved — spec + permission-model doc updated 2026-09-15.**
6. **F-6 — Resolved-config stdout carries literal API values (security
   confirmation, not a new class).** The developer's returned `opencode debug
   config` output contains the resolved `OPENAI_API_KEY` / `ZEROENTROPY_API_KEY`
   values while the source `.jsonc` correctly holds `{env:...}` placeholders.
   This **confirms** the sensitive-data guard class: field extraction from the
   capture is correctly denied, the exam's capture-delete discipline is right,
   and `opencode debug config` stdout must be treated as secret-bearing. Values
   are not reproduced in this report.

## Tier 3 — Deep pass: LOCKED (developer-unlock decision deferred to the gate)

- **OC3-1** full restart + single-load regression — developer-run, on the
  developer's schedule (a restart interrupts this running session itself)
- **OC3-2** WSL default-distro confirmation via `wsl.exe -l -v` — Windows-side
  read, developer-run
- **OC3-3** upgrade-policy decision — no check failed; **stay on 1.15.12**
  (policy: never on newness, only on check failure)

## Deferred (runner attribution)

- ~~**OC1-2, OC1-4…10, OC2-3** — guard-forbidden (sensitive-data class) → developer
  bundle~~ — **all developer-verified 2026-09-15: PASS, every expected field
  confirmed** (see per-row "developer-verified")
- ~~**OC1-11** — guard-forbidden standing (raw `opencode.jsonc` content never
  agent-read)~~ — **developer-verified 2026-09-15: match vs spec table**, with F-4
  and F-5 spec omissions flagged
- **Tier 3 (OC3-1/2/3)** — unlock-gated; decision deferred to the gate

## Guard layers

Three denials this run, all honored absolutely, all known classes: (1) step-0
compound loop text carrying the cupcake token (exec-protection — matches even
non-execution command text); (2) resolved-config field extraction via grep
(sensitive-data); (3) a cupcake-token grep argument (exec-protection). The
installed-glob and directory-glob forms were used instead; no denial was retried
through an alternate path.

## Developer-run items — bundle (ONE request) — COMPLETED, developer-verified 2026-09-15

The two commands below were run by the developer; results verified field-by-field
against the spec table in the Tier 1 rows above (all PASS). Kept verbatim so the
next run can re-request precisely.

```bash
# (a) OC1-2/4/5/6/7/8/9/10 + OC2-3 — resolved-config field check
opencode debug config

# Expect (per opencode-config.md §Global config):
#   default_agent = plan
#   permission.task = deny
#   permission.edit = ask, with **/anvil.yaml deny
#   permission.webfetch = ask
#   permission.bash = ask, with the destructive-git / DROP|TRUNCATE / piped-curl-wget deny set
#   permission.external_directory = allow on C:\mybizz\**, C:\dev\**, C:\pdlf\**
#   agent.plan.permission.edit = deny
#   mcp.gbrain = local server entry present (keys env-passed — do not print values)

# (b) OC1-11 — global config content key-by-key vs the spec table
cat ~/.config/opencode/opencode.jsonc
```

Results recorded verbatim, tagged developer-verified, alongside the exact
commands — so the next run can re-request precisely. Do not paste key values into
the report — confirm match/non-match by field name only.
