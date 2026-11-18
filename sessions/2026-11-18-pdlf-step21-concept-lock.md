---
title: "2026-11-18-pdlf-step21-concept-lock"
doc-id: "mb-3d57e4f8"
updated: "2026-11-18"
---
# PDLF Step 21 — concept check and concept-locked (mb-3-cs, run app1)

## What was done

PDLF Step 21 (Concept Check) of run app1, opened in mb-3-cs-app1 via `/pdlf-init`. All nine
concept documents read in full (design doc 1,290 lines, test plan, access matrix, threat
model, glossary, 5 local ADRs, authoritative schema 71 tables, all 52 tickets + ticket list
+ 28 Archify flow digests extracted from HTML, DESIGN.md 1,189 lines). All 36 document pairs
compared and named. Six fixed checks run — Tables, Access, Terms, Tests, Decisions all PASS;
Receipts (PR-05) pass via `ts_report.py --check` for c17, c18, c19, c20.

## Findings and decisions (David's)

- 12 contradictions found between documents, each shown with both statements and a
  recommended correction; David approved all as recommended: C1 Settings tabs 14→15 (design
  doc); C2 Brevo deletion ticket 28→29 (ticket 04); C3 payment_config fields aligned to
  schema (DESIGN.md); C4 payment option wording (glossary); C5 FIDO2 enrolment at first
  sign-in, not onboarding step 1 (ticket 51); C6 SC-08 and C7 ST-13 added to the test plan;
  C8 homepage editor aligned to the shared section inventory (ticket 34); C9 four glossary
  entries added (System currency, Display currency, Unassigned, Morning briefing); C10 ADR
  clarified that contacts live in the scaffold's server_customers package;
  C11 design doc F-34 gains plan-summary (seven endpoints); C12 ticket 22 display-currency
  fields corrected. Observations O1 (design doc marking wording) and O2 (ticket list
  divergence line) also fixed at David's direction.
- Numbering note David required: the ticket-22 finding had been labelled C13 in chat with
  C12 skipped — nothing was dropped; the report renumbers it C12.
- Gate `concept-locked` presented with Full BFT; David answered yes and recorded it himself:
  `bash /mnt/c/mybizz/scripts/pdlf-gate.sh mb-3-cs concept-locked app1` → gates row id 2,
  2026-11-18 08:31:16 UTC. The concept is locked; no feature is added after this without
  the gate being reopened by an authorised deviation.

## Evidence

- `mb-3-cs-project-library/pdlf-outputs/c21/`: concept check report, checks XML (DC-11,
  PR-05), PR-05 tool output, receipt.
- Ledger: steps row id 14 complete; bft_records id 10 (full); triage_findings id 16
  (`sentinel-21-app1`, clear, Medium); gates id 2.

## Quirks

- The c21-module.md is an empty stub (5 lines), so the reference governed — same recorded
  pattern as c19.
- Writing ledger JSON and backslash paths through the WSL→PowerShell psql bridge mangles
  double quotes and backslashes; safe constructs: `to_jsonb(ARRAY[...])` for inputs_used and
  `replace('a/b', '/', chr(92))` for path strings.
- Cupcake blocked a `sed -n` read of commit-all.sh as a shell-mediated write; the Read tool
  is the read path for scripts.

## Documents written or changed

Project library: design-doc.md, test-plan.md, GLOSSARY.md, DESIGN.md, adr-crm-package-
replaces-marketing.md, tickets 04/22/34/51, the c19 ticket list; new c21 outputs (4 files).
Full list in the c21 receipt.

## Open

- DEFERRED TO STEP 22: correct the flow-51 card's step-1 label ("Password / FIDO2 enrol") —
  onboarding step 1 is Welcome and orientation. Carried in the ledger row's notes.
- Step 22 (screen requirements) is next; resumes from the ledger via `/pdlf-init`.
