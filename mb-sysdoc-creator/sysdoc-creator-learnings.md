---
title: "sysdoc-creator-learnings"
doc-id: "mb-ad2e912c"
updated: "2026-10-20"
---

# sysdoc-creator — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why. Read
in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | A mb-* skill's canonical source may live in its own GitHub-backed repository rather than the suite folder; an empty or stubbed in-folder skill copy is not proof of lost content. | Before declaring a skill source lost, check the skills catalog's source column and the registered GBrain sources. | skills-catalog source column; repo-organization |
| L2 | An installed-copy delta against an old recorded baseline may be committed canonical change, not drift. | Baselines age; only the current canonical source defines drift. Diff against the current source before classifying any installed divergence. | reference Checks (sync) |
| L4 | Verify a tool live with its own version or health command; when installed, registry and upstream versions disagree, the installed one defines behaviour. | Version surfaces disagree; live output is the only one that defines what will actually run. | Developer-approved lesson |
| L5 | A vendor's SKILL.md (the file actually executed) outranks its README; the vendor's worked examples break ties. | The executed file defines behaviour; READMEs and docs lag it. | Developer-approved lesson |
| L6 | Upstream drift: compare the local commit with the upstream API's latest commit (one call, exact match). | Exact sha equality needs no fetch and beats sync dates and mtimes. | Developer-approved lesson |
| L7 | Check every vendor skill for sub-agent, Task or spawn use against the environment's denial layers, and record the inline-execution alternative. | Parallel execution is denied by the task/spawn denial stack; the honest record is the alternative, not "broken". | Developer-approved lesson |
| L8 | Phrase any Cupcake finding as standing policy, with a pointer to cupcake-config.md's Operational status section, never as permanently true. | Enforcement state changes independently of any rule's content. | Developer-approved lesson |
| L9 | The security-global library is `C:\dev\project-library-global\security-global\`. | A wrong path voids the cross-system check's "none found" verdicts. | Developer-approved lesson |
| L10 | Credentials: discover by variable-name inventory only, never print a value, and mask secrets in every document and example. | Reading a secret-bearing file prints the secret; masked structure is non-sensitive and complete. | Developer-approved lesson |
| L11 | A command whose text names a protected path can be denied by text match; hand such commands to the developer, never disguise them. | Guards match command text, not intent; Read/Glob/Grep tools are unaffected. | Developer-approved lesson |
| L12 | On Refresh, list every fact in the existing documents and mark each carried, corrected or retired before the first approval. | A silently dropped fact survives drafting and surfaces only at the gate — or never. | Developer-approved lesson |
| L13 | Check the explainer's section order against the specification before writing any section. | A rewrite can ship without the required structure even while the standard is fresh. | Developer-approved lesson |
| L14 | Run every documented procedure against the live system before it is written down. | Broken commands would otherwise be published as canonical. | Developer-approved lesson |
| L15 | Prove a scheduled or background mechanism by its work output (its log file exists, its data changed), never by a status counter. | A completed, real run can leave a freshness counter unchanged; only work output proves the work. | Developer-approved lesson |
| L16 | Re-verify every old open item; never carry one forward. | Historical claims silently expire; a stale open item reports done work as outstanding. | Developer-approved lesson |
| L17 | Request the destination grant at Phase 0, since the destination is always the system's folder. | The destination is knowable before drafting; a late request converts a plan into a stall. | Developer-approved lesson |
| L18 | On Refresh, check the learnings table's own structure (columns, ID scheme) against the specification, not only the rows' content. | Off-spec table structure survives a content-only refresh silently. | Developer-approved lesson |