---
title: "memory-system-diagnostic-skill"
doc-id: "memory-system-diagnostic-skill"
---

# Memory Diagnostic

A runnable, stepwise procedure for the OpenCode agent. Invoked only when the
developer explicitly asks for a "memory system diagnostic" or names this
skill. The agent reads this document and runs it section by section, in
order, stopping where this document says to stop.

**What this is not:** a compliance audit that produces one large report at
the end. **What this is:** a live pass through the memory ecosystem —
diagnose a section, remediate in place if something's wrong, log the outcome
immediately, then move to the next section. A healthy system should move
through this quickly with minimal interruption. A section with a real defect
stops and waits for a developer decision before continuing.

---

## Scope

**In scope (the memory ecosystem):** GBrain, PostgreSQL Instance B (WSL —
`gbrain` + `memory_governor` databases only), Memory Governor, mb-submit-memory,
Graphify, GBrain Dream Cycle.

**Explicitly out of scope:** PostgreSQL Instance A / the `pdlf` ledger — not
part of the memory system, never touched by this skill. Cupcake's own
internals — not a memory component, and the agent is forbidden from
live-testing the binary it is policed by. Cupcake is tested only for its
*effect on* the memory system (§7), never as a subject in its own right.

---

## Section 0 — Principles

1. **Never invent a result.** Every check runs for real; the report carries
   the real output or a faithful summary of it.
2. **The pipeline is Diagnostic → Remediation → Reporting, per section, in a
   loop** — not three phases run once across the whole suite. Reporting for
   a section happens immediately after that section closes, before the next
   section starts.
3. **Fast when healthy.** A section with no defects gets a one-line pass
   logged with its real metrics, then the next section starts immediately —
   no confirmation prompt for a clean result.
4. **Two distinct gates — do not conflate them:**
   - **Trouble gate:** a diagnostic finds a real defect → STOP, present the
     finding and a proposed remediation, wait for an explicit developer
     decision (`remediate` / `skip` / `abort run`) before continuing.
   - **Heavyweight-action gate:** a section performs a real-cost or
     state-changing action (a governed write, a dream cycle run) →
     always ask before running it, healthy system or not. This is not a
     trouble gate; it exists regardless of findings.
5. **A check that cannot run is a finding**, not a skip — report exactly
   what blocked it, then apply the trouble gate.
6. **Never read, print, or copy credential values.** Reference by variable
   name only, always.
7. **Known documentation drift, checked live rather than assumed:**
   `postgresql-reference.md` (verified 2026-09-13) states WSL here has no
   systemd. The Memory Governor's systemd migration was executed and
   verified two days later (2026-09-15), and is documented as affecting the
   entire WSL environment, not just the Governor's own processes. This
   skill does not silently pick a side — §2 runs a live init-model check
   first, before any other PostgreSQL Instance B command, and logs the real
   result. §3's Governor restart-posture check uses `systemctl --user
   status` per the newer record; if that fails outright, treat it as a
   finding, not a contradiction to paper over.

---

## Report file

Write to `C:\mybizz\memory-diagnostic-reports\memory-diagnostic-(date).md`
(date = run date, `YYYY-MM-DD`). **Append a result block for each section as
it closes** — do not hold results in memory and write once at the end. If
the run stops or is aborted partway, everything that completed is already on
disk.

Report style: **structured, technical, fact-finding. No prose narrative.**
Every entry is metrics + verdict, not paragraphs. Template per section:

```markdown
## Section N — <name>
Status: PASS | REMEDIATED | SKIPPED | ABORTED | BLOCKED
Metrics:
| Metric | Value |
|---|---|
| ... | ... |
Findings: (none) | <defect, one line each>
Remediation: (n/a) | <action taken> → <re-check result>
Developer decision: (n/a) | remediate / skip / abort — <timestamp>
```

---

## Section 1 — GBrain core

**Diagnostic:**

```bash
gbrain --version
gbrain doctor --fast --json | tee /tmp/gbrain-doctor.json
gbrain sources status 2>&1 | head -20
gbrain stats
```

**Interpreting `doctor`'s exit code — upstream-documented contract
(garrytan/gbrain `skillpack-check`), not just the score number:**

| Exit | Meaning                                                 | Action                                                                                                               |
| ---- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `0`  | Healthy                                                 | Log score, continue                                                                                                  |
| `1`  | Action needed                                           | Read `actions[]` from the JSON — this is a real finding → trouble gate, proposed remediation is `actions[]` verbatim |
| `2`  | Could not determine (binary crash / missing subcommand) | Finding → trouble gate, investigate before anything else in this section                                             |

**Source-remote check (per `dev-tooling-source-repos-must-be-github-backed`
ADR):** for each registered source with a `local_path`:

```bash
cd <source local_path> && git remote -v
```

Empty output = finding. **Remediation is heavyweight (creates a real GitHub
repo) — never auto-run.** If the developer approves, the ADR's documented
sequence applies:

```bash
gh repo create sassycomapp/<repo-name> --private --source=. --remote=origin --push
```

This finding exists so a future `sync_freshness` FAIL on this source is read
correctly (real uncommitted work) rather than mistaken for a gbrain defect.

**Metrics logged:** version, doctor exit code + score, page/chunk/embed-%
counts, source count with/without a remote.

**Pass:** exit `0`, all sources reachable, no source missing a remote (or
missing-remote findings logged and dispositioned).

---

## Section 2 — PostgreSQL Instance B — WSL-native, version 16 (`gbrain` + `memory_governor` only)

**Instance A (Windows-native PostgreSQL 15, `pdlf` ledger) is out of scope —
not checked anywhere in this section or this skill.**

**Live init-model check — run first, before anything else in this section.**
`postgresql-reference.md` (verified 2026-09-13) documents WSL here as having
no systemd (`pg_ctlcluster`/`service` only). The Memory Governor's auto-start
migration flipped `systemd=true` in `/etc/wsl.conf` two days later
(2026-09-15) — a change stated in the Governor's own docs to affect "the
entire WSL environment," not just its two processes. Which management path
is actually correct for Instance B *today* is therefore unverified, not
assumed either way:

```bash
ps -p 1 -o comm=
pg_lsclusters
systemctl status postgresql 2>&1 | head -5
service postgresql status
```

Log which command(s) actually work. If `systemctl` now works where the
reference doc says it can't, or `service`/`pg_ctlcluster` has stopped
working, that is a **finding** — trouble gate, remediation is a documentation
correction to `postgresql-reference.md` (developer-approved before editing;
this skill does not silently rewrite other suites' docs), not a live-system
fix. If both paths work, log both as currently valid and note the doc as
due for a reconciling update regardless.

**Diagnostic:**

```bash
pg_lsclusters
psql "postgresql://postgres:***@localhost:5432/gbrain" -c "SELECT count(*) AS tables, count(*) FILTER (WHERE relrowsecurity) AS rls_tables FROM pg_class WHERE relkind='r' AND relnamespace=(SELECT oid FROM pg_namespace WHERE nspname='public');"
psql "postgresql://postgres:***@localhost:5432/postgres" -c "SELECT rolname, rolcanlogin FROM pg_roles WHERE rolcanlogin ORDER BY rolname;"
```

**Role isolation — `has_database_privilege` only, never `SET ROLE`** (a
superuser session's `SET ROLE` always succeeds and proves nothing about the
role's real privileges):

```sql
SELECT has_database_privilege('memory_governor_svc', 'gbrain', 'CONNECT');   -- expect false
SELECT has_database_privilege('memory_governor_svc', 'memory_governor', 'CONNECT'); -- expect true
```

**Metrics logged:** live init system (PID 1 command), which management
path(s) work (`systemctl` / `service` / `pg_ctlcluster` — pass/fail each),
cluster status, table count + RLS-enabled count for `gbrain`, role isolation
result (pass/fail per role pair checked).

**Pass:** cluster `online`, RLS coverage matches the recorded 62/62, role
isolation confirms scoped access both directions, init-model check completed
and logged (mismatch against the reference doc is a finding, not a run
failure).

---

## Section 3 — Memory Governor

**Diagnostic:**

```bash
ss -tlnp | grep 8321
curl -s -o /dev/null -w "HTTP %{http_code}\n" --max-time 8 http://127.0.0.1:8321/memory/review-queue
ps aux | grep "app.worker" | grep -v grep
```

Pass on the curl: **HTTP 422** (credential-required — proves the API is up
AND its auth gate works). `000`/refused = finding.

```bash
cd /home/dev-p/memory-governor && set -a && source .env && set +a
.venv/bin/python -c "
import psycopg, os
with psycopg.connect(os.environ['MEMORY_GOVERNOR_DATABASE_URL']) as conn:
    with conn.cursor() as cur:
        cur.execute('SELECT count(*) FROM memory_events WHERE processed_at IS NULL AND permanently_failed = FALSE')
        print('pending:', cur.fetchone()[0])
        cur.execute('SELECT count(*) FROM memory_events WHERE permanently_failed = TRUE')
        print('permanently_failed:', cur.fetchone()[0])
"
git -C /home/dev-p/memory-governor status --porcelain registers/ | head -5
systemctl --user status memory-governor-api memory-governor-worker --no-pager 2>&1 | head -6
```

**Metrics logged:** API status code, worker process present (y/n), outbox
pending count, permanently-failed count, register git-clean (y/n), systemd
unit states.

**Pass:** 422, worker alive, `permanently_failed` = 0, register clean, both
units `active (running)`.

---

## Section 4 — Governed write, positive path (heavyweight — always gated)

**Ask before running, regardless of §1–3 health:** "Run the positive-path
governed write test now? This submits and cleans up one disposable
candidate." Proceed only on explicit yes.

**Diagnostic (the write):** the proven end-to-end pattern — submit via the
real API with a disposable GBrain source, run the worker's polling pass,
confirm GBrain presence + `private` visibility + register write, then
unconditionally clean up (DB rows, GBrain fact via `forget`, disposable
source removed). Full script: same shape as the corrected Check 8 from the
prior audit document, with `tempfile` imported. Do not omit the cleanup
block under any circumstance, including a mid-run failure — wrap in
`try`/`finally`.

**Pass:** submit `201 promoted`, worker processed ≥1, GBrain presence true,
`private` visibility true, register written true, cleanup confirmed complete.

**Metrics logged:** submit status, worker-processed count, presence/
visibility/register booleans, cleanup confirmation.

---

## Section 5 — Governed write, negative path (heavyweight — always gated)

**Ask before running:** "Run the negative-path governed write test now?
This proves the gate can say no, not just yes — submits a candidate
designed to trigger review, confirms it is NOT promoted, then resolves and
cleans up." Proceed only on explicit yes.

**Diagnostic (the write):** submit a disposable candidate with
`"memory_type": "policy"` (a `HIGH_RISK_TYPES` category — triggers
`high_risk_type` classification deterministically, regardless of
confidence, per the documented decision chain). Confirm the response is
`under_review`, never `promoted`. Then:

```
POST /memory/{memory_id}/review
{"decision": "reject", "reason": "memory-system-diagnostic negative-path test", "reviewer": "diagnostic-skill"}
```

Confirm state transitions to `rejected`. Clean up DB rows exactly as in §4
(`try`/`finally`, unconditional).

**Pass:** submit response is `under_review` (not `promoted`), review
resolution succeeds, final state `rejected`, cleanup confirmed complete.

**Metrics logged:** submit status/classification, review-queue presence,
resolution result, cleanup confirmation.

---

## Section 6 — Graphify (read-only)

**Diagnostic:**

```bash
graphify --version 2>&1 || pip show graphifyy 2>&1 | head -3
jq -r '.built_at_commit' <repo>/graphify-out/graph.json
git -C <repo> rev-parse HEAD
graphify query "<a real question about the active project>" --graph <repo>/graphify-out/graph.json
```

Compare the two commit hashes — mismatch = stale graph, a finding (trouble
gate; remediation is `graphify update <repo-root>` run from the repo root,
developer-approved before running since it writes files).

**Metrics logged:** installed version, node/edge counts (from
`graphify-out/graph.json`), `built_at_commit` vs live HEAD (match/mismatch),
one live query returned a real result (y/n).

**Pass:** commit hashes match, query surface answers.

---

## Section 7 — Cupcake interaction test (memory-system effect only, never Cupcake internals)

**This section never executes the Cupcake binary and never live-tests a
Cupcake rule** — that is permanently developer-only. What it checks instead:
did Cupcake interfere with anything in §1–6 of *this run*.

**Diagnostic:**

```bash
grep -i "deny\|block" /tmp/memory-governor.log /tmp/memory-governor-worker.log 2>/dev/null | tail -20
```

Review every denial/block line surfaced during this run's own log output.
Confirm the loopback exemption held (§4/§5's API calls succeeded — if they
didn't, and the failure mode looks policy-related rather than
connection-related, that is a Cupcake-interaction finding, not a Governor
defect).

**Then ask the developer directly:** "Did anything in this run feel blocked
or slowed by Cupcake, from your side — outside what the logs show?" Log the
answer verbatim as a metric, not a paragraph.

**Metrics logged:** denial/block line count found in this run's logs,
loopback exemption held (y/n), developer's direct answer.

**Pass:** zero policy-related denials in this run's logs, loopback held.
**This section cannot "remediate" Cupcake** — any real finding here routes
to a developer decision about whether Cupcake needs to be reconfigured or
disabled before memory operations, never an in-skill fix.

---

## Section 8 — mb-submit-memory (prerequisite state only)

**Diagnostic:**

```bash
gbrain sources list
ss -tlnp | grep 8321
```

Confirm the skill's own prerequisites are met (registered source, governor
reachable — already proven live by §3–5, cross-referenced here rather than
re-tested).

**Metrics logged:** prerequisite checks pass/fail, cross-reference to §3–5
results.

**Pass:** both prerequisites hold.

---

## Section 9 — Backups (Instance B only — `gbrain` + `memory_governor`)

**Diagnostic:**

```bash
ls -la /home/dev-p/backup-gbrain/ | grep -E "gbrain|memory_governor"
ls -la /mnt/c/backup-gbrain/ | grep -E "gbrain|memory_governor"
```

Confirm both dump files exist in both locations, age ≤ 7 days, and hash-match
the pair:

```bash
sha256sum /home/dev-p/backup-gbrain/<file> /mnt/c/backup-gbrain/<file>
```

**Metrics logged:** dump age (days) per database, presence in both
locations, hash match (y/n).

**Pass:** both databases, both locations, ≤7 days old, hashes match.
**Instance A (`pdlf`) backups are out of scope — not checked, not reported.**

---

## Section 10 — Dream Cycle (last section — state report, then explicit ask)

**Diagnostic (read-only, zero cost):**

```bash
gbrain doctor --fast --json | jq '.cycle_freshness // "field not present"'
```

Report the last known acceptance-run evidence (from prior config records)
alongside this live `cycle_freshness` reading. This is a state report, not
a pass/fail — a FAIL here on an already-synced brain is documented as
expected per the dream-cycle reference and is not itself a defect.

**Then stop and ask, regardless of state:** "Run a real Dream Cycle now,
including its mandatory post-run verification? This has real cost (LLM
spend, minutes, changes the brain) and is never run automatically."

- **If yes:** run `gbrain dream --json`, then the full post-run verification
  procedure — per-phase status via `.phase` (never `.name`), before/after
  `gbrain stats` delta, `cycle_freshness` re-check, and mandatory
  `gbrain eval suspected-contradictions --query "<real topic>"` with every
  finding reviewed before the section closes.
- **If no:** log as "skipped by developer choice," not a defect.

**Metrics logged:** pre-run `cycle_freshness` state; if run — per-phase
ok/skipped/warn counts, page/chunk delta, contradiction-eval finding count.

---

## Section 11 — Final report

Not a new discovery phase — a roll-up of what §1–10 already logged in real
time. Append to the same report file:

```markdown
## Summary

| # | Section | Status | Key metric |
|---|---|---|---|
| 1 | GBrain core | ... | ... |
| 2 | PostgreSQL Instance B | ... | ... |
| 3 | Memory Governor | ... | ... |
| 4 | Governed write (positive) | ... | ... |
| 5 | Governed write (negative) | ... | ... |
| 6 | Graphify | ... | ... |
| 7 | Cupcake interaction | ... | ... |
| 8 | mb-submit-memory | ... | ... |
| 9 | Backups | ... | ... |
| 10 | Dream Cycle | ... | ... |

## Aggregate verdict
(one line: e.g. "9/10 sections PASS, 1 REMEDIATED, 0 ABORTED — memory
system fully functional" — or the equivalent honest statement)

## Findings requiring developer follow-up
(only items not fully resolved during the run — real list or "none")
```

No prose beyond the table and the two one-line summaries above. This is a
technical record, not a narrative report.

---

## Do not

- Do not treat this as an audit that accumulates findings for one big report
  — remediate in place, per section, as findings occur.
- Do not gate a clean section on developer confirmation — only trouble and
  heavyweight-action gates stop the run.
- Do not run §4, §5, or §10's real-write path without an explicit yes, ever,
  regardless of how healthy the rest of the system looks.
- Do not execute the Cupcake binary or live-test a Cupcake rule — developer-
  only, permanently.
- Do not touch PostgreSQL Instance A / `pdlf` in any check.
- Do not auto-run the ADR's `gh repo create` remediation — always
  developer-approved first, since it creates a real GitHub repository.
- Do not hold section results unwritten — append to the report file as each
  section closes.
