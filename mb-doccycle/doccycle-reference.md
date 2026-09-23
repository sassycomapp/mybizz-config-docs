---
document: "mb-doccycle Usage and Invocation"
doc-id: doccycle-reference
state: Live
date-created: 2026-09-22
---

# mb-doccycle — Usage, Invocation, and Worked Examples

# mb-doccycle — Usage, Invocation, and Worked Examples

Operational reference for the mb-doccycle documentation-management
workflow. Companion to [[doccycle-config|mb-doccycle Configuration]]
(current state) and [[doccycle-run-discipline|mb-doccycle — Shared Run
Discipline]] (the binding run frame — cycle-level steps, approvals,
collective grants, verification, commits and sync). Exam set: the
configuration cycle runs via [[doccycle-skill|the exam skill]] under
[[doccycle-exam-plan|a fresh plan]]; outcomes in [[doccycle-exam-report|
the report]] and [[doccycle-log|the log]].

---

## Invocation

```
/mb-doccycle (all)              # sequential corpus cycles, every in-scope source
/mb-doccycle (corpus)           # one corpus cycle, end to end
/mb-doccycle (phase corpus)     # one phase only against one corpus
/mb-doccycle (closeout)         # bounded session-closeout pass
/mb-doccycle                    # asks which target is meant — never assumed
```

One corpus cycle per session. Quote folder names containing spaces. The
workflow never auto-triggers and never infers which corpus is meant.

## The cycle (per the run frame)

Cycle-level, once per invocation, in order: (1) resume check; (2)
learnings load; (3) scope read (`mybizz-scope-list.md`, live); (4) Cupcake
preflight (plugin active; skeleton handling automatic); (5) collective
grant handover, constructed after detection and presented at the approval
pause.

Per phase, A → B → C, each: verified stop-cold backup sized to the
phase's write surface → detect → report → approve → apply → verify →
commit plan → index row → learnings. B-close gates C. Phase commits land
between phases under the commit plan or the commit allowance.

## The canonical Phase-C tool

```
python3 /mnt/c/mybizz/mb-doccycle/tool/doccycle-detect.py <target> \
  --build-universe-es /mnt/c/dev/project-library-global \
  --format human
```

- Read-only — detection writes nothing; apply happens through the
  governed file tools with the tool's emitted old-string → new-string
  pairs, one pair at a time (highest byte offset first), verified by diff
  against the phase backup.
- `--universe PATH` consumes a pre-built corpus-wide listing; `--format
  json` emits machine-readable pairs with byte offsets.
- Resolution classes: MATCH (emits pair) / AMBIGUOUS / MISSING-DOC-CANDIDATE /
  NO-MATCH / QUARANTINE-KEEP / SKIP classes. Full contract and the 27-test
  suite live in the tool and `C:\mybizz\mb-doccycle\tests\`.

## Grant commands (developer-terminal only)

```
mg-grant --path <folder> --count N          # path slip (folder writes)
git-grant --repo <folder> --count N --minutes M   # commit allowance
mg-revoke --path <folder>
```

Issued in ONE collective block per cycle after detection and approval:
path slips per restricted folder (approved file count + buffer), the
backup-root line, and the commit allowance per repo. The workflow never
issues a grant itself and never works around a denial. Grant paths in
forward-slash WSL form, lowercase. 30-minute default expiry; a re-grant
updates the entry **in place** — a grant of N is N total, not N plus the
residual count; size each block for the whole remaining cycle or request
a follow-up block.

## File search — es.exe (Everything) first

```
"/mnt/c/Program Files/Everything 1.5a/es.exe" -p "C:\dev\" -n 1000000 -s "*.md"
```

Primary tool for every file search. Raise `-n` or scope with `-p` before
filtering — a small unfiltered limit is consumed by backup copies first.
A zero-hit result on a supposedly existing file is verified with one
fallback check before any missing finding is proposed. A fallback to
`find`/`glob` is reported in the run record, never silent. Results are
Windows paths — convert to `/mnt/c/...` before opening.

## Records

```
# run record created at start, appended at every decision point
C:\mybizz\logs\mb-doccycle\in-progress\<run-timestamp>.md
# at close: moved to last-completed-run\ + one row appended to
C:\mybizz\logs\mb-doccycle\run-index.md
# learnings: C:\mybizz\logs\mb-doccycle\learnings\ (advisory, supersession marks)
```

## Verification and sync (per the run frame)

After every write: re-read what was written or diff against the backup —
evidence or silence. Chained commands verify each result before the next.
After commits: per-source GBrain sync for every changed source, verified
per source with `gbrain sources status` — never a blanket success report.

## Worked example — a bounded close-out

```
/mb-doccycle (closeout)
```

1. Inventory exactly what the session changed (files, folders, new links).
2. Run the three phases over those touched files and folders only.
3. One grouped plain-English report; one approval; the same collective
   block for slips and the commit allowance.
4. Anything beyond the session's own changes is proposed for the next
   scheduled cycle — the close-out can never balloon into a run.
5. Commit plan → batch approval → one commit per repo → per-source
   `gbrain sources status` evidence → learnings write-back → index row.

## Completion status protocol

Report one of: **DONE** (all approved conversions and changes applied,
all diffs clean), **DONE_WITH_CONCERNS** (list what was caught and
resolved), **BLOCKED** (state exactly what stopped the run and what was
tried), or the run-record equivalent at close. Never mark a phase done
with a skipped or unresolved diff check, and never apply without an
explicit approval on record from the same run.