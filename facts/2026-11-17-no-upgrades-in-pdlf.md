---
title: "2026-11-17-no-upgrades-in-pdlf"
doc-id: "mb-fe0f982b"
updated: "2026-11-18"
---
# No upgrades inside PDLF steps

Rule: gstack and gbrain update prompts and upgrades are never part of a PDLF step or any PDLF run. Update checks are permanently disabled (`gstack-config set update_check false`, set 2026-11-17 at the Step 20 close-out gate). The developer decides upgrades on his own schedule; an agent never raises an upgrade prompt in any run, and never upgrades shared tooling mid-step.
