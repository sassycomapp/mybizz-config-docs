---
title: "2026-09-23-whole-register-mechanical-scan"
doc-id: "mb-02e7c1b0"
updated: "2026-10-01"
---
# Fact — register field checks must scan every row mechanically

Sample-based register findings under-detect: 9 malformed date-registered
rows were found by reading; a mechanical scan of ALL rows found 89 (the
2026-09-11 truncated-batch repair block carried the same defect
systematically). Every register field-format conformance check must run a
mechanical whole-register scan, never a sample. Repair pairs are generated
byte-exact from the file itself and uniqueness-verified before any write.

Context: session 015 (`sessions/2026-09-23-015-mb-doccycle-makepdlf-first-cycle`),
89-row repair verified to zero malformed across 249 rows. Confidence 1.0,
method: mechanical scan vs read-based sampling, both run. Approved at the
2026-09-23 close-out gate.
