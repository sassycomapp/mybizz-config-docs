# Anvil Docs — Reference

Companion to `anvil-docs-config.md` (current state) and
`anvil-docs-explainer.md` (mechanics and real incidents). Agent-facing.

---

## Finding official documentation content

`site-map.md` is the authoritative URL → path lookup for every one of
the 298 real, scraped documentation pages. Given a real
`anvil.works/docs/...` URL, the exact local file path is directly
derivable from it (URL-slug naming — no separate lookup needed beyond
`site-map.md` for confirming a page's exact location in the tree).

Example: `anvil.works/docs/users` → `users/_index.md`.
`anvil.works/docs/users/presenting-a-login-form` →
`users/presenting-a-login-form.md`.

## Finding absorbed runtime source content

**No separate index exists for this — real content was placed by subject
during absorption, directly into the matching documentation topic
folder.** To find real source code for a given Anvil feature, go to that
feature's own topic folder first (e.g. `integrations/stripe/` for
Stripe, `data-tables/` for Data Tables) — the real source sits alongside
the real documentation for the same subject, not in a separate location.

## Re-running the content-stripping pipeline

`step1b-strip-write.py` is a real, working, reusable tool — not
historical. If any single official documentation page ever needs
re-scraping (a live-site correction, a page previously missed), this is
the correct, validated tool for it:

```bash
python3 step1b-strip-write.py TARGET_RELPATH < RAW_MARKDOWN_FILE
```

`TARGET_RELPATH` is the file's real path relative to this corpus's root
(e.g. `overview/faq.md`). `RAW_MARKDOWN_FILE` is a real `webfetch`
markdown capture of the live page, piped in via stdin. The script
preserves the target file's existing frontmatter byte-for-byte and
replaces only the body.

**Real, validated strip rule** (proven on the original 298-page scrape,
zero known failures): article body starts at the page's own first `# `
heading, ends at either `### Do you still have questions?` or a
`TM[](` footer-logo marker, with the chrome separator between body and
footer correctly excluded.

## Real cross-references left as plain hyperlinks, not wikilinks

Links inside scraped documentation pages (e.g.
`[Quickstart for logins](users/quickstart-login)`) are real, plain,
relative markdown links — not GBrain wikilinks. This was a deliberate
choice: GBrain's `mb-wikilinks` resolver is scoped to markdown files by
its own design (confirmed directly from its source), and would not
meaningfully apply to the many non-markdown source files also present
in this corpus. Fixing a broken relative link, if one is found, means
correcting the relative path directly in the file — there is no
automatic resolution mechanism for these.

## Verifying real file counts (no backup currently exists for this corpus)

```bash
find /mnt/c/mybizz/config/anvil/anvil-docs -type f | wc -l
```

Given there is no standing backup of this corpus, any bulk operation
against it should be preceded by a real count like this, and followed
by the same command to confirm the expected before/after delta — the
same discipline used throughout the corpus's own construction.

## Do not

- Do not assume a wikilink (`[[name]]`) will resolve anything in this
  corpus — none exist here by design.
- Do not assume `step1b-strip-write.py` needs modification before
  reuse — it is a generic, validated tool, not tied to any specific
  page's content.
- Do not search for runtime source code by the Anvil Runtime's own
  internal folder names (`services/`, `native_rpc_handlers/`) — that
  structure no longer exists in this corpus; search by subject/topic
  instead.
- Do not perform a bulk operation against this corpus without a real,
  independent file-count check before and after — there is no backup
  to fall back on.
