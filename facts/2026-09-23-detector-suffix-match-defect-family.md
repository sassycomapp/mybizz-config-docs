---
title: "2026-09-23-detector-suffix-match-defect-family"
doc-id: "mb-44871199"
updated: "2026-10-01"
---
# Fact — detector suffix-variant matching over-matches common words

The Phase-C detector's "-<token>" suffix rule matches bare common words to
unrelated filenames: "search"→a learnings file, "count"→a learnings file,
"description"→system-description, "data"→a postgres data-dir mention,
"workflow"→a memory-governor file, "state.md"→a global ADR. All were caught
by context-read triage before reaching the developer (never auto-converted).
Rule-pipeline candidate for the git-backed detector: word-boundary or
minimum-length guards on bare suffix matches; skill-file mentions
(`SKILL.md`, `CONTEXT.md`, `DESIGN.md`, `CLAUDE.md`) also require the
context-read pass — the resolver's only SKILL.md is mb-doccycle's own.

Context: session 015 (`sessions/2026-09-23-015-mb-doccycle-makepdlf-first-cycle`),
Phase C triage (156 skips incl. ~42 word/suffix-level false positives).
Confidence 1.0, method: full-corpus triage, every occurrence context-read.
Approved at the 2026-09-23 close-out gate.
