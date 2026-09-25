---
title: "gbrain-dream-cycle-reference"
doc-id: "gbrain-dream-cycle-reference"
---
# GBrain Dream Cycle — Reference: Invocation, Verification, Diagnostics

Companion to [[gbrain-dream-cycle-config|Configuration]] (current state, acceptance-test
record) and [[gbrain-dream-cycle-explainer|Explainer]] (reasoning, incident).
Config-management set: [[gbrain-dream-cycle-exam-plan|Exam Plan]] (transient job-spec —
read second, every run), [[gbrain-dream-cycle-exam-report|Exam Report]] (last verified
state), [[gbrain-dream-cycle-log|Log]] (chronological events),
[[gbrain-dream-cycle-learnings|Learnings]] (transient knowledge). Agent-facing.

**Invocation model:** manual, on-demand only — the scheduled autopilot was
found inert and deliberately removed (2026-09-06). Nothing runs unless you
run it, which makes the post-run verification procedure below mandatory, not
optional: an unverified dream run is an unknown-state run.

---

## Running a dream cycle

```
gbrain dream                        # full cycle, all phases
gbrain dream --source <id>          # source-scoped cycle
gbrain dream --phase <name>         # single phase (diagnosis / targeted re-run)
gbrain dream --dry-run --json       # preview — SAFE, but SLOW: exceeded 120s in-session; real phases exceed the 30s worker deadline (upstream #1972)
gbrain dream --json                 # full run with per-phase machine-readable output
```

**All 23 phases live-verified 2026-09-06**, in the exact confirmed sequence:
`lint, backlinks, sync, synthesize, extract, extract_facts, extract_atoms,
resolve_symbol_edges, patterns, synthesize_concepts,
recompute_emotional_weight, consolidate, propose_takes, grade_takes,
calibration_profile, drift, conversation_facts_backfill, enrich_thin,
skillopt, embed, orphans, schema-suggest, purge`. Phase taxonomy (verified
via doctor): 12 source-scoped, 9 brain-global, 2 mixed — full classification
in [[gbrain-config|Configuration]]'s doctor notes and [[memory-master-explainer|Master Explainer]] §4.

## Post-run verification procedure — after EVERY dream invocation

A completed run proves the sequence ended. It does **not** prove every phase
did real work — the confirmed failure modes are silent (a bare failure count
with the real error swallowed; a phase resolving zero results by design).
Verified end-to-end on the 2026-09-06 acceptance run. Verify in this order:

1. **Capture per-phase output, not the summary.** The per-phase field is
   **`.phase`** (not `.name` — the previously documented `.name` recipe
   silently matched nothing):
   ```bash
   gbrain dream --json | tee /tmp/dream-last.json
   jq -r '.phases[] | "\(.phase): \(.status) (\(.duration_ms)ms)"' /tmp/dream-last.json
   ```
   Every phase must show `ok`. `skipped` is legitimate on a fresh brain (11
   of 23 skipped on the verified run). `warn`/anything else → isolate (step 5).

2. **Before/after delta — did the brain actually change?**
   ```bash
   gbrain stats        # run before AND after
   ```
   Record pages / chunks / links / tags. The verified acceptance run moved
   pages 1,666 → 1,755 and chunks 5,437 → 5,526. If every counter is
   identical, the run no-op'd — distinguish "legitimately nothing to do"
   from "silently failed" via step 5 before accepting it.

3. **Freshness bookkeeping — check the RIGHT counter, and know the stamping
   mechanism.** Dream and sync are different operations with different
   bookkeeping: a completed dream clears `cycle_freshness` **only when its
   sync phase actually processes new commits** — a dream over an
   already-fresh brain skips sync and stamps nothing (verified 2026-09-06:
   cycle_freshness FAIL persisted after a successful +89-page run).
   ```bash
   gbrain doctor
   ```
   After a dream: `cycle_freshness` improves for sources that had new
   content; `sync_freshness` is **expected to be unchanged** — if sources
   need syncing, that is a separate `gbrain sync` run, not a dream failure.

4. **The governor discipline — immediately, every time.** The dream cycle is
   structurally ungovernable (Memory Governor cannot intercept it — permanent
   limit), so its output reaches durable memory unreviewed. The always-applied
   compensation — note the **bare syntax fails** (exit 2); a query is
   required, and the probe is per-query (top-5 retrieval set, Haiku judge,
   $1 default budget):
   ```bash
   gbrain eval suspected-contradictions --query "<a real topic from the content just deepened>"
   ```
   Verified working 2026-09-06: 0 contradictions / 7 findings (2
   supersession, 1 regression, 4 evolution) on the acceptance run. The tool
   itself warns n<30 is below statistical threshold — run multiple real
   queries for meaningful coverage. Review every finding before considering
   the run complete.

5. **Isolating a failed phase.**
   ```bash
   gbrain dream --phase <name> --json | jq .
   ```
   Inspect the real error field, never the summary count. If the phase is
   `extract_atoms`, check credential validity FIRST (confirmed cause of one
   extended silent outage; re-verified valid 2026-09-06):
   ```bash
   curl -s https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" -H "content-type: application/json" -d '{"model":"claude-haiku-4-5-20251001","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'
   ```
   A `401 authentication_error` confirms a dead key. If a key was recently
   rotated, check for stray whitespace inside its quoted value:
   ```bash
   echo "$ANTHROPIC_API_KEY" | cat -A
   ```
   Exactly one line ending in `$` is clean.

## Verification expectations per phase (what "worked" means)

| Phase | Verified-success looks like |
|---|---|
| `extract_atoms` | Success status AND no bare-failure count — a silent zero here is the confirmed historical failure mode (2026-09-06: ok, 182s) |
| `resolve_symbol_edges` | Success status. **Zero edges resolved is EXPECTED** (pack limitation, permanent) — treat a phase *error* as the failure, never the 0 |
| `synthesize_concepts` / emotional-weight recompute | Success status; concept/atom counters may move (+89 pages on the verified run) |
| `purge` | Success status; page count may *decrease* — a decrease is work done, not damage |
| `sync` (inside the cycle) | Does **not** substitute for `gbrain sync` — freshness counters are separate (step 3); a skipped sync phase on a fresh brain is normal |
| `orphans` | `warn` with a count is the expected healthy output — it reports, it does not fix; the orphan count is content-hygiene backlog (config.md open items) |
| Long durations | Phases exceeding the 30s worker force-evict deadline emit warnings but complete (verified: `extract_atoms` 182s, `synthesize_concepts` 163s, `propose_takes` 106s — upstream #1972). Duration alone is not a failure |

## The gstack overlap trap (real incident, 2026-08-16)

`/sync-gbrain --dream` derives its own source ID (`gstack-code-<slug>-<hash8>`)
and fails on path overlap with a manually registered source (real case:
`gstack-code-mb-3-cs-12c8ee2f` vs `mb-3-cs-code`). Repair: bypass the
orchestrator's code stage — `gbrain dream --source <existing-id>` directly.

## Do not

- Do not accept a bare "N failed" summary as a diagnosis — always read the
  real per-phase JSON output first (and use `.phase`, not `.name`).
- Do not treat a completed run as proof every phase did meaningful work —
  run the post-run verification procedure, every time.
- Do not use `sync_freshness` as evidence a dream ran — dream and sync are
  different bookkeeping operations, and a no-op dream stamps nothing.
- Do not treat 0 resolved edges from `resolve_symbol_edges` as a failure —
  it is the permanent pack limitation; a phase error is the failure.
- Do not assume a credential problem without checking — but do check it
  first for any `extract_atoms` failure, given its confirmed history.
- Do not run a full dream cycle to diagnose a single failing phase —
  isolate with `--phase`.
- Do not re-enable the autopilot schedule or put the dream cycle on a
  scheduler — on-demand invocation is the deliberate design (autopilot found
  inert and removed 2026-09-06; see [[gbrain-dream-cycle-config|Configuration]]).
