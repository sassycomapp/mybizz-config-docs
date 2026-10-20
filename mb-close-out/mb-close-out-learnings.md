---
title: "mb-close-out-learnings"
doc-id: "mb-07f09f8b"
updated: "2026-10-20"
---
# mb-close-out — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why. Read in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | The skill's version identity is the source repository's latest commit (`git log -1` of `/mnt/c/mybizz/mb-close-out`); SKILL.md declares no version field. | A version-less skill still needs a stable identity for the register and for drift checks; this is the developer's standing convention. | developer decision |
| L2 | The installed copy's frontmatter differs from the source's by design — OpenCode needs `name`/`description`, the corpus needs `title`/`doc-id`/`updated`. Never align them. | Each loader reads its own format; aligning them would break one side. Copy currency is proven by the body diff below the frontmatter. | live diff of the two copies |
