#!/usr/bin/env python3
"""TEMPLATE — PreToolUse hook (Claude Code).

Prescribed by gates scaffold H1 + H6: argv parsing (shlex-tokenized) over
regex-on-string. Reads the tool-use payload from stdin. Exits 2 to block
with a message the model will see; exits 0 to allow.

Implementation shape — this template is hardened against the bypass family
logged in `docs/reflection-log/` (per-entry files dated to when each round
of bypasses was discovered; canonical examples in this repo are the
`2026-05-16-hook-*-bypasses-round{1,2,3}.md` entries). Categories covered:
  - Real newlines pre-processed into `;` outside quotes (multi-line
    commands count as compound statements).
  - Command substitutions (`$(...)`, backticks, `<(...)`, `>(...)`)
    extracted and recursively checked.
  - `shlex` with `punctuation_chars=True` tokenizes; pipeline splits on
    `;`, `&&`, `||`, `|`, `&`.
  - Wrapper unwrap: env-var prefixes (`FOO=bar cmd`) and transparent
    wrappers (`sudo`, `time`, `env`, `command`, `nice`, `ionice`, `doas`,
    `exec`). Wrapper flags with values (`sudo -u root cmd`) are consumed.
  - Wrapper flags whose VALUE is a command (`env -S "rm -rf /etc"`) are
    recursively inspected.
  - Shell launchers (`bash`, `sh`, `zsh`, ...) — `-c "cmd"`, `-c<cmd>`,
    combined-flag `-lc "cmd"`, long-form `--command="cmd"` — the command
    string value is recursively inspected.
  - For `rm`: `os.path.normpath` canonicalizes targets; protected dirs
    checked both for absolute paths AND for relative paths resolved
    against a simulated cwd tracked across `cd` segments in the pipeline.
    Relative targets with `..` escape are blocked even when cwd is unknown.
    `~`, `$HOME`, AND `${HOME}` are all recognized.
  - For `git`: global options with separate-token values (`-C`, `-c`,
    `--work-tree`, `--git-dir`, `--namespace`, `--super-prefix`,
    `--config-env`, `--exec-path`) consume the next token before
    subcommand dispatch.

Customization — fill from your three-tier table (gates scaffold H1):
- PROTECTED_GIT_BRANCHES — branches `git push --force` is blocked against.
- PROTECTED_TOP_DIRS — top-level dirs `rm -r` is blocked against.
- Add new predicates in the `check_segment` dispatch for additional
  forbidden actions named in your three-tier table. Every predicate must
  trace to a specific project-knowledge input — no boilerplate (W9).
- Ships with a companion test fixture (`pretooluse-hook-test.py`). Hook +
  tests are one scaffold artifact (gates scaffold H5). The test fixture's
  variant-matrix coverage rules are enumerated in `gates.md` scaffold H5.

W3: prose at ~70%, hooks at 100%. Anything safety-relevant lives here, not
in AGENTS.md alone.
"""

import json
import os
import shlex
import sys

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

SHELL_LAUNCHERS = frozenset(["sh", "bash", "zsh", "dash", "ksh", "ash", "fish"])

WRAPPER_VALUE_FLAGS = {
    "sudo": frozenset(
        [
            "-u", "-g", "-h", "-p", "-r", "-t", "-U", "-D", "-C", "-G",
            "--user", "--group", "--host", "--prompt", "--role",
            "--type", "--other-user", "--chdir", "--close-from",
            "--group-list",
        ]
    ),
    "doas": frozenset(["-u", "-C"]),
    "env": frozenset(["-u", "--unset", "-S", "--split-string"]),
    "nice": frozenset(["-n", "--adjustment"]),
    "ionice": frozenset(["-c", "-n", "-p", "-P", "-u"]),
}

# (wrapper, flag) pairs where the consumed value is a command string and must
# be recursively inspected (`env -S 'rm -rf /etc'`).
WRAPPER_COMMAND_VALUE_FLAGS = frozenset(
    [
        ("env", "-S"),
        ("env", "--split-string"),
    ]
)

GIT_VALUE_FLAGS = frozenset(
    [
        "-C", "-c",
        "--work-tree", "--git-dir", "--namespace", "--super-prefix",
        "--config-env", "--exec-path", "--list-cmds",
    ]
)

PIPELINE_SEPARATORS = frozenset([";", "&", "&&", "|", "||"])


def replace_unquoted_newlines(command):
    """Replace real newlines with `; ` outside of quoted strings."""
    out = []
    in_single = False
    in_double = False
    escape = False
    for c in command:
        if escape:
            out.append(c)
            escape = False
            continue
        if c == "\\":
            out.append(c)
            escape = True
            continue
        if c == "'" and not in_double:
            in_single = not in_single
            out.append(c)
        elif c == '"' and not in_single:
            in_double = not in_double
            out.append(c)
        elif (c == "\n" or c == "\r") and not in_single and not in_double:
            out.append(";")
            out.append(" ")
        else:
            out.append(c)
    return "".join(out)


def extract_command_substitutions(command):
    subs = []
    i = 0
    n = len(command)
    while i < n:
        c = command[i]
        if c in "$<>" and i + 1 < n and command[i + 1] == "(":
            depth = 1
            start = i + 2
            j = start
            while j < n:
                if command[j] == "(":
                    depth += 1
                elif command[j] == ")":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if depth == 0:
                subs.append(command[start:j])
                i = j + 1
                continue
        elif c == "`":
            j = command.find("`", i + 1)
            if j != -1:
                subs.append(command[i + 1 : j])
                i = j + 1
                continue
        i += 1
    return subs


def split_pipeline(command):
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


def _skip_wrapper_flags(argv, i, value_flags, wrapper_name, command_values):
    while i < len(argv) and argv[i].startswith("-"):
        if argv[i] == "--":
            i += 1
            break
        flag, sep, inline_value = argv[i].partition("=")
        i += 1
        inspect = (wrapper_name, flag) in WRAPPER_COMMAND_VALUE_FLAGS
        if flag in value_flags and sep != "=":
            if i < len(argv):
                if inspect:
                    command_values.append(argv[i])
                i += 1
        elif sep == "=" and inspect:
            command_values.append(inline_value)
    return i


def resolve_executable(argv):
    command_values = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if _is_env_assignment(a):
            i += 1
            continue
        if a in TRANSPARENT_WRAPPERS:
            value_flags = WRAPPER_VALUE_FLAGS.get(a, frozenset())
            wrapper_name = a
            i += 1
            i = _skip_wrapper_flags(argv, i, value_flags, wrapper_name, command_values)
            continue
        break
    if i >= len(argv):
        return None, [], command_values
    return argv[i], argv[i + 1 :], command_values


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


_HOME_PREFIXES = ("~/", "$HOME/", "${HOME}/")
_HOME_EXACT = frozenset(["~", "$HOME", "${HOME}"])


def check_rm(argv, cwd=None):
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
        if target in _HOME_EXACT:
            return f"rm -r of {target}"
        if any(target.startswith(p) for p in _HOME_PREFIXES):
            return f"rm -r under $HOME ({target!r})"
        if target == "/" or target.rstrip("/") == "":
            return "rm -r of /"
        if target.startswith("/"):
            normalized = os.path.normpath(target)
            if normalized == "/":
                return "rm -r of /"
            head = _first_path_component(normalized)
            if head in PROTECTED_TOP_DIRS:
                return f"rm -r under protected dir {head}"
        else:
            if cwd is not None:
                joined = os.path.normpath(os.path.join(cwd, target))
                if joined == "/":
                    return f"rm -r of / (relative target {target!r} from cwd={cwd})"
                if joined.startswith("/"):
                    head = _first_path_component(joined)
                    if head in PROTECTED_TOP_DIRS:
                        return f"rm -r under protected dir {head} (relative target {target!r} from cwd={cwd})"
            normalized_rel = os.path.normpath(target)
            if normalized_rel == ".." or normalized_rel.startswith("../"):
                return f"rm -r of cwd-escape path ({target!r})"

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
    i = 0
    while i < len(git_rest):
        a = git_rest[i]
        if not a.startswith("-"):
            break
        flag, sep, _value = a.partition("=")
        i += 1
        if flag in GIT_VALUE_FLAGS and sep != "=":
            if i < len(git_rest):
                i += 1
    sub = git_rest[i:]
    if not sub:
        return None
    if sub[0] == "push":
        return check_git_push(sub)
    if sub[0] == "branch":
        return check_git_branch_force_delete(sub)
    return None


def _extract_shell_c_payloads(rest):
    """Return any `-c <cmd>` / `-c<cmd>` / combined-flag command strings."""
    payloads = []
    i = 0
    while i < len(rest):
        a = rest[i]
        if a == "-c":
            if i + 1 < len(rest):
                payloads.append(rest[i + 1])
            i += 2
            continue
        if a.startswith("-c") and not a.startswith("--"):
            payloads.append(a[2:])
            i += 1
            continue
        if a.startswith("--command="):
            payloads.append(a[len("--command=") :])
            i += 1
            continue
        if a == "--command":
            if i + 1 < len(rest):
                payloads.append(rest[i + 1])
            i += 2
            continue
        if a.startswith("-") and not a.startswith("--") and "c" in a[1:]:
            for j in range(i + 1, len(rest)):
                if not rest[j].startswith("-"):
                    payloads.append(rest[j])
                    break
            i += 1
            continue
        i += 1
    return payloads


# ---------------------------------------------------------------------------
# Top-level dispatch. Extend the if-chain below with predicates from your
# three-tier table. Each predicate returns (violation_label or None).
# ---------------------------------------------------------------------------


def check_segment(tokens, cwd=None):
    if not tokens:
        return None
    cmd, rest, command_values = resolve_executable(tokens)

    for value in command_values:
        violation = check_command(value)
        if violation:
            return f"{violation} (in wrapper flag-value)"

    if cmd is None:
        return None

    if cmd in SHELL_LAUNCHERS:
        for payload in _extract_shell_c_payloads(rest):
            violation = check_command(payload)
            if violation:
                return f"{violation} (in {cmd} -c)"
        return None
    if cmd == "rm":
        return check_rm(rest, cwd=cwd)
    if cmd == "git":
        return check_git(rest)
    return None


def _update_cwd_from_cd(tokens, cwd):
    if not tokens or tokens[0] != "cd":
        return cwd
    if len(tokens) < 2:
        return cwd
    target = None
    for t in tokens[1:]:
        if t.startswith("-"):
            continue
        target = t
        break
    if target is None:
        return cwd
    if target == "/":
        return "/"
    if target.startswith("/"):
        return os.path.normpath(target)
    if cwd is not None:
        return os.path.normpath(os.path.join(cwd, target))
    return None


def check_command(command):
    if not isinstance(command, str) or not command.strip():
        return None

    command = replace_unquoted_newlines(command)

    for sub in extract_command_substitutions(command):
        violation = check_command(sub)
        if violation:
            return f"{violation} (in command substitution)"

    cwd = None
    for segment in split_pipeline(command):
        violation = check_segment(segment, cwd=cwd)
        if violation:
            return violation
        cwd = _update_cwd_from_cd(segment, cwd)
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
