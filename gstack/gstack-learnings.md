---
title: "gstack-learnings"
doc-id: "gstack-learnings"
---
# GStack — Learnings

Transient way-station for exam-run knowledge: patterns, decisions, nuances. No
narrative, no history. Every entry is eventually dropped or written into a
**permanent home** (skill / config / reference / explainer / reference) — then
deleted from here immediately on graduation. The plan is never an absorption
destination — it is transient; pruning into a plan destroys the knowledge when the next cycle overwrites it. Entries never accumulate. Cross-cutting learnings (guard classes, graduation rules) live in the orchestrator's own [[config-manager-learnings|Learnings]], not here.

| # | learning | right action | destination |
|---|---|---|---|
| LE-1 | The `bin/` tree is mixed-interpreter: most scripts are bash, but `gstack-gbrain-detect` was rewritten to TypeScript/Bun (shebang `#!/usr/bin/env -S bun run`; the script comment documents the rewrite). Running `bash <name>` on a Bun script yields confusing multi-line errors — invocation must follow the individual script's shebang. Reference's `bash .../gstack-brain-sync` verified still correct (bash). | Add a bin-tree note to [[gstack-reference|GStack Reference]] documenting the mixed interpreters and the shebang-follow rule | gstack-reference.md (via docs governance) |
| LE-2 | Generated SKILL.md preambles hardcode OpenClaw/Claude host roots (`~/.openclaw/skills/gstack/bin`, `~/.claude/skills/gstack/bin`) for their runtime-path detection; on this OpenCode host those default resolutions are absent or discouraged, and the preamble's `|| true` fallbacks keep the skill running without ever resolving `~/.config/opencode/skills/gstack/bin` at load time. Proven live 2026-09-16 (Tier 3 GS3-1): skills load and work, but preamble runtime-path detection does not match the installed host layout. The global AGENTS.md GStack-binary-path rule is the authoritative resolution chain. | Document in [[gstack-reference|GStack Reference]] (pair with LE-1's bin-tree note): on the OpenCode host the correct runtime root is `~/.config/opencode/skills/gstack/bin`, not the preamble defaults | gstack-reference.md (via docs governance) |
| LE-3 | GStack artifacts live at `~/.gstack/projects/$SLUG/` (per-skill sub-directories: ceo-plans, designs, retros, checkpoints, qa-reports, health, security-audits, specs); later skills find prior output by re-computing the same deterministic `$SLUG` via `gstack-slug`. The AGENTS.md `gstack-outputs/` copy lane is a **convention only — it does not exist on this system** outside backups (verified 2026-09-16), so `~/.gstack/projects/$SLUG/` is the sole authoritative location. Recorded as the annotated fact in [[gstack-reference|GStack Reference]] §Artifact locations (2026-09-16) | No action — fact already in permanent home (reference) | resolved — permanent home exists |
