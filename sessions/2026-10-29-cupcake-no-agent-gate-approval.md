---
title: "2026-10-29-cupcake-no-agent-gate-approval"
doc-id: "mb-18935479"
updated: "2026-10-29"
---
Compiled the developer-authored rule no_agent_gate_approval into a live, tested Cupcake policy: agent bash calls may not run pdlf-gate.sh in any form except a whole shell segment ending `pdlf-gate.sh --check`, and may not write to the PDLF ledger's gates table by SQL; SELECT stays free for the orchestrator's approval checks.

Three redraft cycles, each closed by real developer-run eval output. Cycle 1 compiled and loaded but never fired: all seven fixtures allowed. Cycle 2 fixed the tool gate to the exact `input.tool_name == "Bash"` and rebuilt the helpers from the proven commit-rule shapes — the script branch then denied correctly, but the SQL branch stayed silent. Cycle 3 root-caused it: bash delivers escaped quotes to the policy as literal backslashes (`public.\"gates\"`), fixed by tolerating an optional backslash before each optional quote. The full t0–t8 suite then matched and the developer kept the rule.

Evidence: opa check clean on OPA 1.19.1; live eval suite t0–t8 run by the developer (health allow; control git-commit deny; t1/t3/t5/t6/t8 deny; t2/t4 allow); the rule loads as `cupcake.global.policies.no_agent_gate_approval` in the engine log. Regression fixture sheet retained at /tmp/opencode (t0–t8 plus norm-* inputs) — ephemeral by design.

Decisions the developer set: the `--check` exception is anchored to the whole segment (a trailing `# --check` after real arguments denies); `(?i)` on every SQL pattern; double quotes tolerated around both `public` and `gates`; redraft before any placement; keep after real results.

Quirks: three cupcake_exec_protection denials this session (`cupcake --version`; `opa eval` carrying a `data.cupcake.` query string; one combined opa check command) — all honored, none retried, each became a developer-run line.

Documents: `cupcake/cupcake-config.md` estate updated to 22 sources ↔ 21 deployed rule files with the new rule row. Source `rules-cupcake-global/no_agent_gate_approval.md` unchanged and already committed before close-out.

Open: nothing.
