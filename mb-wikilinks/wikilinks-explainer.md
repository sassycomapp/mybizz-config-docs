---
document: "wikilinks — Explainer"
doc-id: wikilinks-explainer
state: Live
date-created: 2026-09-10
---

# wikilinks — Explainer

Updated 2026-09-20 to reflect the refactored skill (`SKILL.md`, 2026-09-19):
scope from the single authority list, shared run frame in
[[doc-skills-run-discipline|Shared Run Discipline]], corpus-wide collision census, run-level
backups, and the locked align-docs-first order.

## 1. What this actually is

`mb-wikilinks` is the skill that turns a documentation corpus's informal cross-references
into links a knowledge graph can actually follow. Documentation naturally accumulates
references in whatever shape the author used that day — a path in backticks, a sentence like
"see the payment-security ADR", a Related Documents table. Humans read those fine; software
doesn't. GBrain's link extractor only recognizes one form — `[[wikilink]]` — so every
reference left in an informal shape is invisible to the graph: it contributes nothing to
"what connects to what", and no tool can later answer questions like "which documents depend
on this ADR?"

The skill works through a corpus leaf folder by leaf folder: it backs the folder up in one
verified action, reads without changing anything, proposes an exact conversion for every
genuine document reference (and correctly refuses the ones that aren't document references
at all — most backticked strings are code identifiers, config keys, or table names, and
converting those would corrupt them), shows you the full report, applies only what you
approve, and proves each edit with a line-by-line diff against the backup before it's
committed. It runs only where align-docs has already healed the references it converts —
packaging follows product.

## 2. Feature summary

- Pattern recognition across the corpus's three established reference styles, with
  per-candidate line-level precision.
- Honest classification: every candidate is either a confident match, a confident
  non-reference, or an explicit uncertainty (AMBIGUOUS) — the skill never guesses
  which a backticked string is.
- Missing-document reporting: a name that matches nothing anywhere but reads as a document
  reference is reported to align-docs as a MISSING-DOCUMENT finding — investigated, never
  buried, never converted.
- Treatment rules that protect structure: registers, templates, and quarantine content are
  never converted; a healed Global→Local reference is never re-converted (that would
  re-create a violation align-docs already fixed); URLs, code identifiers, config keys,
  table/column names, and branch names are never candidates at all.
- Corpus-wide collision awareness: the basename census runs across every in-scope source,
  because the resolver it feeds is global — a basename colliding anywhere in the corpus is
  permanently barred from conversion. An ambiguous link is worse than no link.
- Format enforcement: bare-basename wikilinks only, because that is the only form GBrain's
  resolver actually resolves in this corpus — a syntactically valid link that silently
  resolves to nothing is a defect, not a conversion.
- Proof over trust: every edit is verified by diffing against the untouched backup, line by
  line; end-of-run success is measured by GBrain's own link-coverage counters moving, not by
  an absence of errors.
- A wide mode that scales without losing rigor: `(all)` sweeps every in-scope source in the
  locked order, leaf folder by leaf folder, each with its own complete cycle — the safety
  discipline is per-folder, so the wide run is many small safe runs, not one big risky one.
- A shared run frame defined once ([[doc-skills-run-discipline|Shared Run Discipline]]) and carried by every
  documentation skill: resume check, learnings load, git-clean precondition, verified
  stop-cold backup, decision-point checkpointing, run-record lifecycle with one index row
  in `run-log.md`, es.exe-first file search, and per-source GBrain sync at close.

## 3. Suitability

**Best for:** the reference-packaging pass of the documentation cycle — it runs AFTER
mb-align-docs, which validates and heals every reference in its existing written form first
(the product); this skill then converts the now-correct references into `[[wikilink]]`
form (the packaging). Per-folder for routine maintenance; `(all)` after a big refactoring.

**Good for:** onboarding a new source into the knowledge graph (converting its conventions
as part of initial ingestion); preparing a corpus for graph-dependent tooling; cleaning up
legacy reference styles anywhere they persist.

**Not good for:** creating references where none exist — it converts existing ones only;
checking whether references are *semantically* right — that is mb-align-docs, which runs
before this skill (this skill fixes form, not meaning); folder/index maintenance —
mb-docs-manager; anything inside an Anvil code repo — categorically denied, including
documentation under `theme\assets\docs` (Anvil owns how those files are interpreted; and
whether wikilinks can ever mean anything on the Anvil platform is standing research,
feeding a separate future decision).

## 4. Design reasoning

**Why conversion is proposed, not applied.** A backticked string is ambiguous by nature —
the same shape means a document to one author and a database column to another. The skill's
report therefore shows its evidence for every candidate and stops; approval converts the
skill's pattern-match into the developer's judgment. The strict rule that apply executes
*exactly* what was approved — the user's own corrections verbatim — keeps that judgment
authoritative end to end.

**Why the diff gate exists.** The riskiest failure in a text-rewriting skill is the silent
extra change: an edit that is almost right, or right plus something unintended. Diffing every
edited file against its untouched backup — and stopping at any line that doesn't precisely
match an approval — makes that failure impossible to miss. Backups are one run-level
timestamp per leaf folder: a single timestamp cannot collide with itself, the copy count is
verified against the source, and git HEAD (clean pre-run tree) is the sanctioned fallback
if a file is ever found unbacked.

**Why bare basename.** The corpus's folder names are not in GBrain's directory pattern, so
folder-qualified links parse but never resolve — a conversion that looks right and dead-ends.
Enforcing the one working form, and banning the plausible-but-broken one, encodes a live
technical constraint as a rule so no run re-discovers it.

**Why the collision census is corpus-wide.** The wikilink resolver resolves across the whole
brain, not one source. A census scoped to the scanned source under-counts collisions and
would bless links that are ambiguous the moment another source enters scope — a mistake
learned the hard way in 2026-09-11 runs and now encoded as the universe-matches-the-resolver
rule.

**Why leaf folders are the unit.** A leaf folder is small enough to review completely in one
report and small enough that a mistake is contained; larger units invite skimming. The wide
mode preserves this by sequencing full per-folder cycles — scale comes from repetition of
the safe unit, never from enlarging the unit.

**Where it sits.** After mb-align-docs, by the product-then-packaging principle: align-docs
first ensures every reference points where it should (the product), and this skill then
converts the validated references into the link format (the packaging). A reference that
still fails to resolve at conversion time is a missing-document finding for align-docs —
never buried, never converted. Its measure of success is external: not "the skill reported
clean," but GBrain's own link-coverage numbers moving — the corpus's connections becoming
real.

**Open items.** The 2026-09-11 runs (adr-global, specifications-global, security-global
batch, makepdlf-project-library, pdlf-library) completed under the pre-refactor skill and
converted to the plain `[[stem]]` form; those existing links stay untouched — the plain
form remains resolvable, and existing wikilinks are not conversion candidates. The
2026-09-17 wide sweep ran under an older method (folder references converted, plain
`[[stem]]`, per-file backups); at the 2026-09-20 resume check it was abandoned at the
developer's decision — its working record, detect artifacts, and flagged findings are
preserved in `abandoned-runs\`, and its approval was voided with it. The first
post-refactor run is pending and will be row one of `run-log.md`. The `templates-global`
frontmatter question (five files without any block) is excluded from retrofit and belongs
to align-docs' front-matter territory.
