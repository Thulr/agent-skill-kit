# Gate Hardening

Use this playbook when a promoted reflection-log pattern closes through a
hook, static validator, CI check, branch-protection rule, sandbox policy, or
other enforcement point. The common failure is a plausible gate that catches
the observed case but misses equivalent syntax, wrapper forms, portability, or
the required CI path.

## Promotion Standard

Before writing a gate, name:

- **Policy invariant:** what must never regress.
- **Execution surface:** shell hook, static check, CI workflow,
  branch-protection rule, schema validator, or sandbox policy.
- **Required fixture:** the test or static case that proves the gate catches
  the observed failure and equivalent forms.
- **CI binding:** the required job, script, or branch rule that runs it for
  PRs, not only local `just check`.

If any item is missing, promote a smaller documentation rule first and record
the enforcement gap as `needs_evidence` or `planned`.

## Variant Matrix

For command, path, schema, or symlink gates, cover every applicable class:

1. **Direct form:** the exact observed failure.
2. **Equivalent syntax:** short/long flags, split flags, `=` forms, option
   terminators, aliases, and refspec-style alternatives.
3. **Wrapper form:** `sudo`, `env`, `time`, shell launchers, global tool
   options, and value-taking wrapper flags.
4. **Nested execution:** shell `-c`, command substitution, process
   substitution, multiline payloads, or a dangerous command after a pipeline
   separator.
5. **Canonicalization:** relative paths, `..` traversal, symlink resolution,
   basename matching, case sensitivity when relevant, and absolute-vs-relative
   portability.
6. **Source-of-truth drift:** lists/counts derived from CSVs, schemas,
   templates, or shared references must be parsed from the source, not
   hardcoded.
7. **CI parity:** the gate must run in the required PR path. Local-only gates
   are diagnostics, not enforcement.
8. **Negative controls:** include safe variants so the gate does not block
   legitimate work and cause agents to route around it.

## Hook-Specific Requirements

Shell-deny hooks should parse argv structurally rather than regexing the raw
string. Tokenize, split command separators, preserve newlines as separators,
unwrap transparent wrappers while consuming their value flags, recursively
inspect shell command payloads, and normalize paths before protected-target
checks. For every new executable or wrapper the dispatcher treats specially,
add positive and negative fixture rows in the same commit.

## Static-Check Requirements

Static validators must assert presence first, then parse shape. A conditional
validator like "if file exists, validate it" silently passes when the required
file is deleted. Regexes should match the canonical syntax they claim to
enforce; when a registry or schema is available, parse it instead of grepping
nearby prose.

## Shared-Content Requirements

Shared references must be portable and exact: relative symlink, target under
`skills/_shared/`, basename-to-basename match, and coverage across all install
lanes (`skills/*`, `skills/.experimental/*`, `.agents/skills/*`). Absolute
symlinks and "somewhere under `_shared`" checks are not sufficient.

## Closeout

A promoted gate is `verified` only when:

- the fixture fails on the pre-fix state or documented reproduction,
- the fixture passes after the change,
- the gate runs in CI or the protected enforcement path,
- and the reflection-log entry's `## Closed by` names the commit or PR.
