# ui-design Eval Cases

Activation + behavioral cases for `ui-design` — generatively producing and
polishing visual UI artifacts (screens, design systems, prototypes, decks,
motion, handoff bundles), including a self-polish anti-slop pass. Auditing an
existing interface's usability/accessibility with no new visual design is
`ux-audit`; developer-facing API/SDK/CLI surfaces are `dx-design`. Those
appear here as **negatives**.

## Static verification

```bash
bash skills/ui-design/evals/run-static-checks.sh
```

Verifies file presence, skill.json + trigger-evals contracts (name ==
ui-design), the one-layer intent-router well-formedness (7 intents, every
`detail_files`/`templates` entry resolves, no orphan references), SKILL.md
source-author cleanliness, and the SKILL.md word-count bound (<800).

## Behavioral protocol

Run each case in a fresh session with only this skill loaded. Passing means the
agent: activates for realistic UI-build prompts; on a bare invocation shows the
intent menu and waits (no file inspection, network, or writes); routes
`intent-router.csv` → one or more of the 7 intents → the row's `detail_files`
and `templates`; grounds in the brief/system/screenshots before inventing
visuals; emits a runnable/viewable artifact plus a design brief; and runs the
anti-slop self-polish pass.

---

## Case 1 — Bare activation menu
**Prompt:** `Use ui-design.`
**Expected:** loads `starter-scenarios.csv` + `intent-router.csv`; shows the intent menu with named starters on top; offers the mode choice; waits.
**Fail if:** inspects files, runs commands, or invents a design.

## Case 2 — Product screen polish
**Prompt:** `Make this dashboard look less like a generic AI template.`
**Expected:** routes `product-ui` (often plus `quality-review`); inspects the existing UI/system; emits a concrete `design-brief.md` + `ui-plan.md` before edits; applies the anti-slop pass.
**Fail if:** redesigns blindly without grounding, or skips the anti-slop review.

## Case 3 — Design system
**Prompt:** `Author a small design system for this app — tokens, components, preview pages.`
**Expected:** routes `design-system`; loads `design-systems.md`; produces token/component/preview requirements via `design-system-spec.md`.

## Case 4 — Prototype with variants
**Prompt:** `Prototype this onboarding flow with a tweaks panel for density and color.`
**Expected:** routes `prototype`; loads `prototypes-and-host.md`; maps variation axes; emits a runnable artifact + `prototype-handoff.md`.

## Case 5 — Deck
**Prompt:** `Turn these notes into an HTML slide deck with speaker notes.`
**Expected:** routes `deck`; chooses a slide system; asks only if audience or export target is unknown; emits `deck-plan.md`.

## Case 6 — Motion
**Prompt:** `Add subtle animated depth to this hero.`
**Expected:** routes `motion-scene`; checks reduced-motion and intensity.

## Case 7 — Handoff
**Prompt:** `Package this prototype for standalone HTML export and direct editing.`
**Expected:** routes `host-handoff`; checks bundling, direct edit, export, and limitations.

## Case 8 — Load discipline
**Prompt:** `Make a deck from these notes.` (clear `deck`)
**Expected:** loads `intent-router.csv`, then only the `deck` row's `detail_files` + `templates`. Does NOT load the prototype/design-system/motion playbooks.

---

# Negative cases — should not trigger (or should defer)

## N1 — Pure accessibility audit
**Prompt:** `Run a formal WCAG 2.2 accessibility audit of our checkout — no redesign.`
**Expected:** recognizes this is an **audit** of an existing interface with no new visual design; defers to `ux-audit`.
**Fail if:** produces a visual redesign for an audit-only request.

## N2 — Usability audit of an existing flow
**Prompt:** `Our signup form is confusing — list the heuristic violations.`
**Expected:** defers to `ux-audit` (usability audit, not visual production).

## N3 — Developer API design
**Prompt:** `Design the error envelope and pagination for our REST API before 1.0.`
**Expected:** recognizes a developer-facing surface; defers to `dx-design`.

## N4 — Developer CLI review
**Prompt:** `Review the developer experience of this CLI's --help output.`
**Expected:** defers to the DX skills; does not route through a UI intent.

## N5 — Architecture refactor
**Prompt:** `Refactor this service into clean architecture layers.`
**Expected:** recognizes a code-architecture task, not visual UI; declines.

---

# Edge cases

- Bare `UI designer` invocation shows modes and intents, then waits.
- If a design system is named but unavailable, ask for it or state the
  from-scratch fallback before inventing visuals.
- If asked to copy a third-party product's distinctive UI without evidence of
  ownership, refuse the copy and offer an original adjacent style.
- If host protocol files are not relevant to the target environment, skip them
  and document the portability assumption.
