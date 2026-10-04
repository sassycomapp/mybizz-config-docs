---
title: "memory-ecosystem-scope"
doc-id: "mb-8f007ac3"
updated: "2026-10-04"
---
# Scope Card — memory-ecosystem

## Intent

The Memory Master Explainer describes a single memory system in which content
enters through five distinct write paths into two storage layers (a mirror
layer written by sync, ungated, and a durable layer written only through the
Memory Governor's gate), and questions are answered through two independent
read mechanisms (GBrain's hybrid search and Graphify's deterministic parsing).

## Load-bearing claim

The mirror is written un-gated because its authority is fidelity to existing
files, while the durable layer is gated because it alone claims to be believed
— and the governed spine (submit → gate → verify → write) is the one path that
confers durable status.

## Decisions (developer-approved verbatim)

- **Type:** `architecture` (guide agrees; low confidence, subject-justified)
- **Quality profile:** `showcase`
- **One store, two badges:** GBrain is one node with "mirror layer · durable layer"
- **Read paths are primary nodes** (GBrain hybrid search + Graphify)

## Type reason

The subject is a component ecosystem with five write flows and two read flows.
`architecture` forgives many edges and supports trust boundaries; `dataflow`
(the keyword-driven choice that failed previously) is a strict grid that
punishes dense crossing flows. Guide call returned `architecture`.

## Node Inventory (9 primary)

| id | type | label | role |
|---|---|---|---|
| real-files | external | Real Files | ultimate source; authority tier 1 |
| submit-memory | backend | mb-submit-memory | front door of the gate (Path 2) |
| governor-api | security | Memory Governor API | durability gate: auth + decide |
| delivery-worker | backend | Delivery Worker | gate delivery: outbox + register The use of registers has been discontinued. Please review |
| gbrain-store | database | GBrain — mirror layer · durable layer | one store, two badges |
| sync-task | backend | Sync | mirror refresh (Path 1) |
| dream-cycle | backend | Dream Cycle | deepening, unreviewed exception (Path 4) |
| graphify-parser | backend | Graphify | deterministic read mechanism |
| developer | frontend | Developer / Agent | consumer of both read paths |

## Main path

`real-files → submit-memory → governor-api → delivery-worker → gbrain-store`
(the governed spine — the only path that confers durable status).

## Side branches

- `real-files → sync-task → gbrain-store` (ungated mirror write, top lane)
- `dream-cycle → gbrain-store` (dashed, unreviewed)
- `real-files → graphify-parser` and `graphify-parser → developer` (read lane)
- `developer ⇄ gbrain-store` (question / advisory answer)
- `submit-memory → gbrain-store` (query related, dashed judgment input, below spine)

## Boundary

- `security-group` "durable gate" wrapping `governor-api` + `delivery-worker`

## Deferred to cards

- PDLF step-completion writer (Path 3) — same gate, own credential, parked
- Quick path (Path 5) — raw remember writes, always present; discipline documented, not mechanical
- PostgreSQL substrate — two instances, one port trap, RLS; every check names its instance
- Cupcake — mechanical enforcement on every tool call; loopback allowed by design
- Transactional outbox + register The use of registers has been discontinued. Please review commit; supersession not erasure; contradiction is a flag not a verdict

## Corridor plan

- Top lane: real-files → sync-task → gbrain-store (mirror, ungated)
- Middle lane: governed spine (emphasis, thickest read)
- Right: gate boundary, then store, then read/consume
- Bottom lane: dream-cycle → gbrain-store (dashed exception)
- Reads at far right: developer ⇄ gbrain, developer ⇄ graphify
- query-related routed below the spine

## Views (3 curated)

Write paths · Governed spine · Read paths

## Layout budget source

Architecture uses free `pos` placement (schema `layout.mode: grid` optional);
no renderer README exists for architecture — grid placement per example
`examples/web-app.architecture.json`; viewBox default `[320, 240]` minimum,
desktop-first.

## Probe declaration

Stub `validate` of components + boundary before connections, run in Archify
execution. Expected: 9 components + gate boundary validate clean, 0 composition
errors, no component overlap, viewBox fits 5-column span.

## Abort conditions

If the probe shows overlapping components or a viewBox that cannot fit the
spine at desktop widths, execution returns to Phase 5 for row reshaping —
never proceeds past a failed probe.

## Status

Approved 2026-09-15 by developer.
