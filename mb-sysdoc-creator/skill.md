---
name: mb-sysdoc-creator
description: |
  Creates the canonical three-document suite (config/reference/explainer)
  for a system component, per doc-suite-specification.md. Input is any
  combination of: a plain-language description, uploaded starter
  material, or links/URLs. Researches the real, live, applied state of
  the component — via GBrain search across all sources, direct
  verification where possible, and identification of cross-cutting
  system aspects with real bearing on it (Cupcake rules/exemptions,
  Memory Governor treatment, security-global principles, related
  skills) — rather than transcribing provided source material as fact.
  One continuous skill run per invocation — learnings, intake,
  destination check, research, report, pause inline for approval, draft,
  pause inline for approval, apply, log, learnings — the same modus
  operandi as Docs Manager, mb-align-docs, and mb-wikilinks. Invoked as
  /mb-sysdoc-creator (system-name). Use only when explicitly invoked —
  never auto-trigger.
---

# mb-sysdoc-creator

Produces a real, verified `<name>-config.md` / `<name>-reference.md` /
`<name>-explainer.md` suite for a system component — grounded in
research, not a rewrite of whatever the developer happened to supply.
Provided material is a starting point and a lead to verify, never a
source to transcribe directly into a canonical doc.

**Governing specification:** `doc-suite-specification.md`, permanently
located at `C:\mybizz\mybizz-config-docs\mb-sysdoc-creator\doc-suite-specification.md`.
Every drafted document must satisfy that spec's per-document contents,
never-contains list, and stray-line test before being presented. This
skill does not improvise document structure independently of that spec.

---

## User-invocable

Invoked as `/mb-sysdoc-creator (system-name)`, alongside whatever the
developer supplies in the same message: a description, uploaded files,
URLs, or any combination. `system-name` becomes the file-name prefix
(`<system-name>-config.md`, etc.) — confirm it matches the developer's
intended naming convention (kebab-case, matching this environment's
standing convention) before drafting; correct it with the developer
rather than silently normalizing it.

---

## Section 0 — Hard rules. Do not deviate.

1. **Never write a fact from provided source material alone if it can be
   live-verified instead.** A README, a URL, or a developer's
   description is a lead, not ground truth — this environment has
   repeatedly found source material stale or wrong in ways nobody
   caught until checked live. Where this skill can verify directly
   (GBrain search, reading a real file already in scope), it does.
   Where it can't (a terminal command only the developer can run), it
   hands over the exact command and waits for real output — never
   proceeds on an assumed result.
2. **Never guess the destination path.** If not given in the invocation,
   STOP at Phase 2 and ask. Do not infer a folder from naming convention
   alone, even a highly consistent one.
3. **Never skip the cross-cutting system check**, even when the
   developer's own description seems complete. Every run explicitly
   checks whether Cupcake (rules or exemptions), Memory Governor
   (governance treatment or bypass status), `security-global/`
   principles, related skills, or adjacent GBrain sources have a real
   bearing on this component — not only when one seems obviously
   relevant. A component with none of these findings still gets the
   check; "none found" is a real, reportable result, not a skipped step.
4. **Every fact lives in exactly one of the three documents.** Governed
   by `doc-suite-specification.md`'s single-source-of-truth rule — a
   fact duplicated across two of the three drafted documents is a
   drafting error, not acceptable reinforcement.
5. **Confirmed facts and claimed-but-unverified facts from source
   material are never blended silently.** Where research couldn't
   verify something the developer or a source claimed, the drafted
   document says so plainly (an "open items" entry, a flagged
   uncertainty) rather than presenting it as settled.
6. **Never mark a document set DONE without the developer's explicit
   approval of the drafted content**, separate from and after their
   approval of the research findings. Two distinct approval points, not
   one combined.
7. **If any action is blocked by Cupcake or any other policy
   mechanism, STOP and report the exact block plainly — never silently
   skip the blocked action, substitute a workaround, or proceed as if
   it succeeded.** This applies at any phase: a destination write
   blocked by `cup-no_cross_project_filesystem_access_by_default.rego`,
   a read blocked by a secrets-protection rule, or any other policy
   denial. Report the real error, state what's needed to proceed (e.g.
   a cross-project grant via `mg-grant`, or a different destination),
   and wait for the developer's explicit decision. Never invoke
   `mg-grant` or any other permission-altering command on this skill's
   own initiative — the developer decides whether to grant access, this
   skill only reports that access is needed.

---

## Section 1 — Phase sequence (one continuous run)

### Phase 0 — Resume check and folder setup

Confirm these folders exist; create any that don't before proceeding —
never assume they're already there:
```bash
mkdir -p "/mnt/c/mybizz/logs/mb-sysdoc-creator/learnings"
mkdir -p "/mnt/c/mybizz/logs/mb-sysdoc-creator/in-progress"
mkdir -p "/mnt/c/mybizz/logs/mb-sysdoc-creator/last-completed-run"
mkdir -p "/mnt/c/mybizz/logs/mb-sysdoc-creator/abandoned-runs"
```

Then check `C:\mybizz\logs\mb-sysdoc-creator\in-progress\` for an
unfinished run against this exact system name. If found, offer to
resume from where it left off, including research already gathered and
decisions already made, instead of starting over. If declined, move
that run to `C:\mybizz\logs\mb-sysdoc-creator\abandoned-runs\` (never
deleted) and start fresh.

### Phase 1 — Learnings (open)

Load `C:\mybizz\logs\mb-sysdoc-creator\learnings\` for any prior,
durable pattern about doc-suite drafting in general, or specifically
about this component if it's been partially documented before. Apply
anything already-settled rather than re-deriving it.

### Phase 2 — Intake and destination check

Confirm `doc-suite-specification.md` exists at its permanent location
(`C:\mybizz\mybizz-config-docs\mb-sysdoc-creator\doc-suite-specification.md`).
If it doesn't, STOP and report — do not draft from memory of the spec's
contents or improvise a substitute structure.

Read everything the developer supplied in full — not by filename or URL
alone. Fetch every provided URL. Read every uploaded file's actual
content.

**If no destination path was given: STOP here and ask.** Do not proceed
to research without a confirmed destination.

### Phase 3 — Research (the substantial phase)

1. **GBrain search, multiple queries, not one vague pass.** Search
   across all registered sources for the component's real name and any
   known aliases. A single query is not sufficient — vary terms the way
   real investigation in this environment has (e.g. searching a
   component's name, its function, and adjacent terminology separately
   when the first pass comes back thin).
2. **Cross-cutting system check, explicitly, every run:**
   - Does any Cupcake rule govern, restrict, or exempt this component?
   - Does Memory Governor treat this component specially (a governed
     source vs. a permanent bypass exception, as with vendor-published
     reference material)?
   - Does any `security-global/` principle bear directly on this
     component's defaults or risk profile?
   - Are there related skills, adjacent GBrain sources, or other
     system components with a real structural relationship to this one?
   Report "none found" explicitly for any category with no result —
   never silently omit a category.
3. **Direct verification wherever possible.** For any fact checkable via
   a real file read, a GBrain query, or a command this skill can run
   directly: verify it, don't take the developer's or source material's
   word for it. For anything only checkable via a terminal command this
   skill cannot run itself, present the exact command and wait for the
   developer's real output — mirroring `mb-compile-rules`' Prerequisite 3
   and `mb-submit-memory`'s Detect step.
4. **Track provenance per fact** — confirmed-live, confirmed-via-GBrain,
   claimed-in-source-material-unverified, or developer-stated. This
   tracking is what Phase 5's report and the drafted documents' honesty
   depend on.

### Phase 4 — Report

Present the research findings before drafting anything:
- What was found, organized by the eventual document it will inform.
- Explicit confirmed vs. unverified status for each material fact.
- The cross-cutting system check's results, including any "none found."
- Any point where research was blocked and a developer-run command is
  needed before drafting can proceed responsibly.

Stop and wait for the developer's reply in the same run. Do not proceed
to Phase 5 in this pass.

### Phase 5 — Approve (research)

The developer's reply is one of: approval to proceed to drafting as
reported; a correction or addition (authoritative — incorporate exactly
what they return); a request to research further before drafting; or a
rejection (return to Phase 3 with the specific gap identified).

Phase 6 never runs without explicit approval of the research findings,
in this same run.

### Phase 6 — Draft

Write all three documents, each bound by `doc-suite-specification.md`:

- **`<system-name>-config.md`** — state only. Identity, structure,
  integration facts, open items. No rules, no rationale, no prose
  narrative.
- **`<system-name>-reference.md`** — execution only. Exact commands,
  exact rules as imperatives, procedures as ordered steps, a closing
  "Do not" list. No architecture framing, no justification beyond a
  one-line pointer to the explainer.
- **`<system-name>-explainer.md`** — orientation, suitability, and
  reasoning, in that order: what the thing is in plain terms; a
  conceptual feature summary; explicit best-for/good-for/not-good-for
  suitability; then design reasoning, cross-cutting relationships, and
  open architectural questions. No exact command syntax, no config facts
  restated verbatim.

**Self-check before presenting:** run each document against its own
stray-line test from `doc-suite-specification.md`. Move any misplaced
content to the document that actually owns it before Phase 7.

### Phase 7 — Approve (draft)

Present all three drafted documents together. The developer's reply is
one of: approval to write them to the destination; corrections
(authoritative — apply exactly as returned); or rejection of one or more
documents (return to Phase 6 for the rejected document(s) specifically —
approved documents from this same pass are not re-drafted).

Phase 8 never runs without explicit approval of the drafted content,
separate from Phase 5's research approval.

### Phase 8 — Apply

Write the approved documents to the confirmed destination path from
Phase 2. If a document of the same name already exists there, confirm
with the developer whether this is a full replacement or a merge before
overwriting — never silently overwrite existing canonical docs. If the
write itself is blocked by Cupcake or any other policy mechanism (e.g.
the destination is outside the current project and no grant exists),
apply Hard Rule 7 — stop, report the exact block, and wait for the
developer's decision rather than skipping the write or attempting a
workaround.

### Phase 9 — Log

Append to `C:\mybizz\logs\mb-sysdoc-creator\`: system name, destination
path, sources consulted (GBrain queries run, URLs fetched, files read),
cross-cutting findings, any developer corrections applied at Phase 5 or
7, and the real outcome.

### Phase 10 — Learnings (close)

Record anything durable for next run — a GBrain search pattern that
worked well for this class of component, a cross-cutting check that
turned out relevant in a non-obvious way, a source-material discrepancy
worth remembering. Move this run's record from `in-progress\` to
`last-completed-run\`.

---

## Section 2 — Hard constraints

- No drafting without Phase 5's research approval; no writing to disk
  without Phase 7's separate draft approval.
- No destination path is ever assumed — confirmed explicitly at Phase 2
  or the run stops there.
- Any Cupcake or policy block, at any phase, stops the run for an
  explicit developer decision — never silently skipped, never worked
  around, never treated as an implicit "not applicable."
- The cross-cutting system check (Cupcake, Memory Governor,
  security-global, related skills/sources) runs every time, with
  explicit "none found" reporting — never conditionally skipped based on
  the skill's own judgment that it's "probably not relevant here."
- A fact's provenance (confirmed-live / confirmed-via-GBrain /
  unverified-from-source / developer-stated) is tracked from Phase 3
  onward and reflected honestly in the drafted documents — never
  presented uniformly as settled fact.
- A lost session never loses work — resume (Phase 0) picks up exactly
  where it left off, including research already gathered.

---

## Section 3 — Completion status protocol

- **DONE** — all three documents drafted, approved at both Phase 5 and
  Phase 7, and written to the confirmed destination.
- **BLOCKED** — no destination path was given and the developer hasn't
  yet supplied one, or research could not establish enough confirmed
  fact to draft responsibly and is waiting on a developer-run command's
  real output.
- **PERMISSION_REQUIRED** — an action was denied by Cupcake or another
  policy mechanism (Hard Rule 7). State the exact block encountered and
  what the developer needs to decide (grant access, choose a different
  destination, or otherwise) — never silently skipped or worked around.
- **REPORT_REJECTED** — the developer rejected the Phase 4 research
  findings; state what needs further research before Phase 4 is redone.
- **DRAFT_REJECTED** — the developer rejected one or more drafted
  documents at Phase 7; state which document(s) and why; redraft only
  those at Phase 6.

Never mark a run DONE without both the Phase 5 and Phase 7 approvals on
record from within this same run, and never present a drafted document
that hasn't passed its own stray-line self-check.

---

## Folders

| Folder | Holds |
|---|---|
| `C:\mybizz\logs\mb-sysdoc-creator\` | Permanent history, one record per run |
| `C:\mybizz\logs\mb-sysdoc-creator\learnings\` | Durable patterns from past runs |
| `C:\mybizz\logs\mb-sysdoc-creator\in-progress\` | Current run only — resume source if interrupted |
| `C:\mybizz\logs\mb-sysdoc-creator\last-completed-run\` | Full detail of most recent finished run |
| `C:\mybizz\logs\mb-sysdoc-creator\abandoned-runs\` | Declined-resume runs, kept, never deleted |
