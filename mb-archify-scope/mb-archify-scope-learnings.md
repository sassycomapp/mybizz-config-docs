---
title: "mb-archify-scope-learnings"
doc-id: "mb-083dbb4b"
updated: "2026-10-20"
---

# mb-archify-scope — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why. Read
in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | This suite's spec body carries its wikilinks in stored form, so the commit hook rewrites nothing in the body: the repo spec and the installed copy stay body-identical across close-out commits. | Sources whose bodies are born short-form diverge from their installed copies at every close-out commit, because the hook rewrites their links; a stored-form-born body removes that divergence class. | [[[mybizz-os-docs:os-reference-docs/skills-catalog\|skills catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md) source column; [[[mybizz-os-docs:os-reference-docs/repo-organization\|repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) |
