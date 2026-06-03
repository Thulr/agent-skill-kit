# Depth Rubric

Every curated skill picks a **routing depth**. Three shapes are named
because they have working canonical examples in this repo, but the
pattern is recursive: a skill can route through as many CSV layers as
its content actually needs. Progressive disclosure is the load-bearing
mechanism — the agent only reads the next layer when it commits to
that branch — and it generalizes to any depth.

Pick deliberately. Most curated skills land at **single-layer**.

## The named shapes (canonical anchors, not a closed set)

| Shape | Anatomy in short | Use when |
|---|---|---|
| **Flat** (depth 0) | `SKILL.md` + 0–2 supporting files | One procedure or one well-named technique. No internal branching. |
| **Single-layer** (depth 1, hub-and-spoke) | `SKILL.md` + `references/` + optional `templates/`/`evals/` + one registry CSV | 3–8 distinct intents that share rubrics, output templates, or vocabulary. |
| **Two-level routing** (depth 2) | `SKILL.md` + intent-router CSV + intent-specific CSVs + per-surface playbooks + shared `core/` rubrics + per-intent `templates/` + `evals/` with static check | Two orthogonal dimensions (intent × surface, mode × topic) where each leaf needs distinct content. |
| **Deeper** (depth ≥3) | Same pattern recursively: each registry CSV's rows can name a child registry CSV that routes the next axis | Three or more genuinely orthogonal axes (intent × surface × persona, mode × topic × stage). Each axis must independently change which content loads. |

Full anatomy for the named shapes: `shapes/flat.md`, `shapes/single-layer.md`,
`shapes/two-level.md`. For depth ≥3, follow the two-level recursion
described in **Going deeper** below — no named anchor exists yet
because no skill in this repo has hit a real 3-axis need.

## Decision questions

Run these in order. Stop at the first depth that comfortably fits.

1. **How many distinct invocations does this skill need to handle?**
   - 1–2 → flat
   - 3–8 → single-layer
   - 9+ → two-level or deeper

2. **How many orthogonal axes does the invocation space have?**
   An axis is orthogonal when changing it changes which content loads
   independently of the other axes. Examples: intent × surface,
   audience × format, mode × topic, intent × surface × persona.
   - 0 axes (no branching) → flat
   - 1 axis → single-layer
   - 2 axes → two-level
   - 3+ axes → deeper, following the same recursive pattern

3. **How much content does each leaf need?**
   - <100 words → flat is fine
   - 200–500 words → single-layer
   - 500+ words → two-level or deeper (so each leaf loads only when relevant)

4. **Is there a shared rubric, vocabulary, or template across leaves?**
   - Yes → single-layer or deeper (put it in `references/core/`)
   - No → flat

5. **Will the runtime files at the current depth exceed their word cap?**
   - SKILL.md > ~500 lines, or a playbook > ~1500 words → escalate one
     depth so each consumer reads only what it needs.

## Bias toward shallow

Start at the shallowest shape that fits, and grow into a deeper shape
only when content demands it. A shallower skill that outgrows itself
can always be promoted; an over-engineered deeper skill rarely gets
flattened back.

Signals that a flat skill should become single-layer:

- A second clearly-distinct intent appears.
- An output template would be reused enough to deserve its own file.
- Three or more rubrics or vocabularies start to share text.

Signals that a single-layer skill should become two-level:

- The registry needs a second axis (not just "intent" but
  "intent × audience" or "intent × surface").
- A single leaf needs to load 9+ distinct chunks of content depending on
  context.
- One leaf grows past ~1500 words — that's usually several variants
  pretending to be one row.

Signals that a two-level skill should go deeper:

- A third axis is doing real work — picking it changes which content
  loads independently of intent and surface.
- A single (intent × surface) playbook has its own internal routing
  ("if persona is X, do A; if Y, do B") that wants to be a CSV.
- One playbook grows past ~1500 words because it's covering several
  variants of a hidden third axis.

## Going deeper (depth ≥3)

The two-level pattern recurses. At depth N you have:

- `references/intent-router.csv` — the top-level axis
- `references/intents/<intent>.csv` — second-level axis per intent
- `references/<intent>/<subintent>.csv` (or similar nested directory)
  — third-level axis per (intent, subintent)
- ... and so on until the leaves are playbooks under
  `references/playbooks/`

Each CSV layer follows the same rules as `shapes/two-level.md`:

- Every row in a registry differs meaningfully from its siblings (no
  collapsed axis at any depth).
- Every leaf playbook follows the canonical section structure
  (`## Scope`, `## Grounding`, `## Good signals`, `## Common failures`,
  `## Heuristics`, `## Quick diagnostic`, `## Cross-references`).
- Shared rubrics live in `references/core/`, reachable from any depth.
- The static check auto-derives the registry chain from disk; no
  hardcoded depth.

Until a skill genuinely needs depth ≥3, treat two-level as the
practical ceiling and reach for splitting only when adding a third
axis would *itself* be the anti-pattern (e.g., the "axes" aren't
actually orthogonal and a second skill would model the situation
better).

## Canonical examples

- **Flat:** `skills/example-minimal/` (or any single-file skill).
- **Single-layer:** most user-facing skills with one intent registry.
- **Two-level:** `skills/dx-audit/` (intent: audit/debug/edge-pass
  × surface: api/sdk/cli/docs/errors/...).
- **Deeper:** none in this repo yet. When the first skill genuinely
  needs depth ≥3, add a worked example here and write a matching
  `shapes/<name>.md` anatomy doc by adapting `shapes/two-level.md`.

Read the closest canonical example end-to-end before scaffolding your
own — copying structure beats inventing it.

## Anti-patterns

- **Adding a level that has only 1–2 values at one axis.** That axis
  isn't pulling weight. Collapse it back into its parent.
- **Flat with 10 procedures in one `SKILL.md`.** Split to single-layer
  with a registry.
- **A registry whose rows all point at the same files (at any depth).**
  No routing is happening. Either collapse that layer or differentiate
  the rows.
- **Going deeper because "we can."** The cap is content-driven, not
  arbitrary; without a real third axis doing independent work, a
  third CSV layer is just overhead.
- **Pretending two axes are three** (e.g., audience and persona are
  often the same axis). Confirm orthogonality before adding depth.
- **Routing depth as a substitute for skill splitting.** If two
  proposed branches don't share rubrics, vocabulary, or templates,
  they probably belong in separate skills — depth is for one cohesive
  skill that needs to route, not for stapling unrelated behaviors
  together.
