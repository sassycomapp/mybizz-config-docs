---
name: mb-wikilinks
description: |
  Convert existing cross-references (backtick paths, inline "see X ADR" prose,
  Related Documents tables) into GBrain-resolvable [[wikilink]] syntax. One
  continuous skill run per leaf folder — learnings, backup, detect, report,
  pause inline for approval, apply, verify, commit/push, log, learnings — the
  same single-run modus operandi as Docs Manager. Detect never writes to a
  file; apply only runs against the explicit approval returned in the same run.
  Invoked per leaf folder as /mb-wikilinks (leaf-folder-name). Use only when
  explicitly invoked for the wikilink retrofit task — never auto-trigger. Scope
  is locked to project-library-global, dev-root, and dev-makepdlf
  (makepdlf-project-library only). Do not run against mb-3-cs, mb4ecom,
  mb5pdlf, or project-template sources — these are explicitly excluded (see
  Section 0).
---

# mb-wikilinks

Converts this corpus's existing cross-reference conventions (backtick-wrapped
paths, inline prose references, Related Documents tables) into `[[wikilink]]`
syntax that GBrain's link extractor can actually parse into a real graph.

**One continuous run per leaf folder — same modus operandi as Docs Manager.**
`/mb-wikilinks <leaf-folder-name>` is a single skill invocation covering
learnings → backup → detect → report → approve → apply → verify →
commit/push → log → learnings. It is not two separate invocations. The
run pauses in place at the report step and presents findings; the moment
the user replies with approvals in the same conversational continuum, the
same run resumes through apply, verify, commit/push, log, and learnings.
The user never has to type `/mb-wikilinks <folder>` a second time to
complete a folder that's already been started.

**Why this runs before mb-align-docs:** mb-align-docs validates
cross-document references as part of its content-agreement function
(register enforcement, dead-reference detection against `obsolete` /
`imported-context`). It needs a stable, final reference convention to
validate against. Running this retrofit first means mb-align-docs
validates against `[[wikilink]]` syntax as the permanent convention,
rather than validating the old backtick/table style and needing a
re-scope once wikilinks land. mb-align-docs has not yet been run for this
reason — do not start it until this retrofit's in-scope sources
(Section 0) are complete.

---

## User-invocable

When the user types `/mb-wikilinks <leaf-folder-name>`, run the full
Section 3 cycle for that specific leaf folder, start to finish, as one
continuous run. The folder name is always given explicitly by the user —
do not infer which leaf folder is "next" and run it automatically.

Quote folder names containing spaces, e.g. `/mb-wikilinks "Agent readiness"`.

---

## Section 0 — Locked scope. Do not deviate.

**In scope, in this order:**

1. `project-library-global` — `/mnt/c/dev/project-library-global`
2. `dev-root` — `/mnt/c/dev/dev-root`
3. `dev-makepdlf` — content lives ONLY in `/mnt/c/dev/dev-makepdlf/makepdlf-project-library`.
   The sibling `makepdlf` folder is a ceremonial placeholder (this project has
   no Anvil code repo) — do not scan or touch it.

**Explicitly excluded — do not run this skill against these under any
circumstance, even if asked casually to "do the rest":**

- `mb-3-cs-code`, `mb-3-cs-project-library` — will be migrated into a new
  project (`dev-mb3cons`) via Step 11 init; current paths will cease to exist
- `mb4ecom-code`, `mb4ecom-project-library` — placeholder, no real content yet
- `mb5pdlf-code`, `mb5pdlf-project-library` — disposable test project, reset
  repeatedly during PDLF development
- `project-template` — wikilinks belong to real projects at Step 11 init, not
  the template source itself
- `pdlf` (the installed application at `C:\pdlf`) — not under `C:\dev`, out of
  scope by path boundary

**Blanket folder exclusions within any in-scope source:**

- any folder named `obsolete`
- any folder named `archive`
- any folder with `backup` in the name, in any variation
- `templates-global` — frontmatter status still unresolved (5 files with no
  frontmatter block at all); excluded from this retrofit regardless of that
  status being fixed later
- `quarantine` / `Quarantine` — quarantined content, not live documentation
- `register-global` / `register-local` — structured register tables, not
  narrative content; mb-align-docs' territory, not this skill's
- `pdlf-temp` — working/temp folder
- `workspace` — working folder, not documentation content
- `.gstack`, `.opencode`, `.scratch`, `.out-of-scope` — tooling/dotfolders,
  never content
- `Frontmatter-prompts` (under `dev-root`) — temporary working folder, not
  documentation content

If asked to extend scope to an excluded source, stop and confirm explicitly
with the user before proceeding — do not treat a general instruction to
"keep going" as authorization to expand scope.

---

## Section 1 — Prerequisites (one-time, before the first source)

1. Confirm the global-basename wikilink resolver is enabled:
   ```bash
   gbrain config get link_resolution.global_basename
   ```
   If not `true`, set it:
   ```bash
   gbrain config set link_resolution.global_basename true
   ```
2. Confirm the wikilink target format: `[[basename|Display Text]]` — bare
   filename stem (no folder prefix, no extension), NOT `[[folder/basename]]`.
   This corpus's folder names (`adr-global`, `specifications-global`, etc.)
   are not in GBrain's compiled `DIR_PATTERN`, so directory-qualified
   wikilinks will never resolve here — bare-basename is the only working form.
3. Create the two working directories if they don't already exist:
   ```bash
   mkdir -p "/mnt/c/backup-wikilinks"
   mkdir -p "/mnt/c/mybizz/logs/wikilinks"
   ```

---

## Section 2 — Per-source preparation (once per source, before its first leaf folder)

1. **Basename-collision check.** Run across the full source:
   ```bash
   find <source-root> -iname "*.md" -exec basename {} \; | sort | uniq -c | sort -rn
   ```
   Any basename with count > 1 is a collision within this source. Record each
   as an exception: that basename is NEVER wikilinked in this source — leave
   it as plain text / backtick reference instead. (Known exception already
   confirmed: `INDEX.md` collides 3 ways in `project-library-global`.)

2. **Leaf-folder map.** List all directories in the source, classify each as:
   - **leaf** — contains files directly, no subdirectories (or only
     excluded subdirectories per Section 0's blanket exclusions)
   - **non-leaf** — contains subdirectories; never batch this as one unit,
     decompose into its child leaf folders instead

3. Report both the collision-exception list and the leaf-folder map to the
   user before starting Section 3. Do not proceed without this confirmed.

---

## Section 3 — Per-leaf-folder cycle (one continuous run)

`/mb-wikilinks <leaf-folder-name>` runs this entire cycle as a single
invocation, pausing only in place at the approval step (step 5) and
resuming in the same run once the user replies.

### Step 1 — Learnings

Check `/mnt/c/mybizz/logs/wikilinks/` for any prior learnings file for this
source (e.g. recurring `NO_MATCH` patterns already resolved in an earlier
leaf folder, naming conventions already confirmed). Apply anything
already-settled rather than re-asking.

### Step 2 — Backup

Back up every file in the leaf folder, unedited, before any detection work
happens:
```
/mnt/c/backup-wikilinks/backup-wikilinks_<source>_<folder-path-flattened-with-underscores>_<filename>_<YYYYMMDDTHHMMSS>.md
```
Example, for `dev-makepdlf/makepdlf-project-library/docs-local/system-description.md`:
```
/mnt/c/backup-wikilinks/backup-wikilinks_dev-makepdlf_docs-local_system-description_20260801T143022.md
```
The `.md` extension is always the true final suffix — never append the
timestamp after it. Wait one full second between each file's backup, so
timestamps can never collide.

### Step 3 — Detect (read-only, no edits)

For each file in the folder, identify every candidate cross-reference
across all three known patterns:
- Backtick-wrapped bare references: `` `document-slug` ``
- Related Documents table rows: `` | ``path/to/file.md`` | relationship | ``
- Inline prose references: `see \`document-slug\` ADR`, `(\`document-slug\` ADR)`

For each candidate, note its exact line number, then resolve it against the
actual file listing (`gbrain sources list` / `find <source-root> -iname
"*.md"`) and record one of:
- `MATCH` — matches exactly one real file basename in this source.
- `NO_MATCH` — does not match any real file (likely a code identifier,
  config key, or table name, not a document reference at all).
- `AMBIGUOUS` — matches a Section 2 collision-exception basename, or
  resolves to more than one real file, or references a file outside this
  source entirely (expected for cross-source references — flag, don't guess).

Do not convert anything. Do not write to any document file in this step.

### Step 4 — Report

Present the findings inline, in the chat, in this exact structure — do not
substitute a different format:

- One heading per file, using the file's path as the heading.
- Under each heading, one entry per candidate, in line-number order,
  formatted as exactly four parts, in this order:
  1. **Line number**
  2. **State the anomaly** — what was found, quoted exactly as it appears
  3. **State the proposed fix** — the exact `[[slug|Display Text]]` this
     would become, for `MATCH` candidates; "no proposed fix — flagged for
     your decision" for `NO_MATCH` / `AMBIGUOUS`
  4. **Justify** — why this is believed to be a document reference (or,
     for `NO_MATCH`/`AMBIGUOUS`, why it's uncertain) — only as long as
     needed, not padded

Example:
```
### adr-global/anvil-platform-constraints.md

- Line 42 — anomaly: backtick reference `` `payment-security-boundary-vault` ``
  in prose — proposed fix: `[[payment-security-boundary-vault|Vault system]]`
  — justification: matches a real file in this source; used in "the custom
  Vault system (`payment-security-boundary-vault` ADR)" pattern
- Line 58 — anomaly: backtick reference `` `app_tables` `` — proposed fix:
  none, flagged NO_MATCH — justification: no file in this source has this
  basename; reads as a code identifier, not a document reference
```

After the full report is presented, stop and wait for the user's reply in
the same run. Do not proceed to Step 6 in this pass.

### Step 5 — Approve (inline, same run, user's next message)

The user's reply is one of:
- Full approval of the report as presented
- A partial/corrected approval — their own edits to any entry are
  authoritative; apply exactly what they return, not the original proposal,
  wherever they changed it
- A request for clarification on specific entries, answered before any
  approval is treated as final
- A rejection of the report, to be redone

Step 6 never runs without an explicit approval on record for this exact
report, in this same run. A clean-looking report with no `NO_MATCH`/
`AMBIGUOUS` entries still requires this step.

### Step 6 — Apply

For each file with at least one approved conversion, apply only what was
approved — exactly as returned in Step 5, using the user's own edits where
given. Do not re-derive, re-interpret, or extend beyond the approved list.
Do not alter anything else in the file — no rewording, no restructuring,
no touching frontmatter.

### Step 7 — Verify

For each edited file, diff against its Step 2 backup:
```bash
diff <backup-path> <edited-file-path>
```
Confirm every changed line matches an approved conversion exactly, and
nothing else differs. If the diff shows any unexpected change — including
an approved-looking change that doesn't match the approval text precisely —
STOP. Report the anomaly to the user before continuing to the next file.

### Step 8 — Commit/push (if this source is a git repo with a remote)

If applicable per the source's normal workflow, stage and commit only the
files edited in this cycle, with a message identifying the leaf folder and
this task (e.g. `mb-wikilinks: adr-global — N references converted`).
Do not commit unrelated files. Skip this step entirely if the source isn't
a git repo or the user's standing workflow doesn't call for a commit here —
confirm rather than assume.

### Step 9 — Log

Append to `/mnt/c/mybizz/logs/wikilinks/`: filename, backup path, number of
approved references converted, diff-clean (yes/no), commit hash if step 8
ran.

### Step 10 — Learnings

Record anything durable that would save time on the next leaf folder in
this source — e.g. a `NO_MATCH` pattern that recurred and how it was
resolved, a naming convention confirmed. Write to the same learnings file
checked in Step 1.

### End of run

```bash
gbrain sync --source <source-id>
gbrain extract --stale
gbrain doctor
```
Confirm `link_resolution_opportunity` / `graph_signals_coverage` moved, not
just "no errors." Report the run complete. The next leaf folder starts as
its own separate `/mb-wikilinks <folder>` invocation, whenever the user
chooses to run it. Once every leaf folder in a source is done, the source
is done — no additional aggregation or re-validation step exists or is
required. Move directly to the next source in Section 0's order.

---

## Section 4 — Completion status protocol

Report one of the following at the end of a run:

- **DONE** — all approved conversions applied, all diffs clean.
- **DONE_WITH_CONCERNS** — completed, but list any diff anomalies caught
  and resolved.
- **BLOCKED** — cannot proceed; state exactly what stopped the run (e.g. an
  unresolved diff anomaly, or an edit that didn't match the approval text)
  and what was tried.
- **REPORT_REJECTED** — the user rejected the Step 4 report; state what
  needs to change before it's redone.

Never mark a leaf folder DONE if any file's diff check was skipped or
unresolved, and never run Step 6 (apply) without a corresponding explicit
approval on record from within this same run.

A source is complete once every one of its leaf folders has independently
reported DONE (or DONE_WITH_CONCERNS, with concerns resolved) — no separate
source-level status report exists.
