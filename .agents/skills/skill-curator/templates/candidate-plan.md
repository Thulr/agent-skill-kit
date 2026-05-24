# Candidate Skill Plan

Saved at `.agents/state/candidate-plans/<plan-slug>.md`. This is the
**Phase 3 artifact** — the gate between research and any file write.
Curator must present this plan and wait for explicit user approval
before Phase 4 (Scaffold).

## Back-links

- Intake brief: `.agents/state/intake-briefs/<intake-slug>.md`
- Source dossier: `.agents/state/source-dossiers/<source-slug>.md`

## Source

- Title and creator:
- Why this source is being curated now (1 line):

## Recommended Pack Decisions

- Pack tag(s) used:
- New pack created? If yes, justify per `references/pack-placement-rubric.md`:

## Draft Skill Candidates

One block per candidate. Every field is required.

```text
candidate:                  # skill slug
pack:                       # capability pack tag (not a directory)
shape:                      # flat | single-layer | two-level
action:                     # create | extend-existing | reference-only
public_path:                # skills/<slug>/ (or path being extended)
dossier_ref:                # back-link to dossier slug
audience_ref:               # back-link to intake brief slug
shape_decision:
  rubric_evidence:          # which depth-rubric question(s) justified the shape
  promotion_path:           # what would later cause promotion to a deeper shape
anti_pattern_check:         # walk references/depth-rubric.md anti-patterns
  - one_dim_collapsed:      # for two-level: both axes have >=3 values? yes/no
  - registry_routes:        # for single-layer/two-level: rows differ on what they load? yes/no
  - cargo_culting:          # picked shape because of content, not prestige? yes/no
  - bloat_check:            # SKILL.md projected to stay within shape's word cap? yes/no
playbook_outline:           # for single-layer / two-level
  - <playbook-slug>:
      heuristic_seeds:
        - <seed 1>
        - <seed 2>
      common_failure_seeds:
        - <seed 1>
        - <seed 2>
registry_sketch:            # for shapes with a registry
  rows:
    - intent: <intent>
      detail_file: <path>
      templates: <paths>
      notes: <how this row differs from the others>
activation_case_seeds:
  positive:                 # >= 3 (flat/single-layer), >= 10 (two-level)
    - prompt: "<...>" -> route: <intent / surface>
  negative:                 # >= 3 (flat/single-layer), >= 8 (two-level)
    - prompt: "<...>" -> use sibling: <skill-slug> because <reason>
  edge:                     # >= 1
    - prompt: "<...>" -> activates only if <condition>
grounding_map:              # for each inspired_by source, which playbooks
  - source: <name>, year: <year>
    playbooks: [<playbook-slug>, <playbook-slug>]
    contribution: <one-line paraphrase of what the source contributes>
reason:                     # why this candidate is worth shipping
inspired_by:                # short list of source slugs (full metadata in skill.json later)
```

## Reference Additions

References that should land in other skills (not in this candidate)
or in `skills/_shared/`. Each entry names the target skill and the
file added.

- Target: `<existing-skill>`. Add: `<file>`. Reason:

## Anti-pattern self-check (rubric walk)

Curator confirms — yes/no — for each candidate above:

- [ ] No two-level candidate has a dimension with <3 values.
- [ ] No single-layer candidate has a registry whose rows all load
      the same files.
- [ ] No flat candidate's SKILL.md is projected over 800 words.
- [ ] Every `playbooks: []` in `grounding_map` is non-empty.
- [ ] Every negative activation case names a specific sibling skill.
- [ ] Every playbook in `playbook_outline` has ≥2 heuristic seeds and
      ≥1 common-failure seed.

If any box is unchecked, the plan is not ready for the gate — fix
or remove the candidate.

## Review Handoff (filled at end of Phase 5)

- Draft paths:
- Known risks:
- Suggested reviewer focus:
- Validation report: `.agents/state/validation-reports/<timestamp>.md`

## Gate

Curator: present this plan to the user and ask:

> "Approve the plan, or revise? Reply with `go` to advance to Phase 4
> (Scaffold). Any rejection sends us back to Phase 2 (Research) or
> Phase 1 (Intake) depending on the reason."

This is the critical gate. Once approved, scaffolding is mechanical —
the curator may not write any file outside `public_path` without
re-opening Phase 3.
