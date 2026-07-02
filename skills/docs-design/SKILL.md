---
name: docs-design
description: "Use to DESIGN or MEASURE documentation — plan or reshape a docs/help/agent-readable surface before implementation (IA, structure, examples, error copy, versioning, accessibility), or define telemetry, CI gates, retrieval evals, and feedback loops. Triggers on 'design our docs IA', 'how should we structure the quickstart/reference', 'set up docs CI gates / freshness checks'. Do NOT use to AUDIT or debug existing docs (use docs-audit)."
license: MIT
---

# Docs Design

Documentation-experience design and measurement for any surface someone reads
to learn, integrate, recover, or retrieve — developer docs, end-user help, and
agent-readable docs. Applied *before* the docs exist (design) or to keep them
honest over time (measure). Provenance lives in `skill.json`; this file is
runtime routing only.

**Produces:** a `design-doc.md` — a concrete proposed structure (source of
truth, renderings, IA, audience paths, acceptance criteria) — or a
`measurement-plan.md` — signals, thresholds, owners, actions, and release gates.

## Boundaries

Do NOT use to AUDIT or debug existing docs (use docs-audit), to design a code package's developer experience — API/SDK/CLI shape, errors, first-run flow (use dx-design), for end-user visual UI design (use ui-design), or repo agent hardening (use harden-repo-for-coding-agents), or agent-native docs — AGENTS.md, llms.txt (use agent-docs).

## Core principle

**Decide the source of truth and the audience's job before you write.** The
cheapest time to fix a docs problem is before content sprawls across mixed-mode
pages and divergent sources; name the canonical artifact and the page shape
concretely rather than describing principles abstractly.

## Activation

- **Bare invocation** ("use docs-design", "design our docs", "start"): show a compact menu: mode choice (guided / autopilot / grill me?) and numbered intents from the router. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with both intent and surface inferable: skip to step 3.
- **Ambiguous invocation**: ask one — e.g., *"Are you designing a new docs surface or defining measurement/telemetry?"* or *"Is this for developer docs, end-user help, or agent-readable surfaces?"*

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to one
   of: `design`, `measure`. Ambiguous → ask once. (Auditing or debugging
   *existing* docs instead? That is `docs-audit`.)
2. **Pick surface.** Load the intent's CSV from
   `references/intents/<intent>.csv`. Match to one or more surfaces. Ambiguous →
   ask once with the CSV menu.
3. **Load grounded context.** Load only the chosen CSV row's files: one playbook
   from `references/playbooks/<surface>.md` plus its `core_refs`. Do not load
   other playbooks.
4. **Identify the target audience** from `references/core/personas.md` and the
   shared `references/core/audience-matrix.md` — the design is *for* a specific
   audience and task; name who is helped and who could be harmed.
5. **Name the proposed structure (design) or the metric contract (measure).**
   Apply the playbook heuristics tagged for the intent. For `design`, produce a
   concrete structure — source of truth, renderings, IA, and the audience paths
   — not abstract advice. For `measure`, define each signal, threshold, owner,
   and action so a number can trigger work. For a wide space, optionally dispatch
   parallel sketches by audience lens (developer, end user, agent) and
   synthesize the strongest; preserve audience disagreements.
6. **Emit output.** Design → `templates/design-doc.md`: target audience, proposed
   structure, audience paths, acceptance criteria, risks and trade-offs.
   Measure → `templates/measurement-plan.md`: metrics table, gates and evals,
   baseline plan, caveats, reporting cadence.

> **Wrong direction?** If the user says this isn't what they meant, go back to step 1 (Pick intent) — do not patch in the wrong direction. Restate the corrected understanding and re-plan.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the target audience, the playbook(s) applied, the concrete
proposed structure or metric contract, the grounding sources from
`skill.json.inspired_by`, and acceptance criteria checkable by reading the
artifact or running a check.

## Reference map

- `references/intent-router.csv` — level-1 router (design / measure).
- `references/intents/<intent>.csv` — level-2 router (surface) per intent.
- `references/playbooks/<surface>.md` — surface playbooks (shared with docs-audit).
- `references/core/personas.md`, `references/core/audience-matrix.md` — audiences.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `templates/design-doc.md`, `templates/measurement-plan.md` — output shapes.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.
