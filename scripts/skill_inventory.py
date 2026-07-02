#!/usr/bin/env python3
"""Typed inventory for the repository's Agent Skill install lanes.

The lane names are intentionally explicit. ADR 0002 and AGENTS.md Rule 1 require
path-based gates to cover all three install lanes:

- `skills/<name>/`
- `skills/.experimental/<name>/`
- `.agents/skills/<name>/`

This module keeps that topology local while preserving auditability for callers.
"""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


INTERNAL_RE = re.compile(
    r"(?m)^metadata:\s*\n(?:^[ \t]+[^\n]*\n)*^[ \t]+internal:\s*true\s*$"
)


@dataclass(frozen=True)
class SkillLane:
    name: str
    rel_path: Path


PRODUCT_LANE = SkillLane("product", Path("skills"))
EXPERIMENTAL_LANE = SkillLane("experimental", Path("skills/.experimental"))
REPO_LOCAL_LANE = SkillLane("repo-local", Path(".agents/skills"))
INSTALL_LANES = (PRODUCT_LANE, EXPERIMENTAL_LANE, REPO_LOCAL_LANE)


class SkillInventory:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def lane_path(self, lane: SkillLane) -> Path:
        return self.root / lane.rel_path

    def is_internal(self, skill_dir: Path) -> bool:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            return False
        return bool(INTERNAL_RE.search(skill_md.read_text()))

    def product_lane_skill_dirs(self) -> list[Path]:
        """Skills under `skills/<name>/`, including internal templates.

        Excludes `_shared/` and the reserved `.experimental/` lane.
        """
        base = self.lane_path(PRODUCT_LANE)
        dirs = [
            path
            for path in self._child_dirs(base)
            if path.name not in {"_shared", ".experimental"}
        ]
        return self._without_gitignored(dirs)

    def experimental_skill_dirs(self) -> list[Path]:
        """Skill directories under the reserved experimental lane."""
        return self._without_gitignored(self._child_dirs(self.lane_path(EXPERIMENTAL_LANE)))

    def release_skill_dirs(self) -> list[Path]:
        """All product-lane release artifacts, including the reserved lane."""
        return sorted(self.product_lane_skill_dirs() + self.experimental_skill_dirs())

    def all_skill_dirs(self) -> list[Path]:
        """Every skill directory in every install lane."""
        return sorted(self.release_skill_dirs() + self.repo_local_skill_dirs())

    def catalog_skill_dirs(self) -> list[Path]:
        """Installable public skills rendered into the README catalog."""
        return [
            path
            for path in self.product_lane_skill_dirs()
            if not self.is_internal(path)
        ]

    def repo_local_skill_dirs(self) -> list[Path]:
        """Repo-local authoring/review skills under `.agents/skills/<name>/`."""
        return self._without_gitignored(self._child_dirs(self.lane_path(REPO_LOCAL_LANE)))

    def experimental_lane_entries(self) -> list[Path]:
        """Non-placeholder entries in the reserved experimental lane.

        Used by release gates to enforce that the lane stays empty until a future
        decision reopens it.
        """
        base = self.lane_path(EXPERIMENTAL_LANE)
        if not base.exists():
            return []
        entries = [path for path in base.iterdir() if path.name != ".gitkeep"]
        return sorted(self._without_gitignored(entries))

    def static_check_scripts(self) -> list[Path]:
        """Existing per-skill static-check scripts across all install lanes.

        Also includes the template contract's script (AGENTS.md Rule 3):
        the template must satisfy every gate published skills satisfy, so
        its static check runs in the same sweep instead of silently rotting
        outside the install lanes.
        """
        scripts: list[Path] = []
        for skill_dir in self.all_skill_dirs():
            script = skill_dir / "evals" / "run-static-checks.sh"
            if script.exists():
                scripts.append(script)
        template_script = (
            self.root / "docs" / "templates" / "example-minimal" / "evals" / "run-static-checks.sh"
        )
        if template_script.exists():
            scripts.append(template_script)
        return sorted(scripts)

    def routing_csv_files(self) -> list[Path]:
        """Routing CSV files across all install lanes.

        A routing CSV is any `*-router.csv` or any CSV under an `intents/`
        directory. This mirrors the repo contract documented in
        `skills/_shared/routing-contract.md`.
        """
        files: list[Path] = []
        for skill_dir in self.all_skill_dirs():
            refs = skill_dir / "references"
            if not refs.exists():
                continue
            for path in refs.rglob("*.csv"):
                if path.name.endswith("-router.csv") or "intents" in path.relative_to(refs).parts:
                    files.append(path)
        return self._without_gitignored(files)

    def _child_dirs(self, base: Path) -> list[Path]:
        if not base.exists():
            return []
        return sorted(path for path in base.iterdir() if path.is_dir())

    def _without_gitignored(self, paths: list[Path]) -> list[Path]:
        ignored = self.git_ignored(paths)
        return sorted(path for path in paths if path not in ignored)

    def git_ignored(self, paths: list[Path]) -> set[Path]:
        """Return the subset of paths ignored by git.

        Gitignored local skill clutter is not a release artifact. On clean CI
        checkouts this is normally empty; if git is unavailable or errors, the
        method falls back to treating nothing as ignored, matching the previous
        gate behavior.
        """
        if not paths:
            return set()
        by_rel = {self._git_path(path): path for path in paths}
        try:
            proc = subprocess.run(
                ["git", "check-ignore", "--stdin"],
                cwd=self.root,
                text=True,
                capture_output=True,
                input="\n".join(by_rel),
            )
        except OSError:
            return set()
        if proc.returncode not in (0, 1):
            return set()
        return {by_rel[line] for line in proc.stdout.splitlines() if line in by_rel}

    def _git_path(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return str(path)
