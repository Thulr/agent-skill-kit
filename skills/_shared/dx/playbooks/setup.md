# Setup Playbook

## Scope

Bootstrap, env config, first-run friction, install commands, declared
dependencies, smoke-test path. Routes to `inner-loop.md` for the
edit-run-test cycle after setup, `docs.md` for setup-doc patterns, and
`contributor.md` for fresh-fork onboarding.

## Grounding

- **Adam Wiggins — *The Twelve-Factor App*** — config in environment,
  dependency declaration, and build/release/run separation; the operational
  baseline for cloud-native setup.
- **Daniele Procida — Diátaxis framework** — setup docs are how-to guides
  (sequential, goal-directed steps), not tutorials (exploratory); the two
  are different genres and must not be mixed.
- **Joel Spolsky — "The Joel Test"** — the 1-step build rule: a new developer
  should be able to bootstrap the project with a single command.

## Good signals

- One command bootstraps the entire environment (`make setup` or
  `./bin/setup` or equivalent).
- A `.env.example` (or equivalent) lists every required env var with a
  sample or documented default.
- Missing dependencies are detected before any work begins, and the error
  names the missing dep and the install command.
- A documented smoke test lets the user confirm setup worked ("run
  `cli check` — should print `ok`"), and it passes on a fresh clone with
  no secrets — checks needing paid credentials skip and say so.
- Setup works on a fresh machine without tribal knowledge or private Slack
  context.
- A clean uninstall path is documented alongside the install path.
- Running setup twice is a no-op or a safe upsert — not a double-install.
- Setup warns when the detected runtime version (Node, Python, Go, etc.)
  does not match the required major version.

## Common failures

- README maze with multiple competing setup paths and no indication of
  which applies to the reader.
- Required env vars not listed anywhere; developers are told to "ask in
  Slack."
- Install commands assume already-present tooling (`brew` on Linux, `apt`
  on macOS) and fail silently or with cryptic errors.
- No smoke test — the user must guess whether setup succeeded.
- Verified only on the maintainer's machine; fails on fresh environments.
- Setup mutates global state (system Python, global `~/.npmrc`) without
  warning the user.
- The quickstart's first verification fails on a fresh clone because a
  default test hard-requires a paid API key the new user does not have.
- Re-running setup breaks the existing install — no idempotency.
- No documented way to undo the setup after the fact.

## Heuristics

- **One-command bootstrap** *(design, audit)* — a single `make setup` or
  `./bin/setup` runs every installation step. No out-of-band prerequisites.
- **Declared env vars with example** *(design, audit)* — `.env.example`
  lists every required var with a sample value; checked into source control,
  never gitignored.
- **Fail-fast on missing deps** *(audit, debug)* — setup detects missing
  dependencies before doing any work; the next line tells the user exactly
  what to install.
- **Documented smoke test** *(design, audit)* — every setup ends with a
  verification step the user can run; success and failure output are both
  documented.
- **Fresh-machine verified** *(audit)* — setup is exercised periodically in
  a clean container or VM; a CI fresh-install job is the reliable form of this.
- **Idempotent setup** *(design)* — running setup twice produces the same
  result as running it once; operations use safe-upsert patterns.
- **Clean uninstall path** *(design, audit)* — there is a documented command
  or script that reverses everything setup did.
- **Version-skew detection** *(audit, debug)* — setup reads the detected
  runtime version and warns (or errors) if the major version does not match
  what the project requires.
- **Time-to-hello-world target** *(design, audit)* — a documented target
  exists for "clone to first visible success" (commonly five or ten minutes
  on a clean machine); the target is measured periodically, not aspirational.
- **Committed runtime pin** *(design, audit)* — a runtime-version manifest
  (`.nvmrc`, `.tool-versions`, `.python-version`, `rust-toolchain.toml`) is
  committed so version managers pick up the right version automatically; a
  contributor doing `nvm use` succeeds without reading docs.
- **Dev-container or Codespaces support** *(design)* — a `.devcontainer/`
  config or Codespaces template lets a first-time user click "open in
  container" and bypass local setup entirely; especially load-bearing when
  the dependency set is heavy.
- **Post-setup next-step pointer** *(design, audit)* — the last line of
  successful setup names the next command to run, not "you're all set."
  "Setup complete. Try: `<tool> hello`" beats a vague success message.
- **Scaffold / init command for new users** *(design)* — for tools that
  generate projects (CLIs, frameworks), a `<tool> init` or `npx create-X`
  command scaffolds a working starter so the user can paste-and-go without
  hand-rolling a project layout.
- **Adoptable in a thin slice** *(design, audit)* — a broad SDK or framework
  documents a minimal first use that touches only a fraction of the surface;
  the new user reaches a working result before learning the full API, and
  nothing in the quickstart forces config they don't yet need.
- **Pinned installer in the quickstart** *(design, audit)* — the bootstrap
  command names the exact version so the documented first run is reproducible
  (e.g. `uv tool install <pkg> --from git+<url>@<tag>`), not a floating
  `@latest`. Distinct from the committed runtime pin: this pins the *installer
  invocation* the reader copies, not the project's own runtime manifest.
- **Credential-optional first verification** *(audit, debug)* — the smoke
  test or default test command passes on a fresh clone with zero secrets;
  checks needing optional paid credentials skip rather than fail, and the
  output names exactly which checks were skipped and why.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is bootstrap a single command? | Multi-step manual setup | Add `./bin/setup` script |
| Are env vars in `.env.example`? | Hidden config, ask-in-Slack | Create and commit example file |
| Does setup fail-fast on missing deps? | Cryptic mid-run failures | Add preflight check before work |
| Is there a smoke-test command? | Users guess whether it worked | Add `check` or `doctor` subcommand |
| Does first verification pass with no secrets? | Fails without a paid key | Skip credential checks and name what was skipped |
| Is setup idempotent? | Re-run breaks the install | Make operations safe-upsert |
| Is fresh-machine tested? | Works for maintainer only | Add CI fresh-install job |

## Cross-references

- → `inner-loop.md` for the edit-run-test cycle after setup is complete.
- → `docs.md` for setup-doc patterns (it's a how-to, not a tutorial).
- → `contributor.md` for fresh-fork onboarding.
- → `readme.md` for the install command that appears on the README's first
  screen.
- → `package.md` for install footprint, peer dependencies, and registry
  metadata.
- → `config.md` for runtime configuration distinct from one-time install.
