# OpenCode Configuration

Canonical current-state configuration record. Agent-facing. Consolidates
and supersedes `opencode-reference.md`, `opencode-permission-access-
control-model.md`, and `opencode-project-session-data-integrity.md` —
those three documents overlapped significantly and are retired in favor
of this single record. See `opencode-explainer.md` for mechanics and
real incidents.

---

## Identity

| Item | Value |
|---|---|
| Global config | `~/.config/opencode/opencode.jsonc` — the only global config file (consolidated from two, 2026-09-01) |
| Config precedence | Per-project `opencode.json` overrides global `opencode.jsonc` for that project only. Stricter rule wins on conflict. |
| Plugin discovery | `~/.config/opencode/plugin/` — must contain exactly one copy of any given plugin; a second discoverable path (even a symlink to the same file) causes double-loading |
| WSL distro (real, active) | Non-default distro — any Windows-triggered command invoking `wsl.exe` must explicitly pass `-d <distro> -u dev-p` |

## Global config — real, current content (post-consolidation)

| Key | Value |
|---|---|
| `default_agent` | `plan` |
| `instructions` | `C:/dev/project-library-global/register-global/register-global.md` (corrected 2026-09-01 — previously pointed at four deleted `INDEX.md` files) |
| `permission.task` | `deny` — Layer 1 of the three-layer `task`-denial system, see `cupcake-config.md` |
| `permission.edit` | `ask` by default; `**/anvil.yaml` explicitly `deny` |
| `permission.webfetch` | `ask` |
| `permission.bash` | `ask` by default; explicit `deny` on destructive git operations, `DROP`/`TRUNCATE` SQL patterns, and `curl`/`wget` piped directly to a shell |
| `permission.external_directory` | `allow` for `C:\mybizz\**`, `C:\dev\**`, `C:\pdlf\**` |
| `agent.plan.permission.edit` | `deny` — Plan agent cannot write, by design |
| `mcp.gbrain` | Local MCP server, `gbrain serve`, real API keys passed via environment |

## Active Project Standard

| Status | Meaning | Config expectation |
|---|---|---|
| **Active** | Currently being built | Full, real `opencode.json` |
| **Paused** | Real, deliberate prior work exists; correctly waiting on a known, real prerequisite before resuming | Real config retained — represents genuine prior work, not mistaken for the current active standard |
| **Never started** | No real work has begun | Zero configuration — any config found here is presumed stale by default |

**Current real project status:**

| Project | Status | Notes |
|---|---|---|
| `makepdlf-project-library` | Active | |
| `mb-3-cs` / `mb-3-cs-project-library` | **Paused** | Real, deliberate — genuine prior setup exists (including a project-local Graphify MCP plugin), correctly waiting on PDLF's own completion before resuming |
| `mb4ecom`, `mb5pdlf` | Never started | Zero configuration expected |
| `project-template` | Template scaffold | Contains literal, unsubstituted `{SLUG}` placeholders by design — not a real project |

## Skill discovery — real, confirmed methods (not uniform)

| Skill-set | Real install method |
|---|---|
| Custom skills (`mb-*`) | Plain, real folders — no symlink |
| Anvil, Archify, most GStack skills | Symlink to a real folder elsewhere on the same drive |
| GStack (top-level) | Hybrid — real folder containing further symlinks to individual skills |
| Magdoub wireframe skill | Two-hop — empty intermediate folder pointing to real content in `~/.claude/skills/` |

Full, current skill inventory by owner: `skill-index.md`. Full GStack-specific detail: `gstack-config.md`.

## Known scope limitations

- **No native session-start hook.** The session-start checklist is human-run, pasted manually — not a technical OpenCode mechanism.
- **No skill-identity field reaches any plugin.** Per-skill permission rules are not currently possible — confirmed against OpenCode's own real source, not assumed.
- **Plugin deduplication is by discovery path, not file identity.** A plugin must be discoverable from exactly one path.

## Do not

- Do not edit a plugin's code and expect it to take effect without a
  full OpenCode restart — changes are only read at process start.
- Do not create a second discoverable path for any plugin already
  installed — even a symlink to the identical file causes double-loading.
- Do not create a WSL-side symlink pointing at a Windows-drive target —
  confirmed unreadable by Windows Explorer. Create it from the Windows
  side instead (`mklink /D`), with Developer Mode enabled.
- Do not invoke `wsl.exe` from a Windows-triggered command without
  explicitly specifying `-d <distro> -u dev-p` — this machine has two
  WSL distributions installed.
- Do not treat a "Paused" project's existing configuration as stale —
  only "Never started" projects default to zero configuration.
