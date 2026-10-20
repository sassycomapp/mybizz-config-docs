---
title: "gbrain-dream-cycle-learnings"
doc-id: "mb-b03f3642"
updated: "2026-10-20"
---
# GBrain Dream Cycle — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why. Read
in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | `gbrain dream --dry-run` is not a zero-cost preview: it runs the scored triage LLM pass and caches its verdicts, skips the synthesis subagents and the judgment phases, and cannot serve as the post-run governance discipline. | The executed binary's own help defines behavior; the governance discipline requires a real run. | `gbrain dream --help` (0.59.18.0); [[[mybizz-config-docs:memory-governor/memory-governor-explainer\|Memory Governor Explainer]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-explainer.md) |
| L2 | Autopilot is off by decision: the cycle runs by hand weekly, after the Sunday backup, through `/mb-memory-system-diagnostic`, and doctor's remediation advice to install autopilot is deliberately not followed. | MyBizz optimizes for governance — a person present at every run of an ungovernable, silently-failing mechanism; doctor optimizes for freshness. | `gbrain doctor` (0.59.18.0) |
| L3 | An `extract_atoms` backlog drains with `gbrain dream --phase extract_atoms --drain --source <id> --window <seconds>`; exit 3 means backlog remains. | The documented isolation flag alone does not drain; the drain mode is the purpose-built path. | `gbrain dream --help` (0.59.18.0) |
