# Subagent Dispatch

**Default for `diagnose`** and wide-scope reviews; optional for a broad
`persuade`/`structure` design space; skip for a single tightly-scoped
paragraph or a deterministic copyedit.

Spawn **reader-lens** sub-agents in parallel. Each agent reads the same draft
plus the chosen genre playbook and its `core_refs`, then returns findings from
one vantage only — it does not rewrite. The lenses are defined in
[`core/audience-frame.md`](./core/audience-frame.md):

- **time-pressed scanner** — skims headings and first lines
- **skeptical decision-maker** — hunts the ask, stakes, and evidence
- **first-time / novice reader** — hits undefined terms and assumptions
- **implementer** — must act from the text (instructions only)

Pick the 2–3 lenses that fit the genre:

- argument-memo → scanner + decision-maker
- technical-doc → novice + implementer
- talk-pitch → scanner + decision-maker
- narrative → novice + decision-maker
- general-prose → scanner + (novice or decision-maker)

**Each agent returns:** findings as `severity (0–4) — location — one-line fix`,
grounded in the playbook heuristics, with no rewrite of the draft.

**Synthesis:** dedupe overlapping findings (keep the highest severity), order
by severity, and attribute which lens surfaced each. If the host has no
delegation primitive, run the lenses sequentially yourself and synthesize the
same way.
