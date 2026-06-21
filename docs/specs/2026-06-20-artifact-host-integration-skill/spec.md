# Spec: Add `artifact-host-integration` skill

**Date:** 2026-06-20
**Status:** Implemented (gates green)
**Decision record:** none required — adds one singleton inside the existing
`heuristics` family; no family-level architecture change (cf. ADR 0008/0011).

## Problem

The `design-workflows` source pack has two folders: the numbered design
playbooks and `design-host-integration/` (seven docs). `ui-design` already
distills the **whole** pack — its `skill.json` cites both packs in `inspired_by`
and `metadata.source_paths`. But `ui-design` is a *visual-craft* skill for an
agent **producing** an artifact, so it compresses the entire host-integration
protocol (~4,500 words: postMessage handshakes, the EDITMODE persistence block,
fixed-canvas scaling, speaker-notes sync, comment/scene anchors, direct-edit
markup, bundling/export) into a single ~370-word `prototypes-and-host.md`
summary. The precise *contract* — exact message types, marker shapes, attribute
names — is gone.

That contract has a **distinct audience**: whoever wires the artifact↔host
boundary (an agent emitting a host-cooperative artifact, or an engineer building
the host shell). The source README says it directly: "these aren't *design*
knowledge … they're *integration contracts*." Visual craft and integration
contract are different surfaces for different readers.

## Decision: separate skill, not a merge or a replacement

Considered three options (the framing the request arrived in):

- **Replace `ui-design`** — rejected. `ui-design` is the faithful distillation of
  the *design* half of the pack and is unrelated to most of the host protocol.
- **Merge the protocol into `ui-design`** — rejected. It would bloat a
  visual-craft skill with an engineering protocol, blur its audience, and push it
  past its word budget. The protocol depth `ui-design` *needs* (emit a
  cooperative artifact) it already has; the depth it drops is for a different
  reader.
- **Separate singleton skill** — chosen. Owns the full contract; `ui-design`
  keeps its thin designer-facing slice. The two are siblings from one source
  pack, fenced by description and cross-linked.

## Goal

A `heuristics`/`singleton` skill `artifact-host-integration` that routes over the
host pack's contracts and reproduces the protocol faithfully (exact message
types, markers, attributes, snippets), grounded 100% in the source pack.

## Constraints (from the gate contract)

- `metadata.family` is a closed enum (`heuristics | research | ax | discovery`);
  `function` is `audit | design | singleton`, and `audit`/`design` force a
  name-suffix + (for a complete pair) a `_shared/<domain>/` substrate +
  `docs/architecture/README.md` entry. → **`singleton`** (like
  `minimal-modular-code`): no suffix, no shared-substrate obligation.
- `family: heuristics` places it beside `ui-design` (also heuristics) in the
  catalog; `build-catalog.py` renders it automatically from `metadata`.
- SKILL.md must not leak any `inspired_by` author/title (source-leak gate); each
  skill sets its own word cap in `run-static-checks.sh`.

## Shape

One-layer router (`detail_files`/`templates`, like `ui-design`/`ux-audit`) over
seven contracts: `architecture`, `tweak-panel`, `fixed-canvas`, `speaker-notes`,
`mentioned-elements`, `direct-edit`, `bundling-export`. Every route also loads
`references/architecture.md` (shared conventions + the portability invariant) and
`references/modes.md` (relative symlink to `_shared/modes.md`). Emits
`templates/integration-checklist.md` (+ `handoff-readiness.md` for export).

## Boundary with `ui-design`

Real activation overlap: `ui-design` already has a `host-handoff` route and
activates on "prepare this prototype for export and direct editing." Resolution:

- `artifact-host-integration` owns the **deep contract** ("wire the tweak-panel
  handshake", "what's the EDITMODE block format", "build the host side").
- `ui-design` keeps the **designer's slice** ("prepare/polish my artifact").
- Both descriptions fence each other; overlapping queries appear as **negatives**
  in each skill's `trigger-evals.json`; `ui-design`'s `prototypes-and-host.md`
  cross-links to the full protocol.

## Acceptance criteria

- `bash skills/artifact-host-integration/evals/run-static-checks.sh` passes.
- `just check` green across all three lanes; `build-catalog.py --check` in sync.
- New skill appears in `npx skills add . --list`, the README Pick-a-skill matrix,
  and the README Catalog (heuristics family).
- SKILL.md grounded only in the source pack (no invented generalization).

## Risks

- **Outlier in `heuristics`.** The family prose is literature-grounded
  audit/design pairs; this is a project-pack-grounded protocol singleton. Same
  stretch `ui-design` already makes — acceptable; the family is the right home
  by surface adjacency.
- **Seam prompts** between visual prep and protocol wiring. Mitigated by the
  description fences + cross-linked negatives above.
