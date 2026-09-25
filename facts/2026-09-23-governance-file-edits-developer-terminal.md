---
title: "2026-09-23-governance-file-edits-developer-terminal"
doc-id: "2026-09-23-governance-file-edits-developer-terminal"
---
# Fact — governance-file edits are developer-terminal even under group approval

The protected-AI-governance-files policy denies any agent edit to AGENTS.md
regardless of a chat group-approval that names the exact finding: the policy
requires the developer's explicit per-file instruction and cannot see chat
approvals. Working protocol (proven three times, 2026-09-23): hand the
developer the exact old/new lines; they edit; the agent verifies by diff
against the backup. Never re-attempt the edit and never work around it.

Context: session 015 (`sessions/2026-09-23-015-mb-doccycle-makepdlf-first-cycle`),
makepdlf first full cycle (A-1, rule-3 rewording, marker-typo handovers).
Confidence 1.0, method: three live denials + three verified developer
self-edits. Approved at the 2026-09-23 close-out gate.
