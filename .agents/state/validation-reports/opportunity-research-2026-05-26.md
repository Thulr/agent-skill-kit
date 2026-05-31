# Validation Report — opportunity-research — 2026-05-26

- Skill: `skills/opportunity-research/`
- Shape: two-level (intent × research-area)
- Source dossier: `.agents/state/source-dossiers/opportunity-research-taxonomy.md`
- Candidate plan: `.agents/state/candidate-plans/opportunity-research.md`
- Curator: claude opus 4.7 (1M context)

## Deterministic validator

`scripts/validate-generated-skill.py skills/opportunity-research/`

```
## note (1)
- [note] shape detected — skills/opportunity-research — running checks for shape=two-level
```

**0 blocking, 0 warning, 1 note (informational).**

## Per-skill static check

`bash skills/opportunity-research/evals/run-static-checks.sh`

```
opportunity-research static eval passed.
```

## LLM self-review (Explore agent against two-level rubric)

### Blocking (0)

None.

### Warning (1)

- **Pseudo-intent playbooks below 1000-word target.** `synthesize.md`
  (841 words) and `decide.md` (904 words) are below the 400–1500
  range typical for surface playbooks. Acceptable here because they
  consolidate / fold across the 14 area playbooks rather than
  carrying their own deep-research load. No action.

### Note (3)

- **Positive activation cases skew toward `investigate` intent.** 14
  of 18 positive cases route to `investigate/*`; 1 scope, 1
  synthesize, 2 decide. Coverage still exceeds rubric minimums (4
  intents covered, 15 surfaces covered). Distribution is
  intentional — `investigate` is the largest user-facing surface and
  the only intent that fans out.
- **Grounding uses both surface slugs and `<intent>-intent` markers.**
  21 `inspired_by` sources collectively reference 16 surface
  playbooks plus the `scope-intent` / `synthesize-intent` /
  `decide-intent` markers. Internally consistent and rubric-allowed
  (validator's `accepted_slugs` includes both forms).
- **Playbook "Common failures" sections are concrete and load-bearing.**
  Sampled 5 across areas (market, customer, technical, legal, risk):
  all name mechanisms, not vague warnings. No action.

## Rubric coverage summary

| Rubric area | Result |
|---|---|
| Required artifacts | All present |
| Dimension orthogonality (≥3 values per axis, materially different routing) | ✓ |
| Registry integrity (all paths resolve) | ✓ |
| Playbook content (canonical sections, intent-tagged heuristics, word band) | 16 / 16 playbooks conform |
| SKILL.md (under 1200 words, both registries consulted, dispatch referenced) | 998 words, ✓ |
| Activation cases (≥10 positive, ≥8 negative-with-sibling, ≥1 edge) | 18 / 16 / 3 |
| Grounding (object-array `inspired_by`, non-empty `playbooks[]`) | 21 sources, all populated |
| Anti-patterns (Cartesian smell, hardcoded surfaces, detail in SKILL.md) | None detected |
| Static check + just check | Skill-level: passes; repo-level: pre-existing BMAD-skills failures unrelated to this work |

## Overall verdict

**READY for `informed-skill-reviewer` handoff.**

Recommended reviewer focus:

1. **Pseudo-playbook lane.** Confirm the convention of putting
   `synthesize.md` and `decide.md` under `references/playbooks/`
   (treating them as "intent-pseudo playbooks" routed from
   non-area-keyed intent CSVs) is acceptable, or split them into a
   separate directory.
2. **Source-safety on legal / financial templates.** The "this is
   not legal advice / not investment advice" markers are present in
   `templates/artifacts/legal-register.md` and
   `templates/artifacts/unit-economics.md`. Verify wording is
   strong enough.
3. **Sub-agent fan-out cap.** `subagent-dispatch.md` defaults to a
   6-area first-pass subset for `surface = all`. Confirm that
   default is conservative enough (vs. 14-agent fan-out being the
   named failure mode from the source).
4. **Cross-skill non-collision.** Negative activation cases name 13
   sibling skills (morphological-analysis, scamper, novel-ideation,
   proposal-red-team, plan-red-team, premortem,
   interview-guide-critique, persona-critique, clean-architecture,
   dx-heuristics, ux-accessibility-heuristics, validation-context,
   tradeoff-analysis, metric-sanity-check, survey-question-review).
   Confirm no skill in this set is missed where it should be a
   sibling-route.

## Files written under `skills/opportunity-research/`

```
SKILL.md                                                998 words
skill.json                                              21 inspired_by sources
references/intent-router.csv                            4 intents
references/intents/{scope,investigate,synthesize,decide}.csv  4 files
references/playbooks/{14 areas + synthesize + decide}.md      16 files
references/core/{severity,confidence}-rubric.md         2 files
references/core/{fadr-framework,personas,decision-gates,modes}.md  4 files
references/subagent-dispatch.md                         1 file
references/starter-scenarios.csv                        1 file
references/trackable-findings.md                        1 file
templates/{scope-plan,investigation-brief,cross-area-brief,fadr-memo}.md  4 files
templates/artifacts/{14 area artifacts}.md              14 files
templates/{findings-ledger.md,workflow-state.json}      2 files
evals/{activation-cases.md,run-static-checks.sh,trigger-evals.json}  3 files
```

**Total: 53 files** across SKILL.md / skill.json / references / templates / evals.

## Reproduction

```bash
# Deterministic validator
python3 scripts/validate-generated-skill.py skills/opportunity-research/

# Per-skill static check
bash skills/opportunity-research/evals/run-static-checks.sh

# Repo-wide (will fail on pre-existing BMAD-skill release-contract issues)
just check
```
