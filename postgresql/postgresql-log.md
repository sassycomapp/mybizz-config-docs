---
document: "PostgreSQL — Log"
doc-id: postgresql-log
state: Live
date-created: 2026-09-12
---

# PostgreSQL — Log

Chronological record of notable events for this system: exam runs and outcomes,
crashes, failure incidents, upgrades, error reports, significant guard denials.
Events, not lessons — lessons live in `postgresql-learnings.md`. Pruned under the
absorption rule: an entry goes once absorbed into a learning, skill row, plan item,
or governance flag, and resolved.

| date | event | outcome / disposition |
|---|---|---|
| 2026-09-05 | Windows `postgres` admin DB graveyard (28 mem0/vector tables + `vecs` schema) removed | Cleaned after verified backup; `compliance_ledger` (Instance B) same day |
| 2026-09-09 | `pgvector_user`/`pgvector_readonly` roles investigated + removed; `.env` line-16 quoting fixed; boot-durability fix proven across full WSL restart | All verified live; last open item closed |
| 2026-09-12 | First exam run (pilot, detection-only, Tier 0–2, both instances) | Verdict: HEALTHY. 2 findings: spec counts stale (docs governance); agent execution boundary confirmed (bundled system-path probe guard-blocked; checks rerouted developer-run) |
| 2026-09-12 | Same-day follow-up closed coverage gaps: B autovacuum + idle-in-txn probed; cupcake/gbrain cross-checks | B green; A operational probes agent-forbidden (secrets guard on `.env` sourcing) → developer-run class |
| 2026-09-12 | Exam architecture enhanced: plan-driven cycle adopted; exam-plan, log, learnings added to suite | First plan (this file's first run) hand-written as format template |
| 2026-09-12 | Architecture stabilization pass: check inventory graduated plan→skill; plan restructured (erred-last-run section; standing checks by reference); graduation rule applied (learnings entry deleted on graduate); developer-run request list completed | Plan and skill now division-of-labor clean; verification duty carried forward (CF-5) |
| 2026-09-12 | QC hardening pass: write-then-replace report discipline; pruning restricted to permanent homes (plan never an absorption destination); skill source restored to suite folder (copy-install model; hash d56843357f1bdf43 in register) | Fragility points locked; report/log/learnings rules now failure-proof |