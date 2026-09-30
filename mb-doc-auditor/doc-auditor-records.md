---
title: "doc-auditor-records"
doc-id: "mb-686cc79d"
---

# doc-auditor-records

Append-only audit record for `mb-doc-auditor`. One block per audit
run: date, scope, purpose, checked, findings by classification,
actions, outstanding items, terminal state. Blocks are never
rewritten or deleted.

## 2026-09-25 — scope: project-library-global (register-global)

- purpose: Phase 5 operational verification: full live audit of the global library against the G-brain contract
- checked: scope (486 files in-scope, exclusions applied); frontmatter (486/486 compliant, 0 findings); WikiLinks (12 missing targets, 0 ambiguous); basename collisions (27); register-global schema+rows (487->491 rows); gbrain sources list (18 sources live)
- findings: must-fix=14, can-wait=36, doesnt-matter=0, human-judgement=14
- actions: registered 4 session pages (2026-09-21-012, 2026-09-22-013, 2026-09-22-014, 2026-09-23-015); retired-in-place 2 obsolete rows (SmokeTest-README, enterprise-deployment-index); zero frontmatter repairs needed
- outstanding: 1 stem-collision registration decision (README x5); 12 broken WikiLinks needing target decisions; 9 pre-existing legacy-schema register rows (Can wait); 27 basename collisions (G7 signal, Can wait); prose-conversion candidates left unconverted (anti-work-generation)
- terminal: AUDIT COMPLETE — scope satisfies defined G-brain requirements except 14 items requiring human judgement

## 2026-09-28 — scope: full estate (C:\data-mybizz-mgt, C:\dev, C:\mybizz, C:\pdlf per mybizz-scope-list.md)

- purpose: full sanity audit, all aspects (developer-invoked, scope "(ALL)"; prior 2026-09-25 items re-checked per developer instruction)
- checked: 1,482 in-scope .md files (G1–G5, O1/O2 frontmatter); 7 registers (O4 schema, four-event model, membership both directions); 3,108 wikilinks (O6 form, O7 targets, G7 collisions); gbrain prerequisites via read-only CLI (G9: 17 sources all synced 2026-09-28; G10: 1,031/1,752 orphans — signal, not error); maintainer run-log as evidence only; exempt classes skipped (tmp-, stencil, quarantine, backups, logs, obsolete, WIP/temp, Anvil anvil.yaml subtrees, dotfolders)
- findings: must-fix=6 clusters (91→186 missing registrations incl. plg _index stem collisions; 3 files missing frontmatter; 405 stale-Live rows; 55 malformed register rows incl. 3 txt-record rows, 8 six-cell quarantine rows, 5 dash-state rows, 39 blank-state rows, 1 wrong-location daily-ops row; pdlf-register six-field schema deviation; G2 contract-vs-implementation contradiction). can-wait=78 ambiguous bare-name links (G7, mostly makepdlf stepwise), 96 broken links in Retired- snapshot folders, C:\mybizz root has no register (memory-diagnostic report unregistrable), SKILL.md register-paths.md reference stale. doesnt-matter=quarantine-lane frontmatter violations (exempt class), grammar-example wikilinks. human-judgement=4 asked, all decided: pdlf-register migrated to O4; contract G2 amended; broken links got full decision list (9 patterns, 88 links)
- actions: R2 frontmatter added to 3 files (2x Tools and apps, memory-diagnostic-2026-09-28); R1 186 creation rows appended (config-docs 80, plg 102, os-docs 2, data-mgt 2); R3 405 stale-Live rows retired in place + 1 wrong-location daily-ops row (data-mgt) retired, live row kept in mybizz-os-docs; R4 55 rows normalized to O4 schema (original values preserved in notes); R5 pdlf-register migrated to six-field→O4 (12 rows, superseded-by filled from row notes: environment-explainer, pdlf-explainer; folder/type preserved in notes) + 49 creation rows (app-factory modules 1–46, AGENTS.md, pdlf-pol-stepwise-gating, pdlf-proc-stepwise-closeout); R6 gbrain-doc-contract.md G2 amended — non-empty-body clause removed per Level A precedence (markdown.ts implements no EMPTY_BODY check; 243 frontmatter-only stubs ingest fine); R7 75 broken links repaired (26 retargets: skill-index→skills-register 16, agents→mb-3-cs-project-library:AGENTS 8, +2; 49 prose conversions to display text), 13 grammar-example links left as-is, 96 broken links in Retired- folders left as-is (retired snapshot). H over-conversion (15 valid links) caught in verification, restored via git checkout, re-applied broken-only (29). All repairs verified by re-scan: frontmatter live-corpus clean; broken non-retired links = 12 grammar examples only; all 7 registers 0 malformed / 0 unregistered / 0 stale-Live (pdlf-register retains 2 pre-existing row-only doc-ids app-factory-readme, step-13-readme — doc-ids intentionally not stems, docs exist)
- outstanding: 12 grammar-example wikilinks (intentional, no change); 96 broken links in Retired- folders (retired material); G7 ambiguity signals (no requirement violated); register-universe gap: no register-local.md at C:\mybizz root; gbrain upgrade available 0.46.1.0→0.59.3.0; SKILL.md register-paths.md pointer stale
- terminal: AUDIT COMPLETE — audited scope satisfies the defined G-brain requirements; no outstanding issues requiring human judgement (all four decision requests resolved by developer during the run)

## 2026-09-28 — standing decisions (follow-up to the full-estate audit)

- 1. Grammar examples in backticks: five prose grammar examples wrapped in inline code (facts/2026-09-20-doc-skills-charter, facts/2026-09-20-mb-wikilinks-conversion-rules, facts/2026-09-23-renderings-stencils-not-link-targets, mb-doc-auditor/doc-auditor-learnings; the fifth, sessions/2026-09-23-015, was deleted by the developer before the edit). Basis: G-brain link-extraction.ts stripCodeBlocks (lines 200-217) ignores inline code and fenced blocks — "slugs inside code are not real entity references". Content remains fully indexed and searchable; only the false broken-link signal is removed. The other seven examples were already inside code and were never extracted.
- 2. Retired- snapshot folders: C:\mybizz\mybizz-config-docs\memory-governor\Retired- Memory-upgrade-work-done and Retired-memory-governor-agent are never link-repaired (developer agreement 2026-09-28). Their 96 broken internal links are frozen by definition; retired material is never live knowledge.
- 3. Files at the C:\mybizz root remain unregistered (developer decision 2026-09-28); no register-local.md is created at that root.
- 4. G-Brain upgrade recommendation withdrawn: the documented upgrade policy in mybizz-os-docs/os-reference-docs/memory-master-explainer.md ("never upgrade on newness, only on check failure") governs; no new rule created. Any future upgrade is a developer-triggered decision, run as its own session with post-upgrade verification (doctor, sources list, search sanity, embedding provider still OpenAI per ADR).
- 5. pdlf-register descriptive doc-ids: app-factory-readme and step-13-readme kept as the accepted pre-2026-09-28 convention; register prose updated to explain the exception so the intent is preserved.
- 6. Developer deletions 2026-09-28: sessions 2026-09-22-013-mb-doccycle-wp0-wp1, 2026-09-22-014-mb-doccycle-wp2-wp8, 2026-09-23-015-mb-doccycle-makepdlf-first-cycle deleted from project-library-global/sessions; register rows retired in place; no wikilinks to them existed (prose mentions only, left untouched).
- 7. Models folder moved by the developer from C:\mybizz\Models to C:\data-mybizz-mgt\Models; its five documents registered in the data-mybizz-mgt register (creation rows; frontmatter verified compliant).
