# Target personas

Pick the persona that best matches the audience for this output. The choice shapes vocabulary,
depth, and which trade-offs to surface. The audience here builds the **interaction surface an
agent acts through** — not docs an agent reads (`agent-docs`), an SDK it calls (`agent-dx`), or a
human-only product UX (`ux-audit` / `ui-design`).

## Persona A — Engineer building an agent-facing surface mid-change (DO)

Making a UI, app, or computer-use target an agent must perceive and act on right now, and wants
it usable by an agent without over-building. Comfortable with their framework; not looking for an
accessibility-theory lecture.

- **Speak to:** exposing state/actions as structure (roles, labels, text), targeting controls by
  a stable handle, making a retried action safe, gating an irreversible action in-path.
- **Avoid:** a full accessibility rewrite for one control; ungated destructive actions.

## Persona B — Product/platform lead auditing agent usability (REVIEW)

Owns a judgment about whether an agent can actually use the surface: can it perceive state, target
actions, act within gated authority, and is the human/agent trade-off resolved. Wants scored
findings and a short "fix three first" list, not a re-platforming.

- **Speak to:** human-only affordances, coordinate-only targets, non-idempotent actions, ungated
  irreversible actions, missing on-behalf consent, unnamed trade-offs.
- **Avoid:** prescribing a vendor; treating every gap as a blocker regardless of project scale
  (calibrate).

## Persona C — Architect designing the agent-facing surface (DESIGN)

Deciding the minimal interaction surface an agent acts through: the machine-readable state, the
stable action handles, the approval/authority gate, the human/agent dual path. Wants the smallest
surface that earns its place, with clear trade-offs.

- **Speak to:** structured state + observable results, semantic handles + idempotency, the
  mechanical-vs-judgment gate + scoped on-behalf consent, one-source-many-renderings.
- **Avoid:** speculative agent affordances; ungated autonomy; an agent-only fork that drifts.

## Persona D — Lead hardening a UI for agent use under deadline

Cannot rebuild the UI. Needs a sequenced plan to close the gaps (expose state, stabilize handles,
gate irreversible actions, add on-behalf consent) with a safety net at every step.

- **Speak to:** smallest reversible step, adding a machine-readable path beside the human one,
  gating a destructive action before trusting an agent on it, what breaks if hardening stops at
  step N.
- **Avoid:** "first make everything accessible"; sequences that block the human UI.

## Default persona

When the prompt does not signal a clear audience, assume **Persona A** for DO, **Persona B**
for REVIEW, and **Persona C** for DESIGN, and state the assumption so the reader can redirect.
