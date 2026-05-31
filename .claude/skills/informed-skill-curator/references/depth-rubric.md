# Depth Rubric

Every curated skill takes one of three shapes. Pick deliberately — most
curated skills land at **single-layer**.

## The three shapes

| Shape | Anatomy in short | Use when |
|---|---|---|
| **Flat** | `SKILL.md` + 0–2 supporting files | One procedure or one well-named technique. No internal branching. |
| **Single-layer** (hub-and-spoke) | `SKILL.md` + `references/` + optional `templates/`/`evals/` + one registry CSV | 3–8 distinct intents that share rubrics, output templates, or vocabulary. |
| **Two-level routing** | `SKILL.md` + intent-router CSV + intent-specific CSVs + per-surface playbooks + shared `core/` rubrics + per-intent `templates/` + `evals/` with static check | Two orthogonal dimensions (intent × surface, mode × topic) where each leaf needs distinct content. |

Full anatomy per shape: `shapes/flat.md`, `shapes/single-layer.md`,
`shapes/two-level.md`.

## Decision questions

Run these in order. Stop at the first depth that comfortably fits.

1. **How many distinct invocations does this skill need to handle?**
   - 1–2 → flat
   - 3–8 → single-layer
   - 9+ → consider two-level

2. **Are intents orthogonal — can they be described as a matrix?**
   Examples of orthogonal axes: intent × surface, audience × format,
   mode × topic.
   - Yes → two-level may help
   - No, they're a flat list → single-layer

3. **How much content does each leaf need?**
   - <100 words → flat is fine
   - 200–500 words → single-layer
   - 500+ words → two-level (so each leaf loads only when relevant)

4. **Is there a shared rubric, vocabulary, or template across leaves?**
   - Yes → single-layer or two-level (put it in `references/core/`)
   - No → flat

5. **Will `SKILL.md` exceed ~500 lines if I keep everything inline?**
   - Yes → escalate one depth

## Bias toward shallow

Start at the shallowest shape that fits, and grow into a deeper shape only
when content demands it. A flat skill that outgrows itself can always be
promoted; an over-engineered two-level skill rarely gets flattened back.

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

## Canonical examples

- **Flat:** `skills/example-minimal/` (or any single-file skill).
- **Single-layer:** most user-facing skills with one intent registry.
- **Two-level:** `skills/dx-critique/` (intent: audit/debug/edge-pass
  × surface: api/sdk/cli/docs/errors/...).

Read the canonical example end-to-end before scaffolding your own at that
depth — copying structure beats inventing it.

## Anti-patterns

- **Two-level with one dimension that has only 1–2 values.** The second
  axis isn't pulling weight. Collapse to single-layer.
- **Flat with 10 procedures in one `SKILL.md`.** Split to single-layer
  with a registry.
- **Single-layer with a registry whose rows all point at the same files.**
  No routing is happening. Either collapse to flat, or differentiate the
  rows.
- **Two-level because "it's the canonical shape."** Cargo-culting
  dx-critique on a skill whose space isn't a real 2-axis matrix. Pick
  the shape the content asks for, not the prestigious one.
