# wikilinks — Explainer

## 1. What this actually is

`mb-wikilinks` is the skill that turns a documentation corpus's informal cross-references
into links a knowledge graph can actually follow. Documentation naturally accumulates
references in whatever shape the author used that day — a path in backticks, a sentence like
"see the payment-security ADR", a Related Documents table. Humans read those fine; software
doesn't. GBrain's link extractor only recognizes one form — `[[wikilink]]` — so every
reference left in an informal shape is invisible to the graph: it contributes nothing to
"what connects to what", and no tool can later answer questions like "which documents depend
on this ADR?"

The skill works through a corpus leaf folder by leaf folder: it backs every file up, reads
without changing anything, proposes an exact conversion for every genuine document reference
(and correctly refuses the ones that aren't document references at all — most backticked
strings are code identifiers, config keys, or table names, and converting those would
corrupt them), shows you the full report, applies only what you approve, and proves each
edit with a line-by-line diff against the backup before it's committed.

## 2. Feature summary

- Pattern recognition across the corpus's three established reference styles, with
  per-candidate line-level precision.
- Honest classification: every candidate is either a confident match, a confident
  non-reference (NO_MATCH), or an explicit uncertainty (AMBIGUOUS) — the skill never guesses
  which a backticked string is.
- Collision awareness: basenames that exist more than once in a source are permanently
  barred from conversion — an ambiguous link is worse than no link.
- Format enforcement: bare-basename wikilinks only, because that is the only form GBrain's
  resolver actually resolves in this corpus — a syntactically valid link that silently
  resolves to nothing is a defect, not a conversion.
- Proof over trust: every edit is verified by diffing against the untouched backup, line by
  line; end-of-run success is measured by GBrain's own link-coverage counters moving, not by
  an absence of errors.
- A wide mode that scales without losing rigor: `(all)` sweeps every locked source leaf
  folder by leaf folder, each with its own complete cycle — the safety discipline is
  per-folder, so the wide run is many small safe runs, not one big risky one.

## 3. Suitability

**Best for:** the reference-modernization pass of the documentation cycle — run after
structure is true (mb-docs-manager) and before content-agreement validation
(mb-align-docs), so alignment validates the final `[[wikilink]]` convention instead of a
style about to be replaced. Per-folder for routine maintenance; `(all)` after a big
refactoring.

**Good for:** onboarding a new source into the knowledge graph (converting its conventions
as part of initial ingestion); preparing a corpus for graph-dependent tooling; cleaning up
legacy reference styles anywhere they persist.

**Not good for:** creating references where none exist — it converts existing ones only;
checking whether references are *semantically* right — that is mb-align-docs (this skill
fixes form, not meaning); folder/index maintenance — mb-docs-manager; anything inside an
Anvil code repo — categorically denied, including documentation under `theme\assets\docs`
(Anvil owns how those files are interpreted; and whether wikilinks can ever mean anything on
the Anvil platform is standing research, feeding a separate future decision).

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
match an approval — makes that failure impossible to miss. Similarly, backups are spaced a
second apart so two files can never receive the same timestamp and overwrite each other.

**Why bare basename.** The corpus's folder names are not in GBrain's directory pattern, so
folder-qualified links parse but never resolve — a conversion that looks right and dead-ends.
Enforcing the one working form, and banning the plausible-but-broken one, encodes a live
technical constraint as a rule so no run re-discovers it.

**Why leaf folders are the unit.** A leaf folder is small enough to review completely in one
report and small enough that a mistake is contained; larger units invite skimming. The wide
mode preserves this by sequencing full per-folder cycles — scale comes from repetition of
the safe unit, never from enlarging the unit.

**Where it sits.** Middle of the documentation-skill sequence, and a dependency of the last
one: mb-docs-manager → **mb-wikilinks** → mb-align-docs. Alignment explicitly waits for this
retrofit to finish, because validating the old reference style and then re-validating the
new one would double the work. Its measure of success is external: not "the skill reported
clean," but GBrain's own link-coverage numbers moving — the corpus's connections becoming
real.

**Open items.** The earlier manual retrofit predates the run-logging discipline, so its
history lives only in git commits; the first properly logged runs are the planned wide-mode
run. The `templates-global` frontmatter question (five files without any block) is excluded
from retrofit and belongs to align-docs' front-matter territory.
