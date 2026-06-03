---
date: 2026-05-28
harness: claude-code
sub-surface: other
severity: 2
status: resolved
related: []
---
# Proposed a skill split from a "<800-word cap violation" the gates never enforced

## What happened

During a catalog-restructure analysis, a multi-agent pass recommended splitting
`project-agentification` (1804 words) and `agent-rules` (1551
words) into ~7 smaller skills. Its single load-bearing justification was that
these skills "violate the catalog's own <800-word SKILL.md contract."

That premise was false **as enforced**. The 800-word bound is not a global gate —
it is set per skill inside each `evals/run-static-checks.sh`, and the maintainer
had already tuned it for exactly these skills:

- `project-agentification/evals/run-static-checks.sh` — **no** SKILL.md word
  cap (only a 900–3200 *playbook* bound).
- `agent-rules/evals/run-static-checks.sh` — **no** word cap.
- `opportunity-research/evals/run-static-checks.sh` — cap deliberately raised to
  `< 1200` (file was 962).

`just check` was green for all three. The "only these three break the cap"
evidence was an artifact of reading the AGENTS.md guideline ("under 800 words")
as a hard, uniform gate without grep-checking what each `run-static-checks.sh`
actually asserts. Acting on it would also have contradicted the same plan's
review-family *merge* (splitting one engine-with-many-surfaces while merging
seven of them) and regressed `project-agentification`'s documented 90%-case.
The split was dropped; the merges (review 7→1, research 2→1) shipped.

## What to do differently

Before citing a "contract/gate violation" as the reason for a structural change,
**read the gate that supposedly enforces it** and confirm it fails — don't infer
enforcement from a prose guideline in AGENTS.md. Per-skill `run-static-checks.sh`
can and do override repo-wide defaults (word caps here; the same is true of any
"every skill must…" statement). This is a W1-adjacent failure: scaffolding (here,
a 7-way split) proposed from an unverified premise. The cheap check that closes
it: `grep -nE 'wc|word|[0-9]{3,}' skills/*/evals/run-static-checks.sh` to see the
*actual* bound per skill before treating any single number as a contract.

## Closed by

This entry + `docs/specs/2026-05-28-catalog-consolidation/` (the restructure that
dropped the split and shipped the consolidation instead). The merged catalog
keeps `project-agentification` and `agent-rules` whole.
