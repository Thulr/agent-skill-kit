# Glossary

Terms used across the agent-ux playbooks. Definitions are operational, not exhaustive.

- **Agent-UX** — the design of an interaction surface (a product UI, app, or computer-use target)
  for an **AI agent as the end user** — one that perceives the surface, chooses an action, and
  acts, often on a human's behalf. The agent-actor analog of human UX.
- **Computer-use** — an agent driving a graphical or web surface built for humans, by perceiving
  its structure and issuing actions.
- **Accessibility tree** — the structured, semantic representation of a UI (roles, names, states,
  values) that assistive tech and agents read instead of pixels.
- **ARIA role / accessible name / state** — the semantic role of a control, its machine-readable
  label, and its current state — the handles an agent perceives and targets by.
- **Semantic handle** — a stable way to target a control (role + accessible name, a documented
  action, a stable test id), as opposed to pixel coordinates or brittle XPath.
- **Human-only affordance** — a control or rule conveyed only by a tooltip, hover, icon, color,
  spatial ordering, or animation, with no text/role/schema equivalent — invisible to an agent and
  to screen-reader users.
- **Observable result** — an action outcome reflected in machine-readable state (not only a
  transient toast or a visual cue), so an agent can tell whether the action succeeded.
- **Idempotency / retry-safety** — the property that repeating or mis-firing an action does not
  double-execute (double-charge, double-post); essential because computer-use is stochastic.
- **In-path confirmation** — a confirmation for an irreversible action presented within the action
  flow itself, not buried in hover, fine print, or a separate page.
- **Mechanical vs judgment** — the useful split for agent agency: routine reversible actions the
  agent takes; irreversible/authority-crossing actions (payments, deletions, permission grants,
  external sends) surface for human confirmation.
- **On-behalf / delegated session** — an agent acting as a user; the product makes this visible
  ("an agent is acting on your account") and the consent is scoped and revocable. (The SDK
  token-exchange *mechanism* is `agent-dx`; the product consent UX is here.)
- **Scoped, revocable consent** — permission for an agent to act that is limited in scope and can
  be withdrawn, surfaced to the user.
- **Audience conflict** — a choice that serves a human visual user but harms an agent actor on the
  same surface, or vice versa.
- **Dual path (visible + machine-readable)** — keeping the human affordance while duplicating
  load-bearing facts/actions in text, role, or schema an agent can read.
- **One source, many renderings** — one canonical state/action source rendered for both a human
  and an agent, over independently maintained forks.
- **No hidden criticals** — irreversible consequences, required inputs, auth scopes, and
  retry-safety never live only in hover, color, screenshot, or prose outside the action surface.
- **Smallest affordance** — the least interaction surface that still lets the agent complete the
  task.
