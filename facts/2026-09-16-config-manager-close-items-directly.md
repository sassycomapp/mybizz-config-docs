---
document: "Durable fact — Config-manager open items are closed directly when the developer asks"
doc-id: 2026-09-16-config-manager-close-items-directly
state: Live
date-created: 2026-09-16
---

# Durable fact — Config-manager open items are closed directly when the developer asks

Config-manager open items that the developer asks to be closed are resolved
directly, never left as "flagged to docs governance" rows. A direct closure has
three parts, all applied to the suite's own documents: the spec's stale rows are
corrected to the verified live values, an evidence-backed disposition is written
into the config.md open-items table itself, and where a missing review was the
gap (e.g. a supply-chain licensing axis), the review is performed and recorded on
the spot rather than deferred.

The "flagged to docs governance" path remains the standing default for drift the
developer has not approved for correction — it is the fallback, never a terminal
state for an item the developer has explicitly asked to be closed.

Established 2026-09-16 on the anvil-agent-references config-management run #1
closure, where the developer directed the session: "sort out this fucking shit
now" after the initial gate dispositions left W-1..W-5 as governance-flag rows.
All five items were then closed by direct resolution — the spec details were
corrected to live state, an adoption review was performed and recorded for the
license axis, and each item received a dated, evidenced disposition. This is
consistent with the session-005 standard "flags are not resolutions — correct
the record."

Permanent homes: `config-setup-prompt.md` Amendment (clarity discipline — open
issues are never left open); the anvil-agent-references config-manager suite's
open-items table and adoption-review section.