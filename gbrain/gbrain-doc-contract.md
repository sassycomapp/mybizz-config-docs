---
title: "gbrain-doc-contract"
doc-id: "mb-62de0f89"
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
- **G7** — A wikilink, if used, is `[[bare-name]]` or `[[dir/slug]]`, optionally with `|Display Text`. A bare name must be the only file with that basename in the source; otherwise it does not resolve.
- **G8** — GBrain takes the page title from `title:`, else the first H1, else the path. No other field is used.
- **G9** — GBrain ingests only committed files in a registered source. Uncommitted edits are not ingested.

## MyBizz convention (developer-owned; GBrain does not require it)

- **C1** — Documentation files and documentation skills (on C:\, not installed): frontmatter is `title: "filename-stem"` and `doc-id: "mb-xxxxxxxx"`. The doc-id is a permanent random code that `mb-doc-check` adds and never changes, so a renamed or moved document can always be recognised. GBrain ignores it.
- **C2** — Installed skills (WSL): frontmatter `name` and `description`, both YAML strings. Out of scope for this contract; documentation skills never modify them.
