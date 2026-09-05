# mb-submit-memory — Explainer

*Companion note: for current confirmed state (location, prerequisites,
environment, open items) see `mb-submit-memory-config.md`. For exact
invocation syntax and the full step cycle, see `mb-submit-memory-reference.md`.*

---

## 1. Why this skill exists

`gbrain remember` and `gbrain sync` both write directly into durable GBrain
memory with no check on whether the content is actually true, non-contradictory,
or provenance-clean — that's precisely the ungoverned-write gap
`memory-governor` exists to close (see `memory-governor-explainer.md` §1).
A governor with no correct, habitual way to reach it doesn't help, though —
if raw `gbrain remember`/`sync` are still sitting right there as an easier
path, they'll get used out of habit under time pressure. `mb-submit-memory`
exists to be that single correct path: the *only* sanctioned way a developer
or a PDLF step submits real content into memory, deliberately narrower and
less convenient than calling GBrain directly, on purpose.

## 2. Why it pauses instead of running fully autonomously

The skill forms a genuine confidence score and contradiction judgment (Section
2, Step 3) — but it does not act on that judgment unilaterally. It reports its
findings and stops, waiting for the developer's explicit approval in the same
run before calling the governor's API at all. This mirrors the governor's own
design principle (see `memory-governor-config.md`'s decision engine: only
`auto_promote` or `needs_review`, never an automatic reject/quarantine) —
judgment forms the recommendation, but a human confirms anything with real
consequence. The developer's correction, if given, is authoritative and
submitted exactly as returned, not blended with the original judgment.

## 3. Why folders are never submitted as one unit

Batching would mean one confidence score and one contradiction check standing
in for content that may vary wildly file to file — exactly the kind of
shortcut Section 0's "no placeholder value" rule is meant to prevent. Every
file gets its own independently-formed judgment, even inside a single
`/mb-submit-memory (folder)` run.

## 4. The confidence-scoring method — and why it's honest about its own nature

The three bands (0.85+, 0.5–0.85, below 0.5) are explicitly tagged
`"method": "model_based"` in every submission — a deliberate acknowledgment
that this is a real reading-comprehension judgment, not a rule the developer
has personally verified line-by-line. This honesty matters downstream: the
governor's high-risk-type and contradiction logic can weigh a `model_based`
score differently than a hypothetical developer-verified one, and nothing in
this pipeline pretends otherwise.

## 5. A real worked incident — the 2026-08-27 submission

The only confirmed real run to date is directly instructive, both for how the
supersession/contradiction distinction actually plays out and for the
operational failure modes that surfaced around it.

**What happened:** a developer directly submitted
`spec-postgres-ledger.md` from the PDLF docs repo. GBrain's `recall` on
specific content phrases came back empty, but a broader hybrid query
surfaced the *prior, pre-edit* version of the same page. The file had been
live-verified against the real Postgres ledger that same session, so this
was correctly judged **not a contradiction** — it was the deliberate,
correct replacement of an already-known-outdated fact. Confidence: 0.85
(top band — clearly stated, and the only related content found was the
thing it was correctly superseding). Contradiction object: `detected=true`,
`resolution=closed_by_new_fact`, `cross_project=false`. The governor
auto-promoted it (`decision_path=auto_promote`, `risk_level=low`).

**What the same run surfaced as real operational lessons** (recorded verbatim
in `learnings.md`, summarized here):

- **The governor has no dotenv autoload.** Starting `uvicorn app.main:app`
  without first sourcing `~/memory-governor/.env` leaves it unable to reach
  its own database and with an empty credential registry — every submission
  401s. Not a bug, a real startup-order dependency to remember.
- **`owning_project` must match a real gbrain source ID, or the write silently
  stalls downstream.** The async `gbrain_write` worker (see
  `memory-governor-config.md`'s outbox mechanism) calls
  `gbrain sources default <owning_project>` and raises
  `SourceNotFoundError`, retrying 5× before marking the event
  `permanently_failed`. A candidate can be `promoted` at the API level and
  still never actually reach GBrain if this coupling is broken.
- **Renaming a project ID is a real 3-step transaction, not a plain UPDATE**
  — `memory_candidates.owning_project` is a non-deferrable foreign key.
  Insert the new ID first (copying `display_name`/`dormant`/`created_at`),
  repoint dependent rows, delete the old ID, all inside one transaction.
- **The project registry and gbrain's own source list are two separate
  systems that can drift independently.** A new owning project has to be
  registered with the governor (`POST /memory/projects`) *before* anything
  can be submitted under it — a 404 here is an expected, necessary
  onboarding step, not an error condition.
- **The naming drift this surfaced** — `dev-makepdlf` (gbrain source) vs.
  `makepdlf-project-library` (folder name and governor project, already
  renamed) — is the open item tracked in `mb-submit-memory-config.md`.
