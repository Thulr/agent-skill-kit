# writing-audit Activation Cases

## Positive

The skill should activate and route correctly (intent × genre → playbook →
scored report).

- "Tighten this PRD — it's bloated" → `revise` × `argument-memo`, loads `argument-memo.md`, emits `revision-report.md`.
- "Cut the clutter in this paragraph" → `revise` × `general-prose` → `revision-report.md`.
- "Make this how-to less wordy and easier to follow" → `revise` × `technical-doc` → `revision-report.md`.
- "Edit this announcement for clarity without losing my voice" → `revise` × `general-prose` → `revision-report.md`.
- "Copyedit this blog post for grammar and consistency" → `copyedit` × `general-prose`, loads `general-prose.md`, emits `copyedit-report.md`.
- "Proofread and check this spec for consistency" → `copyedit` × `technical-doc` → `copyedit-report.md`.
- "Why does my talk feel flat?" → `diagnose` × `talk-pitch`, loads `talk-pitch.md`, emits `diagnosis-report.md`.
- "This memo buries the recommendation — what's wrong structurally?" → `diagnose` × `argument-memo` → `diagnosis-report.md`.
- "Review this essay's structure — does it build?" → `diagnose` × `narrative` → `diagnosis-report.md`.
- "Score the stickiness of this launch post" → `diagnose` × `talk-pitch` → `diagnosis-report.md`.
- "Diagnose why this case study loses the reader halfway" → `diagnose` × `narrative` → `diagnosis-report.md`.
- "Proofread and tighten this exec summary" → `copyedit` × `talk-pitch` → `copyedit-report.md`.

## Negative

Near-miss prompts that share keywords but should route to a **sibling skill**.

- "Help me outline this RFC before drafting" → use `writing-design` instead, because it's structuring new writing.
- "Draft a first version of this talk" → use `writing-design` instead, because it's generating a first draft.
- "Give this blog post a narrative arc" → use `writing-design` instead, because it's adding structure to create, not critiquing.
- "Audit our docs site for retrieval and audience conflict" → use `docs-audit` instead, because it's documentation-as-a-system.
- "Why does the agent call the wrong tool from our docs?" → use `docs-audit` instead, because it's agent-readable docs, not prose craft.
- "Review our CLI's flags and help output for friction" → use `dx-audit` instead, because it's a developer-experience surface.
- "Heuristic review of this checkout flow" → use `ux-audit` instead, because it's product UX, not writing.
- "Research and summarize the state of LLM eval methods" → use `research` instead, because the work is a source-grounded report.
- "Review this signup form's labels and error states for usability" → use `ux-audit` instead, because it's a usability surface, not standalone prose.

## Boundary / edge

- "Review this microcopy on our settings screen" → activates (`revise` × `general-prose`) when the ask is the prose quality of the copy; if it's the control's usability or placement, prefer `ux-audit`.
- "Edit our API docs for clarity" → activates (`revise`/`copyedit` × `technical-doc`) for the prose itself; if it's reference structure, retrieval, or mode-mixing across the doc set, prefer `docs-audit`.

## Notes

- Cover the dominant phrasings: "tighten", "cut clutter", "copyedit",
  "proofread", "why does this drag/feel flat", "buries the point", "score".
- One negative per neighbor skill named in the intake brief: `writing-design`,
  `docs-audit`, `dx-audit`, `ux-audit`, `research`.
- Re-read after trigger-evals.json to confirm the two artifacts agree.
