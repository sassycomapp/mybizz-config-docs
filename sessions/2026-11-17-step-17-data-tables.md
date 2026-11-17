---
title: "2026-11-17-step-17-data-tables"
doc-id: "mb-107fd445"
updated: "2026-11-17"
---
# Step 17 ran: the app's tables now match the authoritative schema

Run `app1` (route Application, entry 03) continued at Step 17 — Create Anvil Data Tables, the first step of Phase C. The orchestrator resumed from the ledger, David chose to continue at Step 17.

## What was done and the evidence

- All eight reference sections ran: start checks, the authoritative schema checked against the data design and reviewed with secure-software-engineering, the difference list (234 differences, every one logged), the renames by hand, the schema write through `anvil-yaml`, David's application through one Resolve pass, Sentinel at High (CLEAR), and the receipt.
- The app's `db_schema` now holds the whole 71-table authoritative schema; the committed schema equals it with zero differences; ST-01 validates; ST-06 and ST-07 pass with eight review items David confirmed; the live tables match (Anvil reports no schema mismatch). Evidence: `mb-3-cs-project-library/pdlf-outputs/c17/` (difference list, instructions record Parts A and B, schema copy, db_schema copy, ST-01 JSON, scanner XML, checks XML) and the Step 17 receipt.
- The theme copies landed at David's order: `tests/component-inventory.yaml` (byte-identical to the theme's, which was pulled because the local theme library was stale) and the four theme keys of `tests/ts-config.yaml` aligned to the template.
- Step 17's ledger row id 10 is complete; BFT light row id 7; deviation row id 4; triage_findings row 14 (sentinel-17-app1, clear).

## Decisions and standards the developer set

- The theme inventory was pulled at source (no deviation) and copied into the app.
- The scanner's DD-13 was corrected at source to expect `activity_log` (not `audit_log`) as the audit-trail table — every Mybizz schema names it so; no deviation.
- Four scanner review items (the two public tokens, the four HH:MM availability columns) confirmed as correctly shaped; two more later (the referral on/off switches) — all eight recorded as the review note.
- `authoritative-schema.md` §1.3 corrected: `config.created_at` moved from the Keys table into the column table (it had made ST-07 fail); the design doc's Vault count corrected to 11 secret names.
- Deviation (row id 4, decision B): David applied Resolve directly without the by-name check of the 37 removals; verification ran after the fact and closed it by computation (pre-write 5924469 → committed 1c40fc3 removes exactly the 37 listed columns; Anvil reports no mismatch).

## Quirks

- The Anvil editor force-pushed rewritten git history after its commit; the plain `git pull` failed with divergent branches; reconciled with stash + `git reset --hard origin/master` + stash pop (local held no unique commits). See the governed fact from this session.
- The PowerShell bridge rejects em-dashes and JSON double quotes in SQL; ledger writes use jsonb_build_object and plain hyphens.

## Documents written or changed

- Written: `pdlf-outputs/c17/` — schema-diff, instructions (Parts A and B), authoritative-schema copy, anvil-db-schema.yaml, st01-validate.json, ts-scan.xml, checks.xml, receipt; this session page; a fact file in `facts/`; `schema-migration-log.md` gained the 2026-11-17 application row (prompts P1–P14/P13a superseded as the application method).
- Changed by David at source: ts_scan.py DD-13 (activity_log), authoritative-schema.md §1.3, design-doc.md (11 Vault names), the theme library pull.

## What is open

- Nothing of this step. Next: Step 18 (Phase C, pull to local) in a new session via /pdlf-init.
- Carried, not open work: ST-11's 91 pre-PDLF YAML form templates belong to the build steps; DD-04 stays skipped until Step 31/32 fills core_tables; David's business actions AC-6 and AC-14 remain before the first paying client.
