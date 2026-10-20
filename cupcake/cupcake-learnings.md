---
title: "cupcake-learnings"
doc-id: "mb-a3fa7539"
updated: "2026-10-20"
---
# Cupcake — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why.
Read in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | Any bash command whose text names a grant tool is denied, even read-only resolution such as `command -v`; the exec-protection matcher also fires on read-shaped `sed` whose operand is a control-plane path, and on listings of the grant tools' bin dir. | Guards match command text, not intent; a denial is never retried or worked around. | cupcake-config.md, control-plane rule row; live denial evidence |
| L2 | Grant decrements are serialized by a mkdir-based lock shared by the plugin and the five grant tools; a lock timeout skips the update rather than racing it. | An unserialized read-modify-write loses decrements under parallel tool calls. | cupcake-config.md, grant-mechanics rows; plugin source |
| L3 | The compiled cross-project rule's exempt list is `/tmp/`-only, and the compiled rule is the enforcement truth over its source document. | The compiled state is what actually evaluates; the source document states the same list. | cupcake-config.md, source↔deployed correspondence row |
| L5 | The installed version is kept: enforcement is live-verified with the local plugin amendments; an upgrade replaces the amended plugin and requires re-testing all 20 rules. | An upgrade replaces the amended plugin. | github.com/eqtylab/cupcake; developer decision |
| L7 | A `.cupcake` skeleton holding a rule file but no `system/evaluate.rego` stops the engine (`undefined entrypoint data.cupcake.system.evaluate`); an empty skeleton is skipped. | The upstream documentation describes the skeleton, not this failure; it is what left every project skeleton unenforced. | live evaluation |
| L8 | OpenCode V2 does not run the Cupcake plugin; with the plugin unloaded, no rule applies and nothing reports it. OpenCode stays on version 1. | Fail-closed cannot catch a plugin that never loads; only the plugin-load check and a liveness probe show it. | Developer decision |
| L9 | The plugin is one file, `~/.config/opencode/plugin/cupcake.js`, not the folder the issuer documents. OpenCode loads it, and the liveness probe proves it enforces. | One global file is the only copy, so no project copy can override it. | v0.3.0 plugin reference; liveness probe |
| L10 | The rules protecting `AGENTS.md`, `CLAUDE.md`, `opencode.json` and `package.json` block an agent's edit even when the developer approves it in the same turn. This stays. | An agent never writes these files; the developer changes them in the terminal, which Cupcake does not govern. | Developer decision |
| L11 | A session started in `/home/dev-p`, above the skills folder, still has an ungranted write into `~/.config/opencode/skills/` blocked. | The skills-folder protection holds whatever folder the session starts in. | Developer check |