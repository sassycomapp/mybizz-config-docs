---
title: "gbrain-doc-contract"
doc-id: "mb-33c1a0cb"
updated: "2026-10-01"
---
# gbrain-doc-contract

The minimum a document must meet so GBrain can ingest it and read its title.
Nothing else is required. Rule IDs are kept from the previous version; missing
numbers were removed.

## GBrain requirements

- **G1** — Frontmatter, if present, must be valid YAML. Invalid YAML: the file is not ingested and the source's sync bookmark stops advancing.
- **G2** — Frontmatter, if present: first line `---`, closing `---`, something between them, no null bytes.
- **G4** — Never write a `slug:` field. GBrain derives the slug from the path.
- **G5** — `title` must be a YAML string. Always quote it. A value containing a double quote is wrapped in single quotes.
- **G7** — A link is stored in one standard form: `[[[source-id:slug]]](C:/full/windows/path.md)`, optionally `[[[source-id:slug|Display Text]]](C:/full/windows/path.md)`. GBrain reads the part inside the brackets: `source-id` is the GBrain source of the target, `slug` is the target's path from its repository root in lower case, spaces as hyphens, without `.md`. The part in round brackets is only for MarkText. The link is followed across sources when the page that holds it is in a federated source. Inside a markdown table row the pipe before the display text is written `\|`. A bare `[[name]]` is read only inside its own source, and a link with a bare name inside the wrapper is not followed. Authors write `[[name]]` or `[[name|Display Text]]` and the commit hook rewrites it.
- **G8** — GBrain takes the page title from `title:`, else the first H1, else the path. The only other fields it reads are date fields such as `date`, `event_date`, `published` and `created`: they become the page's effective date and can change search ranking. MyBizz documents therefore use `updated`, which GBrain ignores.
- **G9** — GBrain ingests only committed files in a registered source. Uncommitted edits are not ingested.

## MyBizz convention (developer-owned; GBrain does not require it)

- **C1** — Every documentation file, including documentation skills (on C:\, not installed): frontmatter `title: "filename-stem"`, `doc-id: "mb-xxxxxxxx"` and `updated: "YYYY-MM-DD"`. The `doc-id` is a permanent random code and never changes. `updated` is the date of the last real change. The commit hook `mb-doc-check` adds and keeps all three; nobody writes `doc-id` or `updated` by hand. The files and folders the program skips are listed in [[[mybizz-config-docs:mb-doc-check/doc-check-config]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-config.md).
- **C2** — Installed skills (WSL): frontmatter `name` and `description`, both YAML strings. Out of scope for this contract; documentation skills never modify them.
- **C3** — Documents are stored with LF line endings (GBrain also reads CRLF). The commit hook converts.
- **C4** — `SKILL.md` files and `obsolete` folders are never touched by the commit hook.
