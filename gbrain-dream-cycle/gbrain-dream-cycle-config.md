---
title: "gbrain-dream-cycle-config"
doc-id: "mb-c6df61ed"
updated: "2026-10-20"
---
# GBrain Dream Cycle — Configuration

Canonical current-state configuration record. Agent-facing. States facts, not
history — see [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-explainer.md) for the reasoning; for
commands and the post-run verification procedure, see
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-reference|Reference: Invocation, Verification, Diagnostics]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-reference.md).

**System context:** the Dream Cycle is GBrain's own deepening mechanism — one
of the six closely related memory components (see
[[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md)'s system context). Cross-component reasoning
lives in [[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md), which also owns the
confirmed full phase sequence.

---

## Identity

| Field | Value |
|---|---|
| Issuer | GBrain project (garrytan/gbrain, MIT) — external system |
| Installed version | 0.59.18.0 |
| Standard taken from | The installed version: 0.59.18.0 source and `gbrain dream --help` (github.com/garrytan/gbrain at tag v0.59.18.0) |
| Last researched | 2026-10-20 |

## Settings

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Parent system | — | GBrain (parent suite: [[[mybizz-config-docs:gbrain/gbrain-config\|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md)) | https://github.com/garrytan/gbrain/tree/v0.59.18.0 | |
| Schema pack coupling | — | `gbrain-everything@1.0.0` (sha8 `7021205a`) — the only installed pack; dream phases operate within its extractability rules | MCP `get_active_schema_pack`; `list_schema_packs` | |
| Invocation model | Nightly autonomous schedule (upstream autopilot design) | Manual: run by hand weekly, after the Sunday backup, through `/mb-memory-system-diagnostic`. Autopilot is off by decision; no schedule exists or is wanted | https://github.com/garrytan/gbrain/tree/v0.59.18.0 | L2 |
| Trigger surfaces | `gbrain dream` | `gbrain dream` (full), `gbrain dream --phase <name>` (single phase), `gbrain dream --source <id>` (source-scoped); `/sync-gbrain --dream` exists but is not used in this environment — the cycle runs from `/mb-memory-system-diagnostic` (overlap trap: [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-reference\|Reference]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-reference.md)) | `gbrain dream --help` (0.59.18.0) | |
| Dream config keys | `dream.*` surface exists (triage cascade, synthesis turn cap, per-phase gates) | None set; upstream defaults apply | `gbrain config get dream` | |
| `purge` retention | Pages soft-deleted more than 72 hours earlier are hard-deleted | Same (issuer default in force) | https://github.com/garrytan/gbrain/tree/v0.59.18.0 | |
| Phases most operationally relevant | — | `extract_atoms` (Anthropic-dependent), `resolve_symbol_edges` (call-graph attempt) | `gbrain dream --help` (0.59.18.0) | |
| Job queue | — | No GBrain worker runs, so the `extract` and `facts-absorb` jobs that syncs create wait unprocessed (316 waiting: 305 `facts-absorb`, 11 `extract`). Every waiting job must be authorized or cancelled before a worker is started | `gbrain jobs stats` | |
| Links between repositories | — | The cycle's `extract` phase reads one source at a time and cannot resolve a link into another source. Those links are written by the full read at the end of `sync-gbrain.sh`; if they are missing after a dream, the sync script's link command restores them (command: [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-reference\|Reference]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-reference.md)) | GBrain source at tag v0.59.18.0 | |
| Doctor baseline | — | 15/100. The only distinct FAIL is `cycle_freshness` — the expected state (see [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-explainer\|Explainer]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-explainer.md)). WARNs include `extract_atoms_backlog`, `atom_provenance_drift`, `queue_health`, `backup_coverage`, `dangling_aliases`, `undeclared_db_only_pages`, `source_routing_health`, `takes_count`, `flagged_pages`, `content_sanity` | `gbrain doctor` | |
| MEMORY_VERBS surface | Memory verbs are part of the default MCP surface | `mcp_surface` is set explicitly to `verbs` on the DB plane; the memory-governor suite records `mcp_surface: verbs` as its build prerequisite ([[[mybizz-config-docs:memory-governor/memory-governor-config\|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md)) | `gbrain config get mcp_surface` | |
| Known limitation | `code` is `extractable: false` in every bundled schema pack | `resolve_symbol_edges` returns symbol names only (`resolved: false`), so it does not produce a resolved call graph. Graphify's `get_neighbors` is the tool of record. Permanent | Active schema pack (`schema explain code`) | |

## Provider dependency

| Phase | Provider | Credential |
|---|---|---|
| `extract_atoms` | Anthropic | `ANTHROPIC_API_KEY` — required, present (env-only), verified valid against the live API |

No other dream-cycle phase in active use has a distinct credential requirement
beyond GBrain's base model configuration ([[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md),
Models section).

## Open items

None.
