---
title: "2026-11-18-psql-bridge-quoting"
doc-id: "mb-b230ca1f"
updated: "2026-11-18"
---
# Ledger SQL through the WSL→PowerShell psql bridge: no embedded double quotes, no literal backslashes

The one bridge form every PDLF agent and script uses — `powershell.exe -NoProfile -Command "& 'C:\Program Files\PostgreSQL\15\bin\psql.exe' ... -c \"<SQL>\" ..."` — mangles embedded double quotes and backslashes inside `<SQL>`: a JSON literal like `'["16","17"]'` arrived at psql as `'[" 16\,\17\]'` and failed with a syntax error, and backslash path values break the same way. Write such values with constructs that contain neither character: JSON via `to_jsonb(ARRAY['16','17','18','19','20'])`, and a Windows backslash path via `replace('pdlf-outputs/c21/mb-3-cs-c21-app1-concept-check.md', '/', chr(92))`. Verified live on 2026-11-18 writing PDLF Step 21's row (steps id 14): the plain-quoted attempt failed with `syntax error at end of input`, the constructs inserted cleanly.
