---
title: "doc-suite-specification"
doc-id: "mb-f4adba8c"
updated: "2026-10-01"
---
# Doc Suite Specification — config / reference / explainer

Canonical specification for the three-document pattern used across this
system's component documentation (memory-governor, mb-submit-memory,
postgresql, anvil-agent-references, and future components). Defines what
each of the three documents is for, what it must and must not contain,
and a test for catching content that's drifted into the wrong document.
Reference this before starting any new three-doc set.

---

## The single fastest check across all three

**Each fact should exist in exactly one of the three documents.** If a
fact appears twice — once as a config table row, once as an explainer
sentence — one of those two is in the wrong document. Neither correctly
"reinforces" the other; it's duplication, and duplication is where
these documents drift out of sync with each other over time.

---

## `<name>-config.md` — State

**Purpose:** a settings sheet. Answers "what exists and what is it set
to" — nothing else.

**Contains:**
- Identity/version/location facts (paths, versions, ports, IDs)
- Structural inventory (file/folder layout, component lists, table lists)
- Integration facts with other system parts (how it's registered, synced, exempted)
- An explicit "open items" section for anything not yet verified — stated as a gap, never guessed at

**Never contains:**
- A rule ("never do X") — that's reference.md's job
- A reason ("this exists because...") — that's explainer.md's job
- Prose narrative of any kind — every line should be inventory-shaped: a value, a state, a fact

**Format:** tables and short bullet inventories throughout. If a line
requires more than one sentence to express, it's not a config fact — it
belongs in one of the other two docs.

**Test for a stray line:** *Could this line go stale the moment someone
changes a setting, without any reasoning changing?* If yes, config.md.
If the line would only go stale when the reasoning changes, it doesn't
belong here.

---

## `<name>-reference.md` — Execution

**Purpose:** what an agent (or a person) consults *while doing the
work*, right now, mid-task. Every line should be immediately actionable.

**Contains:**
- Exact commands, exact syntax, exact invocation patterns
- Exact rules stated as imperatives ("never...", "always...", "use X when Y")
- Procedures as ordered steps
- Full technical detail an agent needs to act correctly — no compression, no "see elsewhere" for anything actually needed mid-task
- A "Do not" list at the end, consolidating the sharpest failure modes

**Never contains:**
- Why a rule exists — name the constraint, don't justify it (a one-line pointer to explainer.md is fine; a paragraph of justification is not)
- System-wide architecture framing ("this sits between X and Y because...") — that's explainer.md's job
- Historical/incident narrative beyond what's needed to justify a "do not" (a one-line "confirmed live, YYYY-MM-DD" is fine; a story is not)

**Format:** imperative voice, tables for anything tabular (parameters,
options, mappings), numbered steps for procedures. Density over
readability — this doc is grepped, not read start to finish.

**Test for a stray line:** *If I deleted this line, would an agent
mid-task now do the wrong thing, or just understand less about why?* If
the former, it belongs here. If the latter, it belongs in explainer.md.

---

## `<name>-explainer.md` — Orientation, Suitability, and Reasoning

**Purpose:** the mental model a human builds *once*, so future decisions
about this component are made with real understanding instead of
pattern-matching against a rule list. Required contents, in this order:

**1. What this actually is — plain-terms identity.** One or two
paragraphs, no assumed jargon: what problem does this exist to solve,
for whom, in what situation. A reader with zero context should finish
this section knowing what the thing *is*, before anything about why
it's built a particular way.

**2. Feature summary — conceptual, not syntactic.** What the component
can actually do, at the level of capability, not command. Not "run `X
--flag`" (that's reference.md) — "it validates a manifest before
changes take effect," "it enforces a specific access default unless
overridden." A reader should be able to list its real capabilities
without having memorized a single command.

**3. Suitability — best for / good for / not good for.** Explicit, not
implied. Three honest categories:
   - **Best for:** the cases this was clearly designed around — where using it is obviously the right call.
   - **Good for / adequate for:** cases it handles acceptably but isn't its central purpose.
   - **Not good for / wrong tool for:** cases where reaching for this component would be a mistake — name the actual right tool if one exists in this system.

   This section is what lets a future reader *choose* whether to use
   the thing at all — a distinct question from "how do I use this
   correctly" (reference.md) and even from "why is it built this way"
   (the rest of this document).

**4. Design reasoning.** Why the component is structured the way it is
(why split into these parts, not others); the reasoning behind the
sharpest or most counter-intuitive rules — not the rule itself, the
reason it exists and what it protects against; where the component sits
relative to other real parts of the system (what depends on it, what it
depends on, what treats it specially and why); genuinely open
architectural/integration questions, framed as "why this matters," not
just restated as a to-do.

**Never contains:**
- The exact command or exact rule syntax — name it, reference the reference doc, move on
- A config fact restated in sentence form — if a config.md table row says it, don't also say it here in prose unless the *reasoning* genuinely needs the fact restated for context
- Filler transitions, hedging, or "it's worth noting" — every sentence should carry a reason, a comparison, or a consequence, or it shouldn't be there

**Format:** prose organized under reasoning-shaped headers ("why X
instead of Y," "where this sits relative to Z"), tables only when a
genuine reasoning comparison is tabular (e.g. risk category vs.
consequence) — never a table that exists only to reformat facts already
covered in config.md or rules already covered in reference.md.

**Test for a stray line:** *Does this sentence explain a "why," a
trade-off, or a relationship — or does it just restate a "what" or a
"how"?* If it's a "what" or a "how" and it isn't part of the required
orientation/suitability sections above, cut it or move it to the doc
that owns it.

**Revised test for the doc as a whole:** a reader should be able to
answer, from explainer.md alone, three questions in order — *what is
this, should I use it for my situation, and why does it work the way it
does* — before ever needing reference.md for the how.
