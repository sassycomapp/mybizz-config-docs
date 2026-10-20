---
title: "memory-governor-learnings"
doc-id: "mb-7a408578"
updated: "2026-10-20"
---
# Memory Governor — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why.
Read in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | Governed facts land in the owning project's own GBrain source; the worker sets `GBRAIN_SOURCE` to the owning project on every write. | Delivery is independent of the worker's folder; each fact co-locates with its project's documents. | `app/gbrain.py` |
| L2 | Every governed write re-points the brain-level default source (`sources.default`); under GBrain 0.59.18.0 a default naming a missing source stops every `gbrain sync`. | Setup and examination must always validate `sources.default` after governed writes. | [[[mybizz-config-docs:memory-governor/memory-governor-reference\|Reference]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-reference.md), stale-brain-default procedure |
| L3 | `scripts/run-tests-deterministic.sh` is not systemd-aware: stop the worker unit, run pytest, start the unit — never the runner while the unit is active. | The runner kills the worker and starts an unmanaged copy, leaving the unit stopped and a second worker unmanaged. | `scripts/run-tests-deterministic.sh` |
| L4 | GBrain's dream cycle is structurally ungovernable; the standing control is the manual discipline — real `dream`, then `gbrain eval suspected-contradictions`, then review. | No interception point exists in GBrain's dream cycle; forking GBrain — a permanent re-merge obligation — is rejected. | [[[mybizz-config-docs:memory-governor/memory-governor-explainer\|Explainer]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-explainer.md), Why it works this way |
| L5 | `anvil-agent-references` syncs into GBrain the ordinary way and never passes through the governor API. | Permanent, deliberate exception: reference material need not be fact-checked against itself. | Developer decision |
| L6 | The memory-governor repository is committed by hand; `commit-all` does not cover it. | Separate upstream repository with its own push flow; the worker itself commits and pushes register changes. | Developer decision |
