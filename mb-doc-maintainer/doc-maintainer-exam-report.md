---
title: "doc-maintainer-exam-report"
doc-id: "doc-maintainer-exam-report"
---
# mb-doc-maintainer — Exam Report

**Verdict: HEALTHY.** Run #1 formal (bootstrap), 2026-09-25, plan-driven,
**Tiers 0–3 executed in full** (Tier 3 unlocked at the gate per developer
instruction; DM3-1a–g and DM3-2a–e all executed with evidence). Zero DOWN /
UNHEALTHY / DRIFT on the subject system. Gate dispositions recorded: F-1
repaired in-run, F-2 re-baselined per approved option (a), F-3 delegated to
maintainer work, F-5 (new, minor) open for decision, F-4 standing close-out.
Pipeline proven live: watcher running, single instance, crash-restart verified,
18 real events drained end-to-end with byte-level discipline proofs.

---

## Step 0 — self-validation (recorded in config-manager-log.md)

| Check | Result |
|---|---|
| Installed-skill hash pairs (16 systems incl. this one, approved glob form) | **16/16 PASS vs register** (installed side intact) |
| Suite skill-sources vs register hashes | **15/15 FAIL — systemic.** Cause (verified on the cupcake sample): the 2026-09-24 corpus retrofit rewrote every suite skill-source's frontmatter to the corpus two-field format (`title`/`doc-id`), while installed copies retain functional `name`/`description` frontmatter. Class: source-edited-not-reinstalled → stale GAP × 15, **retrofit-caused**, gate item F-2. Not self-healed |
| Suite completeness (7-file standard, 15 Installed systems) | PASS (see table below) |
| Register spec-doc paths | PASS — all exist |
| Target's last log run-row disposition | None required — bootstrap (no prior run) |

## Tier 0 — Invocability (all PASS)

| ID | Expected (source) | Actual | Result |
|---|---|---|---|
| DM0-1 | Task state `Running` (config §Watcher) | `Running` | PASS |
| DM0-2 | Exactly one watcher process | Count = 1 | PASS |
| DM0-3 | Queue dir + run-log exist (config §Storage) | `True` / `True` | PASS |

## Tier 1 — State conformance (all PASS except DM1-9 GAP)

| ID | Expected (source) | Actual | Result |
|---|---|---|---|
| DM1-1 | Origin `github.com/sassycomapp/mb-doc-maintainer.git`; HEAD `9dae0db`; tree clean (config §Identity) | All three exact | PASS |
| DM1-2 | Installed subject skill byte-identical to source (hash pair, config §Identity) | `40a8b16ce4959f0b` = `40a8b16ce4959f0b` | PASS |
| DM1-3 | Tools compile; 40/40 tests (config §Component layout) | compile-ok; unittest `OK` | PASS |
| DM1-4 | AtLogOn; time limit 0; restart 3/1-min; battery-safe (config §Watcher) | `MSFT_TaskLogonTrigger`; `PT0S`; 3/`PT1M`; `False/False` | PASS |
| DM1-5 | Run-log exists, frontmatter compliant, register row Live (config §Storage/§Register) | compliant `True`; row count 1 | PASS |
| DM1-6 | Source registered, federated no, lag ≈ 0, 100% embed, 1 page (config §GBrain) | `0s / 100% / idle / 1` | PASS |
| DM1-7 | 8-file suite standard (config §Identity — suite) | 9 files = 8 standard + spec-recorded run-log co-resident | PASS (noted) |
| DM1-8 | Contract exists, frontmatter compliant, register row (config §Identity) | All three | PASS |
| DM1-9 | Register rows for the three suite docs (spec open item #1) | 0 rows | **GAP → F-1** |
| DM1-10 | Every queued event well-formed (`path`+`kind`) | 14/14 well-formed | PASS |

## Tier 2 — Functional proof (all PASS)

| ID | Probe | Actual | Result |
|---|---|---|---|
| DM2-1 | `frontmatter.py check` executes against the contract file | exit 0, `compliant: True` (evidence captured at DM1-8) | PASS |
| DM2-2 | Watcher functional + self-exclusion: 14 queued events; none reference the run-log or `watcher.log` | 0 self-events | PASS |
| DM2-3 | `register.py check` on the config-docs register | Tool executed; 238 rows; **3 ROW_MALFORMED findings (lines 208/237/245 — legacy unescaped-pipe titles, pre-existing corpus rows)** | PASS (tool works; findings → F-3) |

## Tier 3 — Deep pass (developer-unlocked at the gate 2026-09-25; executed in full — every sub-check ran, evidence in `/tmp/opencode/tier3-evidence/`)

**Constraint honored: `anvil.yaml` was never read, written, or touched — the class rule was live-tested against the real `C:\dev\dev-mb-3-cs\mb-3-cs` folder (existence check only, via the watcher's own logic).**

| ID | Probe | Actual | Result |
|---|---|---|---|
| DM3-1a | Pre-state capture per event | 18/18 event JSONs + per-doc frontmatter/hash/register-row states captured before any action | PASS |
| DM3-1b | Per-event walkthrough | 18 events processed individually; per-doc tool evidence; register repairs applied as gate-approved | PASS |
| DM3-1c | §20 checklist item-by-item | Verified per affected document (frontmatter two-field ✓, links resolve ✓ — 32/32 wikilinks ok, register current ✓, safe repairs automatic ✓, zero corpus-wide work ✓) | PASS |
| DM3-1d | Register four-event discipline under live load | 9 creation rows appended (8 doc-maintainer suite docs + config-manager-log, discovered missing at pre-state); content edits moved nothing; register 252→263 lines, append-only in-order | PASS |
| DM3-1e | Run-log append-only byte-proof | prefix sha256 identical (`efa19b3e29179488`); 1798→3792 bytes; 10 rows appended covering all 18 events | PASS |
| DM3-1f | Queue drain verification | 18/18 event files removed to evidence; queue 0; no double-processing | PASS |
| DM3-1g | Termination discipline | Invocation ended; no work queues created; findings reported only | PASS |
| DM3-2a | Exclusion suite, live fixtures | Exactly 1 event (positive control); silent: WIP, `temp-*`, `tmp-` prefix, dotfolder, `.git`, non-md, zero-content, **and the real anvil.yaml class rule** | PASS |
| DM3-2b | Coalescing under load | 6 rapid saves → exactly 1 event (`Created+Changed` coalesced) | PASS |
| DM3-2c | Lifecycle churn (create→rename→rename-back→delete in one window) | Net state correct (single deletion for the surviving path, no phantom creation) **but a redundant second deletion event fired for the transient rename path** | PARTIAL → F-5 |
| DM3-2d | Crash-restart resilience | kill → 0 processes → restart proceeded past the mutex (no abandoned-mutex block) → duplicate launch refused by the single-instance guard → queue persisted across restarts | PASS |
| DM3-2e | Scope authority read live | v2 authority with a new exception → excepted path produced no event; positive control produced events | PASS |

**F-5 (new finding, from DM3-2c):** rename-back churn produces a redundant second event for the transient path (its entry retains only `[Renamed]` and promotes as a deletion of a file that never durably existed). Harmless — the maintainer's deletion handler no-ops on unregistered, unreferenced paths — but it is avoidable noise. Options: (a) accept as known noise, record in the suite; (b) harden the coalescing layer to drop entries whose only evidence is a rename-away. Developer decision at close-out.

## Gate dispositions (2026-09-25, recorded)

| Item | Disposition |
|---|---|
| F-1 (suite-doc register rows) | **Approved** — repaired by the maintainer's own invocation during DM3-1 (9 rows appended, including config-manager-log discovered missing at pre-state) |
| F-2 (systemic hash divergence) | **Approved option (a)** — register hashes re-baselined to post-retrofit sources (15/15 updated); dual-format convention recorded in the register's install-discipline note |
| F-3 (3 malformed register rows) | **Relegated to maintainer work** (the register tool exists for exactly this; not exam work) |
| F-4 (uncommitted corpus edits) | **Acknowledged** — standing close-out (developer commit+push, then sync+embed) |
| Tier 3 | **Unlocked and executed in full** (DM3-1a–g + DM3-2a–e above); F-5 recorded for decision |

**Final verdict: HEALTHY.** Tiers 0–3 executed in full; zero DOWN/UNHEALTHY/DRIFT; F-1/F-2 resolved in-run per approved dispositions; F-3 delegated; F-5 open for developer decision (accept-as-noise recommended); F-4 standing close-out.