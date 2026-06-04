---
date: 2026-06-03
harness: claude-code
sub-surface: skills
severity: 2
status: open
related: []
---
# README/dev-doc queries route ambiguously between docs-audit and dx-audit — the disambiguator lives in catalog prose, not the descriptions

## What happened

A maintainer asked, in plain language, which catalog skill would "update
project documentation like a README." The assistant could not name one — it
enumerated `docs-audit`, `docs-design`, `writing-audit`, `dx-audit`, and
`dx-design` (plus two retired `-heuristics` names the harness still surfaces).
A human who knows this catalog having to ask "which one?" is the triggering
signal: if the human can't self-route, an LLM seeing "update my README" has the
same ambiguity.

Root cause in the files: README and developer-doc *content* are legitimately
claimed by **both** `docs-audit` and `dx-audit`. Each skill's `description`
carries three "Do NOT use" cedes, but they fence the **audit↔design** (function)
axis only — neither names the other across the **docs↔dx** (surface) axis. The
seam is unfenced, and READMEs sit exactly on it (a README is both "documentation
content someone reads" and "the onboarding front door to a code package").

Evidence, straight from the evals:

- The near-identical *terraform-module-docs* query is `should_activate: true` in
  **both** skills: `skills/docs-audit/evals/trigger-evals.json:15` (route
  `audit/dx-docs`) and `skills/dx-audit/evals/trigger-evals.json:10` (route
  `audit/docs`). The eval contract itself says both should fire on the same
  prompt.
- `dx-audit` owns a dedicated `readme` route
  (`skills/dx-audit/evals/trigger-evals.json:13`) and a README first-impressions
  edge case (`:14`); `docs-audit` claims README in its `description` and in its
  own L5 positive ("copy this README and tell me where people fall off").
- "Edit our API docs for clarity" is a `writing-audit` positive
  (`skills/writing-audit/evals/trigger-evals.json:24`, route
  `revise/technical-doc`) that `docs-audit` and `dx-audit` could each equally
  claim — neither cedes line-level prose *down* to `writing-audit`, though
  `writing-audit` correctly cedes *up* to `docs-audit` for the docs system.

The deciding criterion already exists — in the wrong place. The
`catalog/catalog.json` `unsure` block (line 32) tells a human: "audit existing
docs → `docs-audit`; … API/SDK friction beyond the docs → `dx-audit`." That
renders into README prose via `scripts/build-catalog.py` but **never reaches the
`description` frontmatter**, which is the only field the model reads at
activation time. So the catalog disambiguates for a human who reads the README
and does nothing for routing.

Compounding (out of repo scope): the harness still lists retired `-heuristics`
skill names (`docs-experience-heuristics`, `dx-heuristics`) — renamed into the
`-audit`/`-design` pairs in PR #42 — alongside the new names, so the
human-facing name space is doubled. That is a stale external install, not a
repo defect, but it sharpened the confusion in this session.

## What to do differently

The routing-load-bearing fence is the `description` field, not catalog prose.
When two skills legitimately claim the same surface (README, developer docs),
each description's "Do NOT use" list must name the other and carry the deciding
question — port the `catalog.json` `unsure` criterion into both descriptions:

- **`docs-audit` ⇄ `dx-audit`** (surface axis). `docs-audit` cedes "a code
  package's developer onboarding / README-as-first-impression alongside its
  API/CLI/errors/setup" to `dx-audit`; `dx-audit` cedes "documentation as a
  reading surface — content quality, IA, findability, retrieval, audience
  conflict" to `docs-audit`.
- **`docs-audit` and `dx-audit` → `writing-audit`**: each cedes "only tighten
  the line-level prose of a single piece, no docs-system judgment" to
  `writing-audit`.
- Mirror on the design side: **`docs-design` ⇄ `dx-design`** (README/dev-doc
  *structure* is double-claimed the same way).

Make the eval double-claim a **documented** decision, not a silent one. The
terraform/README double-positive should either resolve to one owner (make it
`should_activate: false` in the other, with `expected_route`) or stay
double-claimed with a one-line `$comment` rationale. A silent double-positive
encodes the ambiguity rather than resolving it; once `expected_route` is
asserted across skills it becomes the regression test for the fence.

Scope discipline (W1 ≥3 floor). This is **one** observation and the first
cross-skill routing-fence entry in the log (grep of
`docs/reflection-log/[0-9]*.md` for routing/description/collision returns only
incidental matches). The reciprocal cedes are *in-skill fence completion* —
bug-fix level, closing an incomplete "Do NOT use" list — not new scaffolding, so
they are not gated by the ≥3 floor. But do **not** promote to a cross-cutting
rule ("every shared-surface description must name its neighbor + a trigger-eval
asserts the split") or a routing-lint gate until two more collisions surface.
The `catalog.json` `unsure` block already names the next two candidates:
`perf-audit`↔`dx-audit` on local-machine performance, and `ux-audit`↔`docs-audit`
on help content. If either trips, that is entry two/three and the basis to
promote.

## Closed by

Not yet closed. The reciprocal docs↔dx cedes (docs-audit, dx-audit, docs-design,
dx-design descriptions + their skill.json mirrors) and the documented
double-claim (`$comment`) in the docs-audit/dx-audit evals landed on branch
`fix/docs-dx-routing-fence` (PR pending code-owner review; `just check` green).
The systemic gap — description fences cover the function axis but not the surface
axis, and the disambiguator lived in catalog prose rather than the routing
field — is narrowed for this pair but has no general rule or lint, and is below
the W1 ≥3 floor for promoting one.
