---
title: "doc-suite-specification"
doc-id: "mb-f4adba8c"
updated: "2026-10-15"
---
# Doc Suite Specification — config / reference / explainer / learnings

The one specification for the documents that describe every skill and system kept by System Integrity. mb-sysdoc-creator writes documents to it. mb-config-manager reads documents by it. Read it before writing or changing any of these documents.

---

## The folder

- Every skill or system has one folder: `C:\mybizz\mybizz-config-docs\{system}\`.
- The folder name is the system's name. A system MyBizz built starts with `mb-`. An external system keeps its issuer's name.
- The folder holds exactly four documents, one of each, found by the ending of the file name:

| Ending | Document | Holds |
|---|---|---|
| `-config.md` | config | State: what exists, what it is set to, and the issuer's standard for it |
| `-reference.md` | reference | Execution: what an agent needs while working with the system |
| `-explainer.md` | explainer | Orientation and reasoning: what it is, whether to use it, why it works this way |
| `-learnings.md` | learnings | What differs from, or adds to, the standard in the MyBizz setup, and why |

- A new document takes the same name start as the documents already in its folder, for example `doc-check-learnings.md` beside `doc-check-config.md`. In a new or empty folder it takes the folder name, for example `commit-all-config.md`. A document is never renamed.
- An integrity system's folder may also hold the working files that system needs to run, each listed in its own config. Nothing else is kept in any folder.

---

## One fact, one home

Every fact exists in exactly one document. A fact written twice drifts. If a fact appears in two documents, one of them is wrong about where it belongs.

---

## The standard

- The standard is the issuer's authoritative specification for the installed version.
- Its sources are the issuer's official documentation, source repository, release notes and configuration schema.
- For a system MyBizz built, MyBizz is the issuer. The standard is the system's own source files.
- Every standard value is recorded with a link to the exact source it came from. A value with no source is an open item, never a standard.

---

## `-config.md` — State

**Purpose:** a settings sheet. It answers "what exists, what is it set to, and what does the issuer say it should be".

**Contains, in this order:**

1. **Identity table**, one row each:

| Field | Value |
|---|---|
| Issuer | The issuer's name. `MyBizz` for a system MyBizz built |
| Installed version | The version live now |
| Standard taken from | The issuer version the standard values come from |
| Last researched | The date of the last research run |

2. **Settings tables**, one per settings area, all with these columns:

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|

   - **Issuer standard:** the issuer's value for the installed version. `—` when the issuer sets none.
   - **MyBizz value:** the value live now, as verified.
   - **Source:** a link to the exact issuer page or file the standard came from.
   - **Learning:** the learnings ID (`L3`) that justifies a difference. Blank when the MyBizz value equals the standard.
   - Paths, versions, ports, files, folders and integrations are all settings, and use the same table.

3. **Open items:** anything not yet verified, stated as a gap, never guessed.

**Never contains:** a rule, a reason, prose, a list of sources, or history.

**Placement test:** a line belongs here when it goes stale the moment a setting changes, with no reasoning changing.

---

## `-reference.md` — Execution

**Purpose:** what an agent consults while doing the work. Every line is immediately actionable.

**Contains:**

- Exact commands, syntax and invocation patterns.
- Exact rules, stated as imperatives.
- Procedures, as numbered steps.
- **Authoritative sources** (required):

| Source | Link | Issuer version | Date checked |
|---|---|---|---|

- **Checks** (required): how to read each config setting live, the installed version, and whether the system works.

| Check | Method | Run by |
|---|---|---|

   - **Check** names a config setting exactly, or `Installed version`, or `Works`.
   - **Run by** is `agent`, or `developer` where Cupcake reserves the action.

- A **Do not** list, at the end.

**Never contains:** a value (values live in config), a reason beyond a one-line pointer to the explainer, architecture framing, or history.

**Placement test:** a line belongs here when deleting it would make an agent mid-task do the wrong thing.

---

## `-explainer.md` — Orientation, suitability and reasoning

**Purpose:** the understanding a reader builds once, so decisions about this system are made with real understanding. Required sections, in this order:

1. **What it is:** plain terms, no assumed jargon. What problem it solves, for whom, in what situation.
2. **What it can do:** capabilities, not commands.
3. **Suitability:** best for, good for, and not good for, naming the right tool where one exists.
4. **Why it works this way:** the reasons behind its structure and its sharpest rules, and where it sits relative to the systems around it.
5. **What has to happen:** what the developer and other systems must keep doing for it to keep working.

**Never contains:** an exact command, a value, a citation, or history.

**Placement test:** a sentence belongs here when it explains a why, a trade-off or a relationship. A sentence that only states a what or a how belongs in another document.

---

## `-learnings.md` — What differs and why

**Purpose:** the nuances, workarounds, preferences and unique settings that make the MyBizz setup work. They are read in full before any research, examination or proposal for this system.

**Contains one table:**

| ID | Learning | Why it holds | Source |
|---|---|---|---|

- **ID:** `L1`, `L2` and so on. An ID is never reused.
- **Learning:** one fact, stated as it is true now.
- **Why it holds:** the reason it differs from or adds to the standard.
- **Source:** the issuer page, file or finding it came from.

**Rules:**

- An entry is added or changed only with the developer's approval.
- An entry that stops being true is removed. Any config row pointing to it is corrected in the same change.
- No dates, no history, no narrative.

**Placement test:** a line belongs here when losing it would make an agent set up or examine this system wrongly.
