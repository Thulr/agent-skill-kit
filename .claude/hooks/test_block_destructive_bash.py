#!/usr/bin/env python3
"""Test suite for block-destructive-bash.py.

Runs the hook's `check_command` against a fixture table covering:
  - Originals (the patterns the hook has always blocked).
  - Negative cases (commands that must continue to be allowed).
  - Bypasses surfaced by the Codex PR-review bot in PR #5:
      * Refspec force-push (HEAD:main, +main, +HEAD:main).
      * `--force-with-lease=main` `=` form.
      * `rm -- /etc` option terminator.
      * `rm -r -f /etc` split-flag form.
      * `rm --recursive --force /etc` long-form flags.
  - Pipeline / compound statements (`cd /tmp && rm -rf /etc`).
  - Transparent wrappers (`sudo`, `time`, `env`).
  - Quoted paths.

Wired into `just check` and CI (`.github/workflows/ci.yml`). Add a new
fixture row when a new bypass is observed in the failure log
(`docs/agent-failures.md`).
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys


HERE = pathlib.Path(__file__).resolve().parent
HOOK_PATH = HERE / "block-destructive-bash.py"


def _load_hook_module():
    spec = importlib.util.spec_from_file_location("block_destructive_bash", HOOK_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# (command, expect_blocked, label)
CASES = [
    # ----- Negatives: must remain allowed -----
    ("ls", False, "ls"),
    ("rm file.txt", False, "rm without -r"),
    ("rm -f file.txt", False, "rm -f without -r"),
    ("rm -rf /tmp/build", False, "rm -rf /tmp/build"),
    ("rm -rf ./node_modules", False, "rm -rf ./node_modules"),
    ("rm -rf node_modules", False, "rm -rf bare relative dir"),
    ('rm -rf "/tmp/safe"', False, "quoted /tmp/safe"),
    ("git status", False, "git status"),
    ("git push origin feature", False, "push to feature"),
    ("git push -f origin feature", False, "force-push to feature is allowed"),
    ("git push origin +feature", False, "+feature is allowed"),
    ("echo hi | grep hi", False, "safe pipeline"),
    ("cd /tmp && ls", False, "compound with safe ops"),
    ("git fetch origin main", False, "fetch is not push"),

    # ----- Originals: must continue to block -----
    ("rm -rf /", True, "rm -rf /"),
    ("rm -rf /etc", True, "rm -rf /etc"),
    ("rm -rf /Users", True, "rm -rf /Users"),
    ("rm -rf /System", True, "rm -rf /System"),
    ("rm -rf ~", True, "rm -rf ~"),
    ("rm -rf $HOME", True, "rm -rf $HOME"),
    ("git push --force origin main", True, "force-push main"),
    ("git push -f main", True, "-f main"),
    ("git push --force-with-lease origin main", True, "force-with-lease main"),
    ("git push --force origin master", True, "force-push master"),
    ("git branch -D main", True, "branch -D main"),
    ("git branch -D master", True, "branch -D master"),

    # ----- Codex bypasses: PR #5 review comments -----
    ("git push -f origin HEAD:main", True, "HEAD:main refspec"),
    ("git push origin +main", True, "+main refspec (no -f)"),
    ("git push origin +HEAD:main", True, "+HEAD:main refspec"),
    ("git push origin +master", True, "+master refspec"),
    ("git push origin +refs/heads/main", True, "+refs/heads/main refspec"),
    ("git push --force-with-lease=main origin main", True, "lease=main form"),
    ("git push --force-if-includes origin main", True, "force-if-includes"),
    ("rm -rf -- /", True, "rm -- /"),
    ("rm -rf -- /etc", True, "rm -- /etc"),
    ("rm -r -f /etc", True, "split -r -f"),
    ("rm -f -r /etc", True, "split -f -r"),
    ("rm --recursive --force /etc", True, "long-form flags"),
    ("rm --recursive /etc", True, "long --recursive alone"),
    ("rm -r /etc", True, "-r alone (no -f) still recurses"),

    # ----- Pipelines / compound statements -----
    ("cd /tmp && rm -rf /etc", True, "compound: && rm"),
    ("safe-cmd; git push -f origin main", True, "compound: ; push"),
    ("rm -rf /tmp/ok || rm -rf /etc", True, "compound: || rm"),
    ("git push -f origin main | tee log", True, "pipe to tee"),
    ("ls & rm -rf /etc", True, "background & rm"),

    # ----- Transparent wrappers -----
    ("sudo rm -rf /etc", True, "sudo rm"),
    ("sudo -- rm -rf /etc", True, "sudo -- rm"),
    ("time rm -rf /etc", True, "time rm"),
    ("env FOO=bar rm -rf /etc", True, "env FOO=bar rm"),
    ("FOO=bar rm -rf /etc", True, "FOO=bar prefix"),
    ("FOO=1 BAR=2 rm -rf /etc", True, "multiple env vars"),
    ("command rm -rf /etc", True, "command rm (bypasses aliases)"),

    # ----- git wrapper options -----
    ("git -C /tmp/repo push -f origin main", True, "git -C push"),
    ("git -c user.email=x push -f origin main", True, "git -c push"),

    # ----- Home subdirectories (preserve original behavior) -----
    ("rm -rf ~/Downloads", True, "rm under ~"),
    ("rm -rf $HOME/Documents", True, "rm under $HOME"),

    # ----- Round-2 bypasses (Codex bot, PR #5; failure-log entry 8) -----

    # Wrapper option values: sudo -u user, doas -u user, etc.
    ("sudo -u root rm -rf /etc", True, "sudo -u root rm"),
    ("sudo --user=root rm -rf /etc", True, "sudo --user= rm"),
    ("sudo --user root rm -rf /etc", True, "sudo --user separate-value rm"),
    ("doas -u root git push -f origin main", True, "doas -u user push"),
    ("sudo -g wheel -u root rm -rf /etc", True, "sudo multiple value-flags"),

    # Git global options with separate values.
    ("git --work-tree /workspace push -f origin main", True, "git --work-tree push"),
    ("git --git-dir /repo.git push -f origin main", True, "git --git-dir push"),
    ("git --work-tree=/workspace push -f origin main", True, "git --work-tree= push"),
    ("git --namespace ns push -f origin main", True, "git --namespace push"),

    # Path traversal.
    ("rm -rf /tmp/../etc", True, "rm path traversal /tmp/../etc"),
    ("rm -rf /var/../etc", True, "rm path traversal /var/../etc"),
    ("rm -rf /tmp/safe/../../etc", True, "rm path traversal two levels"),
    ("rm -rf /etc/.", True, "rm with /etc/. (canonicalizes)"),
    ("rm -rf /etc//foo", True, "rm with double-slash"),

    # ${HOME} brace expansion.
    ("rm -rf ${HOME}/Documents", True, "rm under ${HOME}"),
    ("rm -rf ${HOME}", True, "rm of ${HOME}"),

    # Real newlines as command separators.
    ("echo ok\nrm -rf /etc", True, "newline-separated rm"),
    ("cd /tmp\ngit push -f origin main", True, "newline-separated push"),
    ("ls\nrm -rf /etc\necho done", True, "newline in middle"),

    # Command substitution.
    ("echo $(rm -rf /etc)", True, "rm inside $()"),
    ("echo `rm -rf /etc`", True, "rm inside backticks"),
    ("diff <(rm -rf /etc) /dev/null", True, "rm inside <()"),
    ("echo $(echo $(rm -rf /etc))", True, "rm inside nested $()"),
    ("echo $(git push -f origin main)", True, "push inside $()"),

    # ----- Round-2 negatives: must remain allowed -----
    ("rm -rf /tmp/../tmp/build", False, "traversal stays in /tmp"),
    ("rm -rf ${HOME}/no-such-thing-here", True, "rm under ${HOME} still blocked"),
    ("git --work-tree /workspace push origin feature", False, "--work-tree to feature"),
    ("sudo -u root ls /etc", False, "sudo -u root ls (non-rm)"),
    ("echo $(ls)", False, "ls inside $()"),
    ("echo ok\nls", False, "newline-separated ls"),
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
        {"tool_name": "Bash", "tool_input": {"command": "rm -rf /etc"}}
    )
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
        print(
            f"\nblock-destructive-bash tests: {total} failure(s)",
            file=sys.stderr,
        )
        return 1

    print(
        f"block-destructive-bash tests: "
        f"{len(CASES)} unit cases + 3 subprocess smokes passed."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
