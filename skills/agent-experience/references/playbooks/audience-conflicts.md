# Audience Conflicts Playbook (AX-first)

## Scope

Covers cases where a documentation or interface choice that serves a **human**
audience harms the **agent** audience, or vice versa: human prose vs machine
structure, in-product help vs retrievable text, conversational voice vs
structured fields, and always-loaded vs load-on-demand agent context. Use when a
proposed AX improvement would make a human surface worse, or a human-facing fix
would hide load-bearing facts from agents.

- In: tooltip/text conflicts, voice vs structured fields, maximal vs minimal
  agent context, plain language vs technical precision, pull-help vs always-on
  guidance, single-source vs forked human/agent docs.
- Out: pure single-audience quality (use the relevant surface playbook); the full
  **four-audience** treatment including Content-ops (use the `docs-audit` /
  `docs-design` `audience-conflicts.md`, which this file is the AX-first cut of).
- Intents this surface answers: audit, design, debug.

## Grounding

- Research Report — Effective Documentation Patterns for DX, AX, and UX (Informed
  Skills synthesis, 2026) — the conflict set and shared/modified/unique
  inheritance model.
- Evaluating repository-level context files for coding agents (Mündler et al.,
  ETH/LogicStar, 2026) — the caution against maximal always-loaded context.
- Cloudflare documentation for AI tooling (2026) — single-source,
  multiple-rendering for humans and agents.

## Good signals

- The output names the audience that benefits and the audience that is harmed
  before proposing a fix.
- Load-bearing content has a human-visible path **and** a machine-readable path.
- One canonical source feeds multiple renderings, or forked sources have explicit
  drift checks.
- Technical terms are preserved where precision matters and explained where they
  block comprehension.
- Agent-context choices are measured against task success and cost, not intuition.

## Common failures

- Average-audience compromise — too vague for agents, too technical for end
  users, too verbose for developers.
- Tooltip-only truth — critical rules help sighted mouse users but disappear for
  keyboard/touch/screen-reader users and agents.
- Voice over contract — warm prose hides parameters, constraints, return shape, or
  next action.
- Context hoarding — every observed agent failure adds lines to an always-loaded
  file instead of a targeted resource, hook, schema, or eval (W6). More context can *lower* task
  success regardless of where it loads: irrelevant tokens alone collapse scores while output stays
  fluent (context rot), so curating retrieval sources (excluding promotional/SEO noise) is itself an
  AX decision.
- Fork without drift control — human docs and agent docs diverge until one is wrong.

## Heuristics

- (audit, design) **Name the trade-off** — state which audience benefits, which is
  harmed, and what evidence would show the harm is real.
- (design, debug) **Visible plus machine-readable** — keep the human affordance,
  but duplicate load-bearing facts in text, schema, aria/semantic structure,
  markdown, or examples that agents and assistive tech can read.
- (design) **One source, many renderings** — prefer canonical content rendered as
  page, markdown, in-product hint, schema description, or bundle over independently
  maintained human/agent forks.
- (audit, design) **Precision with explanation** — preserve exact API verbs, error
  codes, field names, and dangerous-action terms, then explain them in plain
  language rather than replacing them.
- (debug, measure) **Smallest context that completes the task** — the budget question is *how
  little* context still completes the task, not how much fits. Test always-loaded vs load-on-demand
  vs schema/tool descriptions separately, and prefer noise exclusion (curated sources over open-web
  dumps): adding context can hurt via context rot even when the placement is right.
- (audit) **No hidden criticals** — irreversible consequences, required fields,
  retry safety, auth scopes, and version applicability must never live only in
  hover, screenshots, or prose outside the action surface.

## Quick diagnostic

- Does a proposed AX improvement reduce access for a human audience? yes → design
  a dual path; no → use the relevant single-surface playbook.
- Is there one canonical fact source? yes → add renderings; no → choose one or add
  drift gates.
- Would an agent or assistive tech see the same rule a human sees? yes → test
  clarity; no → surface it as text/schema.
- Did context grow after a failure? yes → ask whether a better trigger, schema,
  hook, example, or eval would solve it with less always-loaded text.

## Cross-references

- `references/core/audience-matrix.md` — AX excerpt + conflict rule.
- `references/playbooks/ax-docs.md` — context budget and retrieval patterns.
- `docs-audit` / `docs-design` — the full four-audience matrix and the
  Content-ops audience, plus human-only surfaces (`ux-help`, `dx-docs`).
