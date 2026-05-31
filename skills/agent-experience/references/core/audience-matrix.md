# Audience Matrix (AX excerpt)

This is the AX-focused excerpt. AX is a **peer** of DX and UX — three
audience-differentiated specializations of one parent discipline (experience
design), not a hierarchy; the agent is simply a different audience with a
different substrate (machine-readable structure), success metric (deterministic
action under a context budget), and cost of error (silent failure at scale). See
[ADR 0007](../../../../docs/adr/0007-experience-disciplines-are-audience-peers.md).

The canonical **four-audience** matrix (Developer / End-user / Agent /
Content-ops) lives in `docs-critique` / `docs-design`
(`references/core/audience-matrix.md`); use it when a decision spans human
and agent audiences at once. Use this excerpt when the agent is the audience
under review.

| Audience | Optimizes for | Needs surfaced as | Common failure |
|---|---|---|---|
| Agent (AX) | Machine readability, deterministic action, context budget, stable contracts | Schemas, structured errors, `llms.txt`, markdown pages, context files, examples, tool descriptions | Ambiguous prose, unstable messages, or instructions outside retrievable text. |

## Transfer rules

- **Shared foundations** (apply to every audience): clear modes, stable URLs,
  docs-as-code, plain language, versioning, accessible structure, and measured
  feedback loops.
- **Modified inheritance** (change shape by audience): code samples, style
  rules, and progressive disclosure.
- **AX-only requirements:** routing descriptions, context-budget choices
  (always-loaded vs load-on-demand; W6), chunk survivability, stable machine
  codes, schema descriptions, and enforced forbidden-action gates (W3).

## Conflict rule

When a pattern helps the agent and hurts a human audience (or vice versa), do
not pick a compromise by taste. Prefer one of:

1. **Single source, multiple renderings** — one canonical fact rendered as page,
   markdown, schema, or in-product help.
2. **Visible plus machine-readable** — the human UI keeps its visual affordance
   while text/schema carries the load-bearing instruction.
3. **Scope split** — separate the first-success doc, reference, help article,
   and agent contract when mode mixing is the bug.
4. **Measured exception** — choose an audience-specific optimization and add
   telemetry/eval coverage for the harmed audience.

See `references/playbooks/audience-conflicts.md` for the AX-vs-human resolution
heuristics.
