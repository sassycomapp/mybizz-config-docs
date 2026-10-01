---
title: "gbrain-frontmatter-requirements-and-custom-fields"
doc-id: "mb-07b00e74"
updated: "2026-10-01"
---
# GBrain Frontmatter Requirements and Custom Fields

## Direct answer

Yes. For the two cases below, current GBrain treats them as the same semantic title:

```
title: "Example"
```

and

```
title: Example
```

Both produce the YAML string value `Example`, not `"Example"` including the quotation marks. GBrain then uses the parsed `frontmatter.title` value as the document title.

There is no documented GBrain requirement that a simple title be unquoted. In fact, GBrain's own frontmatter-guard documentation explicitly describes quoted values as valid and states that unquoted values are fine for simple values.

---

## Evidence

### GBrain implementation

GBrain's current frontmatter parser explicitly uses `js-yaml`:

```
import { safeLoad, safeDump } from 'js-yaml';
```

It parses YAML with:

```
value = ... language === 'json' ? JSON.parse(block) : safeLoad(block);
```

Thus, an unlabelled `--- ... ---` frontmatter block is parsed as YAML.

GBrain's title-selection code then does:

```
coerceFrontmatterString(frontmatter.title).trim() || ...
```

The title is therefore taken from the **parsed YAML value**, rather than from the original textual representation of that value.

GBrain's own frontmatter-guard documentation states that:

```
title: 'My "Quoted" Title'
```

is correct, and that:

> Unquoted is fine for simple values

It also describes double-quoted title values as correct syntax.

### YAML specification

The YAML 1.2.2 specification explicitly states:

> “The scalar style is a presentation detail”

It defines double-quoted scalars as being surrounded by quotation-mark indicators.

The specification therefore distinguishes the presentation syntax from the scalar content. For example, the quotation marks in:

```
title: "Example"
```

delimit the scalar; they are not part of the scalar's value.

### js-yaml

GBrain's parser uses `js-yaml`, whose primary documentation identifies it as a YAML parser supporting YAML 1.2 and 1.1.

---

## Technical explanation

The parsing sequence is effectively:

```
title: "Example"        ↓YAML parser        ↓frontmatter.title = Example        ↓GBrain title selection        ↓document title = Example
```

For:

```
title: Example
```

the result is also:

```
frontmatter.title = Example
```

Therefore, for these exact inputs:

| Source syntax      | Parsed title value | GBrain document title |
| ------------------ | ------------------ | --------------------- |
| `title: "Example"` | `Example`          | `Example`             |
| `title: Example`   | `Example`          | `Example`             |

### When quotation marks *are* part of the title

Quotation marks become part of the title when they are actually encoded as content rather than being used as YAML delimiters.

For example:

```
title: '"Example"'
```

has the semantic value:

```
"Example"
```

The YAML specification permits quotation marks as content inside a differently quoted scalar.

Thus:

```
title: "Example"
```

→ title value is `Example`

whereas:

```
title: '"Example"'
```

→ title value is `"Example"`

This is the distinction between **syntactic quotes** and **literal quote characters**.

---

## Frontmatter field requirements

The current GBrain implementation and documentation distinguish between the fields that are part of the documented page convention and what the underlying parser technically requires.

| Field    | Documented convention                                               | Current technical behavior                                 |
| -------- | ------------------------------------------------------------------- | ---------------------------------------------------------- |
| `title`  | Required by GBrain's documented page convention and current linting | Not strictly required by the core parser; it has fallbacks |
| `type`   | Required by GBrain's documented page convention and current linting | Can be inferred when omitted                               |
| `tags`   | Recommended/documented convention                                   | Technically optional; missing `tags` becomes `[]`          |
| `doc-id` | Not a standard GBrain field                                         | Safe to add; arbitrary additional fields are preserved     |

In other words, `title` and `type` should be regarded as required when following GBrain's documented page convention and satisfying its current linting, even though the underlying parser itself can operate without them.

`tags`, by contrast, is not technically mandatory.

---

## Custom `doc-id` field

A custom field such as:

```
doc-id: "<doc-id>"
```

is safe to add.

The current parser treats frontmatter as a general `Record<string, unknown>`. It specifically handles fields such as `type`, `title`, `tags`, and `slug`, while preserving additional frontmatter fields.

The serializer also explicitly supports caller-specific extra fields.

Consequently, there is no known compatibility risk associated with adding:

```
doc-id: "<doc-id>"
```

provided that the value itself is valid YAML.

The strongest implementation evidence is that GBrain:

1. treats frontmatter as a general key/value record;
2. specifically handles its known fields;
3. preserves additional fields; and
4. explicitly supports additional caller-specific fields during serialization.

---

## Recommended frontmatter

For a conventional GBrain document, a frontmatter block could therefore look like:

```
---
title: "Example"
type: "document"
tags:  - exampledoc-id: "<doc-id>"
---
```

A simple title can equally be written as:

```
---
title: Exampletype: documenttags:  - exampledoc-id: "<doc-id>"
---
```

Both forms produce the same semantic title value:

```
Example
```

There is no evidence that GBrain requires the title to be quoted.

---

## Important qualification about H1 headings

One correction to a possible premise is worth noting: GBrain's current generic `parseMarkdown()` implementation does **not** require the H1 to be the document's first line when `title:` is absent.

Its documented implementation precedence is:

```
frontmatter title        ↓first body H1        ↓filename/slug-derived title
```

Its H1 inference searches for the first standalone H1 in the body.

This distinction does not affect the quotation-mark question, but it means that H1 behavior should not be treated as a universal current GBrain requirement without qualification.

---

## Confidence and caveats

**Confidence: High.**

There are three independent sources of evidence:

1. **GBrain implementation** — frontmatter is parsed with `js-yaml`, and the parsed title field is used.
2. **GBrain documentation** — quoted title scalars are explicitly documented as correct, while simple unquoted values are explicitly described as acceptable.
3. **YAML specification** — quoting style is presentation syntax; the surrounding double quotes are not part of the scalar's content.

---

## Primary sources

- GBrain `brain-first.md` — page/frontmatter convention
- GBrain `markdown.ts` — parsing, defaults, preservation of extra fields, and serialization
- GBrain `data-frontmatter.ts` — YAML/JSON frontmatter parsing
- GBrain `lint.ts` — current lint requirements
- GBrain frontmatter-guard documentation — frontmatter validation model
- YAML 1.2.2 specification — scalar styles and quoting
- `js-yaml` primary repository/documentation — YAML parsing behavior

## Conclusion

For a simple title such as `Example`, these are semantically equivalent to GBrain:

```
title: "Example"
```

and:

```
title: Example
```

The quotation marks in the first form are YAML syntax, not part of the title.

Regarding the frontmatter fields:

- **`title`** — conventionally/lint-required by GBrain, although the core parser has fallbacks.
- **`type`** — conventionally/lint-required, although the parser can infer it when omitted.
- **`tags`** — recommended but technically optional; missing tags become `[]`.
- **`doc-id`** — safe to add as a custom field; the current implementation preserves additional frontmatter fields.

**Bottom line:** using `doc-id: "<doc-id>"` alongside `title`, `type`, and `tags` is supported by the current GBrain implementation, and there is no known compatibility blocker associated with the custom `doc-id` field.
