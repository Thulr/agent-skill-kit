# Trackable Findings Workflow

Use this shared workflow when an audit, review, assessment, or diagnostic output
produces enough findings that the user needs follow-through, not just a report.

## When To Load

Load this file when any of these are true:

- The output has 7+ findings.
- Any finding is severity 3 or 4.
- The user asks for a roadmap, GitHub issues, a checklist, workflow state,
  closeout, or a way to track progress.
- A later run references existing finding IDs, a ledger, a roadmap, GitHub
  issues, a PR, or a diff and asks what is done.

Do not create GitHub issues, roadmaps, or modify non-tracking project files
unless the user explicitly asks for that side effect. Tracking artifacts are the
only default write allowed by this workflow. Audit/review skills in this catalog
should create the findings ledger and workflow-state JSON by default when
thresholds or skill-specific instructions require them. Absent that
skill-specific instruction, offer the tracking artifact pair first.

## Finding IDs

Every trackable finding gets a stable ID:

`<skill-prefix>-<surface-or-layer>-<NNN>`

Examples:

- `MM-BND-001` for minimal-modular-code boundary findings.
- `MM-MIN-004` for minimal-modular-code slop findings.
- `AG-GATES-003` for agent-readiness gate findings.
- `DX-CLI-002` for dx-audit CLI findings.
- `SR-SOURCE-001` for skill-reviewer source-safety findings.
- `ED-L4L5-001` for agent-rules maturity gaps.

IDs are immutable once emitted. If a finding is split, keep the original as
`superseded` and create new IDs. If findings merge, keep all IDs and list the
same work package as their closure path.

## Lifecycle

Primary statuses:

- `discovered` - audit found it.
- `accepted` - user agrees it matters.
- `planned` - grouped into roadmap or issue-sized work.
- `in_progress` - someone is working it.
- `implemented` - a change claims to fix it.
- `verified` - the narrow verification rule passes.
- `closed` - maintainer/user accepts the verification.

Side statuses:

- `blocked`
- `needs_evidence`
- `deferred`
- `wont_do`
- `superseded`

Checking a box means `verified` or `closed`, never merely `implemented`.

## Artifact Flow

Default flow:

`audit report -> findings ledger + workflow state -> roadmap -> selected GitHub issues -> closeout pass`

Loop-closure flow:

`signal artifact -> cluster failure modes -> work packages -> artifact changes -> verification closeout -> scoreboard`

A tracking artifact is useful only if it can change the next run. If the
workflow stops at a ledger, report, dashboard, or reflection log, call that out
as **open loop** and propose the smallest closure path before adding more
findings.

Use the smallest artifact set the user needs:

- `templates/findings-ledger.md` is the source of truth for all findings.
- `templates/roadmap.md` groups findings into staged work packages.
- `templates/github-issue.md` turns one work package into an issue.
- `templates/workflow-state.json` records operational state across turns.

Ledger files are Markdown and use this path by default:

`docs/audits/<skill-name>-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`

The filename must start with the full skill name, for example
`dx-audit-findings-ledger-2026-05-19-payments.md` or
`harden-repo-for-coding-agents-findings-ledger-2026-05-19-gates.md`. If the target is not a
repo or `docs/audits/` is not writable, fall back to
`audit-artifacts/<skill-name>-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
and report the fallback path. Save workflow-state JSON alongside the ledger by
default as:

`docs/audits/<skill-name>-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`

If using the fallback directory, save workflow state as:

`audit-artifacts/<skill-name>-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`

For 7+ findings, offer the ledger + workflow-state pair first unless the
consuming skill explicitly says to create them by default. For 15+ findings,
group before making issues. Avoid one issue per finding unless the user
explicitly wants that.

## Loop Closure Contract

Every skill that emits a durable signal artifact should be able to answer five
questions before it claims the loop is closed:

1. **Signal artifact** - where observations accumulate: a findings ledger,
   workflow-state JSON, reflection log, trace export, design state, eval report,
   or issue list.
2. **Interpretation method** - how observations become categories: severity,
   surface, failure-mode ontology, repeated deferral, user-journey step, trace
   span, or root cause.
3. **Closure surface** - what durable artifact can change the next run: tests,
   eval cases, `AGENTS.md`, `SKILL.md`, playbooks, hooks, CI, docs, tool schema,
   prompt, product workflow, or roadmap package.
4. **Verification rule** - what evidence proves the change worked: command
   output, static check, browser/tool run, eval rerun, human review, diff link,
   or trace comparison.
5. **Progress view** - how the user sees momentum: the since-last-run
   scoreboard plus the remaining open clusters or findings.

When a user asks "now what?", "close the loop", "what do we do with these?",
or references a pile of existing observations, do not emit another flat report.
Resume from the signal artifact, cluster recurring failure modes, create
reviewable work packages, and attach one verification rule to each package.

## Closure Surfaces

Pick the lowest-maintenance artifact that changes future behavior:

| Signal says... | Prefer closing with... | Verification example |
|---|---|---|
| Same defect recurs in code or tests | Regression test, eval case, or fixture | The formerly failing case fails before and passes after. |
| Agent repeats an instruction miss | `AGENTS.md`, `SKILL.md`, or playbook patch | Static checks pass; cited failure entries justify the wording. |
| Agent skips a must-run step | Hook, CI gate, script, or deterministic check | Regression fixture exercises the skipped-step path. |
| Users hit unclear product behavior | Product requirement, UX issue, or roadmap package | Browser/user-journey verification or accepted design review. |
| A finding needs external prioritization | Roadmap work package or GitHub issue | Issue links the finding IDs and done-when evidence. |

Avoid closing a loop by adding only more prose. If prose is the right surface,
keep it minimal, cite the signal artifacts that justify it, and include a
future verification path.

## Work Packages

Group findings by the smallest coherent change that can be reviewed and
verified. A work package should list:

- Finding IDs it intends to close.
- Files or surfaces likely to change.
- Verification commands or audit checks.
- Dependencies, blockers, and decisions.
- A clear "done when" statement.

## Verification Closeout

Given a ledger, roadmap item, issue, PR, diff, or branch:

1. Extract referenced finding IDs.
2. Re-run the narrow checks for those IDs.
3. Mark passing findings as `verified`; for failing findings, leave the
   existing status unchanged unless the evidence supports `blocked` or
   `needs_evidence`.
4. Attach evidence: file:line, command output summary, diff pointer, PR/issue,
   or reviewer decision.
5. Close only findings whose verification rule passes.

GitHub issue closure does not automatically close findings. Treat an issue or
PR as evidence to inspect, not proof.

## Resume Path

When a later run references a workflow-state JSON, ledger path, finding ID, PR,
or branch, resume from the strongest artifact available before producing new
findings:

1. If a `workflow-state.json` is provided, read it first, then read the ledger
   it references.
2. If only a ledger is provided, read the ledger directly; do not require a
   workflow-state file to perform closeout.
3. If only finding IDs, a PR, diff, or branch are provided, extract IDs and use
   the ledger named by the user or discoverable from context; ask for the ledger
   only when the verification rule is unavailable.
4. Confirm the skill name and scope match the current request.
5. Extract only the requested IDs, or all open IDs when the user asks for a
   broad closeout pass.
6. Re-run each verification rule and update status/evidence in the ledger.
7. Write or update workflow-state JSON when continuing the workflow, capturing
   current phase, selected IDs, verification timestamp, blockers, and next safe
   action.
8. **Emit a Since-last-run scoreboard.** Whenever resume reads an existing
   workflow-state or ledger, lead the new output with the scoreboard described
   below — before any new findings — so the user sees momentum, not a fresh
   wall of issues.

If the referenced artifacts are missing or from another skill/scope, stop and
ask for the correct artifact instead of inventing continuity.

## Since-last-run scoreboard

When resuming against an existing ledger or workflow-state, the new report
opens with a short scoreboard that compares the current scan to the previous
one. This turns the tracking artifact into visible progress instead of
restarting the user at "fresh wall of findings."

Emit the scoreboard as a fenced `text` block (so it renders single-line in
chat/TUI hosts that mangle Markdown tables) immediately under the report
heading. Include the prior run's date and scope.

Required fields:

- **Closed since last run** — count of findings whose status moved to
  `verified` or `closed`.
- **Regressions** — count of findings that were `verified`/`closed` last run
  and are now re-open (`discovered` or `in_progress`).
- **Still open** — count of findings not yet closed (carried forward).
- **New this run** — count of findings discovered this run with no prior ID.
- **Score delta** — for skills that emit a 0–10 surface score, report
  `previous → current` and the band change (e.g. Mixed → Healthy). Omit when
  the skill does not score.

Example:

```text
Since 2026-04-15 (payments scope):
  Closed since last run: 2   (MM-BND-003, MM-MIN-001)
  Regressions:           1   (MM-BND-005 — re-opened by PR #214)
  Still open:            4
  New this run:          3
  Score delta:           4 → 6   (Eroded → Mixed)
```

When **zero** prior findings remain (clean resume) or no prior run exists,
skip the scoreboard and proceed with the normal report. Don't fabricate
deltas against a missing prior state.

## Workflow State

Workflow state is machine-readable operational memory. Store only:

- Current phase and status.
- Artifact paths or URLs.
- Selected finding IDs and work package IDs.
- User decisions and assumptions.
- Blockers and next safe action.
- Last verification timestamp and result summary.

Do not store secrets, credentials, private data, raw audit transcripts, or broad
personal facts in workflow state.
