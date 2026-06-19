# Activation Evals Playbook

## Scope

The meta-surface: designing evals for whether an *agent or skill activates and
routes correctly* — not whether its output is good once invoked, but whether it
fires on the prompts it should, stays silent on the prompts it should not, and
wins disambiguation against its siblings. This is the surface that designs and
audits trigger-evals-style activation contracts: the positive / negative / edge
case sets, the routing-decision grader, and the re-run discipline that fires
whenever a prompt, skill body, or description changes. You design the
instrument; an operator runs it (see `agent-ops`).

- **In:** positive/negative/edge trigger-case design; false-activation vs
  missed-activation as distinct, separately-budgeted failures; disambiguation
  cases against sibling skills/tools; grading the routing *decision* (which
  skill/tool, with what args) not just the downstream answer; eval-on-change
  triggers when a description or skill body is edited.
- **Out:** designing output/quality evals for the invoked behavior
  (`eval-design`); judge calibration mechanics (`judge-calibration`); run-level
  path grading once invoked (`trajectory-tests`); release/model-swap gates
  (`benchmark-design`); operating the loop or watching drift (`agent-ops`).
- **Intents this surface answers:** do, review, design.

## Grounding

- An activation eval grades a *routing decision*: given a prompt, did the right
  skill/tool fire, with the right args, and did the wrong ones stay quiet?
  Output quality is a separate axis — a skill can activate correctly and still
  answer badly, and the activation eval must not conflate the two.
- False activation (fires when it should not) and missed activation (silent when
  it should fire) are distinct failure modes with distinct costs and distinct
  fixes; collapsing them into one accuracy number hides which way the
  description is mis-tuned. Treat them like precision and recall on the trigger.
- The trigger surface is the natural-language description, not the body. When the
  description, name, or a sibling's description changes, the activation contract
  may silently shift — activation evals are re-run on that change, the way a unit
  suite re-runs on a code change.
- Disambiguation is the hard case: a prompt that plausibly fits two siblings
  must route to the intended one. Cases that only test a skill in isolation never
  exercise the boundary where real mis-routing happens.

## Good signals

- The case set has explicit positive, negative, and edge categories, each tagged,
  with a non-zero margin above any minimum count rather than the bare floor.
- False activation and missed activation are reported as separate rates with
  separate thresholds, not folded into one pass-rate.
- Disambiguation cases pit the skill against each near-neighbor sibling by name,
  and assert the *expected route*, not merely "something activated."
- The grader checks the routing decision (selected skill/tool + args) against an
  expected route, and `null` when nothing should fire — a deterministic match
  where the route is checkable, not an LLM judge.
- Negative cases include near-miss prompts that share vocabulary with the trigger
  but should not fire, not just obviously-unrelated prompts.
- Activation evals are wired to re-run on any edit to a name, description, or
  sibling description — the contract is version-pinned to the trigger surface.
- Edge cases capture ambiguous, multi-intent, and adversarial-phrasing prompts
  where the correct route is debatable and the expected answer is documented.

## Common failures

- **Output-Grading the Trigger.** The eval scores the answer the skill produced,
  so a wrong skill that happened to give a plausible answer passes — the routing
  decision is never graded.
- **Single-Accuracy Collapse.** False and missed activation are averaged into one
  number; a description that over-fires and one that under-fires look identical,
  and neither fix is indicated.
- **Isolation-Only Cases.** Every case tests one skill alone, so the suite is
  green while two siblings fight over the same prompts in production — the
  disambiguation boundary is untested.
- **Friendly Negatives.** Negative cases are all obviously-unrelated prompts, so
  the suite never catches the near-miss vocabulary overlap that causes real false
  activation.
- **Stale Contract.** The description is edited but activation evals are not
  re-run, so a routing regression ships silently — the unit-test-on-change
  discipline is missing for the trigger surface.
- **Bare-Floor Set.** The case count sits exactly at the schema minimum with zero
  margin, so one retired case drops the suite below contract.
- **God Gate on Activation.** A single aggregate activation pass-rate gates the
  skill, hiding whether the regression is a guardrail (must-not-fire) or a
  capability (nice-to-fire) slice.
- **Skeleton Cases.** Cases are one-line keyword stubs, not realistic prompts
  with the surrounding intent — they test substring matching, not activation.

## Heuristics

- **(do, design) Grade the route, not the reply.** Assert the selected skill/tool
  and args against an expected route (and `null` when nothing should fire). If
  the route is deterministically checkable, use a deterministic check, never a
  judge — a judge here is unnecessary attack surface.
- **(design, review) Split false from missed activation.** Report two rates with
  two thresholds. A merged accuracy number tells you the trigger is wrong but not
  which direction to correct, so it cannot drive a fix.
- **(do, design) Write disambiguation cases by sibling name.** For each
  near-neighbor skill, author a prompt that plausibly fits both and assert the
  intended route. Isolation-only suites never exercise the boundary that breaks.
- **(design) Make negatives near-misses, not strangers.** Seed negative cases
  with prompts that share the trigger's vocabulary but should stay silent;
  obviously-unrelated prompts prove almost nothing about precision.
- **(do, review) Re-run on every trigger-surface edit.** Treat the description,
  name, and sibling descriptions as the unit under test; wire activation evals to
  re-run whenever any of them changes, or the contract silently rots.
- **(review, design) Keep a non-zero margin above the floor.** The actual case
  count must exceed the schema minimum with slack; sitting at the floor means one
  retired case breaks contract.
- **(review) Decompose the activation gate by slice.** Tag must-not-fire cases as
  guardrail and nice-to-fire as capability; block on a guardrail regression,
  report-only on a capability dip. Never gate on one aggregate activation number.
- **(do, review) Reject skeleton cases.** Every case is a realistic prompt with
  its surrounding intent, not a keyword stub — a stub tests substring matching,
  not activation, and certifies nothing.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does the eval grade the selected route + args, not the output? | Output-grading the trigger lets the wrong skill pass | Assert expected route (and `null`); deterministic check |
| Are false and missed activation reported separately? | Single-accuracy collapse hides which way to fix | Split into two rates with two thresholds |
| Are there disambiguation cases naming each sibling? | Isolation-only suite misses real mis-routing | Add same-prompt-two-siblings cases with expected route |
| Are negatives near-miss prompts, not strangers? | Friendly negatives never catch false activation | Seed vocabulary-overlapping must-not-fire cases |
| Do activation evals re-run on description/sibling edits? | Stale contract ships a routing regression | Wire eval-on-change to the trigger surface |
| Is the case count above the schema floor with margin? | One retired case breaks contract | Add cases until a non-zero margin exists |
| Is the activation gate decomposed into guardrail vs capability? | God gate hides which slice broke | Tag and gate per slice |

## Cross-references

- `eval-design` — the sibling that designs output/quality evals for the behavior
  *once it has activated*; this surface stops at the routing decision.
- `judge-calibration` — invoke when an activation edge case genuinely needs a
  judge (ambiguous intent not deterministically checkable); a judge is
  trustworthy only once calibrated against a human-labeled set.
- `trajectory-tests` — once the right skill activates, grade the multi-step path
  it runs; activation is the entry condition, trajectory is the run.
- `benchmark-design` — the held-out, baseline-and-rollback gate that a tuned
  activation contract feeds into for a release or model swap.
- → `agent-ops` for the hand-off: this surface designs the activation eval;
  `agent-ops` runs it and watches activation drift in production.
- `references/core/severity-rubric.md`, `references/core/score-rubric.md` —
  REVIEW scales; finding IDs `AGENT-TEST-ACT-NNN`.
- `references/intents/{do,review,design}.csv` row `activation-evals` — the entry
  points.