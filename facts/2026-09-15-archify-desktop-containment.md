---
title: "2026-09-15-archify-desktop-containment"
doc-id: "mb-6a22e43a"
---
# Durable fact — Archify desktop containment is viewer-inherent for card-bearing artifacts

Archify's strict desktop containment rule (`documentElement.scrollHeight <=
window.innerHeight` at 1440×900 / 1600×1000 / 1920×1080 / 2048×1320) is not
achievable for card-bearing artifacts in the current viewer build. The shipped
reference `examples/dataflow-product-analytics.html` (itself 9/9-validated)
produces the identical `viewer/viewport-overflow` failure at all four
viewports — the viewer stacks dock + diagram + legend + cards on a vertically
flowing page. Report `browser_evidence: failed` truthfully with that calibration
noted; do not treat overflow as a drawing defect when the reference fails
identically. Still compact genuinely redundant viewBox height. `visual_review:
passed` requires an actual human or image-capable inspection — it never comes
from the automated containment gate.