---
title: "project-docs-learnings"
doc-id: "mb-e633e576"
updated: "2026-10-16"
---
# mb-project-docs — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why. Read in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | The covered slugs are `mb-3-cs`, `mb-4-ecom`, `mb-5-pdlf` and `pdlf`, as in `repo-organization.md`; a document spelling `mb4ecom` or `mb5pdlf` is out of date. | `repo-organization.md` is the authoritative record of repository naming; the older spellings predate it. | [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) § Names |
| L2 | Anvil carries a folder under `theme\assets` only when it was first uploaded through Anvil's Add asset > Upload folder. Files then added to it locally and pushed arrive in Anvil and stay editable on both sides. A folder created locally and pushed is not carried, and a folder left empty is lost. | Anvil's editor is the source of the app's asset folders; Git only carries files inside folders Anvil already holds. | Developer test 2026-10-16 in `mb-3-cs-app1` |
