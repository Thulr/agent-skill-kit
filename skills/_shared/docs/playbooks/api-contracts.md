# API and Tool Contracts Playbook

## Scope

Covers documentation embedded in machine-readable contracts and operational
interfaces: OpenAPI, MCP, GraphQL schemas, tool descriptions, examples, error
envelopes, idempotency, retries, rate limits, scopes, side effects, cost, and
latency metadata. Use when docs must drive calls, not just explain them.

- In: schema descriptions, parameter docs, request/response examples, tool
  description quality, stable error codes, doc links, idempotency keys,
  `Retry-After`, quota semantics, required scopes, side effects, reversibility,
  and operational metadata.
- Out: general API ergonomics outside documentation (use a DX skill), full
  production observability design (use a performance/observability skill), and
  agent context files (use the `agent-experience` skill).
- Intents this surface answers: audit, design, debug, measure.

## Grounding

- OpenAPI Specification 3.1.0 (OpenAPI Initiative, 2021) — grounds schema
  descriptions and multiple examples as documentation.
- MCP Tool Descriptions Are Smelly! (Hasan and coauthors, 2026) — provides the
  purpose/parameter/return/example/error/constraint rubric and the warning that
  untargeted verbosity can regress agents.
- Stripe API Errors reference (Stripe) — grounds stable error envelope, offending
  parameter, and doc link patterns.
- Improving API Usability (Myers and Stylos, 2016) — grounds example quality as
  a predictor of task success.
- How to Design a Good API and Why It Matters (Bloch, 2006) — grounds
  self-documenting interfaces and hard-to-misuse contracts.
- Research Report — Effective Documentation Patterns and Practices for DX, AX,
  and UX (Informed Skills research synthesis, 2026) — maps these contracts into
  AX and DX docs practice.

## Good signals

- Schema descriptions say what a field/tool/operation is for, not only its type.
- Examples cover minimal, typical, and failure cases and are valid against the
  current schema.
- Errors include stable machine-readable codes, human messages, affected fields,
  and canonical doc links.
- Retry, idempotency, rate-limit, quota, scope, side-effect, and reversibility
  semantics are explicit.
- Agents can choose the right operation/tool from names and descriptions without
  trying calls blindly.

## Common failures

- Type-only schemas — every description says "The user ID" or is blank, leaving
  agents to infer purpose from field names.
- Marketing descriptions — tool docs sell the feature but omit required inputs,
  return shape, constraints, and errors.
- Unstable error strings — callers branch on prose because no stable code or
  name exists.
- Unsafe retry ambiguity — docs say "try again" without idempotency guarantees,
  duplicate side-effect warnings, or server-directed timing.
- Example monoculture — only the happy path is shown, so agents hallucinate error
  handling, pagination, auth, or partial success.

## Heuristics

- (audit, design) Six-part description — operation/tool docs need purpose,
  parameters, return shape, examples, errors, and constraints. Add only details
  that change selection or call construction.
- (audit, design) Description at decision point — put crucial semantics in the
  schema/tool field the agent reads, not only in a prose article nearby.
- (audit, debug) Error envelope contract — every actionable error should expose
  stable code/name, message, affected parameter/object, retryability, and doc
  link.
- (design, debug) Retry safety — document idempotency keys, retry windows,
  `Retry-After`, transient vs permanent failures, and duplicate side effects.
- (audit, design) Operational metadata — surface scopes, cost/quota units,
  expected latency, side effects, reversibility, and dry-run/preview options.
- (audit, design) Examples as contract — include named valid examples and common
  invalid/failure examples; validate them in CI where possible.
- (measure) Tool-call eval — measure correct tool/operation selection, valid
  arguments, safe retry behavior, and recovery from canonical errors.
- (debug) Branch-on-code check — if any docs or examples branch on message text,
  add or expose a stable machine-readable field.

## Quick diagnostic

- Could an agent pick this tool from the description alone? yes → test argument
  quality; no → rewrite purpose/use conditions.
- Can the caller safely retry a failed write? yes → document the exact contract;
  no → document confirmation, preview, or human handoff.
- Does every error class have a stable code and recovery link? yes → inspect
  coverage; no → prioritize high-frequency errors.
- Are examples validated? yes → inspect scenario coverage; no → add validation or
  mark them illustrative.

## Cross-references

- the `agent-experience` skill (ax-docs surface) — retrieval and agent context surfaces around
  the contract.
- `references/playbooks/dx-docs.md` — human API reference, quickstarts, and
  examples.
- `references/playbooks/audience-conflicts.md` — when polished human docs conflict
  with generated or schema-derived docs.
- `references/core/severity-rubric.md` — duplicate side effects and unsafe retries
  often escalate severity.
