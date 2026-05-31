"""Level 3 Sandbox + Repair Harness template.

Use for action-executing agents that run shell commands, write files, or
otherwise mutate system state. Enforces deterministic container execution,
iteration caps, cost circuit-breakers, and a failure-to-artifact repair loop
around an inner agent loop.

CI parses this with `python3 -m py_compile`; the script does NOT execute
imports or shell commands at import time. The skill copies this file into
the host workspace's `ai-ops/` directory when a Level 3 scaffold is
selected.
"""
import json
import subprocess
import sys
from pathlib import Path


class AgentSandboxHarness:
    def __init__(self, workspace_dir, max_iterations=15, max_cost_usd=2.0):
        self.workspace_dir = Path(workspace_dir)
        self.max_iterations = max_iterations
        self.max_cost_usd = max_cost_usd
        self.current_iteration = 0
        self.running_cost = 0.0
        self.repair_log = self.workspace_dir / "ai-ops" / "repair-log.jsonl"

    # 1. Enforce Bounded Execution (Circuit Breakers)
    def check_guardrails(self, token_usage):
        self.current_iteration += 1
        self.running_cost += (
            token_usage["prompt_tokens"] * 0.000015
            + token_usage["completion_tokens"] * 0.00006
        )

        if self.current_iteration >= self.max_iterations:
            print("ERROR: Maximum iteration count exceeded. Circuit breaker triggered.")
            sys.exit(1)
        if self.running_cost >= self.max_cost_usd:
            print(
                f"ERROR: Maximum cost budget (${self.max_cost_usd}) exceeded. Circuit breaker triggered."
            )
            sys.exit(1)

    # 2. Tool Sandboxing (Isolated Docker Execution)
    def execute_terminal_command(self, command):
        print(f"Executing command in sandbox: {command}")
        docker_cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{self.workspace_dir}:/workspace",
            "-w",
            "/workspace",
            "node:22-slim",  # Or python:3.12-slim, etc.
            "bash",
            "-c",
            command,
        ]
        result = subprocess.run(docker_cmd, capture_output=True, text=True)
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    # 3. Deterministic Verification Gate
    def verify_agent_work(self):
        print("Running deterministic verification script...")
        res = self.execute_terminal_command("npm run test")
        if res["exit_code"] != 0:
            print("VERIFICATION FAILED: Agent's code failed local test suite.")
            self.record_repair_candidate(
                failure=res,
                suggested_artifact="tests or README troubleshooting note",
                rationale="Make this failure shape executable or discoverable before the next run.",
            )
            return False
        print("VERIFICATION PASSED: Sandbox tests completed successfully.")
        return True

    # 4. Failure-to-Artifact Repair Loop
    def record_repair_candidate(self, failure, suggested_artifact, rationale):
        """Persist what should change outside the prompt after a failure.

        Examples: add a regression test, improve CLI error output, write a
        skill/rules note, tighten a tool schema, or create a CI gate. A human
        should review and merge the artifact before the next autonomous run.
        """
        self.repair_log.parent.mkdir(parents=True, exist_ok=True)
        event = {
            "iteration": self.current_iteration,
            "failure": failure,
            "suggested_artifact": suggested_artifact,
            "rationale": rationale,
        }
        with self.repair_log.open("a") as f:
            f.write(json.dumps(event) + "\n")
        print(f"Repair candidate recorded at {self.repair_log}")

    def run_agent_loop(self):
        """Coordinate the host's agent loop inside the sandboxed environment."""
        raise NotImplementedError("Wire to the host workspace's agent driver")
