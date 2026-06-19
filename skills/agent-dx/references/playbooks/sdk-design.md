# SDK Design Playbook

## Scope

The shape of an AI/Agent SDK as a surface an agent (or an agent-building
developer) drives: streaming altitudes, the agent loop and its stop
conditions, context compaction, result verification, sub-agent handoffs, the
two standardizable edges (tool edge and client edge), opaque-artifact
round-tripping, and cross-provider honesty.

- **In:** loop ownership and stop predicates, streaming shape, compaction,
  verify-don't-trust, handoff semantics, the tool and client edges, provider-agnostic
  dispatch.
- **Out:** the *contents* of tool definitions and the trust boundary (see
  `tools-and-mcp.md`); structured-output validation (see
  `structured-output.md`); error envelopes and retry (see
  `errors-and-retry.md`); instrumentation (see `sdk-telemetry.md`).
- **Intents this surface answers:** do, review, design.

## Grounding

- **AI SDKs are a superset of HTTP-client SDKs.** A well-designed AI SDK
  inherits the whole HTTP-client floor — typed errors, jittered backoff with
  retry budgets, streaming iterators, sensible defaults — and adds the surface
  that exists because the call is stochastic, multi-step, and emits typed
  artifacts the caller must round-trip. The inherited floor is human-developer
  DX; this playbook is the agentic delta.
- **A stochastic loop will sometimes claim success it did not achieve.** "Done"
  must mean verified, not asserted — the SDK gives callers a deterministic
  checkpoint, not just the model's word.
- **Owning the loop means owning compaction and continuity.** Long runs
  exhaust the context window; an SDK that runs the loop must compress it,
  expose the compaction point, and externalize state, or a later step silently
  loses a fact an earlier one had.

## Good signals

- Streaming ships at two altitudes: a raw event iterator
  (`message_start` / `content_block_delta` / `message_stop`) and a higher-level
  accumulator with `.snapshot` / `get_final_message()`. UI consumers paint from
  the accumulator; infrastructure logs from the events.
- The agent loop has a declarative stop predicate
  (`stopWhen: stepCountIs(n) | hasToolCall("submit")`), per-step callbacks, and
  a turn cap. APIs that deliberately do *not* loop document the
  `stop_reason: "tool_use"` contract so callers know loop ownership is theirs.
- Stop conditions are paired with a deterministic post-step check (tests ran,
  file written, side effect observed), so the loop terminates on verified work.
- The loop owns compaction: the window is compressed on long runs, the
  compaction point is exposed, and state is externalized (files, a durable
  event log) so it survives a restart.
- Sub-agents/handoffs are first-class, and the SDK documents *which* semantics
  it implements — agent-as-tool (caller keeps the loop) vs explicit handoff
  (control and session transfer).
- The SDK names both edges it sits between: the tool edge (what the model can
  call) and the client edge (how a host/editor drives the session); a standard
  client edge lets callers swap agent backends without re-integrating.
- Opaque reasoning artifacts (thinking blocks, reasoning items) are a typed
  "must echo unchanged" category and survive serialization across turns.
- Provider-agnostic dispatch documents where features lowest-common-denominator
  away; per-provider capabilities are discoverable, not implied.

## Common failures

- Streaming returns raw chunks with no typed accumulator; every caller
  reassembles them by hand.
- The agent loop is buried with no stop predicate, no per-step callback, and a
  turn cap that is either too tight to finish real work or too loose to bound
  cost.
- The loop trusts the model's "I'm done" with no verification step; a
  hallucinated success ships.
- Owning the loop without owning compaction: long runs hit the context limit,
  or naive compaction drops a fact a later step needs ("compaction amnesia").
- Handoff semantics are unstated, so callers cannot tell whether control
  returns to them or transfers away.
- Reasoning blocks are discarded by the serializer; the next turn breaks
  because the continuity signature does not validate.
- A provider-agnostic abstraction silently drops prompt caching, citations, or
  reasoning blocks, and leaks the first time a provider-specific feature is
  needed.

## Heuristics

- **(design, review) Inherit the HTTP-client floor first.** Apply the typed
  errors, jittered retries, streaming iterators, and webhook verification of a
  good client SDK *before* the AI-specific surface; they are not optional
  because the body is a `messages[]` array. The human-DX SDK skills own that
  floor.
- **(design, review) Stream at two altitudes.** Expose the raw event iterator
  *and* a typed accumulator; do not force one consumer to pay the other's cost.
- **(design, review) Make stop conditions declarative.** If the SDK owns the
  loop, expose `stopWhen` predicates, per-step callbacks, and a turn cap. If it
  does not, document the `stop_reason` contract so callers own the loop
  deliberately.
- **(do, review) Verify the work, don't trust the report.** Pair every stop
  condition with a deterministic post-step check so "done" is observed, not
  asserted — the single highest-leverage guard against a stochastic loop
  shipping a false success.
- **(design) Compaction and state are loop-owned.** Owning the loop means
  compressing the window, exposing the compaction point, and externalizing
  durable state; treat silent fact-loss as a documented failure mode, not a
  free optimization.
- **(design) Name the handoff semantics.** Document whether a sub-agent is
  agent-as-tool (caller keeps the loop) or an explicit handoff (control +
  session transfer); the fork is loop ownership, not team size.
- **(design) Expose both edges.** An SDK that owns the loop should speak a
  stable client edge (so callers swap backends) as well as a tool edge — not
  only the tool edge.
- **(design, review) Round-trip opaque artifacts.** Give the type system a
  "must echo unchanged" category and preserve it through serde; losing it is a
  continuity bug, not a cosmetic one.
- **(review) Be honest across providers.** A provider-agnostic layer documents
  where capability is lost and makes per-provider features discoverable instead
  of pretending parity.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does streaming expose both raw events and a typed accumulator? | Callers reassemble chunks | Ship two-altitude streaming helpers |
| Does the agent loop have declarative stop conditions + a turn cap? | Unbounded cost or premature stop | Expose `stopWhen` + turn cap + per-step callbacks |
| Is each stop paired with a deterministic verification step? | Hallucinated success ships | Add a post-step check (tests/file/side effect) |
| If the SDK owns the loop, does it own compaction + durable state? | Context exhaustion or compaction amnesia | Compress the window, externalize state, expose the point |
| Are handoff semantics documented (agent-as-tool vs transfer)? | Callers can't tell who owns the loop | State the delegation semantics in the contract |
| Are opaque reasoning artifacts round-tripped intact? | Continuity breaks next turn | Add a typed "must echo" category preserved through serde |

## Cross-references

- `tools-and-mcp.md` — the tool definitions, hooks, and trust boundary the loop
  calls into.
- `structured-output.md` — typing and validating what a step returns.
- `errors-and-retry.md` — what a failed step hands back to the model.
- `sdk-telemetry.md` — the per-step spans that make a loop reconstructable.
- → `dx-audit` / `dx-design` (`sdk`, `errors`, `telemetry`) for the inherited
  human-developer HTTP-client floor.
- `references/core/severity-rubric.md`, `references/core/score-rubric.md` —
  REVIEW scales; finding IDs `AGENT-DX-SDK-NNN`.
- `references/intents/{do,review,design}.csv` row `sdk-design` — the entry points.
