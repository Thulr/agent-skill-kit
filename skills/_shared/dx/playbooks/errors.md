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
  a `request_id`, and a `doc_url`, supporting programmatic recovery, human
  triage, and post-hoc support. Translates unchanged to SDK exception envelopes.

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
- **"Did you mean" pointer** *(design, audit)* — when an unrecognized command,
  flag, field, or symbol is within Levenshtein distance two of a known one, the
  error points at the closest valid alternative (`Did you mean <closest>?`).
  Absent suggestion forces a documentation hunt.
- **Secret hygiene** *(audit)* — secrets are masked in all error paths: logs,
  structured error objects, `--verbose` output, and exception messages. Audit
  every log sink when adding debug context.
- **Stable error-code catalog** *(audit, design)* — every error class has a
  stable, documented code (e.g. `auth.token_expired`, `db.constraint_violation`);
  codes do not change between versions and a public catalog page lists them
  with cause and fix.
- **Retryable discriminator** *(design, audit)* — the error contract marks each
  code/class as retryable or not (a `retryable` boolean or a transient-vs-terminal
  field), so a caller decides whether to back off and retry or fail fast without
  parsing prose. Retry mechanics live in `sdk.md`.
- **TTY-aware rendering** *(audit, design)* — error output adapts to TTY vs
  pipe: colored and indented in a terminal, plain and parseable when piped
  to a log file or CI runner. The same root cause produces the same message
  text in both forms.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does every error name cause + fix? | "Invalid request" dead end | Add cause and remediation to message |
| Is user input preserved on failure? | Silent data loss | Persist state on error path |
| Are correlation IDs included? | Support is blind | Attach `request_id` to every server error |
| Are messages deterministic? | Same cause, different wording | Canonicalize message copy |
| Are secrets masked in all error paths? | Leakage in verbose/logs | Audit all log sinks and error serializers |

## Cross-references

- → `api.md` for HTTP error envelope shape.
- → `cli.md` for CLI error output formatting.
- → `sdk.md` for typed-exception design.
- → `logging.md` for continuous log streams distinct from one-shot errors.
- → `config.md` for config-validation error message copy.
