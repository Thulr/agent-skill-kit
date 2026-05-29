# Shared review workflow

One workflow, seven domains. After [`domain-router.csv`](./domain-router.csv)
selects a domain `D`, everything below runs against `references/D/` and
`templates/D/`. The domains share this engine; their playbooks, routing CSVs,
rubrics, personas, and lens identities are domain-specific and live under
`references/D/`.

## Step 1 — Pick intent

Load `references/D/intent-router.csv`. Match the prompt to one intent row.
Ambiguous → ask once with the intent menu. The router comes in one of two
shapes (see [`routing-contract.md`](../../_shared/routing-contract.md)):

- **Two-layer** (`dx`, `docs`, `perf`, `test`, `architecture`) — the intent row
  has a `registry_file` and a `default_template`. Go to Step 2a.
- **One-layer** (`ux`, `ui-craft`) — the intent row has `detail_files` and
  `templates`. Go to Step 2b.

## Step 2a — Two-layer: pick surface

Load the intent's surface registry named in `registry_file`
(`references/D/intents/<intent>.csv`). Match the prompt to one or more
surfaces, or `all` (where the intent allows it) for a multi-surface fan-out.
Load **only** the chosen row's `playbook` (`references/D/playbooks/<surface>.md`)
plus the files in its `core_refs` (severity/score rubric, personas, etc.).
Do not load other playbooks. For `all`, each spawned surface agent loads its
own playbook in Step 4.

## Step 2b — One-layer: load detail files

Load exactly the files listed in the intent row's `detail_files` (the
domain's playbook(s) plus its rubrics and dispatch file). The templates the
intent emits are named in the `templates` column.

## Step 3 — Identify persona / lens set

If `references/D/` defines reviewer personas or lens identities, load them
(`references/D/core/personas.md` and/or `references/D/subagent-dispatch.md`).
Each domain names its own lenses (e.g. dx uses first-time integrator /
maintainer / adversarial debugger; ux uses its own set). These anchor the
independent perspectives in Step 4.

## Step 4 — Dispatch reviewer lenses (default for audit/review/edge intents)

If the domain ships `references/D/subagent-dispatch.md`, dispatch its lenses in
parallel per that file (single-surface: one lens per agent; multi-surface
`all`: one surface per agent running the lenses inside). Fall back to
sequential lens-switching in one head if the host has no delegation primitive.
Skip dispatch for tiny deterministic checks, secret-bound work, or pure design
sketches where one pass suffices.

## Step 5 — Apply the playbook

Use the playbook heuristics tagged for the active intent. For audit/review,
score the surface with the domain's score rubric (`references/D/core/score-rubric.md`
where present). For design, name the good-shaped pattern. For debug/diagnose,
rank hypotheses before naming fixes. For edge/risk passes, scan every category
in the playbook. If sub-agents ran, synthesize their findings here.

## Step 6 — Severity + stable IDs

Apply severity to every audit/edge finding using
`references/D/core/severity-rubric.md`, and stable finding IDs using the
domain's prefix per `references/D/trackable-findings.md` (e.g. `DX-<surface>-NNN`,
`CA-<surface>-NNN`). IDs are immutable across re-runs.

## Step 7 — Emit output

Write the intent-specific template under `templates/D/` (named by the router's
`default_template` / `templates` column) — `audit-report.md` /
`design-doc.md` / `debug-runbook.md` / `edge-checklist.md` and the domain's
equivalents. In chat/TUI, prefer fixed-width text over Markdown pipe tables;
in saved Markdown files, keep table rows single-line. Every output names the
domain, intent, surface(s), lenses dispatched, the intent's load-bearing
section, severity per finding, and the grounding sources from
`skill.json.inspired_by`.

## Step 8 — Tracking state / closeout

For audit/review/edge outputs with 7+ findings, any severity 3–4, or a
save/track/closeout request, load `references/D/trackable-findings.md` and
follow its ledger + workflow-state contract. If the request names an existing
ledger, workflow-state, PR, branch, or finding ID, read saved state first and
update statuses only after each verification rule passes. Otherwise write both
artifacts under `docs/audits/` (fallback `audit-artifacts/`). Keep roadmaps,
external issues, and non-tracking edits opt-in.

## Modes

Guided Draft (default), Autopilot, Grill Me — each domain's
`references/D/modes.md` carries the contract (all sourced from
`skills/_shared/modes.md`). Offer the mode at bare invocation; default to
Guided Draft on concrete invocations.
