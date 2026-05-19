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

Do not create GitHub issues or roadmaps unless the user explicitly asks for
that side effect. Individual skills may set a narrower default for internal
artifacts, such as creating a findings ledger and workflow-state JSON when
thresholds are met; absent that skill-specific instruction, offer the tracking
artifact pair first.

## Finding IDs

Every trackable finding gets a stable ID:

`<skill-prefix>-<surface-or-layer>-<NNN>`

Examples:

- `CA-DEP-001` for clean-architecture dependency-rule findings.
- `CA-BOUNDARY-004` for clean-architecture boundary findings.
- `AG-GATES-003` for project-agentification gate findings.

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

Use the smallest artifact set the user needs:

- `templates/findings-ledger.md` is the source of truth for all findings.
- `templates/roadmap.md` groups findings into staged work packages.
- `templates/github-issue.md` turns one work package into an issue.
- `templates/workflow-state.json` records operational state across turns.

Ledger files are Markdown and use this path by default:

`docs/audits/<skill-name>-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`

The filename must start with the full skill name, for example
`clean-architecture-findings-ledger-2026-05-19-payments.md` or
`ux-heuristics-findings-ledger-2026-05-19-checkout.md`. If the target is not a
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
