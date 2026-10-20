---
title: "opencode-reference"
doc-id: "mb-2a5a7cdf"
updated: "2026-10-20"
---
# OpenCode Reference

What an agent needs while working with OpenCode. State lives in [[[mybizz-config-docs:opencode/opencode-config|OpenCode Configuration]]](C:/mybizz/mybizz-config-docs/opencode/opencode-config.md); orientation in [[[mybizz-config-docs:opencode/opencode-explainer|OpenCode Explainer]]](C:/mybizz/mybizz-config-docs/opencode/opencode-explainer.md); differences from the standard in [[[mybizz-config-docs:opencode/opencode-learnings|OpenCode Learnings]]](C:/mybizz/mybizz-config-docs/opencode/opencode-learnings.md).

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| Configuration schema | https://opencode.ai/config.json | 1.19.0 | 2026-10-20 |
| Configuration guide (precedence and merge) | https://opencode.ai/docs/config | 1.19.0 | 2026-10-20 |
| Source repository | https://github.com/anomalyco/opencode | 1.19.0 | 2026-10-20 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Installed version | `opencode --version` | agent |
| Global config content | read `~/.config/opencode/opencode.jsonc`, masking any secret value | agent |
| Merged config | `cd <project-root> && opencode debug config` — run from project roots only; it registers the folder as a project | agent |
| Resolved paths | `opencode debug paths` | agent |
| Plugin set | inspect from inside the running OpenCode process — this version writes no plugin-load log lines | agent |
| Cupcake enforcement | after any OpenCode or Cupcake restart, a fetch to a non-allowlisted domain must be denied | developer |
| Skill discoverable | `test -r ~/.config/opencode/skills/<skill-name>/SKILL.md && echo readable` | agent |
| Duplicate-skill warning | `grep -ia "duplicate skill name" ~/.local/share/opencode/log/*.log \| tail -5`; the `i-have-adhd` warning is expected | agent |
| Bash deny-list | a command whose text matches a deny pattern is refused before execution | agent |
| Web UI | reach the server started per the restart procedure; the project box lists real folders under `/home/dev-p` only | agent |
| Session prune | dated backup folders exist under `/mnt/c/backup-wsl/opencode-session-prune/` | agent |
| Cleanup backups | dated folders exist under `/mnt/c/backup-wsl/opencode-db-cleanup/` | agent |
| Session database files | `ls ~/.local/share/opencode/opencode.db*` — presence only | agent |
| WSL distributions | `wsl.exe -l -v` — expect exactly one, `Ubuntu` | agent |
| Works | the running session itself: OpenCode serving, GBrain MCP connected, Cupcake evaluating tool calls | agent |

## Procedures

### Restart OpenCode (required after any plugin or global config change)

1. `pkill -f "opencode web"`
2. `cd ~`
3. `opencode web --hostname 0.0.0.0`
4. Have the developer run the Cupcake enforcement check.

There is no reload mechanism — plugin and config changes are read only at process start.

### Start the web UI

1. `cd ~ && opencode web --hostname 0.0.0.0`
2. The server is protected by `OPENCODE_SERVER_PASSWORD`.

### Register a project

1. `cd <project-root> && opencode debug config` — project roots only; from any other folder it registers that folder as a project.
2. Give the project its bind mount: a new `/etc/fstab` line with `bind,nofail`, exposing it at `~/projects/<name>`.
3. For an app repo, write an `opencode.json` following the app-repo baseline in the [[[mybizz-config-docs:opencode/opencode-config|config]]](C:/mybizz/mybizz-config-docs/opencode/opencode-config.md)'s Projects table.

### Clean the session database (run after renaming or moving any project folder)

1. `bash /mnt/c/mybizz/scripts/opencode-db-cleanup.sh`
2. Confirm with a typed capital `YES` — it accepts nothing else.
3. Run it on demand only; never schedule it.

### Create a Windows-visible symlink

1. From the Windows side, with Developer Mode enabled: `cmd.exe /c mklink /D C:\path\to\link C:\path\to\real\target`
2. Verify from both sides — Windows: `cmd.exe /c dir C:\path\to\` shows `<SYMLINKD>`; WSL: `readlink -v /mnt/c/path/to/link` plus `ls -la /mnt/c/path/to/`.
3. Trust the link only when both sides agree.

### Check Developer Mode

`reg.exe query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock" /v AllowDevelopmentWithoutDevLicense` — a missing key or a value of `0` means it is off.

### Run a Windows-triggered command against WSL

`wsl.exe -d Ubuntu -u dev-p -- <command>` — always pass both flags.

## Do not

- Do not edit a plugin or the global config and expect an effect without a full restart — nothing hot-reloads.
- Do not create a second discoverable path for any plugin — even a symlink to the identical file double-loads it.
- Do not put a file path in the `plugin` config list — the list accepts folders; the plugin folder loads `.js` files automatically.
- Do not build plugin verification on log lines — this version writes none.
- Do not create a WSL-side symlink pointing at a Windows-drive target — Windows Explorer cannot read it.
- Do not trust a single-sided symlink check — verify from Windows and WSL.
- Do not omit `-d Ubuntu -u dev-p` from a Windows-triggered `wsl.exe` command.
- Do not run `opencode debug config` from a folder that must not become a project.
- Do not treat the `i-have-adhd` duplicate-skill warning as a fault — both entries resolve to one file.
- Do not assume a project config can silently weaken the global deny-list — nested maps merge deeply; an explicit re-declaration of a deny pattern as `allow` is a security-review finding.
- Do not work around a deny pattern by disguising intent — rephrase only when the text match is incidental; if the match is on the action's real substance, stop.
- Do not schedule `opencode-db-cleanup.sh` — folder-existence checks can false-positive on a temporarily unmounted drive.
- Do not rely on the agent's own refusal as proof of enforcement — the proof is the enforcement layer's own evaluation.
