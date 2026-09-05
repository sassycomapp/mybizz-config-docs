# Sentinel — What It Is, What It Does, and Why It Matters

## The Problem, Before Sentinel

The applications being built through PDLF will hold real client money, real client data, and, one layer further down, real personal information belonging to their clients' own customers. Every line of code in these applications is written by an AI agent, not by a developer reading and personally checking each function before it ships. That is not a hypothetical risk profile and not a weakness to apologize for — it is simply the real, structural situation this whole project is built around.

That situation creates one specific, well-documented failure mode, and it has a name: an AI agent can produce code that looks completely correct, passes a casual read, and is subtly, dangerously wrong. Not because the agent is careless — because a security flaw rarely announces itself. It looks like ordinary, working code, missing the one check nobody happened to write. A server function that returns exactly the right data in every test, and also, quietly, someone else's. A payment amount trusted from the client instead of computed on the server. A pattern the project's own architecture explicitly and permanently forbids, written anyway, because it happens to be the far more common pattern in the rest of the world's training data.

This is not a new or speculative concern. It is named directly, with a citation, inside this project's own compliance research: an AI agent can fabricate or assert compliance without it being true, and can perform a harmful action that never surfaces in a way anyone would notice until much later. Sentinel exists specifically to close this one gap — not general code quality, not testing, not performance. Security, checked at the exact moments it actually matters, using real, written standards instead of a general sense of caution.

## What Sentinel Actually Is — the Four-Layer Chain

Sentinel is not a standalone security agent, and it does not run continuously. It is an orchestration layer, sitting on top of four distinct components, each with one job and no overlap with the others:

**The security standards library is the authority.** A real, written body of documents — currently 54 of them, organized into seven categories — describing, in concrete and checkable terms, what "secure" actually means for this specific project: which patterns are approved, which are prohibited, and why.

**GBrain is retrieval only, never authority.** This is the same rule already governing every other part of this system's memory: GBrain helps locate where relevant knowledge lives, but the real answer always comes from reading the real, current document — never from what GBrain remembers about it. Sentinel never reasons from a GBrain summary of a security rule; it opens and reads the actual file.

**Sentinel itself is the reasoning layer.** It decides *when* a security question needs asking — based on which PDLF step just occurred — and applies the library's real, specific standards to the real, specific thing being built. Sentinel does not invent security judgment from scratch; it borrows an existing, purpose-built reasoning methodology — the `secure-software-engineering` skill, from the `magnus919/agent-skills` repository — as its actual thinking process, the same way a specific tool is picked up for a specific job rather than reinvented each time.

**PDLF owns enforcement.** Sentinel never fixes anything. Every real finding becomes a row in PDLF's own, already-existing findings table — the same table and the same review discipline already used for every other kind of finding this project produces. Sentinel adds a new *kind* of entry to a mechanism that already existed; it does not build a second, competing system alongside it.

## What Sentinel Deliberately Does Not Duplicate

Before any of Sentinel's own components were built, a real, deliberate check was made for security capability that already existed elsewhere in this environment — and a genuine amount of it did.

A whole-codebase security audit tool — GStack's `/cso` (Chief Security Officer Audit) — already exists, with two real, distinct modes: a daily mode, deliberately tuned to near-zero noise so it only reports what it's genuinely confident about, and a monthly comprehensive mode that casts a much wider net and reports weaker signals honestly labeled as tentative. It covers real, broad territory — secrets scattered through git history, the full dependency supply chain, CI/CD pipeline risk, AI-specific risks like prompt injection and unbounded LLM calls, and standard frameworks like the OWASP Top 10 and STRIDE threat modeling. This tool and Sentinel are not one calling the other — they operate on entirely different rhythms. The audit tool sweeps the whole codebase periodically. Sentinel checks one specific, narrow thing, at one specific moment, triggered by one specific PDLF step. Neither replaces the other.

A dedicated security specialist — living inside GStack's `/review`, which is what PDLF's own Step 37 code-review already invokes — sits confirmed, on inspection, to be real but under-used: invoked in principle, rarely exercised in practice. Sentinel's own arrival doesn't replace this either; if anything, it's a second, independent example of the same underlying gap Sentinel exists to close — real security capability that already existed, sitting mostly idle because nothing forced it to actually run.

This distinction matters for the same reason it mattered when this whole compliance effort first began, hours earlier the same night: building something new without first checking what already existed would have meant duplicating real, working capability for no benefit — the opposite of the minimum-necessary-complexity standard this entire project holds itself to.

## The Security Library Itself — Read the Real Architecture First

Here is the part of Sentinel's own story that most explainers of a tool like this would skip, and it matters more than anything else in how it actually works: Sentinel did not invent the project's security knowledge. It found most of it already sitting there, correctly written, already approved, inside the project's own existing specifications and architectural decisions — the real Vault system design, the real RBAC role table, the real five-app data-isolation model, the real payment-gateway ADRs. Confirmed directly, document by document, before a single new file was written: eight of the fourteen original library categories were already fully covered by material that already existed. Building a second, duplicate copy of any of it would have been exactly the kind of unnecessary complexity this whole system was built to avoid.

Only six categories were genuinely empty — principles, requirements, threat-models, infrastructure, cloud, and testing — and only those six received new, purpose-written content: 54 documents in total, every one of them grounded in a real fact already established somewhere else in this project's own history, not invented from a generic security checklist. A threat model describing broken access control inside a single client instance, for example, exists specifically because it needed to be distinguished from a different, already-solved problem — cross-client isolation, which this project's own five-app architecture already guarantees structurally and which this document takes care to say explicitly, so the two are never confused.

## The Step-Intensity Table — Where and How Hard Sentinel Actually Looks

Sentinel does not review everything, everywhere, at maximum intensity. Doing so would produce so much noise that nothing real would ever stand out against it. Instead, it works from a real, specific table pairing individual PDLF steps against a defined level of scrutiny and a defined question:

Domain modeling gets a light check — is anything sensitive or security-relevant even being named. Creating a data table gets a high level of scrutiny — what data actually exists here, and who is genuinely allowed to touch it. Locking the architecture gets the highest level of scrutiny in the whole table — where, precisely, do trust boundaries actually sit. Building real code, and reviewing that code afterward, both get sustained, serious attention — does this implementation introduce a real vulnerability, and separately, can whatever controls were implemented actually be bypassed. A step not on this table at all gets no review, immediately, with no further action — a deliberate, stated choice, not an oversight.

## The Three Real Outcomes — Why "I Don't Know" Is a Required Answer, Not a Failure

Sentinel reaches exactly one of three outcomes for any review it actually performs: **Clear**, meaning no real concern was found; **Flag**, meaning a real, describable concern exists; or **Escalate**, meaning there genuinely was not enough evidence or confidence to decide either way.

That third outcome is not a weakness in the design — it is the design. A system built to only ever answer "clear" or "flag" will, sooner or later, be forced into guessing when it genuinely does not know, and a confident wrong guess is a strictly worse outcome than an honest admission of uncertainty. This is the same principle already governing every other part of this project's compliance work: verify, or say plainly that verification wasn't possible — never assert something as fact because asserting it felt more useful than admitting doubt.

## How a Real Review Actually Happens, Start to Finish

When a listed step occurs, Sentinel identifies exactly which real document in the library applies — not a category, a specific file, matched to the specific step and the specific feature involved. It reads that document in full, every single time, never reasoning from a filename or a remembered summary. It then compares the real, specific thing being built against that document's own approved and prohibited patterns, using the borrowed security-reasoning methodology described earlier, and reaches one of the three real outcomes.

A **Clear** result writes its own row into PDLF's findings table, resolved immediately, since there is nothing left for a human to review — a real, deliberate correction to an earlier version of Sentinel, described below. A **Flag** or an **Escalate** also writes a real row, using the exact same structured fields as every other kind of finding this project already tracks: what the concern actually is, what asset is at risk, who or what could exploit it, what evidence supports the finding, how severe it is, how confident Sentinel actually is, and what it recommends. Then it stops. Sentinel does not, under any circumstance, implement its own recommendation. The finding sits, exactly as PDLF's own existing findings already do, waiting for a real, explicit human decision before anything happens to it — and if that decision is to fix it, the fix itself goes through PDLF's own ordinary build-review-test cycle, the same path any other real change takes.

## Two Real Mistakes, Found and Fixed After Sentinel Was Already Built

Sentinel's first working version had two real, structural gaps, and both are worth telling honestly, not smoothing over, because the way they were found and closed says as much about this project's own discipline as Sentinel's design does.

**The first gap: a Clear result left no trace of itself anywhere.** Once a conversation ended, there was no way to later prove a review had actually happened and found nothing — only a transcript that might no longer even exist. This was found by directly asking the plain question "is anything still missing here," rather than assuming a finished-looking system was actually finished. The fix was small and precise: the findings table gained one new allowed value specifically for this case, and Sentinel itself was rewritten so a Clear outcome now writes a real, immediately-resolved row, the same as any other outcome — closing the exact gap that prompted the question.

**The second gap: nothing verified Sentinel had actually been invoked at all.** The instruction to run it lived entirely inside a step's own written procedure — real, but only ever a request, never a guarantee, exactly the same category of risk this project's whole compliance-architecture effort exists to eliminate everywhere else. The fix mirrors a pattern already proven elsewhere in this pipeline: the step itself now cannot proceed to its own approval gate without first confirming a real, verifiable row exists proving Sentinel genuinely ran. No row, no gate — the step stops and asks a human, rather than trusting that a written instruction was actually followed.

Both fixes were applied consistently everywhere they needed to be — the skill itself, the one real step file currently using it, that step's own diagram, and its own build history — and both were verified live, against the real, running database, before being treated as closed.

## When Sentinel Actually Runs

Sentinel is not something run manually, the way a document-maintenance tool might be. It is meant to be triggered automatically, from inside a PDLF step's own procedure, at the exact points already identified as carrying real security weight. As more of PDLF's own 46 steps get built, more of Sentinel's own checkpoints become real and usable — a step that doesn't exist yet has nothing for Sentinel to attach to, and its place in the table stays exactly what it is: a real, confirmed intention, not yet exercised.

## A Related but Genuinely Different Mechanism

A second, separate system in this environment, built on a real, independent policy-enforcement tool, exists to turn a written rule into a mechanical, always-on check — the same forbidden action blocked identically, every single time, with no reasoning involved at all. It is easy to mistake for Sentinel, and worth being precise about why it isn't the same thing.

That mechanism is for the things that are always wrong, with no exceptions and no judgment required — a specific forbidden command, a specific forbidden pattern. Sentinel is for the opposite kind of question — the one that cannot be reduced to a fixed pattern, and genuinely requires reading a real document and reasoning about a real, specific feature before an honest answer is possible. Neither replaces the other, and neither was designed to.
