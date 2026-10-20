---
title: "opencode-explainer"
doc-id: "mb-4e022a9c"
updated: "2026-10-20"
---
# OpenCode Explainer

State: [[[mybizz-config-docs:opencode/opencode-config|OpenCode Configuration]]](C:/mybizz/mybizz-config-docs/opencode/opencode-config.md). Execution: [[[mybizz-config-docs:opencode/opencode-reference|OpenCode Reference]]](C:/mybizz/mybizz-config-docs/opencode/opencode-reference.md). Differences from the standard: [[[mybizz-config-docs:opencode/opencode-learnings|OpenCode Learnings]]](C:/mybizz/mybizz-config-docs/opencode/opencode-learnings.md).

## 1. What it is

OpenCode is the agent harness the MyBizz environment runs inside — the program that reads the global rules file, discovers skills, loads plugins, evaluates permissions on every tool call, and connects its agents to MCP servers. Every other system in the estate — Cupcake, GBrain, the memory governor's tooling, the PDLF application — is either a plugin running inside OpenCode or a tool its agents call. OpenCode spans every layer of the environment: the supporting systems run inside or beside it, PDLF is built in it, and the PDLF layer builds the shipped estate through it. Nothing inside it travels to the shipped estate — it is the harness for every layer except the one it produces.

## 2. What it can do

- Run interactive agent sessions with a chosen default agent and per-agent permission overrides, so a planning agent can be held to read-and-reason while a build agent writes.
- Discover skills from several configured roots and make them available to every session.
- Load plugins from its plugin folder at process start and let them evaluate every tool call.
- Connect local and remote MCP servers; GBrain is served to it this way.
- Enforce a permission layer: per-pattern rules for file edits, shell commands, web fetches, task delegation and external directories.
- Merge a per-project config with the global config, so projects specialize without replacing the baseline.
- Serve a browser-based web UI on the network, protected by a password, listing the projects mounted in the home folder.
- Persist projects and sessions in a local database on the machine.

## 3. Suitability

**Best for:** being the single harness for the whole estate. Every layer MyBizz runs already assumes it, and its own permission layer plus the Cupcake plugin give two independent enforcement planes over the same tool calls.

**Good for:** project-specific permission tuning without touching the global baseline; local MCP integration such as GBrain; skills shared across every project; browser-based work through the web UI.

**Not good for:** per-skill permission rules — no skill identity reaches any plugin, so that need routes through the cupcake suite's rules instead. Frequent plugin or config iteration without restarts — nothing hot-reloads. Policing its own database housekeeping — MyBizz's maintenance scripts exist because the issuer ships none. Running any plugin or skill from a second discoverable path — deduplication is by path, not file identity, so a second path means a second running copy. Skill inventory as a reference — that is the skills catalog's job ([[[mybizz-os-docs:os-reference-docs/skills-catalog|Skills Catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md)); project lists and status belong to repo-organization ([[[mybizz-os-docs:os-reference-docs/repo-organization|Repo Organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md)).

## 4. Why it works this way

**Configs merge, not replace.** A project config overrides the global config only for conflicting keys, and nested permission maps merge deeply. This is why each app repo can carry a full baseline and still inherit anything the global config adds: a project can add or override, but it cannot silently weaken a global deny-list. An explicit re-declaration of a deny pattern as `allow` remains possible — it is a visible act in a config file, and MyBizz treats it as a security-review finding.

**Plugins load once, at process start.** State kept by a plugin — a counter, a cache — stays coherent because exactly one instance runs. Deduplication is by discovery path, not by file identity, so exactly-one-path-per-plugin is a hard hygiene rule: a second path, even a symlink to the same file, means a genuinely second running instance.

**Deny patterns match command text.** A harmless command that merely mentions a denied string is refused like the real thing. That makes the deny-list strong — there are no parsing tricks to slip through — and it shapes how commands are written: incidental matches are rephrased, real matches are respected.

**Two enforcement layers sit above every tool call.** OpenCode's own permission system is the interaction gate: it asks the developer or blocks by pattern. Cupcake is the policy layer: it enforces the written rules mechanically. Both evaluate the same call; neither substitutes for the other. The agent's own refusal, under its own written rules, is not proof of enforcement — the enforcement layer's evaluation is. The current enforcement posture is standing policy, recorded in the cupcake suite's [[[mybizz-config-docs:cupcake/cupcake-config|Operational status]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md).

**Skill discovery scans more than one root.** A skill can therefore be found twice and logged as a duplicate; when every entry resolves to the same file the warning is a routing fact, not an error. One of the roots is reachable under two names, through a link — one folder, not two copies.

**Windows and WSL disagree about what a link is.** A link created from inside WSL toward a Windows-drive target produces a link type Windows Explorer cannot read at all; the reverse direction fails from the WSL side. Only a link created from the Windows side, toward a target on the Windows drive, works from both sides — and creating it unprivileged requires Windows Developer Mode. Hence the standing practice: Windows-side links, verified from both sides.

**The web UI trusts real folders and ignores links.** Every project therefore reaches it as a real mounted folder, which is why each project carries its own bind mount into the home folder's projects directory. The UI also reopens the last active project regardless of start folder, and its "recent projects" list is the browser's memory, not OpenCode's — so a stale entry there is browser state, not database corruption.

**The session database has no built-in housekeeping.** Stale project rows survive folder renames, and stored session data grows without limit — both are upstream gaps, not misconfigurations. MyBizz compensates with two scripts of different characters: a manual cleanup, gated behind an explicit typed confirmation because folder-existence checks can false-positive on an unmounted drive, and a scheduled prune, safe unattended because its criterion is purely a timestamp.

**The harness holds the current major version line.** The successor line does not run the Cupcake plugin, and the policy layer is load-bearing — a harness that drops its enforcement layer is not adoptable. Upgrades therefore wait on policy-layer compatibility.

**One WSL distribution exists**, and the working environment is its default — explicit distro and user flags on Windows-triggered commands remain as identity-proofing, so a command can never silently act as a different user or machine context.

## 5. What has to happen

- The developer restarts OpenCode after any plugin or global-config change, and runs the Cupcake enforcement probe afterwards.
- Every plugin keeps exactly one discoverable path; the plugin folder holds `.js` files only; no file path enters the `plugin` config list.
- Every new project gets its bind mount — a new line in the fstab table — and an app repo additionally gets its `opencode.json` baseline.
- After any project folder is renamed or moved, the developer runs the session-database cleanup script and confirms it with the typed confirmation word.
- The scheduled session prune keeps running; its dated backups are the evidence that it works.
- OpenCode stays on its current major version line until the Cupcake plugin runs on the successor.
- [[[mb-sysdoc-creator:mb-sysdoc-creator|mb-sysdoc-creator]]](C:/mybizz/mb-sysdoc-creator/mb-sysdoc-creator.md) refreshes this suite; the skills catalog and repo-organization documents stay current so this suite can point at them instead of restating them.
- The gbrain and cupcake suites keep owning their own facts; this suite points at them rather than duplicating them.
