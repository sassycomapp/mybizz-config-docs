---
title: "2026-09-23-renderings-stencils-not-link-targets"
doc-id: "2026-09-23-renderings-stencils-not-link-targets"
---
# Fact — renderings and stencils are not resolvable link targets

Registered html renderings, .json manifests, and retired stencils are
register rows but not brain pages — GBrain never ingests them as pages —
so their [[...]] references cannot resolve and must NOT convert. The
Phase-C unresolvable-target rule applies: "an unresolvable proposed target
is a finding, not a link." (4 pairs dropped on 2026-09-23: a stencil cheat-
sheet, one html decision tree, one json manifest, in makepdlf.)

Corollary: verify every proposed link target by CLI source-scoped search
(`gbrain search "<stem>" --source <id>`); the MCP get_page cannot see
synced source pages and returns page_not_found for pages the CLI finds.

Context: session 015 (`sessions/2026-09-23-015-mb-doccycle-makepdlf-first-cycle`),
Phase C of the makepdlf cycle. Confidence 1.0, method: live verification ×23
stems. Approved at the 2026-09-23 close-out gate.
