#!/usr/bin/env python3
"""PreToolUse hook for Claude Code: blocks destructive Bash actions.

Reads the tool-use payload from stdin. Exits 2 to block with a message
the model will see; exits 0 to allow. Any other non-zero exit is treated
as a hook error.

Parses Bash commands via shlex (POSIX mode + punctuation_chars), splits
the pipeline on shell operators (`;`, `&&`, `||`, `|`, `&`), and inspects
each segment argv-by-argv. This catches forms a regex-on-string approach
silently allows:
  - Refspec force-pushes: `git push -f origin HEAD:main`
  - `+`-refspec force-updates: `git push origin +main` (no force flag)
  - `--force-with-lease=ref` / `--force-if-includes` long forms.
  - `rm -- /etc` (option terminator) and `rm -r -f /etc` (split flags).
  - `rm --recursive --force /etc` (long-form flags).
  - Wrapper prefixes: `sudo rm -rf /etc`, `time rm -rf /etc`.
  - Compound statements: `cd /tmp && rm -rf /etc`.

Blocked patterns (see AGENTS.md §Forbidden actions):
  - `git push` with `--force` / `-f` / `--force-with-lease[=…]` /
    `--force-if-includes`, OR a `+refspec`, targeting `main` / `master`.
  - `git branch -D main` / `git branch -D master`.
  - `rm -r` (or `-R` / `--recursive`) of `/`, protected system dirs,
    `~` / `$HOME`, or anything under them. `-f` not required — `-r`
    alone still recurses.

If a blocked command is genuinely intended, run it manually in a terminal
outside the agent session.
"""

import json
import shlex
import sys

PROTECTED_GIT_BRANCHES = frozenset(["main", "master"])

# Top-level directory components that should never be the target of `rm -r`.
# The "/" entry is for `rm -r /` itself (the root). Any path whose first
# component matches one of these is blocked.
PROTECTED_TOP_DIRS = frozenset(
    [
        "/bin", "/boot", "/etc", "/lib", "/opt", "/sbin", "/sys",
        "/proc", "/root", "/run", "/srv", "/usr", "/var", "/home",
        "/System", "/Library", "/Applications", "/Users",
    ]
)

# Wrappers that are transparent to the actual command (e.g., `sudo rm -rf /`
# is still a destructive `rm`). After matching one of these, we skip its
# own flags (including `--`) and re-resolve the executable.
TRANSPARENT_WRAPPERS = frozenset(
    ["sudo", "doas", "command", "exec", "time", "nice", "ionice", "env"]
)

PIPELINE_SEPARATORS = frozenset([";", "&", "&&", "|", "||"])


def split_pipeline(command):
    """Tokenize and split a command on shell pipeline operators.

    Returns a list of token lists, one per pipeline segment. Quoting is
    handled by shlex; `punctuation_chars=True` makes `;`, `&`, `|` emit
    as their own tokens (runs like `&&` and `||` come out as a single
    token).

    On a shlex parse error (unbalanced quotes etc.), falls back to a
    whitespace split of the whole command so we still attempt detection
    instead of failing open.
    """
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        try:
            return [shlex.split(command, posix=True)]
        except ValueError:
            return [command.split()]

    segments = []
    current = []
    for tok in tokens:
        if tok in PIPELINE_SEPARATORS:
            if current:
                segments.append(current)
                current = []
        else:
            current.append(tok)
    if current:
        segments.append(current)
    return segments


def _is_env_assignment(token):
    """True if `token` looks like NAME=value at the start of a command line."""
    if "=" not in token:
        return False
    name, _, _ = token.partition("=")
    if not name:
        return False
    if not (name[0].isalpha() or name[0] == "_"):
        return False
    return all(c.isalnum() or c == "_" for c in name)


def resolve_executable(argv):
    """Walk past env-var prefixes and transparent wrappers; return (cmd, rest).

    Returns (None, []) if `argv` is exhausted. We don't try to be exhaustive
    about wrapper flag handling — if we mis-parse a wrapper-with-flag form
    (e.g., `sudo -u user rm -rf /`), the worst case is a false negative
    (we miss the block). The hook is one layer of defense; W10 says hooks
    plus sandbox isolation together close the gap.
    """
    i = 0
    while i < len(argv):
        a = argv[i]
        if _is_env_assignment(a):
            i += 1
            continue
        if a in TRANSPARENT_WRAPPERS:
            i += 1
            # Skip wrapper-owned flags. `--` ends the wrapper's option list.
            while i < len(argv) and argv[i].startswith("-"):
                if argv[i] == "--":
                    i += 1
                    break
                i += 1
            continue
        break
    if i >= len(argv):
        return None, []
    return argv[i], argv[i + 1 :]


def _first_path_component(path):
    """Return the leading absolute path component (e.g., `/etc/foo` -> `/etc`).

    Returns `path` unchanged if it doesn't start with `/`.
    """
    if not path.startswith("/"):
        return path
    rest = path[1:]
    head, _, _ = rest.partition("/")
    return "/" + head


def check_rm(argv):
    """Return a violation label if this `rm` invocation is dangerous, else None.

    Blocks when the command is recursive (`-r` / `-R` / `--recursive`,
    whether or not `-f` / `--force` is also set) and targets `/`,
    a protected top-level system directory, or `~` / `$HOME` (or anything
    under them). `-r` alone still recurses; `-f` only suppresses prompts.
    """
    recursive = False
    targets = []
    after_double_dash = False

    for arg in argv:
        if after_double_dash:
            targets.append(arg)
            continue
        if arg == "--":
            after_double_dash = True
            continue
        if arg.startswith("--"):
            if arg == "--recursive":
                recursive = True
            # `--force`, other long options: do not affect recursion.
            continue
        if arg.startswith("-") and len(arg) >= 2:
            for c in arg[1:]:
                if c == "r" or c == "R":
                    recursive = True
            continue
        targets.append(arg)

    if not recursive:
        return None

    for target in targets:
        if target in ("~", "$HOME"):
            return f"rm -r of {target}"
        if target.startswith("~/") or target.startswith("$HOME/"):
            return f"rm -r under $HOME ({target!r})"

        if target == "/" or target.rstrip("/") == "":
            return "rm -r of /"

        if target.startswith("/"):
            head = _first_path_component(target)
            if head in PROTECTED_TOP_DIRS:
                return f"rm -r under protected dir {head}"

    return None


def _is_force_push_flag(arg):
    """Recognize every form of `git push` force flag."""
    if arg in ("-f", "--force"):
        return True
    # `--force-with-lease`, `--force-with-lease=ref`, `--force-if-includes`, ...
    if arg.startswith("--force-with-lease") or arg.startswith("--force-if-includes"):
        return True
    return False


def _ref_targets_protected_branch(refspec):
    """True if `refspec` (a non-flag `git push` arg) names main/master.

    Handles plain `main`, `+main`, `HEAD:main`, `+refs/heads/main`, etc.
    Returns (matched, plus_prefixed) — plus_prefixed indicates a
    non-fast-forward push regardless of explicit force flag.
    """
    plus = refspec.startswith("+")
    without_plus = refspec[1:] if plus else refspec
    dst = without_plus.split(":")[-1]
    final = dst.rsplit("/", 1)[-1]
    return (final in PROTECTED_GIT_BRANCHES, plus)


def check_git_push(push_argv):
    """Inspect a `git push ...` argv (with leading `push` token).

    Returns a violation label if any non-flag arg names a protected branch
    AND either a force flag is set or the refspec is `+`-prefixed.
    """
    has_force_flag = False
    refspec_tokens = []

    for a in push_argv[1:]:
        if _is_force_push_flag(a):
            has_force_flag = True
        elif a.startswith("-"):
            # Unrelated flag; ignore.
            continue
        else:
            refspec_tokens.append(a)

    for tok in refspec_tokens:
        matched, plus = _ref_targets_protected_branch(tok)
        if not matched:
            continue
        if plus:
            return f"force-update of {tok} via +refspec"
        if has_force_flag:
            return f"force-push to {tok}"
    return None


def check_git_branch_force_delete(branch_argv):
    """Inspect a `git branch ...` argv. Block `-D main` / `-D master`."""
    if "-D" not in branch_argv:
        return None
    targets = [a for a in branch_argv[1:] if not a.startswith("-")]
    for t in targets:
        if t in PROTECTED_GIT_BRANCHES:
            return f"force-delete of {t} branch"
    return None


def check_git(git_rest):
    """Skip `git`-level options (e.g., `-C path`, `-c k=v`) and dispatch."""
    i = 0
    while i < len(git_rest):
        a = git_rest[i]
        if a in ("-C", "-c"):
            i += 2
            continue
        if a.startswith("-"):
            i += 1
            continue
        break
    sub = git_rest[i:]
    if not sub:
        return None
    if sub[0] == "push":
        return check_git_push(sub)
    if sub[0] == "branch":
        return check_git_branch_force_delete(sub)
    return None


def check_segment(tokens):
    """Check a single pipeline segment. Returns violation label or None."""
    if not tokens:
        return None
    cmd, rest = resolve_executable(tokens)
    if cmd is None:
        return None
    if cmd == "rm":
        return check_rm(rest)
    if cmd == "git":
        return check_git(rest)
    return None


def check_command(command):
    """Top-level: split into pipeline segments, check each. Returns label or None."""
    if not isinstance(command, str) or not command.strip():
        return None
    for segment in split_pipeline(command):
        violation = check_segment(segment)
        if violation:
            return violation
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("block-destructive-bash: could not parse hook payload", file=sys.stderr)
        return 0

    if payload.get("tool_name") != "Bash":
        return 0

    command = payload.get("tool_input", {}).get("command", "")
    violation = check_command(command)
    if violation is None:
        return 0

    print(
        f"BLOCKED by PreToolUse hook: command matches the {violation!r} guard.\n"
        f"Command: {command}\n"
        f"See AGENTS.md §Forbidden actions. If this is genuinely intended, "
        f"run it manually in a terminal outside the agent session.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
