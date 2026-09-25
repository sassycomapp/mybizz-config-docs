---
title: "graphify-explainer"
doc-id: "graphify-explainer"
---
# Graphify Explainer

## 1. What this actually is

Graphify is a local tool that turns a folder of code — and optionally docs,
SQL schemas, PDFs, images — into a literal knowledge graph. Nodes are things
that exist in the corpus: functions, classes, modules, files, document
concepts. Edges are typed relationships between them: calls, imports,
contains, inherits. It exists to answer structural questions about a codebase
— what calls this, what breaks if that changes, how do two things connect —
questions that grep cannot answer (it is linear, not relational) and that
GBrain, in this environment, deliberately does not answer (see
[[memory-master-explainer|Master Explainer]] for the four-mechanism division of labor).

It runs entirely on this machine. Code parsing uses tree-sitter — the same
deterministic parser technology a syntax highlighter uses, not a language
model — so the code side of any graph is free, offline, and reproducible.
Only document and media extraction involves an LLM, and none is configured
here: the mb-3-cs graph is entirely code-side extraction plus ghost name
references from templates it cannot structurally parse.

## 2. What it can do (capability level)

- **Two extraction paths.** Structural (AST, tree-sitter, deterministic,
  free) for real code; semantic (LLM or vision, real cost) for markdown,
  HTML-as-document, images, video. A docs-only repo still produces a real
  graph — the tool is not code-only, though every graph here uses the code
  path.
- **Honest confidence labels.** Every edge is EXTRACTED (read directly from
  syntax — as trustworthy as reading the code yourself), INFERRED (the tool's
  educated guess — verify before leaning on it), or AMBIGUOUS (unresolved
  conflicting signals). The current mb-3-cs graph: 96% EXTRACTED, 4%
  INFERRED, 0% AMBIGUOUS.
- **Structure-derived groupings.** Communities are clusters of dense
  interconnection, not folders — they can reveal real coupling across
  directory boundaries. God nodes are the hubs everything flows through;
  changing one has a structurally confirmable blast radius.
- **Four ways to ask.** Broad traversal for a question, shortest path between
  two things, a plain-language explanation of one node, and reverse-impact
  traversal ("what is affected by this?").
- **A work-memory loop.** Question/answer outcomes can be saved against the
  graph and aggregated into lessons, so the graph records how its own past
  answers turned out.
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
  (read the source, run the tests); anything on a graph whose
  `built_at_commit` is behind HEAD (stale graph, confident wrong answers);
  Anvil UI templates as first-class structural nodes — plain `.html`/`.yaml`
  form templates are document types to the detector, so they appear only as
  ghost name references (~95 of them in the current graph), not extracted
  structure; and treating INFERRED or AMBIGUOUS edges as settled.

## 4. Why it works the way it does

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
direction the search walked. This is a standing property of the tool, not a
one-off bug: every surprising negative path result gets a second attempt in
undirected mode before being believed.

**Why `graphify-out/` is gitignored here, though upstream now recommends
committing it.** Upstream's team-setup story targets shared repositories
where a committed map saves every teammate a rebuild. This is a
single-developer environment; the output is a derived artifact, fully
reproducible from committed source at zero API cost, and it mixes
machine-specific files (absolute root marker, AST cache) with
stale-prone derived data. Gitignoring keeps the repo clean and makes provenance
meaningful. This is a tripwire decision, not a closed one: if the output
ever becomes tracked, the hooks decision below must be re-examined with it.

**Why the git hooks and merge driver are not installed.** The hook feature
installs three things inseparably — auto-rebuild hooks plus a union merge
driver for a tracked `graph.json`. The driver resolves conflicts on a file
that is never tracked here, so it is dead weight; the hooks would automate a
refresh that is deliberately run by hand at provenance-relevant moments,
keeping graph currency an explicit, verifiable act rather than a background
one. Revisit only if the gitignore premise above changes.

**Why one shared AGENTS.md managed block.** GBrain and Graphify are the two
mechanisms that write persistent guidance into AGENTS.md; two independent
writers on one file is a write-conflict waiting to happen. One
marker-delimited block (`BEGIN/END GRAPH MEMORY GUIDANCE`, owned via
[[memory-master-explainer|Master Explainer]]) holds a single policy for both — including the
rule that a graph must not be queried for current-state answers when its
provenance lags the checkout. A stale graph misanswers confidently; the
provenance check is what makes "current shape" claims meaningful.

**Why both a CLI and an MCP server exist, and why they always agree.** They
are two frontends to the same `graph.json` — the CLI for mid-task human/agent
invocation, the MCP server for repeated structured tool calls from OpenCode.
Same artifact, so no cross-checking is needed between them; pick whichever
fits the context.

**A worked example that shows the boundary.** Both tools were asked about the
Vault's secret-encryption mechanism. GBrain answered the why — owner-only
vault, TOTP step-up, encryption at rest, governing ADRs. Graphify answered
the where/how — `encrypt()` at a specific line, called by
`save_vault_secret()` and four tests, imported by `vault_service.py`, each
edge EXTRACTED. The answers agreed, and each sat at the trustworthy end of
its own tool's confidence scale — that agreement is the signal. Had either
been low-confidence, the same agreement would have been a lead to verify
rather than a settled answer.

**Open architectural questions.** Upgrade timing: the installed 0.9.40 lags
PyPI's 0.9.56; upstream has since added PR-triage dashboards, HTTP MCP
serving, and a team-setup model that assumes a committed graph — none
adopted here, all requiring a deliberate re-decision against the standing
ones above. Whether the AGENTS.md guidance block should ever travel with the
repo versus staying machine-local is deliberately open (tracked in
[[memory-master-explainer|Master Explainer]]). Whether the `--exclude` flag functions in
0.9.40 is unverified (see [[graphify-config|Graphify Configuration]] open items).

## 5. Config maintenance

Graphify has been under standing configuration management since 2026-09-14 via
the `mb-config-graphify` exam skill (canonical source [[graphify-skill|Graphify Skill]] in
this folder; the installed copy at
`~/.config/opencode/skills/mb-config-graphify/SKILL.md` is the only executing
one, per the mb-config-manager copy-never-move install discipline). The exam is
detection and verification only — it verifies the installed toolchain identity
(CLI, package, skill surface), the mb-3-cs scope configuration, the graph
artifact's provenance and shape, the OpenCode integration surfaces (MCP entry,
AGENTS.md block markers, plugin files), and functional liveness of the read-only
query surfaces. Graphify is working well; the exam repairs nothing — findings
route to a developer gate per the mb-config-manager architecture
([[config-manager-explainer|Explainer]]), and spec-doc corrections are
flagged to docs governance, never applied by the exam. Graphify is a member of
the memory family (developer-stated 2026-09-14): at the close-out of each of
its runs, [[memory-master-explainer|Master Explainer]] is updated to current
verified state — standing rule, committed as its own commit. Exams run on
demand, never scheduled.

## 6. S.W.O.T.

**Strengths.** Deterministic code-side extraction — free, offline, reproducible;
an honest three-label confidence model carried on every edge; a checkable
provenance discipline (`built_at_commit` vs HEAD) that makes graph currency a
verifiable fact rather than an assumption; one shared artifact behind the CLI
and MCP frontends, so the two surfaces cannot disagree; gitignored derived
output keeps the repo clean and provenance meaningful.

**Weaknesses.** Single-project scope — the one real graph serves mb-3-cs,
which is paused, so the tool currently has no active project to serve; the
undirected-storage vs directed-traversal default trap recurs on every path
query; Anvil UI templates appear only as ghost name references, never
extracted structure; community labels are deterministic representative-node
names (no LLM labeling installed); the installed version deliberately lags
upstream with no auto-update path.

**Opportunities.** The 0.9.56 upgrade would add PR-triage dashboards, HTTP MCP
transport, and multi-project serving — each requiring a deliberate re-decision
against the standing ones; other projects' repos become graphable as they
activate; the `--postgres` extraction path is unused and could graph database
schemas when PDLF work resumes.

**Threats.** Stale-provenance misanswers — a graph behind HEAD describes code
that no longer exists (mitigated: the provenance check is a standing exam check
and an AGENTS.md block rule); version drift between the installed CLI and the
skill's references (mitigated: the `.graphify_version` marker plus exam Tier 0);
upstream recommendations conflicting with standing decisions could erode them if
re-decided casually (mitigated: this explainer records the reasoning; the
gitignore premise is a tripwire, not a default); guard-rule changes could
reclassify which checks are agent-runnable (mitigated: denials are always
honored and reclassified developer-run immediately).

*Companion documents: [[graphify-config|Graphify Configuration]] (current state — the spec the exam
runs against), [[graphify-reference|Graphify Reference]] (commands and rules),
[[graphify-exam-plan|Exam Plan]] (next run's job-spec — transient contents),
[[graphify-exam-report|Exam Report]] (current verified state, no history),
[[graphify-log|Log]] (chronological notable events), [[graphify-learnings|Learnings]]
(transient exam knowledge), [[graphify-skill|Graphify Skill]] (exam skill — canonical source;
the installed copy is the only executing one). Cross-component reasoning:
[[memory-master-explainer|Master Explainer]].*
