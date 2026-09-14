---
document: "Durable fact — Graphify rebuild provenance stamping (cwd)"
doc-id: fact-graphify-cwd-provenance
state: Live
date-created: 2026-09-14
---

# Durable fact — Graphify rebuild provenance stamping

`graphify extract` stamps the graph's `built_at_commit` from the invoking
working directory's git repository, not from the scanned repository path.
Every Graphify rebuild (`extract`, `cluster-only`) must therefore be run
from inside the target repository root, and the rebuild procedure's final
provenance-confirmation step (`built_at_commit` == `git rev-parse HEAD`)
is mandatory, never optional.

Proven live 2026-09-14 during the graphify configuration-management run #1
(finding F-4): a full documented rebuild of the mb-3-cs graph, executed
from the mybizz-config-docs working directory, stamped that repo's HEAD
commit (`1194ea9…`) onto the mb-3-cs graph; the verification step caught
the mis-stamp, and the corrected rebuild from the mb-3-cs root stamped
provenance correctly (`59175d9e…` == HEAD). The `graphify update` path
stamps from the scanned path. Permanent homes: `graphify-config.md`
§Open items; `graphify-reference.md` §Graph build procedures;
the `mb-config-graphify` skill's hard behavioral rules.
