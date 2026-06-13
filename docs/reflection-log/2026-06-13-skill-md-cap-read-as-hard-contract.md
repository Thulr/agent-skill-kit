---
date: 2026-06-13
harness: claude-code
sub-surface: instruction-surface
severity: 2
status: resolved
related: [2026-05-28-restructure-split-justified-by-unenforced-cap]
---
# Read the AGENTS.md "under 1200 words" guideline as a hard contract again

## What happened

During a catalog craft pass, I treated the AGENTS.md line "`SKILL.md` … under
1200 words" as an enforced contract that `agent-readiness` (1862 words) and
`agent-rules` (1573) were *violating*. I framed tightening them as "bringing
them under the cap," chased the exact number with micro-trims (`agent-readiness`
1214 → 1193 body words), and was one step from adding a repo-wide SKILL.md
word-count static gate.

Reading [`2026-05-28-restructure-split-justified-by-unenforced-cap.md`](./2026-05-28-restructure-split-justified-by-unenforced-cap.md)
stopped that. The maintainer **deliberately** leaves these two skills uncapped in
their `evals/run-static-checks.sh` (neither asserts a SKILL.md word count), and a
prior multi-agent pass that proposed *splitting* the same two skills on the same
false "cap violation" premise was already judged a W1-adjacent failure. `just
check` was green at 1862/1573 words because nothing gates that number.

The underlying edits were independently sound and were kept: removing an "Output
requirements" section that restated Workflow step 6 verbatim, a "Recording bar"
section that restated the Core principle, a no-pipe-tables rule stated three
times, and a "Lens dispatch" section duplicating the workflow steps — plus fixing
the audit-family H1 drift (`X Critique` → `X Audit`). Only the cap-as-driver
*framing* and the proposed gate were wrong; the de-duplication stands on clarity.

## What to do differently

Same lesson as 2026-05-28, now a second occurrence: do not read the AGENTS.md
word-count prose as an enforced contract. The per-skill `run-static-checks.sh` is
the binding cap, and several skills are deliberately exempt. **Do not add a
repo-wide SKILL.md word-count gate from this** — that scaffolds a gate the
maintainer pointedly omitted (W1: two observations are below the three-entry
promotion floor, and the right fix here is removing ambiguity, not gating). Closed
at the source: AGENTS.md line 85 now says the ~1200 figure is a *default*, names
`run-static-checks.sh` as binding, notes complex skills may raise or omit it, and
links the 2026-05-28 entry. If a third instance lands, the promotion target is
normalizing that guideline's wording across surfaces — still not a gate.

## Closed by

Clarified AGENTS.md line 85 (the per-skill-required-artifacts cap bullet) plus
this entry, in the same change that de-duplicated the two SKILL.md files.
