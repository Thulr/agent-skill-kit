# README Playbook

## Scope

The README and project-root surface — what a developer sees in the first 60
seconds after landing on the repo, package page, or doc site index. Distinct
from `docs.md` (the doc site and reference content) and `setup.md` (the actual
install procedure): the README is the *advertisement and signpost*, not the
manual. Routes to `setup.md` for install detail, `docs.md` for deeper
reference, `examples.md` for runnable samples, and `package.md` for
registry-page metadata that mirrors the README.

## Grounding

- **Karl Fogel — *Producing Open Source Software*** — the README is the
  project's front door; it must answer "what is this, who is it for, how do I
  start" before anything else. Without that, evaluators bounce.
- **Steve Krug — *Don't Make Me Think*** — first-screen scannability and the
  F-pattern: users scan, not read. The first ten lines carry most of the
  weight; the value proposition and install command must be visible without
  scrolling.
- **GitHub — Open Source Guides** — operational patterns for the README as a
  surface: name, one-line description, install + first-use snippet, badges,
  link out to deeper docs, maintenance signals.

## Good signals

- A one-sentence "what this is" line appears at the top, before badges and
  marketing copy.
- Badges (build, version, license, registry) are present but secondary to the
  value proposition; they do not dominate the first screen.
- The install command appears within the first screen, copy-pasteable exactly
  as written.
- A working code example or CLI invocation follows install, paste-runnable
  with at most one substitution.
- A "next steps" section links out to docs, examples, and `CONTRIBUTING.md`
  rather than burying everything in the README.
- A screenshot, GIF, or terminal output shows the user what success looks
  like — especially load-bearing for CLIs and visual tools.
- A "why this exists" or "when to use" section answers the implicit
  comparison the evaluator is making against alternatives.
- Maintenance status is visible: a badge, a last-release date, or a banner
  for archived projects.

## Common failures

- README is marketing copy with no install command, no example, no path to
  trying it.
- README is a reference dump with no introductory framing; the evaluator
  cannot tell what the project does without reading code.
- The install command depends on unstated prerequisites — `npm install` that
  silently requires Node 20+, `pip install` that requires a system library —
  and fails opaquely.
- The first code example uses placeholder values that cannot run
  (`API_KEY = "your-key-here"` with no path to acquire a real one) and is
  not tested anywhere.
- README has no working example at all; the reader must navigate to a docs
  site to see any code.
- Twelve badges sit above the value proposition; the first signal the user
  gets is a wall of shields, not a sentence describing the product.
- "Coming soon" or "TODO" markers where load-bearing content should be — the
  evaluator infers the project is incomplete.
- The README is the only doc; nothing links to deeper material and the
  reader hits a dead end at the bottom.
- README references commands, files, or endpoints that no longer exist
  because nothing keeps the README and code in sync.

## Heuristics

- **One-line "what this is" up top** *(audit, design)* — the first
  non-frontmatter line names the value in one sentence; an evaluator decides
  whether to keep reading within five seconds.
- **Install on the first screen** *(audit, design)* — the install command
  appears before the user has to scroll on a typical laptop. If they have to
  hunt for it, you have lost them.
- **Paste-runnable example** *(audit, design)* — the first example runs with
  at most one substitution. The example is tested in CI; stale examples block
  release.
- **Prereq disclosure before install** *(audit)* — if the install command
  depends on a specific runtime version, system library, or platform, that
  prerequisite is stated before the install line, not below it.
- **Next-step ladder** *(audit, design)* — the README ends with explicit
  links to deeper docs, runnable examples, and `CONTRIBUTING.md`. Dead-end
  READMEs strand developers who are ready to commit.
- **Maintenance signal** *(audit)* — a badge, banner, or sentence makes the
  project's maintenance status legible. Stale-looking READMEs repel
  evaluators who do not want to adopt a dead project.
- **Comparison context** *(design)* — a "vs X" or "when to use" section
  addresses the implicit decision the evaluator is making against
  alternatives. Without it, every evaluator has to do the comparison work
  themselves.
- **Working visual** *(design)* — a screenshot, GIF, or terminal-output block
  shows the result, not just the invocation. Load-bearing for CLIs, visual
  tools, and anything where the output is the point.
- **README-and-code drift gate** *(audit)* — the README's commands and code
  blocks are exercised by CI; broken or removed references fail the build.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does line 1 say what this is? | Lost in five seconds | Add one-line value prop above badges |
| Is the install command on the first screen? | Hidden below marketing | Move install above the fold |
| Does the first example paste-and-run? | Trust dies on first try | Test examples in CI |
| Are prereqs stated before install? | Cryptic install failures | Disclose runtime and platform reqs |
| Is there a links section to deeper docs? | Dead end after README | Add a next-step ladder |
| Can evaluators tell the project is maintained? | Looks abandoned | Add a maintenance signal |
| Is there a visual showing what success looks like? | Hard to picture the result | Add a screenshot, GIF, or output block |

## Cross-references

- → `setup.md` for the actual install steps after the user commits.
- → `docs.md` for the deeper reference site the README links out to.
- → `examples.md` for runnable sample apps the README points at.
- → `package.md` for the registry-page (npm, PyPI, crates) metadata that
  mirrors the README.
- → `changelog.md` for the release-notes surface linked from the README.
- → `docs-experience-heuristics` when README work is part of a cross-audience
  documentation system or agent-readable docs strategy.
