# Output Rubric

Use this rubric to judge Claude Code output before relaying it.

## Review Quality

Strong review output:

- leads with actionable findings
- gives concrete file/line references where possible
- distinguishes confirmed defects from speculation
- explains impact without exaggeration
- includes targeted verification or test advice
- says "no findings" clearly when appropriate

Weak review output:

- summarizes the change instead of reviewing it
- gives generic style advice
- invents behavior not present in the diff
- treats missing tests as a finding without a real risk
- recommends broad rewrites without a concrete defect

## Severity Calibration

- `critical`: data loss, credential exposure, remote code execution, or a
  production-stopping regression.
- `high`: likely user-visible breakage, security boundary failure, broken
  release/build path, or irreversible state corruption.
- `medium`: plausible bug or operational risk that should be fixed before
  merge.
- `low`: minor correctness, maintainability, or test gap that is worth noting
  but not blocking.

## Reflection Quality

Strong cross-project reflection output:

- separates self-reported memory from evidence-backed observations
- names repeated user feedback or workflow checks without inventing examples
- avoids focusing on the current repository unless it appears in global history
- suggests concrete skills, instructions, hooks, templates, or evals
- marks claims that need corroboration

Weak reflection output:

- reviews the current repository instead of cross-project behavior
- overstates "I remember" claims without evidence
- copies raw private transcript material
- recommends broad global prose without a prevention mechanism

## Calling-Agent Checks

Before presenting results:

1. Verify file references exist.
2. Check whether the finding is about changed behavior.
3. Drop duplicate findings.
4. Separate "must fix" from "consider".
5. Note any tests or commands that were not run.
