# Audience Conflicts Playbook

## Scope

One interaction surface, two audiences at once: a **human visual user** who perceives layout, color, motion, and conversational copy, and an **agent actor** that perceives the same screen through structure — the accessibility tree, ARIA roles/labels/states, semantic HTML, and text — then chooses and fires an action, often on a person's behalf. A choice tuned for one audience can silently degrade the other: a control that lives only in a tooltip or color helps a sighted mouse user and vanishes for the agent (and for screen-reader users); a maximal "show everything" panel built for the agent buries the human. This surface names that trade-off and resolves it without forking the product into a human page and an agent page. It uses finding IDs **AGENT-UX-AUD-NNN** for human-vs-agent tension on the acting surface.

- **In:** human-only affordances (hover, color, icon, animation, spatial order) that carry load-bearing state or actions; conversational vs structured-field tension; maximal-context vs smallest-affordance pulls; hidden criticals (irreversible consequences, required inputs, auth scopes, retry-safety) reachable by only one audience; one-source-many-renderings vs forked human/agent surfaces.
- **Out:** the machine-readable perception contract in isolation (`machine-readable-state`); targeting and retry-safety mechanics (`deterministic-actions`); consent and confirmation UX (`approval-and-agency`); the *docs* cut of audience conflict (`docs-audit` / `docs-design`); human-only end-user usability (`ux-audit` / `ui-design`).
- **Intents this surface answers:** do, review, design.

## Grounding

- An agent reads a UI the way assistive tech does: through the accessibility tree and semantic structure, not pixels. So "visible to a sighted human" and "perceivable by an agent" are different guarantees — WCAG's text-alternative and name/role/value contracts are the same bar both audiences need.
- A human-only affordance — a fact or action exposed solely via hover, color, icon, spatial ordering, or animation, with no text/role/state equivalent — is invisible to both the agent and the screen-reader user. The fix that serves one serves both.
- Computer-use is stochastic and on-behalf-of a person, so any fact an agent must act on (irreversible consequence, required input, auth scope, whether a step already succeeded) has to live in structure on the action surface, not in transient toasts or fine print.
- The resolution is one source rendered many ways — page, ARIA, schema, text — not a forked human surface and agent surface that drift apart.

## Good signals

- The output names which audience benefits, which is harmed, and what evidence shows the harm (a screen-reader trace, an accessibility-tree dump, a failed agent run) before proposing a fix.
- Every load-bearing fact and action has both a human-visible rendering and a machine-readable path (text, role, state, schema) from the same source.
- One canonical source feeds multiple renderings; forked human/agent paths, where unavoidable, carry an explicit drift check.
- Color, icon, motion, and position are reinforcements, never the sole carrier of state or of an available action.
- Conversational copy coexists with structured fields/roles; warmth does not replace the contract.
- Context shown to the agent is the smallest that completes the task, while the human view stays scannable — neither audience is served the other's payload.
- Irreversible consequences, required inputs, and auth scopes appear inline on the action surface for both audiences.
- Disagreements between the two audiences are decided with evidence and recorded as AGENT-UX-AUD-NNN findings, not by whoever spoke last.

## Common failures

- **Average-audience mush** — copy tuned to offend neither audience ends up too vague for the agent to act on and too cluttered for the human to scan.
- **Conversational over contract** — friendly prose ("we'll take it from here") with no structured field, role, or state telling the agent what input is required or whether the step succeeded.
- **Forked surfaces that drift** — a separate "agent mode" or API view maintained apart from the human UI until one is stale and an agent acts on wrong state.
- **Context dumping at the agent** — exposing a maximal everything-panel "so the agent has it all," which raises cost, invites mis-targeting, and (when the human shares the surface) buries the primary action.
- **Hidden criticals** — destructive consequence, auth scope, or retry-safety shown only in a screenshot, animation, or paragraph the agent and the screen-reader user never reach.
- **Visual order as priority** — the most important action is "obvious" by layout to a human but unranked in the structure the agent reads.

## Heuristics

- **(do, review, design) Name the trade-off explicitly.** State which audience benefits, which is harmed, and what evidence shows the harm (accessibility-tree dump, screen-reader trace, failed agent run) before changing anything. An unnamed conflict gets resolved by whoever has the mouse.
- **(design, do) Keep the human affordance AND a machine-readable path.** Retain the hover, color, or animation for the sighted user, but mirror every load-bearing fact and action into text, role, state, or schema from the same source. The accessibility fix and the agent fix are usually one fix.
- **(design, review) One source, many renderings.** Prefer canonical state/actions rendered as page + ARIA + schema + text over a forked human page and agent surface. If forking is unavoidable, add a drift gate so they can't silently diverge.
- **(review, design) No hidden criticals on the action surface.** Irreversible consequences, required inputs, auth scopes, and retry-safety must never live only in hover, color, screenshot, or prose outside the action path — they belong inline, perceivable by both audiences (hand off the confirmation UX to `approval-and-agency`).
- **(design, do) Smallest affordance that completes the task.** Give the agent the least context and the fewest controls that finish the job, and keep the human view scannable; resist exposing a maximal panel that serves neither audience well.
- **(review, design) Reinforce with color/motion/order; never carry state with them alone.** Treat visual-only signals as redundant cues over a text/role/state primary, so a repeated agent run and a screen-reader pass both observe the same state.
- **(do, review) Diff the two perceptions.** Compare what a human sees against the accessibility-tree/text view an agent gets; any load-bearing element present in one and absent from the other is the finding (`AGENT-UX-AUD-NNN`).
- **(design) Decide conflicts with evidence, then record them.** When a genuinely irreducible human-vs-agent tension remains, log the trade-off and the chosen resolution as an AGENT-UX-AUD-NNN finding so the next change doesn't relitigate it blind.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Did you name who benefits, who is harmed, and the evidence? | The conflict is unresolved and undocumented | State the trade-off + evidence before changing anything |
| Does every load-bearing fact/action have both a visible and a machine-readable path? | One audience is blind to it | Mirror it into text/role/state/schema from the same source |
| Is there one canonical source feeding the renderings? | Human and agent surfaces will drift | Unify the source or add a drift gate |
| Is any state or action carried only by color/icon/hover/motion/order? | Agent and screen-reader users can't perceive it | Add a text/role/state primary; keep the visual as reinforcement |
| Is the agent given the smallest context that completes the task? | Cost, mis-targeting, and clutter rise | Trim to the minimal affordance; keep the human view scannable |
| Do criticals (irreversible/required/scope/retry) appear inline for both audiences? | A hidden critical fires unseen | Surface inline on the action path |

## Cross-references

- `machine-readable-state` — the perception contract (accessibility tree, ARIA, semantic structure) the machine-readable path depends on.
- `deterministic-actions` — stable targeting and retry-safety for the actions kept perceivable here.
- `approval-and-agency` — consent and inline confirmation UX for the criticals this surface forbids hiding.
- → `ux-audit` / `ui-design` for human-only end-user usability; → `docs-audit` / `docs-design` for the documentation cut of audience conflict; → `agent-dx` for the SDK/tool-schema and token-exchange mechanism; → `agent-ops` for operating the agent loop at runtime.
- `references/core/severity-rubric.md`, `references/core/score-rubric.md` — REVIEW scales; finding IDs `AGENT-UX-AUD-NNN` for human-vs-agent tension.
- `references/intents/{do,review,design}.csv` row `audience-conflicts` — the entry points.