# Calibration — Right-Sizing Output to Project Scale

Shared contract for audit and design skills. Modes (`modes.md`) gate how much
the skill *asks*; calibration gates how much it *produces*. A finding that is
load-bearing for a public, versioned library is noise on a 20-file internal
prototype. Match recommendation depth and breadth to the project's stage,
size, and stakes — not to the number of code artifacts.

Resolve the tier at workflow step 4.5 — after intent, surface, and audience are
known, before applying the playbook or dispatching sub-agents. The tier is an
input to **emission**, never to severity.

## Cheap signals (no private-system inspection)

Read the tier from what is already in context. **Never snoop a private system
just to classify it** — cheap presence is not scope, and inferring scale from
an incidental signal instead of the project's actual stakes produces confident,
wrong calibration. When the signals below aren't already in hand, ask (next
section); don't go spelunking.

- **Size** — file / LOC count; single file vs multi-package monorepo.
- **Public surface** — exported package, published API / OpenAPI, many CLI
  commands, external consumers — vs none.
- **Maturity** — `v0.x`, "internal", "prototype", "spike", pre-release — vs
  published / versioned / "we ship this to customers".
- **Audience** — internal-only / personal vs external / public.
- **People** — solo or pair vs many contributors, CODEOWNERS, review gates.
- **Stated stakes** — "quick", "throwaway", "for now", "just me" are strong
  Prototype signals; "compliance", "GA", "customers", "SLA" push the tier up.

## Resolve the tier

Infer from the signals. **Ask one optionized question only when the tier would
materially change the output AND the signals are weak or conflicting** (Guided
Draft — one question, per `modes.md`). In Autopilot, pick the tier from the
signals and state it in the report. Default to **Growing** when genuinely
undecidable — it is the least-wrong middle.

## The three tiers

### Prototype — barely sufficient

Pre-release, internal, solo, few files, no external consumers.

- **Surfaces:** pick the 1–2 that matter. Do **not** run the `all` fan-out.
- **Emission:** collapse (see below). Lead with a tiny "Now" set (≈3 fixes).
- **Don't recommend** building a docs / test / perf *system* — gates,
  telemetry, feedback loops, dashboards, coverage matrices. Name them once
  under "Later", don't file them as findings.

### Growing — core plus high-leverage

Shipping to a team or early external users.

- **Surfaces:** the core surface(s) plus the one or two highest-leverage extras.
- **Emission:** per-artifact findings for the core; collapse the long tail.
- Recommend the gates / telemetry that pay for themselves now; defer the rest
  to "Later".

### Load-bearing — full coverage

Public, multi-team, versioned, many consumers. This is the catalog's default
behavior:

- **Surfaces:** the full set; the `all` fan-out is appropriate.
- **Emission:** per-artifact coverage; "every method / endpoint / flag" applies.

## The every-X collapse rule

Playbook heuristics phrased "*every* method / endpoint / flag / error / empty
state needs X" scale to the count of code artifacts. Below Load-bearing,
**collapse** per-artifact gaps of the same mechanism into **one systemic
finding** — "API reference is absent; for an internal 12-endpoint tool,
document the 3 most-used inline in the README" — not twelve near-identical
findings.

The collapsed finding **inherits the max severity** of the gaps it subsumes, so
a severity-4 is never buried inside a roll-up. Calibration reshapes *how many
findings you write and which surfaces you run* — it never edits the severity
rubric or the score caps. A critical finding is critical at every tier.

## Output

Name the resolved tier in the report Summary (`Project tier:`), and split the
recommendations into **Now (proportional to a `<tier>` project)** and **Later
(as it grows)**. The Later list is where deferred best-practice lives — visible,
not lost, but not competing for attention with what matters now.

## Grounding

- **Barely-sufficient / just-good-enough documentation** (agile modeling) —
  produce the least that serves the audience's *current* need; more is waste
  until the need is real.
- **YAGNI / "the simplest thing that could possibly work"** (extreme
  programming) — don't build for a scale the project doesn't have yet.
- This catalog's **W6** (token budget is the dominant scarcity — find the
  smallest high-signal set) and **W8** (ship light, evolve) — see
  `empirical-warnings.md`.
