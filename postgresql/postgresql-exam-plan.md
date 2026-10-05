---
title: "postgresql-exam-plan"
doc-id: "mb-c446fbf2"
updated: "2026-10-05"
---
# PostgreSQL — Exam Plan

Transient job-spec for the current exam run. Synthesized by the config-manager
from: [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md) (spec), the last
[[[mybizz-config-docs:postgresql/postgresql-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-exam-report.md), the [[[mybizz-config-docs:postgresql/postgresql-log|Log]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-log.md),
and [[[mybizz-config-docs:postgresql/postgresql-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-learnings.md). Consumed by the skill at run
time; rewritten at the start of the following cycle. The standing check inventory
(P0-1…P3-6) lives in the installed skill; this plan carries run-specifics and
deltas only.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #3 — single-system cycle, explicit developer instruction (2026-10-05) |
| Run date | 2026-10-05 |
| Prior report | [[[mybizz-config-docs:postgresql/postgresql-exam-report\|Exam Report]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-exam-report.md) (run #2, 2026-09-13) |
| Step-0 result | PASS with one estate finding **S0-F1** (register body-hash column stale ×1 — `mb-memory-system-diagnostic`; config-manager's own doc, gate item there; not this system's). 15/15 source↔installed body match; suite 15/15; spec-doc paths 15/15; one-run-at-a-time holds |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only on developer unlock at the gate |
| Developer-run requests this run (bundled) | (a) Instance A ops bundle: P0-2, P1-10, P2-1…P2-7 (incl. carried P2-6 corrected command), P1-9 A log scan; (b) B log scan P1-8 with rate-watch delta; (c) boot config P2-14 (per the retired-boot posture); (d) `.env` integrity P2-15; (e) if P1-11 finds stale dumps: Instance A dump commands for the fresh cycle (listed at the gate) |
| Expected-value source of truth | [[[mybizz-config-docs:postgresql/postgresql-config\|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md) — read fresh at run start; never rely on remembered values |

## 2. Carried-forward items (from run #2 report)

| # | Item | Why carried | This run's action |
|---|---|---|---|
| CF-1 | P2-6 corrected command (A `postgres` admin-DB table count — the one open evidence item) | Returned output last run covered the wrong DB | Bundle exact command (in run #2 report §Not run this cycle) into the Instance A developer request |
| CF-2 | P1-8 log-rate watch (run #2 finding 4: watch the *rate*, not just presence) | Note not yet absorbed into the skill's P1-8 row | Developer B-log scan counts ERROR/FATAL/PANIC lines dated after 2026-09-13 10:25; expected: zero, or only this exam's own probes; lifetime baseline 409 at 2026-09-13 |
| CF-3 | Tier 3 | Unlock not given last run beyond P3-4/5/6; P3-1/2/3 deferred-documented | List as available; execute only on unlock |
| CF-4 | **Backup freshness + fresh-cycle preparation** (developer-requested item 1) | Last full cycle 2026-09-13; standing cadence 7 days | Determine the actual age of every dump in both locations; if any older than 7 days, prepare at the gate the complete fresh cycle for all five databases (Instance B agent-runnable; Instance A developer-run bridge commands) — dump once, copy to both, hash-verify each pair |
| CF-5 | **Spec-currency sweep** (developer-requested item 2) | Spec carries dated history passages | List every dated history passage in the spec (removed roles, resolved records, "verified" dates in narrative) and propose present-state wording, so the spec states the current state only |

## 3. Erred last run

None erred in run #2. Standing execution rules remain in force (from the
2026-09-12 stabilization): psql probes run as one batch; system-path reads
(`/etc/…`, `/var/log/…`) never bundled into a probe command; the Instance A
bridge is never sourced by the agent (execution boundary) — Instance A probes go
straight into the developer request.

## 4. Log-driven items (after the 2026-10-05 sweep appends)

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-09-15 systemd migration | PID 1 is systemd; `systemctl status postgresql` works; cluster online (P0-3) |
| LG-2 | 2026-09-28 credential rotation | The documented variable-form connection (`~/.gbrain/config.json` `database_url`) works — P0-4 exercises exactly that path |
| LG-3 | 2026-09-28 boot-command retirement | `postgresql.service` enabled (agent-checkable); `/etc/wsl.conf` carries no `[boot]` command (P2-14, developer-run, spec-governed expectation) |
| LG-4 | No other notable unlogged events found at sweep time | — |

## 5. Learnings-driven items

None — the learnings file is empty (both run-#2 learnings graduated 2026-09-13).

## 6. Standing checks + run-specific deltas

The complete inventory (P0-1…P3-6, runner per check, pass rules) lives in the
installed skill; expected values come from the spec, read fresh at run start.
Deltas this run:

- **P1-11 (CF-4, item 1):** not just newest-per-DB — list **every** dump in
  `/home/dev-p/backup-gbrain/` and `/mnt/c/backup-gbrain/` with mtime, compute
  age against 2026-10-05, and hash-verify each location-pair (`cmp` + sha256).
  Spec cadence: 7 days, exam-enforced. Any dump older than 7 days → finding →
  prepare the fresh cycle at the gate (all five DBs; Instance B part
  agent-runnable post-approval; Instance A part developer-run `pg_dump.exe`
  commands via the bridge, dump once → copy to both → hash-verify each pair;
  naming `<db>-db-backup-YYYY-MM-DD.dump`, admin DBs disambiguated `-a-`/`-b-`;
  live-database rule: never re-dump one side of a pair).
- **P1-8 (CF-2):** rate-watch delta as in §2.
- **P2-14:** the skill's expected cell ("`[boot]` command intact") is
  superseded by the spec's current boot posture (boot-command retirement,
  2026-09-28): expected = `/etc/wsl.conf` carries **no** `[boot]` command;
  `postgresql.service` enabled; governor user units enabled. Spec governs; the
  skill's cell is flagged for its next revision (gate item, not applied here).

## 7. Report requirements

Write [[[mybizz-config-docs:postgresql/postgresql-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-exam-report.md)
(write-then-replace): verdict line; per-tier tables (ID, expected, actual,
result, runner attribution); findings with class (DOWN/UNHEALTHY/DRIFT/GAP),
evidence, recommended repair (allowlist only), rollback, risk; developer-returned
results recorded verbatim, tagged developer-verified, with exact commands.
This run additionally: (i) a **backup-cycle findings section** with the full
prepared fresh-cycle command set; (ii) a **spec-currency section** listing every
dated history passage with proposed present-state wording. Then: one run row
appended to the log; new learnings filed; prune only absorbed entries whose
permanent home exists. The report is written before any pruning.

## 8. Gate protocol — hard stop, nothing applies without approval

Expected gate items: (G1) fresh backup cycle execution; (G2) spec present-state
rewording (docs governance — spec corrections only on approval); (G3) S0-F1
register column refresh (config-manager's own doc — proposal only); (G4) skill
deltas P1-8 rate rule + P2-14 expected cell (graduation into the skill +
re-install, on approval). Allowlist repairs only; deny-list never healed
(`pg_hba`, role/database drops, service deletion, dead-duplicate start,
`wsl.conf`/boot edits, superuser operations, any data mutation). Credentials by
variable name only, never printed. This run stops at the gate — no repair.
