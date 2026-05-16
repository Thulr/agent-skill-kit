#!/usr/bin/env python3
"""PreToolUse hook for Claude Code: blocks destructive Bash actions.

Reads the tool-use payload from stdin. Exits 2 to block with a message
the model will see; exits 0 to allow. Any other non-zero exit is treated
as a hook error.

Blocked patterns (see AGENTS.md §Forbidden actions):
  - git push --force / -f / --force-with-lease to main or master
  - git branch -D main / master
  - rm -rf / and rm -rf of protected dirs
  - rm -rf ~ / rm -rf $HOME

If a blocked command is genuinely intended, run it manually in a terminal
outside the agent session.
"""

import json
import re
import sys

# Each rule: (compiled regex, human-readable label).
# Patterns intentionally lenient on whitespace and ordering of flags.
# Note: \b does not match before a leading '-' (both '-' and the preceding
# space are non-word chars), so flags use (?<!\S) — "preceded by start or
# whitespace" — as the left boundary instead.
RULES = [
    (
        re.compile(
            r"\bgit\s+push\b"
            r"(?=.*(?<!\S)(?:--force|--force-with-lease|-f)(?=\s|$))"
            r"(?=.*(?<!\S)(?:origin\s+)?(?:main|master)(?=\s|$))"
        ),
        "force-push to main/master",
    ),
    (
        re.compile(r"\bgit\s+branch\s+-D\s+(?:main|master)\b"),
        "force-delete of main/master branch",
    ),
    (
        re.compile(r"\brm\s+-[rRfF]*[rR][rRfF]*\s+/(?:\s|$)"),
        "rm -rf /",
    ),
    (
        re.compile(
            r"\brm\s+-[rRfF]*[rR][rRfF]*\s+/(?:bin|boot|etc|lib|opt|sbin|sys|"
            r"proc|root|run|srv|usr|var|home|System|Library|Applications|Users)\b"
        ),
        "rm -rf of a protected system directory",
    ),
    (
        re.compile(r"\brm\s+-[rRfF]*[rR][rRfF]*\s+(?:~|\$HOME)(?=/|\s|$)"),
        "rm -rf ~ / $HOME",
    ),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        # If we can't parse the payload, don't block — log and exit clean.
        print("block-destructive-bash: could not parse hook payload", file=sys.stderr)
        return 0

    if payload.get("tool_name") != "Bash":
        return 0

    command = payload.get("tool_input", {}).get("command", "")
    if not isinstance(command, str) or not command.strip():
        return 0

    for regex, label in RULES:
        if regex.search(command):
            print(
                f"BLOCKED by PreToolUse hook: command matches the {label!r} guard.\n"
                f"Command: {command}\n"
                f"See AGENTS.md §Forbidden actions. If this is genuinely intended, "
                f"run it manually in a terminal outside the agent session.",
                file=sys.stderr,
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
