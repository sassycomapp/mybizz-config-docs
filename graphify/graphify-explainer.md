# Graphify Explainer

## 1. Opening

GBrain answers "why was this built this way?" — but it has a real, permanent blind spot: it cannot reliably tell you what actually calls what in a codebase right now. No schema pack it ships with extracts a resolved code call-graph, and even where it tries, resolution is limited to symbols in the same file. That gap is exactly what Graphify exists to close.

Graphify is a local, deterministic code and document knowledge-graph builder — independent of GBrain, GStack, and any other skill system in this environment. It parses real source code with Tree-sitter (the same kind of parser a syntax highlighter uses, not a language model) and builds an actual graph of definitions, calls, imports, and containment. Where GBrain gives you the *reasoning*, Graphify gives you the *structurally true, current shape* of the implementation.

---

## 2. What Graphify Actually Is

Graphify has two genuinely different extraction paths, not one. **AST extraction** covers real code files — deterministic, zero LLM calls, zero cost, using Tree-sitter's structural parsing. **Semantic extraction** covers markdown, HTML-as-document, and images — real LLM work with real token cost, dispatched to a subagent or a vision backend.

This matters more than it sounds: a repository with no code files at all, only markdown and documentation, can still produce a real, substantive Graphify extraction. It isn't a code-only tool, even though the code path is the one used most heavily here.

Every relationship Graphify extracts carries a confidence label — **EXTRACTED**, **INFERRED**, or **AMBIGUOUS**. EXTRACTED means the relationship came directly from parsing real syntax — a function call, an import statement, a containing module — and is about as trustworthy as reading the code yourself. INFERRED means Graphify made an educated guess at a relationship not literally spelled out in syntax, worth a second look before leaning on it for anything consequential. In the current graph, the overwhelming majority of edges are EXTRACTED, with a small remainder INFERRED and none AMBIGUOUS — see `graphify-config.md` for the exact current figures.

---

## 3. A Worked Example — Why the Split Actually Matters

During setup, both GBrain and Graphify were asked about the same thing — the Vault's secret-encryption mechanism — as a direct test of whether the GBrain/Graphify split holds up in practice.

**GBrain's answer (the "why"):** the Vault is owner-only, gated behind a TOTP step-up on every open; secrets are encrypted at rest and never displayed again after saving; the encryption key lives in Anvil Secrets; this is governed by named ADRs about the payment security boundary and vault RBAC.

**Graphify's answer (the "where/how"):** `encrypt()` is defined at a specific line in `encryption_service.py`; it's called by `save_vault_secret()` in `vault_service.py`, and by four test methods; `vault_service.py` imports it; a docstring edge even carries the literal sentence describing the encryption method. All of these relationships were marked EXTRACTED — parsed directly from the AST, not inferred.

The two answers agreed — the design intent described in GBrain's documents was faithfully realized in the code Graphify actually found. That agreement is itself the valuable signal: had they disagreed, that would mean either the documentation is stale or the implementation has drifted from what was decided, and either is worth knowing immediately.

---

## 4. Real Incidents Worth Understanding

**Installing from the wrong directory.** Graphify's per-repo activation step writes real, repo-scoped files relative to whatever the current directory happens to be — with no warning if that directory isn't actually a real project. Running the install command from a home directory instead of a project folder writes plugin registration files directly into whatever `~/.opencode/` already contains, potentially a leftover, unrelated scaffold from months earlier. The standing practice this created: always confirm the working directory before running `graphify install`, every time, without exception.

**The directed-path default producing false negatives.** `graphify path` defaults to directed traversal even when the underlying graph is stored undirected. This produces misleading "no path found" results for relationships that are real but only exist in a reverse-structural form. This was confirmed directly, not theoretically: a real cross-check on `get_vault_secret` → `encrypt` returned "no path found" under a directed search, while the identical undirected search correctly returned the true two-hop path matching the actual source code. The standing rule this created: always pass the undirected flag explicitly when checking a cross-file or non-obvious relationship.

---

## 5. Known Limitations, Honestly Stated

**Anvil UI templates are not structurally extracted.** `.html` and `.yaml` form templates are classified as document types, not code types, in Graphify's detector — there is no plain-HTML/YAML AST extractor. This produces "ghost" template-class references (empty source file) as a direct, understood consequence, not a bug. Closing this would require switching to semantic (LLM) extraction for these file types, which is a deliberate future decision, not a default.

**The directed/undirected default is a real, standing trap**, covered fully in Section 4 — worth remembering every time, not just the first time.

**Git hooks and the merge driver were deliberately not installed.** The union merge driver this feature would add is dead weight when the graph output directory is gitignored (the normal, recommended state) — since the file it would resolve conflicts on is never actually tracked, the driver can never fire, yet installing it still adds tracked-file and config churn for no benefit. Standing practice: refresh manually with `graphify update` when currency matters, rather than installing hooks by default.

---

## 6. The GBrain/Graphify Boundary, In Practice

No naming overlap between the two tool sets. They read from entirely separate backends — a Postgres database versus a local graph file — and never write to each other. Graphify never modifies GBrain's database; GBrain does not ingest Graphify's output.

The working rule that emerged from all of the above: for "what calls/imports/contains what," always reach for Graphify — GBrain's own code-analysis commands are not a substitute for it, for the specific, permanent reason covered in `gbrain-explainer.md`.

---

*Companion documents: `graphify-config.md` (current configuration facts), `graphify-reference.md` (command syntax and troubleshooting).*

*End of document*
