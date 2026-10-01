---
title: "2026-09-15-data-mybizz-mgt-folder-rename"
doc-id: "mb-186553e0"
updated: "2026-10-01"
---
# Fact — data-mybizz-mgt folder rename (underscore dropped)

The Mybizz management data folder is `C:\data-mybizz-mgt`. It was renamed
from `C:\_data-mybizz-mgt` on 2026-09-15 by developer decision; the leading
underscore was dropped because it is invalid in GBrain source ids
(`[a-z0-9-]`) and awkward everywhere else (approved by the developer:
"just drop the underscore and save us a lot of trouble later").

Consequences that must be trusted without re-checking:

- The old path `C:\_data-mybizz-mgt` (WSL `/mnt/c/_data-mybizz-mgt`) is
  **dead**. Any reference to it — in docs, configs, skills, or procedures —
  is stale until the document-management skills sweep it.
- Canonical homes for the new state: [[[mybizz-os-docs:os-reference-docs/repo-organization|Repo organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md)
  (repo/source/path correlation table), [[[mybizz-os-docs:os-reference-docs/mybizz-scope-list|Mybizz Scope List]]](C:/mybizz/mybizz-os-docs/os-reference-docs/mybizz-scope-list.md)
  (in-scope root + GitHub repo list), and the folder `README.md` naming note.

Context: session 2026-09-15-001
(`sessions/2026-09-15-001-data-mybizz-mgt-repo-registration`). Registered
end-to-end the same day: GitHub `sassycomapp/data-mybizz-mgt` (private,
master), GBrain source `data-mybizz-mgt` (federated), opencode
`external_directory` allow.

Confidence 0.95, method model_based. Approved at the 2026-09-15 close-out
gate (governed routing).
