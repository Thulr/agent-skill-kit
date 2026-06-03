---
date: 2026-06-03
harness: claude-code
sub-surface: skills
severity: 1
status: open
related: ["2026-06-03-audit-intent-id-vocabulary-drift"]
---
# skill.json and SKILL.md descriptions diverge in 14 of 19 skills

## What happened

The same cross-skill audit found two coexisting conventions for the routing
description every skill carries twice — `SKILL.md` frontmatter `description:` and
`skill.json` `"description"`:

- **5 skills identical** — `agent-evals`, `agent-experience`, `agent-readiness`,
  `agent-rules`, `research`: the two strings are byte-identical.
- **14 skills divergent** — every `*-audit`/`*-design` pair + `ui-design`: the
  `skill.json` copy is a *different* string (opens "Heuristic AUDIT of…", appends
  "Grounded in the canonical … literature (provenance below)."), e.g.
  `architecture-audit/skill.json:3` vs `architecture-audit/SKILL.md:3`.

The routing *targets* match across both copies, so this is stylistic, not a routing
contradiction — but the double-write is real double-maintenance, and it is exactly
what let the `perf-design` → `ux-design` dead route (fixed this session) live
independently in both `SKILL.md:3` and `skill.json:3`. The third description field,
`metadata.catalog_summary`, is deliberately separate (drives the README) and is in
sync — not part of this finding.

## What to do differently

Decide which surface is canonical and apply it uniformly:

- If the enriched `skill.json` blurb (with the provenance line) is wanted → bring the
  5 identical skills up to it.
- If identical-to-`SKILL.md` is wanted → strip the enrichment from the 14.

Once the convention is chosen, the smallest gate is a `run-static-checks.sh` (or
`scripts/`) assertion comparing `skill.json.description` to `SKILL.md` `description:`
(exact-match, or match-modulo-the-provenance-suffix). Do **not** add the gate before
the convention is decided — it would currently fail 14 skills. One observation, below
the W1 ≥3 floor — record only; needs a maintainer decision (enriched vs identical)
before any edit.

## Closed by

Not yet closed.
