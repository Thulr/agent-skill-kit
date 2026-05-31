# Contributor Playbook

## Scope

Repo onboarding, local setup signposting, test expectations, PR template,
code review loop, release steps, ownership boundaries. Routes to `setup.md`
for fresh-fork install, `inner-loop.md` for the edit-run-test cycle a
contributor uses, and `docs.md` for first-PR doc patterns.

## Grounding

- **Karl Fogel — *Producing Open Source Software*** — welcoming guides, low-friction
  first PRs, `CONTRIBUTING.md` as a single source of truth, and governance
  norms that let contributors act without waiting for a maintainer.
- **GitHub Open Source Guides** — operational patterns for `CONTRIBUTING.md`,
  code of conduct, issue templates, `CODEOWNERS`, and PR templates that
  surface the right information at the right time.
- **Nicole Forsgren, Jez Humble, Gene Kim — *Accelerate*** — PR lead time
  (time from PR open to merge) is a leading indicator of team health; short
  lead times are statistically associated with higher-performing teams; rising
  lead time is a signal worth acting on before it compounds.

## Good signals

- A one-page `CONTRIBUTING.md` exists, covers where to start, and links out
  to deeper detail rather than inlining everything.
- First-PR friction is documented: which label to use, where to find starter
  tasks, and the expected review turnaround time.
- Ownership is explicit: a `CODEOWNERS` file or an area-tag scheme maps every
  part of the codebase to a responsible owner.
- The PR template names the evidence expected: passing tests, changelog entry,
  screenshots or command output where relevant.
- Release steps are scripted or documented in a checklist that any maintainer
  can follow, not confined to one person's memory.
- Issue templates separate bug reports from feature requests so the right
  context is collected up front.
- "Good first issue" labels have a curated, maintained list with clear
  acceptance criteria a stranger can act on.
- A code of conduct exists and maintainers respond to violations visibly.

## Common failures

- Setup requires a maintainer's help — "ping me in Slack" is a bus-factor
  smell, not a solution.
- The PR template is generic and does not say what evidence (tests, changelog,
  output) is required for the change type.
- Review turnaround time is unknown; PRs sit for weeks with no acknowledgment.
- Release steps live in one person's head; every release is a coordination
  event.
- First-time contributors get stuck on a lint configuration they cannot
  reproduce locally.
- No `CODEOWNERS`; contributors cannot tell who to ask for review or context.
- "Good first issue" labels are stale — tasks have closed dependencies or
  missing context, and nobody has audited them recently.
- The code of conduct is decorative; violations go unaddressed or are handled
  inconsistently.

## Heuristics

- **One-page CONTRIBUTING** *(design, audit)* — every contributor finds the
  starting point in one file; it covers where to begin, what to expect, and
  where to go for deeper detail. Embedding the full spec in `CONTRIBUTING.md`
  is a failure mode; linking is the right pattern.
- **Documented PR evidence** *(design, audit)* — the PR template names what
  proof a PR must include: which tests to run, whether a changelog entry is
  required, and when screenshots or command output are expected. A blank
  template is equivalent to no template.
- **Clear ownership** *(design, audit)* — a `CODEOWNERS` file or an area-tag
  scheme maps every file or directory to a responsible owner. Contributors
  should never wonder who to ask.
- **Scripted release** *(design)* — `./bin/release` or a committed checklist
  covers every release step. No one person should be a single point of
  knowledge for shipping.
- **Review SLA stated** *(design)* — the expected response time for PRs is
  written down in `CONTRIBUTING.md` and roughly honored in practice. An
  unstated SLA is an infinite SLA in practice.
- **Tested first-PR path** *(audit)* — a "good first issue" can be identified,
  completed, and submitted by a stranger without asking a maintainer for help.
  Periodic audits of the label set are the only way to keep this true.
- **PR lead time tracked** *(audit)* — measure how long PRs sit from open to
  merge. A rising average is an early signal of friction worth investigating
  before it drives contributors away.
- **Bug/feature template split** *(design, audit)* — issue templates are
  differentiated; a bug report collects reproduction steps and expected
  behavior, while a feature request collects motivation and alternatives
  considered.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is there a one-page `CONTRIBUTING.md`? | Tribal onboarding | Write one; link to deeper docs |
| Does the PR template list required evidence? | Generic template, reviewer guesses | Specify tests, changelog, output |
| Is ownership mapped (`CODEOWNERS` or tags)? | Routing failures and stalled reviews | Add `CODEOWNERS` or area-tag scheme |
| Are release steps scripted or documented? | Single-person dependency on every ship | Script and commit the checklist |
| Can a stranger close a "good first issue" without help? | Bus factor 1 on contributor ramp | Audit and refresh the label set |
| Is PR lead time monitored? | Silent accumulation of friction | Add a basic tracking dashboard |

## Cross-references

- → `setup.md` for fresh-fork install and environment bootstrap.
- → `inner-loop.md` for the local dev loop a contributor uses day-to-day.
- → `docs.md` for first-PR doc patterns.
