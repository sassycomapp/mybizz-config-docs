---
title: "2026-09-22-esexe-s-is-search"
doc-id: "mb-7350ec4c"
updated: "2026-10-01"
---
# Fact — es.exe `-s` is the search flag, not sort

In es.exe (Everything CLI), `-s <text>` is the **search** flag: the text
becomes the search terms (e.g. `-s "*.md"` finds all markdown files). It
is **not** a sort flag. The mb-doccycle run frame's file-search section
misdocumented it as "-s sort by path"; the error was found during the WP8
acceptance run when a universe build passed a path-like value to `-s` and
scoped the result set to one file. Two debugging rounds were spent on this
before the flag's real semantics were proven by direct comparison of argv
forms.

The run frame's flag table was healed 2026-09-22 (text-drift correction).
Canonical scoped query form: `es.exe -p "C:\root" -n 1000000 -s "*.md"`.

Context: session 014, WP8 acceptance run + WP2 dry run. Confidence 0.95,
method: live observation, both directions proven. Approved at the
2026-09-22 close-out gate.