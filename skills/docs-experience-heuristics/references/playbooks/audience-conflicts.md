# Audience Conflicts Playbook

## Scope

Covers cases where the documentation optimum for one audience harms another:
DX vs UX vs AX, human prose vs machine structure, in-product help vs retrievable
text, generated reference vs curated explanation, and always-loaded vs
load-on-demand agent context. Use whenever a recommendation would make one
audience worse.

- In: tooltip/text conflicts, conversational voice vs structured fields,
  maximal context vs minimal context, plain language vs technical precision,
  generated vs hand-written docs, pull-help vs always-on guidance, and
  single-source vs forked human/agent docs.
- Out: single-audience quality problems that do not create trade-offs; use the
  relevant surface playbook instead.
- Intents this surface answers: audit, design, debug.

## Grounding

- Research Report — Effective Documentation Patterns and Practices for DX, AX,
  and UX (Informed Skills research synthesis, 2026) — supplies the conflict set
  and the shared/modified/unique inheritance model.
- Agent Skills overview (Anthropic, 2025) — grounds progressive disclosure and
  load-on-demand agent resources.
- Evaluating repository-level context files for coding agents (Gloaguen and
  coauthors, 2026) — grounds the caution against maximal always-loaded context.
- Help and Documentation (Nielsen Norman Group) — grounds contextual human help
  and pull-style guidance.
- Cloudflare documentation for AI tooling (Cloudflare, 2026) — provides a
  single-source, multiple-rendering pattern for humans and agents.
- Information Architecture: For the Web and Beyond (Rosenfeld, Morville, and
  Arango, 2015) — grounds navigation/search trade-offs.

## Good signals

- The output names primary, secondary, and harmed audiences before proposing a
  fix.
- Load-bearing content has a human-visible path and a machine-readable path.
- One canonical source feeds multiple renderings, or forked sources have explicit
  drift checks.
- Technical terms are preserved where precision matters and explained where they
  block comprehension.
- Agent context choices are measured against task success and cost, not intuition.

## Common failures

- Average-audience compromise — the recommendation is too vague for agents, too
  technical for end users, and too verbose for developers.
- Tooltip-only truth — critical rules help sighted mouse users but disappear for
  keyboard users, touch users, screen readers, and agents.
- Voice over contract — warm prose hides parameters, constraints, return shape,
  or next action.
- Context hoarding — every observed agent failure adds lines to an always-loaded
  file instead of a targeted resource, hook, schema, or eval.
- Fork without drift control — human docs and agent docs diverge until one is
  wrong.

## Heuristics

- (audit, design) Name the trade-off — state which audience benefits, which is
  harmed, and what evidence would show the harm is real.
- (design, debug) Visible plus machine-readable — keep the human affordance when
  useful, but duplicate load-bearing facts in text, schema, aria/semantic
  structure, markdown, or examples that agents and assistive tech can read.
- (design) One source, many renderings — prefer canonical content rendered as
  web page, markdown, in-product hint, schema description, or bundle over
  independently maintained human/agent forks.
- (audit, design) Precision with explanation — preserve exact API verbs, error
  codes, field names, and dangerous-action terms, then explain them in plain
  language rather than replacing them.
- (audit, debug) Generated-plus-curated split — let schemas eliminate drift for
  facts; add curated explanation, examples, and task paths where generated docs
  lack why or context.
- (debug, measure) Load-placement experiment — test always-loaded context,
  load-on-demand resources, and schema/tool descriptions separately. Keep the
  smallest surface that improves task success without disproportionate cost.
- (audit, design) Help promotion rule — content that repeatedly appears in a
  failed task path should move closer to the task, unless doing so hides it from
  another audience; then add dual rendering.
- (audit) No hidden criticals — irreversible consequences, required fields,
  retry safety, auth scopes, and version applicability must never live only in
  hover, screenshots, or prose outside the action surface.

## Quick diagnostic

- Does a proposed improvement reduce access for another audience? yes → design a
  dual path; no → use the relevant single-surface playbook.
- Is there one canonical fact source? yes → add renderings; no → choose one or
  add drift gates.
- Would an agent or assistive tech see the same rule a human sees? yes → test
  clarity; no → surface it as text/schema.
- Did context grow after a failure? yes → ask whether a better trigger, schema,
  hook, example, or eval would solve it with less always-loaded text.

## Cross-references

- `references/core/audience-matrix.md` — shared conflict vocabulary.
- `references/playbooks/ux-help.md` — hidden help, onboarding, and in-product
  guidance.
- `references/playbooks/ax-docs.md` — context budget and retrieval patterns.
- `references/playbooks/api-contracts.md` — structured fields and operational
  metadata.
- `references/playbooks/foundations.md` — single source of truth and IA.
