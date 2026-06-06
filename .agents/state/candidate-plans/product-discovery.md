# Candidate Skill Plan: product-discovery

Phase 3 artifact.

## Back-links

- Intake brief: `.agents/state/intake-briefs/product-discovery.md`
- Source dossier: `.agents/state/source-dossiers/product-discovery.md`

## Source

- Cagan (*Inspired*), Torres (*Continuous Discovery Habits*), Perri (*Escaping the Build
  Trap*), Ulwick (*JTBD: Theory to Practice*), Kalbach (*The JTBD Playbook*), Bland &
  Osterwalder (*Testing Business Ideas*), Olsen (*The Lean Product Playbook*).
- Why now: the broad discovery engine of the `discovery` family.

## Recommended Pack Decisions

- Pack tag(s): `discovery` (tags also: product-discovery, jobs-to-be-done,
  opportunity-solution-tree, assumptions, mvp, outcomes). Existing pack (created with
  `customer-interviewing`); this extends the family.

## Draft Skill Candidates

```text
candidate:                  product-discovery
pack:                       discovery
shape:                      single-layer
depth:                      1
action:                     create
public_path:                skills/product-discovery/
dossier_ref:                product-discovery
audience_ref:               product-discovery
shape_decision:
  rubric_evidence:          Q1 = 5 distinct invocations (3–8 → single-layer). Q2 = 1 axis only — "discovery activity/stage"; there is NO orthogonal second axis (the activities are sequential phases, not a surface the same intent crosses), so forcing intent×surface would be the depth-rubric "pretending two axes are three" anti-pattern. Q3 = each leaf 300–500 words. Q4 = shared vocabulary (outcome, opportunity, assumption, evidence) → centralize via one router.
  promotion_path:           Promote to two-level only if a real second axis appears — e.g. B2B vs consumer vs platform contexts each needing distinct content per activity. Split out a sub-skill only if one intent (likely test-assumptions or define-jobs) outgrows ~1500 words.
  axes:                     intent  (frame-outcomes | map-opportunities | define-jobs | test-assumptions | scope-mvp)
  note:                     The approved master plan named "two-level" as a hypothesis and explicitly delegated the final shape to this Phase-3 gate with depth-rubric evidence. Evidence says single-layer. Breadth is honored by ONE skill spanning 7 books, not by routing depth.
anti_pattern_check:
  - one_dim_collapsed:      yes  (5 differentiated rows, ≥3)
  - registry_routes:        yes  (each row loads a distinct playbook; templates differ — frame-outcomes carries none, the other four each carry a distinct artifact)
  - cargo_culting:          yes  (single-layer chosen on content/axis count, and two-level explicitly rejected to avoid a fake axis)
  - bloat_check:            yes  (SKILL.md projected <800 words; each playbook 300–600 < 1500)
  - depth_orthogonality:    N/A  (depth 1, single axis)
playbook_outline:
  - frame-outcomes:
      heuristic_seeds:
        - Reframe an output request ("ship feature X") into an outcome ("move metric M for segment S") tied to the product strategy.
        - Probe the four product risks — value, usability, feasibility, viability — and name which is most uncertain for this bet.
      common_failure_seeds:
        - Feature-factory thinking — counting features shipped as progress.
        - Outcome dogma — shaming legitimately output-shaped work (compliance, platform, table-stakes).
  - map-opportunities:
      heuristic_seeds:
        - Build the tree from a single desired outcome down to opportunities (needs/pains/desires), then candidate solutions, then assumption tests.
        - Keep choices compare-and-contrast across sibling opportunities instead of "should we build this one thing — yes/no."
      common_failure_seeds:
        - Jumping straight to solutions with no opportunity above them.
        - A tree rooted in an output or a vague goal rather than a measurable outcome.
  - define-jobs:
      heuristic_seeds:
        - Map the functional job into solution-free, stable steps, then write desired-outcome statements (direction + metric + object + context).
        - Rank underserved needs by importance vs. satisfaction to find where to focus.
      common_failure_seeds:
        - Writing "jobs" that are really features or solutions in disguise.
        - Treating every stated want as a need without checking importance/satisfaction.
  - test-assumptions:
      heuristic_seeds:
        - List the desirability/viability/feasibility assumptions a bet rests on; plot by importance × evidence; test the riskiest, least-evidenced first.
        - Pick the cheapest experiment that produces real evidence on the assumption, not the most elaborate.
      common_failure_seeds:
        - Testing what is easy or comfortable instead of what is riskiest.
        - Calling a survey/interview "validation" when the assumption needed a behavioral test.
  - scope-mvp:
      heuristic_seeds:
        - Scope the MVP as the smallest test of the value hypothesis, tracing target customer → underserved need → value prop → minimal feature set.
        - Decide build-measure-learn loops and a fit signal before adding scope.
      common_failure_seeds:
        - "MVP" that is just a small v1 with no hypothesis being tested.
        - Skipping target-customer/need clarity and over-building toward assumed fit.
registry_sketch:
  layers:
    - layer: intent-router
      rows:
        - row: frame-outcomes
          loads: references/playbooks/frame-outcomes.md
          notes: Strategy/outcome framing + build-trap diagnosis. No template (reframing in place).
        - row: map-opportunities
          loads: references/playbooks/map-opportunities.md ; templates/opportunity-solution-tree.md
          notes: Opportunity solution tree. Carries the OST template.
        - row: define-jobs
          loads: references/playbooks/define-jobs.md ; templates/jtbd-job-map.md
          notes: Jobs-to-be-done / ODI. Carries the job-map + outcome-statements template.
        - row: test-assumptions
          loads: references/playbooks/test-assumptions.md ; templates/assumption-test-plan.md
          notes: Assumption mapping + experiment selection. Carries the test-plan template.
        - row: scope-mvp
          loads: references/playbooks/scope-mvp.md ; templates/mvp-definition.md
          notes: Lean product process / MVP / PMF. Carries the MVP-definition template.
activation_case_seeds:
  positive:
    - prompt: "We keep shipping features but nothing moves — reframe this roadmap around outcomes." -> route: frame-outcomes
    - prompt: "Help me build an opportunity solution tree for our activation outcome." -> route: map-opportunities
    - prompt: "What job are customers hiring our product for, and which needs are underserved?" -> route: define-jobs
    - prompt: "What's the riskiest assumption behind this bet and how do I test it cheaply?" -> route: test-assumptions
    - prompt: "Scope an MVP that actually tests whether people want this." -> route: scope-mvp
  negative:
    - prompt: "Validate the market size and give me a go/no-go on this opportunity." -> use research because that is sourced desk validation to an F/A/D/R memo, not the team's own discovery reasoning.
    - prompt: "Help me write and run the actual customer interview for this." -> use customer-interviewing because that is live conversation craft, not opportunity/assumption framing.
    - prompt: "Audit our checkout flow for usability problems." -> use ux-audit because that evaluates a built interface.
  edge:
    - prompt: "Turn our discovery into a roadmap we can commit to." -> activates for the outcome/opportunity framing, but sequencing/release planning is general PM, not this skill.
    - prompt: "Is this a good idea?" -> activates only if reframed into an outcome + assumptions to test; otherwise too vague.
grounding_map:
  - source: Inspired, year: 2017
    playbooks: [frame-outcomes, test-assumptions]
    contribution: Outcome over output; the four product risks (value/usability/feasibility/viability) as the risks discovery must reduce.
  - source: Escaping the Build Trap, year: 2018
    playbooks: [frame-outcomes]
    contribution: The build trap / feature factory; product strategy as deployable decisions; the product-kata problem-solving loop.
  - source: Continuous Discovery Habits, year: 2021
    playbooks: [map-opportunities]
    contribution: The opportunity solution tree — outcome → opportunities → solutions → assumption tests.
  - source: Jobs to Be Done Theory to Practice, year: 2016
    playbooks: [define-jobs]
    contribution: Outcome-driven innovation — job mapping, solution-free desired-outcome statements, importance/satisfaction opportunity ranking.
  - source: The Jobs To Be Done Playbook, year: 2020
    playbooks: [define-jobs]
    contribution: Making JTBD actionable — job mapping practice and applying jobs to product decisions.
  - source: Testing Business Ideas, year: 2019
    playbooks: [test-assumptions]
    contribution: Assumptions mapping (desirability/viability/feasibility) and choosing the cheapest experiment for the riskiest, least-evidenced assumption.
  - source: The Lean Product Playbook, year: 2015
    playbooks: [scope-mvp]
    contribution: The lean product process and product-market-fit pyramid — target customer → underserved needs → value prop → MVP → test.
reason:                     The broad discovery engine; consolidates 7 canonical sources into one fenced skill that turns a request into framed outcomes, mapped opportunities, defined jobs, tested assumptions, and a scoped MVP.
inspired_by:                [inspired, continuous-discovery-habits, escaping-the-build-trap, jtbd-theory-to-practice, jtbd-playbook, testing-business-ideas, lean-product-playbook]
```

## Anti-pattern self-check (rubric walk)

- [x] No CSV layer has fewer than 3 differentiated rows. (5)
- [x] No registry layer whose rows all load the same files. (5 distinct playbooks; 4 distinct templates + 1 none)
- [x] SKILL.md projected <800 words; no playbook projected >1500. (300–600 each)
- [x] Depth ≥2 orthogonality — N/A.
- [x] Every `grounding_map.playbooks` non-empty. (all 7 sources → ≥1; all 5 intents covered)
- [x] Every negative names a sibling skill. (research, customer-interviewing, ux-audit)
- [x] Every playbook has ≥2 heuristic seeds and ≥1 common-failure seed.

## Review Handoff (filled at end of Phase 5)

- Draft paths: `skills/product-discovery/` (SKILL.md, skill.json, references/intent-router.csv, 5 playbooks, 4 templates, evals/*); README regenerated.
- Known risks: (1) shape changed from the master plan's "two-level" hypothesis to single-layer — documented with depth-rubric evidence (no orthogonal 2nd axis; two-level would be a fake-axis anti-pattern). (2) Broadest skill in the family (7 sources) — boundary with `research` (opportunity validation), `customer-interviewing` (interview craft), and general roadmap PM relies on description fencing + negative cases. (3) `frame-outcomes` deliberately carries no template (reframing in place) — differentiates router rows.
- Suggested reviewer focus: confirm single-layer is right (vs. splitting define-jobs/test-assumptions into siblings); fencing strength vs `research`; that no reproduced ODI worksheets / 44-experiment catalog leaked.
- Validation report: `.agents/state/validation-reports/product-discovery-phase5.md` (validator exit 0; per-skill static check pass).
