# Errors Playbook

## Scope

Error response shapes, validation messages, stack-trace UX, exception types,
recovery copy, and error-message UX. Routes to `api.md` for the HTTP error
envelope shape, `cli.md` for CLI error output formatting, and `sdk.md` for
typed-exception design.

## Grounding

- **Don Norman — *The Design of Everyday Things*** — slips vs. mistakes: slips
  are competent users executing correctly in the wrong context; mistakes come
  from a wrong mental model. Error copy must serve both: slips need a quick
  course-correction, mistakes need a model repair. Blame-free, actionable
  language reduces friction in both cases.
- **John Ousterhout — *A Philosophy of Software Design*** — define errors out
  of existence: validate at the boundary so internal code never sees malformed
  input. Error masking (silently substituting a default) hides bugs; surfacing
  errors early lets callers recover. Bundling unrelated exceptions into a
  generic throw makes callers guess — error classes should map one-to-one with
  recovery strategies.
- **Rust compiler error-message guidelines (rustc)** — concrete name, file
  location, and suggested fix in every diagnostic; "did you mean ...?" pointer
  when a near-match exists. The rustc guidelines are the operational proof that
  compiler-quality error messages are achievable in production systems.
- **Stripe API error contract** — error responses carry a stable
  machine-readable `code`, a description naming the offending parameter,
  a `request_id`, and a `doc_url`. Supports programmatic recovery, human
  triage, and post-hoc support. Translates unchanged to SDK exception
  envelopes consumed by agents.
- **Agent-callable surfaces (WorkOS practitioner framing)** — when an
  LLM consumes an error, it cannot read tooltips or recover from
  ambiguity the way humans do. It decides on surfaced text alone, at
  machine speed. Agent-consumable errors must be deterministic,
  structured, and name the failing input in a format the model parses.

## Good signals

- Every error names what failed, the likely cause, and the next action — no
  single-word responses like "Unauthorized."
- User input is preserved on failure; the form or buffer retains the user's
  work when an operation errors out.
- Correlation IDs (request_id, trace_id) are included in every server error
  and surfaced to the client for support handoff.
- Messages describe system state, not user fault: "Configuration key 'port' is
  missing" not "You passed bad config."
- Machine-readable error codes accompany every human-readable message so
  clients can handle classes programmatically without string matching.
- "Did you mean ...?" pointers appear when a near-match exists — typo'd flag,
  unrecognized command, unknown field.
- Errors are typed in code: distinguishable exception classes or `Result`
  variants, not stringly-typed sentinel strings.
- Secrets never appear in error output, logs, or stack traces regardless of
  verbosity level.
- For agent-callable surfaces, errors are a typed envelope with discrete
  fields (`code`, parameter-specific `message`, `recovery_hint`), not
  narrative text. The schema is stable across SDK versions.
- Tool-execution failures returned to the LLM name *which input* was
  problematic and *why*, in the same tool-result shape the model
  produced — so the agent can reissue with a corrected argument.
- The error persisted on the tool-call telemetry span is the exact shape
  the LLM saw, so replay or offline eval can simulate the recovery path
  without re-running against production.

## Common failures

- "Invalid request" with no detail — the caller has no path forward.
- A raw stack trace used as the user-facing message — internal implementation
  leaks, signal is buried.
- Swallowed exceptions — a bare `except: pass` or empty `catch {}` discards
  the failure silently; callers see phantom success.
- Messages that suggest a wrong fix — misleading remediation is worse than no
  remediation; the user takes action and the problem persists.
- Non-deterministic wording — the same root cause produces different message
  text across runs or code paths; log search and alerting break.
- Secrets leaked in `--verbose` output, error context objects, or structured
  logs when debug flags are on.
- Overlapping error classes — a single exception type maps to multiple distinct
  failure modes, forcing callers to parse the message to branch.
- Validation fires deep in the call stack rather than at the boundary, surfacing
  partial side-effects alongside the error.
- Errors returned to agents are free text; the LLM cannot branch on
  failure mode and retries blindly or hallucinates a recovery.
- Tool errors omit the offending parameter; the model retries with the
  same bad argument.
- The error stored on a tool-call span is reshaped before persistence;
  replay sees a different error than runtime.
- Error wording changes across SDK versions with no stable code; agents
  that branched on last release's text quietly mis-route.

## Heuristics

- **Cause-fix-context shape** *(audit, design, debug)* — every error message
  provides: what failed (cause), what to do (fix), and enough context to
  reproduce it (diagnostic). Absent any one of the three, the message is
  incomplete.
- **Preserve user input** *(design)* — failed operations do not drop the
  user's work. Persist form state, buffer content, or draft payloads on the
  error path.
- **Correlation IDs** *(audit, design)* — every server-side error attaches a
  `request_id` or `trace_id` that is surfaced to the caller and logged on the
  server side. Support can retrieve the context without a repro.
- **No-blame wording** *(audit)* — error copy describes the system state, not
  what the user did wrong. Most errors are slips (correct execution in the wrong
  context), not malice.
- **Deterministic messages** *(audit, debug)* — the same root cause produces
  the same wording every time. Canonical copy enables alerting, log search,
  and runbook matching.
- **Define-out-of-existence** *(design)* — validate at the boundary so
  internal code can assume well-formed inputs. Push error detection as early
  as possible; never let invalid data travel deep into the call stack.
- **Class-of-error prevention** *(design)* — when the same error recurs, fix
  the class (add a lint rule, tighten a typed contract, add a schema check),
  not just the instance.
- **"Did you mean" pointer** *(design, audit)* — when a near-match exists
  (typo'd flag, missing import, unrecognized field), point at the closest
  valid alternative. Absence of a suggestion forces the user to scan the docs.
- **Secret hygiene** *(audit)* — secrets are masked in all error paths: logs,
  structured error objects, `--verbose` output, and exception messages. Audit
  every log sink when adding debug context.
- **Stable error-code catalog** *(audit, design)* — every error class has a
  stable, documented code (e.g. `auth.token_expired`, `db.constraint_violation`);
  codes do not change between versions and a public catalog page lists them
  with cause and fix.
- **TTY-aware rendering** *(audit, design)* — error output adapts to TTY vs
  pipe: colored and indented in a terminal, plain and parseable when piped
  to a log file or CI runner. The same root cause produces the same message
  text in both forms.
- **"Did you mean" specifically for typos** *(design, audit)* — when an
  unrecognized command, flag, field, or symbol is within Levenshtein
  distance two of a known one, the error includes a "Did you mean
  `<closest>`?" pointer. Absent suggestion forces a documentation hunt.
- **Agent-readable error envelope** *(design, audit)* — for LLM-callable
  surfaces, errors are a typed structure with `code`, parameter-specific
  `message`, and `recovery_hint`. The schema is part of the public
  contract and does not break between minor versions.
- **Tool-error feedback shaped for retry** *(design, audit, debug)* —
  failed tool calls return the same JSON shape the LLM produced, naming
  the offending input; the error path does not collapse to free text.
- **Replay-ready error capture** *(design, audit)* — the error stored
  on the tool-call span is identical to what the LLM saw, so offline
  replay and eval simulate the recovery path without hitting production.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does every error name cause + fix? | "Invalid request" dead end | Add cause and remediation to message |
| Is user input preserved on failure? | Silent data loss | Persist state on error path |
| Are correlation IDs included? | Support is blind | Attach `request_id` to every server error |
| Are messages deterministic? | Same cause, different wording | Canonicalize message copy |
| Are secrets masked in all error paths? | Leakage in verbose/logs | Audit all log sinks and error serializers |
| Agent-callable errors return a typed envelope? | LLM cannot branch on failure mode | Add a stable structured-error schema to the public contract |
| Tool errors name the offending input in the LLM's own shape? | Agent retries with the same bad argument | Echo the parameter; keep the tool-result schema on the failure path |
| Span-attribute error matches what the LLM saw at runtime? | Replay sees a different error than runtime | Persist the runtime error shape verbatim |

## Cross-references

- → `api.md` for HTTP error envelope shape.
- → `cli.md` for CLI error output formatting.
- → `sdk.md` for typed-exception design.
- → `logging.md` for continuous log streams distinct from one-shot errors.
- → `config.md` for config-validation error message copy.
