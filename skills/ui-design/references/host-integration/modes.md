# Modes — Guided Draft / Autopilot / Grill Me

Shared mode contract for skills that take more than a few seconds to produce
output. Picking a mode is the user's first agency lever: it sets depth-vs-speed
*before* the skill starts grinding through routers, lenses, or fan-outs.

Offer the mode choice at **bare invocation**, alongside the scenario or
route menu, and again whenever a request is materially ambiguous about how
much back-and-forth the user wants. Loading the small router CSV (or
starter-scenarios CSV) that backs that menu is fine — the menu would be
empty without it. What should *not* load before the user picks an intent
and surface is the heavier grounded context: playbooks, lenses,
intent-specific files, and per-surface references.

## The three modes

### Guided Draft (default)

One **optionized** question at a time, and only when the answer changes the
output's shape (audience, format, scope, design-system binding, variation
count, …). Each question carries 3–4 likely choices plus a freeform path.
Proceed as soon as the blocker is resolved; don't accumulate questions.

Use when the user has dropped a vague brief and you can decompose it into a
handful of decisions.

### Autopilot

Proceed from available context. Make conservative calls and **state every
assumption** in the output (in a "Decisions" or "Assumptions" section).
Stop only for:

- missing assets, credentials, or external systems the skill can't reach;
- legal/IP risk or destructive edits;
- a request that meaningfully changes scope (not just polish).

Use when the user has said "decide for me" / "just do it" / "you have enough
context" — or when the task is genuinely low-risk and the cost of one bad
guess is small compared to the cost of an extra round-trip.

### Grill Me

Open-ended questions, one at a time, until audience, constraints, success
criteria, and trade-offs are locked. Don't draft until the picture is
complete.

Use when the user explicitly asks to be challenged, when the request hints at
strategic uncertainty ("I'm not sure what we're optimizing for"), or when a
wrong call early would compound through the rest of the work.

## Mode discipline

- **Pick one and name it in the output.** The artifact (audit report, design
  doc, review, ledger entry) records which mode was used. Future runs and
  reviewers can then read the artifact in the right register.
- **Mode changes are explicit.** If the user says "actually, just decide" mid-
  conversation, acknowledge the switch from Guided Draft to Autopilot and
  proceed. Don't silently change registers.
- **Modes don't change rigor.** They change how much the user is asked, not
  how grounded the output is. Severity rubrics, ID schemes, grounding-source
  citations, and verification rules apply in every mode.

## When NOT to ask the user to pick

- Concrete invocation where the intent and surface are inferable: default to
  Guided Draft and proceed; the user can override by saying so.
- Tiny mechanical changes (rename, one-line fix, format-only edits).
- Resume / closeout flows on an existing ledger — the mode is inherited from
  the original run unless the user says otherwise.
