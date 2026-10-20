---
title: "gbrain-dream-cycle-reference"
doc-id: "mb-afe3a341"
updated: "2026-10-20"
---
# GBrain Dream Cycle — Reference: Invocation, Verification, Diagnostics

Companion to [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-config.md) (current state),
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-explainer.md) (reasoning) and
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-learnings.md) (what differs and why). Agent-facing.

**Invocation model:** manual — the cycle runs by hand weekly, after the Sunday
backup, through `/mb-memory-system-diagnostic`; autopilot is off by decision
(L2). Nothing runs unless run, which makes the post-run verification procedure
below mandatory, not optional: an unverified dream run is an unknown-state run.

---

## Running a dream cycle

```
gbrain dream                        # full cycle, all 23 phases
gbrain dream --source <id>          # source-scoped cycle
gbrain dream --phase <name>         # single phase (diagnosis / targeted re-run); repeatable for a multi-phase selection
gbrain dream --once --phase <name>  # run a gated phase once, ignoring its gate (--phase required)
gbrain dream --pull                 # git pull before the cycle runs
gbrain dream --dir <path>           # run against an alternate brain directory
gbrain dream --source-id <id>       # alias of --source
gbrain dream --input <path> --date <date> --from <date> --to <date>   # transcript-synthesis inputs
gbrain dream --phase extract_atoms --drain --source <id> --window <seconds>   # bounded backlog drain (L3); exit 3 = backlog remains
gbrain dream retriage               # retriage subcommand
gbrain dream --dry-run --json       # preview — writes nothing; NOT zero-LLM: runs the scored triage pass and caches verdicts, skips the synthesis subagents and the judgment phases; not a substitute for the post-run contradiction check (L1)
gbrain dream --json                 # full run with per-phase machine-readable output
```

**All 23 phases**, verified against the installed binary's `--phase` valid
list, in the canonical order: `lint, backlinks, sync, synthesize, extract,
extract_facts, extract_atoms, resolve_symbol_edges, patterns,
synthesize_concepts, recompute_emotional_weight, consolidate, propose_takes,
grade_takes, calibration_profile, drift, conversation_facts_backfill,
enrich_thin, skillopt, embed, orphans, schema-suggest, purge`. Phase taxonomy
(via doctor): 12 source-scoped, 9 brain-global, 2 mixed — full classification
in [[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md)'s doctor notes and
[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) §4.

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| GBrain repository | https://github.com/garrytan/gbrain/tree/v0.59.18.0 | 0.59.18.0 | 2026-10-20 |
| Dream cycle CLI surface | `gbrain dream --help` | 0.59.18.0 | 2026-10-20 |
| Doctor checks (phase scope, freshness) | `gbrain doctor` | 0.59.18.0 | 2026-10-20 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Installed version | `gbrain --version`; `git -C /home/dev-p/gbrain log -1` | agent |
| Invocation model (no schedule) | `crontab -l`; `ls ~/.gbrain/autopilot*` (both expect nothing) | agent |
| Dream config keys | `gbrain config get dream` (expects "not found") | agent |
| Schema pack coupling | MCP `get_active_schema_pack`; `list_schema_packs` | agent |
| Job queue | `gbrain jobs stats` | agent |
| Doctor baseline | `gbrain doctor` | agent |
| MEMORY_VERBS surface | `gbrain config get mcp_surface` | agent |
| `purge` retention | Installed source at tag v0.59.18.0, purge phase | agent |
| `ANTHROPIC_API_KEY` presence | `[ -n "$ANTHROPIC_API_KEY" ] && echo SET || echo NOT SET` | developer |
| `ANTHROPIC_API_KEY` validity | `curl -s https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" -H "content-type: application/json" -d '{"model":"claude-haiku-4-5-20251001","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'` | developer |
| Works | The weekly run completes through `/mb-memory-system-diagnostic` and the post-run verification procedure below passes | developer |

## Post-run verification procedure — after EVERY dream invocation

A completed run proves the sequence ended. It does **not** prove every phase
did real work — the known failure modes are silent (a bare failure count with
the real error swallowed; a phase resolving zero results by design). Verify in
this order:

1. **Capture per-phase output, not the summary.** The per-phase field is
   **`.phase`** (not `.name` — the `.name` recipe silently matches nothing):
   ```bash
   gbrain dream --json | tee /tmp/dream-last.json
   jq -r '.phases[] | "\(.phase): \(.status) (\(.duration_ms)ms)"' /tmp/dream-last.json
   ```
   Every phase must show `ok`. `skipped` is legitimate on a fresh brain.
   `warn`/anything else → isolate (step 5).

2. **Before/after delta — did the brain actually change?**
   ```bash
   gbrain stats        # run before AND after
   ```
   Record pages / chunks / links / tags. If every counter is identical, the
   run no-op'd — distinguish "legitimately nothing to do" from "silently
   failed" via step 5 before accepting it.

3. **Freshness bookkeeping — check the RIGHT counter, and know the stamping
   mechanism.** Dream and sync are different operations with different
   bookkeeping: a completed dream clears `cycle_freshness` **only when its
   sync phase actually processes new commits** — a dream over an
   already-fresh brain skips sync and stamps nothing, so `cycle_freshness`
   reporting FAIL until new commits are processed is the expected state, not
   a fault.
   ```bash
   gbrain doctor
   ```
   After a dream: `cycle_freshness` improves for sources that had new
   content; `sync_freshness` is **expected to be unchanged** — if sources
   need syncing, that is a separate `gbrain sync` run, not a dream failure.
   The accepted baseline figure lives in [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-config.md)'s
   Doctor baseline row.

4. **The governor discipline — immediately, every time.** The dream cycle is
   structurally ungovernable (Memory Governor cannot intercept it — permanent
   limit), so its output reaches durable memory unreviewed; the contradiction
   check is the standing compensation and runs after every invocation, with
   every finding reviewed. Note the **bare syntax fails** (exit 2); a query
   is required, and the probe is per-query (top-5 retrieval set, Haiku judge,
   $1 default budget):
   ```bash
   gbrain eval suspected-contradictions --query "<a real topic from the content just deepened>"
   ```
   The tool itself warns n<30 is below statistical threshold — run multiple
   real queries for meaningful coverage. Review every finding before
   considering the run complete.

5. **Isolating a failed phase.**
   ```bash
   gbrain dream --phase <name> --json | jq .
   ```
   Inspect the real error field, never the summary count. If the phase is
   `extract_atoms`, check credential validity FIRST (the confirmed cause of
   extended silent failure):
   ```bash
   curl -s https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" -H "content-type: application/json" -d '{"model":"claude-haiku-4-5-20251001","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'
   ```
   A `401 authentication_error` confirms a dead key. After a recent key
   rotation, check for stray whitespace inside its quoted value:
   ```bash
   echo "$ANTHROPIC_API_KEY" | cat -A
   ```
   Exactly one line ending in `$` is clean.

## Verification expectations per phase (what "worked" means)

| Phase | Verified-success looks like |
|---|---|
| `extract_atoms` | Success status AND no bare-failure count — a silent zero here is the known failure mode |
| `extract` | Success status. It writes links within each source only; links between repositories come from the full read at the end of `sync-gbrain.sh` (`gbrain extract links --source db`) |
| `resolve_symbol_edges` | Success status. **Zero edges resolved is EXPECTED** (pack limitation, permanent) — treat a phase *error* as the failure, never the 0 |
| `synthesize_concepts` / emotional-weight recompute | Success status; concept/atom counters may move |
| `purge` | Success status; page count may *decrease* — a decrease is work done, not damage |
| `sync` (inside the cycle) | Does **not** substitute for `gbrain sync` — freshness counters are separate (step 3); a skipped sync phase on a fresh brain is normal |
| `orphans` | `warn` with a count is the expected healthy output — it reports, it does not fix |
| Long durations | Phases exceeding the 30s worker force-evict deadline emit warnings but complete (e.g. `extract_atoms`, `synthesize_concepts`, `propose_takes` — upstream #1972). Duration alone is not a failure |

## The gstack overlap trap

`/sync-gbrain --dream` derives its own source ID (`gstack-code-<slug>-<hash8>`)
and fails on path overlap with a manually registered source. Repair: bypass
the orchestrator's code stage — run `gbrain dream --source <existing-id>`
directly.

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
  first for any `extract_atoms` failure.
- Do not run a full dream cycle to diagnose a single failing phase —
  isolate with `--phase`.
- Do not re-enable autopilot or put the dream cycle on a scheduler — it runs
  by hand weekly, after the Sunday backup (L2).
- Do not count `--dry-run` as a dream run for the governor discipline, and do
  not follow doctor's autopilot remediation suggestion (L1, L2).
