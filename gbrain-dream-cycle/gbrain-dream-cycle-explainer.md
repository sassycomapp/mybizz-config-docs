---
title: "gbrain-dream-cycle-explainer"
doc-id: "mb-957d54e7"
updated: "2026-10-20"
---
# GBrain Dream Cycle — Explainer

*Companion note: for current state see
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-config.md). For commands and the mandatory
post-run verification procedure, see
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-reference|Reference: Invocation, Verification, Diagnostics]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-reference.md).
For what differs from the standard and why, see
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-learnings.md). For the full 23-phase sequence and
the cross-component framing, see [[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md)
§4.*

---

## 1. What It Is

The Dream Cycle is GBrain's own deepening mechanism: a long, fixed sequence of
23 phases that runs against everything already stored in the brain and builds
a deeper, more structured understanding of it — extracting facts, attempting
code-symbol relationships, scanning for contradictions, synthesizing concepts
across documents, proposing and grading its own interpretive conclusions, and
maintaining the brain's hygiene. Ordinary GBrain search answers "find me
something related to X"; the Dream Cycle does the different kind of work that
makes GBrain's memory more than a pile of separately-searchable pages.

Two framings of its phase structure exist: the confirmed 23-phase sequence for
this environment — grouped in [[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) §4
as housekeeping, extraction, synthesis, judgment/calibration and maintenance —
and upstream's simplified harness-side framing (entity sweep → citation repair
→ consolidation → sync). The 23-phase list is the operative one here.

Three structural facts define it. **It is advisory** — it operates only on
GBrain's stored content, has no authority over real files, and nothing it
produces overrides a repository, an ADR, or a spec. **It is ungovernable** —
Memory Governor structurally cannot intercept it (a permanent limit), so its
output reaches durable memory unreviewed; the compensation is a manual,
always-applied discipline: every dream run is followed by a
suspected-contradictions evaluation whose findings get reviewed. And **it runs
only when invoked** — by hand, weekly, after the Sunday backup. Scheduled
automation is deliberately not used; §4 gives the reasons.

## 2. What It Can Do

- **Fact extraction** (`extract_facts`, `extract_atoms`) — pull discrete,
  structured facts out of stored documents; `extract_atoms` makes its own
  Anthropic calls and is the phase most exposed to credential failure.
- **Code-symbol relationship resolution** (`resolve_symbol_edges`) — GBrain's
  own attempt at the call graph, permanently partial (see §4).
- **Contradiction surface** — the cycle's output feeds the
  suspected-contradictions evaluation that follows every run.
- **Concept synthesis and pattern-finding** (`patterns`,
  `synthesize_concepts`, `consolidate`) — higher-level concept pages
  summarizing many individual facts; near-duplicate consolidation.
- **Self-judgment and calibration** (`propose_takes`, `grade_takes`,
  `calibration_profile`, `drift`) — the system proposing interpretive
  conclusions, grading its own confidence, and tracking drift.
- **Maintenance and closure** (`enrich_thin`, `embed`, `orphans`,
  `schema-suggest`, `purge`) — filling thin pages, embedding new content,
  reporting disconnected pages (the orphans phase reports and does not fix, so
  deepening can outpace linking), suggesting schema improvements, and
  hard-deleting pages soft-deleted beyond the recovery window.

## 3. Suitability

**Best for:** periodic deepening of an already-synced brain — after ingestion
bursts, before design or review work that depends on synthesized
understanding; surfacing contradictions between stored documents; keeping
concept pages and fact coverage current without manual per-page effort.

**Good for:** source-scoped refreshes (`--source`) after heavy work in one
project; targeted single-phase re-runs during diagnosis; the emotional-weight
and calibration passes that keep GBrain's self-assessment honest.

**Not good for:** replacing `gbrain sync` — different operations, different
bookkeeping; a dream that "completed" does not mean sources are fresh, and
freshness counters do not prove a dream did work. Producing governed memory —
its output is structurally outside Memory Governor's reach, which is why the
post-run contradiction discipline exists. Running unattended — every run needs
a person present to verify it; an unattended failing cycle would degrade the
brain invisibly. Resolving the code call graph — permanently partial; Graphify
owns that.

## 4. Why It Works This Way

**Why it runs by hand, weekly, after the Sunday backup.** Upstream designs the
dream cycle as an autonomous nightly cron — "the most important cron job," part
of a large self-running schedule. MyBizz deliberately runs it the other way.
The cycle is expensive and content-changing; its failure modes are silent (a
phase can fail and report only a bare count with the real error swallowed —
`extract_atoms` is the documented case); and its output is the one memory path
nothing governs. A person present at every run, a fresh backup underneath it,
and mandatory verification after it are the standing compensations. Scheduled
automation optimizes for freshness; MyBizz optimizes for governance — and an
unattended cycle cannot be verified at all.

**Why the contradiction discipline exists.** Because Memory Governor
structurally cannot intercept the cycle, its output reaches durable memory
unreviewed. The always-applied compensation is the suspected-contradictions
evaluation immediately after every run, with every finding reviewed before the
run counts as complete (procedure: [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-reference|Reference]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-reference.md),
step 4).

**Why `cycle_freshness` FAIL is the expected state.** Dream and sync keep
different bookkeeping: the freshness stamp updates only when the cycle's sync
phase actually processes new commits. A dream over an already-fresh brain
stamps nothing, so the doctor check reports FAIL until new commits are
processed — a mechanism to understand, not a fault to fix.

**Why `resolve_symbol_edges` stays partial.** `code` is `extractable: false`
in every bundled schema pack, so the phase returns symbol names without
resolved edges. Resolved cross-file relationships are Graphify's job, by
design.

**Where it sits.** Within the six-component memory system (see
[[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md)'s system context), the Dream Cycle is the
deepening layer of GBrain itself. Its relationships: **GBrain** owns it (it
deepens GBrain's own stored content); **Memory Governor** cannot see it (the
manual contradiction discipline is the standing compensation); **PostgreSQL**
carries its output; **mb-submit-memory** is its governed opposite — the two
paths write different layers (facts vs pages) and neither substitutes for the
other; **gstack** supplies the `/sync-gbrain --dream` trigger, whose
orchestrator carries the source-overlap trap (see
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-reference|Reference]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-reference.md)); **Graphify** owns resolved
call-graph work. [[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md)'s four-mechanism
framing places it as the third mechanism, with the same permanent limits.
External recognition: another memory project's feature request models its own
consolidation directly on this cycle — evidence the design is the
differentiator.

## 5. What Has to Happen

- Autopilot and schedulers stay off. Doctor's remediation advice to install
  autopilot is deliberately not followed (L2).
- The cycle runs by hand weekly, after the Sunday backup, through
  `/mb-memory-system-diagnostic`.
- After every run, the contradiction check runs and its findings are reviewed.
- `ANTHROPIC_API_KEY` stays present and valid; its presence and validity are
  developer-run checks ([[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-config.md), Provider
  dependency).
- Sources keep syncing through the standing sync script; a dream does not
  substitute for a sync.
- Cross-repository links, when missing after a run, are restored by the sync
  script's full read.
- The weekly run's real work is verified with the reference's post-run
  procedure — an unverified run is an unknown-state run.

---

*Companion documents:
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-config.md) (state),
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-reference|Reference: Invocation, Verification, Diagnostics]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-reference.md)
(procedures and post-run verification),
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-learnings.md) (what differs and why).
Cross-component framing: [[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) §4.*
