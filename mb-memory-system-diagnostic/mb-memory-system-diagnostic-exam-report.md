---
title: "mb-memory-system-diagnostic-exam-report"
doc-id: "mb-201231c2"
---
# mb-memory-system-diagnostic — Exam Report

**Verdict: mb-memory-system-diagnostic HEALTHY — Tiers 0–3 all PASS on the live
system (run #1, 2026-09-28, plan-driven bootstrap). Zero live defects in the
subject suite. Gate 2026-09-28, all three findings APPROVED and applied: F-1
resolved (subject pair byte-exact after re-copy), F-2 applied (spec open items
#3/#4/#5 closed), F-3 applied (skill source recipe currency + re-install, hash
pair `b90ec20c33bf4272` both sides). Tier 3 UNLOCKED by developer instruction
same day: MS3-1 31/31 PASS, MS3-2 14/14 PASS + one cross-suite awareness note.**

Run header: plan [[mb-memory-system-diagnostic-exam-plan|Exam Plan]] (bootstrap,
hand-written); run date 2026-09-28; executor: config-manager cycle per
[[config-manager-agent|config-manager-agent.md]] + [[config-setup-prompt|config-setup-prompt]];
expected values read fresh from [[mb-memory-system-diagnostic-config|Configuration]] at
run start. Evidence: `/tmp/opencode/mbmsd-run1/`.

## Step 0 — config-manager self-validation (recorded in [[config-manager-log|Config Manager Log]], 2026-09-28)

- Hash pairs probed for 17 installed `mb-config-*` skills via the approved glob
  form (`mb-config-*/SKILL.md`). This system's pair: source
  `d3975df16f28c2f9` / installed `4418e09f0c07ee23` — matches the S-1 register
  row; body-identity from H1 verified at install (11,668 bytes). Other pairs
  recorded factually per the F-4 estate body-drift disposition (2026-09-27):
  per-system re-sync at each system's next exam cycle, not re-flagged.
- Suite completeness: 9/9 files (4 pre-existing + 5 exam set) — all carry
  two-field frontmatter with `doc-id`.
- Register spec-doc paths: all Installed rows resolve; the 4 non-resolving
  cells are Retired rows (mb-align-docs, mb-doccycle, mb-docs-manager,
  mb-wikilinks) — expected.
- One-run-at-a-time: no undispositioned run rows for this system.
- Two guard denials recorded class, honored: suite-folder writes (mg-grant
  count 12 issued by developer) and register-folder writes (mg-grant count 3).
- S-1 executed: register row added by named plan step (precedent:
  doc-maintainer 2026-09-25, doc-auditor 2026-09-26); state WIP → Installed at
  Phase 2.

## Tier 0 — Invocability (runner A)

| ID | Expected | Actual | Result |
|---|---|---|---|
| MS0-1 | Subject skill present with functional frontmatter | Present; `name: mb-memory-system-diagnostic` + description; hash pair source `f0c6b1124ab36bae` / installed `7a5928a33f26f7ec` | PASS |
| MS0-2 | Skill discoverable in the session skill surface | `mb-memory-system-diagnostic` listed in this session's available skills | PASS |

## Tier 1 — State conformance (runner A)

| ID | Expected | Actual | Result |
|---|---|---|---|
| MS1-1 | Source artifact: two-field frontmatter, doc-id = stem, `-skill.md` suffix | `title`/`doc-id` = `mb-memory-system-diagnostic-skill`; file matches | PASS |
| MS1-2 | Hash pair + body byte-identical from H1 | Hashes as above; body diff = **one leading blank line** only — identical modulo whitespace (19,681 vs 19,680 chars) | PASS-with-finding F-1 |
| MS1-3 | Suite completeness per the spec's tables + exam set | 9/9 present | PASS |
| MS1-4 | §Scope of artifact matches spec §Scope | In-scope six components; out-of-scope Instance A / Cupcake internals / outside-ecosystem — tables agree | PASS |
| MS1-5 | 11 sections, gate classes per spec §Section inventory | Sections 0–11 present (13 `##` headings incl. template + summary scaffolding); heavyweight-always §4/§5/§10; trouble-class §1/§2/§3/§6–§9 — matches | PASS |
| MS1-6 | Recorded constants verbatim | 62/62 ✓ · HIGH_RISK_TYPES + `policy` ✓ · HTTP 422 ✓ · has_database_privilege ✓ / SET ROLE prohibition ✓ · cycle_freshness ×4 + `.phase` ✓ · ≤7-day backups ✓ · `gh repo create` heavyweight ✓ · `graphify update` ✓ · journald + /tmp/opencode + tracked-file live notes ✓ | PASS |
| MS1-7 | Register-local absence (open item #1) | No rows for the suite in `register-local.md`; pending-events queue holds no events for these files (43 events, none matching) — matches spec | PASS |
| MS1-8 | GBrain ingest state per spec §GBrain integration | Suite pages live under `mb-memory-system-diagnostic/*` at the new paths; old paths deleted (2026-09-28 sync, 49 chunks). Page/chunk counts exceed the recorded 4 pages/45 chunks — expected post-sync drift (the rename commit + this build), reported factually per the exam discipline | PASS |

## Tier 2 — Functional proof (runner A; read-only)

| ID | Expected | Actual | Result |
|---|---|---|---|
| MS2-1 | Installed copy machine-parsable; exactly `name`+`description`; body intact | Frontmatter parses; two keys; body intact from H1 (F-1's single blank line) | PASS |
| MS2-2 | All section binaries present on PATH (`command -v` only) | gbrain, psql, jq, sha256sum, ss, curl, git, journalctl, graphify — 9/9 present | PASS |
| MS2-3 | Reports parent viable; folder absent per open item #3 | Parent `/mnt/c/mybizz/` present. **Folder present** — contains `memory-diagnostic-2026-09-28.md` (the live run's report). Open item #3 is therefore already closed by events; spec row stale → F-2 | PASS-with-finding F-2 |
| MS2-4 | Cross-suite constants current | postgresql-config records 62 tables all-RLS (line 112); memory-governor-config records HIGH_RISK_TYPES five categories (lines 21/107); spec Gates table matches the skill's heavyweight list (§4/§5/§10 + §1 `gh repo create` + §6 `graphify update`) | PASS |

## Findings

| # | Class | Evidence | Recommended repair | Risk | Status |
|---|---|---|---|---|---|
| F-1 | GAP (benign install-discipline deviation) | Installed subject `SKILL.md` body differed from source by exactly one leading blank line (19,680 vs 19,681 chars; identical modulo whitespace). Harmless to parsing and discovery (MS0-2 proves discovery). Artifact of the re-install copy step | Re-copy source→installed | None | **APPROVED + applied 2026-09-28 (gate)** — supersedes itself: F-3's source edits were applied first, then the pair re-copied byte-exact (hash pair `b90ec20c33bf4272` / `b90ec20c33bf4272`, byte-identical); re-exam MS1-2/MS2-1 re-run: PASS |
| F-2 | GAP (spec staleness ×3) | Spec open item #3 (report folder absent) — folder created by the 2026-09-28 live run; open item #4 (first live run not executed) — run executed 2026-09-28, full §1–§11, 10/10 sections, 7 PASS + 3 REMEDIATED; open item #5 (no `mb-config-*` module) — closed by this build's register row | Spec corrections to the open-items table | None live — the spec under-stated reality | **APPROVED + applied 2026-09-28 (gate):** items #3/#4/#5 closed with event records; spec §Identity updated (source-artifact + installed-skill rows reflect the F-3 edits + re-install hash) |
| F-3 | Observation (skill-recipe currency) | The diagnostic's own 2026-09-28 run report follow-up item 4: §2's prescribed .env-sourcing diagnostic and retired /tmp log paths no longer match the systemd/journald environment — the verified alternates were present in §3/§4 but §2's recipe block still showed the .env path | Update the skill source (§0 principle 8 added — environment currency; §2 recipe switched to the verified PGURL variable-name pattern), re-install, re-hash | Low | **APPROVED + applied 2026-09-28 (gate):** source edited, installed copy re-copied byte-exact, hash pair `b90ec20c33bf4272` both sides verified |

## Tier 3 — Deep pass (developer-unlocked 2026-09-28, "Run tier three now"; runner A executing D-tier items on explicit unlock; evidence to files)

| ID | Expected | Actual | Result |
|---|---|---|---|
| MS3-1 | Paragraph-level source-vs-spec walk: every spec claim located in the artifact, gate classes + constants traced | 31 checks across Identity/Scope/Inventory/Gates/Report/credentials/section mechanics — **31/31 PASS** (one probe-string false-negative corrected by reading: `try`/`finally` present in backtick form ×2, §4 line 262 + §5 line 301). Evidence: `/tmp/opencode/mbmsd-run1/tier3/ms3-1-walk.txt` | PASS |
| MS3-2 | Every recorded constant verified against the owning sibling suite's current state (gbrain, postgresql, memory-governor, graphify, gbrain-dream-cycle + the ADR) | 14 constants — **14/14 PASS** after correction (graphify `graphify update` remediation documented in graphify-reference lines 50/94, not the config file — probe had searched the wrong file; no conflict). One awareness note: the gbrain suite does not record the §4 tracked-file rule for `sources add` — the skill's note is newer live-verified knowledge (2026-09-28 run), no conflict; gbrain's next exam cycle may adopt it if the developer wishes. Evidence: `/tmp/opencode/mbmsd-run1/tier3/ms3-2-verify.txt` | PASS |

**Tier 3 verdict: both sub-checks PASS, zero conflicts between the diagnostic skill and the five sibling suites; one cross-suite awareness note (no action required by this exam).**

## Notes

- MS1-8 count-drift (pages/chunks above the spec's recorded 4/45): expected —
  the rename commit + this exam set joined the source after the recorded sync;
  the standing sync rule covers it. Reported factually, not flagged.
- Tier 3 stayed locked (default). Unlock decision at the gate.
- No component was live-tested beyond form checks; no credential touched; no
  G-brain write performed; Instance A untouched; Cupcake untouched.
