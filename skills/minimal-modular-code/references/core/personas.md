# Target personas

Pick the persona that best matches the audience for this output. The choice shapes
vocabulary, depth, and which trade-offs to surface.

## Persona A — Engineer mid-change, keeping it minimal (DO)

Writing or changing code right now and wants to avoid bloat without slowing down. Comfortable
with their language and framework; not looking for an architecture lecture.

- **Speak to:** reuse before adding, subtracting, the wrong abstraction, the smallest change
  that works, what to flag to a human rather than decide alone.
- **Avoid:** heavy architecture vocabulary, prescriptive patterns, anything that reads as
  ceremony for a small change.

## Persona B — Reviewer or lead auditing a codebase (REVIEW)

Owns a judgment about the health of existing code or a repo: is it bloated, is it coupled, is
it safe for several agents to work in at once. Wants scored findings and a short "fix three
first" list, not a rewrite.

- **Speak to:** duplication and dead code, coupling and boundary clarity, work-partitionability,
  gate coverage, the cost of un-enforced invariants.
- **Avoid:** prescribing a named target architecture; treating every gap as a blocker
  regardless of project scale (calibrate).

## Persona C — Architect or lead shaping structure for an agent fleet (DESIGN)

Deciding the minimal boundary set and contracts that let many agents work in parallel without
colliding. Wants the smallest structure that earns its place, with clear trade-offs.

- **Speak to:** design rules as stable contracts, same-layer work-partitioning, ownership and
  blast radius, what becomes a gate vs what is routed to a human, the seam you need vs the one
  you imagine.
- **Avoid:** speculative generality; importing a full architecture style as a default.

## Persona D — Tech lead refactoring under deadline

Cannot do a big-bang rewrite. Needs a sequenced plan with a safety net at every step and a way
to stop partway.

- **Speak to:** smallest reversible step, characterization tests as a safety net,
  branch-by-abstraction and parallel-change, what breaks if the refactor stops at step N.
- **Avoid:** "first build the perfect model"; sequences that require freezing feature work.

## Default persona

When the prompt does not signal a clear audience, assume **Persona A** for DO, **Persona B**
for REVIEW, and **Persona C** for DESIGN, and state the assumption so the reader can redirect.
