# Config Playbook

## Scope

Runtime configuration UX: config-file design, env-var precedence, schema
validation, hot-reload, defaults, and the dump-effective-config command.
Distinct from `setup.md` (which covers first-run installation) and `auth.md`
(which covers credential handling specifically): this playbook covers the
*ongoing* runtime knobs a developer sets to change behavior. Routes to
`setup.md` for first-run config, `auth.md` for credential-specific config,
`errors.md` for config validation message copy, and `cli.md` for command-line
flags that override config.

## Grounding

- **Adam Wiggins — *The Twelve-Factor App*** — strict separation of config
  from code; config lives in the environment, not in committed files. Same
  artifact, different environments, different config.
- **Heroku Config Precedence Patterns** — operational precedence rules:
  defaults < config file < environment variables < command-line flags.
  Higher-precedence sources override lower; the rule is documented and
  consistent.
- **John Ousterhout — *A Philosophy of Software Design*** — define errors
  out of existence at the boundary: validate config at load time so internal
  code never sees malformed values. The cost of late validation is
  partial-success bugs.

## Good signals

- Config precedence is documented: defaults < file < env var < CLI flag (or
  the project's documented variant), and the rule is consistent everywhere.
- A schema (JSON Schema, Pydantic model, struct with tags, etc.) defines
  every config key, its type, default, and whether it is required.
- Invalid config fails at load time with a message that names the key, the
  expected shape, and the offending value — not deep in the call stack.
- A `config show` or `--print-config` command dumps the effective config
  after all sources are merged, so users can debug "what is actually in
  effect right now."
- A `.env.example` or annotated default config file is checked in and
  matches the schema; every required key has a sample value or documented
  default.
- Config-file paths follow platform conventions (XDG base dirs on Linux,
  `~/Library/Application Support` on macOS, `%APPDATA%` on Windows) rather
  than hard-coded locations.
- Secrets are never inlined in committed config files; the path is via env
  vars, a secret manager, or a separate uncommitted file.
- Hot-reload behavior is documented when supported, and explicitly stated
  as "requires restart" when not.

## Common failures

- Multiple config sources merge with undocumented or inconsistent
  precedence; what wins depends on file order or load timing.
- Invalid config fails at runtime with a stack trace deep in the program,
  with no indication of which key was bad or what the expected shape was.
- The example config file drifts from the schema; following the example
  produces a config that the loader rejects.
- Required keys are not declared anywhere; users discover them by hitting
  runtime errors and grepping the source for env-var names.
- Secrets are committed in a "sample" config file labeled "replace this
  before production" and inevitably ship to production untouched.
- Config keys are renamed without backwards compatibility; users who
  upgrade silently lose settings and only notice when something breaks.
- Config-file location is hard-coded to one path; users on other platforms
  or with multi-user setups cannot override it.
- There is no way to see the effective config; users edit the file and
  guess whether the env var is overriding their change.
- A boolean config key accepts "true", "True", "1", "yes", and "on" in
  different parts of the codebase, producing surprising mixed behavior.

## Heuristics

- **Documented precedence** *(design, audit)* — the precedence rule
  (defaults → file → env → flag, or the project's variant) is documented
  once and applied consistently. Inconsistent precedence is a footgun.
- **Schema-validated config** *(design, audit, debug)* — config is loaded
  through a schema (JSON Schema, language-native model). Unknown keys are
  flagged; type mismatches fail fast with a clear message.
- **Fail-at-load with key-and-value context** *(design, audit, debug)* —
  config errors fire at the boundary with a message naming the key, the
  expected shape, and the offending value. Deep-call-stack failures are a
  validation gap.
- **`config show` command** *(design, audit)* — a subcommand dumps the
  effective merged config, optionally with the source of each value (file,
  env, flag). Users debug "what is actually in effect" without guessing.
- **Annotated example config** *(design, audit)* — a checked-in example or
  `.env.example` is kept in sync with the schema; every key carries a
  sample value or documented default; comments name expected types.
- **Platform-correct paths** *(design, audit)* — config-file locations
  follow XDG base dirs, macOS conventions, and Windows conventions; the
  fallback chain is documented.
- **No secrets in committed files** *(audit)* — committed config carries
  no real credentials; secrets route via env vars, a secret manager, or an
  uncommitted local file. A pre-commit secret scan catches regressions.
- **Backwards-compatible key renames** *(design, audit)* — when a config
  key changes name, the old name is accepted with a deprecation warning for
  one release cycle before removal; the warning names the new key.
- **Canonical boolean parsing** *(audit, design)* — boolean values are
  parsed through a single helper accepting a documented set of synonyms;
  the same input produces the same result everywhere in the codebase.
- **Documented reload behavior** *(design, audit)* — for every config key,
  it is clear whether changes take effect on reload, on next request, or
  only after restart. "It depends" is a documentation failure.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is precedence documented and consistent? | Surprising overrides | Document the precedence rule; audit the loader |
| Is config schema-validated at load? | Runtime stack traces from bad config | Add schema validation at the boundary |
| Does the loader name the bad key and value on error? | Cryptic config failures | Improve error messages with key, expected, got |
| Is there a `config show` command? | Users guess at effective state | Add a dump-effective-config subcommand |
| Is the example config kept in sync with the schema? | Examples fail validation | CI-validate the example against the schema |
| Do config paths follow platform conventions? | Multi-user/multi-platform breaks | Adopt XDG and OS-specific defaults |
| Are secrets kept out of committed config? | Credential leak | Add a secret scan and uncommitted secrets path |
| Is reload behavior documented per key? | Surprises after edit | Annotate reload semantics on each key |

## Cross-references

- → `setup.md` for first-run config bootstrap.
- → `auth.md` for credential-specific configuration.
- → `errors.md` for config validation message copy.
- → `cli.md` for command-line flags that override config.
- → `logging.md` for log-level config and `LOG_LEVEL`-style env vars.
