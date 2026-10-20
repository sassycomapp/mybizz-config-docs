---
title: "graphify-explainer"
doc-id: "mb-c1bcfdd3"
updated: "2026-10-20"
---
# Graphify Explainer

## 1. What it is

Graphify is a local tool that turns a folder of code — and optionally docs,
SQL schemas, PDFs, images — into a literal knowledge graph. Nodes are things
that exist in the corpus: functions, classes, modules, files, document
concepts. Edges are typed relationships between them: calls, imports,
contains, inherits. It exists to answer structural questions about a codebase
— what calls this, what breaks if that is edited, how do two things connect —
questions that grep cannot answer (it is linear, not relational) and that
GBrain, in this environment, deliberately does not answer (see
[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) for the division of labor between
the memory mechanisms).

In the MyBizz setup, Graphify maintains one code graph per app repository —
nine repositories across the three MyBizz projects — and serves each to
agents through OpenCode's MCP. It runs entirely on this machine. Code parsing
uses tree-sitter — the same deterministic parser technology a syntax
highlighter uses, not a language model — so the code side of any graph is
free, offline, and reproducible. Only document and media extraction involves
an LLM, and none is configured here: every graph is code-side extraction plus
ghost name references from Anvil UI templates the extractor cannot
structurally parse.

## 2. What it can do

- **Two extraction paths.** Structural (AST, tree-sitter, deterministic,
  free) for real code; semantic (LLM or vision, real cost) for markdown,
  HTML-as-document, images, video. A docs-only repository still produces a
  real graph — the tool is not code-only, though every graph here uses the
  code path.
- **Honest confidence labels.** Every edge is EXTRACTED (read directly from
  syntax — as trustworthy as reading the code yourself), INFERRED (the
  tool's educated guess — verify before leaning on it), or AMBIGUOUS
  (unresolved conflicting signals).
- **Structure-derived groupings.** Communities are clusters of dense
  interconnection, not folders — they can reveal real coupling across
  directory boundaries. God nodes are the hubs everything flows through;
  editing one has a structurally confirmable blast radius.
- **Four ways to ask.** Broad traversal for a question, shortest path between
  two things, a plain-language explanation of one node, and reverse-impact
  traversal ("what is affected by this?").
- **A work-memory loop.** Question/answer outcomes can be saved against the
  graph and aggregated into lessons, so the graph records how its own past
  answers fared.
- **Serving.** One graph can be exposed to agents over MCP, merged into a
  multi-repo global graph, or exported as interactive HTML, a D3 tree, or a
  call-flow page.

## 3. Suitability

- **Best for:** resolved, current, cross-file structural facts about code —
  callers, import chains, containment, structural paths, blast radius,
  architecture orientation — on a graph whose provenance matches the
  checkout.
- **Good for:** orientation before touching unfamiliar code; validating that
  an implementation still matches documented design intent (see the worked
  example below); including tests and internal scripts in structural review.
- **Not good for:** "why" questions — decisions, rationale, history (that is
  GBrain's job; neither tool replaces the other); verifying runtime behavior
  (read the source, run the tests); anything on a graph whose `built_at_commit`
  is behind HEAD (stale graph, confident wrong answers); Anvil UI templates
  as first-class structural nodes — plain `.html`/`.yaml` form templates are
  document types to the detector, so they appear only as ghost name
  references, not extracted structure; and treating INFERRED or AMBIGUOUS
  edges as settled.

## 4. Why it works this way

**Why every graph here is built code-only.** Code-side extraction is
deterministic, free, and offline: it needs no API key, makes no model calls,
and reproduces identically from the same source. The semantic and LLM paths
would add cost and nondeterminism to a job — structural truth — that does
not need them ([[[mybizz-config-docs:graphify/graphify-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/graphify/graphify-learnings.md) L1).

**Why confidence labels exist.** The honesty model is the product: the tool
never silently mixes what it read from syntax with what it guessed. Treating
an INFERRED edge like an EXTRACTED one is the single easiest way to get a
wrong answer with high apparent confidence — which is why the label is on
every edge, not buried in a log.

**Why the directed-undirected trap exists at all.** The graph is stored
undirected — a relationship is recorded as existing between two nodes,
because structural relations like containment are naturally described in
both directions — while path searches default to directed traversal. A real
relationship can therefore come back "no path found" purely because of the
direction the search walked. This is a standing property of the tool: every
surprising negative path result gets a second attempt in undirected mode
before being believed.

**Why `graphify-out/` is gitignored.** The output is a derived artifact,
fully reproducible from committed source at zero cost, and it mixes
machine-specific files (absolute root marker, AST cache) with derived data.
Gitignoring keeps the repository clean and makes provenance meaningful. If
the output is ever tracked, the hooks decision below must be re-examined
with it — the two stand together.

**Why the git hooks and merge driver are not installed.** The hook feature
installs three things inseparably — auto-rebuild hooks plus a union merge
driver for a tracked `graph.json`. The driver resolves conflicts on a file
that is never tracked here, so it is dead weight; the hooks would automate a
refresh that is deliberately run by hand at provenance-relevant moments,
keeping graph currency an explicit, verifiable act rather than a background
one ([[[mybizz-config-docs:graphify/graphify-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/graphify/graphify-learnings.md) L4).

**Why one shared AGENTS.md managed block.** GBrain and Graphify are the two
mechanisms that write persistent guidance into AGENTS.md; two independent
writers on one file is a write-conflict waiting to happen. One
marker-delimited block (`BEGIN/END GRAPH MEMORY GUIDANCE`, owned via
[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md)) holds a single policy for both —
including the rule that a graph must not be queried for current-state
answers when its provenance lags the checkout. A stale graph misanswers
confidently; the provenance check is what makes "current shape" claims
meaningful.

**Why both a CLI and an MCP server exist, and why they always agree.** They
are two frontends to the same `graph.json` — the CLI for mid-task human/agent
invocation, the MCP server for repeated structured tool calls from OpenCode.
Same artifact, so no cross-checking is needed between them; pick whichever
fits the context.

**A worked example that shows the boundary.** Ask both tools about the
Vault's secret-encryption mechanism. GBrain answers the why — owner-only
vault, TOTP step-up, encryption at rest, governing ADRs. Graphify answers
the where/how — `encrypt()` at a specific line, called by
`save_vault_secret()` and four tests, imported by `vault_service.py`, each
edge EXTRACTED. Agreement between the two, each at the trustworthy end of
its own tool's confidence scale, is the signal; low confidence on either
side turns the same agreement into a lead to verify rather than a settled
answer.

## 5. What has to happen

- After every code commit in a scoped repository, its graph is refreshed (the
  exact command is in [[[mybizz-config-docs:graphify/graphify-reference|Graphify Reference]]](C:/mybizz/mybizz-config-docs/graphify/graphify-reference.md)). The
  refresh restamps `built_at_commit`, which is what keeps the provenance
  check meaningful.
- The provenance check — graph commit against repository HEAD — precedes any
  current-state answer drawn from a graph.
- No API key and no AI backend is configured, and none gets added (L1); git
  hooks and the merge driver stay uninstalled (L4).
- Graphify is a member of the memory family: at the close-out of its runs,
  [[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) is updated to the verified
  state.
- The four documents in this folder are kept current by doc-suite research
  runs against the installed version.

*Companion documents: [[[mybizz-config-docs:graphify/graphify-config|Graphify Configuration]]](C:/mybizz/mybizz-config-docs/graphify/graphify-config.md) (current
state), [[[mybizz-config-docs:graphify/graphify-reference|Graphify Reference]]](C:/mybizz/mybizz-config-docs/graphify/graphify-reference.md) (commands and rules),
[[[mybizz-config-docs:graphify/graphify-learnings|Graphify Learnings]]](C:/mybizz/mybizz-config-docs/graphify/graphify-learnings.md) (differences and why).
Cross-component reasoning: [[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md).*
