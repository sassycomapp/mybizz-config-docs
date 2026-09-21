---
doc-id: 2026-09-13-001-network-grants-and-session-memory
document: "Session 001 — 13 September 2026 — Network Grants and the Session Close-Out Design"
state: Live
date-created: 2026-09-13
type: session-log
title: >-
  Session 001 — 13 September 2026 — Network Grants and the Session Close-Out
  Design
date: '2026-09-13T00:00:00.000Z'
session-number: 1
ingested_via: 'mcp:put_page'
ingested_at: '2026-09-13T15:18:20.674Z'
source_kind: 'mcp:put_page'
---

# Session 001 — Network Grants and the Session Close-Out Design

This page is the full summary of the session closed out on 13 September 2026.
It was written so that a future session can understand what happened here
without reading the original conversation.

## What was built today

The first piece of work was a new network permission system for Cupcake.
Until today, outbound web access from the AI was controlled by a fixed
allowlist of domains (GitHub, PyPI, npm, Anvil, and the machine's own local
addresses). Any other website was simply blocked. Today that rule was
upgraded: the developer can now grant access to any specific website with a
command, in the same style as the existing folder grants. The command to
grant is `net-grant --domain <name> --count N`, and the command to take it
away again is `net-revoke --domain <name>`. Both scripts live in
`~/.config/cupcake/bin/`, and they were tested and verified working.

While building this, a real technical discovery was made: a time check
written inside a Cupcake policy (comparing the current time to a grant's
expiry) silently fails inside the compiled Cupcake engine, which makes any
rule that depends on it fail closed. The working pattern is to check only
that a grant exists and its count is above zero. This lesson is saved as
fact number 46 in GBrain.

The second piece of work was the design of the session close-out routine.
The problem it solves: long sessions slow down because the entire
conversation is re-sent with every prompt, and starting a fresh session
loses everything. The agreed solution is to keep sessions short and store
memory outside them, in GBrain.

## The session close-out routine

At the end of a session, the developer says "close out". The AI then writes
a short list of important facts worth believing later, checks them against
existing memory for contradictions, shows the list once for a single
approval, sends the important facts through the Memory Governor, and saves
the full session summary as a page like this one. It then adds one row to
the sessions log at [[2026-09-15-session-numbers-from-sessions-log|session numbers come from the sessions log]],
recording the number, date, topic, subject, title, and exact page name. A
second log at the same folder, `Facts-log.md`, indexes every durable fact
saved, with its GBrain fact number. At the start of a new session, the AI
reads these logs and loads the relevant summary pages, which restores
memory cheaply without dragging the old conversation along.

## The GBrain page naming convention

The AI chooses each page name at write time. The convention is
`sessions/YYYY-MM-DD-NNN-<short-hint>`, where the short hint comes from the
session's topic and subject in hyphenated words. The full human title lives
in the sessions log only. The page name needs only to be unique and stable;
the sessions log is the authoritative mapping of number to name.

## The communication rules

The developer instructed, and the AI saved as permanent memory (facts 47
and 48, attached to the entity dev-p): always explain in full, complete,
flowing sentences with no shorthand and no missing middle pieces, because
the developer has amnesia, ADHD, and reading-processing difficulties and
cannot join dotted-together snippets. The developer personally designed
every system on this machine; explainer documents exist everywhere for that
reason and should be read before assuming how anything works.

## Open items left at close-out

First, the close-out routine itself is not yet written into the global
AGENTS.md rules file, so future sessions do not automatically know it; that
short addition awaits the developer's approval. Second, the earlier
net-grant fact (number 46) was saved through the quick path before the
rules were learned; the developer may resubmit it through the Memory
Governor or leave it as advisory. Third, the mg-grant script silently
accepted a mangled path with no slashes; hardening it to reject such paths
is a small future improvement. Fourth, grants do not auto-expire because of
the engine time-check limitation; control is by revoke or re-grant, and an
optional later improvement could extend the plugin's existing prune step.
Fifth, an initial path-mangling incident during granting was caused by the
AI supplying the command in Windows path style; grant commands must always
be given in WSL path style.
