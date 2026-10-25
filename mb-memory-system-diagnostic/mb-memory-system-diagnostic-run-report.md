---
title: "mb-memory-system-diagnostic-run-report"
doc-id: "mb-9c32dd94"
updated: "2026-10-25"
---
# Memory System Diagnostic — Run Report

Run start: 2026-10-25 10:52 SAST
Run scope: GBrain, PostgreSQL Instance B (WSL), Memory Governor, mb-submit-memory, Graphify, Dream Cycle. Instance A / pdlf out of scope.

## Section 1 — GBrain core
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| version | 0.59.18.0 (upgrade available 0.60.444.0 — notify mode, not a defect) |
| doctor exit code | 0 |
| doctor status / score | warnings / health_score 95, brain_checks_score 100, actions[] empty |
| pages / chunks / embedded | 2248 / 6482 / 6482 (100%) |
| sources | 18 registered, all reachable, 0 fails, embed 100% |
| sources with GitHub remote | 18/18 (ADR: dev-tooling-source-repos-must-be-github-backed) |
| observation | mb-4-ecom-project-library sync LAG 20h (unsynced repo work exists; not a §1 defect — flagged for commit-all context) |
Findings: (none)
Remediation: (n/a)
Developer decision: (n/a)

## Section 2 — PostgreSQL Instance B (WSL, v16; gbrain + memory_governor only)
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| live init system (PID 1) | systemd — matches reconciled record 2026-09-28 |
| management path: systemctl | pass (postgresql.service active since 2026-10-23 18:08 SAST) |
| management path: service | pass (same unit) |
| cluster status | 16/main, port 5432, online |
| gbrain tables / RLS-enabled | 93 / 93 (100%) |
| login roles | postgres, memory_governor_svc, ledger_approver, ledger_writer |
| role isolation: svc→gbrain CONNECT | false (expected false) |
| role isolation: svc→memory_governor CONNECT | true (expected true) |
Findings: (none)
Remediation: (n/a)
Developer decision: (n/a)

## Section 3 — Memory Governor
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| API listener | 127.0.0.1:8321 (python pid 501) |
| API status code | 422 (auth gate verified — API up) |
| worker process | present (pid 502, running since Oct 24) |
| outbox pending | 0 |
| permanently_failed | 0 |
| register git-clean | yes (porcelain empty) |
| systemd unit: api | active (running) since 2026-10-23 18:08 SAST |
| systemd unit: worker | active (running) since 2026-10-23 18:08 SAST |
Findings: (none) — one run-mechanics event: the §3 append via bash heredoc was blocked by the sensitive-data guard; logging resumed via Edit tool on developer approval (logged for §7)
Remediation: (n/a)
Developer decision: retry via Edit tool — approved 2026-10-25

## Section 4 — Governed write, positive path (heavyweight — developer-approved)
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| submit | HTTP 201, status promoted, decision_path auto_promote, risk_level low (fact, project_local, confidence 0.9) |
| worker-processed count | 3 events for the memory_id (candidate_created no-op + register_write + gbrain_write), all processed_at set |
| GBrain presence | true (facts row written into the disposable owning-project source) |
| visibility | private (project_local → private mapping verified) |
| register written | true (registers/candidates/<id>.json + register-memory-governor.md both contain the memory_id) |
| cleanup | forget rc 0 (fact expired; audit row then cascaded with source removal), governor DB rows left 0/0/0 (events, audit_log, candidates), disposable project deleted |
| source removal | diag-pos-1025 removed via sources remove --confirm-destructive; sources list 0 matches; facts rows 0 |
| brain default | restored to "default" after test (worker's GBrain write had switched it) |
| test artifacts | script /tmp/opencode/section4_positive.py; register git artifact for the test memory_id remains as a permanent audit record (by design) |
Findings: (none)
Remediation: (n/a)
Developer decision: approved 2026-10-25 (heavyweight gate); report append re-denied once by path guard after §3 — grant re-issued by developer

## Section 5 — Governed write, negative path (heavyweight — developer-approved)
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| submit | HTTP 201, status under_review — NOT promoted (policy type with confidence 0.99: high_risk_type routes to review regardless of confidence, determinism proven) |
| classification | high_risk_type, risk_level high, decision_path needs_review |
| review-queue presence | true (candidate listed on GET /memory/review-queue) |
| review resolution | HTTP 200 (decision reject, reviewer diagnostic-skill) |
| final state | rejected |
| cleanup | governor DB rows left 0/0/0 (events, audit_log, candidates), disposable project deleted; no GBrain fact/source involved (rejected candidates fire no writes) |
| test artifacts | script /tmp/opencode/section5_negative.py; first attempt aborted on a script bug (non-optional payload arg) — its candidate was cleaned up by the finally block before the corrected re-run |
Findings: (none)
Remediation: (n/a)
Developer decision: approved 2026-10-25 (heavyweight gate, approved together with §4)

## Section 6 — Graphify (read-only)
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| installed version | graphify 0.9.40 |
| graphs found | 6 (mb-3-cs-app1/app3/app5, mb-4-ecom-app1/app3/app5), all built 2026-10-18 in one batch |
| built_at_commit vs HEAD | match on all 6 graphs (no stale graph) |
| active-project graph (mb-3-cs-app5) | 10 nodes / 6 links / 0 hyperedges |
| live query returned a real result | yes — content-matched question (Form1/BaseLayout) returned BFS traversal, 8 nodes + 6 extracted edges. First phrasing (grid data refresh) matched nothing: the graph holds only 10 scaffold nodes, so that was query-content mismatch, not a surface defect |
Findings: (none)
Remediation: (n/a)
Developer decision: (n/a)

## Section 7 — Cupcake interaction (memory-system effect only)
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| denial/block lines in this run's governor logs (journald, since 10:52 SAST) | 0 |
| loopback exemption held | yes — all §4/§5 API calls succeeded (201/200 throughout); worker journald log shows the run's own events (4446 gbrain_write fact #133, 4448 candidate_created, 4449 review_resolved) processed with no policy interference |
| developer's direct answer | "No, nothing" |
| agent-side context (not a §7 defect) | two policy events hit the diagnostic agent's own actions this run: §3 report-append blocked by sensitive-data guard (developer approved Edit-tool lane); §4 report-append denied by path guard (developer re-issued grant). Neither touched the memory system |
Findings: (none)
Remediation: (n/a) — this section cannot remediate Cupcake; none needed
Developer decision: (n/a)

## Section 8 — mb-submit-memory (prerequisite state only)
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| registered source | mb-submit-memory (federated, 1 page, last sync 2026-10-24) |
| governor reachable | yes — 127.0.0.1:8321 listening (cross-referenced: proven live by §3 API check and §4/§5 real submissions) |
Findings: (none)
Remediation: (n/a)
Developer decision: (n/a)

## Section 9 — Backups (Instance B only — gbrain + memory_governor)
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| dump age | 0 days (both databases dumped 2026-10-25 10:00) |
| presence in both locations | gbrain + memory_governor dumps present in /home/dev-p/backup-gbrain/ and /mnt/c/backup-gbrain/ (prior 2026-10-20 sets also retained in both) |
| hash match | yes — gbrain pair sha256 ff1d3f81…c89de identical; memory_governor pair sha256 6f2fd68e…0f6e identical |
Findings: (none)
Remediation: (n/a)
Developer decision: (n/a)

## Section 10 — Dream Cycle (real run — developer-approved)
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| pre-run cycle_freshness | field not present in doctor --fast (DB-check-dependent; fast mode skips DB checks by design) |
| real run | gbrain dream --json completed — per-phase via .phase: 13 ok, 10 skipped (legitimate: sync/backlinks/lint/patterns/drift/enrich/skillopt/synthesize/extract/conversation_facts_backfill), 0 warn; heaviest phase synthesize_concepts 217385ms |
| page/chunk delta | pages 2248→2254 (+6); chunks 6482→5752 (−730, consolidation merging); links 3103→2748 (−355); embedded 5752/5752 (100%) |
| cycle_freshness re-check (full doctor) | FAIL — sources never-completed/stale (default 1683h; most never full-cycled); documented expected state: the dream's sync phase skipped on an already-synced brain, so nothing was stamped (dream-cycle reference, freshness bookkeeping) |
| doctor health score | 15/100 unhealthy — exactly matches the recorded Doctor baseline (15/100, cycle_freshness the only distinct FAIL, recorded as expected state) |
| contradiction eval (mandatory) | 0 contradictions; 3 findings — 1 temporal_supersession + 2 temporal_evolution (document-lifecycle verdicts, reviewed: map to memory-governor-config, the prior run-report page, and the 2026-09-15 auto-start fact — all part of the already-reconciled 2026-09-28 systemd story; no action). 0 judge errors, cost $0.0315 |
Findings: (none) — cycle_freshness FAIL is the documented expected state, not a defect
Remediation: (n/a)
Developer decision: approved 2026-10-25 (heavyweight gate)

## Summary

| # | Section | Status | Key metric |
|---|---|---|---|
| 1 | GBrain core | PASS | doctor exit 0, health 95, 18/18 sources reachable with GitHub remotes, embed 100% |
| 2 | PostgreSQL Instance B | PASS | cluster online, RLS 93/93, role isolation both directions correct, systemd init model matches record |
| 3 | Memory Governor | PASS | API 422 (auth gate verified), worker alive, outbox pending 0, permanently_failed 0, both units active |
| 4 | Governed write (positive) | PASS | 201 promoted → worker processed 3 events → private GBrain fact + register verified → cleanup complete |
| 5 | Governed write (negative) | PASS | policy type with 0.99 confidence held at under_review (high_risk_type) → rejected → cleanup complete |
| 6 | Graphify | PASS | 0.9.40; 6/6 graphs fresh (built_at_commit = HEAD); live query returned real traversal |
| 7 | Cupcake interaction | PASS | 0 policy denials in governor logs, loopback held, developer answer "No, nothing" |
| 8 | mb-submit-memory | PASS | source registered, governor reachable (cross-referenced §3–5) |
| 9 | Backups | PASS | both DBs, both locations, 0 days old, sha256 pairs identical |
| 10 | Dream Cycle | PASS | real run: 13 phases ok / 0 warn, brain changed (+6 pages, −730 chunks), contradiction probe 0 contradictions |

## Aggregate verdict

10/10 sections PASS, 0 REMEDIATED, 0 ABORTED — memory system fully functional.

## Findings requiring developer follow-up

None. Observations (not defects): gbrain 0.60.444.0 upgrade available (notify mode); mb-4-ecom-project-library carries 20h sync LAG (unsynced repo work — resolves on next commit-all); cycle_freshness FAIL is the documented expected state on an already-synced brain.
