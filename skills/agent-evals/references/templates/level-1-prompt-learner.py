"""Level 1 System-Prompt Learner template.

Use for open-ended agents or developer assistants whose durable behavior lives
in markdown rules. The loop proposes rule diffs from judge explanations, then
gates persistence with held-out evals and human review.

CI parses this with `python3 -m py_compile`; imports are not executed.
"""
from __future__ import annotations

import json
from pathlib import Path

import openai  # or anthropic, litellm


RULES_PATH = Path("CLAUDE.md")
PROPOSED_DIFF_PATH = Path("ai-ops/proposed-rules.diff.md")
RESULTS_PATH = Path("ai-ops/prompt-learning-results.json")

TRAIN_SET = [
    {
        "input": "Write a fast git-commit hook",
        "assertions": ["contains shebang", "uses git diff", "does not bypass hooks"],
    }
]
HELD_OUT_SET = [
    {
        "input": "Write a pre-push check that refuses broken tests",
        "assertions": ["runs tests", "reports failures", "does not use --no-verify"],
    }
]


def redact_trace(text: str) -> str:
    """TODO: remove secrets, customer data, chain-of-thought, and private files."""
    return text


def run_agent_on_task(task_input: str, current_rules: str) -> tuple[str, str]:
    """TODO: wire to the host workspace's agent runner.

    Return (artifact_or_patch, terminal_log). Do not mutate RULES_PATH here.
    """
    raise NotImplementedError("Wire to the host workspace's agent runner")


def judge_run(task_input: str, agent_output: str, logs: str, assertions: list[str]) -> dict:
    client = openai.OpenAI()
    prompt = f"""
Evaluate the agent run against required assertions.

Task: {task_input}
Output: {redact_trace(agent_output)}
Logs: {redact_trace(logs)}
Assertions: {assertions}

Return JSON with:
- passed: boolean
- failed_assertions: string[]
- critique: concise explanation of the missing rule, tool, test, or context
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def propose_rule_diff(current_rules: str, critiques: list[str]) -> str:
    client = openai.OpenAI()
    prompt = f"""
Current rules:
---
{current_rules}
---

Failure critiques:
{json.dumps(critiques, indent=2)}

Propose a minimal Markdown diff chunk. Merge duplicate guidance, delete or
rewrite stale/conflicting rules, and include only instructions that prevent
observed failures. Do not output a full rules file.
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def run_cases(cases: list[dict], rules: str) -> list[dict]:
    results = []
    for case in cases:
        output, logs = run_agent_on_task(case["input"], rules)
        verdict = judge_run(case["input"], output, logs, case["assertions"])
        results.append({"case": case["input"], **verdict})
    return results


def run_optimization_loop() -> None:
    current_rules = RULES_PATH.read_text()
    train_results = run_cases(TRAIN_SET, current_rules)
    critiques = [r["critique"] for r in train_results if not r["passed"]]

    if not critiques:
        print("No train failures. No rule diff proposed.")
        return

    proposed_diff = propose_rule_diff(current_rules, critiques)
    proposed_rules = current_rules + "\n\n" + proposed_diff
    held_out_results = run_cases(HELD_OUT_SET, proposed_rules)

    PROPOSED_DIFF_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROPOSED_DIFF_PATH.write_text(proposed_diff)
    RESULTS_PATH.write_text(
        json.dumps(
            {"train": train_results, "held_out": held_out_results},
            indent=2,
        )
    )

    if any(not r["passed"] for r in held_out_results):
        print("Held-out eval failed. Review ai-ops/prompt-learning-results.json.")
        return

    print(
        "Proposed diff written to ai-ops/proposed-rules.diff.md. "
        "Review and apply manually; do not auto-write learned rules."
    )


if __name__ == "__main__":
    run_optimization_loop()
