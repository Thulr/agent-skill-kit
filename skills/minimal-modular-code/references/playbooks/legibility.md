# Legibility Playbook

## Scope

The readability of the code that remains — for humans and for a context-bound agent.
Covers naming, control-flow visibility, the conciseness-vs-cleverness line, readability
as a measurable property, and machine-queryable structure.

- **In:** naming, visible vs hidden control flow, density vs clarity, structure maps,
  concept/synchronization decomposition for readability.
- **Out:** *how much* code there is (see `minimalism.md`); *where the seams go* (see
  `boundaries.md`).
- **Intents this surface answers:** do, review, design.

## Grounding

- **Abelson & Sussman, SICP (1985)** — programs are written for people to read, only
  incidentally for machines to execute.
- **Donald Knuth, "Literate Programming" (1984)** — explain to humans what the computer
  should do.
- **Kernighan & Plauger, The Elements of Programming Style (1978)** — clarity over
  cleverness; write below your maximum cleverness.
- **Strunk & White (1959) / Paul Graham, "Succinctness is Power" (2002)** — concise means
  no wasted elements (semantic, not character count); golf is not the goal.
- **Buse & Weimer (2010)** — readability is measurable, correlates with defects, and is
  driven by local features; over-dense lines read worse.
- **G. Ann Campbell, "Cognitive Complexity" (2018)** — nesting and flow breaks, not raw
  line count, drive understandability.
- **Meng & Jackson, "What You See Is What It Does" (2025)** — behavior should be readable
  from the unit, without tracing hidden magic.
- **Cherny-Shahar & Yehudai, RIG (2026)** — a deterministic structure map measurably helps
  agents; legibility extends to the repo level.

## Good signals

- Symbols are findable with one search; a reader can name what a function does from its
  name and signature.
- Control flow is visible top-to-bottom; effects happen where you can see them, not via
  reflection, dynamic dispatch, or implicit hooks.
- Lines are scannable, not packed; an reviewer (human or agent) can hold one unit in their
  head without opening five others.
- The repo exposes a structure map (build/test/dependency graph) an agent can treat as
  ground truth.

## Common failures

- **Generic or overloaded names** — `data`, `tmp`, `manager`, `handle`, or a name reused
  for several concepts; a name that needs a comment to disambiguate.
- **Hidden magic** — behavior driven by dynamic imports, reflection, metaprogramming, or
  ORM lifecycle hooks that a reader cannot see from the call site.
- **Dense one-liners** — clever expressions that minimize characters at the cost of the
  reader reconstructing intent; "smart" code the author could not later debug.
- **Comment-as-apology** — a comment compensating for a name or structure that should have
  been clear on its own.

## Heuristics

- **(do, review) Names are precise and grep-unique.** A name that needs a comment, or
  reaches for `data`/`tmp`/`manager`, signals the underlying thing is unclear or does too
  much — rename precisely or split it.
- **(do) Keep control flow visible.** Prefer explicit phases and direct calls over implicit
  dispatch; a unit's behavior should be readable from the unit.
- **(review) Read for readability as a defect signal.** Over-long lines, high identifier
  density, and deep punctuation nesting measurably reduce readability; flag the densest
  units, not merely the longest.
- **(review) Use cognitive complexity, not raw length, as the understandability signal.**
  Nesting and breaks in linear flow cost the reader more than line count.
- **(do, design) Optimize for reading, not writing.** Code is read far more often than it
  is written; pay a little writing cost to save the larger reading cost.
- **(do) Clarity over cleverness.** Do not be too clever; write below your maximum
  cleverness so the code stays debuggable.
- **(do, review) Succinct in elements, not characters.** Remove wasted elements; do not
  shorten by cryptic naming or omitted structure — that is golf, not concision.
- **(design) Make structure machine-queryable.** Provide a deterministic build/test/
  dependency map so a context-bound agent treats topology as ground truth instead of
  guessing it from raw files.
- **(design) Decompose into independent concepts with explicit synchronizations.** A change
  should touch one visible unit, not require tracing hidden coupling across files.

## Quick diagnostic

- Can you find every use of this symbol with one search? — no → rename to something
  grep-unique.
- Can a new reader say what this unit does from its name and signature? — no → the name or
  the unit is wrong.
- Does understanding this line require reconstructing a clever trick? — yes → unpack it;
  clarity beats the character saving.
- Can an agent learn the repo's structure from a map, or must it infer it from raw files?
  — infer → add a structure map.

## Cross-references

- `minimalism.md` — fewer elements first; legibility is about the elements that remain.
- `boundaries.md` — a legible unit still needs the right seam around it.
- `parallel-readiness.md` — machine-queryable structure also partitions agent work.
- `references/intents/{do,review,design}.csv` row `legibility` — the entry points.
