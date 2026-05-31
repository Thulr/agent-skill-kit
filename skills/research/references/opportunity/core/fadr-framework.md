# Facts / Assumptions / Decisions / Risks (F/A/D/R)

The four-layer fold every area artifact ends with. **Required.** A
research branch that ends in "notes" without these four layers is the
named failure mode in the source.

## The four layers

### Facts

What is **observably true**, with a citation (URL, document, recorded
interview) and a confidence tag from
[`confidence-rubric.md`](./confidence-rubric.md). One-line each.

> Example: "The US small-business accounting market is ~$5B in
> annual spend (source: IBISWorld 2025, confidence H)."

Rules:
- Every Fact carries a source. Unsourced "facts" are demoted to
  Assumptions.
- Any L-confidence fact is auto-promoted to an Assumption.
- Facts can be wrong later — when discovered, edit the artifact,
  don't pretend the original was an Assumption all along.

### Assumptions

What we **believe but have not proven** — and what would happen if
the assumption is false. Each assumption carries a falsifiable test
that closes it.

> Example: "We assume SMB accountants will adopt an AI-native tool if
> it saves 4+ hours/week. If false: positioning collapses. Test: run
> 5 paid pilots, measure adopted hours saved, kill if median < 2."

Rules:
- Every Assumption carries a **test** (a falsifiable, ideally
  <1-week experiment).
- Assumptions are ranked by **leverage** — what changes downstream
  if they flip — not by ease of testing.
- The top 3 assumptions become the **investigation plan** for the
  next iteration.

### Decisions

What this research **changes**. A decision is forward-commitment, not
a record of opinion.

> Example: "We will target enterprise (50+ accountant teams) for
> beachhead, not SMB. Reason: ICP signals + Five-Forces analysis
> show prosumer is rivalry-dominated."

Rules:
- Every Decision changes something downstream — staffing, scope,
  pricing, channel, sequencing. If it doesn't change anything, it's a
  Note, not a Decision.
- Every Decision names what it ruled out. Decisions without
  ruled-out alternatives are typically vibes, not decisions.
- Decisions get reviewed when the underlying Assumptions are tested,
  not on a fixed cadence.

### Risks

What could **still go wrong**, with severity (0–4 from
[`severity-rubric.md`](./severity-rubric.md)), likelihood, mitigation,
and owner.

> Example: "Risk: Apple App Store rejects under guideline 3.2.1 —
> severity 4, likelihood Med, mitigation: web-app fallback in
> parallel, owner: @founder. Kill criterion: rejected twice with no
> path."

Rules:
- Severity 4 risks must be either resolved or named in the kill
  criteria for the opportunity.
- Severity 3 risks must have a named owner + mitigation.
- "Watch and see" is not a mitigation.
- Concentration risks (one customer / channel / vendor / data
  source contributing >30%) are first-class — surface them in the
  area artifact and the cross-area brief.

## How to write the F/A/D/R block in an artifact

Every area artifact ends with the four sections. Each section is a
bulleted list with the rules above. If a section is empty, write
"None — explain why." rather than omitting the section. An empty
F or D suggests the research isn't actually done.

## How `decide` intent uses F/A/D/R

The `decide` intent collapses the per-area F/A/D/R sections into a
cross-area fold:

- **Top-3 Facts** that shape the call.
- **Top-3 Assumptions** with their tests, ranked by leverage.
- **The Decision** (go / no-go / pivot) with what it rules out and
  what review trigger reopens it.
- **Top-3 Risks** including any severity-4s that become kill
  criteria.

See [`decision-gates.md`](./decision-gates.md) for the go/no-go
mechanic itself.
