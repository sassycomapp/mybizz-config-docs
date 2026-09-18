---
document: "Fact — mg-grant lowercases the granted path"
doc-id: 2026-09-15-mg-grant-lowercase-paths
state: Live
date-created: 2026-09-15
---

# Fact — mg-grant lowercases the granted path

The `mg-grant` tool (`~/.config/cupcake/bin/mg-grant`) canonicalizes the
`--path` argument through `to_wsl()`, which **lowercases** it. A file-level
grant for an uppercase filename is therefore recorded lowercase — observed
live 2026-09-15: `mg-grant --path /home/dev-p/.config/opencode/AGENTS.md`
produced the grant entry `/home/dev-p/.config/opencode/agents.md`.

On a case-sensitive filesystem that grant may not match the real
`AGENTS.md` path. Prefer **folder-level grants** whenever any path component
contains uppercase characters.

Note: in the same incident the agent-side edit was refused anyway by the
protected-AI-governance-files policy — grants do not unlock protected
governance files; those edits are developer-run regardless of grant state.

Context: session 2026-09-15-001
(`sessions/2026-09-15-001-data-mybizz-mgt-repo-registration`).
Confidence 0.9, method model_based (single live observation). Approved at
the 2026-09-15 close-out gate (governed routing).
