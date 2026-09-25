---
title: "doc-maintainer-reference"
doc-id: "doc-maintainer-reference"
---
# mb-doc-maintainer — Reference: Invocation, Tools, Watcher, Procedures

Companion to [[doc-maintainer-config|Configuration]] (the spec — current state)
and [[doc-maintainer-explainer|Explainer]] (what it is and why). Exam set:
[[doc-maintainer-exam-plan|Exam Plan]] (next run's job-spec — synthesized fresh
before each run), [[doc-maintainer-exam-report|Exam Report]] (last run's
verified state), [[doc-maintainer-log|Log]] (events), [[doc-maintainer-learnings|Learnings]]
(transient). The installed `SKILL.md` is the authoritative procedure for the
maintenance loop itself; this reference carries the exact commands and
mechanics an agent consults while running it.

---

## Invoking the maintainer

The maintainer drains the pending-events queue. Invocation is by the developer
asking an OpenCode agent to run it (or any agent session picking up the queue).

```text
1. List the queue:      C:\mybizz\logs\mb-doc-maintainer\pending-events\*.json
2. Empty queue          -> state "no pending events" in one line; stop.
3. Per event: read path + kind, then run the processing loop (SKILL.md §11).
4. After each event:    remove its event file, append one run-log line.
```

**Event file shape** (written by the watcher):

| Field | Meaning |
|---|---|
| `path` | saved document (Windows form) |
| `old_path` | pre-rename path, `move_rename` only |
| `kind` | `creation` / `modification` / `move_rename` / `deletion` |
| `kinds_seen` | raw watcher event classes coalesced into this event |
| `queued_at` | UTC timestamp |

**Operate on saved state only.** The watcher has already coalesced rapid saves
per file; never follow live editing; never process the same event twice in one
invocation; git is supporting context only, never the trigger.

## The processing loop (SKILL.md §11 — authoritative)

```text
Identify change → determine affected contract requirements → determine
affected documentation → repair what can be safely repaired → update required
registration → verify → summarise → Finish
```

The process must terminate. Detection is not a work queue.

Per event kind (SKILL.md §4):

| Kind | Required work |
|---|---|
| creation | frontmatter to exactly `title:`+`doc-id:` = filename stem; correct location; validate references; convert applicable prose references to wikilinks; verify targets; register (creation event) |
| modification | check only change-relevant requirements; restore exact two-field frontmatter (delete every other field); repair affected links; register **only** if a four-event applies (content edits never move the register) |
| move_rename | re-derive `title`/`doc-id` from the new stem; mechanically determinable reference/link updates; register rename; verify links + location; ambiguity → ask |
| deletion | register row set `state: Retired` (+`superseded-by` when known) — rows are never removed; repair references only where the correct replacement is known; report unresolved references |

## Tool commands (exact syntax)

Run from anywhere; tools are stdlib-only Python.

```bash
python3 /mnt/c/mybizz/mb-doc-maintainer/tool/frontmatter.py check <path>
python3 /mnt/c/mybizz/mb-doc-maintainer/tool/frontmatter.py repair <path>
python3 /mnt/c/mybizz/mb-doc-maintainer/tool/links.py scan <path> --root <corpus-root>
python3 /mnt/c/mybizz/mb-doc-maintainer/tool/links.py collisions --root <corpus-root>
python3 /mnt/c/mybizz/mb-doc-maintainer/tool/register.py check <register.md>
python3 /mnt/c/mybizz/mb-doc-maintainer/tool/register.py diff <register.md> --corpus-root <dir>
python3 /mnt/c/mybizz/mb-doc-maintainer/tool/register.py add-creation <register.md> <doc-id> <title> [--state S] [--notes N]
python3 /mnt/c/mybizz/mb-doc-maintainer/tool/register.py set-rename <register.md> <doc-id> --new-doc-id X --new-title Y
python3 /mnt/c/mybizz/mb-doc-maintainer/tool/register.py set-state <register.md> <doc-id> --state S [--superseded-by Z]
```

Exit codes: `frontmatter.py check/repair` → 0 compliant / 1 findings; `register.py check` → 0/1. JSON output on stdout; findings codes: `NULL_BYTES`, `MISSING_CLOSE`, `EMPTY_BODY`, `NO_FRONTMATTER`, `YAML_PARSE`, `NON_STRING_FIELD`, `EXTRA_FIELD`, `TITLE_MISMATCH`, `DOCID_MISMATCH`, `MISSING_REQUIRED_FIELD` (frontmatter); `SCHEMA_MISSING`, `ROW_MALFORMED`, `DUPLICATE_DOC_ID` (register).

Repair discipline (both tools): only the affected byte range changes — frontmatter repair preserves body bytes exactly; register edits touch exactly one row line. Written content is LF.

## Register determination

Walk from the document's path to its corpus/library root: the
`register-local.md` at the root of the document's project library, or
`register-global.md` for `project-library-global`. Discovered live — never
carried. Four-event model: creation, supersession/retirement, rename,
quarantine — no other mutation exists in the tool surface. Register wins
mismatches. Stencils and catalogues are never registered; register files are
catalogue and never register themselves.

## Watcher management

```bash
# state / start / stop (PowerShell)
Get-ScheduledTask -TaskName "mb-doc-maintainer-save-watcher"
Start-ScheduledTask -TaskName "mb-doc-maintainer-save-watcher"
Stop-ScheduledTask  -TaskName "mb-doc-maintainer-save-watcher"
# Stop-ScheduledTask does NOT kill the watcher's PowerShell child (the cmd
# wrapper's child survives the task stop and keeps the single-instance mutex).
# After stopping, kill any orphan explicitly:
Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" |
  Where-Object { $_.CommandLine -like '*save-watcher.ps1*' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

## Known watcher behavior (accepted noise, developer decision F-5 2026-09-25)

Rename-back churn (create → rename → rename-back → delete inside one debounce
window) emits one redundant deletion event for the transient path — its entry
retains only `[Renamed]` and promotes as a deletion of a file that never
durably existed. This is **accepted as known noise** (developer decision,
2026-09-25): the maintainer's deletion handler no-ops on unregistered,
unreferenced paths, so the cost is one extra event file and one no-op run-log
line. Do not treat it as a defect; do not harden the coalescing layer unless
real save patterns make this noise frequent (the narrow drop-rule — drop
entries whose only kind is `Renamed` and which no longer exist at promotion —
is the recorded candidate, rejected for now because a wrong edge case loses
real events).

```bash
# manual run for testing (short debounce)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\mybizz\mb-doc-maintainer\watch\save-watcher.ps1" `
  -ScopeAuthority "C:\mybizz\mybizz-os-docs\os-reference-docs\mybizz-scope-list.md" `
  -QueueDir "C:\mybizz\logs\mb-doc-maintainer\pending-events" `
  -DebounceSeconds 5 -PollSeconds 2

# syntax check after any edit
powershell.exe -NoProfile -Command "[System.Management.Automation.Language.Parser]::ParseFile('C:\mybizz\mb-doc-maintainer\watch\save-watcher.ps1',[ref]$null,[ref]$e)|Out-Null; $e"
```

Task action: `watch\run-watcher.cmd` → runs the script, appends console output
to `C:\mybizz\logs\mb-doc-maintainer\watcher.log`. The script honours
`-ScopeAuthority`, `-QueueDir`, `-DebounceSeconds`, `-PollSeconds`,
`-RunLogPath`.

## Event classification (every finding, exactly one)

| Category | Action |
|---|---|
| Must fix | violates a contract requirement / concrete integrity problem — repair automatically where safe |
| Can wait | real, not part of this event — never a new work queue |
| Doesn't matter | no meaningful impact — no action |
| Requires human judgement | cannot safely determine — concise decision request |

## Reporting formats

Standard summary:

```text
MB Doc Maintainer

Saved: <filename>

Actions:
- <one line per action>

Status:
- G-brain requirements satisfied. | <what remains unresolved>
- No human action required. | <human action required: one line>
```

Decision request (only when judgement is genuinely needed):

```text
MB Doc Maintainer

Saved: <filename>

Issue: <the ambiguity, one line>

Proposed action: <the recommended repair>

Risk: <low/medium/high and why, one line>

Approve / Reject
```

Summary by default; detail on request (what was checked, what changed, what
was decided not to need changing, which contract requirement caused a change).

## Run log append format

One line per maintenance event, appended to
`C:\mybizz\mybizz-config-docs\mb-doc-maintainer\doc-maintainer-run-log.md`:

```text
| date | path | kind | actions | classification |
```

Append-only. Rows are never deleted or rewritten.

## Tests

```bash
cd /mnt/c/mybizz/mb-doc-maintainer && python3 -m unittest discover -s tests
```

40 tests, stdlib unittest, all passing 2026-09-25 (pytest is not installed; the
suites are pytest-compatible if it ever is).

## Do not

- Do not run a full-corpus audit after every save; do not expand a local change into a corpus-wide investigation.
- Do not invent G-brain requirements — enforce `gbrain-doc-contract.md` as written; the contract changes only by developer decision.
- Do not add frontmatter fields beyond `title`/`doc-id`, ever — repair deletes every other field.
- Do not remove register rows — registers are append-only; deletion is a `state: Retired` change.
- Do not guess when the safe action is uncertain — ask, using the decision format.
- Do not create large routine reports; never demand approval for safe mechanical repairs.
- Do not edit `save-watcher.ps1` without re-running the PowerShell parser check — the script must stay pure ASCII (UTF-8 smart punctuation breaks PowerShell 5.1 parsing, confirmed live 2026-09-25).
- Do not read, write, or touch `anvil.yaml`, and never document a folder containing one.
- Do not re-queue or reprocess an event already processed in the invocation; remove the event file after processing.
- Do not expect the standing sync script to sync this source — `mb-doc-maintainer` gets `gbrain sync --source mb-doc-maintainer` explicitly (new-source rule).