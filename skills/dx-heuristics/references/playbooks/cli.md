# CLI Playbook

## Scope

Command-line tools: subcommand layout, flag design, help output, exit codes,
output formats, install path. Routes to `errors.md` for error message text and
`setup.md` for installation friction. Routes to `auth.md` if the CLI handles
credentials.

## Grounding

- **clig.dev — Command Line Interface Guidelines** — concrete CLI conventions
  for help, flags, output, exit codes; treats CLIs as a UX surface.
- **Heroku CLI Style Guide** — opinionated patterns for subcommand layout,
  output hierarchy, and progress feedback.
- **Don Norman — *The Design of Everyday Things*** — affordances and signifiers
  applied to non-visual interfaces; what in the help output signals "this is
  the next action."

## Good signals

- `--help` shows: usage line, one-sentence purpose, a runnable example, exit
  codes, and where to find more.
- Subcommand names are verbs that match the user's mental task ("init", "run",
  "check"), not implementation labels ("process", "execute").
- Output uses consistent prefixes (✓ ✗ ⚠), indentation, and a single primary
  next-step line when something completed.
- Long-running operations (>500ms) show progress, not silence.
- Exit codes are stable and documented (0 success, non-zero categorized).
- JSON output (`--json`) round-trips through `jq` without parsing tricks.
- Destructive commands prompt by default; `--yes` / `-y` opts out and is
  documented in `--help`.

## Common failures

- `--help` lists flags alphabetically with no example — discoverability dies.
- Subcommands named after internal modules — users guess wrong every time.
- Destructive commands share affordances with safe ones (no prompt, no
  distinct prefix).
- Errors print a stack trace; success prints nothing — asymmetric feedback.
- TTY-only output (color, spinners) breaks piped/CI usage.
- Smoke-test path is undocumented; new users ask the maintainer.
- Exit codes change between versions; scripts break silently.

## Heuristics

- **Help-as-quickstart** *(audit, design)* — `--help` itself shows a working
  example, not just a flag list. Good: pasteable command in help text. Bad:
  flag dump.
- **Verb-noun naming** *(design)* — subcommands are verbs matching user tasks
  ("create user"), not nouns ("user create"), unless the surface is
  resource-first by convention.
- **Smoke-test discoverable** *(audit, debug)* — a first-time user can find
  the "did this install correctly" command from `--help` alone.
- **Safe-by-default destructive ops** *(design)* — destructive commands prompt
  unless `--yes` / `-y` is passed. Document the flag in `--help`.
- **Pipe-safe output** *(audit)* — JSON output is the same shape whether
  stdout is a TTY or a pipe. Colors auto-disable for non-TTY.
- **Exit-code contract** *(audit)* — exit codes are stable across versions and
  documented; scripts can rely on them.
- **Affordant prefixes** *(audit, design)* — output uses consistent visual
  prefixes (✓ ✗ ⚠) so the developer sees state at a glance.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does `--help` show a runnable example? | First-time users stall | Add one paste-and-run example |
| Are subcommand names verbs matching user tasks? | Users guess wrong | Rename to user-task verbs |
| Is there a documented smoke-test path? | Tribal-knowledge support | Add `check` or `doctor` subcommand |
| Does output differ between TTY and pipe? | CI/scripts break silently | Detect TTY; auto-disable color |
| Are exit codes documented? | Scripts can't trust them | Document; add tests for stability |
| Do destructive commands prompt? | Accidental data loss | Prompt unless `--yes` |

## Cross-references

- → `errors.md` for error message text and recovery copy.
- → `setup.md` for install path and bootstrap commands.
- → `auth.md` if the CLI handles credentials.
