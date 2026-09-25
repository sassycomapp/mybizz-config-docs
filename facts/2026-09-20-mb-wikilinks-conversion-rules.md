---
title: "2026-09-20-mb-wikilinks-conversion-rules"
doc-id: "2026-09-20-mb-wikilinks-conversion-rules"
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
