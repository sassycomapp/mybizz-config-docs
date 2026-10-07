---
title: "postgres-sql-anomaly"
doc-id: "mb-bf64ffb0"
updated: "2026-10-07"
---
# Postgres SQL Anomaly

## What this is

This document records four problems found on 2026-10-05 while measuring disk space on David's machine. They concern how the PostgreSQL documentation suite (`C:\mybizz\mybizz-config-docs\postgresql\`) describes the WSL installations that PostgreSQL runs in, and how WSL is shut down. None of them has been fixed. They are recorded here so a later session can resolve them without repeating the investigation.

Nothing in PostgreSQL itself was found to be faulty. Both instances were not touched and are not suspected of any fault. The problems are in the documentation and in the WSL setup around Instance B.

## Verified facts this document relies on

These were read live on 2026-10-05.

WSL lists two installations. The `*` marks the default, which is the installation a bare `wsl` command opens.

```
  NAME            STATE           VERSION
* Ubuntu-22.04    Stopped         2
  Ubuntu          Running         2
```

| | `Ubuntu` | `Ubuntu-22.04` |
|---|---|---|
| Ubuntu version | 24.04.4 LTS | 22.04.5 LTS |
| Linux user | `dev-p` | `myubuntu` |
| Default installation | No | Yes |
| Holds Instance B (PostgreSQL 16) | Yes | No |
| Holds GBrain, memory governor, `backup-gbrain` | Yes (`/home/dev-p/`) | No |
| Last activity in home folder | 2026-10-05 | late May 2026 |
| Space used inside Linux | 9.9 GB | 6.0 GB |
| Virtual disk file | `C:\Users\dev-p\AppData\Local\wsl\{784dab11-afc2-43d3-9a2d-611e29911b7d}\ext4.vhdx` (18.3 GB) | `C:\Users\dev-p\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu22.04LTS_79rhkp1fndgsc\LocalState\ext4.vhdx` (17.3 GB) |
| How it was installed | WSL's newer method (not a Store app) | Microsoft Store app `CanonicalGroupLimited.Ubuntu22.04LTS` |

## Anomaly 1 — The documents use a name WSL does not recognise

**What was found.** The configuration and reference documents describe Instance B's home as "WSL (Ubuntu 24.04)", and the configuration's instance census says "WSL Ubuntu-24.04: one cluster". WSL names that installation `Ubuntu`. No installation called `Ubuntu-24.04` exists.

**Why it matters.** The documents are read and followed by AI agents. An agent that turns the documented name into a command, such as `wsl -d Ubuntu-24.04`, gets an error. An agent that treats the version number as the name may also conclude Instance B's installation is missing.

**What has to happen.** Every place the documents name Instance B's WSL installation must give WSL's actual name, `Ubuntu`, and state the Ubuntu version separately as a fact about it. The same name must be used identically in the configuration, the reference and the explainer.

## Anomaly 2 — The default WSL installation is the one without PostgreSQL

**What was found.** The default installation is `Ubuntu-22.04`. It has no PostgreSQL, no GBrain, no memory governor, and a different Linux user (`myubuntu`), so paths under `/home/dev-p/` do not exist in it.

**Why it matters.** Any command, script, tool or terminal profile that opens WSL without naming an installation lands in `Ubuntu-22.04`. Commands there do not fail loudly about the wrong system; they fail with "not found" errors or find nothing, which can be mistaken for Instance B being down or GBrain being missing. This is the same class of silent trap as the documented port 5432 problem, but the documents do not mention it.

**What has to happen.** David decides what happens to `Ubuntu-22.04` (see "Decisions for David"). Whatever is decided, `Ubuntu` must be the default installation, and the documents must state which installation is the default and that every WSL command names the installation explicitly.

## Anomaly 3 — An old, undocumented GBrain installation exists in Ubuntu-22.04

**What was found.** `Ubuntu-22.04` holds an older GBrain setup: a `gbrain` folder that is a git repository (145 MB), a `.gbrain` folder (40 MB), and a `.gstack` repository. Nothing in it has changed since late May 2026. The PostgreSQL configuration's census records only "WSL Ubuntu-22.04: no PostgreSQL", which is true but says nothing about this older GBrain.

**What is not known.** The contents of `/home/myubuntu/.gbrain` were not inspected. It may hold an old GBrain configuration, an old local memory store, or both. Whether anything in it is needed is not known.

**Why it matters.** The PostgreSQL suite's own principle is that no database or data store on the machine is left unexplained. An unexamined 40 MB GBrain folder breaks that principle, and an agent searching for GBrain's data could find this copy and mistake it for the live one.

**What has to happen.** The `.gbrain` folder in `Ubuntu-22.04` is inspected, its contents identified, and the finding recorded. Then the outcome of the decision on `Ubuntu-22.04` is applied.

## Anomaly 4 — No clean shutdown procedure exists for Instance B

**What was found.** The reference document gives `wsl --shutdown` as "the only real verification method" for boot durability, and treats a "stale pid file" message afterwards as normal. No document describes how to stop PostgreSQL and the two memory governor services (`memory-governor-api`, `memory-governor-worker`) before WSL is shut down.

**Why it matters.** `wsl --shutdown` stops the whole Linux system instantly, the equivalent of pulling the power plug. PostgreSQL recovers from this on restart by replaying its recent changes, which is why the documents describe the stale pid file as self-resolving. Recovery normally works, but every forced stop carries a small risk to `gbrain` and `memory_governor`, and the risk is avoidable. Disk maintenance on the virtual disk (exporting it as a backup, or shrinking it) also needs WSL fully stopped, so a clean stop is needed regularly, not just when testing boot durability.

**What has to happen.** The reference document gains one clean shutdown procedure, used every time WSL is to be shut down: stop the two governor user services, stop the PostgreSQL cluster, confirm both are stopped, then run `wsl --shutdown`. The boot-durability verification then uses that procedure instead of a bare `wsl --shutdown`. The exact commands are to be confirmed live in the resolving session before they are documented.

## Minor — A heading contradicts itself

The configuration has the heading "Known undocumented items (deliberately retained, each documented)". The items under it are documented, so the heading says the opposite of what it means. It needs a heading that describes what the items are: things deliberately left in place.

## Decisions for David

1. What happens to `Ubuntu-22.04`. It appears to be an abandoned early setup. Removing it frees about 17 GB and removes the trap in Anomaly 2 entirely. The alternative is to keep it and change the default installation. If it is removed, whether a small archive of its home folder (excluding reinstallable tools and caches) is kept on drive C: first.
2. Whether the documentation fixes are made by the config-management exam's developer gate or as a direct documentation change.

## Related work

A separate disk space plan (`optimise-windows-plan.md`) is in progress on the same machine. Its later steps export and shrink the `Ubuntu` virtual disk, which requires the clean shutdown procedure in Anomaly 4 and a fresh database backup cycle first, per the backup rule in `postgresql-config.md` ("always before ... destructive operations").
