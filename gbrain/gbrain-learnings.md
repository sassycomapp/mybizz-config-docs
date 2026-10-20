---
title: "gbrain-learnings"
doc-id: "mb-26f4e9cf"
updated: "2026-10-20"
---
# GBrain — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why. Read
in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | The reranker is on, using `voyage:rerank-2.5`. | GBrain ships with it off; reranking puts the right document first far more often. | `gbrain doctor` reranker_health; Voyage rerank documentation |
| L2 | `search.reranker.timeout_ms` is `20000`. | Voyage answers full requests in up to about ten seconds; GBrain's default of 5000 cuts them off. | GBrain `src/core/search/mode.ts` |
| L3 | `GBRAIN_QUERY_EMBED_TIMEOUT_MS` is `15000`. | OpenAI's first embedding call can take about seven seconds; GBrain's default of 6000 cuts it off. | GBrain `src/core/search/hybrid.ts` |
| L4 | WSL tries IPv4 addresses first (`/etc/gai.conf`). | WSL has no IPv6 route; Bun tries IPv6 first and hangs about ten seconds. | Measured with `curl -6` and Bun `fetch` |
| L5 | `systemd-timesyncd` is disabled in WSL. | Two time services made the WSL clock jump, which fired timeouts early. | `journalctl` "Clock change detected" |
| L6 | The Voyage payment method sits on the organization that holds the API key. | Voyage limits keys in any organization without one to 3 requests a minute. | Voyage rate-limits documentation |
