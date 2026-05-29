# Decision gates (go / no-go / pivot + kill criteria)

The gate every opportunity passes through after `synthesize` and
before `decide` emits the F/A/D/R memo. The point is to make the
go/no-go reproducible: name the criteria first, then evaluate, rather
than rationalizing a foregone conclusion.

## The three outcomes

### Go

Conditions, all of which must hold:

- **Market** quality is at least Medium (size × growth × structure ×
  five-forces; see `playbooks/market.md`).
- **Customer pain** is high and revealed (analytics, prior purchase,
  observed behavior) — stated-only evidence is not sufficient on its
  own.
- **Differentiation** survives the do-nothing comparison plus the
  three named direct/substitute competitors.
- **Unit economics** show a credible path to LTV/CAC > 3 and payback
  < 18 months in the base case (longer for capital-intensive,
  shorter for transactional).
- **No severity-4 risk** is unresolved or absent from the kill
  criteria.

### No-Go

Triggered by any of:

- Severity-4 risk that cannot be designed around.
- Market quality fails the five-forces test (e.g., dominant supplier,
  zero switching costs, infinite substitutes at price 0).
- Customer pain is stated-only and no test moves it to revealed.
- Unit economics require an unbounded CAC reduction or LTV expansion.
- Legal / regulatory finding makes the core mechanic illegal in the
  target jurisdiction.

No-go is a **release**, not a failure. Document the kill criteria
and the conditions that would make us reopen the bet.

### Pivot

Triggered when:

- Customer pain is real but the proposed solution doesn't match
  (problem stays, solution changes).
- The beachhead segment is wrong but adjacent segments score well.
- Channel economics fail but the product economics survive
  (channel changes; product stays).
- Technical approach fails but build-vs-buy reframing rescues
  feasibility.

A pivot is a **specific** change, not "we'll figure it out." Name
what changes, what stays, and the new top assumption + test.

## Kill criteria (forward commitment)

Kill criteria are conditions stated **before** investigation that, if
later observed, automatically trigger no-go without re-litigation.
The point is to install a commitment device before the founder is
emotionally invested in the outcome.

Good kill criteria are:

- **Observable** (a specific number, signal, or event — not "if it
  feels wrong").
- **Time-bounded** (by when must we have evidence either way).
- **Asymmetric** (severe enough that hitting them genuinely changes
  the call, not just a milestone-miss).
- **Pre-committed** (named before the test runs, with a witness — a
  co-founder, investor, manager — who can hold the commitment).

> Example: "Kill if we cannot get 3 paid pilots at $500/mo by
> 2026-09-01, OR if median time-saved in pilots is < 2 hours/week,
> OR if Apple rejects the App Store submission twice with no path."

Every severity-4 risk becomes a kill criterion by default; the team
can write it out explicitly with mitigation if they have one, or
accept it as binding if they don't.

## How `decide` uses this

The `decide` intent loads this file plus `fadr-framework.md`:

1. Check **Go** conditions — name each pass / fail with the F/A/D/R
   evidence that supports it.
2. If any fail → check **No-Go** triggers.
3. If No-Go triggers fire → emit no-go in the F/A/D/R memo with
   kill criteria documented.
4. Else if some conditions fail but not catastrophically → consider
   **Pivot**; name the specific change.
5. Else → **Go** with the named kill criteria for the next stage.

Every outcome carries a **review trigger** — the observable event
that would reopen the call (a new entrant, a regulatory change, a
failed assumption-test). Decisions without review triggers atrophy.
