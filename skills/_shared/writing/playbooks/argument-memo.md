# Argument & Memo Playbook

## Scope

- **In:** any piece whose job is to land a conclusion or win a decision — PRDs,
  RFCs, recommendation memos, strategy and decision docs, design rationale,
  proposal sections.
- **Out:** step-by-step instructions (→ `technical-doc.md`), a spoken talk or
  pitch deck (→ `talk-pitch.md`), a discovery write-up with no ask (→
  `narrative.md`).
- **Intents this surface answers:** `structure`, `draft`, `persuade` (design);
  `revise`, `copyedit`, `diagnose` (audit).

## Grounding

- *The Pyramid Principle* (Barbara Minto, 1987) — lead with the answer; the
  Situation–Complication–Question–Answer intro; group support so it's mutually
  exclusive and collectively exhaustive.
- *The Narrative Gym / "ABT"* (Randy Olson, 2015) — compress the spine to one
  *and / but / therefore* sentence before drafting.
- *The Sense of Style* (Steven Pinker, 2014) — the expert blind spot; order
  given-information before new.
- *Revising Prose* (Richard Lanham, 1979) — tighten the bureaucratic noun-style
  a memo drifts into.

## Good signals

- The recommendation or conclusion appears in the first few lines, before the
  supporting detail.
- The opening establishes shared context, the change that prompts the memo, and
  the question it answers — then answers it.
- Supporting points form 3–5 non-overlapping groups whose headings *assert*
  something, not count ("Cost is the blocker," not "Three considerations").
- The reader can tell exactly what they're being asked to decide or approve.

## Common failures

- **Buried recommendation** — the memo retraces the author's discovery path
  (evidence first, conclusion last), so a busy reader never reaches the ask.
  Invert to answer-first.
- **Background dump** — paragraphs of context before any signal of why the
  reader should care; the complication and question are missing.
- **Non-MECE groups** — supporting points overlap or leave gaps, so the
  argument reads as a list and the reader can't tell if it's complete.
- **Counting headings** — "Four findings" tells the reader nothing; the heading
  should state the insight of the group.
- **Hedged ask** — the recommendation is so qualified the reader can't tell
  what's actually being proposed (distinct from honest uncertainty — see
  `voice-guard.md`).

## Heuristics

- **(structure, diagnose) Answer first** — the governing recommendation leads;
  discovery order (evidence → conclusion) is inverted for communication.
- **(structure, draft) SCQA intro** — draft the Situation→Complication→
  Question→Answer before the body, to surface the reader's real question.
- **(structure, diagnose) MECE groups** — support sits in 3–5 non-overlapping,
  gap-free groups; test every grouping for overlap and completeness.
- **(structure, diagnose) Asserting headings** — each section heading states a
  claim, so the headings read top-to-bottom as the argument.
- **(persuade) One-sentence spine** — an *and/but/therefore* line names the
  context, the tension, and the ask; if you can't write it, the memo has no
  spine yet.
- **(revise) Un-bury the verbs** — convert nominalizations and *to-be* verbs
  into active claims (see `clarity-rubric.md`); memos rot into noun-style.
- **(copyedit) One term per concept** — a decision doc that calls the same
  thing three names invites the reader to infer differences that aren't there.
- **(diagnose) Findable ask** — a scanner reading only headings and first lines
  can state what's being decided.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is the recommendation in the first 5 lines? | Reader bounces before the ask | Move the answer up; invert to top-down |
| Does the intro name the complication + question? | Reader doesn't know why to care | Add SCQA framing |
| Do the section headings assert, not count? | Argument reads as a list | Rewrite headings as claims |
| Are the groups MECE? | Gaps or overlap undermine the case | Regroup; test exclusivity and coverage |
| Can a scanner find the ask in 10 seconds? | Decision stalls | Surface the ask in a heading |

## Cross-references

- `references/core/structure-rubric.md` — answer-first, SCQA, MECE, the turn.
- `references/core/persuasion-rubric.md` — when the memo also needs to move someone.
- `references/core/clarity-rubric.md` — the line-level tightening pass.
- `references/playbooks/talk-pitch.md` — when the memo becomes a spoken pitch.
- `references/playbooks/technical-doc.md` — when the ask is "how," not "whether."
