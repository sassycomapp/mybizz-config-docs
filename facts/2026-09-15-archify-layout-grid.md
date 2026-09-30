---
title: "2026-09-15-archify-layout-grid"
doc-id: "mb-8b7e83cc"
---
# Durable fact — Archify dataflow grid budget and the corridor wall

Archify's `dataflow` renderer is a strict stage/row grid: row tops
`y = 128, 242, 356, 470, 584` (+ `yOffset`), stage centers `x = 100 + stage×215`,
default node 112×58, minimum node spacing 10px, minimum flow length 34px,
showcase rhythm ≥8px per segment and ≥16px interior. A flow crossing a
stage/lane band must pass through a **row band that is empty of nodes** —
stacked nodes in a column act as a wall that automatic routing cannot clear
and that explicit routing struggles to thread. Prefer [[architecture|Architecture]] (free
`pos`, edge-tolerant, guides for a component map) unless the subject genuinely
demands grid semantics.

Full budgets live per type at `renderers/<type>/README.md` in the Archify
package — read them at scope time, never from memory.
