---
title: "mb-archify-scope-exam-report"
doc-id: "mb-cf78ddcd"
updated: "2026-10-08"
---

# mb-archify-scope — Exam Report

**Verdict: mb-archify-scope HEALTHY+FLAGS → all findings resolved at the 2026-10-08 gate — Tiers 0–3 all executed, 16/16 checks PASS (run #1, plan-driven bootstrap).** Zero `DOWN`/`UNHEALTHY` findings. The one spec-side `DRIFT` (F-1: repo spec §File conventions flat vs live nested) was approved at the gate and applied the same day: three locations corrected, installed copy re-synced body-to-body, subject pair `c22bef6a8c635424` re-verified. F-2 (register hash-column re-record) applied in the close-out register write. AS1-10 reclassified to runner A (approved read-only tool form) at the gate; the exam skill re-installed, pair `6792a8cf100d6e5a`. The subject skill system is working well: repo↔installed bodies byte-identical, frontmatter discipline intact, discoverable, GBrain-registered, integration facts standing, run artifacts present, and the Phase-8 contract now carries one path shape.

- Run: #1 formal (bootstrap — plan synthesized from the spec alone; no prior report/log/learnings, expected not silence)
- Executor: `mb-config-mb-archify-scope` (installed copy, body hash `6792a8cf100d6e5a`, pair verified both sides) with the [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-plan.md) in hand
- Step-0 (config-manager): PASS — 18/18 installed pairs probed via the approved glob form, 16/18 MATCH (2 estate observations recorded, not self-healed); suites 18/18 COMPLETE-8; register spec-doc paths 18/18 for Installed rows (Deferred 1/1; Retired 6/6 absent as recorded); target log bootstrap-clean. Recorded: [[[mybizz-config-docs:mb-config-manager/config-manager-log|Config Manager Log]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-log.md)
- Evidence: `/tmp/opencode/mb-archify-scope-run1/`
- Guard denials honored (no retries, no reshapes): sessions-provenance page read denied in Phase 0 (sensitive-file class); suite edit refused post-grant-expiry 2026-10-08 08:26 UTC (grant class — fresh grants issued by the developer across the run: suite 6+2+5 / config-manager 2 / install 2 / repo 2 / subject-copy 2)

## Tier 0 — Invocability (3/3 PASS)

| ID | Expected | Actual | Result |
|---|---|---|---|
| AS0-1 | Installed copy present at `~/.config/opencode/skills/mb-archify-scope/SKILL.md` with functional frontmatter | Present — 4-line frontmatter (`---`/`name: mb-archify-scope`/`description`/`---`), body intact from H1 | PASS |
| AS0-2 | Skill name in the running session's discoverable skill surface | Listed (`mb-archify-scope`) | PASS |
| AS0-3 | Suite spec doc present, non-empty | `mb-archify-scope-config.md` present (91 lines at probe time) | PASS |

## Tier 1 — State conformance (10/10 PASS after gate application)

| ID | Expected | Actual | Result |
|---|---|---|---|
| AS1-1 | Repo = `.git/` + `mb-archify-scope.md` only | Exactly that (config §Canonical locations) | PASS |
| AS1-2 | Body-hash pair identical (pinned awk; both files open with `---`) | `5cc7d745ed4d6c7d` at probe; `c22bef6a8c635424` both sides after the gate-approved F-1 correction + body-to-body re-sync | PASS |
| AS1-3 | Recorded sizes | 14,228/14,356 B at probe (spec exact); after F-1: 14,339/14,467 B — spec §Canonical locations refreshed at the gate | PASS |
| AS1-4 | Repo: doc frontmatter (`title`/`doc-id` `mb-ab9e047b`/`updated`); installed: skill frontmatter (`name`/`description`) | As designed (spec `updated` re-stamps at commit per the hook) | PASS |
| AS1-5 | GBrain source `mb-archify-scope`, federated, `/mnt/c/mybizz/mb-archify-scope`, 1 page | Match (host CLI `sources list`; last-sync timestamp volatile, not checked) | PASS |
| AS1-6 | Suite 8 files (config, exam-plan, exam-report, log, learnings, explainer, reference, exam-skill) | 8/8 (step-0 COMPLETE-8) | PASS |
| AS1-7 | Register row: `Installed` + body hash + install date | Row complete; hash column re-recorded at close-out (`6792a8cf100d6e5a` — see F-2 resolution) | PASS |
| AS1-8 | Integration mirror-facts: archify-config §Scoping skill component · archify-reference front-of-pipe note · archify-explainer "Why scoping comes first" · archify-skill AR2-3 | All four present | PASS |
| AS1-9 | Run artifacts per Run history: `archify/output/memory-ecosystem-project/` with scope card, machine header, learnings file | All present (nested convention) | PASS |
| AS1-10 | No `mb-archify-scope`-specific Cupcake rule in either lane | Zero archify-specific rules (compiled-policy lane + rule-documentation lane; only matches were this run's own grants-data records). Executed via the approved read-only tool form — classification confirmed at the gate (G-3); skill updated + re-installed | PASS |

## Tier 2 — Functional proof (4/4 PASS; read-only probes only)

| ID | Expected | Actual | Result |
|---|---|---|---|
| AS2-1 | Frontmatter parses as exactly `name` + `description`; body intact from H1 — nine phases, abort conditions, machine-header JSON, layout budgets | Keys: `name`, `description` (2); nine phase headings; all sections present | PASS |
| AS2-2 | Behavioral discipline intact: read-only-until-Phase-8 · Phase-7 hard gate ("hard stop") · abort-and-reshape · probe declared-not-executed ("Declared here, executed there") · sync rule ("Change this file and the installed copy together") · first-write rule (line-wrapped, verified) | All present (counts: 1/1/2/1/4/1/1) | PASS |
| AS2-3 | Repo live: HEAD resolvable, tree clean, origin GitHub-backed | Clean; HEAD `245cda6`; origin `github.com/sassycomapp/mb-archify-scope.git` | PASS |
| AS2-4 | Sync discipline documented: body-to-body procedure + never-plain-copy rule | Both documented (reference §Keeping spec and installed copy in sync + §Do not) | PASS |

## Tier 3 — Deep pass (executed developer-unlocked; 2/2 PASS)

| ID | Check | Result |
|---|---|---|
| AS3-1 | **Full spec-vs-live conformance walk** — every config table located live: §Identity (skills-catalog row `mybizz / archify / mb-archify-scope / Support / Both / OK` — exact; invocation `model-invoked` with trigger branches in the installed description — exact; Built 2026-09-15 corroborated by git history; the session-page corroboration read was guard-denied, sensitive-file class — recorded, not retried); §Canonical locations (exact; sizes/date cells refreshed at the gate post-F-1); §GBrain registration (exact; last-sync volatile); §Structure nine phases (9/9 phase headings + all nine gate criteria located in the spec text); §Integration (all rows located: /archify header consumption, failed-probe-returns-to-Phase-5, archify suite docs, AR2-3, run artifacts, provenance pages — facts page + session page exist; first-run learnings file present); §Cross-cutting (Cupcake — AS1-10; Memory Governor — ordinary sync corroborated via the GBrain source registration; security-global caution present in the explainer; spawn capability — zero spawn/sub-agent phrasing in the repo spec); §Run history (one run, artifacts match); §Open items (1 confirmed open → resolved at gate; 2–4 standing) | **PASS** — every spec claim located; every live delta itemized (only delta: the F-1 convention drift, resolved at gate) |
| AS3-2 | **Phase-8 contract mechanism deep proof** — `memory-ecosystem-header.json` parses as JSON; 15/15 spec-schema fields present; `status: approved`; all four developer-approved items match card↔header byte-for-content: type (`architecture`), node inventory (9/9 ids + roles textual match), main path (5/5), corridor plan consistent (12 header corridors vs card lanes); `deferred_to_cards` 5/5; `quality_gate` string exact; abort conditions 3/3; render evidence complete (render.html + probe.json + draft.json + 4 visual-check sidecars + visual-check html/json). One observation: `layout_budget_read` deviates from the schema's example shape (`<renderers/<type>/README.md>`) because architecture has no renderer README — free-pos placement documented in card + header; recorded, not a defect | **PASS** |

## Findings — all resolved at the 2026-10-08 gate (per-item dispositions)

| ID | Class | Disposition |
|---|---|---|
| F-1 | DRIFT (spec side) — repo spec §File conventions flat vs live nested | **APPROVED + applied (G-1, option a)** — three locations corrected in one deterministic pass (§File conventions table + Phase 8 inline paths + Phase 9 learnings path; zero residual flat refs); identical body change applied to the installed subject copy (body-to-body, never plain-copy); subject pair re-verified `c22bef6a8c635424` both sides; spec §Canonical locations cells (updated date, sizes, sync state) + open item 1 + explainer open-question section refreshed in-suite |
| F-2 | Self-administrative — register hash-column re-record | **APPROVED + applied (G-2)** — close-out register write: exam-skill pair `6792a8cf100d6e5a` + run outcome + verified live 2026-10-08 |
| AS1-10 | Classification | **CONFIRMED (G-3)** — runner A via the approved read-only tool form; standing row updated in the exam skill; skill re-installed (pair `6792a8cf100d6e5a` both sides) |

## Estate observations (recorded 2026-10-08 at step-0 — not self-healed; belong to those modules' own cycles)

- mb-sysdoc-creator exam-skill pair mismatch (source `db7c198744a607db` vs installed `dc231cc6a86c8fa4`) — standing S0-F1 since 2026-10-07.
- mb-sentinel-review exam-skill pair mismatch (source `14a1b89882fbdb02` vs installed `d22c53f567f57ba4`) — NEW: its close-out commit (2026-10-07) link-rewrote the committed exam-skill source after its step-0 had verified the pair.

## Watch rows (standing)

| # | Watch item | Status |
|---|---|---|
| W-1 | Spec §File conventions flat vs live nested (spec open item 1) | **Closed 2026-10-08** (F-1 applied) |
| W-2 | Fact-ownership reduction in archify-config (spec open item 2) | Standing — developer-run separate task |
| W-3 | mybizz-config-docs has no suite register (spec open item 3) | Standing — no exam action |
| W-4 | Cupcake skills-dir ancestor-cwd case (spec open item 4) | Standing — Cupcake internals out of scope; grant-required sync discipline verified (AS2-4) and exercised live (subject re-sync under grant) |