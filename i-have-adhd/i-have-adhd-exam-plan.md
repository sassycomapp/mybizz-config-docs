---
title: "i-have-adhd-exam-plan"
doc-id: "i-have-adhd-exam-plan"
---
# i-have-adhd — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager before
each run from: [[i-have-adhd-config|Configuration]] (spec), the last [[i-have-adhd-exam-report|Exam Report]],
[[i-have-adhd-log|Log]] (events since last run), [[i-have-adhd-learnings|Learnings]]. Consumed by
the skill at run time; rewritten at the start of the following cycle. The file is
live; its contents are transient.

**This first plan is hand-written** (emulation of the established architecture): it
also serves as the format template. The **standing check inventory lives in the
skill** ([[i-have-adhd-skill|I Have Adhd Skill]], born-with-inventory); this plan carries
run-specifics and references. Once verified by a run, future plans carry
run-specifics + references only.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap) |
| Run date | set at execution |
| Prior report | none — placeholder present; missing prior report = expected, not silence |
| Step-0 result | recorded at execution |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request) | (a) upstream live-state verification (GitHub repo: activity, stars, publisher, HEAD match vs installed bundle) — outbound-network guard class, and the developer decision was to keep upstream unverified pending explicit ask; (b) any check whose command text the guards deny |
| Expected-value source of truth | [[i-have-adhd-config|Configuration]] — read fresh at run start; never rely on remembered values |
| Scope boundary | `mb-config-opencode` owns OpenCode version, global-config consolidation, plugin load-once, MCP entry, permission posture — this exam never re-probes those; it touches `opencode.json` only for the narrow install-surface fact that no i-have-adhd wiring exists (IA1-5). GStack skills belong to `mb-config-gstack`. This component has no MCP entry, no database, no provider dependency, no scheduler — there is nothing else to boundary against |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). Recorded spec states kept under watch
(observations, not findings):

| # | Watch item (config open items) | This run's action |
|---|---|---|
| W-1 | Upstream live state unverified (open item 1): repo activity, stars, publisher identity, HEAD state | No agent probe (outbound network + developer's no-web-access decision); developer-run request item |
| W-2 | No version pin (open item 2): drift between installed bundle and upstream main unknown | Same verification as W-1; until then IA1-1 byte-level conformance is the only drift guard |
| W-3 | Update mechanism untested (open item 3): `npx skills add` overwrite behavior unknown | No agent probe (content-changing to the bundle); Tier 3 / developer |
| W-4 | Supply-chain review owed at adoption (open item 4) | Tier 3 / developer; on-disk signals already recorded as benign-looking in the spec |
| W-5 | Suite siblings populated this setup run (open item 5 — now stale: scaffold filled, exam module created) | Spec-correction flag to docs governance at the gate (exam never edits the spec) |
| W-6 | Design-mode discipline informal (open item 6) | Observation only — no probe exists for it; carried until a mechanism or policy change |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-09-19 install (bundle + symlink + slash command) | IA0-1/IA0-2/IA1-1/IA1-3 execute the install-surface conformance |
| LG-2 | 2026-09-19 always-on marker created; same-day injection evidence | IA1-2 (marker state) + IA2-1 (functional self-evidence probe) |
| LG-3 | 2026-09-20 suite build-out | IA1-6 suite completeness; run #1 closes the bootstrap |

## 5. Learnings-driven items

None — the learnings file is empty at bootstrap; entries filed by run #1 feed run #2.

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in [[i-have-adhd-skill|I Have Adhd Skill]] (Tiers 0–3). Summary:

- **Tier 0 (A) — invocability:** IA0-1 skill bundle present + frontmatter name `i-have-adhd` · IA0-2 slash command present · IA0-3 `disable-model-invocation: true` intact
- **Tier 1 (A/D) — state conformance:** IA1-1 bundle byte-level contents (SKILL.md 7,207 B/142 lines; gemini.toml 2,157 B; openai.yaml 238 B) · IA1-2 always-on marker present + empty · IA1-3 global skills symlink correct · IA1-4 exactly one activation path (no duplicate skill dir / slash command) · IA1-5 no `opencode.json` wiring · IA1-6 suite completeness (8 files + intro) · IA1-7 upstream state (D — outbound network)
- **Tier 2 (A) — functional, present ≠ working:** IA2-1 self-evidence probe — the running session's own system prompt carries the always-on ruleset block when the marker is present · IA2-2 ruleset structure conformance — SKILL.md carries the persistence clause, 10 rule headings, 6 overrides, pre-send check (read-only)
- **Tier 3 (D, locked):** IA3-1 upstream verification (W-1/W-2) · IA3-2 update-mechanism verification (W-3) · IA3-3 supply-chain review discharge (W-4)

## 7. Report requirements

The run writes [[i-have-adhd-exam-report|Exam Report]]: verdict line; per-tier tables
(check ID, expected, actual, result); findings with class + evidence + recommended
repair + risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace; failed runs never
touch the prior report; written before any pruning). Then: one run row appended to
[[i-have-adhd-log|Log]] (run-row format per [[config-manager-reference|Reference: Commands, Procedures]]);
new learnings filed.

## 8. Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items** — the skill bundle, the always-on marker, the slash
  command, and the symlink are vendor/policy surfaces; every repair is
  developer-run or proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the always-on marker (policy surface —
  presence/absence is the developer's standing decision; toggling it silently
  changes every session's output style) · the installed `SKILL.md` + `agents/`
  (vendor material — never hand-patched) · the slash-command file · the
  `~/.config/skills` symlink · any `npx skills` install/update command · any
  upstream network probe without grant
- Credentials: this component has none — no credential discipline beyond the
  estate-wide name-only rule if one is ever discovered
