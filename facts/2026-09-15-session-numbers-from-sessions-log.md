---
document: "Fact — session numbers come from the sessions log"
doc-id: fact-session-numbers-from-log
state: Live
date-created: 2026-09-15
---

# Fact — session numbers come from the sessions log

Session numbers are defined by the developer's sessions log
(`C:\data-mybizz-mgt\_desktop\sessions-log.md`) — never inferred from dates,
commit messages, or the GBrain page-name convention. Recording a session
under the wrong number marks the log incorrectly (developer instruction,
2026-09-15, session 005).

Concrete case: the mb-submit-memory configuration-management work began in
**session 003** and completed in **session 005** (2026-09-15); all close-out
records — the GBrain session page, the sessions-log row, and commit messages
— name it session 005, never session 003, regardless of when the task
started. The GBrain page name carries its own date (`sessions/YYYY-MM-DD-…`)
per the naming convention; the number in the log is the authoritative session
identity.
