# Minimalism Playbook

## Scope

The amount of code: writing less, reusing what exists, subtracting, and refusing
abstractions a present need has not yet forced. Covers reuse-first, the wrong
abstraction, speculative generality, dead code and clones, over-engineering, and
the deletion guardrail.

- **In:** reuse-before-write, subtraction, the duplication-vs-abstraction decision,
  dead-code and over-engineering detection, the timing of abstraction.
- **Out:** *how readable* the code that remains is (see `legibility.md`); *where the
  seams go* (see `boundaries.md`).
- **Intents this surface answers:** do, review, design.

## Grounding

- **Sandi Metz, "The Wrong Abstraction" (2016)** — duplication is cheaper than the
  wrong abstraction; back out a bad abstraction rather than patch it.
- **Martin Fowler, "Yagni" (2015)** — cut speculative features; the carve-out that it
  does *not* license neglecting code health.
- **Adams, Converse, Hales & Klotz, Nature (2021)** — people overlook subtraction
  unless explicitly cued.
- **Charles Krueger, "Software Reuse" (1992)** — build from existing software, not from
  scratch.
- **John Ousterhout, A Philosophy of Software Design (2018)** — many shallow units raise
  total complexity; minimal means minimal surface, not smallest pieces.
- **Fred Brooks, "No Silver Bullet" (1986)** — minimalism removes accidental, not
  essential, complexity.
- **Thomas McCabe (1976)** — complexity is measurable and a smell signal.
- **G. K. Chesterton (1929)** — do not remove what you do not yet understand.

## Good signals

- The change reuses an existing function/module instead of re-implementing it.
- The diff deletes or net-reduces lines as often as it adds.
- Every abstraction has at least two or three real callers, not one speculative one.
- No parameter, flag, or branch exists for a case the code does not handle today.
- Complexity metrics on touched files are flat or falling, not climbing.

## Common failures

- **The wrong abstraction** — an early DRY extraction is patched with parameters and
  conditionals as new cases arrive, until the shared unit is unmaintainable. Cost
  compounds; duplication's cost is linear and visible.
- **Speculative generality** — config hooks, plugin points, or type parameters built for
  an imagined future, not a present requirement.
- **Additive bias** — the change only adds; the option to *remove* something to reach the
  same outcome was never considered.
- **Clone-and-tweak** — a block is copied and edited instead of the shared decision being
  located and reused; the duplication is of *intent*, not just text.
- **Reckless deletion** — "dead-looking" code removed without finding why it was added;
  the guard clause was load-bearing.
- **False subtraction** — tests, validation, error paths, or guards removed to make the
  diff shorter even though they still protect a contract or production invariant.

## Heuristics

- **(do) Search before you write.** Grep the repo and dependency surface for an existing
  helper or abstraction before adding one; prefer composing what exists.
- **(do, review) Prefer duplication to a guessed abstraction.** Wait until the third
  occurrence makes the shared decision obvious; abstracting on the second risks the wrong
  abstraction.
- **(do) Ask "what can be removed?" explicitly.** The subtractive option does not surface
  on its own — make it a deliberate step before proposing additions.
- **(do, design) Scope YAGNI to features, not malleability.** Cut code that serves a
  presumptive feature; keep the refactoring that keeps code easy to change.
- **(review) Flag over-abstraction.** Indirection with a single caller, parameters only
  one path uses, and layers that only pass values through are negative-value structure —
  severity 2–3.
- **(review) Treat rising cyclomatic or cognitive complexity as a refactor signal, not a
  target.** Extracting to lower a per-function number can just move complexity; the metric
  is a smell detector, not a goal.
- **(review) Hunt dead code and clones.** A clone is a duplicated *decision*; flag it for
  consolidation only where the two copies genuinely encode the same intent.
- **(do, review) Concise is not terse.** "No wasted elements" is the bar; do not trade
  clarity for a clever one-liner or a shorter character count (see `legibility.md`).
- **(do) Gate deletion on understanding.** Before removing code, find why it exists (blame,
  tests, linked issue); remove only once the reason is understood and proven obsolete or
  preserved by an equivalent invariant. "Not part of this change" is not enough evidence
  to delete a guard, test, validation, error path, or boundary.
- **(design) Do not oversell simplicity.** Minimalism removes accidental complexity; the
  problem's essential difficulty remains and is the real work.

## Quick diagnostic

- Does an equivalent function/abstraction already exist in the repo or deps? — yes → reuse
  it; no → consider whether the new one earns its place.
- Is this abstraction serving a requirement that exists *today*? — no → inline it / defer
  it; yes → keep it minimal.
- Could the same outcome be reached by deleting something instead of adding? — yes →
  prefer the subtraction; no → proceed.
- Is the abstraction defended mainly because it was expensive to build? — yes → that is
  sunk cost; re-evaluate on merit.

## Cross-references

- `legibility.md` — once the code is minimal, is what remains readable?
- `boundaries.md` — when an abstraction *is* warranted, where does the seam go?
- `references/core/severity-rubric.md`, `references/core/score-rubric.md` — REVIEW scales.
- `references/calibration.md` — right-size how many findings you write to project scale.
- `references/intents/{do,review,design}.csv` row `minimalism` — the entry points.
