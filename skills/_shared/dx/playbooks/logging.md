# Logging Playbook

## Scope

Consumer-facing logging and runtime observability: log levels, structured vs.
unstructured output, redaction, trace-id propagation, debug-flag UX, and the
`doctor` / `status` / `version` family of introspection commands. Distinct
from `errors.md` (one-shot user-facing failure messages) and `telemetry.md`
(opt-in data collection for the maintainer): logging is the *continuous
stream a developer reads when something is wrong*, not a single error and
not data shipped back to a vendor. Routes to `errors.md` for individual
failure messages, `telemetry.md` for collected data, `cli.md` for
`--verbose` flag conventions, and `auth.md` for secret hygiene in log output.

## Grounding

- **Adam Wiggins — *The Twelve-Factor App*** — logs are an event stream the
  application writes to stdout; the operator decides the sink, retention,
  and format. The tool's job is to emit structured, useful events, not to
  choose where they live.
- **Charity Majors, Liz Fong-Jones, George Miranda — *Observability
  Engineering*** — high-cardinality structured events with consistent fields
  beat free-form prose for debugging. Trace IDs and correlation IDs link a
  request across components; a log line without context is a clue without a
  case file.
- **Brendan Gregg — *Systems Performance*** — the USE method depends on
  introspection commands that expose the system's state cheaply; `doctor`,
  `status`, and `version` commands are the developer-facing equivalent of
  USE counters.

## Good signals

- Log levels are named, documented, and consistent across the codebase
  (e.g. `debug`, `info`, `warn`, `error` with stated thresholds).
- A single flag (`--verbose`, `-v` / `-vv` / `-vvv`, or a `LOG_LEVEL` env
  var) raises verbosity without recompilation or config-file edits.
- Logs default to structured (JSON or logfmt) when stdout is a pipe and
  human-readable when stdout is a TTY, or a flag controls the format.
- Every log line includes timestamp, level, and a stable component or
  module field; high-cardinality context (request ID, trace ID) is attached
  where it exists.
- A `doctor` or `status` subcommand reports installed version, runtime
  version, config file in use, declared env vars, and the result of a
  smoke check.
- The startup banner prints the resolved runtime state on boot — derived
  limits (worker, pool, cache sizes), bound ports, effective config loaded,
  detected CPU/GPU — and the docs cite those exact lines when explaining how
  to confirm a setting took effect.
- A `--version` flag and a `version` subcommand both work; the output
  includes the git commit hash or build identifier when relevant.
- Secrets are masked in all log output regardless of level — API keys,
  tokens, passwords, and environment variable values never appear verbatim
  even at the most verbose level.
- A documented "how to capture logs for support" path tells users which
  flag to enable, where logs land, and what to redact before sharing.

## Common failures

- Only `print` statements; no levels, no structure, no way to silence the
  noise or raise the signal when debugging.
- Verbose mode prints secrets — API keys, tokens, full request bodies —
  because the verbose path was never audited for redaction.
- Log lines are free-form prose that grep and structured tools cannot parse
  reliably; debugging requires reading paragraphs of text.
- The same logical event produces different message text across runs or
  code paths; log search and alerting break silently.
- There is no `doctor`, `status`, or `version` command, so debugging
  starts with the user trying to remember which version they have and
  which config file is in effect.
- `--version` prints "1.0" with no build hash, no build date, and no way to
  trace it back to a specific commit or release.
- TTY-only formatting (colors, indentation, spinners) leaks into piped
  output, breaking log aggregation and CI parsing.
- Log files are written to a hard-coded path (`/tmp/foo.log`, the current
  working directory) with no documentation and no rotation, surprising users
  when disks fill up.
- Trace IDs exist in the server-side logs but never make it to client-side
  output, so a user reporting an issue cannot supply the ID support needs.
- Boot is silent about resolved limits and bound ports, so a misconfiguration
  (wrong config picked up, half the workers the user expected) only surfaces
  later as a confusing runtime symptom instead of a visible line at startup.

## Heuristics

- **Documented log levels** *(audit, design)* — log levels are named,
  documented in `README` or `docs`, and consistent across the codebase; a
  developer can predict which level a given event belongs to.
- **Single verbosity dial** *(design, audit)* — one knob (flag, env var, or
  config key) raises verbosity. `-v` / `-vv` / `-vvv` or `LOG_LEVEL=debug`
  is enough; users should not have to edit a config file to debug. The
  corollary holds the other way too: the default level stays terse so the
  signal isn't buried, and the dial is the only thing that opens the firehose.
- **Startup banner emits load-bearing facts** *(audit, design)* — on boot the
  tool prints the config and capacity facts a reader needs to diagnose
  misconfiguration: derived limits (worker, pool, cache sizes), bound ports,
  the effective config actually loaded, and detected CPU/GPU. The docs point
  at those exact banner lines by name. Unlike `doctor` / `status`, this is
  unprompted — it lands in the log stream every run, so a captured log already
  carries the runtime's resolved state without a second command.
- **Structured when piped, human when TTY** *(design, audit)* — output
  detects whether stdout is a TTY and switches between human-readable and
  structured (JSON or logfmt) automatically, or an explicit flag controls it.
- **Stable, parseable fields** *(audit, design)* — every log line carries
  timestamp, level, component, and where present trace ID; field names are
  stable across versions so log aggregation does not break on upgrade.
- **`doctor` / `status` / `version` subcommands** *(design, audit, debug)* —
  introspection commands expose installed version, runtime, config in use,
  and a smoke-check result. A user reporting a bug can run one command and
  paste the output.
- **Build-traceable version** *(audit, design)* — `--version` and `version`
  output includes a build identifier (git SHA, build date, or release tag)
  that maintainers can resolve back to a specific commit.
- **Secret redaction at every level** *(audit, design)* — secrets are
  masked in all log paths, including the most verbose. An automated test
  asserts no known secret patterns appear in representative captures.
- **Deterministic event text** *(audit, debug)* — the same logical event
  produces the same canonical message text every time, so grep, alerts,
  and runbooks remain stable as the codebase evolves.
- **Trace-ID propagation** *(design, audit)* — server-side trace IDs are
  surfaced in client-side output (CLI banners, error responses) so a user
  reporting an issue can supply the ID that maps to server logs.
- **Documented capture path** *(audit, design)* — the docs include a "how
  to capture logs for support" page naming the flag, the file path, and a
  redaction reminder before sharing externally.
- **Conventions over invention** *(design, audit)* — structured log and
  span fields follow published semantic conventions
  (`http.request.method`, `http.response.status_code`, gen-ai `ai.*`)
  rather than bespoke names. Libraries that emit traces depend on the
  observability API, not a specific SDK, so downstream applications
  choose the exporter without per-vendor adapters.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are log levels named and consistent? | Free-form prose | Adopt named levels and document them |
| Is there a single verbosity flag or env var? | Config-file editing to debug | Add `--verbose` or `LOG_LEVEL` |
| Does output adapt to TTY vs pipe? | Color codes leak to logs | Detect TTY; switch format automatically |
| Are secrets masked at every level? | Credentials in verbose logs | Add redaction and an automated payload test |
| Is there a `doctor` or `status` command? | Users guess at install state | Add introspection subcommand |
| Does `--version` include a build identifier? | Cannot trace back to a commit | Embed git SHA or build tag in version output |
| Are trace IDs propagated to user-facing output? | Support cannot match logs | Surface trace ID in CLI and error responses |
| Does boot log resolved limits, ports, and effective config? | Misconfig surfaces only later | Emit a startup banner; cite its lines in the docs |

## Cross-references

- → `errors.md` for individual user-facing failure messages.
- → `telemetry.md` for opt-in collected data, distinct from log streams.
- → `cli.md` for `--verbose` flag conventions and exit-code coupling.
- → `auth.md` for secret hygiene in log output (mask in every path).
