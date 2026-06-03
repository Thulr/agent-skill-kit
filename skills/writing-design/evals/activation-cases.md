# writing-design Activation Cases

## Positive

The skill should activate and route correctly (intent × genre → playbook →
template).

- "Help me outline this RFC before I write it" → `structure` × `argument-memo`, loads `argument-memo.md`, emits `outline-plan.md`.
- "Turn these scattered notes into a recommendation memo that leads with the answer" → `structure` × `argument-memo` → `outline-plan.md`.
- "How should I structure a how-to guide around what the user is trying to do?" → `structure` × `technical-doc` → `outline-plan.md`.
- "Outline a case study about how we cut latency" → `structure` × `narrative` → `outline-plan.md`.
- "I'm staring at a blank page — help me draft this design doc" → `draft` × `argument-memo`, loads `argument-memo.md`, emits `draft-scaffold.md`.
- "Write a first pass of this launch announcement" → `draft` × `general-prose` → `draft-scaffold.md`.
- "Draft a crisp project-update email" → `draft` × `general-prose` → `draft-scaffold.md`.
- "Make this conference talk actually land — give it an arc" → `persuade` × `talk-pitch`, loads `talk-pitch.md`, emits `persuasion-plan.md`.
- "Help me pitch this project to execs so they care" → `persuade` × `talk-pitch` → `persuasion-plan.md`.
- "Add narrative momentum to this engineering blog post" → `persuade` × `narrative` → `persuasion-plan.md`.
- "Frame this strategy memo as where we are vs where we could be" → `persuade` × `argument-memo` → `persuasion-plan.md`.
- "Structure an explainer around the steps a new user takes" → `structure` × `technical-doc` → `outline-plan.md`.

## Negative

Near-miss prompts that share keywords but should route to a **sibling skill**.

- "This draft is wordy — tighten it" → use `writing-audit` instead, because it's revising existing prose, not creating.
- "Copyedit this for grammar and consistency" → use `writing-audit` instead, because it's a mechanics pass on existing text.
- "Why does this section drag and bury the point?" → use `writing-audit` instead, because it's diagnosing an existing draft.
- "Design the information architecture for our whole docs site" → use `docs-design` instead, because it's documentation-as-a-system IA, not composing one piece.
- "How should our API reference and tutorials fit together as a set?" → use `docs-design` instead, because it's corpus architecture across a doc set.
- "Research what's known about RAG retrieval and write it up" → use `research` instead, because the work is source gathering, not composition craft.
- "Validate whether building this product is a good opportunity" → use `research` instead, because it's opportunity validation, not writing.
- "Review this signup form for usability friction" → use `ux-audit` instead, because it's product UX, not writing craft.
- "Audit our SDK's error messages for friction" → use `dx-audit` instead, because it's a developer-experience surface, not a piece of writing.

## Boundary / edge

- "Write the README for this repo" → default `draft` × `general-prose` (use `structure` only for an explicit outline/structure ask) when composing the README's prose and arc; if it's README-as-onboarding-IA or first-impression scoring, prefer `docs-design` or `dx-audit`.
- "Make our error messages clearer" → activates (`draft` × `general-prose`) only when the focus is the wording/craft of the copy; if it's error-UX taxonomy, affordances, or envelope design, prefer `dx-audit` / `dx-design`.

## Notes

- Cover the dominant phrasings: "outline", "structure", "draft", "first pass",
  "make it land", "give it an arc", "pitch", "frame".
- One negative per neighbor skill named in the intake brief: `writing-audit`,
  `docs-design`, `research`, `ux-audit`, `dx-audit`.
- Re-read after trigger-evals.json to confirm the two artifacts agree.
