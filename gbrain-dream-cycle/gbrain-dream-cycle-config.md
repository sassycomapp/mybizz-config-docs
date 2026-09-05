# GBrain Dream Cycle Configuration — mb-3-cs

Canonical current-state configuration record. Agent-facing. States facts,
not history — see `gbrain-dream-cycle-explainer.md` for narrative and the
one incident whose detail is directly operationally relevant.

---

## Identity

| Item | Value |
|---|---|
| Parent system | GBrain `0.46.1.0` (see `gbrain-config.md` for full GBrain identity) |
| Schema pack enabling this feature | `gbrain-everything@1.0.0` (sha8 `7021205a`) — the only installed pack |
| Phases most relevant to this project | `extract_atoms`, `resolve_symbol_edges` |

## Provider dependency

| Phase | Provider | Credential |
|---|---|---|
| `extract_atoms` | Anthropic | `ANTHROPIC_API_KEY` — required, present |

No other dream-cycle phase in active use has a distinct, separately-tracked
credential requirement beyond GBrain's own base model configuration (see
`gbrain-config.md` Models section).

## MEMORY_VERBS surface

| Item | Value |
|---|---|
| Status | Not enabled in this project (`mcp_surface: verbs` never evaluated) |
| Current surface | Full tool surface, in active use |

## Known limitation (active, not historical)

`resolve_symbol_edges` does not produce a fully resolved code call-graph.
No installed or bundled schema pack extracts resolved call-graph edges —
`code-callers`/`code-callees` return symbol names only, unresolved
(`resolved: false`, `to_chunk_id: null`). This is a property of every
bundled pack, not a configuration gap. Graphify's `get_neighbors` is the
correct tool for resolved cross-file relationships — see
`graphify-config.md`.

## Do not

- Do not switch schema packs expecting a fix for the call-graph
  limitation — confirmed not possible with any bundled pack.
- Do not treat a bare dream-cycle failure count as sufficient diagnosis —
  see `gbrain-dream-cycle-explainer.md` Section 4 for why, and check the
  real underlying error before assuming a new, more complex cause.
- Do not enable `MEMORY_VERBS` without explicit instruction — not
  evaluated for this project.
