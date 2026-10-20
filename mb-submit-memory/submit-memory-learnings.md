---
title: "submit-memory-learnings"
doc-id: "mb-57436ffa"
updated: "2026-10-20"
---
# mb-submit-memory — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why.
Read in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | The installed copy and the canonical source are body-identical with different frontmatter by design; verify by body diff, never by whole-file hash. | Skill frontmatter (name/description) and document frontmatter (title/doc-id/updated) differ by construction, so whole-file hash equality is impossible. | Live body diff |
| L2 | The two skills-directory entries are one physical file, not two copies. | Prevents "dual copy" and "which one runs" confusion. | Inode and sha256 check |
| L3 | `project_local` is the default visibility for submissions and is agent-recallable under the installed GBrain. | Treating `project_local` as private or unrecallable misreports every governed fact. | Live recall check on GBrain 0.59.18.0 |
