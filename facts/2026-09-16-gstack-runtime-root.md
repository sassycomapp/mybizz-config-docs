---
title: "2026-09-16-gstack-runtime-root"
doc-id: "2026-09-16-gstack-runtime-root"
---
# Fact — GStack runtime root and mixed-interpreter bin tree on the OpenCode host

On this OpenCode host, the correct GStack runtime root is:

    ~/.config/opencode/skills/gstack/bin

Generated SKILL.md preambles default their runtime-path detection to
`~/.openclaw/skills/gstack/bin` or `~/.claude/skills/gstack/bin` — the first is
absent here and the second is a fallback symlink the global AGENTS.md says not
to rely on. Preamble `|| true` fallbacks keep skills running, but the preamble
never resolves the OpenCode root at load time (verified live 2026-09-16, Tier 3
GS3-1).

The `bin/` tree is **mixed-interpreter**: most scripts are bash, but
`gstack-gbrain-detect` (and gbrain-facing diagnostics) were rewritten to
TypeScript/Bun (shebang `#!/usr/bin/env -S bun run`). Invoke per-script
shebang — running `bash <name>` on a Bun script yields confusing multi-line
errors. `gstack-brain-sync` is still bash (reference's `bash ...` invocation
correct).

Recorded in [[gstack-reference|GStack Reference]] (§bin-tree notes via docs governance).
