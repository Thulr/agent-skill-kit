# Usability Playbook

## Scope

Use for user-facing screens, flows, dashboards, onboarding, settings, checkout,
and task completion. Do not use for developer-facing setup, docs, CLIs, SDKs,
or APIs; those route to `dx-heuristics`.

## Grounding

- Norman: users need visible signifiers, feedback, constraints, and safe
  recovery when slips happen.
- Nielsen: evaluate visibility, match to the user's world, control,
  consistency, prevention, recognition, efficiency, minimalism, recovery, and
  help.
- Krug: users scan; the best interface makes the next action obvious without a
  tutorial.

## Good signals

- Primary task and next step are obvious within the current state.
- Controls look interactive and communicate state, consequences, and feedback.
- Users can recover from mistakes without re-entering work.
- Labels use the user's language, not internal product vocabulary.
- Repeated workflows have efficient shortcuts without hiding the default path.

## Common failures

- Important state is invisible or only implied by color.
- CTAs compete, change labels, or appear before prerequisites are clear.
- The interface asks users to remember prior context or hidden rules.
- Empty, loading, and error states lack a next action.
- Copy tells users what happened but not what they can do.

## Heuristics

- **Visible next action** *(usability-audit)* - each state has one clear primary action or a deliberate choice set.
- **Feedback after action** *(usability-audit)* - every user action gets timely confirmation, progress, or failure feedback.
- **Recognition over recall** *(usability-audit, navigation-review)* - labels, breadcrumbs, examples, and previews reduce memory load.
- **Reversible by default** *(usability-audit, error-recovery)* - risky actions have undo, confirmation, or draft preservation.
- **User language** *(usability-audit)* - terms match what the target user would say while doing the task.

## Quick diagnostic

Ask: "What is the user trying to do, what do they think will happen next, and
what evidence does the screen provide?" If the screen cannot answer all three,
the finding is not just aesthetic.

## Cross-references

- Use `forms.md` for field-level work.
- Use `navigation.md` for IA and wayfinding.
- Use `error-recovery.md` when the issue appears after failure or before a
  destructive action.
- Use `docs-experience-heuristics` when the issue is help/documentation
  strategy across product help, docs sites, or agent-readable content.
