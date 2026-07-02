# Skill Authoring Principles

How to write and maintain the skills in this catalog. This complements the
per-skill release contract in [AGENTS.md §Per-skill required artifacts](../AGENTS.md#per-skill-required-artifacts)
and the shared guardrails in
[`skills/_shared/empirical-warnings.md`](../skills/_shared/empirical-warnings.md)
(W2–W10 cover repo hardening; this file covers skill content).
`skill-curator` applies these when scaffolding; `skill-reviewer` gates on
them at review time. Sources for each principle are at the bottom — every
one traces to published field results, not taste.

## 1. Write the description for the model's routing decision

The frontmatter `description` has one job: let a model pick the right skill
from a crowded catalog. Name the user intents that should trigger it, and —
when a sibling skill is nearby — the anti-triggers ("Do NOT use for X; use
`<sibling>`"). No marketing language, no claims the body doesn't deliver.
Routing failure is the dominant failure mode of model-invoked skills, and
descriptions are the only surface the router sees. `just eval` measures
exactly this: each `trigger-evals.json` query graded against the *whole*
catalog's descriptions. Treat a new skill's trigger as unproven until those
runs say otherwise.

## 2. Keep `SKILL.md` small; route branch detail through references

A skill's always-loaded surface competes with the task's own context
(W6). Keep `SKILL.md` to the workflow spine and route branch-specific
playbooks, rubrics, and templates through the registry CSVs so the agent
loads only the branch it commits to. The ~1200-word default cap exists to
force this split, not as a style rule: a small `SKILL.md` is cheaper to
load, easier to audit, and less likely to hide a branch-only instruction
in the wrong place.

## 3. Inline the invariants an agent cannot afford to miss

The counter-rule to §2: agents routinely skip reference loads — extra
reads are expensive, and models economize. A safety boundary, a scoring
invariant, or a hard "never do X" that lives *only* behind a router row
can silently never fire. Anything whose omission breaks the skill's core
promise belongs in the `SKILL.md` body; references carry detail, never the
only copy of a must-not-miss rule. (Canonical failure: an agent with live
database tools created a SQL view but missed the product rule that keeps
row-level security intact — the invariant was discoverable but not inlined.)

## 4. Encode gotchas and opinions, not manuals

Models already know how to do the generic task; a skill earns its context
cost by carrying what they get reliably wrong — landmines, opinionated
defaults, non-obvious sequencing. Never paste volatile external facts
(vendor CLI flags, API surfaces, version numbers) as static prose: point
at the live source of truth and tell the agent to verify against it.
The measured case for restraint: WorkOS generated 10,000+ lines of
doc-derived skills that underperformed baseline — one dropped task
correctness from 97% to 77% — then replaced them with 553 lines of
observed gotchas and improved pass rates. Related: don't distill a
one-off procedure into a durable skill; a procedure that worked once can
be less robust than no skill at all (MUSE's canonical regression:
80% → 20%).

## 5. Steer with named concepts, not prose

Where behavior must bend, coin or reuse a compact term the agent will
repeat in its own reasoning ("vertical slices", "tracer bullet",
"deletion test") instead of paragraphs of "don't do it the other way".
A leading word survives summarization and costs fewer tokens every
subsequent turn; generic prose fails silently.

## 6. Prune with deletion tests

Skills accumulate three kinds of dead weight: **duplication** (the same
rule stated twice inside one skill), **sediment** (references or branch
instructions for workflows that no longer exist), and **no-ops**
(instructions that sound meaningful but change no behavior — "be
thoughtful", restating what any competent agent does unprompted). When
touching a skill, ask of each line: *what breaks if this is deleted?*
If the answer is nothing, delete it. More text is not more capability;
it is more routing noise and more attention spent per load.

## 7. Loops need stop conditions and iteration caps

Any skill that drives an iterate/retry/review-until-clean workflow must
state an explicit, checkable termination condition *and* a hard iteration
cap, plus an escalation rule for conflicting signals ("abort and ask").
Shipped examples set the pattern: Greptile's `greploop` stops at full
confidence with zero unresolved comments *or* five iterations, whichever
comes first. A loop without a cap is a runaway-session bug waiting for an
oversized input.

## 8. Skills guide; gates guarantee

A skill is instructions the model may not follow — per-step compliance
compounds, so a 10-step workflow at 90% per-step yields ~35% end-to-end.
Anything that must happen *every* time (safety boundaries, required
checks, output contracts) belongs in a deterministic gate — hook, CI
check, static check — with the skill referencing the gate, not
substituting for it (W3). This repo practices the split: destructive-git
protection is a PreToolUse hook and branch protection, not skill prose.

## 9. Measure, don't assume

A skill can read well, route perfectly, and still make results worse —
active harm is invisible without comparison. The gold standard is an
ablation: run the same tasks with and without the skill and score
outcomes; benchmark results show skills lifting pass rates by roughly
13–15 points on average, which means individual skills vary widely and
some go negative. This repo's `just eval` covers routing; treat outcome
ablations as the bar when a skill's value is questioned, and treat every
skill as a hypothesis under test (W8). Adoption and stars are
distribution signal, not eval proof.

## Sources

- Matt Pocock — *Building Great Agent Skills: The Missing Manual*
  (<https://youtu.be/UNzCG3lw6O0>): the trigger / structure / steering /
  pruning audit behind §1, §2, §5, §6.
- Nick Nisi (WorkOS) — *How I deleted 95% of my agent skills and got
  better results*, AI Engineer 2026 (<https://youtu.be/vy7o1g2iHY8>):
  the 10k→553-line rewrite, the 97%→77% ablation, "enforce, don't
  instruct" — §4, §8, §9.
- Nick Nisi & Zack Proser (WorkOS) — *Full Walkthrough: Writing & Using
  Skills* (<https://youtu.be/pFsfax19yOM>): "the description is for the
  model", constraints over recipes — §1, §4.
- Pedro Rodrigues (Supabase) — *Combine Skills and MCP to Close the
  Context Gap* (<https://youtu.be/JT3OzDKrucU>): non-skippable guidance
  belongs in the main skill file; point at the source of truth — §3, §4.
- Li et al. 2026 — *SkillsBench* (arXiv:2602.12670): side-effect-graded
  skill evals; +13–15pp mean lift with high variance — §9.
- Lin et al. 2026 (ByteDance) — *MUSE-Autoskill*: test-gated skill
  lifecycle; the one-off-procedure regression — §4, §9.
- David Gomes (Cursor) — *Replacing 12K LoC with a 200 LoC Skill*
  (<https://youtu.be/WE_Gnowy3uw>): prompt-enforced vs code-enforced
  boundaries — §8.
- Greptile — `check-pr` / `greploop` agent skills: explicit stop
  conditions and iteration caps in shipped looping skills — §7.
- Liu et al. 2026 — *Agent Skills in the Wild*: 26.1% of 42k marketplace
  skills carry ≥1 vulnerability; executable scripts raise the odds 2.12× —
  background for treating skill PRs at production depth (W5).
