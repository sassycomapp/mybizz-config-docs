---
document: OpenCode — Permission & Access Control Model
status: Current — describes the system as it stands
---

# OpenCode — Permission & Access Control Model

## What this covers

How OpenCode's `opencode.json` permission system works, and the current,
verified configuration across every project in this ecosystem. This is
the access-control layer only. It does not cover session/database data
integrity — see `opencode-project-session-data-integrity.md` for that.

## The permission model

Each `opencode.json` (one global, one per project) can set:

- **`edit`** — per-file-pattern rule: `"ask"`, `"deny"`. Applies to file
  writes/edits.
- **`webfetch`** — `"ask"` (default posture across this ecosystem).
- **`bash`** — per-command-pattern rule: `"ask"`, `"deny"`. A `"deny"`
  match is a genuine, verified hard block — confirmed live: OpenCode
  refused an `rm -rf` attempt on a real file, and the file was
  physically confirmed to survive.
- **`external_directory`** — grants a session access to read/write
  outside its own project folder, per path glob, `"allow"`/`"ask"`/`"deny"`.
- **`agent`** — per-agent overrides (e.g. the `plan` agent has
  `edit: "deny"` globally, enforcing the plan/build split regardless of
  the top-level `edit` setting).

**Config precedence:** global config is the baseline; project-level
config may tighten but should not be assumed to override a broader
global grant — this has not been independently verified against
OpenCode's actual merge behavior and should not be relied upon without
testing if it becomes safety-critical.

## Current configuration — code repos (write-capable, higher risk)

All three carry the full deny-list below and correct
`external_directory` scoping to their paired documentation repo only:

| Repo | Full path |
|---|---|
| `mb-3-cs` | `C:\dev\dev-mb-3-cs\mb-3-cs\opencode.json` |
| `mb4ecom` | `C:\dev\dev-mb4ecom\mb4ecom\opencode.json` |
| `mb5pdlf` | `C:\dev\dev-mb5pdlf\mb5pdlf\opencode.json` |

**Standard bash deny-list (all three code repos):**
```
rm -rf *, rm -r -f *, git reset --hard*, git push --force*, git push -f*,
git clean -fd*, *DROP TABLE*, *DROP DATABASE*, *TRUNCATE*,
curl*|*sh, curl*|*bash, wget*|*sh, wget*|*bash
```

## Current configuration — `makepdlf-project-library`

Full path: `C:\dev\dev-makepdlf\makepdlf-project-library\opencode.json`

This repo has genuine write access into `C:\pdlf\` (the live PDLF
product being built) and read access to
`C:\dev\project-library-global\` — it carries the same expanded deny-list
as the code repos above, since it has real write consequences.

## Current configuration — global

Full path: `C:\Users\dev-p\.config\opencode\opencode.jsonc` (WSL path:
`~/.config/opencode/opencode.jsonc`)

`instructions` array points at the four global index files
(`adr-global`, `specifications-global`, `policy-global`,
`standard-operating-procedures-global`, all under
`C:\dev\project-library-global\`). `external_directory` grants
`C:\mybizz\**`, `C:\dev\**`, `C:\pdlf\**`.

## Problem / remedy reference

**Symptom:** a permission grant or index-file pointer silently has no
effect, even though the JSON looks syntactically correct.
**Cause:** the path in the config points at a folder that no longer
exists (e.g. a stale root like `C:\projects\...` after a rename to
`C:\dev\...`).
**Remedy:** always verify a path in `opencode.json` actually resolves
(`Test-Path` in PowerShell, or `[ -d ... ]` in WSL bash) before trusting
that the permission/instruction it configures is active. A config file
saving correctly is not evidence that its content is correct.

**Symptom:** a code repo has a bash `"ask"` default but no destructive-
command deny-list, while its paired documentation repo does.
**Cause:** inconsistent rollout — deny-lists were added ad hoc per
repo over time without a shared baseline.
**Remedy:** any new code repo added to this ecosystem must get the full
standard deny-list above at creation, not just `"*": "ask"`.

---

*End of document*
