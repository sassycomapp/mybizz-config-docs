---
title: "2026-09-15-archify-learnings-closeout"
doc-id: "mb-2bfedf6f"
---
# Durable fact — Archify learnings close-out trigger

Archify run learnings are recorded only on an explicit trigger: after a run,
the developer either asks for learnings directly or answers the scoping skill's
Phase 9 close-out question ("record learnings for this run?"). Nothing in the
stack auto-triggers learnings capture — the Archify skill's lifecycle ends at
handoff, its update checker is version-only, and no daemon watches the CLI.
Learnings land in `archify/output/learnings/{YYYY-MM-DD}-{subject}.md` in the
suite's transient table format (learning | right action | destination), so
notable entries can later graduate into the skill or reference. Silence is
never consent — if the developer does not ask, no learnings file is written.