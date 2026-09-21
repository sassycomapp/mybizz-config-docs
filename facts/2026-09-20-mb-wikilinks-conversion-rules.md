---
document: "Durable fact — mb-wikilinks conversion rules (developer-confirmed 2026-09-20)"
doc-id: 2026-09-20-mb-wikilinks-conversion-rules
state: Live
date-created: 2026-09-20
---

# Durable fact — mb-wikilinks conversion rules

mb-wikilinks converts document references to [[basename|Display Text]] form
only. Never candidates: folder references, URLs, code identifiers, config keys,
table/column names, registers, templates, quoted shell command text, and
collision basenames — including case-collisions (agents.md ≡ AGENTS.md on
Windows). Detection and the collision census run against the whole resolver
universe (all registered sources), not the scanned source alone.

Developer-stated 2026-09-20 during the mb-wikilinks full run
(sessions/2026-09-21-012-mb-wikilinks-full-run).
