#!/usr/bin/env python3
"""Cursor adapter for the shared destructive-bash hook test suite."""
from __future__ import annotations

import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "hooks"))

from destructive_bash_test_suite import run_suite


if __name__ == "__main__":
    hook = pathlib.Path(__file__).resolve().with_name("block-destructive-bash.py")
    raise SystemExit(run_suite(hook, ".cursor"))
