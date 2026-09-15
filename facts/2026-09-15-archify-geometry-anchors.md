---
document: "Durable fact — Archify explicit geometry anchors and repair order"
doc-id: fact-archify-geometry-anchors
state: Live
date-created: 2026-09-15
---

# Durable fact — Archify explicit geometry anchors and repair order

When an Archify connection uses explicit `via`/`fromSide`/`toSide`, the port
anchors at the node's **side midpoint** (e.g. a database node's top port at
(x-center, top-y), bottom port at (x-center, bottom-y)). A `via` that does not
share the port's exact coordinate produces a diagonal final segment and fails
`clean-flow/endpoint-side-direction`. Automatic Port Spread is skipped for
explicit routes, so when several flows share one side they collapse onto the
midpoint port — give each anti-parallel pair its own physical channel (one
over, one under) rather than sharing the channel.

Repair order (confirmed live): fix quality_profile/schema → node overlap →
edge-through-node and endpoint-direction → proper-crossing, corridor, rhythm →
label clearance. Apply one diagnosed geometry control at a time and stop when
the objective error count reaches its minimum.