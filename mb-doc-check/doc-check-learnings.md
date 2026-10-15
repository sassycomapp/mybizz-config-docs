---
title: "doc-check-learnings"
doc-id: "mb-0321e5b1"
updated: "2026-10-15"
---
# mb-doc-check — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why. Read in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | Source ids in `mb-doc-check.sources` are copied verbatim from GBrain's list; hand-written short forms drift. | The ids are GBrain's data, not MyBizz's; sources-check and repo-organization.md are the two sources to copy from. | Developer-approved lesson |
| L2 | The program has no release system. Its version is the commit in `/mnt/c/mybizz/scripts` (source repo `mybizz-scripts`) plus the file size, never a release number. | MyBizz is the issuer; the standard is the system's own source files. | repo-organization.md; live git log |
