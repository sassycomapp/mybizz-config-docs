---
title: "i-have-adhd-intro"
doc-id: "i-have-adhd-intro"
---
This skill is very likely to **improve** your day‑to‑day work with GLM‑5.3 Flash in OpenCode, especially if you often feel the model “buries the answer” in long, chatty explanations.[[github](https://github.com/ayghri/i-have-adhd)] https://github.com/ayghri/i-have-adhd

## What the skill changes

The `i-have-adhd` skill enforces a compact, action‑first style for your coding agent:

- **Lead with the next action** instead of long preambles.
- **Number multi‑step tasks** and give concrete commands (e.g., “Run `npm test -- auth.spec.ts`”).
- **End with one concrete next step**, not open‑ended “let me know if you want to dig deeper”.
- **Cap lists at 5 items**, suppress tangents, and avoid “Hope this helps!” closers.[[github](https://github.com/ayghri/i-have-adhd)]

In practice, your GLM‑5.3 Flash responses in OpenCode should look more like:

> Run `npm install jsonwebtoken@latest`, then edit `src/auth.ts:42`.
> 
> 1. Open `src/auth.ts`
> 2. Replace `verifyToken` (lines 42–58) with the snippet below
> 3. Run `npm test -- auth.spec.ts`  
>    Next: paste the first failing line if any test fails.[[github](https://github.com/ayghri/i-have-adhd)]

instead of long, exploratory paragraphs.

## How that affects your development workflow

Likely benefits for you as an independent developer using AI‑assisted coding:

- **Faster time‑to‑action**: You see the exact command or file edit first, so you can execute immediately without scrolling.[[github](https://github.com/ayghri/i-have-adhd)]
- **Clearer task breakdowns**: Numbered steps map well to your “spec → implementation → test” style of work.[[github](https://github.com/ayghri/i-have-adhd)]
- **Lower cognitive load**: Fewer tangents and capped lists reduce the mental overhead of parsing long answers, which helps when you’re juggling multiple projects.[[github](https://github.com/ayghri/i-have-adhd)]
- **Better multi‑turn flow**: Each turn restates state and ends with one next step, which keeps long OpenCode sessions more focused and less likely to drift.[[github](https://github.com/ayghri/i-have-adhd)]

Potential trade‑offs:

- You may lose some **exploratory reasoning** or alternative options the model would normally surface. For complex architectural decisions, you might occasionally want the “longer thinking” mode and then switch back.
- If you sometimes rely on the model’s narrative to understand *why* a change is needed, you’ll need to explicitly ask for explanations (e.g., “briefly explain why this fix works”).

## Does it work with GLM‑5.3 Flash + OpenCode?

Yes. The repo explicitly supports **OpenCode** (there’s an `opencode.json` and OpenCode plugin config), and it’s designed to work with any underlying LLM, including models like GLM‑5.3 Flash. The skill shapes the **output style**, not the model’s core capabilities.[[github](https://github.com/ayghri/i-have-adhd)]

Given your setup (Windows 11, OpenCode, GLM‑5.3 Flash, cost‑conscious, spec‑driven development), this skill aligns well with your workflow: it makes the agent’s output more executable and less noisy, which usually translates into **faster iteration and lower token waste** on fluff.[[github](https://github.com/ayghri/i-have-adhd)]

---

Below is a concrete, OpenCode‑specific setup for the **i‑have‑adhd** skill with GLM‑5.3 Flash, including:

- How to install it
- How to keep it **always‑on**
- How to **temporarily disable** it for deep‑design discussions
- A couple of tuning tips so it doesn’t fight your own workflows.[[toolsdepth](https://toolsdepth.com/reviews/i-have-adhd-review-2026)][[opentrend](https://opentrend.org/project/i-have-adhd)][[sourcefeed](https://sourcefeed.dev/a/why-28000-developers-told-their-agent-they-have-adhd)][[ailect](https://ailect.com/i-have-adhd-review-the-tiny-skill-that-stopped-claude-from-burying-the-answer/)][[reveneau](https://reveneau.com/ainews/i-have-adhd-coding-agent-skill-29k-stars-lead-with-answer)][[blog.damavis](https://blog.damavis.com/en/opencode-step-by-step-installation-and-configuration/)]

---

## 1) Install the skill in OpenCode

The repo supports OpenCode via a plugin manifest and a slash command. You have two main options:

### Option A — Use the repo’s install command (recommended)

From your project root (or globally if you prefer), run one of these in your terminal:

```
# Project‑local install (affects only this repo)
npx skills add ayghri/i-have-adhd -a opencode -y

# Or global install (all OpenCode projects)
npx skills add ayghri/i-have-adhd -a opencode -y -g
```

This will:

- Pull the skill files into `.opencode/skills/i-have-adhd/` (or your global skills dir)
- Wire up the slash command `/i-have-adhd` inside OpenCode sessions.[[toolsdepth](https://toolsdepth.com/reviews/i-have-adhd-review-2026)][[opentrend](https://opentrend.org/project/i-have-adhd)][[blog.damavis](https://blog.damavis.com/en/opencode-step-by-step-installation-and-configuration/)][[agentmods](https://agentmods.dev/skills/ayghri/i-have-adhd/i-have-adhd)]

If `npx skills` isn’t available in your environment, the fallback is to clone/copy the skill files manually (see Option B).

### Option B — Manual copy (no extra CLI)

1. Create the skills directory if it doesn’t exist:

```
mkdir -p .opencode/skills/i-have-adhd
```

2. Copy the main skill definition into that folder:
- Source: `SKILL.md` (or equivalent) from  
  `https://github.com/ayghri/i-have-adhd` → `skills/i-have-adhd.md` (or `SKILL.md` depending on branch layout).[[toolsdepth](https://toolsdepth.com/reviews/i-have-adhd-review-2026)][[blog.damavis](https://blog.damavis.com/en/opencode-step-by-step-installation-and-configuration/)]

For example (PowerShell on Windows):

```
# From your project root
$skillUrl = "https://raw.githubusercontent.com/ayghri/i-have-adhd/refs/heads/main/skills/i-have-adhd.md"
New-Item -ItemType Directory -Force -Path ".opencode\skills\i-have-adhd" | Out-Null
Invoke-WebRequest -Uri $skillUrl -OutFile ".opencode\skills\i-have-adhd\SKILL.md"
```

OpenCode will treat anything under `.opencode/skills/<name>/SKILL.md` as a skill.[[blog.damavis](https://blog.damavis.com/en/opencode-step-by-step-installation-and-configuration/)]

---

## 2) Activate it in an OpenCode session

Once installed:

- Start an OpenCode session as usual (with GLM‑5.3 Flash as your model).
- In the chat, type:

```
/i-have-adhd
```

From that point on in the session, the agent’s outputs should follow the “action‑first, numbered steps, no fluff” rules.[[toolsdepth](https://toolsdepth.com/reviews/i-have-adhd-review-2026)][[opentrend](https://opentrend.org/project/i-have-adhd)][[ailect](https://ailect.com/i-have-adhd-review-the-tiny-skill-that-stopped-claude-from-burying-the-answer/)]

You should see responses that:

- Start with the next action on line 1
- Use numbered steps (max 5 per list)
- Avoid long preambles and “Hope this helps!” closers.[[toolsdepth](https://toolsdepth.com/reviews/i-have-adhd-review-2026)][[ailect](https://ailect.com/i-have-adhd-review-the-tiny-skill-that-stopped-claude-from-burying-the-answer/)]

---

## 3) Make it always‑on (so you don’t type `/i-have-adhd` every time)

The skill supports an **always‑on** mode via a marker file / hook. For OpenCode specifically, the pattern used by similar agents is:

- Create an empty file named `.i-have-adhd-always` in your OpenCode config directory.[[opentrend](https://opentrend.org/project/i-have-adhd)][[ailect](https://ailect.com/i-have-adhd-review-the-tiny-skill-that-stopped-claude-from-burying-the-answer/)][[genztech](https://genztech.blog/p/i-have-adhd-claude-code-setup/)][[note](https://note.com/generativeai_new/n/n97de07351bec?hl=en)]

On Windows (PowerShell), assuming OpenCode uses a `~/.opencode` config dir:

```
New-Item -Path "$HOME\.opencode\.i-have-adhd-always" -ItemType File -Force
```

If your OpenCode setup uses a different config path (e.g. `%APPDATA%\opencode`), put the file there instead. The idea is:

- If `.i-have-adhd-always` exists, the skill’s rules are injected at **session start**, so every new chat begins in ADHD‑mode without a slash command.[[ailect](https://ailect.com/i-have-adhd-review-the-tiny-skill-that-stopped-claude-from-burying-the-answer/)][[genztech](https://genztech.blog/p/i-have-adhd-claude-code-setup/)][[note](https://note.com/generativeai_new/n/n97de07351bec?hl=en)]

To confirm it’s working:

- Start a fresh OpenCode session.
- Ask a simple coding question.
- Check that the first line is an action or direct answer, not a preamble.

If you ever want to revert to on‑demand mode, just delete or rename that file:

```
Remove-Item "$HOME\.opencode\.i-have-adhd-always"
```

---

## 4) Temporarily disable it for deep‑design discussions

You don’t need to uninstall anything. The skill is designed to be toggled per session or per conversation:

### 4.1) Per‑session: start a session without the skill

If you’re using **always‑on** (`.i-have-adhd-always` present):

- For a specific deep‑design session, either:
  
  - Temporarily rename/remove the `.i-have-adhd-always` file before starting OpenCode, then restore it afterward, or
  - Start a separate OpenCode instance with a different config/profile that doesn’t include the always‑on file (e.g. a “design” profile).

If you’re using **on‑demand** (no always‑on file):

- Just start a new session and **don’t** run `/i-have-adhd`. That session will use the model’s default style.

### 4.2) Mid‑session: turn it off with a spoken command

The skill documents a simple off‑switch phrase you can type in the chat:

```
stop adhd mode
```

or

```
normal mode
```

After that, subsequent turns in the same session should revert to the model’s normal, more explanatory style until you re‑enable it with `/i-have-adhd`.[[toolsdepth](https://toolsdepth.com/reviews/i-have-adhd-review-2026)][[opentrend](https://opentrend.org/project/i-have-adhd)]

Practical pattern:

- Day‑to‑day coding sessions: always‑on or `/i-have-adhd` at the start.
- Architecture/design sessions: start clean (no skill) or say `normal mode` once you’re in.

---

## 5) Tuning it for your GLM‑5.3 Flash + OpenCode workflow

A few light adjustments so the skill complements rather than fights your style:

### 5.1) Keep “why” available on request

The skill suppresses long explanations by default. For design discussions, you can add a standing instruction like:

```
When I say “explain why”, give a concise rationale (max 5 bullets), then return to action-first style.
```

You can either:

- Put that in your project’s `.opencode/instructions.md` (or equivalent), or
- Say it once at the start of a design session so the model knows you still want occasional reasoning.[[toolsdepth](https://toolsdepth.com/reviews/i-have-adhd-review-2026)][[blog.damavis](https://blog.damavis.com/en/opencode-step-by-step-installation-and-configuration/)]

### 5.2) Cap context bloat

Because the skill restates progress each turn, long sessions can grow verbose. To avoid wasting tokens with GLM‑5.3 Flash:

- Periodically summarize the session yourself (“Current state: … Next: …”) and ask the model to “continue from here” so earlier recap text can be dropped by context compaction.
- If you notice repeated long recaps, add a rule like “recap in ≤2 lines” to your local instructions.[[toolsdepth](https://toolsdepth.com/reviews/i-have-adhd-review-2026)][[sourcefeed](https://sourcefeed.dev/a/why-28000-developers-told-their-agent-they-have-adhd)]

### 5.3) Use different modes for different work

You can think in terms of three modes:

1. **Implementation mode** (default): always‑on i‑have‑adhd → fast, action‑first.
2. **Design mode**: `normal mode` or sessions without the skill → more exploration, trade‑off discussion.
3. **Debug mode**: i‑have‑adhd on, but you explicitly ask for “brief why” when needed.

You don’t need extra config for this; it’s just a discipline about when you run `/i-have-adhd` or keep the always‑on file active.

---

## 6) Quick checklist

- Install: `npx skills add ayghri/i-have-adhd -a opencode -y` (or manual copy into `.opencode/skills/i-have-adhd/`).[[opentrend](https://opentrend.org/project/i-have-adhd)][[blog.damavis](https://blog.damavis.com/en/opencode-step-by-step-installation-and-configuration/)]

- Test: in an OpenCode session, run `/i-have-adhd` and ask a coding question.

- Always‑on (optional): create `$HOME\.opencode\.i-have-adhd-always`.[[ailect](https://ailect.com/i-have-adhd-review-the-tiny-skill-that-stopped-claude-from-burying-the-answer/)][[genztech](https://genztech.blog/p/i-have-adhd-claude-code-setup/)]

- Disable temporarily:
  
  - Per session: don’t run `/i-have-adhd` or remove/rename the always‑on file.
  - Mid session: type `stop adhd mode` or `normal mode`.[[toolsdepth](https://toolsdepth.com/reviews/i-have-adhd-review-2026)][[opentrend](https://opentrend.org/project/i-have-adhd)]

- Tune: add local instructions for “explain why” and recap length as needed.

If you tell me your exact OpenCode config path on Windows (e.g. `%APPDATA%\opencode` vs `~/.opencode`), I can give you precise commands tailored to your setup.
