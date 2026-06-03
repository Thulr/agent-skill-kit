#!/usr/bin/env python3
"""Shared PreToolUse policy for blocking destructive Bash actions.

Harness adapters read the tool-use payload from stdin and call `main()`.
This policy exits 2 to block with a message the model will see and exits 0
to allow. Any other non-zero exit is treated as a hook error.

Implementation shape:
  - Real newlines are pre-processed into `;` outside quotes (multi-line
    commands count as compound statements, not single segments).
  - Command substitutions (`$(...)`, backticks, `<(...)`, `>(...)`) are
    extracted and recursively checked as their own commands.
  - `shlex` tokenizes the result with `punctuation_chars=True`; the
    pipeline splits on `;`, `&&`, `||`, `|`, `&`, and shell group
    delimiters `(`, `)`, `{`, `}`.
  - Each pipeline segment is unwrapped: env-var prefixes (`FOO=bar cmd`),
    transparent wrappers (`sudo`, `time`, `env`, `command`), and per-
    wrapper value-taking flags (`sudo -u root cmd`) are consumed before
    the executable is identified.
  - For `rm`, target paths are canonicalized via `os.path.normpath` so
    traversal forms like `/tmp/../etc` resolve to `/etc` before the
    protected-dir check; `~`, `$HOME`, and `${HOME}` are all recognized.
  - For `git`, global options with separate-token values (`-C`, `-c`,
    `--work-tree`, `--git-dir`, `--namespace`, `--super-prefix`,
    `--config-env`, `--exec-path`) consume the next token so the
    subcommand dispatch still finds `push` / `branch`.

Blocked patterns (see AGENTS.md §Forbidden actions):
  - `git push` with `--force` / `-f` / `--force-with-lease[=…]` /
    `--force-if-includes`, OR a `+refspec`, targeting `main` / `master`.
    Force pushes with omitted/ambiguous refspecs are also blocked because
    Git may default to the current protected upstream branch.
  - `git branch -D main` / `git branch -D master`.
  - `rm -r` (or `-R` / `--recursive`, in any order, separable, with or
    without `-f` / `--force`, with or without `--` terminator) of `/`,
    protected system dirs, `~` / `$HOME` / `${HOME}`, or anywhere under
    them. Path traversal forms (`/tmp/../etc`) are canonicalized first.
  - `find <protected-root> … -delete` / `-exec rm` / `-execdir rm`, and the
    non-`rm` deleters `shred` / `truncate` / `unlink` / `rmdir` of a
    protected path. Execution wrappers `nohup` / `timeout` / `flock` /
    `setsid` / `stdbuf` / `watch` / `xargs` (plus the existing `sudo` / `env`
    / `nice` / …) are unwrapped before the command is identified.
"""

import json
import os
import shlex
import sys

PROTECTED_GIT_BRANCHES = frozenset(["main", "master"])

PROTECTED_TOP_DIRS = frozenset(
    [
        "/bin", "/boot", "/etc", "/lib", "/opt", "/sbin", "/sys",
        "/proc", "/root", "/run", "/srv", "/usr", "/var", "/home",
        "/System", "/Library", "/Applications", "/Users",
    ]
)

TRANSPARENT_WRAPPERS = frozenset(
    [
        "sudo", "doas", "command", "exec", "time", "nice", "ionice", "env",
        # Execution wrappers that run an arbitrary following command. Omitting
        # them let `nohup rm -rf /etc`, `timeout 5 rm -rf /etc`,
        # `xargs rm -rf /etc`, etc. through unchecked (reflection-log
        # 2026-06-02-hook-wrapper-bypasses).
        "nohup", "setsid", "stdbuf", "timeout", "flock", "watch", "xargs",
    ]
)

# Wrappers that consume a fixed number of positional tokens (after their option
# flags) before the wrapped command: `timeout DURATION cmd`, `flock LOCKFILE cmd`.
WRAPPER_POSITIONAL_ARGS = {"timeout": 1, "flock": 1}

# Non-`rm` commands that destroy a target path outright. Blocked when a target
# resolves to a protected dir, `/`, or $HOME (reflection-log
# 2026-06-02-hook-nonrm-deleters).
SIMPLE_DELETERS = frozenset(["shred", "truncate", "unlink", "rmdir"])

# Shell launchers whose `-c "<cmd>"` value must be inspected as its own command
# (failure-log entry 9: `bash -c 'rm -rf /etc'` was treated as opaque). Handles
# combined short flags like `-lc`.
SHELL_LAUNCHERS = frozenset(["sh", "bash", "zsh", "dash", "ksh", "ash", "fish"])

# Per-wrapper flags that consume a following token as their value (long forms
# with `=` are handled separately). Conservative: only include flags actually
# documented by the wrapper. Unknown wrappers fall back to one-token-per-flag.
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
    "stdbuf": frozenset(["-i", "-o", "-e", "--input", "--output", "--error"]),
    "timeout": frozenset(["-s", "--signal", "-k", "--kill-after"]),
    "flock": frozenset(
        ["-w", "--timeout", "-E", "--conflict-exit-code", "-c", "--command"]
    ),
    "watch": frozenset(["-n", "--interval"]),
    "xargs": frozenset(
        [
            "-I", "-i", "-n", "--max-args", "-P", "--max-procs", "-d",
            "--delimiter", "-E", "-s", "--max-chars", "-a", "--arg-file",
            "-L", "--max-lines",
        ]
    ),
}

# (wrapper, flag) pairs where the consumed value is a command string and must
# be recursively inspected. `env -S 'rm -rf /etc'` packs a command into `-S`.
WRAPPER_COMMAND_VALUE_FLAGS = frozenset(
    [
        ("env", "-S"),
        ("env", "--split-string"),
        # `flock -c '<cmd>'` / `flock --command '<cmd>'` run the value via a shell.
        ("flock", "-c"),
        ("flock", "--command"),
    ]
)

# Top-level `git` options that take a following token as their value.
# Long forms with `=` are handled inline.
GIT_VALUE_FLAGS = frozenset(
    [
        "-C", "-c",
        "--work-tree", "--git-dir", "--namespace", "--super-prefix",
        "--config-env", "--exec-path", "--list-cmds",
    ]
)

PIPELINE_SEPARATORS = frozenset([";", "&", "&&", "|", "||"])
SHELL_GROUP_DELIMITERS = frozenset(["(", ")", "{", "}"])


# ---------------------------------------------------------------------------
# Pre-tokenization passes: newline normalization + command-substitution
# extraction. Both run before shlex sees the command so the lexer doesn't
# lose information.
# ---------------------------------------------------------------------------


def replace_unquoted_newlines(command):
    """Replace real newlines (and \\r) with `; ` outside of quoted strings.

    Bash treats a line break between commands as semantically equivalent to
    `;`. Without this pass, `whitespace_split=True` strips the newline and
    runs the two commands together as a single segment (a bypass).
    """
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
    """Extract one level of `$(...)`, `<(...)`, `>(...)`, and `` `...` `` bodies.

    Returns a list of inner strings (without the wrapping syntax). Nested
    `$(...)` is handled via paren-depth tracking; backticks don't nest
    meaningfully so we just match to the next backtick.

    Callers should recursively `check_command` each returned body; deeper
    nesting unfolds through that recursion.
    """
    subs = []
    i = 0
    n = len(command)
    while i < n:
        c = command[i]
        # $( <( >(
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
        # backticks
        elif c == "`":
            j = command.find("`", i + 1)
            if j != -1:
                subs.append(command[i + 1 : j])
                i = j + 1
                continue
        i += 1
    return subs


def split_pipeline(command):
    """Tokenize and split a command on shell pipeline operators.

    Caller is expected to have already run `replace_unquoted_newlines`.
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
        if tok in PIPELINE_SEPARATORS or tok in SHELL_GROUP_DELIMITERS:
            if current:
                segments.append(current)
                current = []
        else:
            current.append(tok)
    if current:
        segments.append(current)
    return segments


# ---------------------------------------------------------------------------
# Executable resolution: walk past env-var prefixes and transparent wrappers,
# consuming wrapper-owned flags AND their values.
# ---------------------------------------------------------------------------


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
    """Advance `i` past `argv[i]`'s wrapper flags, consuming flag values.

    `value_flags` is the per-wrapper set of flags that take a following token.
    `--` ends the option list. Long forms `--flag=value` keep value inline.

    For (wrapper, flag) pairs in `WRAPPER_COMMAND_VALUE_FLAGS`, the value is
    a command string that must be recursively inspected; we append it to
    `command_values` so the caller can check it.
    """
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
    """Walk past env-var prefixes and transparent wrappers; return (cmd, rest, command_values).

    `command_values` is a list of wrapper flag-values that are themselves
    command strings (e.g. `env -S 'rm -rf /etc'`). The caller recursively
    checks each.
    """
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
            # Some wrappers take positional args (a duration, a lockfile) between
            # their flags and the wrapped command. Consume them, then re-skip
            # flags so trailing options like `flock LOCKFILE -c '<cmd>'` are seen.
            positional = WRAPPER_POSITIONAL_ARGS.get(wrapper_name, 0)
            if positional:
                while positional > 0 and i < len(argv) and not argv[i].startswith("-"):
                    i += 1
                    positional -= 1
                i = _skip_wrapper_flags(argv, i, value_flags, wrapper_name, command_values)
            continue
        break
    if i >= len(argv):
        return None, [], command_values
    return argv[i], argv[i + 1 :], command_values


# ---------------------------------------------------------------------------
# rm — block recursive destruction of protected paths.
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
    """Block recursive rm of protected paths.

    `cwd` is the simulated working directory after any preceding `cd` segments
    in the same pipeline (failure-log entry 9: `cd / && rm -rf etc` was
    allowed because the rm target was relative). When unknown, treated as
    None and relative targets fall back to the `..`-escape check.
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
            # Canonicalize (.., //, .) before the protected-dir check.
            normalized = os.path.normpath(target)
            if normalized == "/":
                return "rm -r of /"
            head = _first_path_component(normalized)
            if head in PROTECTED_TOP_DIRS:
                return f"rm -r under protected dir {head}"
        else:
            # Relative target. Two checks:
            # 1. If we have a simulated cwd from a preceding `cd`, resolve
            #    target against it and re-check against protected dirs.
            # 2. Independently, block any `..` escape (`../../etc`) — even
            #    when cwd is unknown, that's destination-unknown traversal.
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
# find -delete / -exec rm, and non-rm deleters (shred/truncate/unlink/rmdir).
# These destroy protected paths without invoking `rm` (reflection-log
# 2026-06-02-hook-find-delete-bypass / 2026-06-02-hook-nonrm-deleters).
# ---------------------------------------------------------------------------


def _protected_path_reason(target, cwd=None):
    """Return a short reason if `target` resolves to a protected location.

    Shared by `find` and the simple deleters. Mirrors `check_rm`'s protected-path
    logic (home, `/`, protected top dirs, `..` escapes, cwd-resolved relatives)
    but returns only the reason fragment, or None when the target is safe.
    """
    if target in _HOME_EXACT:
        return f"of {target}"
    if any(target.startswith(p) for p in _HOME_PREFIXES):
        return f"under $HOME ({target!r})"
    if target == "/" or target.rstrip("/") == "":
        return "of /"
    if target.startswith("/"):
        normalized = os.path.normpath(target)
        if normalized == "/":
            return "of /"
        head = _first_path_component(normalized)
        if head in PROTECTED_TOP_DIRS:
            return f"under protected dir {head}"
        return None
    # Relative target.
    if cwd is not None:
        joined = os.path.normpath(os.path.join(cwd, target))
        if joined == "/":
            return f"of / (relative {target!r} from cwd={cwd})"
        if joined.startswith("/"):
            head = _first_path_component(joined)
            if head in PROTECTED_TOP_DIRS:
                return f"under protected dir {head} (relative {target!r} from cwd={cwd})"
    normalized_rel = os.path.normpath(target)
    if normalized_rel == ".." or normalized_rel.startswith("../"):
        return f"of cwd-escape path ({target!r})"
    return None


def check_find(argv, cwd=None):
    """Block `find <protected-root> ... -delete` / `-exec rm` / `-execdir rm`.

    Roots are the leading non-option operands (default `.`). The destructive
    actions are `-delete` and `-exec`/`-execdir` invoking `rm` (incl. `/bin/rm`).
    Relative/cwd-local roots (`.`, `/tmp`, ...) are allowed, matching `rm`.

    GNU find accepts global options *before* the path list —
    `find [-H] [-L] [-P] [-D debugopts] [-Olevel] [path...] [expression]` — so
    those are skipped first; otherwise `find -H /etc -delete` would collect an
    empty root list, fall back to `.`, and slip a protected path past the gate
    (reflection-log 2026-06-02-hook-find-option-bypass).
    """
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("-H", "-L", "-P"):
            i += 1
        elif a == "-D":  # -D takes a following debugopts argument
            i += 2
        elif a.startswith("-O"):  # -Olevel, attached (e.g. -O3)
            i += 1
        elif a == "--":  # end of options; the rest are paths/expression
            i += 1
            break
        else:
            break

    roots = []
    while i < len(argv) and not argv[i].startswith(("-", "(", "!", ")")):
        roots.append(argv[i])
        i += 1
    if not roots:
        roots = ["."]

    has_delete = "-delete" in argv
    has_exec_rm = False
    for j, a in enumerate(argv):
        if a in ("-exec", "-execdir") and j + 1 < len(argv):
            if os.path.basename(argv[j + 1]) == "rm":
                has_exec_rm = True
                break
    if not (has_delete or has_exec_rm):
        return None

    action = "-delete" if has_delete else "-exec rm"
    for root in roots:
        reason = _protected_path_reason(root, cwd=cwd)
        if reason:
            return f"find {action} {reason}"
    return None


def check_simple_deleter(cmd, argv, cwd=None):
    """Block `shred`/`truncate`/`unlink`/`rmdir` of a protected target.

    Non-option tokens are candidate targets; option values like the `0` in
    `truncate -s 0` are harmless (they don't resolve to a protected path), so a
    precise per-command value-flag table isn't needed.
    """
    after_double_dash = False
    for arg in argv:
        if not after_double_dash:
            if arg == "--":
                after_double_dash = True
                continue
            if arg.startswith("-"):
                continue
        reason = _protected_path_reason(arg, cwd=cwd)
        if reason:
            return f"{cmd} {reason}"
    return None


# ---------------------------------------------------------------------------
# git push / git branch -D — block force-update to protected branches.
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

    if has_force_flag and len(refspec_tokens) <= 1:
        return "force-push with omitted or ambiguous refspec"

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
    """Skip git-level options (including value-taking ones) and dispatch."""
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


# ---------------------------------------------------------------------------
# Top-level dispatch.
# ---------------------------------------------------------------------------


def _extract_shell_c_payloads(rest):
    """Return any `-c <cmd>` / `-c<cmd>` / combined-flag command strings.

    Handles `bash -c "cmd"`, `bash -lc "cmd"` (combined short flags including
    `c`), and `bash -c"cmd"` (packed form). Long form `--command="cmd"` is
    handled by the same parse.
    """
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
            # Combined short-flag bundle including `c` (e.g. `-lc`, `-lic`).
            # Next non-flag arg is the command string.
            for j in range(i + 1, len(rest)):
                if not rest[j].startswith("-"):
                    payloads.append(rest[j])
                    break
            i += 1
            continue
        i += 1
    return payloads


def check_segment(tokens, cwd=None):
    if not tokens:
        return None
    cmd, rest, command_values = resolve_executable(tokens)

    # Wrapper flag-values that themselves carry commands (e.g. `env -S "rm -rf /etc"`).
    # Inspect before the cmd-None early return — `env -S "rm -rf /etc"` with no
    # following executable still executes the embedded command.
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
    if cmd == "find":
        return check_find(rest, cwd=cwd)
    if cmd in SIMPLE_DELETERS:
        return check_simple_deleter(cmd, rest, cwd=cwd)
    if cmd == "git":
        return check_git(rest)
    return None


def _update_cwd_from_cd(tokens, cwd):
    """If `tokens` is a `cd` segment, return the new simulated cwd; else cwd."""
    if not tokens or tokens[0] != "cd":
        return cwd
    # `cd` with no args goes to $HOME. We don't track that — leave cwd.
    if len(tokens) < 2:
        return cwd
    # Skip `cd` options like `-L`, `-P`, `-e`.
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
    # Unknown starting cwd + relative cd — can't resolve.
    return None


def check_command(command):
    """Top-level: pre-process, extract substitutions, split pipeline, check.

    Tracks a simulated cwd across pipeline segments so that `cd /` followed
    by `rm -rf etc` resolves the relative target to `/etc`. This is an
    approximation — pipe segments (`|`) actually run in subshells with
    inherited cwd, so over-tracking through them is acceptable.
    """
    if not isinstance(command, str) or not command.strip():
        return None

    command = replace_unquoted_newlines(command)

    # Recursively inspect command substitutions — they execute as their own
    # commands during shell expansion, so destructive forms inside them are
    # equally dangerous.
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


def _block_uninspectable(reason):
    print(
        "BLOCKED by PreToolUse hook: shell-tool payload could not be inspected "
        f"({reason}).\n"
        "See AGENTS.md §Forbidden actions. If this is genuinely intended, "
        "run it manually in a terminal outside the agent session.",
        file=sys.stderr,
    )
    return 2


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return _block_uninspectable("invalid JSON")

    if not isinstance(payload, dict):
        return _block_uninspectable("payload is not a JSON object")

    # Recognize each harness's shell-tool name. Claude Code and Codex emit
    # "Bash"; Cursor emits "Shell". Any other tool name is out of scope.
    if payload.get("tool_name") not in ("Bash", "Shell"):
        return 0

    tool_input = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        return _block_uninspectable("tool_input is not a JSON object")

    command = tool_input.get("command", "")
    if not isinstance(command, str):
        return _block_uninspectable("tool_input.command is not a string")

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
