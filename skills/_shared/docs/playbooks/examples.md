# Examples Playbook

## Scope

Runnable sample apps, snippet packs, demo repos, and quickstart projects — the
artifacts that let a developer go from "I want to try this" to "it's running
locally" in minutes. Distinct from `docs.md` (where reference and tutorial
content lives) and `readme.md` (the front door): examples are the *paste-and-run
proof* that the product works, not the narrative explaining it. Routes to
`docs.md` for tutorial framing, `readme.md` for the link the user followed to
get here, `sdk.md` for the language-specific shape examples must match, and
`migration.md` for examples that must be updated alongside breaking changes.

## Grounding

- **Andrew Hunt & David Thomas — *The Pragmatic Programmer*** — tracer
  bullets: a small end-to-end runnable example beats a thick reference manual
  when the goal is to learn shape and feasibility. Working code is the
  fastest path to a correct mental model.
- **Steve Krug — *Don't Make Me Think*** — recognition over recall: a
  runnable example lets the developer recognize the pattern and adapt it,
  rather than recall the API from documentation.
- **Stripe Samples / Vercel Templates** — operational patterns for a samples
  surface: one repo per language or framework, CI'd against the current SDK
  version, runnable in under five minutes, and curated rather than
  community-dumped.

## Good signals

- A samples directory or sibling repo holds runnable examples per language
  or framework the product supports.
- Each example runs end-to-end in under five minutes from clone to first
  visible result.
- Every example carries its own README with prerequisites, a single command
  to run, and the expected output.
- Examples are versioned alongside the main product; the CI for the main
  product exercises the examples or the examples exercise themselves against
  the latest published version.
- At least one canonical example doubles as a test fixture — its request
  shape or output is asserted against the real system, so a contract change
  breaks the build instead of silently outdating the example.
- Examples cover both the simplest "hello world" and at least one realistic
  end-to-end flow per supported language.
- Sample code mirrors the idioms a real integrator would write — not
  showcase code that nobody would ship.
- Examples include a clean uninstall or reset path; users can throw a
  sample away without leaving residue.
- Snippet packs in docs and IDE integrations are sourced from the same
  curated examples, so the same code appears in the README, the docs, and
  the IDE hover content.

## Common failures

- Examples are inline in a Markdown doc; users cannot run them without
  copy-pasting into a new file and guessing at the framing.
- The "hello world" example references a deleted endpoint, an obsolete flag,
  or an old SDK version because nothing tests it.
- Samples repo exists but only covers one language; other supported
  languages have no runnable example at all.
- Each sample takes 30 minutes of yak-shaving (build a custom config, set
  up six env vars, install three peer libraries) before the first run.
- Sample code uses patterns no real integrator would write — global state
  mutated across files, secrets hard-coded inline, no error handling — and
  becomes a bad model for downstream code.
- Examples are community contributions that have not been audited; some
  work, some do not, and the README does not say which.
- The samples directory is at HEAD against the unreleased main branch but
  the README points users at the stable release; what they install does
  not match what they read.
- Sample apps include credentials, real API keys, or production endpoints
  that should never have been committed.
- No expected-output snippet anywhere; users cannot tell whether the example
  worked without already knowing what success looks like.

## Heuristics

- **One-language-per-sample, runnable** *(audit, design)* — each supported
  language has at least one sample that runs end-to-end with a single
  command, after at most one substitution (an API key, a workspace ID).
- **Five-minute clone-to-result** *(audit, design)* — measured from `git
  clone` to the first visible success on a clean machine, including install
  time. Anything longer is a friction signal worth investigating.
- **Per-sample README** *(audit, design)* — every example carries a README
  naming prerequisites, the run command, and the expected output. A samples
  directory with no per-sample READMEs is a documentation gap.
- **CI-tested against current SDK** *(audit, design)* — examples are
  exercised in CI against the current published SDK version; stale examples
  fail the build before they reach users.
- **Idiomatic for the language** *(design)* — sample code mirrors what a
  real integrator would write in that language: native error handling,
  conventional file layout, no cross-language tells.
- **Expected-output block** *(audit, design)* — every sample includes a
  block showing what the user should see when it works. Without it, users
  cannot verify success.
- **Curated, not dumped** *(audit)* — samples are owned by the project and
  reviewed before being added; community contributions are accepted only
  after the same audit as first-party samples.
- **Realistic-flow sample alongside hello-world** *(design)* — at least one
  sample covers a realistic end-to-end flow (auth, list, mutate, handle
  errors), not just a single method call.
- **Snippet-source parity** *(audit)* — the README example, the docs
  snippets, and the IDE hover examples come from the same curated source;
  any one of them changing flags a review of the others.
- **Example-as-fixture** *(audit, design)* — at least one canonical example
  is reused as a validation fixture: a request-schema assertion, or a
  contract/smoke test that runs the example against a live or recorded call.
  Divergence between the documented example and real behavior then fails the
  build rather than surfacing as a user bug report. Extends *Snippet-source
  parity* and *CI-tested against current SDK*: parity keeps the copies in
  sync; this keeps the canonical copy honest against the running system.
- **Secret-clean** *(audit)* — samples contain no real credentials, no
  production endpoints, and no values that would be a security issue if
  cloned and run as-is.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is there at least one runnable example per supported language? | Users blocked at "how do I start" | Add a sample per language, owned by the project |
| Does each sample run end-to-end in under five minutes? | First-try friction | Profile clone-to-result; cut setup steps |
| Is each example tested in CI? | Stale samples accumulate | Add example CI against the current published SDK |
| Is a canonical example reused as a validation fixture? | Documented example can drift from real behavior unnoticed | Assert one example's request schema or output in CI |
| Does each sample carry its own README and expected output? | Users cannot verify success | Add per-sample READMEs with output blocks |
| Do samples reflect real integrator patterns? | Bad model copied downstream | Rewrite samples to match production-quality code |
| Are samples curated rather than community-dumped? | Mixed quality, unclear ownership | Define an audit gate for sample contributions |
| Are samples free of real credentials and production endpoints? | Security incident waiting | Audit and rotate; add a pre-commit secret scan |

## Cross-references

- → `dev-docs.md` for the tutorial and reference content the samples
  support.
- → `readme.md` for the README link that points evaluators at the samples.
- → the `dx-audit` / `dx-design` skills for the SDK shape examples must
  match (`sdk`), breaking changes that require sample updates
  (`migration`), and snippet packs sourced from the same examples (`ide`).
