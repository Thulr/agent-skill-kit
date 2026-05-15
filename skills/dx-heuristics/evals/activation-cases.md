# DX Heuristics Eval Cases

These evals check whether `dx-heuristics` activates at the right time and
produces useful DX review behavior without side effects from vague prompts.

## Static Verification

Run from the repository root:

```bash
bash skills/dx-heuristics/evals/run-static-checks.sh
```

The static check verifies that the skill:

- declares `name: dx-heuristics` in `SKILL.md` frontmatter
- describes concrete triggers for APIs, SDKs, CLIs, docs, setup, errors,
  local dev, build/test workflows, migrations, contracts, and contributors
- routes bare activation through `references/use-case-registry.csv`
- has a non-side-effectful bare-activation rule
- includes scoring, severity, heuristics, diagnostics, anti-patterns, and
  edge-case coverage in `references/dx-heuristics-framework.md`
- provides an artifact template for structured DX audits

## Behavioral Eval Protocol

Run each behavioral case in a fresh agent session with only this skill available
or explicitly loaded. Do not provide extra repository context unless the case
includes it. Record the response and score it against the pass/fail criteria.

Passing all cases means the agent:

- activates the skill for realistic DX prompts
- asks at most one blocker question when scope is missing
- does not inspect files, call networks, or write files from vague invocation
- names a target developer persona
- gives a current score, target score, ordered findings, concrete fixes, and
  verification evidence when reviewing a concrete surface

## Case 1: Bare Activation Menu

**Prompt**

```text
Use dx-heuristics.
```

**Expected behavior**

- Presents a concise mode or use-case menu.
- Waits for the user to choose a surface or mode.
- Does not inspect files, run commands, call network tools, or produce a fake
  audit.

**Fail if**

- It starts reviewing the repository without permission.
- It gives a DX score without a target surface.
- It asks multiple setup questions instead of offering a menu.

## Case 2: Concrete CLI Review

**Prompt**

```text
Review this CLI help output for DX. New users cannot figure out how to run a
local smoke test.

$ acme --help
Usage: acme [command]

Commands:
  init       Create config
  run        Run tasks
  check      Validate project

Options:
  --profile  Profile name
  --json     JSON output
```

**Expected behavior**

- Identifies the target developer as first-time user, contributor, or both.
- Scores current DX and sets target score to 10/10.
- Reviews command naming, missing examples, expected output, smoke-test
  discoverability, and failure recovery.
- Orders findings by severity.
- Gives concrete CLI/help text changes and a verification plan.

**Fail if**

- It only rewrites copy without assigning severity.
- It omits verification evidence.
- It recommends adding docs while leaving `acme --help` unable to reveal the
  smoke-test path.

## Case 3: Actionable API Error

**Prompt**

```text
The API returns "bad request" when the payload is wrong. Is that fine?
```

**Expected behavior**

- Treats the prompt as an actionable failure-state DX issue.
- Explains why the current message is insufficient for recovery.
- Recommends cause-specific validation messages with expected shape, invalid
  field, remediation, request or correlation id where appropriate, and tests.
- Asks for details only if needed to choose between compatible response shapes.

**Fail if**

- It says "bad request" is acceptable because HTTP 400 is standard.
- It gives generic advice without a concrete error response shape.
- It omits test or verification guidance.

## Case 4: Ambiguous Private-System Request

**Prompt**

```text
DX review our onboarding flow and tell me what to fix.
```

**Expected behavior**

- Asks one blocker question to identify the surface or evidence to inspect.
- Does not inspect private systems, files, browser targets, or network resources
  before the user provides scope.
- Offers likely surfaces such as README, quickstart, local setup, CLI help,
  SDK/API docs, examples, tests, or contributor workflow.

**Fail if**

- It begins tool use without knowing the review surface.
- It asks a long questionnaire before establishing the first review target.
- It invents findings without evidence.

## Case 5: Contributor Workflow Review

**Prompt**

```text
Review this contributor workflow for DX:

1. Clone the repo.
2. Run npm install.
3. Ask a maintainer for the test command.
4. Open a PR when it looks right.
```

**Expected behavior**

- Identifies contributor as the target developer.
- Flags missing explicit test command, missing success criteria, tribal
  knowledge, PR evidence expectations, and local setup verification.
- Includes an edge-case pass for fresh machines, Node/package-manager version
  skew, missing credentials, and flaky dependencies.
- Recommends concrete README/script/PR-template changes.

**Fail if**

- It only says "document the test command" and misses the broader local loop.
- It omits current and target DX scores.
- It does not include a way to verify the contributor path improved.
