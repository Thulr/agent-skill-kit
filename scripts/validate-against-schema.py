#!/usr/bin/env python3
"""Validate a JSON file against a JSON Schema.

Usage: validate-against-schema.py <schema_path> <data_path>

Exits 0 on success, 1 on schema violation (with errors on stderr), 2 on
usage/dependency errors.

Used by every skill's evals/run-static-checks.sh so the canonical shape
of skill.json and trigger-evals.json lives in one place under schemas/
(AGENTS.md Rule 2: single source of truth, was duplicated 4x before).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print(
        "error: jsonschema not installed. In CI: apt-get install -y python3-jsonschema. "
        "Locally: pip install jsonschema",
        file=sys.stderr,
    )
    sys.exit(2)


def main() -> int:
    if len(sys.argv) != 3:
        print(
            f"usage: {Path(sys.argv[0]).name} <schema_path> <data_path>",
            file=sys.stderr,
        )
        return 2

    schema_path, data_path = Path(sys.argv[1]), Path(sys.argv[2])

    try:
        schema = json.loads(schema_path.read_text())
    except (OSError, json.JSONDecodeError) as e:
        print(f"{schema_path}: cannot load schema ({e})", file=sys.stderr)
        return 2

    try:
        data = json.loads(data_path.read_text())
    except json.JSONDecodeError as e:
        print(f"{data_path}: invalid JSON ({e})", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"{data_path}: cannot read ({e})", file=sys.stderr)
        return 2

    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(
        validator.iter_errors(data),
        key=lambda err: list(err.absolute_path),
    )
    if errors:
        for err in errors:
            location = "/".join(str(p) for p in err.absolute_path) or "<root>"
            print(f"{data_path}: {location}: {err.message}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
