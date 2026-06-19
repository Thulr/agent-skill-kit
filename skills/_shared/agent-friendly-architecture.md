# Agent-friendly architecture patterns (shared)

This note is shared between `harden-repo-for-coding-agents` and `rules-from-coding-agent-failures` to avoid
drift. It summarizes what the recent repo-level agent literature actually supports about
"architecture that helps agents work on existing projects".

## 1) Make structure machine-queryable (graphs, not prose)

Agents routinely fail at reconstructing **build/test structure** and **cross-file dependencies**
from raw source alone under context limits.

Prefer a deterministic, machine-readable structure map that the agent can treat as ground truth:

- Build/test graphs (targets, runners, tests, dependency edges) as JSON (e.g., RIG-style maps;
  arXiv:2601.10112) — RIG reports **+12.2% mean accuracy and −53.9% completion time** across Claude
  Code / Cursor / Codex, with larger gains in multilingual repos. This is the marquee evidence for
  handing the agent a structure graph.
- Repository-level code graphs for navigation/retrieval (e.g., arXiv:2410.14684).
- Whole-repo symbol maps with a fixed token budget (Tree-sitter → dependency graph → PageRank),
  as a fallback when a richer graph isn’t available.

## 2) Boundaries help — but only if enforced structurally

Architectural boundaries (layering, dependency direction, “no cycles”, forbidden imports) *do*
help agents stay local and safe. The missing ingredient is enforcement: in noisy, open-ended
settings, models’ coupling reasoning is brittle (e.g., large F1 drops under distractors; see
arXiv:2511.20933).

Treat boundary constraints as **gates**, not prose:

- Custom lint rules (import allow/deny lists; layer rules).
- Architecture tests (dependency direction, slice/cycle rules).
- CI-required checks / branch protection.

Designing the boundary model (dependency direction, deep modules, right-sized seams) is owned by
`minimal-modular-code`; `harden-repo-for-coding-agents` owns the enforcement surface.

## 2b) Legibility-first at the source level (not just the graph)

Beyond a machine-queryable graph, the agent-specific design literature (Meng & Jackson, *What You
See Is What It Does*, SPLASH 2025, arXiv:2508.14511; Earendil's practitioner cut) reframes "good
architecture" for an LLM with finite context as **legibility**: a unit's behavior should be readable
from the unit, without tracing hidden magic. Concrete moves an `assess`/`harden` pass can check:

- **Grep-unique names** — symbols findable with one search, not overloaded common words.
- **Visible control flow / workflow phases** — explicit phases over implicit dispatch (dynamic
  imports, reflection, implicit ORM hooks).
- **Less hidden magic** — one obvious interface per risky surface; minimize action-at-a-distance.

Caveat: "legible" ≠ "tidy for a human reader" — the bar is the model's context budget. And named
clean/hex/onion *styles* are unvalidated as agent-success drivers; legibility + enforced boundaries
(§2) are the evidenced lever, the dependency rule is necessary but not sufficient.

## 3) Parallelize work via stable “design rules” (contracts)

For “4 agents in parallel”, the strongest software-architecture guidance is less “pick a specific
architecture style” and more **make modularity real**: identify a small set of stable contracts
(“design rules”) that let modules evolve independently.

- Parnas (1972) frames modules as *responsibility assignments* and argues decomposition should hide
  likely-to-change design decisions; expected benefit: separate groups can work with less
  communication and shortened development time.
- Baldwin & Clark, *Design Rules: The Power of Modularity* (MIT Press, 2000) formalize **design
  rules** as stable decisions (interfaces, APIs, standards) that decouple subordinate decisions:
  modules can be designed independently as long as they obey the rules.
- Wong et al., “Design Rule Hierarchies and Parallelism in Software Development Tasks” (ASE 2009,
  DOI:10.1109/ASE.2009.53) operationalize this into a design-rule hierarchy: modules in the same
  layer are predicted to be independent (parallelizable), while cross-layer dependencies predict
  coordination needs; their Apache Ant study observes substantially less technical communication
  within a layer than across layers.
- MacCormack, Baldwin, Rusnak, “Exploring the duality between product and organizational
  architectures: A test of the ‘mirroring’ hypothesis” (*Research Policy*, 2012,
  DOI:10.1016/j.respol.2012.04.011) finds strong evidence that loosely-coupled organizations
  produce more modular architectures — a good default mental model for multi-agent work.
- Herbsleb & Grinter, “Splitting the Organization and Integrating the Code: Conway’s Law
  Revisited” (ICSE 1999) highlights that coordination breakdowns often surface during integration;
  for agents this pushes even harder toward explicit interface contracts + integration tests.

Implication for agent swarms: treat design rules as **high-blast-radius artifacts** (interfaces,
schemas, dependency direction, core standards). Put ownership + gates around them; then assign agents
to independent modules “under” those contracts and rely on integration tests/CI to catch drift.

## 4) Plan multi-file edits with dependency + impact analysis

Repository-level edits benefit from explicit planning plus dependency/impact analysis (e.g.,
CodePlan: incremental dependency analysis + change impact analysis; arXiv:2309.12499).

## 5) Scale skill libraries with structural retrieval (same lesson)

Loading “everything” into context degrades agents. For large skill libraries, use a structure-aware
retrieval layer that returns a bounded dependency-respecting bundle (e.g., Graph of Skills;
arXiv:2604.05333).
