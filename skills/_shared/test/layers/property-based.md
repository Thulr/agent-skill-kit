# Property-Based Test Playbook

## Scope

Tests that state a *property* of the SUT (an invariant, a round-trip, a metamorphic relation) and generate inputs to challenge it. Distinct from example-based tests, which hard-code specific inputs. Routes to `unit.md` for example-based tests of the same SUT. Routes to `mutation.md` to assess whether the property is meaningful.

## Grounding

- **John Hughes & Koen Claessen — "QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs"** — the original property-based testing framework; introduced random generation + shrinking as a discipline.
- **David R. MacIver — Hypothesis design rationale** — practical generator design for mainstream languages, the targeting framework, and the philosophical case for properties as specifications.
- **John Hughes — "Experiences with QuickCheck: Testing the Hard Stuff and Staying Sane"** — choosing properties that catch real bugs, the model-based property pattern, and the discipline of writing properties that aren't trivial.

## Good signals

- Each property names a real invariant of the SUT: `reverse(reverse(xs)) == xs`, `parse(serialize(x)) == x`, `sort(xs)` is sorted and is a permutation of `xs`.
- Generators cover the meaningful input space: empty, single-element, max-size, unicode, malformed, negative numbers, NaN, very large.
- Shrinking is enabled — failures are reported as the minimal counterexample, not the original 10,000-element input.
- Properties supplement example-based tests; concrete examples document the behavior, properties stress it.
- Failed runs report the seed; rerunning with the seed reproduces.
- Run count is tuned to signal — defaults (~100 runs) for stable code; higher (~10,000) for rare-condition discovery.

## Common failures

- Property is a tautology: `f(x) == f(x)`, `add(a, b) == add(a, b)` — passes for any implementation, catches nothing. False-pass mode by definition.
- Property assumes its own implementation: `sum(xs) == reduce(xs, 0, +)` re-implements `sum` to test it.
- Generators only produce easy inputs (small positive integers) — never exercises the boundaries where bugs live.
- Shrinking disabled or misconfigured — a 10,000-element failing input lands in the report, and nobody can figure out which element caused it.
- Properties run *instead of* example-based regression tests, not alongside them. A regression test for bug #1234 should be a specific example, not a property that "covers" it.
- Failed run doesn't print the seed — flaky property tests can't be reproduced.

## Heuristics

- **Names a real invariant, not a tautology** *(review, author)* *(false-pass)* — `reverse(reverse(x)) == x` good; `f(x) == f(x)` worthless. The property should be falsifiable by a wrong implementation. If you can't construct a wrong implementation that breaks it, the property says nothing.
- **Generators cover the meaningful space** *(review, author)* *(gap)* — boundaries (empty, single, max), unusual characters (unicode, control codes, very long), malformed inputs, edge numerics (zero, negative, NaN, max). Default generators usually produce only easy inputs; the bugs are at the edges.
- **Shrinking enabled & inspected** *(review)* *(confusion)* — failures shrink to the minimal counterexample; the test report shows it. A failing input of 10,000 elements that doesn't shrink is undebuggable.
- **Run-count tuned to signal** *(review, strategize)* *(gap, cost)* — default ~100 runs catches obvious bugs; rare conditions need ~10,000+. Tuning per property based on the rarity of the bug-class it's targeting.
- **Properties supplement example-based, don't replace them** *(review, strategize)* *(confusion)* — concrete examples keep regression-purpose tests legible and grep-able; properties carry the spec-purpose work. Both are needed; neither alone is sufficient.
- **Seeded for reproducibility** *(review)* *(flakiness, confusion)* — failing runs report the seed; rerunning with the seed reproduces. Without this, property tests become flaky by design.
- **Model-based property when applicable** *(author)* *(brittleness, gap)* — compare the SUT against a simpler reference model that's obviously correct (or against the spec). Catches bugs the SUT-vs-itself properties miss.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does the property catch a wrong implementation? | False-pass — tautology | Rewrite as a real invariant the SUT could violate |
| Do generators reach the boundaries? | Gap on edge cases | Add explicit boundary generators (empty, max, unicode, NaN) |
| Does shrinking produce a minimal counterexample? | Undebuggable failures | Enable / configure shrinking; verify on a synthetic failure |
| Is the run count tuned to the rarity of the bug? | Misses rare conditions or wastes CI time | Tune up for rare; down for common |
| Are properties alongside concrete examples? | Regression tests become illegible | Keep example-based tests for bug-specific regressions |
| Does a failure report the seed? | Flaky property test | Configure the framework to print the seed on failure |

## Cross-references

- → `unit.md` for example-based tests of the same SUT
- → `mutation.md` to assess whether the property is meaningful (a strong property kills many mutants)
- → `core/failure-modes.md` — false-pass (tautological properties) and gap (weak generators) are the dominant modes at this layer
- → `core/personas.md` — persona 4 (test skeptic) is the right lens: skeptics catch tautologies fastest
