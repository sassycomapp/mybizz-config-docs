---
title: "2026-10-29-cupcake-bash-rule-exact-tool-name"
doc-id: "mb-657f0a84"
updated: "2026-10-29"
---
Cupcake custom policies that gate on the bash tool must compare `input.tool_name == "Bash"` exactly, capitalized as the harness normalizes it. The form `lower(input.tool_name) == "bash"` passes `opa check`, loads, and compiles into the global WASM module, but silently never fires: observed live 2026-10-29, a gate-approval rule returned allow on every bash fixture until the comparison was switched to the exact string, after which the same fixtures denied. New bash rules should also stay within the helper shapes the proven live rules use — plain `regex.match` rules, iteration over `split(...)` comprehension results, and negation of zero-arg rules only; shapes outside that set are unproven in the WASM path.
