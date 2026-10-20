---
title: "gbrain-learnings"
doc-id: "mb-26f4e9cf"
updated: "2026-10-20"
---
# GBrain — Learnings

Transient way-station for exam-run knowledge: patterns, decisions, nuances. No
narrative, no history. Every entry is eventually dropped or written into a
**permanent home** (skill / config / reference / explainer) — then deleted from
here immediately on graduation. The plan is never an absorption destination — it
is transient; pruning into a plan destroys the knowledge when the next cycle
overwrites it. Entries never accumulate. Cross-cutting learnings (guard classes,
graduation rules) live in the orchestrator's own
[[[mybizz-config-docs:mb-config-manager/config-manager-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-learnings.md), not here.

| # | learning | right action | destination |
|---|---|---|---|
| 1 | Bundle evolution is normal: the dev-mb-3-cs skills bundle regenerates with the CLI — entry counts and file shapes change (60+skillify → 65 with underscore metadata files) | Re-inventory per run; flag only divergence from the *last recorded* state, not from older spec snapshots | config.md (skills-bundle row) — **APPLIED 2026-09-13** |

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | The reranker is on, using `voyage:rerank-2.5`. | GBrain ships with it off; reranking puts the right document first far more often. | `gbrain doctor` reranker_health; Voyage rerank documentation |
| L2 | `search.reranker.timeout_ms` is `20000`. | Voyage answers full requests in up to about ten seconds; GBrain's default of 5000 cuts them off. | GBrain `src/core/search/mode.ts` |
| L3 | `GBRAIN_QUERY_EMBED_TIMEOUT_MS` is `15000`. | OpenAI's first embedding call can take about seven seconds; GBrain's default of 6000 cuts it off. | GBrain `src/core/search/hybrid.ts` |
| L4 | WSL tries IPv4 addresses first (`/etc/gai.conf`). | WSL has no IPv6 route; Bun tries IPv6 first and hangs about ten seconds. | Measured with `curl -6` and Bun `fetch` |
| L5 | `systemd-timesyncd` is disabled in WSL. | Two time services made the WSL clock jump, which fired timeouts early. | `journalctl` "Clock change detected" |
| L6 | The Voyage payment method sits on the organization that holds the API key. | Voyage limits keys in any organization without one to 3 requests a minute. | Voyage rate-limits documentation |
