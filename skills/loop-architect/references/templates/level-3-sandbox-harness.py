"""Level 3 Sandbox Harness template.

Use for action-executing agents that run shell commands, write files, or
otherwise mutate system state. Enforces deterministic container execution,
iteration caps, and cost circuit-breakers around an inner agent loop.

CI parses this with `python3 -m py_compile`; the script does NOT execute
imports or shell commands at import time. The skill copies this file into
the host workspace's `ai-ops/` directory when a Level 3 scaffold is
selected.
"""
import subprocess
import sys


class AgentSandboxHarness:
    def __init__(self, workspace_dir, max_iterations=15, max_cost_usd=2.0):
        self.workspace_dir = workspace_dir
        self.max_iterations = max_iterations
        self.max_cost_usd = max_cost_usd
        self.current_iteration = 0
        self.running_cost = 0.0

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
            return False
        print("VERIFICATION PASSED: Sandbox tests completed successfully.")
        return True

    def run_agent_loop(self):
        """Coordinate the host's agent loop inside the sandboxed environment."""
        raise NotImplementedError("Wire to the host workspace's agent driver")
