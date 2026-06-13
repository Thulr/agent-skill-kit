#!/usr/bin/env python3
"""Catalog taxonomy facts shared by renderers and drift checks."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from skill_inventory import SkillInventory


FAMILIES = ("heuristics", "research", "ax", "discovery")
FUNCTIONS = ("audit", "design", "singleton")
REQUIRED_META = ("family", "function", "catalog_summary")
BACKTICK_RE = re.compile(r"`([^`]+)`")


@dataclass(frozen=True)
class SkillRecord:
    name: str
    path: Path
    manifest: dict
    metadata: dict


class CatalogTaxonomy:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.inventory = SkillInventory(self.root)
        self.catalog_path = self.root / "catalog" / "catalog.json"

    def catalog(self) -> dict:
        return json.loads(self.catalog_path.read_text())

    def public_skills(self) -> dict[str, SkillRecord]:
        skills: dict[str, SkillRecord] = {}
        for skill_dir in self.inventory.catalog_skill_dirs():
            manifest_path = skill_dir / "skill.json"
            if not manifest_path.exists():
                skills[skill_dir.name] = SkillRecord(skill_dir.name, skill_dir, {}, {})
                continue
            manifest = json.loads(manifest_path.read_text())
            name = manifest.get("name", skill_dir.name)
            skills[name] = SkillRecord(
                name=name,
                path=skill_dir,
                manifest=manifest,
                metadata=manifest.get("metadata", {}),
            )
        return skills

    def public_skill_metadata(self) -> dict[str, dict]:
        return {name: record.metadata for name, record in self.public_skills().items()}

    def matrix_skill_refs(self) -> set[str]:
        refs: set[str] = set()
        pick = self.catalog()["pick_a_skill"]
        cells: list[str] = []
        for row in pick["primary"]["rows"]:
            cells += [row["critique"], row["design"]]
        for row in pick["secondary"]["rows"]:
            cells.append(row["skill"])
        for cell in cells:
            refs.update(BACKTICK_RE.findall(cell))
        return refs

    def heuristic_pairs(self) -> dict[str, dict[str, SkillRecord]]:
        pairs: dict[str, dict[str, SkillRecord]] = {}
        for record in self.public_skills().values():
            if record.metadata.get("family") != "heuristics":
                continue
            function = record.metadata.get("function")
            if function not in {"audit", "design"}:
                continue
            suffix = f"-{function}"
            if not record.name.endswith(suffix):
                continue
            domain = record.name[: -len(suffix)]
            pairs.setdefault(domain, {})[function] = record
        return {domain: members for domain, members in pairs.items() if set(members) == {"audit", "design"}}

    def shared_substrate_path(self, domain: str) -> Path:
        return self.root / "skills" / "_shared" / domain

    def validate(self) -> list[str]:
        failures: list[str] = []
        catalog = self.catalog()
        skills = self.public_skills()

        for name, record in skills.items():
            if not record.manifest:
                failures.append(f"{name}: missing skill.json")
                continue
            for key in REQUIRED_META:
                if not record.metadata.get(key):
                    failures.append(
                        f"{name}: skill.json metadata.{key} is required for the catalog but is missing/empty"
                    )
            family = record.metadata.get("family")
            function = record.metadata.get("function")
            if family and family not in FAMILIES:
                failures.append(f"{name}: metadata.family {family!r} not one of {FAMILIES}")
            if function and function not in FUNCTIONS:
                failures.append(f"{name}: metadata.function {function!r} not one of {FUNCTIONS}")
            if function in {"audit", "design"} and record.name.endswith(f"-{function}") is False:
                failures.append(f"{name}: metadata.function {function!r} does not match skill name suffix")

        known = set(skills)
        for ref in sorted(self.matrix_skill_refs()):
            if ref not in known:
                failures.append(f"catalog/catalog.json matrix references unknown skill `{ref}`")

        for family in catalog["catalog"]["families"]:
            if not any(record.metadata.get("family") == family["id"] for record in skills.values()):
                failures.append(f"catalog family {family['id']!r} has no skills")

        for domain in self.heuristic_pairs():
            shared = self.shared_substrate_path(domain)
            if not shared.is_dir() or not any(path.is_file() for path in shared.rglob("*")):
                failures.append(f"heuristic pair {domain!r} is missing shared substrate {shared.relative_to(self.root)}")

        arch_doc = self.root / "docs" / "architecture" / "README.md"
        if arch_doc.is_file():
            text = arch_doc.read_text()
            for domain in sorted(self.heuristic_pairs()):
                if f"`{domain}`" not in text:
                    failures.append(f"docs/architecture/README.md omits heuristic pair domain `{domain}`")
        else:
            failures.append("docs/architecture/README.md is missing")

        return failures
