---
title: "2026-09-14-memory-family"
doc-id: "2026-09-14-memory-family"
---
# Durable fact — The memory family

The memory family, as stated by the developer on 2026-09-14, consists of:
GBrain, the GBrain dream cycle, Memory-Governor (its API being the
to-be-confirmed part of memory-governor), Graphify, and the installed
mb-submit-memory skill — with Cupcake and PostgreSQL indirectly related.

The integration overview for the family lives in two authoritative files:

- [[memory-master-explainer|Master Explainer]] — how the four
  mechanisms fit together; the cross-component coordination point, updated
  by each memory-family run at its close-out (own commit).
- [[memory-functionality-audit|Full-System Procedure]] — the
  full-system audit procedure, invoked whenever the developer asks for a
  memory functionality audit, or after any restart, repair, or suspicion.
