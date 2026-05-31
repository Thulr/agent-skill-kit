# Test Personas

Use these personas to anchor reviews. Assigning a persona prevents the reviewer from imagining only themselves as the audience.

## 1. Test author (you, three months ago)

Wrote the test under deadline. Knew the code intimately at the time; will not in six weeks. Cares: did I capture intent? Will I recognize what this test was for when it goes red?

## 2. On-call engineer at 3am

Did not write the test. Did not write the SUT. Got paged because the test went red in CI on a Sunday deploy. Cares: what was supposed to happen? what actually happened? where do I look first? **The diagnosability lens.**

## 3. Suite operator

Owns the whole test suite as an asset. Cares about runtime, flakiness rate, signal-to-noise, infra cost, and which tests provide the most bug-catching per minute of runtime. **The portfolio lens.**

## 4. Test skeptic reviewer

Reviewing a PR that adds tests. Believes most tests are written badly and most coverage is theater. Cares: does this test actually exercise behavior, or does it just go through the motions to bump coverage? **The false-pass lens.**

## 5. Refactorer (six months from now)

Has good intentions and a legitimate need to restructure the SUT. Cares: which tests will break for the right reason (I changed observable behavior) vs. the wrong reason (I renamed an internal method)? **The robustness lens.**

## How to use

For `review`: pick the persona most at risk from the test as written, and report findings in their voice.
For `author`: write for at least personas 1 and 2 simultaneously.
For `triage`: persona 2 is always relevant.
For `strategize` and `prune`: persona 3 is the primary lens.
