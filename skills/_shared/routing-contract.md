# Routing-CSV contract

Canonical reference for the progressive-disclosure routers shared across the
catalog. A skill's `SKILL.md` loads a small router CSV first and only then
loads the one playbook the route names — keeping the always-on token budget
low (W6). This file documents the column vocabulary so a new skill picks an
existing router shape on purpose instead of forking a new one silently (the
failure class behind the historical `ui-craft`/`ux` 5-column header
divergence; see AGENTS.md Rule 2).

Well-formedness (non-empty header, no ragged rows, `#`-comment lines allowed)
is gated by [`scripts/check-routing-csv.sh`](../../scripts/check-routing-csv.sh),
run in `just check` and CI across all three install lanes. Column vocabulary
below is **convention**, not a hard gate — the catalog intentionally supports
two intent-router shapes.

## Family router (top level, optional)

When one skill covers several domains or decision-frames, the first router
selects which sub-tree to descend into. One row per domain/frame.

| CSV | Columns | Used by |
|---|---|---|
| `domain-router.csv` | `domain,name,when_to_use,path` | `review-heuristics` |
| `frame-router.csv` | `frame,name,when_to_use,path` | `research` |

`path` is the `references/<sub-tree>/` the route descends into; that sub-tree
then carries its own intent-router.

## Level-1 router — intent (`intent-router.csv`)

Two legitimate shapes. Pick one; do not invent a third without documenting it
here.

- **Two-layer** (intent → surface → playbook). The intent row names a
  registry of surfaces to load next:
  `intent,name,when_to_use,registry_file,default_template`
  — `registry_file` points at `intents/<intent>.csv`. Used by `dx`, `docs`,
  `perf`, `test`, `architecture` domains and `research`'s `decide` frame.
  `intent-router.csv` may carry an `additional_rubric` column (e.g. `assess`
  loading a maturity rubric) and a `when_to_pick` column for worked hints.

- **One-layer** (intent → files directly), for skills with no surface layer:
  `intent,trigger_examples,detail_files,templates,notes`
  — `detail_files` lists the reference files to load for that intent. Used by
  the `ux` and `ui-craft` domains.

- **Umbrella hand-off** (a variant of the one-layer shape used by a discipline
  front-door): same columns
  `route,trigger_examples,detail_files,templates,notes`, but rows mix two kinds
  — *load-a-playbook* rows (non-empty `detail_files`) and
  *hand-off-to-a-sibling-skill* rows (empty `detail_files`; `notes` names the
  target top-level skill). Used by `agent-experience`'s `ax-router.csv`, which
  both reviews AX surfaces and routes out to `project-agentification` /
  `evidence-driven-agent-rules` / `eval-flywheel`. This is the only router shape
  that routes across top-level skills; it is reserved for umbrella disciplines
  (see ADR 0006), not for splitting one engine.

## Level-2 router — surface (`intents/<intent>.csv`, `surface-router.csv`)

One row per surface reachable from an intent.

`surface,name,when_to_use,playbook,core_refs` — `playbook` points at
`playbooks/<surface>.md`; `core_refs` lists shared rubric/persona files. An
`output_template` column may be added when the surface emits a specific
artifact (e.g. `research`'s `decide` intents). `project-agentification`'s
`surface-router.csv` retains `layer,sub_surface,what_it_covers` grouping
columns.

## Non-routing CSVs

`starter-scenarios.csv` is example data (named worked scenarios for bare
invocation), not a router; its columns vary by skill and it is **not** subject
to this contract or the gate.
