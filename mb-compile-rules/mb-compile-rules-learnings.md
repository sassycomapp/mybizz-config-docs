---
title: "mb-compile-rules-learnings"
doc-id: "mb-5bf18b53"
updated: "2026-10-15"
---
# mb-compile-rules — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why. Read
in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | The rule estate — the plain-language sources in `rules-cupcake-global/` and the deployed rule files — is recorded in [[[mybizz-config-docs:cupcake/cupcake-config]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md), not in this suite. This suite points to it and carries no estate rows. | Cupcake owns its rules; a second record of them here drifts. | Developer decision |
| L2 | Checks whose command text contains `cupcake` are developer-run: the guard denies on command text, not intent. | Losing it would let an agent re-classify the live-folder and binaries checks as agent-run, or mark a denied check satisfied on earlier evidence. | Live denials; [[[mybizz-config-docs:mb-config-manager/config-manager-learnings\|config-manager Learnings]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-learnings.md) L1–L2 |
