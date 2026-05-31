# fixtures/

These files are **mock workspace content**, not skill code. They exist so
the Phase 2 grader (`evals/phase2-grader.py`) and Phase 3 integration test
(`evals/integration-test.sh`) have realistic inputs to feed into the agent
under audit.

| File | Used by | Purpose |
|------|---------|---------|
| `translator.py` | Phase 2 grader | Mock Level 0 hardcoded prompt; agent should diagnose Level 0 → recommend Level 2 DSPy scaffold |
| `agent.py` | Phase 2 grader | Mock un-sandboxed CLI loop; agent should recommend Level 3 sandbox harness BEFORE optimization |
| `rules.md` | Phase 2 grader | Workspace rules referenced by `agent.py` |
| `classifier.py` | Phase 3 integration test | Mock Level 0 ticket classifier; gets copied into `test-sandbox/src/` before the skill is invoked |

Do not edit these to make tests pass. If a test fails, fix the skill — not
the fixture.
