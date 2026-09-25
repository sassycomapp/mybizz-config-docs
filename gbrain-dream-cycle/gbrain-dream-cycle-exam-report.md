---
title: "gbrain-dream-cycle-exam-report"
doc-id: "gbrain-dream-cycle-exam-report"
---
# GBrain Dream Cycle — Exam Report

Run #1 — **first formal plan-driven exam** (2026-09-14). Plan:
[[gbrain-dream-cycle-exam-plan|Exam Plan]] (bootstrap — no prior report). Step-0: **PASS**
— 5/5 hash pairs match via the approved glob form (`cupcake` f5e8489cf60a8abc ·
`dream-cycle` 3573929bebb1b92e · `gbrain` 58dc0b52cbc86d72 · `memory-governor`
c40df342d523aa59 · `postgresql` b41a3e117dee1809); all five Installed suites carry
the seven files; all register spec docs exist; no open run blocks. One guard
denial at step-0 (token-literal command form — known class, learning #1) —
honored; re-run in the approved glob form. Detection only — Tiers 0–2; Tier 3
locked. Scope boundary honored (parent gbrain / postgresql / Graphify domains
cross-referenced, never re-probed).

## Verdict: HEALTHY — all checks PASS, zero live defects, zero open findings except F-2 (backup second-lane decision pending); 1 method improvement graduated into the skill

The dream cycle is working well. Every check verified the recorded configuration
state; the one unplanned event (F-1) was caused by the exam's own probe, was
absorbed without damage, and produced a standing improvement to the exam method.

## Tier 0 — Invocability: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| DC0-1 | Version | 0.46.1.0 | `gbrain 0.46.1.0` (upgrade banner 0.50.0.0 — recorded open item, never on newness) | PASS |
| DC0-2 | Autopilot absence | crontab empty; script + log absent | Crontab empty; both `~/.gbrain/autopilot-*` artifacts absent | PASS |
| DC0-3 | Schema pack | `gbrain-everything@1.0.0+7021205a`, only pack | Exact (30 page types / 12 link types; "no successor declared") | PASS |

## Tier 1 — State conformance: PASS with 2 deferred (developer bundle issued)

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| DC1-1 | Anthropic credential present (env-only, name-only) | present | `present`. Validity curl: **guard-denied** (sensitive-data + outbound-network classes) → developer bundle | PASS (presence) / DEFERRED (validity) |
| DC1-2 | Trigger surfaces exist | `--phase --source --json --dry-run` | `--dry-run --json` in help; `--source` verified via bare parse-fail ("missing value" — correct usage line); `--phase` existence proven live (F-1 — the flag processed, cycle started). Help text lists only 2 of 4 flags — cosmetic abbreviation, spec row remains accurate | PASS |
| DC1-3 | `mcp_surface` key absent in config | absent (verbs on default surface) | Sensitive-data guard class — **developer bundle** (agent-side corroboration: memory verbs callable on the MCP surface, observed live this session) | DEFERRED |
| DC1-4 | `code` extractability | `extractable: false` | `extractable: false` (schema explain-type, pack `gbrain-everything`) | PASS |
| DC1-5 | Suite completeness | 7 files | 8 files present (7-file standard + skill source) | PASS |

## Tier 2 — Functional proof (present ≠ working): PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| DC2-1 | Single-phase probe `--phase orphans --json` | ok/warn with count; `.phase` field; reports, does not fix | Exit 0, 43ms; `.phase` works exactly as documented; **`warn` — 1,008 orphan pages of 1,886** (344 excluded; was 1,177/1,755 on 2026-09-06 — moved with content, LE-1 explainable); totals all zero (reported only) | PASS |
| DC2-2 | Discipline probe `eval suspected-contradictions --query` (real topic) | Runs; bare form fails exit 2 (query required) | Exit 0, 59.6s, $0.0329: **0 contradictions, 4 findings** (no_contradiction 6 pairs; 0 judge errors) — the mandatory ungovernable-writer compensation tool works | PASS |

## Findings

1. **F-1 — Exam-method incident, no live damage (new learning).** A bare
   `gbrain dream --phase` probe (improvised during DC1-2 detection, not in the
   plan) did **not** parse-fail — it **started a full dream cycle**; the probe's
   output pipe (`head -3`) then killed it via SIGPIPE at `extract_facts` start.
   Consequences verified live: no process remained; counters 1,886/5,610, 100%
   embedded (vs last recorded 1,885/5,608 — +1/+2 benign partial work); **no
   freshness stamps, no stale locks, no corruption** (the stamping mechanism
   held: uncompleted cycles stamp nothing — W-3 confirmed); extract_atoms
   backlog 201 pending (queue state, processed on the next real cycle). Doctor:
   db checks green; brain-score warnings are the known orphan/link backlog (W-2).
   **Recommended repair: none to the live system.** Graduate into the skill:
   hard rule — *never probe `--phase` bare; only `--source` parse-fails safely;
   never pipe live dream output to a truncating consumer.*
2. **F-2 — DB-only concept pages outside file-lane backup coverage (quirk for
   governance, not a defect).** Doctor WARN: 122 DB pages have no backing file
   and sit outside every declared db_only path — sample: dream-synthesized
   `concepts/...` pages. The tool's derive-phase defaults cover
   `life/events/atoms/extracts/dream-cycle-summaries/` but **not `concepts/`** —
   so dream-synthesized concept pages are invisible to file-lane
   backup/recovery. Mitigation is a config change (declare the prefix under
   `storage.db_only` in gbrain.yml) — developer-run, never applied by this
   exam. Flagged for decision.
3. **F-3 — Watch items verified as recorded:** W-2 orphan backlog live
   (1,008/1,886 — content-hygiene debt, by design unmanaged by the cycle); W-3
   `cycle_freshness` FAIL persists exactly per the documented mechanism (a
   completed dream stamps only via a real sync — NOT a defect); W-1 pending the
   developer bundle's config check. `sync_freshness` staleness noted — parent
   gbrain module's domain (separate `gbrain sync` concern, not a dream finding).

## Tier 3 — Deep pass: EXECUTED (developer unlocked at run gate, 2026-09-14)

**DC3-1 — full dream cycle + complete post-run verification: PASS.**

| Step | Expected | Actual |
|---|---|---|
| Pre-capture `gbrain stats` | counters recorded | 1,886 pages / 5,610 chunks / 100% embedded |
| Full cycle `gbrain dream --json` (file-captured) | EXIT 0 | **EXIT 0**, ~13 min wall |
| Per-phase table (`.phase` field) | every phase ok / legitimately skipped / warn-with-count | **11 ok · 12 skipped (legitimate: nothing dirty to lint/sync; nothing to extract/consolidate/enrich) · 1 warn (orphans)** · **0 failures, 0 bare counts** |
| Real-work delta | counters move, explainably | **Pages 1,886→2,010 (+124); chunks 5,610→5,734 (100% embedded); extract_atoms 90 atoms from 36/36 pages (345s — the 201-page backlog drained); synthesize_concepts 126 concepts (T1=7 T2=11 T3=108, 256s); propose_takes 34 new proposals (152s); emotional weight recomputed on 2,009 pages; orphans 1,008→1,039 (+31 — new pages not yet linked, LE-1 point-in-time confirmed)** |
| Doctor | freshness per documented mechanism; no stale locks | `cycle_freshness` FAIL persists — **W-3 mechanism confirmed exactly**: the cycle's sync phase was skipped (nothing dirty at start) so no stamps; `sync_freshness` staleness = parent gbrain module's domain (separate `gbrain sync` concern, not a dream finding); **stale_locks OK, embed_staleness OK** |
| Suspected-contradictions on deepened content | runs; findings reviewed | 0 contradictions / **1 temporal_supersession (benign — expected class)** / 9 no_contradiction; 0 judge errors; $0.0235; n=1 caveat noted (tool's own statistical honesty) |

**Real work proven — "completed" AND "worked" established separately, per doctrine.**

**DC3-2 — upgrade decision:** policy = never on newness, only on check failure. **No check failed** (all green including the live full cycle). Recommendation recorded: stay at 0.46.1.0; the upgrade (0.50.0.0) remains available for a deliberate coordinated cutover whenever the developer chooses — DB backup prerequisite now satisfied (2026-09-13 dump).

## Deferred (runner attribution)

- ~~DC1-3~~ — **developer-verified 2026-09-14: `jq 'has("mcp_surface")' ~/.gbrain/config.json` → `false`** (exact command recorded) — key absent, verbs on the default surface → **PASS**
- ~~DC1-1b~~ — **developer-verified 2026-09-14: validity curl → `message`** (exact command recorded) — credential valid → **PASS**; DC1-1 fully closed
- **Tier 3** (DC3-1 full cycle + DC3-2 upgrade) — unlock-gated; decision deferred by the developer to the end of the build-then-run sequence

## Guard layers

Two denials this run, both honored absolutely, both known classes: (1) step-0
token-literal command text (exec-protection) — approved glob form used instead;
(2) DC1-1 validity curl (sensitive-data + outbound-network allowlist) →
developer bundle. No denial was retried through an alternate path.

## Developer-run items — bundle (ONE request)

```bash
# (a) DC1-3 — mcp_surface key absence (expect: no output / key not found)
jq 'has("mcp_surface")' ~/.gbrain/config.json

# (b) DC1-1b — credential validity (expect: "type":"message" = valid; 401 = dead key)
curl -s https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" -H "content-type: application/json" \
  -d '{"model":"claude-haiku-4-5-20251001","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}' \
  | jq -r '.type // .error.type'
```

Results recorded verbatim, tagged developer-verified, alongside the exact
commands — so the next run can re-request precisely.
