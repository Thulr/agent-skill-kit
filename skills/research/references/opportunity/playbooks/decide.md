# Decide Playbook

## Scope

The final fold: convert investigated areas + synthesis into a
named decision (go / no-go / pivot) with kill criteria and a review
trigger. The point is to make the call reproducible and
forward-committed — what we will do, what would reverse it, what
would have to be true for the call to change.

- In: F/A/D/R fold across areas (using `core/fadr-framework.md`);
  go/no-go evaluation against `core/decision-gates.md`; kill
  criteria authoring; pivot specification; review-trigger naming.
- Out: per-area deep dive (`investigate`); cross-area consolidation
  (`synthesize`); proposal-level adversarial review
  (`proposal-red-team`); execution plan stress-test
  (`plan-red-team`).
- Intents this surface answers: decide (primary), synthesize (sec.).

## Grounding

- **Convo.txt — the FADR test.** "A research branch that ends in
  notes but not decisions is just organized procrastination." The
  decision step is non-optional.
- **Eric Ries — *The Lean Startup*** — pivot vs persevere as a
  forward-committed decision with reasoning, not a quiet course
  correction.
- **Gary Klein — *Pre-Mortem*** — for review-triggers and kill
  criteria as commitment devices before the bet runs.

## Good signals

- Decision is one of three named outcomes: **Go** / **No-Go** /
  **Pivot**. Not "we'll continue researching" — that's a
  scope-extension decision, made explicit if needed.
- Each outcome is supported by the Go-conditions and No-Go-triggers
  in `core/decision-gates.md`. The decision says which conditions
  pass and which fail, with the F/A/D/R citations.
- Kill criteria are forward-committed: observable, time-bounded,
  asymmetric, pre-committed (named before the test runs). A witness
  (co-founder, investor, manager) is named.
- A review trigger is named: what observable event would reopen
  the decision (a new entrant, a regulatory change, a failed
  assumption-test, a new piece of revealed evidence).
- Top-3 assumptions and their tests are listed — the operational
  bridge between today's decision and tomorrow's evidence.
- Pivot, if chosen, names what changes, what stays, and the new
  top assumption.

## Common failures

- **Decision-deferral.** "Need more research" used to avoid the
  call. Sometimes legitimate; usually a hedge. Mitigation: if
  deferring, name *exactly* what evidence would let us decide and
  by when.
- **Kill criteria as soft hopes.** "Kill if it feels wrong" — not
  observable, not pre-committed. Mitigation: numbers, dates,
  events.
- **Decisions without a review trigger.** Decisions atrophy. A
  Go without "we'll review at $X ARR or 6 months whichever comes
  first" tends to stay Go past the point it should have flipped.
- **Pivot as "we'll just iterate."** A pivot is a specific change;
  vague iteration is not a pivot. Mitigation: name what changes,
  what stays, the new top assumption + its test.
- **Severity-4 risks not in kill criteria.** A known-fatal risk
  without a kill criterion is silently betting the company. Catch
  here.
- **No witness on kill criteria.** Self-policed kill criteria are
  weak. A witness is what makes them hold under emotional
  investment.

## Heuristics

- **(decide)** *Pick one of three.* Go / No-Go / Pivot. "Defer"
  requires naming exactly what evidence + by when would let us
  decide.
- **(decide)** *Evaluate against `core/decision-gates.md`.* Each
  Go-condition: pass / fail with F/A/D/R citation. Each No-Go
  trigger: fire / no-fire with citation.
- **(decide)** *Kill criteria — observable, time-bounded,
  asymmetric, pre-committed.* Numbers, dates, events. Named
  witness.
- **(decide)** *Review trigger named.* What observable event
  would reopen the decision. Without one, decisions don't get
  revisited.
- **(decide)** *Top-3 assumptions → next tests.* Each assumption
  has a falsifiable <1-week test, an owner, a deadline.
- **(decide, synthesize)** *Pivot specification.* What changes
  (segment, product, channel, model). What stays. The new top
  assumption + its test.
- **(decide)** *Severity-4 risks: resolved, mitigated to
  threshold, or kill criterion.* No fourth option.
- **(decide)** *Confidence honesty.* If the Go is built on
  L-confidence assumptions, the call is Conditional-Go with the
  tests that promote L → H named.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is the outcome one of Go / No-Go / Pivot (or Defer with named evidence-by-date)? | Vague continuation | Force the call. |
| Are Go-conditions / No-Go-triggers evaluated with F/A/D/R citations? | Decision without evaluation | Re-evaluate per `decision-gates.md`. |
| Are kill criteria observable, time-bounded, asymmetric, pre-committed? | Soft hopes | Re-spec with numbers, dates, events. |
| Is a witness named on kill criteria? | Self-policed | Name a witness (co-founder / investor / manager). |
| Is a review trigger named? | None | Name the event that would reopen the call. |
| Are top-3 assumptions converted to <1-week tests with owners? | Open assumptions | Spec tests + owners + deadlines. |
| Are severity-4 risks resolved, mitigated to threshold, or in kill criteria? | Hanging severity-4 | Resolve / threshold / kill. |
| Is confidence honesty preserved (Conditional-Go if L assumptions)? | L silently treated as H | Re-tag as Conditional with named promoting tests. |

## Cross-references

- → `references/playbooks/synthesize.md` — the prior step.
- → All area playbooks — the evidence sources.
- → `references/core/fadr-framework.md` — the fold each area
  artifact ends in.
- → `references/core/decision-gates.md` — Go-conditions, No-Go-
  triggers, kill criteria mechanics.
- → `references/core/severity-rubric.md` — for severity-4 → kill
  criterion routing.
- → `references/intents/decide.csv` row `go-no-go` / `kill-criteria`
  / `pivot` — the entry point.
- → `templates/fadr-memo.md` — the artifact this playbook produces.
- → Sibling skills: `premortem` for backwards-from-failure depth;
  `proposal-red-team` for adversarial pitch review;
  `plan-red-team` for execution-plan stress-testing. Use them
  *before* commitment to high-stakes decisions; they are not
  substitutes for `decide`.
