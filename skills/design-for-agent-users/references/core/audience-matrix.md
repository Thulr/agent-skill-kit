# Audience Matrix (AX excerpt)

This is the AX-focused excerpt. AX is a **peer** of DX and UX — three
audience-differentiated specializations of one parent discipline (experience
design), not a hierarchy; the agent is simply a different audience with a
different substrate (machine-readable structure), success metric (**tokens per
successful outcome** — token, tool-call, and retry cost per completed job, not
just task success), and cost of error (silent failure at scale). See
[ADR 0007](../../../../docs/adr/0007-experience-disciplines-are-audience-peers.md).

Peer does not mean symmetric. AX **dominates upstream** whenever an agent builds,
operates, or repairs the product: a polished screen does not rescue an agent that
cannot discover the workflow, parse the contract, or recover from the error. When
a surface is consumed both ways, decide AX-first for the agent-reachable path and
keep the human affordance alongside it (see `audience-conflicts.md`).

The canonical **four-audience** matrix (Developer / End-user / Agent /
Content-ops) lives in `docs-audit` / `docs-design`
(`references/core/audience-matrix.md`); use it when a decision spans human
and agent audiences at once. Use this excerpt when the agent is the audience
under review.

| Audience | Optimizes for | Needs surfaced as | Common failure |
|---|---|---|---|
| Agent (AX) | Machine readability, deterministic action, context budget, stable contracts, recoverable errors, authority-aware action | Schemas, structured errors, `llms.txt`, markdown pages, context files, examples, tool descriptions, approval surfaces that show real side effects | Ambiguous prose, unstable messages, instructions outside retrievable text, or an approval that hides what the action really does. |

## Transfer rules

- **Shared foundations** (apply to every audience): clear modes, stable URLs,
  docs-as-code, plain language, versioning, accessible structure, and measured
  feedback loops.
- **Modified inheritance** (change shape by audience): code samples, style
  rules, and progressive disclosure.
- **AX-only requirements:** routing descriptions, context-budget choices
  (always-loaded vs load-on-demand vs durable memory; W6), chunk survivability,
  stable machine codes, schema descriptions, enforced forbidden-action gates
  (W3), **authority/trust boundaries** (approval surfaces that show the real side
  effect; deliberate judgment friction where authority is crossed),
  **recoverable errors** (messages that tell the agent how to repair the next
  call), and **task grounding** (intake that makes the agent restate the job,
  workflow, and success criteria before acting).

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
