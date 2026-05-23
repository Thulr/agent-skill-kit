"""Level 1 System-Prompt Learner template.

Use for open-ended agents or developer assistants. The loop runs an agent
against a held-out eval set, lets an LLM-as-a-judge produce structured
critiques on failure, and a meta-prompt optimizer appends corrective rules
to the markdown instruction file.

CI parses this with `python3 -m py_compile`; imports are NOT executed, so
`openai` / `anthropic` need not be installed in the sandbox. The skill
expects this script to be copied into the host workspace's `ai-ops/` dir
when a Level 1 scaffold is selected.
"""
import json
import os
import openai  # or anthropic, litellm


# 1. Define Golden Eval Dataset
EVAL_DATASET = [
    {
        "input": "Write a fast git-commit hook",
        "assertions": ["contains shebang", "uses git diff", "does not bypass hooks"],
    }
]


# 2. Run the Agent (Simulated Workspace Run)
def run_agent_on_task(task_input, current_rules):
    """Spin up the host agent with the current rules loaded into its context.
    Returns (final_patch_or_files, terminal_log)."""
    raise NotImplementedError("Wire to the host workspace's agent runner")


# 3. LLM-as-a-Judge Evaluation (Detailed Explanations)
def evaluate_run(task_input, agent_output, assertions):
    client = openai.OpenAI()
    prompt = f"""
    Analyze this AI agent's work.
    Task: {task_input}
    Agent Output: {agent_output}
    Required Assertions: {assertions}

    If any assertions failed, output a detailed, structured explanation of exactly
    WHY the agent failed and what instruction or checklist rule it skipped.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# 4. Meta-Prompt Optimizer (Markdown Patching)
def optimize_rules(current_rules, failure_critique):
    client = openai.OpenAI()
    prompt = f"""
    You are a Meta-Prompt Optimizer.
    We run a software engineering agent with these rules:
    ---
    {current_rules}
    ---

    During a recent test, the agent failed with this critique:
    "{failure_critique}"

    Analyze the failure. Output a precise Markdown text chunk to APPEND or MERGE
    into our rules that will explicitly prevent this failure mode in the future.
    Do not rewrite the whole file; output only the corrective rule to add.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def run_optimization_loop():
    rules_path = ".claudemd"
    with open(rules_path, "r") as f:
        current_rules = f.read()

    for case in EVAL_DATASET:
        output, logs = run_agent_on_task(case["input"], current_rules)
        critique = evaluate_run(case["input"], output, case["assertions"])

        if "FAILED" in critique or "assertion failed" in critique:
            new_rule = optimize_rules(current_rules, critique)
            current_rules += f"\n\n{new_rule}"

    with open(rules_path, "w") as f:
        f.write(current_rules)
    print("Optimization complete. Instruction files updated.")


if __name__ == "__main__":
    run_optimization_loop()
