---
document: "wikilinks — Reference"
doc-id: wikilinks-reference
state: Live
date-created: 2026-09-10
---

# wikilinks — Reference

Execution procedure for the `mb-wikilinks` skill. `SKILL.md` in the installed
folder (`~/.config/opencode/skills/mb-wikilinks/`) is the authoritative
definition; this document is the operational form. Why the rules are shaped
this way: `wikilinks-explainer.md`.

## Invocation

- `/mb-wikilinks (leaf-folder-name)` — full cycle for that leaf folder, one continuous run.
- `/mb-wikilinks (all)` — every locked source, in order, leaf folder by leaf folder — each
  leaf folder still gets its own complete cycle (own backup, report, approval pause, apply,
  verify, commit); a wide run is a sequence of full cycles, never a merged batch.
- **Empty or omitted target: the skill asks and does nothing until answered.** Never assumed.
- Quote folder names containing spaces: `/mb-wikilinks ("Agent readiness")`.
- **A code repo is not a valid target** — Anvil code repos are denied entirely, including any
  docs folder inside them.
- Explicit invocation only — never auto-trigger, never infer "the next" leaf folder.

## Prerequisites (once, before the first source)

1. Confirm the resolver:
   ```bash
   gbrain config get link_resolution.global_basename
   ```
   If not `true`: `gbrain config set link_resolution.global_basename true`
2. Confirm the target format: `[[basename|Display Text]]` — bare filename stem only. Never
   `[[folder/basename]]` — directory-qualified wikilinks do not resolve in this corpus.
3. Ensure the working directories exist:
   ```bash
   mkdir -p "/mnt/c/backup-mb-wikilinks"
   mkdir -p "/mnt/c/mybizz/logs/mb-wikilinks/learnings"
   mkdir -p "/mnt/c/mybizz/logs/mb-wikilinks/in-progress"
   mkdir -p "/mnt/c/mybizz/logs/mb-wikilinks/last-completed-run"
   mkdir -p "/mnt/c/mybizz/logs/mb-wikilinks/abandoned-runs"
   ```

## Per-source preparation (once per source)

1. **Basename-collision check:**
   ```bash
   find <source-root> -iname "*.md" -exec basename {} \; | sort | uniq -c | sort -rn
   ```
   Any basename with count > 1 → permanent exception: that basename is NEVER wikilinked in
   this source. (Known: `INDEX.md` — 3-way collision in project-library-global.)
2. **Leaf-folder map:** classify every directory — leaf (files directly, or only excluded
   subfolders) vs non-leaf (has subdirectories — decompose into child leaf folders; never
   batch a non-leaf as one unit).
3. Report both the collision-exception list and the leaf-folder map before starting the
   cycle. Do not proceed without confirmation.

## The per-leaf-folder cycle (one continuous run)

1. **Learnings** — check `C:\mybizz\logs\mb-wikilinks\learnings\` for prior patterns for this
   source; apply what is already settled.
2. **Backup** — every file in the leaf folder, unedited, before detection:
   ```
   /mnt/c/backup-mb-wikilinks/backup-mb-wikilinks_<source>_<folder-path-flattened-with-underscores>_<filename>_<YYYYMMDDTHHMMSS>.md
   ```
   `.md` is always the true final suffix; wait ≥1 full second between file backups.
3. **Detect** (read-only) — find every candidate cross-reference in the three known patterns:
   backtick-wrapped bare references (`` `document-slug` ``), Related Documents table rows
   (`| ``path/to/file.md`` | relationship |`), inline prose references
   (`see \`document-slug\` ADR`). Resolve each against the real file listing and classify:
   `MATCH` (exactly one real file), `NO_MATCH` (no file — likely a code identifier, config
   key, or table name), `AMBIGUOUS` (collision-exception basename, multiple files, or
   outside this source — flag, don't guess). Nothing converted in this step.
4. **Report** — inline, in this exact structure: one heading per file (its path); under it,
   per candidate in line-number order, exactly four parts: (1) line number; (2) the anomaly,
   quoted exactly as it appears; (3) the proposed exact fix — `[[slug|Display Text]]` for
   MATCH, "no proposed fix — flagged for your decision" otherwise; (4) a short justification.
   After the full report: **stop and wait for the reply in the same run.**
5. **Approve** — full approval; partial/corrected approval (user edits are authoritative —
   apply exactly what they return); clarification request (answered before any approval is
   final); or rejection (redo the report). No apply without an explicit on-record approval
   for this exact report, in this same run — a clean-looking report still requires this step.
6. **Apply** — only what was approved, exactly as returned. No re-deriving, re-interpreting,
   or extending; nothing else in the file changes — no rewording, no restructuring, no
   touching frontmatter.
7. **Verify** — per edited file:
   ```bash
   diff <backup-path> <edited-file-path>
   ```
   Every changed line must match an approved conversion exactly; anything else → STOP and
   report the anomaly before continuing to the next file.
8. **Commit/push** — only the files edited in this cycle; message identifies leaf folder and
   task (`mb-wikilinks: adr-global — N references converted`); never commit unrelated files;
   skip if the source isn't a git repo or the workflow says no — confirm rather than assume.
9. **Log** — append to `C:\mybizz\logs\mb-wikilinks\run-log.md` (or the in-progress record
   moved to `last-completed-run\` at close-out): filename, backup path, count of approved
   references converted, diff-clean yes/no, commit hash if step 8 ran.
10. **Learnings** — record durable patterns for the next leaf folder (recurring NO_MATCH
    resolutions, confirmed naming conventions) in the same learnings file as step 1.

**End of run:**
```bash
gbrain sync --source <source-id>
gbrain extract --stale
gbrain doctor
```
Confirm `link_resolution_opportunity` / `graph_signals_coverage` **moved** — not just "no
errors." Report the run complete. The next leaf folder is its own invocation. When every
leaf folder in a source is done, the source is done — move to the next source in order.

## Scope rules

**Locked sources, in this order:** 1. `project-library-global` — `/mnt/c/dev/project-library-global`; 2. `dev-root` — `/mnt/c/dev/dev-root`; 3. `dev-makepdlf` — content ONLY in
`/mnt/c/dev/dev-makepdlf/makepdlf-project-library` (the `makepdlf` sibling is a ceremonial
placeholder — never scanned). Scope is intersected with the scope scaffold — out-of-scope
stays out in every mode.

**Explicitly excluded sources (never run against, even casually asked):** `mb-3-cs` code +
project-library; `mb4ecom` (placeholder); `mb5pdlf` (disposable test project);
`project-template` (wikilinks belong to real projects at init); `C:\pdlf` (outside the path
boundary). Asked to extend scope to an excluded source → stop and confirm explicitly; a
general "keep going" is never authorization.

**Blanket folder exclusions within any in-scope source:** any Anvil code repo (denied
entirely — including any docs folder inside it); `obsolete`; `archive`; any folder with
`backup` in the name; `templates-global`; `quarantine`/`Quarantine`;
`register-global`/`register-local` (align-docs territory); `pdlf-temp`; `workspace`;
`.gstack`/`.opencode`/`.scratch`/`.out-of-scope`; `Frontmatter-prompts` (under dev-root).

## Completion status protocol

- **DONE** — all approved conversions applied, all diffs clean.
- **DONE_WITH_CONCERNS** — completed, but diff anomalies were caught and resolved; list them.
- **BLOCKED** — state exactly what stopped the run (unresolved diff anomaly, an edit that
  didn't match the approval text) and what was tried.
- **REPORT_REJECTED** — the user rejected the report; state what must change before it's redone.

Never mark a leaf folder DONE if any file's diff check was skipped or unresolved, and never
run apply without the explicit approval on record from the same run.

## Do not

- Do not convert anything during Detect — detection is read-only.
- Do not apply anything without the explicit on-record approval from the same run.
- Do not extend an approval — apply exactly what was returned, nothing derived or reworded.
- Do not touch frontmatter, or anything in a file beyond the approved conversions.
- Do not wikilink a collision-exception basename — plain text stays plain text.
- Do not use `[[folder/basename]]` — bare basename only, or the link will not resolve.
- Do not batch a non-leaf folder — decompose it into leaf folders.
- Do not run against excluded sources, or extend scope without explicit confirmation.
- Do not open anything inside an Anvil code repo — including `theme\assets\docs`.
- Do not trust "no errors" as end-of-run proof — the GBrain counters must move.
- Do not start without a target, and do not assume one when it is omitted.
