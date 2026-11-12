---
title: "mb-form-builder-learnings"
doc-id: "mb-e892477f"
updated: "2026-11-12"
---

# mb-form-builder — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why. Read
in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | The repo spec's body carries no wikilinks — every file reference is a backticked path — so the commit hook rewrites nothing in the body, and the repo spec and the installed copy stay body-identical across close-out commits. | Sources whose bodies are born with `[[links]]` diverge from their installed copies at every close-out commit, because the hook rewrites their links; a link-free body removes that divergence class. | body diff, 2026-11-12; [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-learnings\|mb-archify-scope learnings]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-learnings.md) L1 pattern |
