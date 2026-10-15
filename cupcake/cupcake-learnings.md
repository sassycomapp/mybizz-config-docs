---
title: "cupcake-learnings"
doc-id: "mb-a3fa7539"
updated: "2026-10-15"
---
# Cupcake — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why.
Read in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | Any bash command whose text names a grant tool is denied, even read-only resolution such as `command -v`; the exec-protection matcher also fires on read-shaped `sed` whose operand is a control-plane path, and on listings of the grant tools' bin dir. | Guards match command text, not intent; a denial is never retried or worked around. | cupcake-config.md, control-plane rule row; live denial evidence |
| L2 | Grant decrements are serialized by a mkdir-based lock shared by the plugin and the five grant tools; a lock timeout skips the update rather than racing it. | An unserialized read-modify-write loses decrements under parallel tool calls. | cupcake-config.md, grant-mechanics rows; plugin source |
| L3 | The compiled cross-project rule's exempt list is `/tmp/`-only, and the compiled rule is the enforcement truth over its source document. | The compiled state is what actually evaluates; the source document states the same list. | cupcake-config.md, source↔deployed correspondence row |
| L5 | 0.3.0 kept: enforcement is live-verified with the local plugin amendments; 0.3.0 to 0.5.1 is unreviewed (103 commits, empty release notes) and an upgrade replaces the amended plugin and requires re-testing all 20 rules. | The upgrade replaces the amended plugin and its delta is unreviewed. | github.com/eqtylab/cupcake/releases; developer decision |
| L6 | Cupcake runs with failMode open: a Cupcake failure allows the tool call and logs it. | A guard that blocks all work when it breaks gets switched off; failing open keeps it trusted and in place. | Developer decision |