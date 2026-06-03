#!/usr/bin/env bash
#
# Asserts that every skill referencing a file from `skills/_shared/` does so
# via a relative symlink to the canonical source, not via a regular-file copy.
#
# Background: `npx skills` dereferences symlinks at install time (verified
# 2026-05-16 — see docs/specs/2026-05-16-agent-rules-split/spec.md
# §Q1), so the symlink approach gives single-source-of-truth at maintenance
# time AND self-contained skills at install time. The one regression vector
# is a maintainer accidentally replacing a symlink with an edited regular
# file, which silently breaks the canonical contract. This check catches
# that.
#
# Run by `just check` and CI.
#
# Invariants enforced:
# 1. The canonical shared corpus is any file under `skills/_shared/**`,
#    including nested shared templates.
# 2. For every top-level Markdown file in `skills/_shared/`, every skill that
#    has a file of the same basename under `<skill>/references/` MUST have it
#    as a symlink (not a regular file).
# 3. Every symlink anywhere under a skill that resolves into `skills/_shared/**`
#    MUST be relative, resolve, stay inside `skills/_shared/`, and point to a
#    canonical file with the same basename. This covers shared templates as
#    well as shared references.
# 4. Every such symlink MUST resolve to an existing file (no orphan symlinks).
#
# Skills that don't reference a given shared file are not required to —
# this only enforces consistency for skills that DO reference one.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SHARED_DIR="skills/_shared"

if [[ ! -d $SHARED_DIR ]]; then
    echo "OK:   no $SHARED_DIR/ yet — nothing to check"
    exit 0
fi

shared_count=$(find "$SHARED_DIR" -type f | wc -l | tr -d ' ')
if [[ $shared_count -eq 0 ]]; then
    echo "OK:   $SHARED_DIR/ exists but contains no shared files yet"
    exit 0
fi

failed=0
checked=0
checked_paths=""
shared_abs="$(cd "$SHARED_DIR" && pwd)"

check_shared_symlink() {
    local candidate=$1
    local expected_basename=${2:-}

    if printf '%s' "$checked_paths" | grep -Fxq "$candidate"; then
        return
    fi
    checked_paths="${checked_paths}${candidate}"$'\n'
    checked=$((checked + 1))

    if [[ ! -L $candidate ]]; then
        echo "FAIL: $candidate exists as a regular file but a shared file is its canonical source" >&2
        echo "      → replace with a relative symlink into $SHARED_DIR/" >&2
        failed=1
        return
    fi

    if [[ ! -e $candidate ]]; then
        local missing_target
        missing_target=$(readlink "$candidate")
        echo "FAIL: $candidate is a symlink to '$missing_target' which does not resolve" >&2
        failed=1
        return
    fi

    local target
    target=$(readlink "$candidate")
    if [[ $target == /* ]]; then
        echo "FAIL: $candidate is an absolute symlink ('$target') — must be relative" >&2
        echo "      → recreate as a relative symlink into $SHARED_DIR/" >&2
        failed=1
        return
    fi

    local resolved
    resolved=$(python3 -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "$candidate")
    if [[ $resolved != "$shared_abs"/* ]]; then
        echo "FAIL: $candidate resolves to '$resolved' which is outside $SHARED_DIR/" >&2
        failed=1
        return
    fi

    local basename
    basename=$(basename "$resolved")
    if [[ -n $expected_basename && $basename != "$expected_basename" ]]; then
        echo "FAIL: $candidate is a symlink to '$resolved' but the basename does not match '$expected_basename'" >&2
        echo "      → fix the symlink target to point at $SHARED_DIR/$expected_basename" >&2
        failed=1
        return
    fi

    echo "OK:   $candidate -> $target"
}

# Enumerate every skill (all three install lanes per AGENTS.md Rule 1).
shopt -s nullglob
for skill_dir in skills/*/ skills/.experimental/*/ .agents/skills/*/; do
    # Skip the _shared dir itself if the glob picked it up.
    [[ $skill_dir == "skills/_shared/" ]] && continue
    # Skip dirs without SKILL.md (not actually skills).
    [[ -f "${skill_dir}SKILL.md" ]] || continue

    refs_dir="${skill_dir}references"
    [[ -d $refs_dir ]] || continue

    for shared_file in "$SHARED_DIR"/*.md; do
        [[ -f $shared_file ]] || continue
        basename=$(basename "$shared_file")
        candidate="$refs_dir/$basename"

        # If this skill has no file of that name, it doesn't reference the
        # shared one. That's fine.
        [[ -e $candidate || -L $candidate ]] || continue

        check_shared_symlink "$candidate" "$basename"
    done

    while IFS= read -r symlink; do
        resolved=$(python3 -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "$symlink")
        [[ $resolved == "$shared_abs"/* ]] || continue
        check_shared_symlink "$symlink" "$(basename "$resolved")"
    done < <(find "$skill_dir" -type l -print)
done

if [[ $checked -eq 0 ]]; then
    echo "OK:   no skill currently references any shared file (consider why $SHARED_DIR/ has $shared_count file(s) but no consumers)"
fi

if [[ $failed -ne 0 ]]; then
    echo
    echo "Shared-content checks FAILED."
    exit 1
fi

echo "All shared-content checks passed ($checked symlink(s) verified)."
