# Investigation Report — The Custom Six-Skill Pipeline and the GBrain Dream Cycle
*Prepared to support planning a "learning → self-healing → refining" loop. Combines what I
have on record from earlier work in this system with what I've now verified directly from
GBrain's own current documentation. Sources are marked throughout — this report keeps the
two apart deliberately, since one is solid ground and the other needs to be checked against
what's actually on disk.*

---

## 1. Why this matters right now

While building out the PDLF explainer, you raised the idea of an inherent
learning/self-healing/refining loop in the system. PDLF's own documentation doesn't define
one. But something adjacent to exactly that already exists, was already built once, and may
now need re-evaluating given today's news that GBrain's underlying issues have been fixed.
This report exists to give you a clean base to investigate from, rather than starting that
investigation from memory alone.

---

## 2. What the native GBrain Dream Cycle actually is (verified against GBrain's own current docs)

GBrain ships with a built-in autonomous maintenance mechanism, cron-driven, that runs while
nobody is actively working. Per GBrain's own README, the loop is described as:

> signal → search → respond → write → auto-link → sync

with the **cron-driven enrichment** stage running overnight-style maintenance:
- Dedup people/entity pages
- Fix citations
- Score salience
- **Find contradictions** — specifically called out, and wired into a dedicated eval
  (`gbrain eval suspected-contradictions`), described as sampling retrieval pairs with a
  date pre-filter and an LLM judge, with a persistent cache
- Prep next-day tasks

This is a real, autonomous, non-human-triggered process. It is the closest thing GBrain
itself has to a "self-healing" mechanism — it operates on the *quality and internal
consistency of the brain's own content*, not on PDLF's build artifacts or code.

One structural detail worth knowing: GBrain organizes content as **brains** (databases) and
**sources** (repos registered inside a brain) — a single brain can hold many project sources
at once. Cross-source querying is possible but not automatic by default; a query has to
explicitly nominate an additional source to reach beyond its own pinned default. This is
relevant background, not the main subject of this report, but it's the same finding that
corrected the "compounds across every project indefinitely" claim earlier — worth keeping in
mind when investigating scope.

---

## 3. What I have on record about your own GBrain history in this system

This section is from memory of earlier work in this system, not from a document uploaded in
this conversation — flagged clearly so you know to verify it against what's actually on disk
rather than take it as confirmed fact.

**The audit finding.** At some point, a GBrain audit was run against your setup and scored
poorly. The stated cause: **the dream cycle had never actually run.** Whatever the native
mechanism described in Section 2 is supposed to be doing autonomously, it wasn't happening —
the brain wasn't being enriched, deduplicated, or contradiction-checked on any cadence.

**Why you didn't just fix the native dream cycle directly.** Two specific obstacles are on
record:
1. **Anthropic API pricing wasn't viable for your use case** — the dream cycle's LLM calls
   (synthesis, contradiction-judging, citation-fixing) presumably default toward
   higher-cost models, and running that autonomously and repeatedly wasn't affordable at
   your usage pattern.
2. **Upstream GBrain bugs were blocking alternative model routing** — you wanted to point
   the dream cycle's LLM calls at cheaper models instead, and hit bugs in GBrain itself that
   prevented that routing from working.

**The decision made as a result.** Rather than forking GBrain's internals to fix the routing
bug yourself — a maintenance burden against someone else's actively-developed codebase — you
made an explicit, deliberate decision **not** to fork, and instead designed a custom
replacement.

**Separately, also on record:** a distinct set of operational GBrain problems were found and
fixed in an earlier session — `pg_toast` corruption, PGLite WASM failures caused by OpenCode
holding the database lock during a CLI sync, and the resulting operational rule that `gbrain
sync` must only run when OpenCode is fully stopped, with `--strategy code` required
specifically for mb-3-cs syncs. A stale reranker configuration (`ZEROENTROPY_API_KEY` missing,
230 failed audit log entries over three weeks) was also found and fixed by supplying the key.
These are likely related context — a GBrain setup with enough friction to need this much
manual repair is exactly the kind of environment where the native dream cycle would also be
failing quietly — but I don't have a document confirming they're the *same* root cause as the
dream-cycle-never-ran finding. Worth checking as part of the investigation.

---

## 4. The custom six-skill pipeline, as designed

Six named skills, on record: **synthesize, consolidate, citation-repair, fact-extract,
contradiction-check, pattern-detect** — explicitly built "to replicate dream cycle value
using affordable models." `gbrain sync` and `gbrain embed --stale` were established as
mandatory closing steps of this pipeline.

I don't have the actual skill definition files for any of these six — what follows is an
informed mapping against the native dream cycle's real, documented components (Section 2),
not confirmed content. Treat this as a hypothesis to check against what's actually on disk,
not as established fact:

| Custom skill | Likely native dream-cycle equivalent |
|---|---|
| `contradiction-check` | The native `gbrain eval suspected-contradictions` mechanism — near-certain match, GBrain's own docs use almost this exact term. |
| `citation-repair` | The native "fix citations" enrichment step — near-certain match by name. |
| `consolidate` | Likely the native "dedup people/entity pages" step, generalized. |
| `synthesize` | Possibly a custom equivalent to `gbrain think`'s synthesis-with-citations behavior, run as a batch/cron job rather than per-query. |
| `fact-extract` | No obvious one-to-one native equivalent named in what I've read — could correspond to entity/edge extraction (GBrain's auto-linking, which fires on every page write and extracts entity references with zero LLM calls) — but that's a stretch, worth confirming directly. |
| `pattern-detect` | No native equivalent I can identify from what I've verified — this may be a genuinely custom addition beyond what dream cycle itself does, or may correspond to "score salience." Unclear. |

---

## 5. What's genuinely unknown — the actual open questions for investigation

This is the core of what this report is for. Everything below needs checking against the
real, current state of your system, not assumed from memory:

1. **Was the six-skill pipeline ever actually built as real, invocable skill files** — or
   did the decision get made and documented, without the skills themselves being written?
   Check for skill definition files matching these six names, and where they'd logically
   live (likely alongside GStack/Matt Pocock skills, or in a dedicated custom-skills-store
   location per this system's established conventions).

2. **If built, has it ever actually run?** On what cadence — manual invocation, a cron job,
   something else? Is there any log or ledger record of a run having happened?

3. **You mentioned today that GBrain's issues have been fixed and can now be tested.** Does
   that specifically mean:
   - The model-routing bug that blocked the native dream cycle is resolved, meaning the
     *native* mechanism might now be usable directly, potentially making the custom
     pipeline unnecessary going forward? Or
   - A different, unrelated GBrain issue was fixed, and the routing/pricing problem behind
     the original decision still stands?

4. **Re-run the original audit.** The finding that triggered this whole investigation was "the
   dream cycle never ran" — that's directly, mechanically checkable right now. `gbrain
   doctor` and the eval framework (Section 2) can confirm current dream-cycle run history and
   brain quality score. This is the single most useful first action — it tells you, in one
   command, whether either mechanism (native or custom) has been doing its job.

5. **If both the native dream cycle and the custom six-skill pipeline are now viable**, that's
   a genuine decision to make, not an automatic default: run native (simpler, one less thing
   you maintain, but subject to whatever cost/routing constraints originally existed), run the
   custom pipeline (more control, more maintenance burden, already designed for your specific
   cost constraints), or some hybrid where the custom pipeline only runs the parts native
   doesn't cover well.

---

## 6. Recommended next steps, in order

1. Run `gbrain doctor` and check dream-cycle-related health indicators directly — establishes
   current, factual ground truth before anything else.
2. Search the filesystem for the six named skills, to confirm whether they exist as real
   files or only as a documented decision.
3. If they exist, check for any run history, log, or ledger record showing whether they've
   ever actually executed.
4. Confirm precisely what "GBrain issues have been fixed" refers to — specifically whether it
   touches the original model-routing bug or the Anthropic pricing constraint.
5. Once 1–4 are answered, the native-vs-custom-vs-hybrid decision in Section 5, point 5
   becomes a concrete, informed choice rather than a guess.

This report deliberately stops here — at "here's what to check," not "here's the plan" —
since steps 1–4 will change what the actual right plan is.
