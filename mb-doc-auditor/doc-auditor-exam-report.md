---
title: "doc-auditor-exam-report"
doc-id: "doc-auditor-exam-report"
---
# mb-doc-auditor — Exam Report

**Verdict: mb-doc-auditor HEALTHY — Tiers 0–2 all PASS on the live system (run #1, 2026-09-27, plan-driven bootstrap). Install defect in the config-management skill found and fixed in-run (F-1/S-3); suite-wording gap approved and applied at gate (F-2, re-hash verified). Gate 2026-09-27: F-3 corrected, F-4 accepted-known-drift, Tier 3 stayed locked.**

Run header: plan [[doc-auditor-exam-plan|Exam Plan]] (bootstrap, hand-written); run date 2026-09-27; executor: config-manager agent cycle; expected values read fresh from [[doc-auditor-config|Configuration]] at run start. Evidence files: `/tmp/opencode/doc-auditor-run1/` (step-0 pairs, hashes, per-probe captures, byte-proof).

## Step 0 — config-manager self-validation (recorded in [[config-manager-log|Config Manager Log]], 2026-09-27)

Estate pairs probed for 16 of 17 Installed rows (mb-doccycle source deleted — the developer's own uncommitted deletions, stated in session, no action):

- doc-auditor pair BODY-ID PASS post-S-3 (source `48ef240f94d482a2` / installed `92d78bfedd1fd42b`).
- doc-maintainer installed copy byte-identical to its corpus source (`bfa7a0d95a61fdbd` both sides → installed copy carries corpus frontmatter, undiscoverable) — same defect class as F-1; out of scope per developer 2026-09-27, recorded only.
- 14 remaining pairs: source hashes match register columns and installed hashes match recorded re-hashes, but body-identity fails beyond frontmatter — post-retrofit wikilink conversions in sources absent from installed copies (sample diff: gbrain). Class: source-edited-not-reinstalled → **stale GAP ×14, estate-wide, systemic, pre-dates this run**; extends the doc-maintainer run's F-2 note (retrofit touched bodies too, not frontmatter only). Recorded, NOT self-healed — config-manager-level gate item.
- Register path-cell finding: row 38 spec-doc cell `doc-maintainer/doc-maintainer-config.md` does not resolve as written; actual `mb-doc-maintainer/doc-maintainer-config.md` exists. Gate item (config-manager level).
- Suite completeness: all suites at the 8-file standard; spec-doc paths 15/17 resolve (two above); doc-auditor log had no prior run row (bootstrap, expected). One-run-at-a-time: doc-maintainer run #1 sits gate-pending (developer-held); this run instructed 2026-09-27.

## Tier 0 — Invocability (runner A)

| ID | Expected | Actual | Result |
|---|---|---|---|
| DA0-1 | Subject skill present with functional frontmatter | Present; `name: mb-doc-auditor` + description; hash pair source `8e0def60659e0854` / installed `42790f675a784bdd` matches spec §Identity | PASS |
| DA0-2 | All five tools compile | `py_compile` clean on scope.py, runlog.py, gbrain_reader.py, record.py, audit.py (cache redirected to /tmp — repo untouched) | PASS |

## Tier 1 — State conformance (runner A)

| ID | Expected | Actual | Result |
|---|---|---|---|
| DA1-1 | Origin `github.com/sassycomapp/mb-doc-auditor.git`; HEAD `aa91ff7`; tree clean | All three exact | PASS |
| DA1-2 | Source `8e0def60659e0854` / installed `42790f675a784bdd`; body byte-identical from H1 | Both hashes exact; cmp from H1 identical | PASS |
| DA1-3 | 22/22 tests pass | 22/22 OK (1.381s) | PASS |
| DA1-4 | 8-file standard + record co-resident | 9 files present (8 + `doc-auditor-records.md`) | PASS |
| DA1-5 | Record exists; two-field frontmatter; register row Live | All three (register-local row `doc-auditor-records`, Live) | PASS |
| DA1-6 | Register rows for the suite docs | Rows present for all 9 suite files (config/reference/explainer + records + 5 exam set) | PASS |
| DA1-7 | Contract exists; two-field frontmatter; register row | All three (row `gbrain-doc-contract`, Live) | PASS |
| DA1-8 | Scope authority present, readable; parses live | Present at the locked path; parsed live in DA2-1 (in_scope=true) | PASS |
| DA1-9 | Run-log evidence input present | Present, 47 lines (`doc-maintainer-run-log.md` — the §10 hard-wired path) | PASS |
| DA1-10 | No `mb-doc-auditor` row in gbrain sources list | 17 sources live; no mb-doc-auditor row — matches spec open item #2 state | PASS |

## Tier 2 — Functional proof (runner A; read-only; byte-proof clean)

| ID | Expected | Actual | Result |
|---|---|---|---|
| DA2-1 | Exit 0; authority parses live; paths enumerate with exclusions | validate: in_scope=true, in_roots=true, excepted=false, exit 0; paths enumerated (498-line capture) | PASS |
| DA2-2 | Evidence rows for the real log; graceful absent-path message | Real log: status ok, 34 events parsed by kind; absent path: "no maintenance history available", exit 0 | PASS |
| DA2-3 | Exit 0; JSON findings for real files; no byte changed | Exit 0; JSON: 9 files, frontmatter 9 ok / 0 findings, links 6 missing (watch note, W-1), register check 3 ROW_MALFORMED (lines 208/237/245), missing_registrations 0; hash-proof: zero bytes changed | PASS |
| DA2-4 | Exit 0; zero bytes changed | **Zero bytes changed (hash-proof ✓)**; exit=1 with refusal-class residuals (236 obsolete-rows-outside-library-root, human judgement; applicable fixes 0) — the reference documents exit 1 with residuals as the designed semantics for a non-library-root audit; the skill's "Exit 0" cell is inconsistent with it → finding F-2 | PASS-with-finding |
| DA2-5 | Source list returned; failure → Can wait | Source list returned (17 sources), exit 0 | PASS |

## Findings

| # | Class | Evidence | Recommended repair | Risk | Status |
|---|---|---|---|---|---|
| F-1 | DRIFT/GAP (install discipline) | Installed copy was byte-identical (13163 bytes both sides) — corpus frontmatter on the installed copy; OpenCode did not discover the skill (absent from the session skill list while 14 sibling `mb-config-*` skills present) | **S-3 applied 2026-09-27** under the approved plan: functional frontmatter (`name: mb-config-doc-auditor` + description), body byte-identical from H1 (cmp-verified); hash pair source `48ef240f94d482a2` / installed `92d78bfedd1fd42b`; register note corrected; log row appended | None (fixed) | CLOSED in-run |
| F-2 | GAP (suite-internal wording) | Skill DA2-4 expected cell said "Exit 0"; reference §Tool commands documents exit 1 with refusal residuals as designed for non-library-root audits; live dry-run: zero bytes changed, exit 1, 0 applicable fixes | Amend the DA2-4 expected cell (agent-healable suite file) to match the reference's exit semantics; if applied: re-install + re-hash + register hash update per install discipline | None live — the tool behaved per its documented contract | **APPROVED + applied 2026-09-27** (gate): cell amended in source, re-installed dual-format, body-identical from H1; hash pair source `5d781c96344f6e05` / installed `c9a7d735de3a0625`; register row updated |
| F-3 | GAP (register path cell — step-0 carry, config-manager level) | config-manager-register row 38 spec-doc cell does not resolve as written; actual location verified | Correct the path cell (the register is the config-manager's own file) | Navigation only | **APPROVED + corrected 2026-09-27** (gate) |
| F-4 | stale GAP ×14 estate-wide (step-0 carry, config-manager level) | 14 pairs body-drift beyond frontmatter — post-retrofit wikilink conversions in sources, absent from installed copies (see Step 0) | Developer decision at the config-manager level (re-baseline vs format exemption vs re-install campaign; re-install strips discovery frontmatter — not recommended as-is) | Pre-existing; no doc-auditor impact | **APPROVED: accepted known drift, resolve per-system at each system's next exam cycle** (gate 2026-09-27; install-discipline note amended) |

## Deferred items and runner attribution

- Tier 3 (DA3-1/2/3): runner D (developer), **stayed locked at gate (2026-09-27)** — executes at a deliberate future session if unlocked.
- Guard-forbidden classes this run: none encountered. Environment note (transparency): Cupcake was disabled by the developer mid-run (2026-09-27) after two mg-grant slips registered reads but not writes on the install path and the disabled plugin remained active until an OpenCode restart; the run proceeded per developer instruction. All probes were read-only; the only write was the S-3 install under explicit developer slips and plan approval.

## Watch rows (plan §2)

- W-1 (nested-corpus convention): new evidence — the bounded-root check reports 6 "missing" links; all are cross-suite wikilinks (`[[config-manager-log]]`, `[[config-manager-reference]]`, `[[config-manager-explainer]]`, …) whose targets exist elsewhere in the corpus but not under the bounded root. Consistent with spec open item #1 (developer decision pending); no convention decided by the exam.
- W-2 (GBrain source registration): DA1-10 verified the not-registered state matches the spec — no divergence.
- W-3 (record's carried items): record artifact verified (DA1-5); the check probe's 3 ROW_MALFORMED register rows (lines 208/237/245) align with the record's carried "9 pre-existing legacy-schema register rows (Can wait)" class. No new work queue created.
- W-4 (discovery confirmation): S-3 corrected the frontmatter; confirmation lands at the next session start (this session's skill list predates the fix).
