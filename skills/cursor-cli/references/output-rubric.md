# Output Rubric

Use this rubric to judge cursor-agent output before relaying it.

## Review Quality

Strong review output: leads with actionable findings; gives concrete file/line
references; distinguishes confirmed defects from speculation; explains impact
without exaggeration; includes targeted verification or test advice; says "no
findings" clearly when appropriate.

Weak review output: summarizes the change instead of reviewing it; gives generic
style advice; invents behavior not present in the diff; treats missing tests as a
finding without real risk; recommends broad rewrites without a concrete defect.

## Severity Calibration

- `critical`: data loss, credential exposure, remote code execution, or a
  production-stopping regression.
- `high`: likely user-visible breakage, security boundary failure, broken
  release/build path, or irreversible state corruption.
- `medium`: plausible bug or operational risk that should be fixed before merge.
- `low`: minor correctness, maintainability, or test gap worth noting but not
  blocking.

## Calling-Agent Checks

Before presenting results: verify file references exist; check the finding is
about changed behavior; drop duplicate findings; separate "must fix" from
"consider"; note any tests or commands that were not run. cursor-agent may have
run under a different model than the code's author — treat its output as an
independent second opinion, not authority.
