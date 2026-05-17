#!/usr/bin/env bash
#
# Asserts that every skill referencing a file from `skills/_shared/` does so
# via a relative symlink to the canonical source, not via a regular-file copy.
#
# Background: `npx skills` dereferences symlinks at install time (verified
# 2026-05-16 — see docs/specs/2026-05-16-evidence-driven-agent-rules-split/spec.md
# §Q1), so the symlink approach gives single-source-of-truth at maintenance
# time AND self-contained skills at install time. The one regression vector
# is a maintainer accidentally replacing a symlink with an edited regular
# file, which silently breaks the canonical contract. This check catches
# that.
#
# Run by `just check` and CI.
#
# Invariants enforced:
# 1. For every file in `skills/_shared/`, every skill that has a file of the
#    same basename under `<skill>/references/` MUST have it as a symlink (not
#    a regular file).
# 2. Every such symlink MUST resolve to a file inside `skills/_shared/`.
# 3. Every such symlink MUST resolve to an existing file (no orphan
#    symlinks).
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

shared_count=$(find "$SHARED_DIR" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')
if [[ $shared_count -eq 0 ]]; then
    echo "OK:   $SHARED_DIR/ exists but contains no shared files yet"
    exit 0
fi

failed=0
checked=0

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
        basename=$(basename "$shared_file")
        candidate="$refs_dir/$basename"

        # If this skill has no file of that name, it doesn't reference the
        # shared one. That's fine.
        [[ -e $candidate || -L $candidate ]] || continue

        checked=$((checked + 1))

        # Must be a symlink, not a regular file.
        if [[ ! -L $candidate ]]; then
            echo "FAIL: $candidate exists as a regular file but $shared_file is its canonical source" >&2
            echo "      → replace with: ln -sf <relative-path>/$basename $candidate" >&2
            failed=1
            continue
        fi

        # Symlink target must resolve.
        if [[ ! -e $candidate ]]; then
            target=$(readlink "$candidate")
            echo "FAIL: $candidate is a symlink to '$target' which does not resolve" >&2
            failed=1
            continue
        fi

        # Symlink target must be a RELATIVE path. Absolute symlinks
        # (e.g., /workspace/informed-skills/skills/_shared/lenses.md)
        # validate fine on the machine that wrote them but break on
        # clone/install elsewhere because the absolute prefix doesn't
        # exist. Regression vector Codex caught on PR #12 (commit
        # 2057166): the realpath-under-_shared check below passes for
        # absolute targets even though they are non-portable.
        target=$(readlink "$candidate")
        if [[ $target == /* ]]; then
            echo "FAIL: $candidate is an absolute symlink ('$target') — must be relative" >&2
            echo "      → recreate as: ln -sf <relative-path>/$basename $candidate" >&2
            failed=1
            continue
        fi

        # Symlink must resolve to a file inside skills/_shared/.
        resolved=$(python3 -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "$candidate")
        shared_abs="$(cd "$SHARED_DIR" && pwd)"
        if [[ $resolved != "$shared_abs"/* ]]; then
            echo "FAIL: $candidate resolves to '$resolved' which is outside $SHARED_DIR/" >&2
            failed=1
            continue
        fi

        # Symlink must resolve to the file with the matching basename.
        # Otherwise references/lenses.md -> _shared/empirical-warnings.md
        # would silently pass: the symlink IS inside _shared/, but the
        # content is wrong. This is the regression vector Codex caught
        # on PR #12 (commit 83d97400).
        if [[ "$(basename "$resolved")" != "$basename" ]]; then
            echo "FAIL: $candidate is a symlink to '$resolved' but the basename does not match '$basename'" >&2
            echo "      → fix the symlink target to point at $SHARED_DIR/$basename" >&2
            failed=1
            continue
        fi

        echo "OK:   $candidate -> $(readlink "$candidate")"
    done
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
