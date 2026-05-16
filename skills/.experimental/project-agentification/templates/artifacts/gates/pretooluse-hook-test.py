#!/usr/bin/env python3
"""TEMPLATE — PreToolUse hook test fixture.

Prescribed by gates scaffold H5 (deny-list hook ships with its negative-case
test fixture as one scaffold artifact, not two). Runs the hook's
`check_command` against a fixture table covering:

  - Negatives (allow): commands the hook MUST NOT block.
  - Originals (block): commands the hook has always blocked.
  - Variant matrix (block): forms a regex deny-list would silently allow:
      * Split short flags (`-r -f` vs `-rf`).
      * Long-form aliases (`--recursive`, `--force`).
      * `=` forms (`--force-with-lease=ref`).
      * `--` option terminator (`rm -rf -- /etc`).
      * Transparent wrappers (`sudo`, `time`, `env`, `command`).
      * Env-var prefixes (`FOO=bar cmd …`).
      * Compound statements (`cd /tmp && rm -rf /etc`).
      * Refspec forms for git (`HEAD:main`, `+main`, `+HEAD:main`).
      * Quoted paths.

Add a new fixture row when a new bypass is observed in
`docs/agent-failures.md`. CI runs this file on every PR.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys


HERE = pathlib.Path(__file__).resolve().parent
HOOK_PATH = HERE / "<hook-filename>.py"  # FILL: e.g., block-destructive-bash.py


def _load_hook_module():
    spec = importlib.util.spec_from_file_location("hook_under_test", HOOK_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# CASES: (command, expect_blocked, label)
#
# Required matrix per gates scaffold H5. Coverage rules (each MUST have at
# least one positive row in the table below — additions to entry 7 of any
# repo's failure log expanded this list in round 2):
#   1. Flag forms: single short flag (`-rf`), split short flags (`-r -f`),
#      long-form alias (`--recursive`), `=` form where applicable
#      (`--force-with-lease=ref`), `--` option terminator (`rm -rf -- /etc`).
#   2. Path traversal: target with `..` segments that resolve to a protected
#      dir (`rm -rf /tmp/../etc`).
#   3. Shell variable expansion: `$VAR`, `${VAR}`, both with and without
#      trailing path components (`rm -rf ${HOME}/Documents`).
#   4. Command substitution: `$(...)`, backticks `` `...` ``, process
#      substitution `<(...)`, `>(...)`, and nested forms (`$(echo $(rm))`).
#   5. Multi-line commands: real newlines as command separators
#      (`echo ok\nrm -rf /etc`).
#   6. Transparent wrappers: bare wrapper (`sudo rm`), wrapper with flag
#      value (`sudo -u root rm`), `=` form (`sudo --user=root rm`), and
#      multiple value flags (`sudo -g wheel -u root rm`).
#   7. Env-var prefixes: single (`FOO=bar cmd`), multiple (`FOO=1 BAR=2 cmd`),
#      via `env` builtin (`env FOO=bar cmd`).
#   8. Compound statements: dangerous command in the second pipeline segment
#      (`safe-cmd && dangerous`), with each pipeline separator (`;`, `&&`,
#      `||`, `|`, `&`).
#   9. Quoted paths: dangerous target quoted (`rm -rf "/etc"`).
#   10. Tool-level global options with separate-token values
#       (`git --work-tree /path push -f origin main`).
#   11. Negatives: at least one variant of each form that should be ALLOWED
#       (`git push -f origin feature-branch`, `rm -rf /tmp/safe`, etc.).
# ---------------------------------------------------------------------------

CASES = [
    # ----- Negatives: must remain allowed -----
    # FILL from your forbidden-action table: for every forbidden form, write
    # at least one negative case proving the hook doesn't over-block.
    ("ls", False, "ls"),
    # ("git push origin feature", False, "push to non-protected"),

    # ----- Originals: must continue to block -----
    # FILL: every case the regex version (if any) caught. These prevent
    # regression when you tighten the predicate.
    # ("rm -rf /etc", True, "rm -rf /etc"),

    # ----- Variant matrix: must block -----
    # FILL: for every flag in your deny-list, write rows for each variant
    # form (see header). Each row should pair (form, label) so the CI
    # failure message points at the specific bypass.
    # ("rm -r -f /etc", True, "split -r -f"),
    # ("rm --recursive --force /etc", True, "long-form flags"),
    # ("rm -rf -- /etc", True, "-- terminator"),

    # ----- Pipelines / compound statements -----
    # ("cd /tmp && rm -rf /etc", True, "compound: && rm"),

    # ----- Transparent wrappers -----
    # ("sudo rm -rf /etc", True, "sudo rm"),
    # ("FOO=bar rm -rf /etc", True, "env-var prefix"),
]


def run_unit_tests(module):
    failures = []
    for cmd, expected_blocked, label in CASES:
        result = module.check_command(cmd)
        blocked = result is not None
        if blocked != expected_blocked:
            failures.append(
                {
                    "label": label,
                    "cmd": cmd,
                    "expected_blocked": expected_blocked,
                    "actual_blocked": blocked,
                    "violation": result,
                }
            )
    return failures


def run_subprocess_smoke():
    """End-to-end: invoke the hook script with a JSON payload on stdin."""
    payload_block = json.dumps(
        {"tool_name": "Bash", "tool_input": {"command": "<command-that-must-block>"}}
    )  # FILL with a concrete blocking command.
    payload_allow = json.dumps(
        {"tool_name": "Bash", "tool_input": {"command": "ls -la"}}
    )
    payload_nonbash = json.dumps(
        {"tool_name": "Read", "tool_input": {"file_path": "/etc/passwd"}}
    )

    failures = []
    proc = subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=payload_block,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if proc.returncode != 2:
        failures.append(f"block payload: expected exit 2, got {proc.returncode}")

    proc = subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=payload_allow,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if proc.returncode != 0:
        failures.append(f"allow payload: expected exit 0, got {proc.returncode}")

    proc = subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=payload_nonbash,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if proc.returncode != 0:
        failures.append(f"non-Bash payload: expected exit 0, got {proc.returncode}")
    return failures


def main():
    module = _load_hook_module()
    unit_failures = run_unit_tests(module)
    smoke_failures = run_subprocess_smoke()

    if unit_failures:
        print(f"UNIT: {len(unit_failures)} failure(s)", file=sys.stderr)
        for f in unit_failures:
            print(
                f"  - {f['label']}: cmd={f['cmd']!r} "
                f"expected_blocked={f['expected_blocked']} "
                f"actual_blocked={f['actual_blocked']} "
                f"violation={f['violation']!r}",
                file=sys.stderr,
            )
    if smoke_failures:
        print(f"SMOKE: {len(smoke_failures)} failure(s)", file=sys.stderr)
        for f in smoke_failures:
            print(f"  - {f}", file=sys.stderr)

    total = len(unit_failures) + len(smoke_failures)
    if total > 0:
        print(f"\nhook tests: {total} failure(s)", file=sys.stderr)
        return 1

    print(
        f"hook tests: {len(CASES)} unit cases + 3 subprocess smokes passed."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
