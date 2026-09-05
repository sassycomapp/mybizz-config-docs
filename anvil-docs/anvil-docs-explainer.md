# Anvil Docs — Explainer

## 1. Opening

This corpus exists to answer one real, recurring problem: building Anvil
applications meant constantly re-deriving the same answers — what does
`anvil.yaml` actually support, how does a given built-in service really
work, what does the real source code do when the official documentation
is ambiguous or silent. This corpus combines both — the real, official
documentation and the real, ground-truth runtime source — organized
together, by subject, so neither has to be found or re-derived from
scratch again.

---

## 2. What This Corpus Actually Is, Structurally

Two genuinely different kinds of real content, deliberately merged:

**Scraped official documentation** — the real, live content of every
page under `anvil.works/docs`, 298 pages across 19 top-level areas,
captured directly via `webfetch` and a validated stripping pipeline that
removes site chrome (navigation, footer) while preserving the real
article content byte-faithfully, including original Unicode
typography.

**Absorbed runtime source code** — real Python and Clojure source,
originally cloned from `github.com/anvil-works/anvil-runtime`
(commit `34067eb`, "Anvil App Server v1.17.0"), then moved into this
same corpus, organized by subject rather than by the runtime's own
internal folder structure.

**The deliberate reorganization is the important part.** The runtime's
own source tree groups things by *how the Anvil Runtime itself is
built* — `services/`, `native_rpc_handlers/`, `dispatcher/`. This
corpus instead groups by *what an app builder is trying to do* —
Stripe code sits with Stripe documentation, Data Tables code sits with
Data Tables documentation. The runtime's own structure was never
meant for this purpose; it was a real, deliberate act of reorganization,
not just a copy.

---

## 3. Real Incidents That Shaped This Corpus

### 3A. An Accidental Wipe, and a Real, Patchwork Recovery

During the scraping phase, a scaffold-generation script was
accidentally re-run against the already-populated corpus, wiping every
scraped page back to its empty placeholder state. Recovery required
reassembling content from several different real sources at once — raw
transcription relays, saved tool-output files for two specific pages,
and direct re-fetches for four pages where no other record existed.

**The genuinely important lesson from this, not just the incident
itself:** the recovery was verified independently — real, programmatic
byte-diffs against fresh re-fetches of the highest-risk files, not
trusted from a self-report. The script responsible was afterward
guarded against accidental re-invocation. If any content in this corpus
is ever suspected of drift, the same direct-diff verification method,
not a summary claim, is the correct way to check it.

### 3B. Real Content Preserved Where a First Pass Would Have Discarded It

Several times during absorption, an initial classification would have
discarded genuinely valuable content by treating it as generic
scaffolding:

- **`database/schema-base.sql` and `schema-runtime.sql`** — originally
  symlinks inside a folder marked for full deletion (`database/`,
  otherwise pure migration tooling). Once confirmed to hold real,
  dereferenced schema content, both were rescued and moved into
  `data-tables/` instead.
- **`client/`'s real, non-vendored JavaScript runtime and 9 real HTML
  files** — an initial pass proposed deleting all of it as
  "platform-internal." Corrected: genuine, non-vendored Anvil client
  code and content is real reference material and was moved into
  `client/`, not discarded. Only a bare `README` (no real content) was
  actually deleted.
- **`tests/apps/SmokeTest/`** — a real, complete, minimal working Anvil
  application (genuine `anvil.yaml` with a real `db_schema`, real
  client/server code) sitting inside a folder otherwise correctly
  treated as disposable CI/test scaffolding. Preserved deliberately as
  concrete, working example material, not discarded as "just tests."

**The standing lesson, applicable to any future addition to this
corpus:** a file's location inside a "scaffolding" or "test" folder is
not, by itself, evidence it lacks real value. Check the actual content
before excluding anything.

### 3C. Symlinks Converted to Plain Text, Not Preserved as Symlinks

The original runtime clone contained 49 real filesystem symlinks —
Anvil's own build-deduplication mechanism, letting `uplink/`,
`downlink/`, and various `server/` build locations share one real copy
of the same client library code without duplicating it.

**These were deliberately converted to plain-text reference notes
before absorption, not preserved as working symlinks, for two real,
confirmed reasons:**

1. **Symlinks created from inside WSL, pointing at a Windows-drive
   target, are invisible to Windows Explorer** — they display as
   empty, 0-byte files, confirmed directly via raw filesystem
   reparse-point inspection during an earlier, unrelated incident in
   this same environment.
2. **This corpus is documentary reference material, never executed** —
   a symlink's real value (letting running code share one file) has no
   purpose here. A plain note recording the same relationship (e.g.
   `email.py.md` stating "same as `services/anvil/email.py`") preserves
   the same *information* without the fragility.

**33 of the 49 became real, genuine `.md` reference notes.** The
remaining 16 had already been independently dereferenced into real,
standalone files before this conversion happened — confirmed,
individually, by direct diff against their real counterparts elsewhere
in this corpus, to be genuine, byte-identical duplicates, and deleted
on that basis, not guessed at.

### 3D. Cross-References Left as Plain Links, Not Converted to Wikilinks

A real, extended investigation considered converting every
cross-reference in this corpus — both the documentation's own internal
links and the 49 symlink relationships — into GBrain `[[wikilink]]`
syntax, specifically to make them resilient to future file moves.

**Confirmed, directly, from `mb-wikilinks`'s own source: this resolver
is scoped to markdown files.** Given a large portion of this corpus's
real cross-references involve non-markdown source files (`.py`, `.clj`),
wikilinks were judged not to cleanly apply corpus-wide. The simpler,
more consistent decision: leave documentation-internal links as plain,
relative markdown links, and record the symlink relationships as plain
text notes (see 3C) — both fixable manually and directly if a future
move breaks them, rather than depending on a resolver whose real scope
doesn't cleanly cover this whole corpus.

### 3E. A Real Process Violation, Caught and Verified

Partway through the runtime-source absorption, several folders were
processed consecutively without pausing for review between them,
directly against the explicit, standing instruction to check in after
every single folder. Given no backup existed at this stage, the
completed folders were independently verified after the fact — real,
direct spot-checks of specific claimed files on disk, not a re-read of
the self-report — before being trusted. All checked out correctly on
inspection, but the process failure itself is the standing lesson:
pacing discipline exists specifically to catch problems before they
compound across multiple folders, and skipping it removes exactly that
safety margin, regardless of how the specific outcome happens to turn
out.

---

## 4. What Was Deliberately Excluded From `server/`, and Why

91 real files from the runtime clone's `server/core/` were deliberately
not absorbed — not an oversight, a considered exclusion, by category:

- **Platform operations** (`worker_pool.clj`, `accounting.clj`,
  `metrics.clj`, `quota.clj`, `cache.clj`) — Anvil's own hosted
  platform's internal traffic-management and billing infrastructure.
  Never seen, configured, or benefited from by an app builder.
- **SSO protocol internals below what app code touches** —
  the low-level OAuth/SAML handshake code. App code calls a much
  higher-level function; this layer is only relevant for debugging a
  genuine protocol-level failure, a rare, deep case.
- **The Runtime's own build/test tooling** (`project.clj`, `core/test/`,
  `.clj-kondo/`) — exists to build and verify the Anvil Runtime's own
  source, with zero relevance to writing an Anvil application.
- **`app-server/`'s own packaging and standalone-hosting code** —
  relevant only to self-hosting the Anvil platform, a deployment model
  this project has explicitly decided never to use.

---

## 5. Known Limitations, Honestly Stated

**`_components.py` is a confirmed, permanent orphan.** Two references
to it existed in the original clone; direct investigation confirmed no
real source file for it exists anywhere in the checkout. This is not
unresolved — it's a confirmed, dead end, recorded honestly rather than
silently dropped.

**This corpus is not yet registered with GBrain.** Real, substantial
content exists here, but it is not yet searchable through GBrain until
that registration happens — a genuine, separate, still-open task.

**No standing backup currently exists for this corpus.** Any future
bulk operation against it should include real, independent
verification at every step — the same discipline this corpus's own
construction required, learned directly through the incidents in
Section 3.

---

*Companion documents: `anvil-docs-config.md` (current state, real
structure), `anvil-docs-reference.md` (navigation, real commands).*

*End of document*
