# Memory Governor — Explainer

*Companion note (2026-09-05): for the confirmed real local clone path
(`/home/dev-p/memory-governor`, WSL-native, do not relocate), a live database
check, and the GBrain-source recommendation, see `memory-governor-config.md` §
"Local installation & infrastructure."*

## 1. Opening

An AI agent that writes directly from its own raw output into durable, permanent memory has no check on whether what it just wrote is actually true. This isn't hypothetical — it's a documented failure mode in the field: episodic memory in AI agents introduces unwanted retention, unpredictability, and real deception risk, precisely because memory formation is typically ungoverned. Concretely, in this environment: GBrain's own dream cycle synthesizes concepts and facts from raw project material, and nothing checked those candidates for provenance, contradiction, or risk before they became part of GBrain's durable, queryable memory.

Memory Governor exists to close that gap. It is a control-plane service — provenance-checked, rule-based, audit-logged — sitting between memory generation and durable GBrain storage. No candidate reaches durable, queryable memory without passing through it first. It is a gatekeeping layer, not a memory store in its own right. It does not replace GBrain; it decides what GBrain is allowed to durably remember.

---

## 2. The Decision Engine — Exactly Two Automatic Outcomes

The governor's decision function, `decide_path()`, is fully deterministic and rule-based by design — no AI judgment, no model call, decides a candidate's fate. This is a deliberate tradeoff: adaptive, LLM-judged promotion exists elsewhere in the field, and was rejected here in favor of determinism and auditability.

**The automatic engine may only ever produce one of two outcomes: promote a candidate straight through, or route it to the developer's review list.** This is a real, live design correction, not the original plan — the system's first version allowed the engine to automatically reject or quarantine a candidate on its own, closing it out without the developer ever being told. Direct review caught this, and the design was rewritten: there is no automatic reject and no automatic quarantine. Those become dispositions the developer chooses only when actually resolving a review item.

A candidate routed to review is genuinely blocking — it cannot reach a durable, retrievable state before an explicit developer decision is recorded against it. It carries a **recommendation**, a **validation summary**, and a **ramifications statement**, and may carry a suggested `classification` (a machine-readable reason tag, like `"unresolved_contradiction"`) and a `recommended_action` — but that suggestion is always attached to an open item, never a decision the system has already made.

**This correction was not just designed — it was actually carried through into the live, running code.** The real, already-built engine from earlier in the project still used the old four-outcome logic; a dedicated phase (6.5) rewrote `decide_path()`, added the new `classification`/`recommended_action` fields, and re-ran the entire existing test suite against the corrected version — 240 tests, confirmed passing, before anything further was built on top of it.

---

## 3. Where Confidence and Contradiction Judgments Actually Come From

The governor enforces rules against a candidate's `confidence.score` and `contradiction` status — but it never computes either value itself. Doing so would require exactly the kind of AI judgment the deterministic engine principle rules out.

**Responsibility sits with whichever agent is actually proposing the candidate** — the one with direct, contemporaneous knowledge of what it just did. Before submitting anything, that agent must query GBrain for related existing material, read what comes back, and arrive at a genuine confidence assessment and contradiction determination — never a hardcoded default, never a plausible-looking guess typed in to fill the field. This is a process requirement placed on every writer, not a governor capability: `mb-submit-memory` and PDLF's own step-completion writer both carry this obligation as a mandatory part of their procedure, not an optional nicety.

---

## 4. Contradiction Handling — A Flag, Not a Verdict

Contradiction checking runs for every candidate, every memory type, with no exceptions — an earlier version gated it to only high-risk types, and that gap was corrected.

**A detected contradiction is not, by itself, a judgment that something is wrong.** It only means two things disagree. If a decision was genuinely and deliberately changed later, that's not an error — it's one true fact correctly replacing an earlier one, handled through supersession: the proposing agent, which has direct knowledge the change was intentional, marks the contradiction `resolution: closed_by_new_fact`, and a resolved contradiction doesn't block automatic promotion. Only a genuinely unexplained disagreement — where nothing tells the proposing agent which of two conflicting claims is current — routes to review. The governor never judges on its own whether a past decision was the *right* one; it only judges whether the disagreement has been accounted for.

**Cross-project contradictions are a hard exception.** They always route to review, regardless of confidence score, with no exception path.

---

## 5. Cross-Project Sharing — A Real Gap That Had to Be Found and Built

Every candidate carries `owning_project` and `shared_with` — `[]` for project-local (the default), `["all"]` for globally visible, or an explicit list of named projects. This directly mirrors GBrain's own federated-source pattern, applied one level below the source level.

**A real, genuine gap surfaced during build, worth understanding precisely.** The write-time check — does a candidate's `shared_with` field make internal sense given its declared visibility — was built and tested early. But a completely different question, the read-time one, had gone unbuilt: given a candidate marked shared with project B, does a request actually scoped to project B see it? Checking directly confirmed this: `list_candidates()`'s project filter only ever matched a candidate's *own* project — there was no code path anywhere that resolved cross-project visibility on read, and neither of the relevant endpoints even accepted a parameter identifying which project was asking. This wasn't a minor oversight — it was the actual mechanism the whole sharing model depended on, missing entirely. It was found by checking directly rather than assumed complete, then built properly, with permanent regression coverage added specifically for cross-project read visibility.

---

## 6. Backup and Disaster Recovery — Why Two Writes, Not One

Every promoted memory produces two things, committed together: a human-readable index row, and a full JSON payload of the complete candidate. The index alone was found insufficient for genuine recovery — it has no column for `content.text`, meaning it could tell you a memory existed and what happened to it, but not what it actually said. The two together can fully reconstruct a lost Postgres record; the index alone cannot.

**Postgres and git cannot be committed to atomically together**, so rather than coupling the two into the promotion request itself, the register-and-payload write is asynchronous — a queued, retryable consumer of the same transactional-outbox event mechanism used for every other downstream effect in the system. On failure, it retries with exponential backoff; after five consecutive failures, it stops retrying automatically and surfaces the failure to the developer rather than either blocking the original promotion or retrying silently forever.

This was proven, not just designed: a real disaster-recovery drill deliberately dropped the test database, and Postgres state was reconstructed from the git-tracked register and payload store alone. It was run twice — once early, once again as part of full system integration — confirming the register/payload mechanism holds up once GBrain writes are part of the picture too.

---

## 7. The Event Backbone, and Why There's No Message Broker

Given a single-operator, single-machine deployment, a separate Kafka/Redis/RabbitMQ instance was judged unjustified infrastructure — it would violate the "simple" part of the project's own credo for no benefit at this scale. Instead: a transactional outbox plus Postgres's native `LISTEN`/`NOTIFY`, with one dedicated worker process.

Any state change that should trigger downstream processing — a new candidate, a detected contradiction, a promotion needing a register write or a GBrain write — inserts a row into the same event table, in the same transaction as the state change itself, and issues a `NOTIFY`. A single worker holds a persistent `LISTEN` connection and wakes immediately; it also polls on a fixed interval as a safety net, covering the case where a notification is genuinely missed (the worker was mid-restart, for instance). This single mechanism serves as both the durable event log and the queue — one piece of real infrastructure, not two — and it's what resolves the Postgres/git dual-write problem as well: the register write is just another queued consumer of this same stream. Confirmed live: the notify-driven wake was measured at roughly 0.15 seconds during verification — not a batched or scheduled delay in practice, despite being asynchronous in design.

---

## 8. `mb-submit-memory` — The Real Front End for Manual Submission

The developer's actual way of submitting material for governance is not a raw API call — it's `mb-submit-memory`, an OpenCode skill, invoked as `/mb-submit-memory <path>`. It's deliberately its own skill, not folded into `docs-manager`, `mb-align-docs`, or `mb-wikilinks` — each of those three owns exactly one job and interoperates with nothing else by design, and folding memory-submission into any of them would break that boundary.

It follows the same rhythm already used by those other skills — learnings, backup, detect, report, approve, apply, verify, log — and it carries the full §11A obligation directly: it must query GBrain for related content and read it before submitting, supplying a genuinely reasoned confidence and contradiction assessment, never a placeholder. It was proven, not just built: a real, genuinely new markdown document was pushed through the full real pipeline — save, `/mb-wikilinks`, `/docs-manager`, `/mb-align-docs`, `/mb-submit-memory` — confirming the skill's own GBrain query step actually ran against real content, and that the submitted confidence/contradiction values were traceably derived from that step rather than a fixed default.

---

## 9. The Writer GBrain's Dream Cycle Cannot Actually Be, and Why

This is the single most important structural nuance in the whole system, and it's worth stating precisely rather than glossed over.

**GBrain's dream cycle cannot be routed through the governor at all.** This was not assumed — it was investigated exhaustively. GBrain's `dream` command has no interception point of any kind: no redirect parameter, nothing in its MCP tool schema, nothing exposed via its own config inspection. Dreaming writes directly into GBrain's own database through its own internal engine. Forking GBrain's own source to intercept those writes was considered and rejected — a permanent obligation to re-merge against GBrain's own ongoing releases, forever, for a problem solvable another way.

**The real, working alternative:** `dream` runs in real, distinct, named phases, and GBrain separately ships a real, purpose-built tool — `gbrain eval suspected-contradictions` — confirmed to *not* run automatically as part of the dream cycle; it only reads a cached result from the last deliberate, explicit invocation. The accepted, documented discipline for this one writer: run `dream` for real (never `--dry-run`, which writes nothing and cannot serve as a review step), run `gbrain eval suspected-contradictions` immediately afterward, then review the findings. This is the one honestly-documented exception to "every writer's output is governed through the same API" — a genuine structural limit of governing third-party software with no exposed extension point, named plainly as such rather than quietly left as an unmet promise.

Only two writers actually submit through the governor's real API: manual submission via `mb-submit-memory`, and PDLF's own step-completion writer, using a distinct, dedicated credential (`pdlf_step_sync`) so the governor can always tell which writer a candidate came from.

---

## 10. A Real Incident — An Accidental Write Into Live Memory, and How It Was Recovered

During testing of the GBrain-write logic, a chained script ran several commands in sequence without verifying each one's actual result before letting the next one run. The command meant to create a disposable test source failed cleanly — GBrain requires `sources add`'s target to already be a real, committed git repository, and the test path was just an empty directory. The script didn't stop; the next command, a `remember` call, executed anyway — against whatever source was actually still active, which was the real `mb-3-cs-code` source, not the intended disposable one. A real, permanent fact was written into live memory, and its content was now also factually false, since it claimed to exist only inside a test source that had never actually been created.

**Recovery was deliberate and fully verified at each step, not rushed.** The right tool to find the fact was `recall` (the actual paired read-verb to `remember`), not `search`, which was tried first and returned unrelated content by semantic similarity instead. Once the real `fact_id` was confirmed, `forget` was used to correct it — which **expires a fact, keeping its full audit trail, rather than deleting it outright** — consistent with the project's own standing "never delete, only retire" principle. The correction was independently re-verified afterward via a second `recall` call, rather than trusting the tool's own success response at face value.

**The lasting fix wasn't just the recovery — it was a redesigned test fixture**, built with the specific, hard-won lesson applied directly: create a genuinely git-initialized, committed disposable source first; use a language where a failed step actually halts execution (Python's `subprocess.run(..., check=True)`, not an unguarded bash chain); and use a `try`/`finally` block that unconditionally restores the real, original active source, regardless of whether the test itself succeeds or fails. A standing regression test was added specifically to catch this exact class of failure — leftover disposable test sources from a prior run — permanently.

---

## 11. Known Limitations, Honestly Stated

**GBrain's dream cycle is structurally ungovernable through this system's own API** — covered fully in Section 9. Its content reaches GBrain through a real, deliberate, always-applied manual discipline instead of automated governance, and that's a permanent property of the tool, not a temporary gap.

**Several phases were closed by explicit developer decision, not by completion**, pending PDLF's own real go-live: observing a genuine PDLF step running end-to-end through the governor, and repeated, real dream cycles under ordinary use. A narrower, synthetic substitute for either was considered and deliberately rejected as less honest than waiting for the real thing. This is not an absence of testing — every writer, the GBrain write path, disaster recovery, and cross-project isolation have all been proven live repeatedly; these specific items simply cannot exist before PDLF itself does.

**The governor may observe patterns in its own decision history and propose a policy change, but may never apply one to itself.** Because policy changes are themselves high-risk content, any such self-generated candidate is guaranteed to require human review before anything about the governor's actual behavior changes.

---

## 12. Closing

The governor's entire job is narrow: decide what's allowed to become permanent, trusted memory, using rules a human can audit, never a judgment call it makes for itself. Every real correction described here — the shift from four automatic outcomes to two, the read-time sharing gap that had to be found before it caused a real problem, the accidental write and its careful, verified recovery, the honest acknowledgment that one entire writer simply cannot be governed the way the others are — came from the same discipline: check directly, verify at each step, and never let "should work" stand in for "confirmed working."

---

*Companion documents: `memory-governor-config.md` (current configuration and status), `memory-governor-reference.md` (invocation, worked examples, and incident-response procedure).*

*End of document*
