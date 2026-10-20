---
title: "postgresql-learnings"
doc-id: "mb-9b586d8e"
updated: "2026-10-20"
---
# PostgreSQL — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why.
Read in full before any research, review or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | Instance A listens on 5433, not the issuer's default port, because Windows port 5432 belongs to WSL's localhost relay to Instance B; every Instance A command carries `-p 5433` explicitly. | The only MyBizz setting that departs from an issuer-set value: the relay makes the default port serve Instance B on both sides of the WSL boundary, so an unnamed port silently reaches the wrong server. | Live port-listener checks; the issuer's documented default port in the PostgreSQL runtime configuration ([[[mybizz-config-docs:postgresql/postgresql-config\|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md), Instance A port row) |
