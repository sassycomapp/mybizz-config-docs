---
document: "wikilinks — Reference"
doc-id: wikilinks-reference
state: Live
date-created: 2026-09-10
---

# wikilinks — Reference

Execution procedure for the `mb-wikilinks` skill. `SKILL.md` in the installed
folder (`~/.config/opencode/skills/mb-wikilinks/`) is the authoritative
definition; this document is the operational form. Updated 2026-09-20 to
reflect the refactored skill (2026-09-19: scope from the single authority
list, shared run frame, corpus-wide collision census, run-level backup).
Why the rules are shaped this way: [[wikilinks-explainer|Explainer]].

## Run-state discipline — mandatory, end to end

The shared run frame (resume check, learnings load, git-clean precondition,
verified stop-cold backup, decision-point checkpointing, run-record lifecycle,
approvals in chat, permission discipline, verification, commit plan and
per-source GBrain sync, es.exe-first search, Anvil code repos denied) is
defined once in
[[doc-skills-run-discipline|Shared Run Discipline]]
and is mandatory for every run. One working record per run lives in
`C:\mybizz\logs\mb-wikilinks\in-progress\` (run timestamp, Filename-Safe ISO
8601 UTC+2), is appended at every decision point, moves to
`last-completed-run\` at close, and leaves ONE index row in `run-log.md` —
the permanent audit trail.

## Invocation

- `/mb-wikilinks (leaf-folder-name)` — full cycle for that leaf folder, one continuous run.
- `/mb-wikilinks (all)` — every in-scope source in the locked order, leaf folder by leaf
  folder — each leaf folder still gets its own complete cycle (own backup, report,
  approval pause, apply, verify, commit); a wide run is a sequence of full cycles, never
  a merged batch.
- **Empty or omitted target: the skill asks and does nothing until answered.** Never assumed.
- Quote folder names containing spaces: `/mb-wikilinks ("Agent readiness")`.
- **A code repo is not a valid target** — Anvil code repos are denied entirely, including any
  docs folder inside them.
- Explicit invocation only — never auto-trigger, never infer "the next" leaf folder.

## Scope

Scope comes from the scoping list
([[mybizz-scope-list|Mybizz Scope List]]) — the single scope
authority for every documentation skill, read at Phase 0 of every run. The skill never
carries its own scope list. In-scope roots: `C:\data-mybizz-mgt`, `C:\dev`, `C:\mybizz`,
`C:\pdlf`; exceptions only as listed there. If asked to extend scope to an excepted
path, stop and confirm explicitly with the developer — the scoping list is the only
authorization for scope.

**Default processing order (each corpus's first retrofit; leaf folder by leaf folder
inside each):**

1. `project-library-global` — `/mnt/c/dev/project-library-global`
2. `dev-root` — `/mnt/c/dev/dev-root`
3. `makepdlf-project-library` — `/mnt/c/dev/dev-makepdlf/makepdlf-project-library` (the
   `makepdlf` sibling is a ceremonial placeholder — nothing to convert)
4. `pdlf` — `/mnt/c/pdlf/pdlf-library` plus the app-factory README (the only content
   file in `app-factory\`; the 46 module files are empty placeholders — nothing to
   convert)
5. `mb-3-cs-project-library` — in development; transient state schedules the work,
   never removes scope
6. `mybizz-os-docs`
7. `mybizz-config-docs` — authored documents only; regenerated `*-skill.md` /
   `*-learnings.md` / `*-log.md` operational artifacts are not conversion targets
8. `data-mybizz-mgt`

**Conversion treatment rules:**

- Candidates are references to documents. Code identifiers, config keys,
  table/column names, branch names, and URLs are never candidates.
- Registers (`register-global`, `register-local`, any `*-register`) are structured
  catalogue tables — never converted.
- Templates are stencils — never converted, never cited as knowledge.
- Quarantine content is terminal — a trackable reference into it is a drift item,
  never converted.
- **Global→Local directionality:** a global document never carries a trackable
  reference into a project library. Prose healed by align-docs into the form
  `` `stem.md` (owning project library) `` is NOT a conversion candidate — converting
  it would re-create a healed violation.
- Ambiguous basenames (corpus-wide census) are never converted — flagged for the
  developer's decision.
- A reference that resolves nowhere but reads as a document reference is a
  MISSING-DOCUMENT finding for align-docs — reported, never buried, never converted.

## Prerequisites (once, before the first source)

1. Confirm the resolver:
   ```bash
   gbrain config get link_resolution.global_basename
   ```
   If not `true`: `gbrain config set link_resolution.global_basename true`
2. Confirm the target format: `[[basename|Display Text]]` — bare filename stem only.
   Never `[[folder/basename]]` — this corpus's folder names are not in GBrain's
   compiled `DIR_PATTERN`, so directory-qualified wikilinks never resolve here.
3. Ensure the working directories exist:
   ```bash
   mkdir -p "/mnt/c/backup-mb-wikilinks"
   mkdir -p "/mnt/c/mybizz/logs/mb-wikilinks/learnings"
   mkdir -p "/mnt/c/mybizz/logs/mb-wikilinks/in-progress"
   mkdir -p "/mnt/c/mybizz/logs/mb-wikilinks/last-completed-run"
   mkdir -p "/mnt/c/mybizz/logs/mb-wikilinks/abandoned-runs"
   ```

## Per-source preparation (once per source, before its first leaf folder)

1. **Basename-collision check — corpus-wide.** The resolver is global, so the census
   universe must match: query with es.exe (`-s "*.md"`, folder-scoped per source if
   needed), filter to the in-scope sources, reduce to basenames, count. Any basename
   with count > 1 anywhere in the corpus is an exception: that basename is NEVER
   wikilinked — a globally ambiguous link is worse than no link. (Known collisions
   already confirmed: `_index` 67× and `quickstart` 24× in the anvil-docs corpus;
   `README` 4×; `INDEX.md` collides 3 ways in `project-library-global`.)
2. **Leaf-folder map.** Classify every directory in the source: leaf (files directly,
   or only excluded subfolders per the scoping list) vs non-leaf (has subdirectories —
   decompose into child leaf folders; never batch a non-leaf as one unit).
3. Report both the collision-exception list and the leaf-folder map before starting
   the cycle. Do not proceed without this confirmed.

## The per-leaf-folder cycle (one continuous run)

1. **Learnings** — check `C:\mybizz\logs\mb-wikilinks\learnings\` for prior learnings
   for this source (recurring patterns, confirmed conventions); apply anything
   already-settled rather than re-asking.
2. **Backup** — the leaf folder in ONE action, unedited, before any detection work:
   ```
   /mnt/c/backup-mb-wikilinks/backup-mb-wikilinks_<source>_<folder-path-flattened-with-underscores>_<YYYYMMDDTHHMMSS>/<original-filename>.md
   ```
   ONE run-level timestamp (the per-file 1-second-sleep scheme is retired). `.md` is
   always the true final suffix. Verify the copy count equals the source file count
   before proceeding. If a file is ever found unbacked at verify time, git HEAD (clean
   pre-run tree) is the sanctioned fallback pre-edit state.
3. **Detect** (read-only) — find every candidate cross-reference in the three known
   patterns: backtick-wrapped bare references (`` `document-slug` ``), Related
   Documents table rows (`| ``path/to/file.md`` | relationship |`), inline prose
   references (`see \`document-slug\` ADR`). Resolve each against the CORPUS-WIDE file
   listing (every registered source's md basenames — all of `gbrain sources list`,
   built with es.exe) and classify:
   - `MATCH` — exactly one real file basename anywhere in the corpus. Cross-source
     matches convert (normal in one corpus spanning many folders).
   - `AMBIGUOUS` — collision-exception basename, or resolves to more than one real
     file anywhere in the corpus. Never converted automatically; flagged for the
     developer's decision.
   - `MISSING-DOCUMENT` — matches nothing anywhere but reads as a document reference —
     a serious align-docs finding per the hard-won rule: investigate, never dismiss;
     no conversion.
   - Not a reference — code identifiers, config keys, table/column names, branch
     names, URLs. Skipped entirely; never candidates at all.
   Nothing converted in this step.
4. **Report** — inline, in this exact structure: one heading per file (its path); under
   it, per candidate in line-number order, exactly four parts: (1) line number; (2) the
   anomaly, quoted exactly as it appears; (3) the proposed exact fix —
   `[[slug|Display Text]]` for MATCH, "no proposed fix — flagged for your decision"
   otherwise; (4) a short justification. After the full report: **stop and wait for
   the reply in the same run.**
5. **Approve** — full approval; partial/corrected approval (user edits are
   authoritative — apply exactly what they return); clarification request (answered
   before any approval is final); or rejection (redo the report). Asked in chat, never
   the question tool. No apply without an explicit on-record approval for this exact
   report, in this same run — a clean-looking report still requires this step.
6. **Apply** — only what was approved, exactly as returned. No re-deriving,
   re-interpreting, or extending; nothing else in the file changes — no rewording, no
   restructuring, no touching frontmatter.
7. **Verify** — per edited file:
   ```bash
   diff <backup-path> <edited-file-path>
   ```
   Every changed line must match an approved conversion exactly; anything else → STOP
   and report the anomaly before continuing to the next file.
8. **Commit/push** — only the files edited in this cycle; message identifies leaf
   folder and task (`mb-wikilinks: adr-global — N references converted`); never commit
   unrelated files; skip if the source isn't a git repo or the workflow says no —
   confirm rather than assume.
9. **Log** — append one row to `C:\mybizz\logs\mb-wikilinks\run-log.md` (single
   append-only file): filename, backup path, count of approved references converted,
   diff-clean yes/no, commit hash if step 8 ran. The working record in `in-progress\`
   moves to `last-completed-run\` at close.
10. **Learnings** — record durable patterns for the next leaf folder (recurring
    NO_MATCH resolutions, confirmed naming conventions) in the same learnings file as
    step 1.

**End of run (per source):**
```bash
gbrain sync --source <source-id>
gbrain extract --stale
gbrain doctor
```
Confirm `link_resolution_opportunity` / `graph_signals_coverage` **moved** — not just
"no errors" — and verify `gbrain sources list` last-sync timestamps before reporting
done. The next leaf folder is its own invocation. When every leaf folder in a source
is done, the source is done — move to the next source in the locked order.

## Completion status protocol

- **DONE** — all approved conversions applied, all diffs clean.
- **DONE_WITH_CONCERNS** — completed, but diff anomalies were caught and resolved;
  list them.
- **BLOCKED** — state exactly what stopped the run (unresolved diff anomaly, an edit
  that didn't match the approval text) and what was tried.
- **REPORT_REJECTED** — the user rejected the report; state what must change before
  it's redone.

Never mark a leaf folder DONE if any file's diff check was skipped or unresolved, and
never run apply without the explicit approval on record from the same run.

## Do not

- Do not convert anything during Detect — detection is read-only.
- Do not apply anything without the explicit on-record approval from the same run.
- Do not extend an approval — apply exactly what was returned, nothing derived or
  reworded.
- Do not touch frontmatter, or anything in a file beyond the approved conversions.
- Do not wikilink an ambiguous basename — plain text stays plain text, flagged for
  the developer's decision.
- Do not use `[[folder/basename]]` — bare basename only, or the link will not resolve.
- Do not convert a reference that resolves nowhere — it is a MISSING-DOCUMENT finding
  for align-docs, reported, never buried, never converted.
- Do not convert register, template, or quarantine references, or a Global→Local
  healed reference — re-creating a healed violation is a defect.
- Do not batch a non-leaf folder — decompose it into leaf folders.
- Do not extend scope beyond the scoping list without explicit confirmation — the
  list is the only authorization for scope.
- Do not open anything inside an Anvil code repo — including `theme\assets\docs`.
- Do not trust "no errors" as end-of-run proof — the GBrain counters must move, and
  last-sync timestamps must be verified.
- Do not start without a target, and do not assume one when it is omitted.
