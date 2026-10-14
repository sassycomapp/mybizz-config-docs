---
title: "config-manager-learnings"
doc-id: "mb-8c382f68"
updated: "2026-10-14"
---
# mb-config-manager — Learnings

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | Guard-denial classes are permanent execution boundaries — `.env` sourcing, `config.json` reads, system-path reads, and any command whose text contains a protected token (e.g. `cupcake`). A check in a blocked class is developer-run: stop, and hand the developer the exact terminal lines. | Guards match command text, not intent; a denial is never retried, never reshaped, never worked around. | agent hard rule 6; live denials |
| L2 | A check that passed earlier the same day may still be denied later. Never mark a denied check as satisfied on earlier evidence. | Guard behaviour is not deterministic from the agent's viewpoint; prior-session evidence informs but never substitutes. | live proof on the postgres bridge |
| L3 | When a system was rebuilt after its documents were written, its source is the standard and its documents are not; correct the documents through a Refresh, never the source through the documents. | The rebuild defines current behaviour; documents written before it describe a superseded design. | developer decision |
