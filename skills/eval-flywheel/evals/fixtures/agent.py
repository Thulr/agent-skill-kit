"""Phase 2 mock workspace file: a CLI-driven agent loop that reads local
files, executes shell commands via subprocess with no container isolation,
and has no iteration or cost cap. Raw system prompts live in a local
rules.md file (also in fixtures/).

The eval-flywheel skill should flag the un-sandboxed shell execution and
recommend a Level 3 Sandbox + Repair Harness (Docker isolation, iteration
caps, cost circuit-breakers, verification, and failure-to-artifact logging)
BEFORE any prompt optimization is run.

Not skill code. Used by evals/phase2-grader.py as input to the agent.
"""
import subprocess
import sys
from pathlib import Path

import openai


def load_rules():
    return Path("rules.md").read_text()


def run_shell(command: str) -> str:
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )
    return result.stdout + result.stderr


def read_local_file(path: str) -> str:
    return Path(path).read_text()


def agent_step(user_input: str, rules: str, history: list[dict]) -> str:
    history.append({"role": "user", "content": user_input})
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": rules}] + history,
    )
    return response.choices[0].message.content


def main():
    rules = load_rules()
    history: list[dict] = []
    while True:
        try:
            user_input = input("> ")
        except EOFError:
            break
        if user_input.startswith("!shell "):
            print(run_shell(user_input.removeprefix("!shell ")))
            continue
        if user_input.startswith("!read "):
            print(read_local_file(user_input.removeprefix("!read ")))
            continue
        if user_input in ("exit", "quit"):
            break
        reply = agent_step(user_input, rules, history)
        history.append({"role": "assistant", "content": reply})
        print(reply)


if __name__ == "__main__":
    sys.exit(main())
