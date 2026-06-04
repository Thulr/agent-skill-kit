# Mutation Testing Playbook

## Scope

A meta-technique: mutate the SUT (flip a `>` to `>=`, replace `return x` with `return null`, remove a method call), run the existing test suite, and check whether the mutation is detected. Surviving mutants reveal weak assertions or missing tests. Routes to `unit.md` (where the mutants usually survive) and to `property-based.md` (which often catches them).

## Grounding

- **Yue Jia & Mark Harman — "An Analysis and Survey of the Development of Mutation Testing"** — comprehensive survey of mutation operators, the equivalent-mutant problem, operator-selection strategies, and the empirical landscape.
- **René Just et al. — "Are Mutants a Valid Substitute for Real Faults in Software Testing?"** — empirical evidence that mutation score correlates meaningfully with real-fault detection, validating mutation testing as a signal worth measuring.
- **PIT (Java) and Stryker (JavaScript / .NET / Scala) documentation** — practical state of the art: configuration, performance tuning, sample reports.

## Good signals

- Mutation runs are scoped to recently-changed modules, not the whole repo on every PR.
- Equivalent mutants (those that don't change observable behavior) are suppressed with explicit justification, not silently.
- Mutation score is treated as a *thermometer* (higher generally indicates stronger assertions), not as a *target* (chasing a percentage induces gaming).
- Surviving mutants are triaged: each one is either an equivalent mutant (suppress with rationale), a weak assertion in an existing test (tighten the assertion), or a genuine gap (write a new test).
- Mutation testing runs nightly or on-demand, not blocking every PR — cost is too high otherwise.
- It's used after coverage and bug-shape thinking have been exhausted, as the final-mile signal.

## Common failures

- Whole-repo mutation testing run on every PR — CI bill blows up, developers learn to ignore the report.
- Equivalent mutants left unsuppressed — every run produces noise, real signal drowns.
- "X% mutation score" set as an OKR — engineers add weak tests to bump the score, the test suite gets worse.
- Mutation report ignored — surviving mutants noted in a dashboard nobody reads.
- Mutation used as a coverage substitute on a project with no other test discipline — produces a report that says "you have no tests" verbosely.
- The report shows surviving mutants but doesn't link to the specific test that should have caught each — triage is impossible.

## Heuristics

- **Targets are scoped** *(audit, strategize)* *(cost)* — run mutation testing against modules under change, not the whole repo. Whole-repo mutation is impractical except as a quarterly audit; per-PR mutation should target the diff.
- **Equivalent mutants triaged, not chased** *(audit)* *(cost, confusion)* — known-equivalent mutants are suppressed with a justification comment, not silently ignored. Suppression without rationale is technical debt that turns into noise.
- **Mutation score is a thermometer, not a goal** *(audit, strategize)* *(false-pass)* — surviving mutants are the signal; the percent score is a temperature reading. Targeting "X% mutation score" creates the same gaming dynamic as line-coverage targets: engineers add weak tests to bump the number, the suite gets worse.
- **Surviving mutants reveal weak assertions** *(audit)* *(false-pass)* — the typical fix is a stronger assertion in an existing test, not always a new test. The unit-test author sees the surviving mutant and tightens the relevant assertion. New tests come second.
- **Run gated for cost** *(strategize)* *(cost)* — sampled / on-demand / nightly. Not on every PR. Diff-targeted mutation testing on PR is acceptable if the per-PR cost stays under the suite's overall budget.
- **Used when other signals plateau** *(strategize)* *(cost)* — diminishing returns once coverage and bug-shape thinking are exhausted; mutation is the final-mile signal. Reaching for it before basic test hygiene is in place produces a wall of noise.
- **Report links survivors to candidate tests** *(audit, author)* *(confusion)* — for triage to be feasible, the report should suggest which existing test ought to have caught each surviving mutant. Without that link, mutation reports become unactionable.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is the mutation run scoped to changed code? | CI bill blows up; developers ignore the report | Configure diff-targeted runs; nightly for full sweep |
| Are equivalent mutants suppressed with rationale? | Noise drowns signal | Add suppression annotations with one-line justifications |
| Is mutation score used as a thermometer, not a target? | Gaming via weak tests | Remove score from OKRs; report surviving mutants, not percent |
| Are surviving mutants triaged? | Report ignored | Owner per file; weekly triage cadence |
| Does the run gate on cost? | Per-PR cost unsustainable | Move to nightly + on-demand |
| Does the report link mutants to candidate tests? | Triage is infeasible | Configure the framework to show implicated tests per mutant |

## Cross-references

- → `unit.md` — surviving mutants usually point at weak unit-test assertions
- → `property-based.md` — properties often kill many mutants at once; the two layers reinforce each other
- → `core/failure-modes.md` — false-pass (weak assertions that fail to detect mutations) is the headline mode this layer surfaces
- → `core/personas.md` — persona 3 (suite operator) owns the cost/value tradeoff; persona 4 (test skeptic) reads the report
