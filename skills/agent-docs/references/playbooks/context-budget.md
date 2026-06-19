# Context Budget Playbook

## Scope

Context budget is the load-budget discipline governing what an AI agent loads,
when, and from where — the spending plan behind every always-loaded file,
on-demand resource, and durable memory store an agent reads. This surface treats
the agent's working context as a scarce, measured resource: more always-loaded
text can lower task accuracy, not only raise token cost, so the default posture
is minimal-and-measured, with expansive material deferred to load-on-demand.

- **In:** the three tiers (always-loaded invariant rules / load-on-demand
  expertise, examples, schemas, playbooks / durable cross-session memory);
  context (seen now) versus memory (retrieved later) as distinct tiers;
  progressive disclosure of metadata, instructions, and resources; the
  everything-dump anti-pattern; budgeting always-loaded text against measured
  task success.
- **Out:** the trigger DESCRIPTION wording that decides whether a resource
  loads (see `tool-descriptions`); the AGENTS.md contract whose body must stay
  minimal (see `agents-md`); the curated retrieval index of fetch-first pages
  (see `llms-txt`); chunk anchors and stable URLs for retrieved docs (see
  `machine-reference`).
- **Intents this surface answers:** do, review, design.

## Grounding

- An agent's context window is a budget, not a backpack. Every token of
  always-loaded text competes for the model's attention; the tier system
  (always-loaded / load-on-demand / durable memory) exists to keep the
  always-loaded tier small and push everything expansive behind a trigger.
- Context is what the model sees now; memory is what it retrieves later. They
  are distinct tiers with distinct economics — a fact a future session needs
  belongs in durable memory or an externalized high-signal summary, not bloated
  into always-loaded prose that pays a per-turn tax.
- Progressive disclosure shows up across AGENTS.md, MCP, and skill systems:
  metadata is always loaded, instructions load on trigger, heavy resources load
  on demand. The budget is the discipline of keeping each rung as thin as it can
  be and still trigger correctly.
- Curation raises average task success; it does not guarantee worst-case
  behavior. A mandatory invariant left in markdown the model may skip is not
  enforced — that is the docs-as-reliability-fix trap, and it hands off to a
  deterministic gate.

## Good signals

- The always-loaded tier holds only minimal invariant rules; expansive
  expertise, examples, schemas, and playbooks live one fetch away under
  load-on-demand resources.
- Always-loaded context size is measured against task success, not assumed
  helpful — someone has checked that adding the text raised, not lowered,
  accuracy on a representative task set.
- Context and memory are separated: durable cross-session facts go to a memory
  store or externalized state, not into per-turn always-loaded prose.
- Progressive disclosure is wired correctly — metadata always present,
  instructions on trigger, resources on demand — so the model pays for depth
  only when it needs it.
- High-signal summaries front load-on-demand resources, so a context-bound or
  post-compaction agent can act on the summary without fetching the full body.
- Mandatory invariants live in deterministic gates (hooks/CI), with the markdown
  describing them rather than being the sole enforcement.

## Common failures

- The everything-dump: a large always-loaded file pastes schemas, examples, and
  edge-case prose into every session, lowering accuracy and raising cost at once.
- Treating more always-loaded context as monotonically helpful — adding text
  without measuring whether task success moved, so regressions go unnoticed.
- Conflating context and memory: cross-session facts are wedged into
  always-loaded prose (paying a per-turn tax) instead of a durable memory tier,
  or session-only context is mistaken for something that will persist.
- Flat loading with no progressive disclosure — every resource is always-on, so
  the model can never spend attention selectively.
- Pasting a source-of-truth into an always-loaded file instead of pointing to
  it, so the budget balloons and the copy drifts from the canonical source.
- The docs-as-reliability-fix trap: a load-bearing invariant ("never deploy from
  a dirty tree") lives only in always-loaded markdown, treated as enforcement
  when the model may simply not read or follow it.

## Heuristics

- **(do, review, design) Keep the always-loaded tier to minimal invariant
  rules.** The top tier is for the few facts every turn needs; expertise,
  examples, schemas, and playbooks belong in load-on-demand resources. If a line
  is not needed on most turns, it is not an always-loaded line.
- **(review, design) Measure always-loaded text against task success, don't
  assume.** Treat each always-loaded addition as a hypothesis: it must raise
  accuracy on a representative task set, not just feel useful. More text can
  lower accuracy — budget it, hand the measurement loop to `agent-test`.
- **(do, design) Separate context from memory explicitly.** Decide per fact:
  needed this turn (context) or needed across sessions (durable memory /
  externalized state). Cross-session facts go to a memory store or a high-signal
  summary, never into always-loaded prose that pays a per-turn tax.
- **(do, design) Wire progressive disclosure across three rungs.** Metadata
  always loaded, instructions on trigger, resources on demand. Each rung carries
  only what that level needs to do its job and route to the next.
- **(review, design) Point to the source-of-truth; do not paste it.** Place
  reference behind a fetch, task guidance in a skill, live actions behind a tool.
  An always-loaded file links the canonical source rather than embedding a copy
  that bloats the budget and drifts.
- **(do, review) Front every load-on-demand resource with a high-signal
  summary.** A context-bound or post-compaction agent should be able to act on
  the summary alone; the full body is there only when the summary is not enough.
- **(review, design) Route mandatory invariants to deterministic gates, not
  markdown.** Curation raises average success, not worst-case reliability. Any
  rule that MUST hold belongs in a hook or CI check; hand enforcement to
  `harden-repo-for-coding-agents` and let the doc describe, not enforce.
- **(review) Audit for the everything-dump first.** When accuracy is poor and
  the always-loaded surface is large, suspect overload before underload — trim
  to invariants and re-measure before adding more guidance.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is the always-loaded tier limited to minimal invariant rules? | Expansive prose is taxing every turn | Demote expertise/examples/schemas to load-on-demand resources |
| Has always-loaded text been measured against task success? | Bloat may be lowering accuracy unnoticed | Run an eval pass (`agent-test`); keep only additions that help |
| Are cross-session facts in durable memory, not always-loaded prose? | Memory is mistaken for context (or vice versa) | Move durable facts to a memory store / externalized summary |
| Is progressive disclosure wired (metadata / instructions / resources)? | Everything loads flat and always-on | Split into the three rungs; trigger depth on demand |
| Do load-on-demand resources start with a high-signal summary? | A compacted agent can't act without the full body | Add a summary-first block to each resource |
| Are mandatory invariants enforced by gates, not markdown? | A load-bearing rule can be silently ignored | Move it to a hook/CI gate (`harden-repo-for-coding-agents`) |

## Cross-references

- `agents-md` — the always-loaded repo contract whose body this budget keeps minimal.
- `llms-txt` — the curated fetch-first index that the load-on-demand tier points to.
- `tool-descriptions` — the trigger wording that decides whether a resource loads at all.
- `machine-reference` — the chunk summaries and stable anchors that survive retrieval and compaction.
- → `harden-repo-for-coding-agents` — moves mandatory invariants out of markdown into deterministic hooks/CI gates (the docs-as-reliability-fix hand-off).
- → `agent-test` — measures the always-loaded budget against task success so additions are proven, not assumed.
- Finding IDs `AGENT-DOC-CTX-NNN`.
- `references/intents/{do,review,design}.csv` row `context-budget`.