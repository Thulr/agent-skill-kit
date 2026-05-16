# Test Oracles

An *oracle* is a principle that tells you whether a test result is right or wrong. Most tests have an explicit oracle (an `assert` clause). Exploratory testing relies on softer oracles. This file distills two widely-used heuristic mnemonics from the rapid-software-testing tradition. Use them in:
- `exploratory` sessions to drive variation
- `review` mode to check whether a layer's tests cover any oracle other than "the function returned the value I hard-coded"
- as raw material for the **bug-shape hunter** lens prompt

## SFDIPOT — coverage of testable aspects

Used to ensure an exploratory session covers more than one obvious aspect of the system.

| Letter | Aspect | Sample probe |
|---|---|---|
| **S** | Structure | What components, files, modules exist? Have we exercised each? |
| **F** | Function | What does each function do? Have we triggered all the documented behaviors? |
| **D** | Data | What inputs (empty, null, max, malformed, unicode, very long, very small)? |
| **I** | Interfaces | API, CLI, UI, queue, file — each is a separate surface |
| **P** | Platform | OS, browser, locale, timezone, CPU arch, container vs bare metal |
| **O** | Operations | How is it used in real workflows, including misuses and recovery? |
| **T** | Time | Behavior over time: timeouts, scheduling, sequencing, concurrency, clock changes |

A unit test covers one cell. A suite that only covers SF (structure + function) has a coverage gap on D, I, P, O, T.

## FEW HICCUPPS — consistency oracles

A failure to satisfy any of these is potentially a bug. Useful when there's no specification to assert against.

| Letter | Consistency with… |
|---|---|
| **F** | Familiarity (does the system behave like the user has come to expect of it) |
| **E** | Explainability (can the behavior be reasoned about?) |
| **W** | World (real-world facts and conventions) |
| **H** | History (prior versions of the system) |
| **I** | Image (the company/product brand and reputation) |
| **C** | Comparable products |
| **C** | Claims (marketing, docs, help text) |
| **U** | User expectations |
| **P** | Purpose (the system's stated goals) |
| **P** | Product (internal consistency across the system) |
| **S** | Standards (regulatory, technical, accessibility, security) |

When a tester says "this is wrong" and can't point at a spec, the conversation goes faster if they cite an oracle: "this violates *Standards* — it's not WCAG-compliant," or "this violates *History* — version 2.3 returned 200 here, this returns 204."

## Using oracles in `review` mode

For each layer, ask: *which oracles does this test or test class actually validate?* Most automated test suites validate Function and a slice of Data. Suites that never test Time, Platform, or Operations are prone to mode 4 (gap).

## Cross-references

- `failure-modes.md` — mode 4 (gap) is most often a missing-oracle problem
- `references/layers/exploratory.md` — exploratory sessions should pick an oracle and drive variation along it
- `references/subagent-dispatch.md` — the bug-shape hunter lens uses these oracles to imagine bugs the existing suite misses
