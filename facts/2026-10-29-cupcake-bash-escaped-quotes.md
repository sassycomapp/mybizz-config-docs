---
title: "2026-10-29-cupcake-bash-escaped-quotes"
doc-id: "mb-51a0ed94"
updated: "2026-10-29"
---
Bash command text reaches Cupcake policies with shell-escaped quotes as literal backslash plus quote: `psql -c "INSERT INTO public.\"gates\" ..."` carries `\"` (backslash immediately before each double quote), not a bare quote. Optional-quote patterns in deny rules must tolerate that backslash — in RE2, `\\?\"?` (an optional backslash before the optional quote). Observed live 2026-10-29: SQL-write deny patterns using a bare optional quote silently missed `public.\"gates\"` and `\"public\".\"gates\"`; adding the optional backslash made the same fixtures deny while the SELECT fixture stayed clean.
