---
document: Register — Projects Config
doc-id: projects-config-register
state: Live
date-created: 2026-08-13
---

# Register — Projects Config

Append-only. Rows are never deleted. Only `state`, `date-state-changed`, `superseded-by`, and
`notes` may be updated in place after a row is created. All other fields are permanent from
first registration.

Tracks every `{slug}-config.yaml` — the single source of truth for that project or folder's
configuration. Kept fresh by `mb-config-manager` (see `master-task-list.md` Section 8) and,
going forward, as a required step in the "start a project" protocol.

| doc-id | filename | folder | type | state | date-registered | date-state-changed | superseded-by | notes |
|---|---|---|---|---|---|---|---|---|
| makepdlf-config | makepdlf-config.yaml | C:\dev\dev-makepdlf\ | config | Live | 2026-08-13 | 2026-08-13 | | |
| mb-3-cs-config | mb-3-cs-config.yaml | C:\dev\dev-mb-3-cs\ | config | Live | 2026-08-13 | 2026-08-13 | | |
| mb4ecom-config | mb4ecom-config.yaml | C:\dev\dev-mb4ecom\ | config | Live | 2026-08-13 | 2026-08-13 | | |
| mb5pdlf-config | mb5pdlf-config.yaml | C:\dev\dev-mb5pdlf\ | config | Live | 2026-08-13 | 2026-08-13 | | |
| pdlf-config | pdlf-config.yaml | C:\pdlf\ | config | Live | 2026-08-13 | 2026-08-13 | | placeholder project, not live — see the file itself |
| dev-root-hub-config | dev-root-hub-config.yaml | C:\dev\dev-root\ | config | Live | 2026-08-13 | 2026-08-13 | | |
| project-library-global-config | project-library-global-config.yaml | C:\dev\project-library-global\ | config | Live | 2026-08-13 | 2026-08-13 | | |
| project-template-config | project-template-config.yaml | C:\dev\project-template\ | config | Live | 2026-08-13 | 2026-08-13 | | |
| mybizz-config | mybizz-config.yaml | C:\mybizz\ | config | Live | 2026-08-13 | 2026-08-13 | | |

## Field definitions

- **doc-id** — permanent identifier, the filename's own slug. Never reused even if the row's
  state becomes Retired.
- **filename** — current registered name of the document.
- **folder** — the project/folder root this config belongs to (not the YAML's own file
  location, which is always directly inside that root).
- **type** — always `config` in this register.
- **state** — one of: `Live`, `Retired`.
- **date-registered** — date this row was first appended. Never changes.
- **date-state-changed** — date `state` last changed. Updated whenever state flips.
- **superseded-by** — doc-id of the version that replaced this one, if state is Retired due
  to versioning. Blank otherwise.
- **notes** — free text, optional.

## Explicitly excluded

`projects-reference` — confirmed personal content, outside the Mybizz/PDLF operating system
entirely. Does not get a config YAML, does not appear in this register. See `docmap.md`
Section 4.
