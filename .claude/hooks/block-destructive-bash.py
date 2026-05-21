#!/usr/bin/env python3
"""Claude Code PreToolUse adapter for the shared destructive Bash policy."""

from __future__ import annotations

import importlib.util
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / "scripts" / "hooks" / "destructive_bash_policy.py"


def _load_policy_module():
    spec = importlib.util.spec_from_file_location(
        "destructive_bash_policy", POLICY_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_policy = _load_policy_module()
check_command = _policy.check_command
main = _policy.main


if __name__ == "__main__":
    sys.exit(main())
