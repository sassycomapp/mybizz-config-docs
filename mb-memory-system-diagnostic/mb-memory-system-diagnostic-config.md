---
title: "mb-memory-system-diagnostic-config"
doc-id: "mb-2b9404b5"
updated: "2026-10-20"
---
# mb-memory-system-diagnostic — Configuration

Canonical current-state configuration record for `mb-memory-system-diagnostic`
as a system component. Agent-facing. Reflects the live-verified current state.
States facts, not history — reasoning in
[[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-explainer.md); commands and procedures in
[[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-reference.md).

---

## Identity

| Item | Value |
|---|---|
| Issuer | MyBizz |
| Installed version | `7b47fe6` (source repository HEAD) |
| Standard taken from | `7b47fe6` |
| Last researched | 2026-10-20 |
| Component | `mb-memory-system-diagnostic` — gated, stepwise health-check skill for the memory ecosystem |
| Run surface | OpenCode agent procedure; invoked explicitly as `/mb-memory-system-diagnostic` |
| Source artifact | `C:\mybizz\mb-memory-system-diagnostic\mb-memory-system-diagnostic.md` — the skill's own repository (GitHub-backed: `sassycomapp/mb-memory-system-diagnostic`; registered as the federated GBrain source `mb-memory-system-diagnostic`) |
| Installed skill | `~/.config/opencode/skills/mb-memory-system-diagnostic/SKILL.md` — body identical to the source artifact body; the installed frontmatter (`name`/`description`) is kept exactly |
| Skill frontmatter | source: `title`/`doc-id`/`updated` (`title`/`doc-id` = `mb-memory-system-diagnostic`, the filename stem); installed copy: `name`/`description` |
| Ecosystem boundary | `archify/output/memory-ecosystem-project/memory-ecosystem-scope.md` (scope card) |
| Standing references | `postgresql/postgresql-reference.md`; `gbrain/gbrain-reference.md`; `gbrain-dream-cycle/gbrain-dream-cycle-reference.md`; `memory-governor/memory-governor-reference.md`; ADR `dev-tooling-source-repos-must-be-github-backed` (`C:\dev\project-library-global\adr-global\`) |

## Scope

| Class | Members |
|---|---|
| In scope | GBrain; PostgreSQL Instance B (WSL PG16 — `gbrain` + `memory_governor` databases only); Memory Governor (API `:8321` + worker + registers); mb-submit-memory (prerequisite state only); Graphify (read-only); GBrain Dream Cycle (state report + gated run); Cupcake (its effect on §1–§6 of the run only — never the binary) |
| Out of scope | PostgreSQL Instance A (Windows PG15, `pdlf` ledger); Cupcake internals and any Cupcake rule execution (developer-only, permanent); everything outside the memory ecosystem |

## Section inventory

| # | Section | Subject | Gate class |
|---|---|---|---|
| 0 | Principles | run rules — never invent a result; per-section loop; two distinct gates; credential rule; drift rule | — |
| 1 | GBrain core | version, `doctor --fast`, sources, stats, per-source GitHub remote check | trouble; remediation heavyweight |
| 2 | PostgreSQL Instance B | live init-model check, cluster, RLS coverage, role isolation | trouble |
| 3 | Memory Governor | API + auth gate, worker, outbox, registers, systemd units | trouble |
| 4 | Governed write — positive path | submit → worker → GBrain `private` fact → register → cleanup | heavyweight (always) |
| 5 | Governed write — negative path | `policy`-type submit must not promote → reject → cleanup | heavyweight (always) |
| 6 | Graphify | version, graph freshness (`built_at_commit` vs HEAD), one live query | trouble; remediation heavyweight |
| 7 | Cupcake interaction | denial/block lines in this run's logs, loopback exemption, developer's direct answer | trouble; no in-skill remediation |
| 8 | mb-submit-memory | prerequisite state only (registered source + governor reachable) | trouble |
| 9 | Backups | Instance B dumps in both locations, age ≤ 7 days, pair hash match | trouble |
| 10 | Dream Cycle | `cycle_freshness` state report; gated real run + mandatory post-run verification | heavyweight (always) |
| 11 | Final report | roll-up of §1–§10 + aggregate verdict + unresolved findings | — |

## Gates

| Gate | Trigger | Effect | Allowed continuations |
|---|---|---|---|
| Trouble gate | a diagnostic finds a real defect — or a check cannot run | run stops at that section | `remediate` (developer-approved) / `skip` / `abort run` |
| Heavyweight-action gate | a section performs a real-cost or state-changing action | ask before running, healthy system or not | explicit yes / no |

Heavyweight-gated actions: §4 positive-path governed write; §5 negative-path
governed write; §10 real Dream Cycle run; §1's `gh repo create` remediation;
§6's `graphify update` remediation.

## Report storage

| Item | Path | Character |
|---|---|---|
| Run report | `C:\mybizz\mybizz-config-docs\mb-memory-system-diagnostic\mb-memory-system-diagnostic-run-report.md` | one file, replaced at the start of every run; one result block appended per section as it closes during the run, then the §11 roll-up |

## Live-verified component presence

| Item | Verified state |
|---|---|
| `gbrain` CLI | `/home/dev-p/.bun/bin/gbrain` |
| `graphify` CLI | `/home/dev-p/.local/bin/graphify` |
| Memory Governor repo | `/home/dev-p/memory-governor` present |
| Backup locations | `/home/dev-p/backup-gbrain` and `/mnt/c/backup-gbrain` both present |

Live runtime state (unit health, API status, outbox counts, dump ages, graph
freshness) is measured by the run itself, never asserted here — each
component's own config suite (`gbrain-config.md`, `memory-governor-config.md`,
`postgresql-config.md`, `graphify-config.md`,
`gbrain-dream-cycle-config.md`) is the standing record.

## GBrain integration

| Item | Value |
|---|---|
| Source | suite documents: `mybizz-config-docs` (federated; corpus-wide); skill source: its own repository, the federated GBrain source `mb-memory-system-diagnostic` |
| Sync | standing `sync-gbrain` script (or targeted `gbrain sync --source <id>`) picks up changes in both sources |

## Recorded decisions (developer)

| Decision | Value |
|---|---|
| Skill artifact format | source `<skill>.md` carries the documentation-skill frontmatter (`title`/`doc-id`/`updated`; title/doc-id = filename stem) in its own repository; `SKILL.md` with `name`/`description` exists only at the install location |
| Invocation | explicit only — never auto-triggered, never scheduled |

## Open items

None.
