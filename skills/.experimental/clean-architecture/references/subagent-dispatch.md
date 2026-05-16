# Subagent dispatch — three lenses for clean-architecture work

Three sub-agents, each held strictly in their lens, produce three
independent finding lists. The host agent synthesizes them, deduplicates,
preserves disagreements as open questions, and emits the template-shaped
output.

## When to dispatch

| Intent | Dispatch by default? | When to skip |
|--------|----------------------|--------------|
| audit | **Yes** | Single-file change with no architectural implications |
| design | **Strongly preferred** | A small design tweak where one lens dominates |
| refactor | **Optional** | Trivial mechanical refactor with no boundary changes |
| explain | **No** | Lens disagreement is not useful when the goal is grounded explanation |

## The three lenses

### Lens 1 — Dependency-auditor

**Prompt:** "You are auditing this code/design strictly for **dependency
direction**. Find every place an inner concern depends on an outer one,
every cycle, every framework or infrastructure type that has leaked
into the domain or application layer. Cite the playbook's heuristics by
number. Do not propose refactors — only findings. Do not score the
overall surface — only individual findings with severity (0-4 from
`severity-rubric.md`)."

**Anchors on:** dependency-rule violations, layer leakage, framework
coupling, anti-corruption-layer absence between contexts.

### Lens 2 — Boundary-designer

**Prompt:** "You are evaluating this code/design for **boundary
quality**. Are seams in the right places? Are interfaces minimal and in
the core's vocabulary? Are deep modules (simple interface, rich
implementation) preferred over shallow ones? Are ports symmetric? Cite
the playbook's heuristics. Propose better-shaped boundaries with brief
justification. Do not rank refactor sequence — that is the next lens."

**Anchors on:** port symmetry, deep modules, interface minimality, layer
mechanics, leaky abstractions.

### Lens 3 — Refactor-pragmatist

**Prompt:** "You are sequencing a refactor toward better architecture
under **realistic constraints**: feature work continues, big-bang is
forbidden, every step must be reversible. Use strangler-fig,
branch-by-abstraction, parallel-change, characterization tests as
safety nets. Sequence findings from the other lenses; do not introduce
new findings yourself. Estimate effort per step (S/M/L); name what
breaks if the refactor stops partway."

**Anchors on:** smallest-reversible-step, strangler-fig pathways,
characterization tests, parallel-change, expand-contract migrations.

## Dispatch template

When the host has a delegation primitive, fan out:

```
Spawn three subagents in parallel.

Agent 1 (dependency-auditor): <Lens 1 prompt above>, applied to <surface>.
Read references/playbooks/<surface>.md and references/core/severity-rubric.md
and references/core/glossary.md before starting.

Agent 2 (boundary-designer): <Lens 2 prompt above>, applied to <surface>.
Read references/playbooks/<surface>.md and references/core/glossary.md
before starting.

Agent 3 (refactor-pragmatist): <Lens 3 prompt above>, applied to
<surface>. Read references/playbooks/<surface>.md and
references/core/severity-rubric.md before starting. Wait for agents 1
and 2 to complete; sequence their findings.

Each agent returns: a list of findings/proposals with severity, citing
heuristic numbers from the playbook. No prose summary at the top.
```

If the host has no delegation primitive: run the three lenses
sequentially in one head, switching lens explicitly between passes.
The discipline of switching lens matters more than the parallelism.

## Synthesis step

After the three lenses return, the host agent:

1. **Deduplicate.** When two lenses report the same finding, keep one
   with the higher-severity attribution.
2. **Preserve disagreements** as `Open questions` in the output. Do not
   resolve them silently — name the disagreement and the trade-off
   between the lenses' framings.
3. **Order by severity** (4 → 0).
4. **Map to template.** Emit the intent-appropriate template
   (`templates/<intent>.md`) populated from the synthesized list.

## Fan-out variant (surface = `all`, audit only)

For `audit` with `all`-fanout, the structure inverts: spawn one agent
per surface (5 agents, one each for dependency-rule, boundaries,
domain-model, bounded-context, cross-cutting). Each surface-agent runs
all three lenses sequentially inside itself and returns a per-surface
finding list. The host synthesizes across surfaces and emits
`templates/audit-report-multi.md`.
