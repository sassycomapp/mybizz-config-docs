---
title: "sentinel-explainer"
doc-id: "mb-d54f779d"
updated: "2026-10-08"
---
# Sentinel — What It Is, What It Does, and Why It Matters

Companion to [[[mybizz-config-docs:mb-sentinel-review/sentinel-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-config.md) (the spec — current state) and
[[[mybizz-config-docs:mb-sentinel-review/sentinel-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-reference.md) (procedures and worked examples). The
config-management exam set for this suite ([[[mybizz-config-docs:mb-sentinel-review/sentinel-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-exam-plan.md) ·
[[[mybizz-config-docs:mb-sentinel-review/sentinel-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-exam-report.md) · [[[mybizz-config-docs:mb-sentinel-review/sentinel-log|Log]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-log.md) ·
[[[mybizz-config-docs:mb-sentinel-review/sentinel-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-learnings.md) · [[[mybizz-config-docs:mb-sentinel-review/sentinel-skill|Exam Skill]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-skill.md)) is
synthesized and consumed per the [[[mybizz-config-docs:mb-config-manager/config-manager-agent|Config Manager]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-agent.md)
plan-driven cycle — the exam verifies this suite's state and never runs the
subject skill itself.

## The Objective, Stated Plainly

The applications built through PDLF will hold real client money, real
client data, and real personal information belonging to their clients' own
customers. Every line of their code is written by an AI agent. Sentinel
exists for one reason: **so that the applications which come out of the
PDLF system are safe for the developer's clients and their users** — not
hacked, identities not stolen, not robbed. It is build-time safeguarding in
service of shipped-application safety, and it is part of PDLF itself:
pre-built into specific steps, at the specific moments where security
weight sits.

## The Original Concept Source

Sentinel's reasoning methodology is borrowed, not invented — from the
`secure-software-engineering` skill at
`github.com/magnus919/agent-skills/tree/main/secure-software-engineering`
(MIT; a five-phase, prevention-oriented workflow with eleven reference
files — threat modeling, authentication and authorization, input
validation, secrets lifecycle, dependency supply chain, logging and audit,
multi-tenant isolation, secure code review, release evidence, incident
learning, AI/LLM security — plus templates and evals). This is the original
concept source: the collection was researched when Sentinel was conceived,
and its workflow is the reasoning process Sentinel's review step applies.
The skill was installed into this environment on 2026-09-09, after passing
the standing supply-chain review (publisher, licence, maintenance, no
spawn capability).

The design genesis — the original research conversation where the concept
was formed, the alternatives surveyed, and the architecture sketched — is
preserved in this folder as [[[mybizz-config-docs:mb-sentinel-review/sentinel-security-system|SSS - sentinel Security System]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-security-system.md).

Two honesty notes about the borrow: first, the multi-tenant isolation
reference in the collection **does not apply to this platform** — the
governing ADR ([[[default:adr-global/adr-dependency-based-not-multi-tenant|Mybizz CS is a Dependency-Based Architecture, Not a Multi-Tenant Architecture]]](C:/dev/project-library-global/adr-global/adr-dependency-based-not-multi-tenant.md), Sealed)
establishes that cross-client isolation is structural, and the review
vocabulary is within-instance. Second, the skill is a *methodology*, not a
ready-made enforcement mechanism — nothing in it blocks a vulnerable
function from shipping. Its value is that it makes the reviewing agent
better-informed at the moment of judgment.

## What Sentinel Actually Is — the Four-Layer Chain

Sentinel is not a standalone security agent, and it does not run
continuously. It is an orchestration layer, sitting on top of four distinct
components, each with one job and no overlap with the others:

**The security standards library is the authority.** A real, written body
of documents — 54 of them, organized into seven categories — describing, in
concrete and checkable terms, what "secure" actually means for this
specific project: which patterns are approved, which are prohibited, and
why.

**GBrain is retrieval only, never authority.** The same rule governing
every other part of this system's memory: GBrain helps locate where
relevant knowledge lives, but the real answer always comes from reading the
real, current document. Sentinel never reasons from a GBrain summary of a
security rule; it opens and reads the actual file.

**Sentinel itself is the reasoning layer.** It decides *when* a security
question needs asking — based on which PDLF step just occurred — and
applies the library's real, specific standards to the real, specific thing
being built, using the borrowed methodology as its thinking process.

**PDLF owns enforcement.** Sentinel never fixes anything. Every real
finding becomes a row in PDLF's own, already-existing findings table — the
same table and the same review discipline already used for every other
kind of finding this project produces.

## What Sentinel Deliberately Does Not Duplicate

Before any of Sentinel's own components were built, a real, deliberate
check was made for security capability that already existed — and a genuine
amount of it did.

GStack's `/cso` already exists, with two real, distinct modes: a daily
mode, deliberately tuned to near-zero noise, and a monthly comprehensive
mode that casts a much wider net. It covers broad territory — secrets in
git history, the dependency supply chain, CI/CD risk, AI-specific risks,
OWASP and STRIDE. Sentinel and `/cso` are not one calling the other — they
operate on entirely different rhythms: the audit sweeps the whole codebase
periodically; Sentinel checks one specific, narrow thing, at one specific
moment, triggered by one specific PDLF step.

GStack's `/review` contains a security specialist that PDLF's own Step 37
code-review invokes — confirmed real but under-used. Sentinel doesn't
replace this either; it is a second, independent example of the same gap:
real security capability that already existed, sitting mostly idle because
nothing forced it to run.

And a third neighbor must not be conflated: Cupcake — the mechanical
policy-enforcement layer — "keeps honest agents honest": the same forbidden
action blocked identically, every single time, with no reasoning involved.
Sentinel is for the opposite kind of question — the one that cannot be
reduced to a fixed pattern and genuinely requires reading a real document
and reasoning about a real, specific feature. Neither replaces the other,
and neither was designed to.

## The Library Itself — Found, Not Invented

Sentinel did not invent the project's security knowledge. It found most of
it already sitting there, correctly written, inside the project's own
existing specifications and architectural decisions — the real Vault system
design, the real RBAC role table, the real five-app data-isolation model,
the real payment-gateway ADRs. Confirmed document by document before a
single new file was written: eight of the fourteen original library
categories were already fully covered. Only six categories were genuinely
empty — principles, requirements, threat-models, infrastructure, cloud, and
testing — and only those six received new, purpose-written content: 54
documents, every one grounded in a real fact already established in this
project's own history.

## The Step-Intensity Table — Where and How Hard

Sentinel does not review everything, everywhere, at maximum intensity —
that would produce so much noise that nothing real would ever stand out
against it. Instead, it works from a real, specific table pairing individual
PDLF steps against a defined level of scrutiny and a defined question:
domain modeling gets a light check; creating a data table gets high
scrutiny; locking the architecture gets the highest in the whole table;
building real code, and reviewing that code afterward, both get sustained,
serious attention; QA asks whether the requirements can be demonstrated; a
step not on the table at all gets no review — a deliberate, stated choice.

## The Three Real Outcomes — Why "I Don't Know" Is a Required Answer

Sentinel reaches exactly one of three outcomes for any review it actually
performs: **Clear** (no real concern found), **Flag** (a real, describable
concern exists), or **Escalate** (there genuinely was not enough evidence
or confidence to decide either way).

That third outcome is not a weakness in the design — it is the design. A
system built to only ever answer "clear" or "flag" will, sooner or later,
be forced into guessing when it genuinely does not know, and a confident
wrong guess is a strictly worse outcome than an honest admission of
uncertainty.

## The Flag Is a Snake in the Grass — the Three Kinds, and What Each Requires

Every flag is triaged into exactly one of three kinds, and the triage is
where the system's own quality is tested:

- **Legitimate, minimal consequence** — something real happened and does
  not warrant work: thank the flag, set it aside, move on.
- **Illegitimate** — raised with no real problem: **this is a defect in the
  detection itself**, and the detection logic (the rule, the mapping, the
  threshold) must be corrected through the rule pipeline — not just this
  flag dismissed.
- **Legitimate, requires attention** — the normal case: decide, and PDLF's
  ordinary cycle implements.

The same doctrine governs alarms generally: over-warning is preferred to
silence; an alarm with a real event of minimal consequence is legitimate;
an alarm raised with no cause is a fault in the raising system that must be
corrected. The distinction matters because misclassified flags corrupt the
system's trustworthiness — the snake in the grass is the misclassification,
not the flag.

## How a Real Review Actually Happens, Start to Finish

When a listed step occurs, Sentinel identifies exactly which real document
in the library applies — not a category, a specific file, matched to the
specific step and the specific feature involved. It reads that document in
full, every single time. It then compares the real, specific thing being
built against that document's own approved and prohibited patterns, using
the borrowed methodology, and reaches one of the three real outcomes.

A **Clear** result writes its own row into the findings table, resolved
immediately — a real, deliberate correction to an earlier version of
Sentinel. A **Flag** or an **Escalate** also writes a real row, using the
exact same structured fields as every other kind of finding this project
tracks: what the concern actually is, what asset is at risk, who or what
could exploit it, what evidence supports the finding, how severe it is, how
confident Sentinel actually is, and what it recommends. Then it stops. It
does not, under any circumstance, implement its own recommendation.

## Two Real Mistakes, Found and Fixed After Sentinel Was Already Built

**The first gap: a Clear result left no trace of itself anywhere.** Once a
conversation ended, there was no way to later prove a review had actually
happened and found nothing. The fix was small and precise: the findings
table gained one new allowed value specifically for this case, and
Sentinel was rewritten so a Clear outcome now writes a real,
immediately-resolved row — closing the exact gap that prompted the
question.

**The second gap: nothing verified Sentinel had actually been invoked at
all.** The instruction to run it lived entirely inside a step's own written
procedure — real, but only ever a request, never a guarantee. The fix
mirrors a pattern already proven elsewhere in this pipeline: the step
itself now cannot proceed to its own approval gate without first confirming
a real, verifiable row exists proving Sentinel genuinely ran. No row, no
gate — the step stops and asks a human.

Both fixes were applied consistently everywhere they needed to be — the
skill itself, the one real step file currently using it, and its build
history — and both were verified live, against the real, running database,
before being treated as closed.

## When Sentinel Actually Runs

Sentinel is meant to be triggered automatically, from inside a PDLF step's
own procedure, at the exact points already identified as carrying real
security weight. As more of PDLF's own 46 steps get built, more of
Sentinel's own checkpoints become real and usable — a step that doesn't
exist yet has nothing for Sentinel to attach to, and its place in the table
stays exactly what it is: a real, confirmed intention, not yet exercised.

## The Architectural Boundary Sentinel Reviews Within — Read This First

Cross-client data isolation in this platform is **structural**: each client
is a separate Anvil application with its own database, and `app_tables`
resolves to the calling client's own tables — confirmed by live test,
sealed by ADR. This changes what the review looks for in two directions.

First, multi-tenancy patterns are not idioms that need review — they are
**security findings that would replace structural isolation with a
failure-prone filter**. An agent defaulting to a tenant discriminator or a
tenant-filtered query has produced incorrect, less-secure code, and
Sentinel's review catches it against the project's own sealed ADR.

Second, the genuine threats live *within* an instance: user-role access
control, the Vault, input validation, server-side-only data access. The
security library's within-instance threat models exist precisely because
the platform's architecture already solved the cross-client problem
structurally — and the review concentrates on what the architecture cannot
solve: the quality of the code inside one client instance.

## A Related but Genuinely Different Mechanism

A second, separate system in this environment — built on an independent
policy-enforcement tool — turns written rules into mechanical, always-on
checks: the same forbidden action blocked identically every single time,
with no reasoning involved at all. It is easy to mistake for Sentinel, and
the precision matters: **that mechanism keeps honest agents honest** — it
handles the actions that are always wrong with no exceptions and no
judgment required. Sentinel is for the opposite kind of question — the one
that cannot be reduced to a fixed pattern and genuinely requires reading a
real document and reasoning about a real, specific feature before an
honest answer is possible. Neither replaces the other, and neither was
designed to.

## Where Sentinel's Own Parts Live in the Layered Environment

The environment has four named layers — the pre-makePDLF layer, the
makePDLF layer, the PDLF layer, and the shipped estate (full map:
[[pdlf:pdlf-library/pdlf-explainer-docs/pdlf-environment-explainer|the pre-makePDLF, makePDLF, PDLF, and shipped layers]]). Sentinel spans three of them,
and the span is deliberate:

- **Pre-makePDLF (now):** the skill, the security-global library, the
  findings database, and the installed methodology — all built, verified,
  and usable.
- **makePDLF:** the step-intensity wiring — built into each
  Sentinel-covered step file as it is developed (Step 16 done as the
  pattern; Steps 17–46 pending as built).
- **PDLF:** the reviews fire during real step executions — testable
  against a real feature from PDLF's first run.
- **Shipped estate:** out of Sentinel's scope. No runtime safeguards are
  built into the applications; that is a different scope of work, deferred
  until the PDLF steps that scope shipping are developed. The boundary is
  named here so it is never silently crossed.

## Known Limitations, Honestly Stated

**Sentinel has never been run live against a real feature.** Built,
installed, wired into Step 16, with its database path verified live
2026-09-09 — but the first real PDLF-run feature is the test that matters.

**The reasoning is self-review by the writing agent.** The mitigations
(the checkable patterns, the evidence-required rows, the independent
tools) reduce the risk; the developer's triage of every flag into its
three kinds is the standing control.

**Eleven of twelve scoped steps have nothing to retrofit into** — their
intensity numbers remain provisional until each real step file exists.

**The findings table lives on the Windows-side ledger, reachable only
through the documented PowerShell bridge** — a direct WSL database call
silently reaches the wrong server. The bridge is the only route, always.

## Config maintenance — how this system is examined and kept healthy

This suite participates in the config-management system (`mb-config-manager`).
The roles of the seven suite files, and the exam cycle that runs them, are the
architecture described in [[config-manager-explainer|the config-manager
explainer]] — emulated from the PostgreSQL pilot. The short local version:

- [[[mybizz-config-docs:mb-sentinel-review/sentinel-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-config.md) is the **spec** — the ideal state every
  exam checks against.
- Before each exam run, the config-manager synthesizes
  [[[mybizz-config-docs:mb-sentinel-review/sentinel-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-exam-plan.md): a fresh job-spec built from this spec, the
  last report, the log, and the learnings. The plan is transient (the file is
  live; contents rewritten each cycle).
- The exam runs the installed skill (`mb-config-mb-sentinel-review`) with the
  plan in hand — detection fully autonomous; healing gated.
- **Agent-healable items are suite-file repairs only** (the exam set files).
  The installed subject skills, the PDLF step files, the security-global
  library, the governing ADR, and the `triage_findings` database are
  deny-list: changes reach them only as gate proposals the developer approves
  item by item.
- The database route carries a credential by variable name only
  (`PGPASSWORD`, bridge procedure); the exam never reads `.env` contents, and
  the bridge probes are developer-run by proven guard class.
- The run rewrites [[[mybizz-config-docs:mb-sentinel-review/sentinel-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-exam-report.md) (current state, no
  history), appends one row to [[[mybizz-config-docs:mb-sentinel-review/sentinel-log|Log]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-log.md), files new learnings, and
  prunes absorbed entries.

## S.W.O.T.

**Strengths.** A real, written authority (54 security-global documents)
instead of ad-hoc judgment; the borrowed five-phase methodology making the
reviewing agent better-informed at the moment of judgment; three outcomes
with "I don't know" as a required answer; every outcome leaves a queryable
trace (the CLEAR-row correction); the gate-proof pattern proving invocation,
not mere instruction; deliberate non-duplication of /cso, the /review
security specialist, and Cupcake.

**Weaknesses.** Never yet run live against a real feature — the first real
PDLF-run feature is the test that matters. The reasoning is self-review by
the writing agent (mitigated by checkable patterns, evidence-required rows,
and the developer's triage of every flag). Ten of the twelve intensity-table
steps exist as files but carry no wiring yet — coverage depends on the
makePDLF wiring work landing. The installed skill cites a plan-document
filename that no longer exists (recovered under a different name, without
numbered sections).

**Opportunities.** The config-management exam adds standing verification this
system never had; the intensity wiring can land step by step as PDLF builds,
following the Step 16 pattern; learnings graduation can move settled patterns
into the skill itself.

**Threats.** Spec-doc drift between runs silently weakens exams (mitigated:
exams flag spec drift, never edit it). An unwired built step silently skips
its security review — the exact class of failure Sentinel exists to prevent
(mitigated: the exam's built-status and wiring checks surface it every run).
Citation rot — skill content pointing at renamed or restructured documents
(observed: the `sentinel-security-system-plan.md` references).

---

*Companion documents: [[[mybizz-config-docs:mb-sentinel-review/sentinel-config|dev-makepdlf]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-config.md) (current state),
[[[mybizz-config-docs:mb-sentinel-review/sentinel-reference|Usage, Invocation, and Worked Examples]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-reference.md) (procedures and worked examples),
[[[mybizz-config-docs:mb-sentinel-review/sentinel-scope|Scope]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-scope.md) (the agreed scope), [[[mybizz-config-docs:mb-sentinel-review/sentinel-security-system|SSS - sentinel Security System]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-security-system.md)
(the design genesis), the exam set ([[[mybizz-config-docs:mb-sentinel-review/sentinel-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-exam-plan.md) ·
[[[mybizz-config-docs:mb-sentinel-review/sentinel-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-exam-report.md) · [[[mybizz-config-docs:mb-sentinel-review/sentinel-log|Log]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-log.md) ·
[[[mybizz-config-docs:mb-sentinel-review/sentinel-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-learnings.md) · [[[mybizz-config-docs:mb-sentinel-review/sentinel-skill|Exam Skill]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-skill.md)). The reasoning methodology:
`github.com/magnus919/agent-skills/tree/main/secure-software-engineering`.
The full environment map: [[pdlf:pdlf-library/pdlf-explainer-docs/pdlf-environment-explainer|the pre-makePDLF, makePDLF, PDLF, and shipped layers]].*

*End of document*
