# Errors and Retry Playbook

## Scope

Errors as a surface an LLM consumes and recovers from: the agent-readable error
envelope, tool-error feedback shaped so the model can retry, replay-ready error
capture, and the retryable/terminal discriminator. This is the agent-actor
analog of human error-message UX.

- **In:** typed error envelope for LLM consumers, retry-shaped tool feedback,
  error capture on the tool-call span, retryable-vs-terminal signalling.
- **Out:** semantic-vs-transport retry *mechanics* in generation (see
  `structured-output.md` and `sdk-design.md`); human-facing error copy, stack
  traces, and `--verbose` UX (see `dx-audit` / `dx-design`).
- **Intents this surface answers:** do, review, design.

## Grounding

- **An LLM consuming an error cannot read tooltips or recover from ambiguity the
  way a human can.** It decides on the surfaced text alone, at machine speed.
  Agent-consumable errors must be deterministic, structured, and name the
  failing input in a format the model parses — narrative prose is for humans.
- **A tool error is the model's feedback loop, not a log line.** A failed tool
  call is the model's next input; its shape determines whether the model can
  correct course or spins. Collapsing it to free text breaks the loop.
- **What the model saw is what eval must replay.** If the error stored for
  observability differs from what the model received, offline replay and evals
  reconstruct a recovery path that never happened.

## Good signals

- For LLM-callable surfaces, errors are a typed structure with a stable `code`,
  a parameter-specific `message`, and a `recovery_hint`; the envelope is a
  discrete-field schema, not narrative text.
- The error schema is part of the public contract and does not break between
  minor versions — the `code` is stable across SDK releases.
- A failed tool call returns the same JSON shape the model produced, naming the
  offending input; the error path does not collapse to free text the model must
  parse heuristically.
- The error stored on the tool-call span is byte-identical to what the model
  saw, so replay and eval simulate the recovery path without hitting
  production.
- Each error `code`/class is marked retryable or terminal (a `retryable`
  boolean or transient-vs-terminal field), so the loop decides to back off or
  fail fast without parsing prose.
- A semantic retry (validation/tool failure) appends the failing detail to the
  next request; a transport retry follows the client-floor backoff — the two
  are distinct and the model is told which happened.

## Common failures

- Errors are free text an agent cannot branch on; the model re-reads a prose
  sentence every turn and guesses at the cause.
- A tool error omits the offending parameter, so the model retries with the same
  bad input and loops.
- Error wording changes across versions with no stable `code`, so anything that
  matched on the message silently breaks.
- The error path collapses a structured tool failure into a string, discarding
  the shape the model needs to correct.
- The error captured for observability is a reformatted summary, not what the
  model saw, so replayed evals diverge from production behavior.
- A retryable transient failure is presented identically to a terminal one, so
  the loop either gives up on recoverable work or hammers an unrecoverable
  call.

## Heuristics

- **(design, review) Ship a typed, stable error envelope.** For LLM-callable
  surfaces, errors carry a stable `code`, a parameter-specific `message`, and a
  `recovery_hint` as discrete fields; the schema is public contract and the
  `code` does not change between minor versions.
- **(design, review) Shape tool errors for retry.** A failed tool call returns
  the same JSON shape the model produced and names the offending input, so the
  model's next attempt is informed — the error path never collapses to free
  text.
- **(do, review) Capture the error the model saw, verbatim.** Persist on the
  tool-call span exactly what was surfaced to the model, so offline replay and
  eval reproduce the real recovery path rather than a reformatted summary.
- **(design, review) Discriminate retryable from terminal.** Mark each
  code/class retryable or terminal with a typed field so the loop backs off or
  fails fast without parsing prose; an undifferentiated error path makes the
  loop guess.
- **(design) Tell the model which retry happened.** Distinguish a semantic retry
  (append the validation/tool failure detail) from a transport retry (silent
  backoff); the model corrects on the former and waits on the latter.
- **(review) Branch-test the error contract, not just the happy path.** A
  surface is agent-ready only if a consuming model can branch on every error
  `code` deterministically; review the error space the way you review the
  success space.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are LLM-facing errors a typed envelope with a stable `code`? | Agent re-parses prose each turn | Add `code` / `message` / `recovery_hint` discrete fields |
| Does a tool error name the offending input in the tool-result shape? | Model retries the same bad input | Return the produced shape + the bad parameter |
| Is the captured error identical to what the model saw? | Replayed evals diverge from prod | Persist the verbatim error on the tool-call span |
| Is each error marked retryable or terminal? | Loop guesses whether to retry | Add a `retryable`/transient-vs-terminal field |
| Is the `code` stable across minor versions? | Message-matching breaks on upgrade | Freeze codes in the public contract |

## Cross-references

- `structured-output.md` — validation-failure semantic retry on generation.
- `sdk-design.md` — the loop that consumes a tool error as its next input.
- `tools-and-mcp.md` — the tool whose failure this envelope describes.
- `sdk-telemetry.md` — capturing the error on the span for replay.
- → `dx-audit` / `dx-design` (`errors`) for human-facing error copy, stack-trace
  UX, and the retryable discriminator as general developer DX.
- `references/core/severity-rubric.md`, `references/core/score-rubric.md` —
  REVIEW scales; finding IDs `AGENT-DX-ERR-NNN`.
- `references/intents/{do,review,design}.csv` row `errors-and-retry` — the entry points.
