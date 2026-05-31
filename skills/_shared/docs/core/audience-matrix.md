# Audience Matrix

DX, UX, and AX are **audience-differentiated peers of one parent discipline —
experience design** (designing a system for the cognition and goals of whoever is
on the other side). They are **peers, not nested: DX is not a subset of UX.** DX
inherits UX's cognitive theory (mental models, friction, feedback, error
recovery) but not its practice — each peer differs by **substrate** (what the
audience reads), **success metric** (what "good" optimizes for), and **cost of
error** (re-clickable for UX, contract-permanent for DX, silent-at-scale for AX).
Content-ops is the cross-cutting closure layer, not a fourth audience. See
[ADR 0007](../../../../docs/adr/0007-experience-disciplines-are-audience-peers.md)
for the full model and [ADR 0006](../../../../docs/adr/0006-discipline-front-doors-vs-one-engine-many-surfaces.md)
for why AX is packaged as its own skill while dx/ux stay routed domains.

Use this matrix before recommending changes to multi-audience documentation. The
columns map to the differentiators above: *Optimizes for* ≈ success metric,
*Needs surfaced as* ≈ substrate, *Common failure* ≈ the audience's cost of error.

| Audience | Optimizes for | Needs surfaced as | Common failure |
|---|---|---|---|
| Developer (DX) | Cognitive efficiency and integration speed | README, quickstart, API reference, types, examples, changelog, searchable troubleshooting | Reference without a first-success path; examples that do not run. |
| End user (UX) | Learnability, recovery, and reduced context switching | Labels, empty states, in-product help, help-center articles, plain-language errors, accessible structure | Critical guidance hidden in tooltips or long articles. |
| Agent (AX) | Machine readability, deterministic action, context budget, stable contracts | Schemas, structured errors, `llms.txt`, markdown pages, context files, examples, tool descriptions | Ambiguous prose, unstable messages, or instructions outside retrievable text. |
| Content operations | Freshness and feedback closure | CI checks, telemetry, issue backlog, review ownership, release gates | Helpful page scores with no action path or no owner. |

## Transfer rules

- Shared foundations: clear modes, stable URLs, docs-as-code, plain language, versioning, accessible structure, and measured feedback loops.
- Modified inheritance: code samples, style rules, and progressive disclosure change shape by audience.
- AX-only requirements: routing descriptions, context budget choices, chunk survivability, stable machine codes, schema descriptions, and enforced forbidden-action gates.

## Conflict rule

When a pattern helps one audience and hurts another, do not choose a compromise by taste. Prefer one of:

1. **Single source, multiple renderings** — same canonical content rendered as page, markdown, schema, or in-product help.
2. **Visible plus machine-readable** — human UI keeps visual affordance while text/schema carries the load-bearing instruction.
3. **Scope split** — separate first-success docs, reference, help article, and agent contract when mode mixing is the bug.
4. **Measured exception** — choose an audience-specific optimization and add telemetry/eval coverage for the harmed audience.
