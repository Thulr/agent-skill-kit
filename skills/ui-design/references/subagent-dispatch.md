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

## Preamble Before Dispatch

Before spawning sub-agents, emit a short user-facing preamble — 3–4 lines, no
more. Sub-agent fan-outs go silent for a minute or more; the preamble converts
that wait from a black box into an anticipated reveal.

The preamble must name:

- **Reviewers dispatched** (e.g., "visual-craft, user-task,
  implementation/handoff").
- **Artifact + use case** being reviewed.
- **Rough time estimate** ("~1–2 minutes," not a hard number).
- **What to watch for** — one sentence telegraphing the kind of finding the
  user should expect.

Example:

```text
Dispatching 3 reviewers (visual-craft, user-task, implementation/handoff)
against the checkout prototype. ~1–2 min.
Watch for: hierarchy that buries the primary CTA, copy that hides system
state, and motion that ignores reduced-motion preferences.
```

Skip for tiny single-role passes or hosts without streaming text.

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
