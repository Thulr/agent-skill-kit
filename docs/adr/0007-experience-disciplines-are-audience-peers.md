# ADR 0007: Experience Disciplines Are Audience-Differentiated Peers, Not Nested

**Status:** Accepted (2026-05-30). Names the conceptual model that
[ADR 0005](./0005-one-engine-many-surfaces-skills-are-routed-not-split.md) and
[ADR 0006](./0006-discipline-front-doors-vs-one-engine-many-surfaces.md) already
assumed structurally; supersedes neither.

## Context

A recurring question — "isn't DX just a subset of UX?" — has no written answer in
the catalog, yet the structure already takes a side. The canonical audience
matrix (`review-heuristics/references/docs/core/audience-matrix.md`) is a **flat**
table, not a nesting; `dx` and `ux` are **sibling** domains under
`review-heuristics` (0005); and `design-for-agents` calls itself "the agent-facing
analog of UX **and** DX" (0006). Three places encode peers, none states *why*, so
the next contributor can read the structure either way — and "DX ⊂ UX" is the
tempting default, because a developer *is* a kind of user and Nielsen/Norman
heuristics genuinely transfer to API surfaces.

The cost of leaving it implicit is concrete: a team that buys "DX is just UX"
staffs DX with product designers who optimize quickstart polish and delight, then
ship an SDK with no typed error hierarchy and a breaking change every minor
version — because the parts of DX that aren't UX are exactly the parts that get
dropped. The model needs to be load-bearing, not inferable.

## Decision

UX, DX, and AX are **audience-differentiated peers of one parent discipline —
experience design** (the design of a system for the cognition and goals of
whoever is on the other side; equivalently, human/agent–system interaction). They
are **not** nested. DX inherits UX's *cognitive theory* (mental models, friction,
feedback, error recovery — the Nielsen/Norman core) but is not contained by UX's
*practice*.

Each peer differs along three axes, and the non-overlap on both sides is too
large to nest cleanly:

| Peer | Audience | Substrate | Success metric | Cost of error |
|---|---|---|---|---|
| **UX** | End user | Visual GUI, copy, flows | Task completion, learnability, delight | Re-clickable — A/B-test and reship |
| **DX** | Developer (a *builder*) | Code & text — signatures, types, error strings, CLI flags, traces | Integration leverage — time-to-first-call, glue code eliminated, tickets avoided | Contract-permanent — APIs are forever (semver, deprecation) |
| **AX** | AI agent | Machine-readable structure — schemas, `llms.txt`, tool descriptions | Deterministic action under a context budget | Silent failure at scale |

The visual/interaction half of UX has no DX analog; the contract / type-system /
composition / permanence half of DX has no UX analog. Same parent, disjoint
extremities. **Content-ops** (freshness, ownership, feedback closure) is the
cross-cutting layer that serves all three, not a fourth peer audience.

The diagnostic that settles it: if DX were a strict subset of UX, then AX (agents
consume developer surfaces) would be a subset of DX, and all three collapse into
"UX." Nobody who has built agent-readable systems believes that — which is the
same reason the peer model beats the nesting model one level down.

## Consequences

- The audience matrix stays **flat by design** and now states the model
  explicitly (parent discipline + the three differentiators + an explicit
  "DX is not a subset of UX" note), citing this ADR. Both copies — the canonical
  `review-heuristics` matrix and the `design-for-agents` AX excerpt — carry the
  framing.
- Routing language treats `dx`, `ux`, and agent experience as **peers**: the
  `domain-router` `when_to_use` text for `dx`/`ux` names the sibling disciplines
  and the "not a subset" relationship, so an agent disambiguating a prompt sees
  the peer set, not a hierarchy.
- This is the **conceptual** decision; 0005 and 0006 are its **structural**
  expressions. 0005 makes `dx`/`ux` sibling domains of one review engine; 0006
  lets AX earn a peer *skill* because it is a distinct discipline (disjoint
  corpus + cross-skill orchestration), not because experiences nest. Read
  together: peers at the *concept* layer; routed-or-standalone at the *packaging*
  layer per the 0006 front-door test.
- **Staffing/measurement implication, recorded so it isn't re-litigated:** do not
  manage, staff, or measure DX as a branch of UX. Shared cognition-level
  heuristics transfer; contract, type-safety, and composition concerns do not
  have UX owners and must be owned within DX.
- **Risk:** the peer model could be misread as license to stand up a separate
  skill per audience. It is not — packaging is governed by 0006's front-door
  test, not by this ADR. A discipline being a *peer* does not make it a separate
  *skill*; `dx` and `ux` are peers that remain routed domains.

## History

- **2026-05-30:** Original decision (this ADR). Triggered by a maintainer asking
  whether DX is a subset of UX; the answer ("sibling, not subset") had no written
  home, so the model the catalog already assumed is recorded here.
- **2026-05-30 (later):**
  [ADR 0008](./0008-reverse-review-consolidation-split-by-domain-and-function.md)
  splits `review-heuristics` into per-domain × per-function skills. The **peer
  concept here is unchanged** — UX/DX/AX remain audience-differentiated peers of
  experience design. Only the *structural* expression updates: where this ADR
  says 0005 makes `dx`/`ux` "sibling **domains** of one review engine," post-0008
  they are sibling **skills** (`dx-critique`/`dx-design`/`ux-critique`/…). The
  audience matrix's canonical home moves with the content (see 0008 / the split
  spec).
