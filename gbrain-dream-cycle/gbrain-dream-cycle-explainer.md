# GBrain Dream Cycle — Explainer

## 1. What It Actually Is

The Dream Cycle is GBrain's own autonomous maintenance mechanism — a background process that runs against everything already stored in the brain and tries to build a deeper, more structured understanding of it, without a human asking a specific question first.

Ordinary GBrain search answers "find me something related to X." The Dream Cycle does a different kind of work: it extracts facts, attempts to resolve which code symbols call which other symbols, checks whether stored content contradicts itself, and synthesizes concepts across many separate documents rather than treating each one in isolation. It is the mechanism through which GBrain's memory becomes more than a pile of separately-searchable pages.

It matters to understand where it sits relative to everything else: the Dream Cycle only ever operates on GBrain's own stored content. It has no authority over real files, and nothing it produces overrides what's actually written in a repository, an ADR, or a spec. Its output is advisory, exactly like the rest of GBrain.

---

## 2. How It Actually Works

The Dream Cycle runs as a set of distinct, separately-invocable phases, not one monolithic pass. The two phases most directly relevant day to day:

- **`extract_atoms`** — pulls discrete facts out of stored content. This phase makes its own LLM calls, using Anthropic, and is the phase most likely to be affected by a credential problem (see Section 4).
- **`resolve_symbol_edges`** — attempts to build the call-graph relationships between code symbols GBrain has ingested.

Both are part of the active `gbrain-everything` schema pack, which is the only schema pack currently installed. Each phase can be invoked individually — `gbrain dream --phase extract_atoms`, `gbrain dream --phase resolve_symbol_edges` — rather than only as a full, all-phases run.

A dream cycle can be triggered manually, or run as part of a fuller `sync --dream` pass. Its own JSON output can be inspected directly per-phase, which is the real, reliable way to check whether a specific phase actually succeeded, rather than trusting only the cycle's own summary line.

---

## 3. What It's Actually For, In This Project

The most direct, practical payoff of the Dream Cycle in this environment is the code call-graph it attempts to build via `resolve_symbol_edges`. This matters because of a real, permanent limitation elsewhere in GBrain: no schema pack — not even `gbrain-engineer`, despite its name — actually extracts resolved code-symbol call-graph edges. `code-callers`/`code-callees` can name a symbol but cannot resolve it to a defining location. The Dream Cycle's `resolve_symbol_edges` phase is GBrain's own attempt to close part of that gap from the memory side; **Graphify remains the correct, fully-resolved tool for cross-file call/import/containment relationships** — see `graphify-explainer.md`.

---

## 4. A Real Incident Worth Understanding, Not Just Noting

For a real stretch of time, every Dream Cycle run, across every registered source, failed completely at the `extract_atoms` phase — and the tool's own summary output never explained why. It reported a bare count: "5 failed," with no further detail, no matter how many times it was re-run.

The actual cause required direct investigation: `extract_atoms` uses its own Anthropic API key, and that key had quietly expired. The real error — "API key is invalid" — existed in the code but was never surfaced to the terminal; it was silently swallowed and reduced to a bare failure count. Finding it required temporarily adding one diagnostic line directly into GBrain's own source, catching the real message on a single run, then removing the diagnostic line immediately afterward.

Fixing the key wasn't the end of it either. The replacement key, once pasted into its configuration, had picked up a single stray line break inside its quoted value — invisible on a plain read of the file, but enough to corrupt every request using it, producing a completely different, misleading "invalid JSON" error with no obvious connection to the real problem.

**Why this belongs here, not just in a changelog:** both failures share the same lesson, and it applies every time a dream cycle run reports a bare failure count with no visible reason — go find the actual underlying error rather than accepting "it just doesn't work" as an answer. A clean-looking config file is not proof the value inside it is actually clean.

---

## 5. Known Limitations, Honestly Stated

**`resolve_symbol_edges` does not fully close GBrain's call-graph gap.** It is GBrain's own attempt at the problem, not a complete solution to it. Graphify remains the tool of record for anything requiring fully resolved, cross-file call/import/containment relationships.

**Dream cycle failures can be silent.** A phase can fail and report only a bare count, with the real, underlying error never surfacing on its own. Section 4 is the standing reminder of why that matters and how to actually find the real cause when it happens again.

**Provider dependency.** `extract_atoms` specifically depends on a valid, current Anthropic API key. A dream cycle that suddenly starts failing across the board is worth checking against credential validity before assuming anything more complex is wrong.

---

*Companion documents: `gbrain-dream-cycle-config.md` (current configuration facts), `gbrain-dream-cycle-reference.md` (invocation and query syntax).*
