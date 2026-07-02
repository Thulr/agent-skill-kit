# ADR 0014: The docs Family Owns Documentation as a Reading Surface

**Status:** Accepted (2026-07-02). Refines the domain boundary between the
`dx` and `docs` domains established by [ADR 0008](./0008-reverse-review-consolidation-split-by-domain-and-function.md);
does not disturb the domain × function architecture itself.

## Context

ADR 0008 split skills by domain × function but never assigned developer
documentation to a domain. Both families claimed it: `dx-audit`/`dx-design`
shipped `readme`, `changelog`, `docs`, `contributor`, and `examples` rows
over deep `_shared/dx/` playbooks (916–1,324 words each), while
`docs-audit`/`docs-design` routed the same scope through one flat 702-word
`dx-docs.md` playbook whose Scope named "README, quickstarts, tutorials, API
reference, code samples, examples, changelogs".

The seam was measured, not hypothesized: a scoped activation-routing run
(`just eval`, 209 queries judged against all 23 catalog descriptions) routed
**4 of 4** ambiguous developer-doc queries (README, CHANGELOG, contributor
onboarding doc, samples directory) to `docs-*` against the trigger-evals'
`dx-*` expectations — with anti-trigger fences already present. The catalog
had also already conceded the boundary in three places: `docs-audit`'s
description ("audit our docs/README/help"), the README routing-matrix docs
row ("READMEs, quickstarts, …"), and the PR #74 fence on `dx-audit` ("audit
docs as a reading surface → docs-audit").

## Decision

**`docs-*` owns every document a human reads — including developer docs.
`dx-*` keeps documentation friction only as it surfaces inside install /
API / error flows.**

Concretely:

- `readme.md`, `changelog.md`, `contributor.md`, `examples.md` moved from
  `skills/_shared/dx/playbooks/` to `skills/_shared/docs/playbooks/`;
  `docs.md` moved and merged with the retired `dx-docs.md` into
  `dev-docs.md` (union of heuristics; the flat playbook's unique
  search-query-replay, TTFHW, and sample-freshness heuristics survive).
- `docs-audit` (audit + debug) and `docs-design` (design + measure) route
  the five as first-class surfaces; the `dx-docs` surface id is retired.
- `dx-audit`/`dx-design` drop those five intent rows. The `edge-pass`
  intent keeps cross-domain *references* to the moved playbooks (the
  first-impressions and contributor-path sweeps still read them), which is
  reference access, not routing ownership.
- The four misrouted trigger queries flipped polarity: negatives in
  `dx-*`, positives in `docs-*`.
- Descriptions on both families now state the boundary in one sentence
  each ("owns every doc a human reads" / "docs as a reading surface →
  docs-audit").

The composition implemented all three candidates from the 2026-07-02
architecture review to the extent they compose: A (transfer readme /
changelog / dev-docs) ⊂ C (also transfer contributor / examples), plus
candidate B's fencing mechanism applied in the adopted boundary's
direction. B's ownership direction (dx keeps the surfaces) is mutually
exclusive with A/C and was not adopted.

## Consequences

- One family per reading surface: routing ambiguity measured at the seam
  should drop to zero; re-run `just eval --skills dx-audit,dx-design,docs-audit,docs-design`
  after description edits to verify.
- `_shared/<domain>/` still means "one source, many skills" (ADR 0008);
  cross-domain symlinks (dx-audit → `_shared/docs/playbooks/`) are
  legitimate for reference access and are validated by
  `scripts/check-shared-content.sh` like any other.
- Sources that informed only the moved playbooks migrated between the
  families' `skill.json.inspired_by` lists; mixed sources kept their
  remaining markers in `dx-*` and gained the moved markers in `docs-*`.
- If contributor/examples queries start misrouting back toward `dx-*` in
  future eval runs, revisit whether those two playbooks are
  workflow-shaped enough to warrant partial return — that was the known
  risk of preferring C over A.
