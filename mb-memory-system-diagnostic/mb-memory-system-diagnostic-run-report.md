---
title: "mb-memory-system-diagnostic-run-report"
doc-id: "mb-9c32dd94"
updated: "2026-10-05"
---

# Memory System Diagnostic — 2026-09-28

Run mode: full (§1–§11). Heavyweight gates (§4, §5, §10) paused inline for developer decision. Approved scope set at start: §6 Graphify target = /mnt/c/dev/dev-mb-3-cs/mb-3-cs. Grant slips: /mnt/c/mybizz/memory-diagnostic-reports ×15; /mnt/c/dev/dev-mb-3-cs/mb-3-cs ×2 (conditional §6).

## Section 1 — GBrain core
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| CLI version | gbrain 0.46.1.0 (upgrade available: 0.59.0.0, `gbrain self-upgrade`) |
| doctor exit code | 0 |
| doctor checks | 14 ok, 1 warn — `connection: Skipping DB checks (--fast mode, URL present from config-file)` (expected in --fast, not a defect) |
| doctor brain_score | null (not produced by --fast) |
| doctor actions[] | empty |
| Pages / chunks | 2162 / 6497 |
| Embed coverage | 6497/6497 = 100% |
| Sources registered | 17 (all embed 100%, fails 0, backfill idle, queue 0) |
| Source lag | default 2d (last sync 2026-09-25 11:18); mybizz-config-docs 9m; rest ≤1d/0s |
| Sources with git remote | 17/17 — no empty-remote finding |
Findings: (none)
Remediation: (n/a)
Developer decision: (n/a)
Notes: default-source 2d sync lag logged; upgrade availability logged — neither is a §1 pass criterion.

## Section 2 — PostgreSQL Instance B
Status: PASS (1 finding)
Metrics:
| Metric | Value |
|---|---|
| Live init system | PID 1 = systemd (WSL) |
| systemctl status postgresql | works — active (exited) since 08:25:15 SAST, EXIT=0 |
| service postgresql status | works — same systemd-backed output, EXIT=0 |
| pg_ctlcluster path | pg_lsclusters: 16/main online, port 5432 |
| Cluster | 16/main online |
| gbrain tables / RLS | 62 / 62 — matches recorded 62/62 |
| Login roles | ledger_approver, ledger_writer, memory_governor_svc, postgres |
| Role isolation: memory_governor_svc → gbrain CONNECT | false (expected) |
| Role isolation: memory_governor_svc → memory_governor CONNECT | true (expected) |
Findings:
- Doc drift: postgresql-reference.md (verified 2026-09-13) states WSL has no systemd; live check shows systemd IS PID 1 and both systemctl and service management paths now work. Both paths logged as currently valid; doc is due for a reconciling update (developer-approved edit only).
Remediation: (pending developer decision)
Developer decision: (pending — doc-drift gate)
Developer decision: remediate — developer chose "Remediate: fix doc" at 2026-09-28 run; edit to postgresql-reference.md §Management pending grant slip for mybizz-config-docs.

## Section 3 — Memory Governor
Status: REMEDIATED
Metrics:
| Metric | Value |
|---|---|
| API HTTP status | 422 (auth gate proven — served by pid 64, boot-script instance) |
| Port 8321 | LISTEN, pid 64 (python), up since 08:25 boot |
| Worker process | present — pid 467, app.worker, up 1h15m |
| Outbox pending | 0 |
| Permanently failed | 0 |
| Register git-clean | yes (empty porcelain) |
| memory-governor-worker.service | active (running) since 08:25:15 |
| memory-governor-api.service | CRASH-LOOPING — activating (auto-restart), exit status=3 |
Findings:
- memory-governor-api.service bind conflict: journal shows Errno 98 (address already in use) on 127.0.0.1:8321. Boot-script instance (pid 64, started 08:25 via start-memory-system.sh) owns the port; the systemd unit (enabled per the 2026-09-15 migration) cannot bind and restarts indefinitely. The API service itself is functional (422 proves it), but the documented pass criterion "both units active (running)" fails.
- Process note: the skill's prescribed sourced-env command was blocked by Cupcake's secrets guard (correctly). Outbox counts were obtained via the already-authorized postgres URL variable instead. One psql retry echoed a connection value to the terminal once; not recorded in any artifact, not repeated here.
Remediation: kill duplicate boot-script API instance (pid 64) → systemd unit binds port and owns API. Re-check: unit active (running) since 09:45:01, Main PID 17850; port 8321 bound by pid 17850; old pid gone; gate re-check HTTP 422 (auth gate intact under new owner).
Developer decision: remediate — developer chose "Kill duplicate, systemd owns (Recommended)" at 2026-09-28. Follow-up (dev-owned, out of this skill's scope): start-memory-system.sh still spawns a duplicate API at every WSL boot — cleanup decision for the memory-governor suite.

## Section 4 — Governed write, positive path
Status: PASS
Heavyweight gate: asked before running; developer approved ("Run positive-path test").
Metrics:
| Metric | Value |
|---|---|
| Disposable gbrain source | diag-mg-sec4 (temp dir + README placeholder, git-tracked — empty-commit sources are refused by design) |
| Project registration | HTTP 201 (POST /memory/projects) |
| Submit | HTTP 201 — status `promoted`, decision_path `auto_promote`, risk `low`, event_id 4421 (memory_id 9847df5c-4133-487b-b38a-7b769372934e) |
| Worker polling pass | rc 0, processed 2 |
| Outbox events | candidate_created / register_write / gbrain_write — all processed=true |
| GBrain presence | true — 2 facts written for entity diag-mg-sec4 |
| GBrain visibility | `private` on both facts (project_local mapping correct) |
| Register written | true (row present in register-memory-governor.md + payload JSON) |
| Cleanup | DB rows 0 (events/candidates/audit/projects verified by read-back), gbrain facts expired (2), source removed, register row + payload removed (scoped commit 5135485 pushed), temp dir removed |
Findings: (none)
Remediation: (n/a)
Developer decision: heavyweight gate — approved to run.
Notes: two facts per single remember call — benign for the test (both private, both expired); noted only. The MCP forget verb could not see the private facts (world-only transport, by design) — cleanup used the same soft-expire semantics (expired_at set, audit trail preserved) directly at the DB layer; the local CLI (0.46.1.0) has no forget subcommand.

## Section 5 — Governed write, negative path
Status: PASS
Heavyweight gate: asked before running; developer approved ("Run negative-path test").
Metrics:
| Metric | Value |
|---|---|
| Disposable gbrain source / project | diag-mg-sec5 (source add rc 0; project POST 201) |
| Submit (memory_type=policy) | HTTP 201 — status `under_review`, decision_path `needs_review`, risk `high` — NEVER `promoted` |
| Classification | high_risk_type (deterministic HIGH_RISK_TYPES route) |
| Review-queue presence | true |
| Worker pass | rc 0, processed 0 (nothing promotable in queue — correct) |
| Outbox events | candidate_created processed=true; NO register_write, NO gbrain_write events (correct for under_review) |
| Review resolution | HTTP 200 — under_review → `rejected` (reviewer diagnostic-skill, reason per skill text) |
| GBrain write | none — 0 facts for the entity (correct: only promoted writes reach GBrain) |
| Register write | none — register_row_present false (correct) |
| Cleanup | DB rows 0 (events/candidates/audit/projects read-back verified), gbrain facts none, source removed (verified gone from sources list), register nothing-to-clean, temp dir removed |
Findings: (none)
Remediation: (n/a) — one cleanup gap during the run (script omits source removal; §4's was MCP-removed) caught by post-run verification and closed immediately; no residue.
Developer decision: heavyweight gate — approved to run.

## Section 6 — Graphify
Status: PASS (1 finding at trouble gate — pending developer decision)
Metrics:
| Metric | Value |
|---|---|
| Installed version | graphify 0.9.40 |
| Graph artifact | /mnt/c/dev/dev-mb-3-cs/mb-3-cs/graphify-out/graph.json (developer-supplied target) |
| Nodes / links / hyperedges | 537 / 434 / 0 (edge data lives under `links` — an `edges` key is absent by design; the first read of 0 was a wrong key, not a malformed graph) |
| built_at_commit | 59175d9e504808ab278336e70b189066a2eae7e2 |
| Live HEAD | ad4da5fe3632dba5f2ac5d62265d7897e4d732d0 |
| Commit match | MISMATCH — graph is stale |
| Live query | yes — real traversal returned (27 nodes, BFS depth 2, real symbols/forms/tests) |
Findings:
- Stale graph: built_at_commit ≠ live HEAD. Remediation per skill: `graphify update /mnt/c/dev/dev-mb-3-cs/mb-3-cs` from the repo root — writes files, developer-approved before running. Grant slip (×2, conditional §6) already granted for this path.
Remediation: `graphify update` run from the repo root (developer-approved, grant slip used) → rebuilt 562 nodes / 457 links / 157 communities; built_at_commit now equals live HEAD (ad4da5fe); fresh live query returned a real traversal (payment webhook → server_code/server_payments/webhook_handlers.py + PaymentGatewayForm, 5 nodes); graphify-out left git-clean (no dirty files to commit).
Developer decision: remediate — developer chose "Run graphify update (Recommended)".

## Section 7 — Cupcake interaction
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| Denial/block lines in governor's own logs this run | 0 (journalctl --user for both units since 08:25; the skill's /tmp/memory-governor.log path does not exist in the current systemd-managed setup — logs live in journald) |
| Loopback exemption held | yes — §4 API calls 201/201, §5 201/200, all review/queue reads succeeded |
| Developer's direct answer (verbatim) | "All tests must be fully run and correctly completed. Do not skip running tests because you do not have a right grant. You have to request the right grants, and I will provide the permission slips. But do not skip the tests because you are having a challenge with writing. Rather stop. Tell me what your challenge is, and I will correct the issue,  I want the tests to run completely and correctly. Understand this, it's critically important" |
| Agent-side Cupcake denials during this run (data) | 6, all matching documented policy surfaces: 2 report-heredoc writes (secrets-guard pattern triggers), 1 inline sourced-env read, 1 probe git commit, 1 bash grep whose command text contained destructive-SQL tokens, 1 inline process-environment read. None altered §1–§6 outcomes; nothing was worked around — report writing continued via file-tool writes plus fresh grant slips |
Findings: (none — every denial matched a documented policy surface)
Remediation: (n/a)
Developer decision: (n/a)
Notes: Cupcake was never executed as a subject; this section checks only its effect on §1–§6 of this run.

## Section 8 — mb-submit-memory (prerequisite state only)
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| Prereq 1: registered source | `memory-governor-code` registered, 46 pages (config records 53 — count drift noted, not a prereq failure) |
| Prereq 2: governor reachable | yes — port 8321 LISTEN; cross-ref §3: HTTP 422 auth gate proven |
| Naming drift | RESOLVED per config (2026-09-15): evidenced owning_projects (mybizz-config-docs, makepdlf-project-library) both match registered sources exactly in the live list |
Findings: (none)
Remediation: (n/a)
Developer decision: (n/a)
Notes: cross-referenced §3–§5 live results, not re-tested.

## Section 9 — Backups (Instance B only)
Status: REMEDIATED
Metrics:
| Metric | Value |
|---|---|
| Pre-check | both dumps present in both locations, sha256 pairs identical — but dated 2026-09-13 = 15 days old (criterion ≤7 days) → FAIL |
| gbrain-db-backup-2026-09-28.dump | 66,293,105 B, both locations, pg_dump rc 0, sha256 e9700911c6fe71050de2efce0893f6bf5f9f4ac2b4474b3d6d34aaff99d9e73b — pair match |
| memory-governor-db-backup-2026-09-28.dump | 54,217 B, both locations, pg_dump rc 0, sha256 0f74ac9e99926f5d52038e1ea1525fcde9160ad052a77d9f322c100e0b0f7cad — pair match |
| Dump age after refresh | 0 days |
Findings: (resolved in-run — stale dumps refreshed)
Remediation: pg_dump both databases (URLs by variable name only) → mirror-copy to Windows side → sha256 both pairs verified identical.
Developer decision: remediate — developer chose "Refresh backups now (Recommended)".
Notes: Instance A (pdlf) dumps exist on disk but are out of scope — not checked, not reported.

## Section 10 — Dream Cycle
Status: PASS — fully run and verified (re-run after developer credit top-up and a mid-run reboot)
Heavyweight gate: asked before running; developer approved. Run 1 EXIT 0 but degraded by empty Anthropic balance → developer topped up credits and ordered a full re-run. Run 2 was killed mid-flight by a full computer reboot (internet loss + reboot, developer-confirmed) — doctor showed no stale locks; its partial work integrated cleanly (+42 pages). Run 3 completed in full.
Metrics:
| Metric | Value |
|---|---|
| Final run result | EXIT 0, 23 phases — 13 ok / 10 skipped / 0 warn / 0 fail |
| Credit errors | 0 (all 13 previous extract_atoms balance errors gone after top-up) |
| Long phases (documented #1972 informational shape, all completed) | extract_atoms 142s, synthesize_concepts 401s, propose_takes 57s |
| Pre-run base (after reboot-integrated partial work) | 2205 pages / 6539 chunks / 100% embedded |
| Post-run stats | 2295 pages (+90) / 6630 chunks (+91) / 100% embedded / links 2296 |
| cycle_freshness (live) | field not present in --fast doctor JSON on 0.46.1.0 — reading unavailable, logged as-is; freshness-FAIL-on-fresh-brain is documented expected mechanism (W-3), not a defect |
| Contradictions eval (judge fully working) | query "memory governor systemd migration": 8 findings — 0 contradiction, 2 temporal_supersession, 6 temporal_evolution, 1 no_contradiction; judge errors 0; $0.0305; 47s |
| Finding review (mandatory) | all 8 reviewed — every one is info-severity temporal record evolution (pending → executed timelines); zero hard contradictions, zero regressions, zero negation artifacts. Corroboration: the records' "boot script idempotent skip proves itself at next natural restart" claim is DISPROVED by today's boot (duplicate API spawned, bind race) — folds into follow-up #2 |
Findings: (none open — run-1's credit-balance degradation resolved by developer top-up + full re-run)
Remediation: developer topped up Anthropic credits → full re-run EXIT 0, 13 ok / 0 warn / 0 fail; eval re-run with working judge (8 findings reviewed, 0 contradictions).
Developer decision: heavyweight gate — approved; developer then directed the full re-run after top-up ("I require that you go back and fully run that test as there are now credits available").

## Summary

| # | Section | Status | Key metric |
|---|---|---|---|
| 1 | GBrain core | PASS | doctor exit 0; 2162 pages, 6497 chunks, 100% embedded; 17/17 sources with remotes |
| 2 | PostgreSQL Instance B | REMEDIATED | 62/62 RLS match; role isolation correct; init-model doc corrected (systemd PID 1 since 2026-09-15) |
| 3 | Memory Governor | REMEDIATED | 422 gate, worker alive, outbox 0/0; API crash-loop fixed (systemd owns port 8321) |
| 4 | Governed write (positive) | PASS | 201 promoted → worker 3/3 events → gbrain private + register row; cleanup verified 0 residue |
| 5 | Governed write (negative) | PASS | 201 under_review (never promoted) → review → rejected; no gbrain/register writes; cleanup verified 0 residue |
| 6 | Graphify | REMEDIATED | stale graph refreshed: built_at_commit = HEAD; 562 nodes / 457 links; query surface answers |
| 7 | Cupcake interaction | PASS | 0 denials in governor logs; loopback held; 6 agent-side denials all documented policy surfaces |
| 8 | mb-submit-memory | PASS | both prerequisites hold (source registered, governor reachable) |
| 9 | Backups | REMEDIATED | fresh dumps, both DBs, both locations, 0 days old, sha256 pairs match |
| 10 | Dream Cycle | PASS | full re-run after credit top-up: EXIT 0, 13 ok / 0 warn / 0 fail; +90 pages; eval judged cleanly (8 findings reviewed, 0 contradictions) |

## Aggregate verdict

10/10 sections completed with zero aborts and zero skips — 7 PASS, 3 REMEDIATED in-run; memory system fully functional. Run weathered two external interruptions (empty Anthropic credits — resolved by developer top-up + full §10 re-run; internet loss + full computer reboot — no corruption, partial dream work integrated cleanly, §3 fix re-applied post-boot).

## Findings requiring developer follow-up

1. start-memory-system.sh still spawns a duplicate API at every WSL boot that fights the enabled memory-governor-api.service unit for port 8321 — §3 root cause; fixed at runtime twice today (kill pid 64 after 08:25 boot; kill pid 63 after the 11:01 reboot boot); the suite docs' "idempotent skip" claim was disproved by both boots. Cleanup decision for the memory-governor suite (script edit and/or boot-command change; /etc/wsl.conf is a system file — developer-owned).
2. postgresql-config.md line 89 carries the same stale no-systemd claim corrected in postgresql-reference.md today — flagged out-of-scope during the run; correction decision for the postgresql suite.
3. gbrain self-upgrade available (0.46.1.0 → 0.59.0.0) — noted §1; dream-cycle standing decision DC3-2 keeps 0.46.1.0; upgrade decision belongs to the developer.
4. The §2 prescribed .env-sourcing diagnostic and the /tmp log paths no longer match the systemd-managed environment (journald holds the logs; .env access is agent-forbidden) — the memory-system-diagnostic skill's §3/§7 recipes could be updated to the verified alternates (developer decision).
5. default gbrain source at 2d sync lag (last sync 2026-09-25) — noted §1, not a §1 pass criterion; a `gbrain sync` (or the standing sync script) refreshes it.

## Amendment — same-day remediation pass (2026-09-28, later the same day)

Scope approved by the developer: all follow-ups except the gbrain upgrade. Dispositions:

| # | Follow-up | Disposition | Detail |
|---|---|---|---|
| 1 | Boot-script duplicate API | DECIDED + DOCS RECONCILED — config change pending developer | Full boot-command retirement approved. All suite docs updated: memory-governor-config (Operational status, Processes, pending-item-4 parenthetical), memory-governor-reference (Correction 2026-09-28 section: idempotent-skip claim disproved at both boots, retirement decided), postgresql-config (Boot config row), postgresql-reference (Boot durability section rewritten), memory-governor-log (2026-09-28 row), facts page (both disproved claims corrected). Script body untouched — retained as manual fallback only. PENDING: developer applies the /etc/wsl.conf edit (system file, developer-owned), commits, and runs the fresh-boot proof (port 8321 held by the unit's pid only, no crash loop, 422) |
| 2 | postgresql-config.md stale no-systemd row | REMEDIATED | Management-tooling row now matches the postgresql-reference correction (systemd PID 1 since 2026-09-15, both paths verified 2026-09-28). Pending: commit/push + targeted sync |
| 3 | gbrain self-upgrade 0.46.1.0 → 0.59.0.0 | NO ACTION (by decision) | DC3-2 standing decision holds (no failed check; upgrade never on newness). Today's diagnostic verified 0.46.1.0 throughout; upgrade stays a deliberate future session |
| 4 | Skill recipes out of date (§3/§7 + §4/§5 pattern) | REMEDIATED in the corpus skill — installed copy pending | memory-system-diagnostic-skill.md updated: §3 outbox counts via the gbrain superuser URL (single-argument conninfo; .env path marked agent-forbidden), §7 logs via journalctl (the /tmp paths retired), §4/§5 implementation notes (script-file pattern, tracked-file requirement for sources add, caller-side source removal + read-back). The OpenCode installed copy (SKILL.md) could not be edited by the agent — the /home/dev-p/.config/skills path is refused by policy even with an active grant; the developer runs one body-sync command (challenge reported per the standing rule) |
| 5 | default source 2d sync lag | REMEDIATED | `gbrain sync --source default` run: 4a853d46..42b33915, 1 page modified, 13 chunks embedded, 0 stale |

Also closed during this pass: memory-governor-config's "pending developer execution" lines (auto-start was executed + verified 2026-09-15) reconciled with the executed state.

**Security observation (flag only, no action taken):** postgresql-config.md line 87 contains a full connection string with an inline password. Pre-existing suite-doc content, out of this pass's scope — the developer may want it referenced by variable name per the corpus's own credential rule (§Do-not: never quote a password value).

**Outstanding after this pass (developer actions):**
1. Edit `/etc/wsl.conf` — remove the `[boot]` command line (or comment it out; rollback = restore). Then `wsl --shutdown` from PowerShell, reopen, and the agent verifies: port 8321 held by the unit's pid only, both units active, no crash loop, auth-gate 422.
2. Commit + push the config-docs changes (9 files: postgresql-config, postgresql-reference, memory-governor-config, memory-governor-reference, memory-governor-log, facts page, memory-system-diagnostic-skill), then a targeted `gbrain sync --source mybizz-config-docs`.
3. Run the one-line SKILL.md body-sync command (provided in chat) to update the installed OpenCode copy.

## Amendment 2 — retirement executed and PROVEN (2026-09-28, same pass, later)

All three outstanding actions completed and verified:

| Action | Result |
|---|---|
| wsl.conf edit | `[boot]` now contains only `systemd=true`; the whole `command = ...` line deleted (verified from the developer's `cat` paste — agent cannot read the system path) |
| Fresh-boot proof (wsl --shutdown + reopen, uptime 2 min) | **PASSED on every check** — port 8321 held by pid 412 = memory-governor-api.service Main PID (unit journal confirms); both units active (running) since 12:25:03 with no crash loop; exactly 2 governor processes, both under unit cgroups, zero duplicates; cluster 16/main online started by postgresql.service alone; auth-gate HTTP 422 |
| Commit + push + sync | commit 4325b3e pushed (7 files, 82 insertions, 49 deletions); targeted sync d4afc380..4325b3e7 — 7 pages modified, 53 chunks re-embedded |
| Installed OpenCode skill copy | synced by the developer's one-line command; body verified identical to the corpus artifact (frontmatter intact) |

**Follow-up 1 is now CLOSED at the configuration level:** systemd owns all three boot processes; the boot script no longer runs at boot; the crash-loop failure mode is eliminated rather than repeatedly patched. The script remains on disk as a manual fallback only.

**Diagnostic run final state: 10/10 sections completed; every remediation either applied and verified in-run or applied and proven by the fresh-boot test. The one flagged-but-untouched item is the pre-existing inline credential in postgresql-config.md line 87 (security observation, developer decision pending).**

## Amendment 3 — credential rotation + corpus scrub (2026-09-28, closing the security observation)

The developer challenged the proposed one-line fix ("how do you know it has no downstream effect?") — the challenge triggered a source-verified expansion:

| Phase | Result |
|---|---|
| Consumer enumeration (paths + variable names only, values never printed) | Live consumers: `~/.pgpass` (stale — dated Jul 9, authentication actually FAILED with it) + `~/.gbrain/config.json` `database_url` + conditionally the governor `.env` (holds the separate `memory_governor_svc` credential). Systemd units, sync scripts, governor scripts: clean — zero embedded URLs. Exposure footprint: 13 doc occurrences across 3 files (config ×2, reference ×9, retired implementation doc ×3) + gbrain-indexed chunks + git history |
| Rotation (developer hands, interactive prompts — the value never passed through the agent) | `sudo -u postgres psql -c "\password postgres"` — role rotated. `.pgpass` updated (turned out to already hold the new value). `config.json` updated. Both live routes verified post-rotation: config-URL route SELECT 1 OK (exit 0), `.pgpass`-fallback route SELECT 1 OK (exit 0); `.pgpass` still `-rw-------` |
| Doc scrub (agent, grant-authorized) | All 13 occurrences de-materialized to variable-name form: config rows rewritten to "password lives only in ~/.pgpass + config.json, reference by variable, rotated 2026-09-28"; reference §Connecting + §Useful live queries rewritten to the `PGURL=$(jq -r .database_url ~/.gbrain/config.json)` + `${PGURL%/*}/postgres` pattern (the pattern proven live in §2 of this run); retired doc ×3 → `$PGURL`. Corpus-wide grep: zero password literals remain (only the unrelated variable name `gbrain_local_status` in retired agent scripts) |
| Downstream-effect check (the developer's actual question) | Verified BEFORE the scrub: no exam check (P1-1..P1-11, P2-x) consumes the credential literal — they compare live reality; wikilinks are doc-id-based and unchanged; the variable-name form was already proven live in §2; live systems never read credentials from markdown. The edit could not break a consumer that exists |
| Residuals (logged honestly) | The retired value remains in git history and in old gbrain page versions/chunks until re-sync replaces the current chunks — it is inert (no longer authenticates anything, which is the point of rotate-first) |

**Security observation CLOSED** — with the caveat that rotation is what retired the exposure; the scrub prevents future re-quoting.

**Outstanding (developer):** commit + push the 3 scrubbed files (postgresql-config.md, postgresql-reference.md, retired implementation doc), then a targeted `gbrain sync --source mybizz-config-docs` replaces the indexed chunks that still carry the old value.

## Section 7 — Cupcake interaction
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| Denial/block lines in governor's own logs this run | 0 (journalctl --user -u memory-governor-api -u memory-governor-worker since 08:25; the skill's /tmp/memory-governor.log path does not exist in the current systemd-managed setup — logs live in journald) |
| Loopback exemption held | yes — §4 API calls 201/201, §5 201/200, all review/queue reads succeeded |
| Developer's direct answer (verbatim) | "All tests must be fully run and correctly completed. Do not skip running tests because you do not have a right grant. You have to request the right grants, and I will provide the permission slips. But do not skip the tests because you are having a challenge with writing. Rather stop. Tell me what your challenge is, and I will correct the issue,  I want the tests to run completely and correctly. Understand this, it's critically important" |
| Agent-side denials during this run (data) | 6, all correctly-enforced documented policy surfaces: 2 report-heredoc writes (secrets-guard pattern triggers), 1 inline sourced-env read, 1 probe git commit, 1 bash grep whose command text contained DELETE-FROM tokens, 1 inline process-environment read. None altered §1–§6 outcomes; report writing continued via file-tool writes + fresh grant slips |
Findings: (none — every denial matched a documented policy surface; nothing worked around)
Remediation: (n/a)
Developer decision: (n/a)
Notes: Cupcake never executed as a subject in this section; this checks only its effect on §1–§6.

## Section 8 — mb-submit-memory (prerequisite state only)
Status: PASS
Metrics:
| Metric | Value |
|---|---|
| Prereq 1: registered source | `memory-governor-code` registered, 46 pages (config records 53 — count drift noted, not a prereq failure) |
| Prereq 2: governor reachable | yes — port 8321 LISTEN (count 1); cross-ref §3: HTTP 422 auth gate |
| Naming drift | RESOLVED per config (2026-09-15): evidenced owning_projects (mybizz-config-docs, makepdlf-project-library) both match registered sources exactly in the live list |
Findings: (none)
Remediation: (n/a)
Developer decision: (n/a)
Notes: cross-referenced §3–§5 live results, not re-tested.

## Section 9 — Backups (Instance B only)
Status: REMEDIATED
Metrics:
| Metric | Value |
|---|---|
| Pre-check | both dumps present in both locations, sha256 pairs identical — but dated 2026-09-13 = 15 days old (criterion ≤7) → FAIL |
| Remediation (developer-approved: "Refresh backups now") | fresh pg_dump of gbrain + memory_governor (custom format, rc 0 both) |
| gbrain-db-backup-2026-09-28.dump | 66,293,105 B, both locations, sha256 e9700911c6fe71050de2efce0893f6bf5f9f4ac2b4474b3d6d34aaff99d9e73b — match |
| memory-governor-db-backup-2026-09-28.dump | 54,217 B, both locations, sha256 0f74ac9e99926f5d52038e1ea1525fcde9160ad052a77d9f322c100e0b0f7cad — match |
| Dump age after refresh | 0 days |
Findings: (resolved in-run — stale dumps refreshed)
Remediation: pg_dump both DBs → mirror-copy both locations → sha256 both pairs verified identical.
Developer decision: remediate — "Refresh backups now (Recommended)".
Notes: Instance A (pdlf) dumps exist on disk but are out of scope — not checked, not reported.

## Section 10 — Dream Cycle
Status: PASS (1 finding — verification degraded by an external condition)
Heavyweight gate: asked before running; developer approved ("Run Dream Cycle after backups") — run executed after the §9 backup refresh (pre-dream restore point on disk).
Metrics:
| Metric | Value |
|---|---|
| Pre-run cycle_freshness (live) | field not present in `--fast` doctor JSON on 0.46.1.0 — reading unavailable, logged as-is |
| Prior acceptance-run evidence | 2026-09-14 DC3-1: full run PASS (EXIT 0, ~13 min, 11 ok / 12 skips / 1 warn, +124 pages); freshness-FAIL-on-fresh-brain documented as expected mechanism (W-3), not a defect |
| Run result | EXIT 0, 23 phases — 11 ok / 10 skipped / 2 warn |
| Warn 1 | extract_atoms: 13 × "credit balance is too low" (Anthropic account empty; key itself valid) — phase degraded gracefully, cycle completed |
| Warn 2 | synthesize_concepts: 84s duration exceeding the 30s force-evict deadline — documented benign shape (#1972), completed |
| Real-work delta (gbrain stats) | pages 2162→2163 (+1), chunks 6497→6498, links 2296→2296, embed coverage 100% |
| Contradictions eval (`eval suspected-contradictions --query "memory governor systemd migration"`) | 0 findings — BUT 9 judge errors at $0.00 (same empty Anthropic balance): "0 findings" means NO judgments were made, not clean evidence |
| Cost | dream: brain-internal LLM spend (phases ran); eval: $0.0000 (judge never executed) |
Findings:
- Empty Anthropic credit balance degrades extract_atoms (13 failed calls) and blinds the contradictions-eval judge (9 errors). Cycle still EXIT 0 with real work (+1 page). Developer follow-up: top up credits, then re-run the eval to complete §10's verification honestly.
Remediation: (pending developer follow-up — credit top-up is developer-owned)
Developer decision: heavyweight gate — approved to run; the follow-up above routes to §11.
