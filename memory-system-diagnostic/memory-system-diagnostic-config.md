---
title: "memory-system-diagnostic-config"
doc-id: "memory-system-diagnostic-config"
---
# memory-system-diagnostic — Configuration

Canonical current-state configuration record for `memory-system-diagnostic` as
a system component. Agent-facing. Reflects the live-verified state as of
2026-09-28. States facts, not history — reasoning in
[[memory-system-diagnostic-explainer|Explainer]]; commands and procedures in
[[memory-system-diagnostic-reference|Reference]].

---

## Identity

| Item | Value |
|---|---|
| Component | `memory-system-diagnostic` — gated, stepwise health-check skill for the memory ecosystem |
| Run surface | OpenCode agent procedure; invoked explicitly as `/memory-system-diagnostic` |
| Source artifact | `C:\mybizz\mybizz-config-docs\memory-system-diagnostic\memory-system-diagnostic-SKILL.md` (authored 2026-09-27) |
| Installed skill | `~/.config/opencode/skills/memory-system-diagnostic/SKILL.md` — verbatim copy of the source artifact; installed 2026-09-28 |
| Skill frontmatter | skill-discovery format: `name: memory-system-diagnostic` + `description:` (developer-mandated convention for this artifact, 2026-09-28) |
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

The folder does not exist as of 2026-09-28; the first run creates it.

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
| `C:\mybizz\mybizz-config-docs\register-local.md` | no rows for this suite as of 2026-09-28; registration is creation-event work for [[doc-maintainer-config|mb-doc-maintainer]] — the pending-events queue holds no events for these files as of 2026-09-28 |

## Recorded decisions (developer)

| Decision | Value |
|---|---|
| Skill front matter | `name`/`description` skill-discovery format for the artifact in this folder (instruction given with the implementation task, 2026-09-28) |
| Invocation | explicit only — never auto-triggered, never scheduled |

## Open items

| # | Item | Status |
|---|---|---|
| 1 | Register rows for the suite's four documents — pending a [[doc-maintainer-config|mb-doc-maintainer]] run; creation events for the folder's files are absent from the queue (folder created 2026-09-27 evening) | Open |
| 2 | GBrain ingest of the suite — closed 2026-09-28 (targeted sync ingested 4 pages at commit `c0570db`) | Closed |
| 3 | Report folder `C:\mybizz\memory-diagnostic-reports\` absent — created by the first run | Open |
| 4 | First live run of the skill — not yet executed; all runtime claims remain procedure until then | Open |
| 5 | No `mb-config-*` config-exam module exists for this suite | Open |
| 6 | Frontmatter-format conflict at the maintainer's repair surface: the artifact carries skill-discovery frontmatter (`name`/`description`), which the two-field doc-contract rule would classify as `EXTRA_FIELD` and repair away — needs a developer decision (exemption, or a two-field `-skill.md` corpus copy with `SKILL.md` only at the install location, per the sibling-suite pattern) before the next maintenance run touches this folder | Open |
