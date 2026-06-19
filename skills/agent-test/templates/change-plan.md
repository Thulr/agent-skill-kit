# Change Plan — <what measurement instrument you are building>

**Target persona:** <from references/core/personas.md> (usually Persona A)
**Surfaces in scope:** <eval-design | judge-calibration | trajectory-tests | benchmark-design | activation-evals>
**Date:** <YYYY-MM-DD>

A pre-flight plan for an in-progress eval/judge/test change. Fill it before writing much; it is
a thinking tool, not a deliverable to track.

## What already exists

<What measurement you have before changing — the existing eval, judge, fixtures, or benchmark
you will build on. Confirm fixtures are held-out (disjoint from training) and candidates are
non-trivial (real prompt+completion+tool I/O) before relying on them.>

## The minimal change

- **Reuse:** <existing eval/fixture/judge this builds on>
- **Add:** <the smallest measurement that gates the change at hand>
- **Remove:** <evals this lets you retire — answer even if "nothing">

## Trust check

- **Decomposable:** <does a red result attribute to a named failure mode / trajectory span?>
- **Calibrated:** <if a judge gates — calibrated against a human-labeled set, with explanations?>
- **Held-out:** <are benchmark fixtures disjoint from training, with a count margin?>
- **Right-sized:** <is this the smallest eval that gates this change's staircase tier?>

## Seams I am deliberately NOT adding

<The benchmark suites, judges, or coverage you considered and are leaving out because no present
need forces them (YAGNI). Naming them documents the restraint.>

## Blast radius

<What this gates — a prompt edit, a model swap, a release. If it becomes the release gate, note
it must be per-slice (not a single aggregate) before you trust it.>

## Routing

- **Mechanical** (fixture wiring, schema asserts, CI hook): handled by <gate / locally>.
- **Judgment call to flag to a human:** <trusting a judge as a gate, a rollback threshold, a
  held-out relabel — or "none">.

## Grounding sources applied

- <skill.json inspired_by entry> — <how it shaped this plan>
