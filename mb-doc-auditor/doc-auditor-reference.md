---
title: "doc-auditor-reference"
doc-id: "mb-a644e935"
---
# mb-doc-auditor — Reference: Invocation, Tools, Procedures

Companion to [[doc-auditor-config|Configuration]] (the spec — current state)
and [[doc-auditor-explainer|Explainer]] (what it is and why). Exam set:
[[doc-auditor-exam-plan|Exam Plan]] (next run's job-spec — synthesized fresh
before each run), [[doc-auditor-exam-report|Exam Report]] (last run's verified
state), [[doc-auditor-log|Log]] (events), [[doc-auditor-learnings|Learnings]]
(transient). The installed
`SKILL.md` is the authoritative procedure for the audit loop itself; this
reference carries the exact commands and mechanics an agent consults while
running it.

---

## Invoking the auditor

The auditor runs one audit per invocation over one stated scope. Invocation is
by the developer asking an OpenCode agent to run it — explicitly or on a stated
audit condition.

```text
1. State the audit scope and its purpose (the invocation supplies both;
   missing either -> ask before examining anything).
2. Run the processing loop (SKILL.md §11) against the G-brain contract.
3. Apply safe mechanical repairs (tooling `repair --apply`); classify the rest.
4. Append one audit-record block; deliver the concise summary; finish.
```

**Never:** triggered by a document save; drains no queue; runs no scheduler
(v1 has none — "defined schedule" is future/not established). One run = one
scope = one terminal state. Never an open-ended reconciliation loop.

## The processing loop (SKILL.md §11 — authoritative)

```text
Identify audit scope → load authoritative G-brain requirements → examine
relevant documentation → detect potential integrity conditions → determine
affected requirements → classify each significant finding → repair safe,
mechanically determinable issues → verify repairs and remaining conditions →
summarise result → Finish
```

The process must terminate. More detectable differences are not evidence the
audit is incomplete.

## Tool commands (exact syntax)

Tools are stdlib-only Python; the orchestrator imports the maintainer's
`frontmatter.py`/`links.py`/`register.py` from
`/mnt/c/mybizz/mb-doc-maintainer/tool/` (shared infrastructure — that repo
remains their home).

```bash
python3 /mnt/c/mybizz/mb-doc-auditor/tool/audit.py check --root <audit-root>
python3 /mnt/c/mybizz/mb-doc-auditor/tool/audit.py repair --root <audit-root> [--fix frontmatter,register] [--apply]
python3 /mnt/c/mybizz/mb-doc-auditor/tool/scope.py paths <root>
python3 /mnt/c/mybizz/mb-doc-auditor/tool/scope.py validate --root <dir>
python3 /mnt/c/mybizz/mb-doc-auditor/tool/scope.py discover-register <path>
python3 /mnt/c/mybizz/mb-doc-auditor/tool/runlog.py summary [--log PATH]
python3 /mnt/c/mybizz/mb-doc-auditor/tool/gbrain_reader.py sources|orphans|live
python3 /mnt/c/mybizz/mb-doc-auditor/tool/record.py append --scope S --purpose P --checked C --terminal T [counts/flags] [--records PATH] [--register PATH]
```

`audit.py check` is read-only and always exit 0 (findings ride in JSON).
`audit.py repair` without `--apply` is a dry run (zero bytes changed, verified
by tests); with `--apply` it performs only the mechanical repairs below and
re-runs the corresponding checks — the verification rides in the same result.
`repair` exits 0 when nothing was refused, 1 with residual findings (refusals
are the human-judgement path, never silent).

## What the tooling repairs automatically (and refuses)

| Repair | Condition |
|---|---|
| Frontmatter restore | exact two-field block (`title`/`doc-id` = stem); body byte-preserved; structurally unrepairable files (null bytes, missing close, empty body) are reported, never touched |
| Register add-creation | in-scope file with no register row AND unique stem AND no basename collision |
| Register retire-in-place | live-state row matching no file under any doc-id candidate, ONLY when the audit root is the register's library root; rows already Retired/Superseded/Quarantined are history, never re-flagged |

Refusal classes (surfaced, never guessed): collision stems; multiply-occurring
stems (nested-corpus doc-id convention); obsolete rows outside a library-root
audit; structurally unrepairable frontmatter. Links are never tool-repaired —
semantics are agent-level.

Doc-id candidates (detection only, lowercase): bare stem, trailing-pair path
join, full relative join. The nested-corpus convention itself is a developer
decision (config open item 1).

## Scope and register determination

Scope authority (read live, never carried):
`C:\mybizz\mybizz-os-docs\os-reference-docs\mybizz-scope-list.md`. Exclusions:
authority exceptions and folder-name rules (parsed live), the Anvil class rule
(any folder containing `anvil.yaml` — the file itself is never read), dotdirs,
`.git`, and treatment classes (`tmp-` (O3), stencils, quarantine, backups,
catalogue, logs). Register files are catalogue and never scanned as documents.

Register universe: discovered live by walking up from the audit root —
`<dir>/register-local.md` or `<dir>/register-local/register-local.md`, likewise
`register-global`. Current known inventory (six files):
`register-paths.md` in the planning folder. `pdlf-register.md` is outside the
inventory — surface for human judgement if a C:\pdlf scope encounters it.

## Run-log evidence

```bash
python3 /mnt/c/mybizz/mb-doc-auditor/tool/runlog.py summary
```

Hard-wired to
`C:\mybizz\mybizz-config-docs\mb-doc-maintainer\doc-maintainer-run-log.md` (the
maintainer SKILL.md §10 path — not the unrelated `doc-maintainer-log.md` in the
same directory). Absent/empty → "no maintenance history available"; the audit
proceeds. Evidence only — a repeated event does not create an audit task
without a reasoned connection to a contract requirement.

## Finding classification (every finding, exactly one)

| Category | Action |
|---|---|
| Must fix | violates a contract requirement / concrete integrity problem — repair automatically where safe |
| Can wait | real, not needed for this purpose/scope — never a new work queue; never blocks completion |
| Doesn't matter | no meaningful impact — no action |
| Requires human judgement | cannot safely determine — concise decision request |

## Reporting formats

Standard summary:

```text
MB Doc Auditor

Scope:
<the audited scope>

Checked:
- <examination areas actually performed>

Actions:
- <one line per action>

Outstanding:
- <what remains unresolved, if anything>

Status:
Corpus healthy against defined G-brain requirements
[with N issues requiring human judgement].
```

Terminal states: `AUDIT COMPLETE` with either "No outstanding issues requiring
action" or "except for N issues requiring human judgement".

Decision request (only when judgement is genuinely needed):

```text
MB Doc Auditor

Issue:
<the ambiguity, one line>

Proposed action:
<the recommended repair>

Risk:
<low/medium/high and why, one line>

Approve / Reject
```

Summary by default; detail on demand from the audit record (what was checked,
what changed and why, what was decided not to need changing, which requirement
caused an action, which run-log entries led to investigation).

## Audit record append format

One block per run, appended to
`C:\mybizz\mybizz-config-docs\mb-doc-auditor\doc-auditor-records.md`
(append-only; file created with two-field frontmatter + register row on first
use):

```text
## <date> — scope: <scope>

- purpose: ...
- checked: ...
- findings: must-fix=N, can-wait=N, doesnt-matter=N, human-judgement=N
- actions: ...
- outstanding: ...
- terminal: ...
```

## Tests

```bash
cd /mnt/c/mybizz/mb-doc-auditor && python3 -m unittest discover -s tests
```

22 tests, stdlib unittest, all passing 2026-09-25 — including byte-preservation
through auditor-routed repairs and every refusal class.

## Do not

- Do not trigger on saves; the auditor is never a save-time handler and never duplicates `mb-doc-maintainer`.
- Do not involve DocCycle in any way (modify, migrate, refactor, dismantle, retire, extract from, incorporate).
- Do not invent G-brain requirements — enforce `gbrain-doc-contract.md` as written.
- Do not remove register rows — retirement is `state: Retired` in place; wrong-register rows are retired there plus appended in the correct register.
- Do not auto-register collision stems or multiply-occurring stems — surface for human judgement.
- Do not write to G-brain — `gbrain_reader.py` is read-only by construction.
- Do not read, write, or touch `anvil.yaml`, and never scan a folder containing one.
- Do not default to the largest possible scan; scope is minimum-sufficient for the stated purpose.
- Do not guess when the safe action is uncertain — ask, using the decision format.
- Do not turn the maintainer run-log into a work queue, and do not generate large routine reports.
