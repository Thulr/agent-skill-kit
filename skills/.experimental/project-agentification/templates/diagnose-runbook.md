# Diagnose Runbook — <symptom-name>

**Date:** <YYYY-MM-DD>
**Symptom source:** <PR #, session ID, trace ID, user report>

## Symptom

<What the agent did or didn't do. Concrete: name the file, the wrong output, the missed step, the loop that didn't terminate.>

## Hypothesis ranking

Ranked by prior probability for this class of failure. Investigate top-to-bottom; stop at the first hypothesis confirmed by evidence.

1. **Context rot** (lost-in-the-middle, instruction follow-through decay)
   - Evidence to check: AGENTS.md line count (>200 = suspect, W2); number of instructions injected by harness; trace showing the agent ignored a middle-of-file rule.
2. **Ambiguous instruction** (rule could be read two ways)
   - Evidence to check: re-read the rule the agent violated; did it have an unambiguous interpretation?
3. **Token-budget overflow** (file or context exceeded budget)
   - Evidence to check: file size (>500 lines = suspect); total context loaded vs model's limit; was there a binary-search / surgical-extraction fallback?
4. **Missing tool** (agent guessed instead of calling an MCP method that didn't exist)
   - Evidence to check: would an MCP method have made the right answer trivially callable?
5. **Wrong harness layer** (e.g., put global rule in skill where AGENTS.md was needed, or vice versa) — W7
   - Evidence to check: would moving the rule between AGENTS.md / SKILL.md / hook have produced the right behavior?
6. **Unmet preconditions** (build broken, test flaky, env drift)
   - Evidence to check: was the dev loop deterministic? Did the test-suite signal what it should have?
7. **Nondeterministic env** (flaky test, race, time-of-day-dependent state)
   - Evidence to check: same agent + same input → different output?

## Confirmed root cause

<One of the hypotheses, with the specific evidence that confirmed it.>

## Fix

**Layer / sub-surface affected:** <legibility|action|control / sub-surface>
**Specific artifact to add or edit:** <file path / hook / MCP method>
**Pointer to the relevant playbook section:** <references/playbooks/<sub-surface>.md#<heuristic-id>>

## Prevention — eval / hook to add

<Specific eval case or hook config that would have failed-loud at the time the regression was introduced. Add this to `evals/` so the failure can't recur silently.>

## Empirical warnings invoked

<list of W-IDs that this diagnosis surfaced>

## Sources cited

(list of skill.json `inspired_by` entries)
