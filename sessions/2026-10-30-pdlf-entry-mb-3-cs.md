---
title: "2026-10-30-pdlf-entry-mb-3-cs"
doc-id: "mb-c7d02dbf"
updated: "2026-10-30"
---
# PDLF entry — mb-3-cs registered through entry 03 (new-app-with-context)

## What was done

The PDLF orchestrator (`/pdlf-init`, Step 1) ran in `mb-3-cs-app1` and took the
business's first entry. Start checks passed: working folder is the App 1 repo
(slug `mb-3-cs`), the bind link `/home/dev-p/projects/mb-3-cs-app1` is connected,
and the ledger answers (read-only `SELECT 1` through the PowerShell bridge,
pattern taken from `pdlf-gate.sh` — no `.env` ever read). The resume check found
no `projects` row: nothing to resume, no earlier PDLF history.

David chose entry **03 `new-app-with-context`** and answered its questions: name
**Mybizz Consulting Services**, mode **full**; apps **1, 2, 3, 5** exist (confirmed
against the four folders); the context is **`mb-3-cs-project-context`** and already
sits at its final path (the project-library folder is empty, so Step 11 needs no
move permission); **no reference platform**; the GBrain document list of the
context (source `mb-3-cs-project-context`, 303 pages) confirmed.

Ledger writes (database `pdlf`, port 5433, via the bridge): the `projects` row;
the entry `steps` row (id 4, entry 03, run `app1`, status `complete`) holding the
entry record in `inputs_used`; and its Light BFT record (BONES + HEALTH). PR-01
verified by ledger read-back. Receipt and checks.xml were **not** written: per
`a01-config`, entries 02/03 have Step 11 write them once the library exists.

Evidence: ledger rows read back in-session; app folders listed; GBrain source
registry and page list shown to David.

## Decisions and standards David set

- Mode `full` — this is a real build, not a test-mode run.
- All four apps attested as real; the pipeline inherits existing work rather than
  re-litigating it (named in the entry's BFT as an intangible bone for Steps 11/12).

## Quirks

- Doubled single quotes (`''`) in SQL are eaten by `powershell.exe -Command`
  parsing; the working shape is `pdlf-gate.sh`'s: bash double quotes around the
  PowerShell command, `\"` around the `-c` payload, single-quoted SQL literals.
- A JSON payload (the entry record) cannot pass through that shape at all; the
  working method is a UTF-8 BOM-free `.sql` file written from WSL and run with
  `psql -f` (spec-postgres-ledger's Out-File BOM warning does not apply to
  WSL-written files).

## Documents written or changed

- Close-out: this session page; the advisory fact below; the four canonical
  project documents created in `mb-3-cs-app1` at `theme/assets/docs/app1/`
  (`mb-3-cs-config.md`, `mb-3-cs-reference.md`, `mb-3-cs-explainer.md`,
  `README.md`). The PDLF entry step itself wrote no repository files — one
  transient SQL file in `dev-mb-3-cs/wip/` was created and deleted; ledger rows
  are the record.

## What is open

- Run `app1`, route Application: **Step 11 (Phase B)** is next, on David's
  "continue". The run will pause after Step 16's `domain-locked` gate — Phases C
  to F are not built yet.
- Step 11 also writes this entry's receipt
  (`pdlf-outputs\a03\mb-3-cs-a03-app1-receipt.md`) and checks.xml from the entry row.
