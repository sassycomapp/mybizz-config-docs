---
document: "Memory Governor — Log"
doc-id: memory-governor-log
state: Live
date-created: 2026-09-13
---

# Memory Governor — Log

Chronological record of notable events for this system: exam runs and outcomes,
crashes, failure incidents, upgrades, error reports, significant guard denials.
Events, not lessons — lessons live in `memory-governor-learnings.md`. Pruned under
the absorption rule. (Seeded with development-period events so the system has
working data.)

| date | event | outcome / disposition |
|---|---|---|
| 2026-09-08 | System went ACTIVE after the full-resolution pass: two-outcome model live (commit c4df67d), HIGH_RISK_TYPES extended to all 5 spec categories, 304 tests passed 0 failed, both processes running for the first time in system history, worker's first persistent LISTEN/NOTIFY run | ACTIVE — all listed defects resolved |
| 2026-09-08 | Register integrity verified (index ↔ payload 1:1, real promoted candidates incl. a supersession pair); recovery proven twice (Phase 7.5 isolated + Phase 15.2 full-system drills) | Disaster-recovery proven |
| 2026-09-09 | Governor dev-testing errors visible in the postgres log (FK/dupe-key on `memory_candidates`) — historical, attributable to live RLS/insert testing | No action; watch for recurrence |
| 2026-09-09 | `ledger_writer`/`ledger_approver` RLS test roles documented in the postgres suite as the verified access-control precedent | Cross-referenced, not governed content |
| 2026-09-13 | Database included in the estate-wide backup convention (postgres-config §Backups — 26 KB dump, 5 tables verified, both locations) | Backup coverage confirmed |
| 2026-09-13 | Config-management architecture emulated onto this suite: exam-plan created (ID'd checks M0-1…M3-4), log created (this file), learnings filed; exam skill written (was an empty placeholder) | Suite at the 7-file standard; first formal plan-driven run pending |
| 2026-09-13 | M3-2 preparation COMPLETE: both systemd unit files authored + placed at `~/.config/systemd/user/` via the sanctioned mg-grant path (grant requested → 2 writes → revoked); migration procedure recorded in the reference doc. Remaining: developer-run wsl.conf edit + wsl --shutdown + systemctl enable --now (the restart terminates agent sessions — run last) | Pending item 4 → prepared state; memory-governor config management COMPLETE except the developer-executed restart step |
| 2026-09-13 | Run #1 — first formal plan-driven exam (bootstrap; step-0 PASS; Tiers 0–2 complete) | Verdict: **HEALTHY + FLAGS** — liveness fully green (M0-4's 422 probe validated); conformance green except spec-internal route-count inconsistency (header 12 vs table 11 vs live 11); **finding: events 3802–3806 failed attempt 1/5 (stale git lock + gbrain FileNotFoundError) with zero retries logged and no timestamps in the worker log** — developer verification bundle issued; 1 guard denial honored (/proc environ read) |
| 2026-09-13 | Governance applied (developer approval): route-count header corrected 12→11; point-in-time row-count note added to config.md; all three learnings graduated + deleted (skill ×2, config.md ×1); skill pair re-synced (3ac6c162174493a2) | Architecture completion pass done; remaining open: worker PATH + events 3802–3806 verification (developer bundle), Tier-3 items (locked), spec pending items 2–4 |
| 2026-09-13 | Finding 3 RESOLVED: outbox holds zero unprocessed events and no rows ≥ 3802 — the failed events were **delivered and purged** (outbox deletes on delivery); stale lock gone (clean tree). M3-4 repo push state already satisfied (main = origin/main). M3-1 full test suite rerouted developer-run (requires `MEMORY_GOVERNOR_DATABASE_URL` env — agent run without it produced KeyError, not a system fault; also covers M2-7 credentialed tests). Skill pair re-synced (c40df342d523aa59) | Memory-governor config management COMPLETE pending: developer suite run + worker PATH check + timestamps decision; Tier-3 unlock items |
| 2026-09-13 | M3-1 test suite: **304 passed, 0 failed** (developer-verified, env-loaded) — M2-7 credentialed tests covered → PASS. Commit 4b13706 pushed. Check 8 prepared for agent execution: grant requested via mg-grant, script bug corrected (missing `import tempfile`); agent run denied by the sensitive-data guard (.env sourcing — honored); grant revoked | Check 8 block handed to developer; report updated |
| 2026-09-13 | **Check 8 EXECUTED by the developer — ALL PASS CRITERIA MET**: submit 201 promoted; worker processed 3 events; worker git chain pushed live (e932be2); gbrain presence True, private visibility True, register written True; cleanup complete. Finding 3 follow-up **closed with live proof** (worker gbrain-write + git push succeeded — historical PATH failure did not recur). Verdict upgraded: SYSTEM HEALTHY, fully verified end-to-end | Memory-governor: architecture, exam, and live verification COMPLETE |
| 2026-09-13 | Timestamps decision RESOLVED: worker logging implemented with timestamps (worker.py basicConfig format — the run-#1 observability gap closed at source); syntax-verified; grant requested + revoked (edit cycle); suite re-run by developer confirms no regression | Memory-governor has ZERO open issues — all findings resolved, all Tier-3 items executed or prepared |
| 2026-09-13 | **Suite-race FIX implemented** (not just recorded): `scripts/run-tests-deterministic.sh` added to the governor repo — pauses the worker (kill by PID, documented safe method), runs the suite, always restarts the worker (trap); executable, syntax-verified; reference doc updated (bare pytest forbidden while the worker is live); learning graduated into the script + reference | Suite determinism fixed; awaiting developer verification run + commits |
