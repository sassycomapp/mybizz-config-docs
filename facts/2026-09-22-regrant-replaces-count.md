---
title: "2026-09-22-regrant-replaces-count"
doc-id: "mb-bfda00e3"
updated: "2026-10-01"
---
# Fact — re-granting a path replaces the entry count

Re-running `mg-grant --path <folder> --count N` for an already-granted
path updates the grant entry **in place**, replacing the count: a grant
of N is **N total**, not N plus the residual count. Observed live three
times during the mb-doccycle WP8 acceptance run (2026-09-22): the initial
count=3 decremented to 1; a supplementary grant of count=6 produced
count=6 (not 7); after six successful file edits the count hit 0 and the
next write denied; a further grant of count=3 restored it to 3 total.

Consequence: size each collective slip block for the **whole remaining
cycle** from the moment it is issued, or request a follow-up block when a
count is exceeded. The residual count never persists across a re-grant.

Context: session 014 (`sessions/2026-09-22-014-mb-doccycle-wp2-wp8`),
WP8 acceptance run. Confidence 0.9, method: live observation ×3. Approved
at the 2026-09-22 close-out gate. Graduated into
mb-doccycle Reference §Grant commands (2026-09-22).