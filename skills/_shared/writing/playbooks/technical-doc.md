# Technical & Task Doc Playbook

## Scope

- **In:** documentation organized around getting something done — how-to
  guides, procedures, runbooks, setup guides, explainers, and AI/agent
  playbooks. The unit of value is a completed user task.
- **Out:** documentation *systems* — IA across a whole doc set, retrieval, mode
  taxonomy, telemetry (→ the `docs-audit` / `docs-design` skills). A
  recommendation memo (→ `argument-memo.md`).
- **Intents this surface answers:** `structure`, `draft` (design); `revise`,
  `copyedit`, `diagnose` (audit).

## Grounding

- *Writing Software Documentation: A Task-Oriented Approach* (Thomas Barker,
  1998) — organize by what the user is trying to accomplish, not by features;
  analyze audience and tasks first; decompose into ordered steps; write
  minimally.
- *The Pyramid Principle* (Barbara Minto, 1987) — answer-first still applies to
  an explainer's framing.
- *The Sense of Style* (Steven Pinker, 2014) — the expert blind spot is the
  dominant failure in technical writing; define terms, show an example.

> This playbook is about *composing the prose and task structure of one doc*.
> For the architecture of a documentation **system**, route to `docs-design`.

## Good signals

- Sections map to user goals ("Deploy a preview", "Roll back a release"), not to
  product features or UI menus.
- Each procedure is a sequence of discrete, ordered steps with one action per
  step; the user never has to guess the order.
- Prerequisites and the expected end-state are stated before the steps.
- Reference material (options, parameters) is separated from task material (do
  this, then this).
- Terms a novice wouldn't know are defined or linked on first use.

## Common failures

- **Feature tour** — the doc walks the product's surface area instead of the
  user's goal, so the reader can't find the path for their task.
- **Fused steps** — one numbered step bundles three actions, or assumes an
  unstated precondition, and the reader falls off mid-procedure.
- **Curse-of-knowledge gaps** — the author skips the step that's obvious to
  them; the novice hits an undefined term or an unexplained jump.
- **Procedure/reference bleed** — lookup tables interrupt the steps, or the
  steps hide inside prose, so neither job is well served.
- **No success signal** — the reader can't tell whether the task worked.

## Heuristics

- **(structure, diagnose) Task orientation** — every section maps to a real
  user goal; headings name goals, not features.
- **(structure, draft) One action per step** — decompose procedures into
  discrete, ordered steps; split any step that bundles actions.
- **(structure) State pre- and post-conditions** — name prerequisites up front
  and the end-state the user is checking for.
- **(draft, revise) Write minimally** — cut elaboration that doesn't serve task
  completion; the reader is here to do something, not to read.
- **(revise) Close the blind-spot gaps** — read as the novice lens (see
  `audience-frame.md`); define the term, add the missing step.
- **(diagnose) Separate task from reference** — goal-driven steps and
  lookup/option content are different doc types; flag where they're tangled.
- **(copyedit) Consistent command and term forms** — one name per command,
  flag, and concept; mismatches read as different things.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Do sections map to user goals? | Reader can't find their task | Reorganize by task, not feature |
| Is it one action per step? | Reader falls off mid-procedure | Split fused steps |
| Are prereqs stated before the steps? | Steps fail opaquely | Move prerequisites up front |
| Can a novice follow it cold? | Blind-spot gaps strand them | Define terms; add the skipped step |
| Is there a success signal? | Reader can't confirm it worked | Add the expected end-state |

## Cross-references

- `references/core/structure-rubric.md` — task decomposition and ordering.
- `references/core/audience-frame.md` — the novice and implementer lenses.
- `references/core/clarity-rubric.md` — minimal, concrete line-level writing.
- `references/playbooks/argument-memo.md` — when the doc argues "whether," not "how."
- the `docs-design` / `docs-audit` skills — for the documentation *system*, not one doc.
