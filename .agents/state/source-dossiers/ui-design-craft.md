---
source: ui-design-craft
status: draft-created
date: 2026-05-21
---

# UI Design Craft Source Dossier

## Source Seeds

- `claude-design-workflows/`: designer workflow, question discipline, design
  systems, content, visual craft, components, motion, prototypes, decks,
  output formats, environment capabilities, 2D animation, 3D/depth effects,
  and anti-slop guidance.
- `claude-design-host-integration/`: artifact host protocols for tweak panels,
  fixed-canvas scaling, speaker notes, mentioned elements, direct edit,
  bundling, export, and handoff.

## Public Shape Decision

Single-layer routing. The source set has seven practical invocation families
that share vocabulary and templates: product UI, design systems, prototypes,
decks, motion scenes, host handoff, and quality review. A two-level matrix
would add ceremony without a clean orthogonal second axis.

## External Grounding Checked

- W3C WCAG 2.2: current W3C Recommendation baseline for web accessibility.
- Nielsen Norman Group 10 Usability Heuristics: broad interaction-design
  heuristics, updated page checked.
- Apple Human Interface Guidelines: platform visual hierarchy, layout, and
  motion guidance.
- GOV.UK Design System: component and pattern guidance with coded examples.
- Material Design 3 Foundations: system vocabulary for color, type, motion,
  and component consistency.
- MDN `prefers-reduced-motion`: confirms browser feature behavior and
  reduced-motion user preference semantics.

## Skill Output

Created `skills/ui-design-craft/` as a draft public skill with runtime
`SKILL.md`, `skill.json`, use-case registry, routed references, artifact
templates, activation cases, trigger evals, and static checks.
