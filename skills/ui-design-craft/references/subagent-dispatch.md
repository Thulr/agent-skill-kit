# Subagent Dispatch

Use independent perspectives only when the host permits subagents and the task
is substantive enough to benefit. Do not spawn subagents for small tweaks,
purely mechanical changes, secret-bound work, or immediate blocking edits.

## Roles

### Visual-Craft Reviewer

Prompt: Review the artifact for visual specificity, hierarchy, typography,
spacing, color roles, radius consistency, component state coverage, icon
coherence, imagery strategy, and anti-slop tropes. Return only actionable
findings with severity and suggested fixes.

### User-Task Reviewer

Prompt: Assume the primary user and task named in the brief. Walk the screen or
flow in order. Identify where the next action, status, recovery path, or content
meaning is unclear. Separate usability risk from personal taste.

### Implementation and Handoff Reviewer

Prompt: Inspect whether the artifact can run, reload, be edited, export, and
handoff cleanly. Check direct-edit readiness, host protocol markers, static
markup, component states, responsive behavior, reduced motion, console errors,
and packaging notes.

## Dispatch Pattern

For reviews or edge passes, run all three roles independently and synthesize
disagreements. For design generation, use the roles after the first working
draft, not before; critique works better against something concrete.

## Sequential Fallback

When subagents are unavailable, run the lenses yourself in this order:

1. Visual craft.
2. User task.
3. Implementation and handoff.

Keep the findings separated until synthesis so one lens does not flatten the
others.
