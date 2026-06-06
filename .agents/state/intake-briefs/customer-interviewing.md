# Intake Brief: customer-interviewing

Saved at `.agents/state/intake-briefs/customer-interviewing.md`. Phase 1 artifact.
Active curator intent: `create-single-layer`.

## Source seed

- Title / creator / URL:
  - *The Mom Test* — Rob Fitzpatrick (2013)
  - *Interviewing Users* — Steve Portigal (2013; 2nd ed. 2023)
  - *Continuous Discovery Habits* — Teresa Torres (2021), customer-interview & weekly-touchpoint chapters only
- One-line of what the source is about: how to talk to customers so you learn
  the truth about their problems instead of collecting polite, biased, or
  hypothetical feedback — planning interviews, asking non-leading questions,
  conducting the conversation, and synthesizing what you heard into evidence.
- Why this source, now: the informed-skills catalog has **no** discovery/interview
  skill; `customer-interviewing` is skill #1 of a new `discovery` family. These
  three books are the canonical, mutually-reinforcing sources on interview craft
  (Fitzpatrick = question hygiene, Portigal = conducting/fieldwork, Torres =
  continuous cadence + synthesis-to-evidence).

## Audience

- Who invokes the skill: PMs, founders, designers, researchers, and agents acting
  on their behalf — early-to-mid practitioners running discovery, not trained
  ethnographers.
- When in their workflow: before/around customer conversations — planning who to
  talk to and why, sanity-checking a question list, steadying themselves to run a
  session, and turning raw notes into shareable insight.
- What they already know: that talking to users matters; they typically do *not*
  know how to avoid leading/pitching/hypothetical questions or how to synthesize
  without cherry-picking confirming quotes.

## Success criteria

- Good first outcome: the agent routes to the right intent (plan vs. fix-questions
  vs. conduct vs. synthesize) and returns concrete, source-grounded moves — e.g.
  rewrites a leading question into a past-behavior question, or produces an
  interview plan with a learning goal + segment + recruiting screen.
- Later signal it helped: fewer "so would you buy this?" questions; interviews
  anchored in real past behavior; synthesis that names disconfirming evidence.
- Signal it's missing/wrong: it generates generic "tips for good interviews"
  rather than diagnosing the specific question/plan/transcript in front of it, or
  it drifts into desk research / usability testing.

## Scope boundaries

- In scope: planning a discovery interview (goal, segment, recruiting/screening);
  critiquing & rewriting interview questions (Mom Test hygiene); conducting the
  conversation (rapport, silence, probing, observation — Portigal); synthesizing
  raw notes into evidence (coding, interview snapshots, opportunity-shaped insight).
- Out of scope: desk/secondary/market research and opportunity go/no-go
  (→ `research`); usability/task testing of an existing interface (→ `ux-audit`);
  survey design; turning insights into an opportunity-solution-tree or roadmap
  (→ future `product-discovery`); persona authoring.
- Neighboring skill NOT to replicate: `research`'s opportunity-validation frame and
  `ux-audit`'s evaluative-testing frame. This skill is **generative, live, 1:1
  qualitative conversation**, not desk research and not interface evaluation.

## Comparable existing skills

(Grepped `skills/*/skill.json`; no catalog skill mentions interview/customer/
discovery — confirmed gap. Closest two:)

- `skills/research/` — source-grounded **desk** research + opportunity validation
  across 14 areas ending in a go/no-go memo. Distinct: customer-interviewing is the
  **live 1:1 conversation craft** that *feeds* discovery; it does not do secondary
  research or render an opportunity verdict. Fence both ways in descriptions.
- `skills/ux-audit/` — heuristic **evaluation** of an existing interface (usability,
  forms, navigation, accessibility). Distinct: that's evaluative testing of a built
  thing; this is generative problem-discovery before/independent of any UI.
- (Prior art, not in this repo) the user's global `~/.agents/skills/` pack has
  `discovery-interview-prep` and `interview-guide-critique` — **ungrounded**, no
  `skill.json`/evals. Concept reference only; author fresh from the books.

## Safety, copyright, sensitive-domain notes

- All three sources are under copyright. Posture: paraphrase concepts into
  operational methods only — **no** chapter summaries, no reproduced question lists/
  scripts/exercises, no distinctive phrasing (e.g. don't reproduce Fitzpatrick's
  exact "rules" verbatim; express the underlying technique in our own words). Run
  the Phase 2 Paraphrase Audit.
- Not a sensitive/regulated domain. One mild ethics note worth a heuristic:
  interviewing involves human subjects — consent, recording permission, and not
  manipulating respondents are in-scope guidance, not a blocker.
- Nothing here changes pack placement or shape.

## Working hypothesis (revised after research)

> _Hypothesis:_ Pack/family = `discovery` (new). Shape = **single-layer**
> (hub-and-spoke) — one intent-router CSV over ~4 orthogonal intents that load
> independently: `prep` (plan: learning goal, segment, recruiting/screening),
> `critique-questions` (diagnose & rewrite leading/pitching/hypothetical questions —
> Mom Test), `conduct` (run the session: rapport, silence, probing, observation —
> Portigal), `synthesize` (code notes → interview snapshots → evidence — Torres).
> Each intent is a single self-contained dimension (no second axis), each needs
> ~200–500 words, and they share a light vocabulary (evidence, past behavior,
> commitment) → single-layer per depth-rubric, not flat (too many distinct
> invocations) and not two-level (no orthogonal second axis). To be confirmed in
> Phase 3 with depth-rubric evidence.

## Gate

> **Phase 1 → Phase 2 gate.** Anything missing or wrong before we research?
> Reply `go` to advance to Phase 2 (Research), or describe what to revise.
