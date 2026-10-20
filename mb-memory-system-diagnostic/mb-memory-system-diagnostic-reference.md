---
title: "mb-memory-system-diagnostic-reference"
doc-id: "mb-b0ec721d"
updated: "2026-10-20"
---
# mb-memory-system-diagnostic — Reference: Invocation, Sections, Gates, Reporting

Companion to [[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-config.md) (the spec —
current state) and [[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-explainer.md) (what it is
and why). The installed `SKILL.md` is the authoritative procedure; this
reference carries the exact commands, interpretation rules, and report formats
an agent consults while running it. Read the suite's
[[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-learnings.md) in full before any
research, examination or proposal for this system.

---

## Invoking the diagnostic

| Rule | Value |
|---|---|
| Invocation | `/mb-memory-system-diagnostic` in an OpenCode session — or the developer asking for a "memory system diagnostic" / a memory-system health check |
| Trigger discipline | explicit only — never auto-triggered, never scheduled, never chained from another skill without the developer naming it |
| Termination | the run ends after §11 or on an `abort run` decision; `skip` only skips a finding's remediation |

## Run flow

```text
1. Replace the run report file (create if missing):
   C:\mybizz\mybizz-config-docs\mb-memory-system-diagnostic\mb-memory-system-diagnostic-run-report.md
   — one file; every run replaces it in full.
2. Run Section 1 → Section 10 in order.
3. Append each section's result block to the report as the section closes —
   never hold results in memory; if the run aborts, everything completed is on disk.
4. Section 11: append the roll-up (summary table + aggregate verdict + unresolved findings).
```

## Status vocabulary

| Status | Meaning |
|---|---|
| PASS | healthy — one line logged with real metrics |
| REMEDIATED | defect found, remediated with developer approval, re-check passed |
| SKIPPED | developer chose skip on a finding — or declined a heavyweight action ("skipped by developer choice", not a defect) |
| ABORTED | developer aborted the run at this section |
| BLOCKED | check could not run — itself a finding (trouble gate) |

## Gates

| Gate | Trigger | Effect | Outcomes |
|---|---|---|---|
| Trouble | real defect, or a check that cannot run | STOP at that section | remediate (developer-approved) / skip / abort run |
| Heavyweight action | the section performs a real-cost or state-changing write | ask first, always — healthy system or not | explicit yes / no |

Do not conflate the gates: a clean §1–§3 does not authorize §4/§5/§10's
writes, and a declined heavyweight action is not a finding.

## Report block template (per section)

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

Report style: structured, technical, fact-finding — metrics + verdict, no
prose narrative.

## Section 1 — GBrain core

```bash
gbrain --version
gbrain doctor --fast --json | tee /tmp/gbrain-doctor.json
gbrain sources status 2>&1 | head -20
gbrain stats
# per registered source with a local_path:
cd <source local_path> && git remote -v
```

| `doctor` exit | Meaning | Action |
|---|---|---|
| `0` | healthy | log score, continue |
| `1` | action needed | read `actions[]` from the JSON — real finding → trouble gate; proposed remediation is `actions[]` verbatim |
| `2` | could not determine (binary crash / missing subcommand) | finding → trouble gate; investigate before anything else in this section |

Empty `git remote -v` output = finding. Remediation is heavyweight — never
auto-run. If the developer approves, the ADR sequence applies:

```bash
gh repo create sassycomapp/<repo-name> --private --source=. --remote=origin --push
```

Pass: exit `0`; all sources reachable; no source missing a GitHub remote (or
missing-remote findings logged and dispositioned).

## Section 2 — PostgreSQL Instance B

**Run the live init-model check first, before any other Instance B command.**
Log which command(s) actually work; a live result that contradicts the record
— or a management path that has stopped working — is a finding routed to a
documentation correction to `postgresql-reference.md` (developer-approved
before editing) — never a live-system fix.

```bash
ps -p 1 -o comm=
pg_lsclusters
systemctl status postgresql 2>&1 | head -5
service postgresql status
```

```bash
# Reach the DB through the gbrain config's database_url read into a shell
# variable — never source .env (agent-forbidden by the secrets guard); keep
# conninfo a single argument so psql errors cannot echo it. Credential
# referenced by variable name only.
PGURL=$(jq -r .database_url /home/dev-p/.gbrain/config.json)
pg_lsclusters
psql "${PGURL%/*}/gbrain" -c "SELECT count(*) AS tables, count(*) FILTER (WHERE relrowsecurity) AS rls_tables FROM pg_class WHERE relkind='r' AND relnamespace=(SELECT oid FROM pg_namespace WHERE nspname='public');"
psql "${PGURL%/*}/postgres" -c "SELECT rolname, rolcanlogin FROM pg_roles WHERE rolcanlogin ORDER BY rolname;"
```

Role isolation — `has_database_privilege` only, never `SET ROLE` (a
superuser session's `SET ROLE` always succeeds and proves nothing about the
role's real privileges):

```sql
SELECT has_database_privilege('memory_governor_svc', 'gbrain', 'CONNECT');           -- expect false
SELECT has_database_privilege('memory_governor_svc', 'memory_governor', 'CONNECT');  -- expect true
```

Pass: cluster `online`; every table has row-level security switched on
(`tables` equals `rls_tables`); role isolation confirms scoped access both
directions; init-model check completed and logged.

## Section 3 — Memory Governor

```bash
ss -tlnp | grep 8321
curl -s -o /dev/null -w "HTTP %{http_code}\n" --max-time 8 http://127.0.0.1:8321/memory/review-queue
ps aux | grep "app.worker" | grep -v grep
```

curl pass value: **HTTP 422** (credential-required — proves the API is up AND
its auth gate works). `000`/refused = finding.

```bash
# Reach the governor DB through the gbrain superuser URL (same cluster);
# reference by variable name only and never print it. The .env-sourcing path
# is agent-forbidden by the secrets guard. Keep the conninfo a single argument
# so psql errors cannot echo it.
PGURL=$(jq -r .database_url /home/dev-p/.gbrain/config.json)
psql "${PGURL%/*}/memory_governor" -t \
  -c "SELECT 'pending: ' || count(*) FROM memory_events WHERE processed_at IS NULL AND permanently_failed = FALSE;" \
  -c "SELECT 'permanently_failed: ' || count(*) FROM memory_events WHERE permanently_failed = TRUE;"
git -C /home/dev-p/memory-governor status --porcelain registers/ | head -5
systemctl --user status memory-governor-api memory-governor-worker --no-pager 2>&1 | head -6
```

Pass: 422; worker alive; `permanently_failed` = 0; register clean; both units
`active (running)`.

## Section 4 — Governed write, positive path (heavyweight — always gated)

Ask: "Run the positive-path governed write test now? This submits and cleans
up one disposable candidate." Proceed only on explicit yes.

Pattern (shape from the prior audit document's corrected Check 8):

```text
POST /memory/candidate        # disposable candidate via the real API
                              # writer_identity never in the payload — derived from the credential
→ run the worker's polling pass
→ confirm GBrain presence + `private` visibility + register write
→ unconditionally clean up: DB rows, GBrain fact via `forget`, disposable source removed
```

Cleanup is in `try`/`finally` — never omitted, including mid-run failure.

Pass: submit `201 promoted`; worker processed ≥ 1; GBrain presence true;
`private` visibility true; register written true; cleanup confirmed complete.

## Section 5 — Governed write, negative path (heavyweight — always gated)

Ask: "Run the negative-path governed write test now? This proves the gate can
say no, not just yes — submits a candidate designed to trigger review,
confirms it is NOT promoted, then resolves and cleans up." Proceed only on
explicit yes.

```text
POST /memory/candidate        # disposable candidate with "memory_type": "policy"
```

`policy` is one of the five high-risk categories (`policy`, `credential`,
`identity`, architecture, security check) → deterministic `high_risk_type`
classification, regardless of confidence. Confirm the response is
`under_review`, never `promoted`. Then resolve:

```json
POST /memory/{memory_id}/review
{"decision": "reject", "reason": "mb-memory-system-diagnostic negative-path test", "reviewer": "diagnostic-skill"}
```

Confirm the final state is `rejected`. Clean up DB rows exactly as in §4
(`try`/`finally`, unconditional).

Pass: `under_review` on submit (not `promoted`); resolution succeeds; final
state `rejected`; cleanup confirmed complete.

## Section 6 — Graphify (read-only)

```bash
graphify --version 2>&1 || pip show graphifyy 2>&1 | head -3
jq -r '.built_at_commit' <repo>/graphify-out/graph.json
git -C <repo> rev-parse HEAD
graphify query "<a real question about the active project>" --graph <repo>/graphify-out/graph.json
```

Compare the two commit hashes — mismatch = stale graph, a finding (trouble
gate; remediation is `graphify update <repo-root>` run from the repo root,
developer-approved before running since it writes files).

Pass: commit hashes match; the query returns a real result.

## Section 7 — Cupcake interaction (effect only — never Cupcake internals)

```bash
# The governor's logs live in journald under systemd — the retired
# /tmp/memory-governor*.log paths must not be used. Scope to this run's start.
journalctl --user -u memory-governor-api -u memory-governor-worker \
  --since "<run start time HH:MM>" --no-pager 2>/dev/null \
  | grep -i "deny\|block\|reject" | tail -20
```

Review every denial/block line surfaced in this run's own log output. Confirm
the loopback exemption held (§4/§5's API calls succeeded — if they did not,
and the failure mode looks policy-related rather than connection-related,
that is a Cupcake-interaction finding, not a Governor defect). Then ask the
developer directly: "Did anything in this run feel blocked or slowed by
Cupcake, from your side — outside what the logs show?" Log the answer
verbatim as a metric, not a paragraph.

Pass: zero policy-related denials in this run's logs; loopback held. This
section cannot remediate — any real finding routes to a developer decision
about reconfiguring or disabling Cupcake before memory operations, never an
in-skill fix.

## Section 8 — mb-submit-memory (prerequisite state only)

```bash
gbrain sources list
ss -tlnp | grep 8321
```

Cross-references §3–§5 results rather than re-testing. Pass: both
prerequisites hold (registered source; governor reachable).

## Section 9 — Backups (Instance B only)

```bash
ls -la /home/dev-p/backup-gbrain/ | grep -E "gbrain|memory_governor"
ls -la /mnt/c/backup-gbrain/ | grep -E "gbrain|memory_governor"
sha256sum /home/dev-p/backup-gbrain/<file> /mnt/c/backup-gbrain/<file>
```

Pass: both databases, both locations, age ≤ 7 days, hashes match. Instance A
(`pdlf`) backups are out of scope — not checked, not reported.

## Section 10 — Dream Cycle (last section)

```bash
gbrain doctor --fast --json | jq '.cycle_freshness // "field not present"'
```

State report, not pass/fail — a FAIL here on an already-synced brain is
documented as expected (dream-cycle reference), not a defect. Then stop and
ask, regardless of state: "Run a real Dream Cycle now, including its
mandatory post-run verification? This has real cost (LLM spend, minutes,
changes the brain) and is never run automatically."

If yes: `gbrain dream --json`, then the full post-run verification —
per-phase status via `.phase` (never `.name`), before/after `gbrain stats`
delta, `cycle_freshness` re-check, and mandatory
`gbrain eval suspected-contradictions --query "<real topic>"` with every
finding reviewed before the section closes. If no: log as "skipped by
developer choice", not a defect.

## Section 11 — Final report

Roll-up of §1–§10 — no new probing. Append to the same report file:

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
(one line, honest)

## Findings requiring developer follow-up
(only items not fully resolved during the run — real list or "none")
```

No prose beyond the table and the two one-line summaries.

## Credential handling

Never read, print, or copy credential values — reference by variable name
only. §2 and §3 reach both databases through the gbrain config's
`database_url` read into a shell variable (`PGURL=$(jq -r .database_url
/home/dev-p/.gbrain/config.json)`) — never source `.env` (agent-forbidden by
the secrets guard); keep conninfo a single argument so psql errors cannot
echo it.

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| Skill source artifact (issuer: MyBizz) | `C:\mybizz\mb-memory-system-diagnostic\mb-memory-system-diagnostic.md` — repository `sassycomapp/mb-memory-system-diagnostic` | `7b47fe6` | — |
| Installed skill | `~/.config/opencode/skills/mb-memory-system-diagnostic/SKILL.md` | `7b47fe6` — body identical to the source artifact body | — |
| [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification\|Doc Suite Specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md) | `C:\mybizz\mybizz-config-docs\mb-sysdoc-creator\doc-suite-specification.md` | — | — |
| ADR `dev-tooling-source-repos-must-be-github-backed` | `C:\dev\project-library-global\adr-global\adr-dev-tooling-source-repos-must-be-github-backed.md` | — | — |

## Checks

| Check | Method | Run by |
|---|---|---|
| Installed version | `git -C /mnt/c/mybizz/mb-memory-system-diagnostic rev-parse HEAD` | agent |
| §1 GBrain core | the §1 command block — `gbrain --version`, `gbrain doctor --fast --json`, `gbrain sources status`, `gbrain stats`, `git remote -v` per source | agent |
| §2 init model | the §2 init-model command block, run before any other Instance B command | agent |
| §2 RLS coverage | the §2 psql table/RLS count — passes only when every table has row-level security switched on | agent |
| §2 role isolation | the §2 `has_database_privilege` queries — never `SET ROLE` | agent |
| §3 Memory Governor | the §3 command block — 422 curl, worker process, outbox counts, register state, unit states | agent |
| §4/§5/§10 gate approvals | the §4, §5 and §10 asks, answered explicitly before any write | developer |
| §4 governed write (positive) | the §4 script and unconditional cleanup, only after the yes | agent |
| §5 governed write (negative) | the §5 submit, review resolution and cleanup, only after the yes | agent |
| §6 Graphify | the §6 command block — version, `built_at_commit` vs live HEAD, one live query | agent |
| §7 log sweep | the §7 `journalctl` sweep and loopback confirmation | agent |
| §7 developer's direct answer | the §7 question, answered and logged verbatim | developer |
| §8 mb-submit-memory prerequisites | the §8 command block — registered source, governor reachable | agent |
| §9 backups | the §9 listings and `sha256sum` pair check | agent |
| §10 Dream Cycle state report | the §10 `cycle_freshness` read | agent |
| §10 real Dream Cycle run | the §10 gated `gbrain dream` run and mandatory post-run verification, only after the yes | agent |
| `gh repo create` remediation | the §1 ADR sequence for a source missing a GitHub remote | developer |
| `graphify update` remediation | the §6 stale-graph remediation, run from the repo root | developer |
| Works | the developer invokes the skill; a run reaching the §11 roll-up with the honest verdict is the evidence | developer |

## Do not

- Do not treat the run as an accumulating audit — remediate in place, per section, as findings occur.
- Do not gate a clean section on developer confirmation — only trouble and heavyweight gates stop the run.
- Do not run §4, §5, or §10's real-write path without an explicit yes, ever, regardless of how healthy the rest of the system looks.
- Do not execute the Cupcake binary or live-test a Cupcake rule — developer-only, permanently.
- Do not touch PostgreSQL Instance A / `pdlf` in any check.
- Do not auto-run the ADR's `gh repo create` remediation — developer-approved first (it creates a real GitHub repository).
- Do not hold section results unwritten — append to the report file as each section closes.
- Do not auto-trigger this skill — invocation is explicit only.
