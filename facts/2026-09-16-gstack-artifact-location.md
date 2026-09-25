---
title: "2026-09-16-gstack-artifact-location"
doc-id: "2026-09-16-gstack-artifact-location"
---
# Fact — GStack artifact location and the missing gstack-outputs lane

GStack skills save all their output to a per-project directory under the user
home:

    ~/.gstack/projects/$SLUG/

where `$SLUG` is the deterministic per-repo project slug produced by
`gstack-slug` (example, this config-docs repo: `sassycomapp-mybizz-config-docs`).
Later skills find prior output by re-computing the same slug and reading the
known skill sub-directory (`ceo-plans/`, `designs/`, `retros/`, `qa-reports/`,
`.context/`, etc.), plus `/context-restore` and project-keyed
`learnings.jsonl` / `timeline.jsonl`.

The AGENTS.md `gstack-outputs/` repo-visible copy lane is a **convention only —
it does not exist anywhere on this system**, except inside backup folders
(out of scope). Verified 2026-09-16: no `gstack-outputs/` folder exists in any
project root; the earlier config claim "confirmed live in
`mb5pdlf-project-library`" was falsified (folder absent there). Never rely on a
repo-side copy; `~/.gstack/projects/$SLUG/` is the sole authoritative artifact
location.

Full annotated record: [[gstack-reference|GStack Reference]] §Artifact locations.
