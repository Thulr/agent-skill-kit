# Tool Descriptions Playbook

## Scope

A tool or MCP-server description is agent-facing documentation: it reaches the
model before any human reads it, and the model decides whether and when to call
the tool from that description alone. This surface covers the *clarity* of that
readable description — does it state what the tool does, when to use it, and
when not to — so an agent routes to the right tool. It does not cover the typed
schema (parameter types, required fields, return shape) as code; that contract
is owned by `agent-dx`. Here the unit of work is prose the model reads, not the
signature it binds against.

- **In:** writing and reviewing tool/MCP descriptions for trigger clarity;
  disambiguating near-identical tools so the agent stops choosing the wrong one;
  applying the purpose / use-conditions / near-miss-exclusion test; deciding
  whether a routing failure is a description fix or a tuning problem.
- **Out:** the typed parameter/return schema and its validation (`agent-dx`);
  measuring a description's effect on tool-selection accuracy with an eval set
  (`agent-test`); generic human-facing API docs and reference pages
  (docs-audit / docs-design own those); repo gates and hooks
  (`harden-repo-for-coding-agents`).
- **Intents this surface answers:** do, review, design.

## Grounding

- A tool description is a trigger description in the progressive-disclosure
  sense: metadata (name + description) is always loaded into the model's tool
  list, while the full behavior runs only on call. Because the description is
  the always-loaded part, it must carry the routing decision by itself — the
  body of the tool never gets read until after the model has already chosen.
- Public agent conventions — MCP server/tool descriptions, OpenAPI `summary`
  and `description` fields, function-calling tool specs — all expose a free-text
  description distinct from the typed schema. That free text is the lever this
  playbook tunes; the schema is `agent-dx`'s.
- More description is not strictly better. An untargeted description (padded
  with caveats, history, or overlapping language) can *regress* tool-selection
  behavior — the model over- or under-triggers. Tune wording against observed
  routing, not by adding words.
- When two tools have overlapping descriptions, the agent picks one
  semi-arbitrarily and the wrong call looks like a model failure when it is a
  documentation collision. The fix is disambiguation in the descriptions, not a
  stronger prompt.

## Good signals

- Each description states **purpose** (what the tool does in one high-signal
  line), **use conditions** (when the agent should reach for it), and
  **near-miss exclusions** (the adjacent situation where it should *not*).
- Near-identical tools name each other in their exclusions ("for X use
  `other_tool`"), so an agent comparing the two has an explicit tiebreaker.
- The opening clause is the highest-signal summary — it reads correctly even if
  truncated in a crowded tool list, and survives as a standalone chunk.
- Descriptions define their own terms and avoid anaphora ("this resource", "see
  above"); each one is legible without the surrounding tool list.
- Description changes are justified by a measured shift in tool-selection
  accuracy, not by intuition that "more detail helps."
- Under-triggering is treated as a description-tuning task first — the wording is
  sharpened before any new tool or body content is added.
- The description is written for the model as reader: concrete trigger phrases an
  agent's query would match, not marketing or internal jargon.

## Common failures

- **Schema-as-description.** The description just restates parameter names and
  types; it says *how to call* the tool but never *when to* — so the model has
  no routing signal. (The schema is `agent-dx`'s job; the description's job is
  the decision.)
- **Overlapping twins.** Two tools carry near-identical descriptions, the agent
  calls the wrong one, and it is misread as a model error rather than a
  documentation collision.
- **No exclusions.** The description states purpose and use conditions but never
  the near-miss it should decline, so the tool over-triggers into adjacent
  requests it shouldn't handle.
- **Description bloat.** Caveats, history, and edge cases pad the description
  until the trigger signal is buried; selection accuracy regresses even though
  the text is "more complete."
- **Body-first reflex.** An under-triggering tool gets more body content or a
  louder system prompt while the always-loaded description — the only part that
  drives routing — is left vague.
- **Chunk amnesia.** The description leans on anaphora or a prior tool's context
  ("like the above, but…"), so it is unreadable once isolated in the tool list.
- **Docs-as-routing-guarantee.** A sharpened description is treated as a hard
  guarantee the agent will route correctly; it raises *average* selection
  accuracy, not a worst-case floor. A genuine must-not-call invariant belongs in
  a deterministic gate, not in prose the model may still ignore.

## Heuristics

- **(do, review) Apply the trigger-description test to every tool.** Confirm the
  description states purpose, use conditions, and at least one near-miss
  exclusion. If any of the three is missing, the description is incomplete
  regardless of length.
- **(do, design) Lead with the highest-signal summary.** Put what the tool does
  and when to use it in the first clause, so it routes correctly even when the
  tool list is truncated or crowded.
- **(review, design) Disambiguate overlapping tools by cross-naming.** When two
  descriptions could both match a query, have each name the other in its
  exclusions ("for X, use `other_tool`") so the agent has a deterministic
  tiebreaker.
- **(review) Read a wrong-tool call as a description defect first.** Before
  blaming the model or the prompt, diff the descriptions of the two candidate
  tools; near-identical wording is the likely cause and the cheapest fix.
- **(do, review) Tune the description before adding body.** When a tool
  under-triggers, sharpen the wording first; only add body content or a new tool
  if the tuned description still misses. Description is the always-loaded lever.
- **(review, design) Treat more text as a possible regression.** Cut padding,
  history, and stacked caveats; an untargeted description can lower selection
  accuracy. Shorter-and-targeted beats longer-and-complete.
- **(do, design) Write self-contained, anaphora-free descriptions.** Define local
  terms, avoid "this/above/see," and make each description legible as a
  standalone chunk in a flat tool list.
- **(design) Keep must-not-call invariants out of prose.** If a tool must never
  fire in some state, enforce it with a deterministic gate or guard, not a
  description the model may override.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does the description state purpose, use conditions, and a near-miss exclusion? | No routing signal — model guesses when to call | Rewrite to the trigger-description test |
| Do overlapping tools cross-name each other in exclusions? | Agent calls the wrong twin | Add "for X use `other_tool`" to each |
| Is the highest-signal summary in the first clause? | Trigger buried; truncation breaks routing | Front-load purpose + use condition |
| Is each description legible in isolation (no anaphora)? | Chunk amnesia in the tool list | Define terms inline; drop "this/above" |
| Was the last description change checked against selection accuracy? | Bloat may have regressed routing | Measure via `agent-test`; cut untargeted text |
| Is an under-triggering tool being fixed by tuning the description first? | Body-first reflex leaves the real lever vague | Sharpen wording before adding body |

## Cross-references

- `machine-reference.md` — the structured reference (llms.txt-style) an agent
  fetches *after* a tool routes it somewhere; this surface owns the routing
  decision, that one owns the destination content.
- `agents-md.md` — the always-loaded repo contract; tool descriptions and
  AGENTS.md share the progressive-disclosure budget covered in
  `context-budget.md`.
- `llms-txt.md` — the curated index; a tool description points to a live action,
  an llms.txt entry points to retrievable reference.
- → `agent-dx` for the typed tool **schema** as code (parameter types, required
  fields, return shape) — this playbook owns the description's clarity, not the
  signature it binds against.
- → `agent-test` for **eval-improving** a description: measure tool-selection
  accuracy against a labeled query set before and after a wording change, so
  tuning is grounded rather than intuited.
- `references/core/severity-rubric.md`, `references/core/score-rubric.md` —
  REVIEW scales; finding IDs `AGENT-DOC-TOOL-NNN`.
- `references/intents/{do,review,design}.csv` row `tool-descriptions` — the
  entry points.