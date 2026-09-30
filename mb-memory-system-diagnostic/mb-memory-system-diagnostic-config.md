---
title: "mb-memory-system-diagnostic-config"
doc-id: "mb-2b9404b5"
---
# mb-memory-system-diagnostic — Configuration

Canonical current-state configuration record for `mb-memory-system-diagnostic`
as a system component. Agent-facing. Reflects the live-verified state as of
2026-09-28. Formerly named `memory-system-diagnostic`; renamed 2026-09-28
(naming convention — homegrown skills carry the `mb-` prefix). States facts,
not history — reasoning in
[[mb-memory-system-diagnostic-explainer|Explainer]]; commands and procedures in
[[mb-memory-system-diagnostic-reference|Reference]].

---

## Identity

| Item | Value |
|---|---|
| Component | `mb-memory-system-diagnostic` — gated, stepwise health-check skill for the memory ecosystem |
| Run surface | OpenCode agent procedure; invoked explicitly as `/mb-memory-system-diagnostic` |
| Source artifact | `C:\mybizz\mybizz-config-docs\mb-memory-system-diagnostic\mb-memory-system-diagnostic-skill.md` (authored 2026-09-27; renamed from the `-SKILL` suffix and converted to the documentation-skill frontmatter 2026-09-28; suite folder and files renamed to the `mb-` prefix 2026-09-28; §0 principle 8 + §2 recipe updated to the verified variable-name/journald pattern 2026-09-28 by config-exam F-3) |
| Installed skill | `~/.config/opencode/skills/mb-memory-system-diagnostic/SKILL.md` — copy of the source artifact body; installed 2026-09-28, re-installed under the new name 2026-09-28, re-installed byte-exact after the F-3 edits (hash pair `b90ec20c33bf4272` / `b90ec20c33bf4272`, 2026-09-28) |
| Skill frontmatter | corpus copy: documentation-skill format — `title`/`doc-id` = `mb-memory-system-diagnostic-skill`; installed copy: `name`/`description` (developer convention, 2026-09-28: documentation skills on C:\ carry `title`/`doc-id`; installed skills in WSL carry `name`/`description`) |
| Ecosystem boundary | `archify/output/memory-ecosystem-project/memory-ecosystem-scope.md` (scope card) |
| Standing references | `postgresql/postgresql-reference.md`; `gbrain/gbrain-reference.md`; `gbrain-dream-cycle/gbrain-dream-cycle-reference.md` + `-log.md`; `memory-governor/memory-governor-reference.md`; ADR `dev-tooling-source-repos-must-be-github-backed` (`C:\dev\project-library-global\adr-global\`) |

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
| Run report | `C:\mybizz\memory-diagnostic-reports\memory-diagnostic-(YYYY-MM-DD).md` | append-only during the run — one result block per section as it closes, then the §11 roll-up |

The folder was created by the first live run (2026-09-28); it holds one report
per run, appended section by section.

## Live-verified component presence (2026-09-28)

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
| Source | `mybizz-config-docs` (federated; corpus-wide) — no dedicated source for this suite |
| Ingest state | ingested 2026-09-28 by targeted `gbrain sync --source mybizz-config-docs` at commit `c0570db` — 4 pages, 45 chunks, 13 links extracted; source now 266 pages |
| Next sync | standing `sync-gbrain` script (or targeted `gbrain sync --source mybizz-config-docs`) picks up future changes |

## Register usage

| Register | State |
|---|---|
| `C:\mybizz\mybizz-config-docs\register-local.md` | no rows for this suite as of 2026-09-28; registration is creation-event work for mb-doc-maintainer — the pending-events queue holds no events for these files as of 2026-09-28 |

## Recorded decisions (developer)

| Decision | Value |
|---|---|
| Skill artifact format | documentation-skill convention on the corpus copy — `title`/`doc-id` = filename stem, lowercase `-skill.md` suffix, `SKILL.md` reserved for the install location (developer convention, 2026-09-28; survey: 20/21 corpus skill files conform) |
| Invocation | explicit only — never auto-triggered, never scheduled |

## Open items

| # | Item | Status |
|---|---|---|
| 1 | Register rows for the suite's four documents — pending a mb-doc-maintainer run; creation events for the folder's files are absent from the queue (folder created 2026-09-27 evening) | Open |
| 2 | GBrain ingest of the suite — closed 2026-09-28 (targeted sync ingested 4 pages at commit `c0570db`) | Closed |
| 3 | Report folder `C:\mybizz\memory-diagnostic-reports\` — closed 2026-09-28: created by the first live run; holds `memory-diagnostic-2026-09-28.md` | Closed |
| 4 | First live run — closed 2026-09-28: executed full §1–§11, 10/10 sections completed, 7 PASS + 3 REMEDIATED in-run, zero aborts/skips; report at `C:\mybizz\memory-diagnostic-reports\memory-diagnostic-2026-09-28.md`; follow-up item 4 (skill-recipe currency) resolved same day by config-exam F-3 | Closed |
| 5 | No `mb-config-*` config-exam module — closed 2026-09-28: `mb-config-mb-memory-system-diagnostic` built by config-exam run #1 (register row Installed, hash pair `d3975df16f28c2f9` / `4418e09f0c07ee23` at build) | Closed |
| 6 | Frontmatter-format conflict at the maintainer's repair surface — closed 2026-09-28: corpus copy renamed to `memory-system-diagnostic-skill.md` and converted to the two-field documentation-skill format (survey: 20/21 corpus skill files conform); `SKILL.md` with `name`/`description` exists only at the install location | Closed |
