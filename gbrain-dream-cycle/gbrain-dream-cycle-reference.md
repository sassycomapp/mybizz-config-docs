# GBrain Dream Cycle Reference — Invocation and Diagnostics

Companion to `gbrain-dream-cycle-config.md` (current state) and
`gbrain-dream-cycle-explainer.md` (narrative and the one operationally
relevant incident). Agent-facing.

---

## Running a full dream cycle

```
gbrain dream
```

Runs all phases in sequence, including `extract_atoms` and
`resolve_symbol_edges`.

## Running a single phase

```
gbrain dream --phase extract_atoms
gbrain dream --phase resolve_symbol_edges
```

Use this when only one phase needs to be re-run, or when diagnosing a
specific phase's failure without re-running the whole cycle.

## Inspecting real phase-level output

```
gbrain dream --json | jq '.phases[] | select(.name=="extract_atoms")'
```

**This is the real, reliable diagnostic — not the cycle's own summary
line.** A summary can report a bare failure count with no explanation;
the per-phase JSON output is where the actual underlying error, if any,
is findable. See `gbrain-dream-cycle-explainer.md` Section 4 for the
real incident this specifically matters for.

## Dry-run

```
gbrain dream --dry-run --json
```

Confirmed clean of embed-summary noise in stdout — safe to use for a
quick check of what a cycle would do without committing to a full run.

## Diagnosing a silent or repeated failure

1. Run the single failing phase directly (`--phase`), not the full cycle.
2. Pipe its `--json` output through `jq` and inspect the actual error
   field, not just the summary count.
3. If the phase is `extract_atoms` specifically, check
   `ANTHROPIC_API_KEY` validity first — this is the real, confirmed
   cause of one prior extended outage (see explainer, Section 4).
   Diagnose the key directly, since the CLI does not surface the real
   error itself:
   ```bash
   curl -s https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" -H "content-type: application/json" -d '{"model":"claude-haiku-4-5-20251001","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'
   ```
   A `401 authentication_error` confirms the key is genuinely dead.
4. If a key was recently rotated, confirm the pasted value has no stray
   line break or trailing whitespace inside its quoted form — a second,
   distinct real cause of the same outage, surfacing as an unrelated
   "invalid JSON" error:
   ```bash
   echo "$ANTHROPIC_API_KEY" | cat -A
   ```
   Should show exactly one line ending in `$`.

## Do not

- Do not accept a bare "N failed" summary as a diagnosis — always check
  the real per-phase JSON output first.
- Do not assume a credential problem is the cause without checking —
  but do check it first for any `extract_atoms` failure, given its
  confirmed history.
- Do not run a full dream cycle to diagnose a single failing phase —
  use `--phase` to isolate it.
