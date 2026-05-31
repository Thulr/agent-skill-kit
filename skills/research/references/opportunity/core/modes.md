# Modes (Guided Draft / Autopilot / Grill Me)

Elicitation styles for the workflow. Modes set how much the skill asks
before producing artifacts; they do **not** override the load-bearing
rules (cite sources, tag confidence, end every artifact in F/A/D/R,
name kill criteria, fan out sub-agents where the workflow says so).

## Guided Draft (default)

The default for any concrete invocation.

- Skill picks the most likely intent + surface from the user's prompt.
- Skill asks **one blocker question** only when intent or surface is
  ambiguous *and* asking would change which playbook loads.
- Skill drafts the artifact, names confidence on every load-bearing
  claim, and presents the F/A/D/R fold for review.
- User can accept, request a specific revision, or escalate to
  Grill Me for deeper interrogation.

Use this for first-pass investigations, scoping, and decisions where
the user has at least a one-sentence opportunity statement.

## Autopilot

For users who've already done the elicitation work themselves.

- Skill executes the workflow with conservative defaults and does not
  ask blocker questions.
- Skill flags ambiguity in the artifact rather than blocking on it
  ("Assumption: target segment is SMB given the prompt mentions
  'accountants' — flip to enterprise if needed").
- Sub-agents fan out by default (founder + skeptic minimum; all four
  lenses if `investigate` with surface `all`).
- All other gates (F/A/D/R fold, kill criteria, citations, severity /
  confidence tags) remain hard.

Use this when batching multiple opportunities, when a downstream skill
will consume the artifact (`proposal-red-team`, `premortem`), or when
the user has explicitly said "skip the questions."

## Grill Me

For early-stage opportunities or when the user wants the skill to be
the forcing function.

- Skill asks one question at a time before moving to the next phase.
- Each answer is recorded in the artifact's "Inputs" section so the
  user can see the chain of reasoning.
- Skeptic lens dominates by default; founder lens runs as a check on
  the skeptic, not the other way around.
- Useful for pre-investment diligence, pivot calls, and any decision
  with a kill-criterion implication.

Use this when the cost of being wrong is high (irreversible
investment, public commitment, regulatory exposure) or when the user
has explicitly asked to be challenged.

## Mode-switching rules

- Modes are **session-scoped**. Switching mode mid-workflow is fine;
  the skill announces the switch in the artifact.
- The user can re-invoke the skill in a different mode on the same
  opportunity — the artifacts compound, they don't reset.
- The skill **does not** demote a Grill-Me artifact to Autopilot
  silently. If the user says "go faster," the skill confirms once
  before dropping the question loop.

## Bare invocation

When the user invokes the skill without an intent or opportunity
("opportunity research", "validate this idea"), load
`references/starter-scenarios.csv` + `references/intent-router.csv`
and offer the mode choice **before** any other elicitation.
