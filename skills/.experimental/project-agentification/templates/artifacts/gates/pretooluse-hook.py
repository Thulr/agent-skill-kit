#!/usr/bin/env python3
"""TEMPLATE — PreToolUse hook (Claude Code).

Prescribed by gates scaffold H1 + H6: argv parsing (shlex-tokenized) over
regex-on-string. Reads the tool-use payload from stdin. Exits 2 to block
with a message the model will see; exits 0 to allow.

Splits the command pipeline on `;`, `&&`, `||`, `|`, `&`, then walks each
segment's argv after stripping env-var prefixes and transparent wrappers
(`sudo`, `time`, `env`, `command`, `git -C path`). This catches forms a
regex-on-string approach silently allows: refspec force-pushes, `--` option
terminators, split short flags, long-form aliases. See
[`docs/agent-failures.md` entry tracking your initial scaffold] for the
bypass family that motivated argv parsing.

W3: prose at ~70%, hooks at 100%. Anything safety-relevant lives here, not
in AGENTS.md alone.

Customization:
- Fill the FORBIDDEN_ACTIONS section with patterns derived from your
  three-tier table (gates scaffold H1). Each pattern must trace to a
  failure-log row or a named threat — no boilerplate.
- Ships with a companion test file at the same path with `test_` prefix.
  Hook + tests are one scaffold artifact (gates scaffold H5).
"""

import json
import shlex
import sys

# ---------------------------------------------------------------------------
# FORBIDDEN_ACTIONS — fill from the three-tier table.
# Each entry is a tuple of (predicate_fn, human-readable label, failure-ref).
# `predicate_fn` takes a tokenized argv list (after wrapper-unwrapping) and
# returns a violation label (str) or None.
# ---------------------------------------------------------------------------

PROTECTED_GIT_BRANCHES = frozenset(["main", "master"])  # extend per repo

PROTECTED_TOP_DIRS = frozenset(
    [
        "/bin", "/boot", "/etc", "/lib", "/opt", "/sbin", "/sys",
        "/proc", "/root", "/run", "/srv", "/usr", "/var", "/home",
        "/System", "/Library", "/Applications", "/Users",
    ]
)

TRANSPARENT_WRAPPERS = frozenset(
    ["sudo", "doas", "command", "exec", "time", "nice", "ionice", "env"]
)

PIPELINE_SEPARATORS = frozenset([";", "&", "&&", "|", "||"])


def split_pipeline(command):
    """Tokenize and split a command on shell pipeline operators.

    Returns a list of token lists, one per pipeline segment. Quoting is
    handled by shlex; `punctuation_chars=True` makes `;`, `&`, `|` emit
    as their own tokens.
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
    if "=" not in token:
        return False
    name, _, _ = token.partition("=")
    if not name:
        return False
    if not (name[0].isalpha() or name[0] == "_"):
        return False
    return all(c.isalnum() or c == "_" for c in name)


def resolve_executable(argv):
    """Walk past env-var prefixes and transparent wrappers; return (cmd, rest)."""
    i = 0
    while i < len(argv):
        a = argv[i]
        if _is_env_assignment(a):
            i += 1
            continue
        if a in TRANSPARENT_WRAPPERS:
            i += 1
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


# ---------------------------------------------------------------------------
# Example predicate: rm of protected paths. KEEP if your forbidden-action
# table includes `rm -r` of protected paths; DELETE otherwise.
# ---------------------------------------------------------------------------

def _first_path_component(path):
    if not path.startswith("/"):
        return path
    rest = path[1:]
    head, _, _ = rest.partition("/")
    return "/" + head


def check_rm(argv):
    """Block recursive rm of /, protected top-level dirs, ~, $HOME, or anywhere
    under them. Handles `--`, split flags (`-r -f`), long-form (`--recursive`)."""
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


# ---------------------------------------------------------------------------
# Example predicate: git push --force / +refspec to protected branch.
# KEEP if your forbidden-action table includes force-push protection;
# DELETE otherwise.
# ---------------------------------------------------------------------------

def _is_force_push_flag(arg):
    if arg in ("-f", "--force"):
        return True
    if arg.startswith("--force-with-lease") or arg.startswith("--force-if-includes"):
        return True
    return False


def _ref_targets_protected_branch(refspec):
    plus = refspec.startswith("+")
    without_plus = refspec[1:] if plus else refspec
    dst = without_plus.split(":")[-1]
    final = dst.rsplit("/", 1)[-1]
    return (final in PROTECTED_GIT_BRANCHES, plus)


def check_git_push(push_argv):
    has_force_flag = False
    refspec_tokens = []
    for a in push_argv[1:]:
        if _is_force_push_flag(a):
            has_force_flag = True
        elif a.startswith("-"):
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
    if "-D" not in branch_argv:
        return None
    targets = [a for a in branch_argv[1:] if not a.startswith("-")]
    for t in targets:
        if t in PROTECTED_GIT_BRANCHES:
            return f"force-delete of {t} branch"
    return None


def check_git(git_rest):
    """Skip `git`-level options (`-C path`, `-c k=v`) and dispatch."""
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


# ---------------------------------------------------------------------------
# Top-level dispatch. Extend the if-chain below with predicates from your
# three-tier table. Each predicate returns (violation_label or None).
# ---------------------------------------------------------------------------

def check_segment(tokens):
    if not tokens:
        return None
    cmd, rest = resolve_executable(tokens)
    if cmd is None:
        return None
    if cmd == "rm":
        return check_rm(rest)
    if cmd == "git":
        return check_git(rest)
    # ADD predicates for additional forbidden actions here.
    return None


def check_command(command):
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
