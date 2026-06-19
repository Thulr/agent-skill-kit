# Structured Output Playbook

## Scope

How an SDK turns a stochastic model into a typed result a caller can branch on:
schema-typed output, the two guarantee levels (validate-then-repair vs
constrained decoding), refusal as a typed field, and semantic retry distinct
from transport retry. Also covers the skill's own machine-readable contract
files (`SKILL.md` / `skill.json`) as an agent-facing schema.

- **In:** native-schema output, decode-time vs post-hoc guarantees, refusal
  typing, semantic-retry design, agent-facing contract files.
- **Out:** the tool schema a tool *accepts* (see `tools-and-mcp.md`); the error
  envelope thrown on unrecoverable failure (see `errors-and-retry.md`); the
  loop that calls generation (see `sdk-design.md`).
- **Intents this surface answers:** do, review, design.

## Grounding

- **Schema-first beats string-first.** A structured-output API accepts a native
  schema type and validates on the way out; "ask the model for JSON and hope"
  is not structured output. The typed result is the contract; the raw text is a
  fallback for debugging.
- **The two guarantee levels are not interchangeable.** Validate-then-repair
  (`.parse()` + semantic retry) catches a bad object *after* generation;
  constrained/structured decoding makes illegal tokens unreachable *during*
  generation. Function calling names the tool interface; structured generation
  names the decode-time guarantee — production stacks should not collapse them.
- **A refusal is a valid outcome, not an error.** A model declining to answer is
  a typed state the caller handles, distinct from a transport failure or a
  validation failure.

## Good signals

- Structured outputs accept a native schema (Zod, Pydantic, JSON Schema) and
  round-trip a typed result; `.parse()` / `generateObject({ schema })`
  validates and returns a typed object.
- Model refusals surface as a typed field, not a status code or a magic string
  the caller must pattern-match.
- On validation failure the API throws a typed error with the raw text
  attached, so the caller can inspect what the model actually produced.
- Validation-error retries are a first-class parameter: a schema failure
  triggers a semantic retry with the validator's message appended to the next
  request — distinct from an HTTP retry.
- The docs state which guarantee level applies (post-hoc repair vs constrained
  decoding) so callers know whether illegal output is impossible or merely
  caught.
- The skill's own `SKILL.md` frontmatter and `skill.json` read as a stable,
  machine-parseable contract: an agent can route from them without prose
  inference.

## Common failures

- "Structured output" means the SDK asks for JSON and returns a string; there
  is no schema, no validation, no refusal field, no typed result.
- A validation failure triggers an HTTP retry instead of a semantic retry, so
  the model gets the same prompt back and emits the same broken JSON N times.
- Refusals are folded into the error path, so a deliberate decline is
  indistinguishable from a 500 and the caller cannot branch.
- The two guarantee levels are conflated: the docs imply illegal output is
  impossible when the SDK only validates and repairs after the fact.
- The raw model text is discarded on a parse failure, leaving no way to debug
  why validation failed.

## Heuristics

- **(design, review) Accept a native schema and round-trip a typed object.**
  Take the language's schema type, validate on the way out, and return a typed
  result — not a string the caller re-parses.
- **(design, review) Surface refusals as a typed field.** A model decline is a
  first-class outcome the caller branches on, not a status code and not an
  exception bucketed with transport errors.
- **(design) Keep semantic retry distinct from transport retry.** A `max_retries`
  for validation failures appends the validator's message to the next request;
  HTTP retries follow the client-floor backoff rules. Conflating them returns
  the same broken object repeatedly — a design smell.
- **(design, review) Name the guarantee level.** State whether the API does
  validate-then-repair (catches bad output after generation) or constrained
  decoding (makes illegal tokens unreachable); do not let callers assume the
  stronger guarantee from the weaker mechanism.
- **(do, review) Preserve the raw text on validation failure.** Attach the raw
  model output to the typed error so a failed parse is debuggable, not opaque.
- **(design, review) Treat the skill's contract files as agent-facing schema.**
  `SKILL.md` frontmatter and `skill.json` are read by an agent to decide routing;
  keep them stable, machine-parseable, and free of prose an agent must infer
  from — the same schema-first discipline applied to the skill itself.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does structured output accept a native schema and return a typed object? | Callers parse JSON strings | Add `.parse(response_format=…)` / `generateObject({ schema })` |
| Are refusals a typed field distinct from errors? | A decline looks like a 500 | Add a typed refusal field |
| Is semantic retry distinct from transport retry? | Same broken JSON returned N times | Add `max_retries` that appends validator messages |
| Is the guarantee level (repair vs constrained) documented? | Callers assume impossible-illegal output | State decode-time vs post-hoc in the contract |
| Is raw text preserved on validation failure? | Failed parses are undebuggable | Attach raw output to the typed error |

## Cross-references

- `sdk-design.md` — the loop step that calls generation.
- `tools-and-mcp.md` — the schema a tool *accepts* (vs the result it returns here).
- `errors-and-retry.md` — the envelope thrown when repair/retry is exhausted.
- → `agent-docs` for `SKILL.md`/`AGENTS.md`/`llms.txt` as agent-readable
  *documentation* (vs this playbook's schema-as-contract framing).
- `references/core/severity-rubric.md`, `references/core/score-rubric.md` —
  REVIEW scales; finding IDs `AGENT-DX-OUT-NNN`.
- `references/intents/{do,review,design}.csv` row `structured-output` — the entry points.
