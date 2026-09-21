---
document: "sysdoc-creator — Reference"
doc-id: sysdoc-creator-reference
state: Live
date-created: 2026-09-09
---

# sysdoc-creator — Reference

Execution procedure for the `mb-sysdoc-creator` skill. `skill.md` in this
folder is the authoritative definition; this document is the operational
form. Why the rules are shaped this way: [[sysdoc-creator-explainer|Explainer]].

## Invocation

- Invoke as `/mb-sysdoc-creator (system-name)` plus whatever the
  developer supplies: description, files, URLs, any combination.
- Never auto-trigger. Explicit invocation only.
- `system-name` becomes the file-name prefix. Confirm it matches the
  developer's intended naming before drafting; correct with the
  developer rather than silently normalizing.

## Phase procedure (one continuous run)

### Phase 0 — Resume check and folder setup
1. Run:
   ```bash
   mkdir -p "/mnt/c/mybizz/logs/mb-sysdoc-creator/learnings"
   mkdir -p "/mnt/c/mybizz/logs/mb-sysdoc-creator/in-progress"
   mkdir -p "/mnt/c/mybizz/logs/mb-sysdoc-creator/last-completed-run"
   mkdir -p "/mnt/c/mybizz/logs/mb-sysdoc-creator/abandoned-runs"
   ```
2. Check `in-progress\` for an unfinished run against this exact system
   name. Found → offer resume. Declined → move that run to
   `abandoned-runs\` (never delete) and start fresh.

### Phase 1 — Learnings (open)
3. Read `learnings.md`. Apply anything already-settled; do not re-derive.

### Phase 2 — Intake and destination check
4. Confirm [[doc-suite-specification|config / reference / explainer]] exists at
   [[doc-suite-specification|config / reference / explainer]].
   Missing → STOP and report; never draft from memory of the spec.
5. Read every supplied file in full; fetch every provided URL.
6. No destination path given → STOP here and ask.

### Phase 3 — Research
7. Run multiple GBrain searches — component name, function, adjacent
   terminology separately. One vague pass is not sufficient.
8. Run the cross-cutting check, all four categories, every run:
   Cupcake rules/exemptions; Memory Governor treatment; security-global
   principles; related skills and adjacent GBrain sources. Report
   "none found" explicitly per category.
9. Live-verify everything verifiable by file read, GBrain query, or a
   command you can run. Anything needing a developer-only terminal
   command: hand over the exact command and wait for real output.
10. Track provenance per fact: confirmed-live / confirmed-via-GBrain /
    unverified-from-source / developer-stated.

### Phase 4 — Report
11. Present findings organized by destination document, each material
    fact tagged confirmed or unverified, all four cross-cutting results,
    and any blocked point needing a developer-run command. Stop.

### Phase 5 — Approve (research)
12. Developer reply is one of: approval; correction (authoritative —
    incorporate exactly); further-research request; rejection (return to
    Phase 3 with the named gap). Never draft without this approval.

### Phase 6 — Draft
13. Draft all three documents bound by [[doc-suite-specification|config / reference / explainer]]:
    `-config.md` = state only; `-reference.md` = execution only;
    `-explainer.md` = orientation, suitability, reasoning, in that order.
14. Self-check each draft against its stray-line test; move misplaced
    content to the owning document before Phase 7.

### Phase 7 — Approve (draft)
15. Present all three drafts together. Developer reply: approval;
    corrections (apply exactly); or rejection of specific documents
    (redraft only those). Never write to disk without this approval,
    separate from Phase 5's.

### Phase 8 — Apply
16. Write to the confirmed destination. Same-name document already
    exists → confirm full replacement or merge first; never silently
    overwrite. Write blocked by Cupcake or any policy mechanism →
    Hard Rule 7 (below).

### Phase 9 — Log
17. Append the run record to `C:\mybizz\logs\mb-sysdoc-creator\`:
    system, destination, sources consulted (GBrain queries, URLs,
    files), cross-cutting findings, developer corrections from both
    gates, real outcome.

### Phase 10 — Learnings (close)
18. Append durable patterns to `learnings.md`. Move this run's record
    from `in-progress\` to `last-completed-run\`.

## Hard rules (operational form)

1. Never write a fact from provided source material alone if it can be
   live-verified instead. Source material is a lead, never ground truth.
2. Never guess the destination path. Not given → STOP at Phase 2.
3. Never skip the cross-cutting check — "none found" is a real result,
   not a skipped step.
4. Every fact lives in exactly one of the three documents. Duplication
   across the suite is a drafting error.
5. Never blend confirmed and claimed-but-unverified facts silently —
   unverified items surface as open items or flagged uncertainty.
6. Never mark DONE without Phase 5 and Phase 7 approvals, both on
   record from within the same run.
7. Any Cupcake or policy block, at any phase: STOP, report the exact
   block, state what is needed, wait for the developer's decision.
   Never silently skip, work around, or treat as implicit n/a.

## Completion status protocol

| Status | When |
|---|---|
| DONE | Drafted, approved at both gates, written to confirmed destination |
| BLOCKED | No destination given, or research awaits a developer-run command's real output |
| PERMISSION_REQUIRED | A policy mechanism denied an action (Hard Rule 7) |
| REPORT_REJECTED | Phase 4 findings rejected; name what needs further research |
| DRAFT_REJECTED | Phase 7 rejection; name the document(s); redraft only those |

## Do not

- Do not transcribe supplied material into a canonical doc as fact.
- Do not infer a destination folder from naming convention.
- Do not conditionally skip a cross-cutting category because it seems
  irrelevant.
- Do not duplicate a fact across two of the three documents.
- Do not present unverified claims as settled.
- Do not combine the two approval gates into one.
- Do not work around a policy block, and never invoke `mg-grant` or any
  permission-altering command on your own initiative.
- Do not continue a drafting round after a rejection of that document.
