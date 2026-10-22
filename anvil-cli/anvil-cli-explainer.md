---
title: "anvil-cli-explainer"
doc-id: "mb-5488f725"
updated: "2026-10-22"
---

# anvil-cli — Explainer

## What it is

The Anvil CLI is Anvil's own command-line tool, in beta, for working on an Anvil app
from a local IDE instead of the web editor. Installed in WSL and logged in to the
developer's Anvil account, it solves a specific problem for MyBizz: an agent can prove
that Anvil app files are syntactically correct without opening the Anvil editor, and
the machine can hold a verified login to the Anvil account. It is the backbone that
every one of Anvil's published agent skills relies on, and the tool PDLF's
data-table step depends on.

## What it can do

It validates app files — the manifest, form templates, HTML templates and the Python
under `client_code` and `server_code` — and reports problems in machine-readable form
an agent can act on. It manages login and per-account tokens through device login,
checks out an app locally from an editor URL or an app ID, caches app
dependencies and table mappings, converts legacy form templates, and diagnoses Git
authentication. Two of its abilities are deliberately not used in MyBizz: the
bidirectional watcher that syncs a local folder with the Anvil editor, and anything
that applies database schema to the live app.

## Suitability

Best for: validating Anvil app files during any PDLF step or skill run; confirming
the tool answers at all (the standing health check); checking configuration; and
one-off checkouts of an app repository.

Good for: diagnosing Git authentication to Anvil; inspecting cached dependencies and
table mappings.

Not good for: applying a schema change to the live app — the developer applies schema
in Anvil's Data Tables view, and the command that would do it from a terminal does not
exist in the installed version. Not good for keeping local and Anvil in sync during a
step — the developer's plain Git push and pull procedure does that, under the
developer's control. The right tool for Anvil knowledge is Anvil's published skill
set; for running an app locally with a test database, the separate Anvil App Server
system.

## Why it works this way

The tool is beta, and Anvil's own documentation leaves the watcher's handling of
conflicting edits undocumented. MyBizz's pipeline sends every change to Anvil through
the developer's explicit push, so a background two-way sync would move an agent's
local edits straight to the development app without a human gate — the exclusion is a
design decision, recorded where the pull procedure is defined, not an oversight.

The schema-applying command of the newer pre-release line registers only inside
Anvil's own hosted agent environment and is self-described as able to delete tables,
columns or data. MyBizz runs the pinned stable, where the command does not exist, and
schema reaches the live app only through the developer — the same human gate, from the
other direction.

The CLI itself only reads and validates app files; it never edits the manifest. Who
may change the manifest, and how, is governed elsewhere (Anvil's anvil-yaml skill, and
MyBizz's write blocks), so the CLI never becomes a path around policy.

## What has to happen

The installer-maintained PATH entries must stay in the shell profiles; agents depend
on them. The login token must stay valid; when commands start failing on
authentication, the developer re-runs the login. The version stays pinned at the
current stable release; the developer decides on any update, and the pre-release line
stays uninstalled. The vendor clone `anvil-agent-references` stays pinned at commit
14b1967; it changes only by the developer's decision. The policy blocks on manifest
writes stay in force.
