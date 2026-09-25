---
title: "2026-09-23-grant-decrement-per-edit-op"
doc-id: "2026-09-23-grant-decrement-per-edit-op"
---
# Fact — grant decrements fire per edit operation, not per file

A `mg-grant` path slip decrements once per successful edit tool call, not
per file touched: a count=26 slip sized for "23 files" was exhausted by 32
edit operations (makepdlf run 2026-09-23). Two consequences:

1. Size every slip to the **operation count plus buffer** (op count + 3
   proved workable), never the file count.
2. Re-granting replaces the entry count (confirmed again — the residual
   never persists). `git add` is NOT grant-gated — only commit/push-class
   operations are — so an expired allowance can strand a staged set; the
   120-minute `--minutes` sizing covered a full apply-and-commit window.

Context: session 015 (`sessions/2026-09-23-015-mb-doccycle-makepdlf-first-cycle`),
run 20260923T085908+0200. Confidence 0.9, method: live observation across
five grant issuances. Approved at the 2026-09-23 close-out gate.
