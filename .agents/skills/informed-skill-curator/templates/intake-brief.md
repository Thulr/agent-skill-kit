# Intake Brief: <skill working title>

Saved at `.agents/state/intake-briefs/<intake-slug>.md`. This is the
**Phase 1 artifact**: it captures what the user wants before any
research starts. The skill-curator must present this brief and wait
for explicit user confirmation before moving to Phase 2 (Research).

## Source seed

- Title / creator / URL:
- One-line of what the source is about:
- Why this source, now:

## Audience

- Who invokes the skill (role, expertise level):
- When in their workflow they reach for it:
- What they already know (so the skill does not over-explain):

## Success criteria

- What does a good outcome look like the first time this skill fires?
- How would we know later that the skill helped?
- What user behavior would tell us it's missing or wrong?

## Scope boundaries

- In scope (what this skill must handle):
- Out of scope (what is deliberately left to other skills / the user):
- What neighboring skill should *not* be replicated:

## Comparable existing skills

List 2–3 closest existing skills in this repo. Curator must `grep` /
inspect to fill this; do not skip. The point is forced de-duplication.

- `skills/<existing-1>/` — what it covers, why this candidate is distinct:
- `skills/<existing-2>/` — what it covers, why this candidate is distinct:
- `skills/<existing-3>/` — what it covers, why this candidate is distinct:

## Safety, copyright, sensitive-domain notes

- Source under copyright? What's the paraphrase / non-substitution posture?
- Sensitive domain (therapy-adjacent, medical, legal, security)?
- Anything that would change pack placement or shape choice?

## Working hypothesis (revised after research)

One paragraph: best current guess at the skill's **pack tag**,
**shape** (flat / single-layer / two-level), and **primary intents**.
Mark as a guess — Phase 2 (research) and Phase 3 (plan) may revise it.

> _Hypothesis:_

## Gate

Curator: present this brief to the user and ask:

> "Anything missing or wrong before we research? Reply with `go` to
> advance to Phase 2 (Research), or describe what to revise."

Do **not** advance until the user confirms. In Autopilot mode, this
gate is soft only for routine flat skills with at least one strong
comparable; it is hard for novel packs, novel shapes, or two-level
candidates.
