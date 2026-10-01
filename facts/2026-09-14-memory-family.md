---
title: "2026-09-14-memory-family"
doc-id: "mb-c48dfae1"
updated: "2026-10-01"
---
# Durable fact — The memory family

The memory family, as stated by the developer on 2026-09-14, consists of:
GBrain, the GBrain dream cycle, Memory-Governor (its API being the
to-be-confirmed part of memory-governor), Graphify, and the installed
mb-submit-memory skill — with Cupcake and PostgreSQL indirectly related.

The integration overview for the family lives in two authoritative files:

- [[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) — how the four
  mechanisms fit together; the cross-component coordination point, updated
  by each memory-family run at its close-out (own commit).
- Full-System Procedure (memory functionality audit) — the
  full-system audit procedure, invoked whenever the developer asks for a
  memory functionality audit, or after any restart, repair, or suspicion.
