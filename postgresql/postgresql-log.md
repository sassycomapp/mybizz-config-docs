---
document: "PostgreSQL — Log"
doc-id: postgresql-log
state: Live
date-created: 2026-09-12
---

# PostgreSQL — Log

Chronological record of notable events for this system: exam runs and outcomes,
crashes, failure incidents, upgrades, error reports, significant guard denials.
Events, not lessons — lessons live in [[postgresql-learnings|Learnings]]. Pruned under the
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
| 2026-09-13 | Run #2 — first formal plan-driven exam (step-0 PASS; Tiers 0–2 agent-runnable complete) | Verdict: HEALTHY — B fully green (incl. connect-privilege isolation proof, schema v128 from config table); A liveness proven, ops probes developer-run; 3 findings (spec-count drift re-flagged; SET-ROLE nuance → learning; CF-5 graduation verified sound) |
| 2026-09-13 | Developer-run blocks 1/3/4/5 returned + recorded developer-verified (A bridge ops, B log scan 409 lines examined no active fault, boot config exact, .env syntax OK 3 vars); block 2 (A log scan) mis-pasted into WSL — PowerShell rerun pending; P2-4/5/6/7 detail follow-up issued | Exam evidence now majority developer-verified; one open finding class (log-rate watch → skill revision note) |
| 2026-09-13 | Block 2 rerun in PowerShell + recorded: A log file last written 2025-10-08 — zero log entries in ~11 months, all errors historical (incl. effective_io_concurrency tuning attempts, Windows-invalid); instance dormant-quiet, PASS. Only P2-4/5/6/7 schema detail now open | Run #2 evidence ~complete |
| 2026-09-13 | Developer approved config.md refresh in-session → applied: counts (1,824/5,529/164 MB), verification date → 2026-09-13, facts-autovacuum nuance + role-isolation method recorded; both learnings graduated + deleted (config.md + skill); skill source re-synced (hash 9f61f34c9634b419) | Finding 1 closed; graduation lifecycle exercised end-to-end for the first time |
| 2026-09-13 | **Estate-wide backup cycle executed** (scope expanded by developer decision: all 5 data-bearing DBs, both instances, one weekly exam-enforced cycle): Instance-B dumps agent-run (gbrain 51,429,231 B / 62 tables; memory_governor 26,032 B / 5 tables; postgres-b admin 1,093 B / 0 tables); Instance-A dumps developer-run via bridge (pdlf 21,720 B / 7 tables; postgres-a admin 5,179 B / 0 tables). All 5 pairs delivered to both locations + hash-verified. One process error caught + corrected: re-dumping one side of a live-DB pair diverged the pair (live DB writes between dump and copy) → re-dump + re-copy both + verify; lesson recorded in spec | Backups section (estate-wide) added to postgresql-config.md; P1-11 freshness check added to skill inventory (hash b41a3e117dee1809); largest unmitigated risk in the estate now mitigated |
| 2026-09-13 | Commits da1a6d3 + 4a15dae pushed; sync+embed run: 54 pages added, 61 chunks created, 57 pages embedded, 0 stale — brain now 1,878 pages / 5,571 chunks / 100% coverage (grew immediately after the exam's count refresh) | Count-type values drift by design at every sync — coverage % + growth explainability are the durable checks, exact counts are point-in-time per verification date (learning filed + graduated into config.md) |
| 2026-09-13 | P2-4/5/7 returned + recorded (schema matches spec incl. CHECKs/FK; plpgsql only; roles exact); P2-6 command error caught in-review (ran pdlf not admin DB) — corrected command issued; Tier-3 split executed: P3-4/5/6 agent-run now (third-instance PASS, guard layers PASS with live denial proof, backups exact), P3-1/2/3 deferred-documented (superuser + restart — carried in every future plan) | Run #2 essentially complete; ONE evidence item open (P2-6 corrected command) |
