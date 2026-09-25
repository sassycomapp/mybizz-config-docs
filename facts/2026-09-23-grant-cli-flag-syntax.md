---
title: "2026-09-23-grant-cli-flag-syntax"
doc-id: "2026-09-23-grant-cli-flag-syntax"
---
# Fact — grant CLI syntax is flag-based

`mg-grant` requires `--path <folder> --count <n>`; `git-grant` requires
`--repo <folder> --count <n>` and accepts optional `--minutes <n>`
(default 30). Positional argument forms exit 2 with "unknown argument"
BEFORE any grant is written — a failed attempt consumes nothing. Both
scripts live in `~/.config/cupcake/bin/`.

This supersedes the positional command form recorded in the WP8 run
record; the commit-allowance rule's own documented syntax
(`git-grant --repo <folder> --count N --minutes M`) is confirmed correct.

Context: session 015 (`sessions/2026-09-23-015-mb-doccycle-makepdlf-first-cycle`),
makepdlf first full cycle. Confidence 1.0, method: script source read +
three live issuances. Approved at the 2026-09-23 close-out gate.
