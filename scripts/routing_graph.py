#!/usr/bin/env python3
"""Executable routing graph checks for Agent Skill CSV routers."""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path


ROUTING_HEADERS = {
    ("intent", "name", "when_to_use", "registry_file", "default_template"),
    ("intent", "trigger_examples", "detail_file", "templates", "notes"),
    ("intent", "trigger_examples", "detail_files", "templates", "notes"),
    ("intent", "when_to_pick", "output_template", "additional_rubric"),
    ("route", "trigger_examples", "detail_files", "templates", "notes"),
    ("frame", "name", "when_to_use", "path"),
    ("layer", "sub_surface", "what_it_covers", "playbook"),
}

INTENT_REGISTRY_PREFIX = ("surface", "name", "when_to_use", "playbook", "core_refs")
OPTIONAL_INTENT_COLUMNS = {"output_template", "artifact_template"}
TARGET_COLUMNS = {
    "additional_rubric",
    "artifact_template",
    "core_refs",
    "default_template",
    "detail_file",
    "detail_files",
    "output_template",
    "path",
    "playbook",
    "registry_file",
    "templates",
}
ROUTE_ID_COLUMNS = ("route", "intent", "frame")
SURFACE_ID_COLUMNS = ("surface", "sub_surface")
VIRTUAL_ROUTE_SUFFIXES = {"all", "closeout", "tracking"}


@dataclass
class CsvDocument:
    path: Path
    header: list[str]
    rows: list[dict[str, str]]


@dataclass
class RoutingGraph:
    skill_dir: Path
    csvs: list[CsvDocument] = field(default_factory=list)
    route_ids: set[str] = field(default_factory=set)
    nested_route_prefixes: set[str] = field(default_factory=set)
    target_paths: set[Path] = field(default_factory=set)
    failures: list[str] = field(default_factory=list)

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def rel(self, path: Path) -> str:
        try:
            return path.relative_to(self.skill_dir).as_posix()
        except ValueError:
            return str(path)


def read_csv_document(path: Path, graph: RoutingGraph) -> CsvDocument | None:
    try:
        with path.open(newline="") as fh:
            raw_rows = [
                row
                for row in csv.reader(fh)
                if row and any(cell.strip() for cell in row) and not row[0].lstrip().startswith("#")
            ]
    except OSError as exc:
        graph.fail(f"{graph.rel(path)}: cannot read CSV ({exc})")
        return None
    if not raw_rows:
        graph.fail(f"{graph.rel(path)}: no header row (only blank/comment lines)")
        return None
    header = raw_rows[0]
    if len(header) < 2:
        graph.fail(f"{graph.rel(path)}: header has fewer than 2 columns: {header}")
        return None
    rows: list[dict[str, str]] = []
    for index, row in enumerate(raw_rows[1:], start=2):
        if len(row) != len(header):
            graph.fail(
                f"{graph.rel(path)}: data row {index} has {len(row)} fields, "
                f"header has {len(header)}: {row}"
            )
            continue
        rows.append(dict(zip(header, row)))
    return CsvDocument(path=path, header=header, rows=rows)


def split_refs(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(";") if part.strip()]


def is_intent_registry(path: Path) -> bool:
    return "intents" in path.parts and path.name.endswith(".csv")


def check_header(doc: CsvDocument, graph: RoutingGraph) -> None:
    header = tuple(doc.header)
    if is_intent_registry(doc.path.relative_to(graph.skill_dir)):
        extra = set(doc.header[len(INTENT_REGISTRY_PREFIX):])
        if tuple(doc.header[: len(INTENT_REGISTRY_PREFIX)]) != INTENT_REGISTRY_PREFIX:
            graph.fail(f"{graph.rel(doc.path)}: unexpected intent-registry header {doc.header}")
        elif extra - OPTIONAL_INTENT_COLUMNS:
            graph.fail(f"{graph.rel(doc.path)}: unexpected intent-registry columns {sorted(extra)}")
    elif header not in ROUTING_HEADERS:
        graph.fail(f"{graph.rel(doc.path)}: unexpected routing header {doc.header}")


def resolve_target(skill_dir: Path, csv_path: Path, value: str) -> Path:
    raw = Path(value)
    candidates = []
    if raw.parts and raw.parts[0] in {"references", "templates", "evals"}:
        candidates.append(skill_dir / raw)
    else:
        candidates.append(csv_path.parent / raw)
        candidates.append(skill_dir / "references" / raw)
        candidates.append(skill_dir / raw)
    for candidate in candidates:
        if candidate.exists() or candidate.is_symlink():
            return candidate.resolve()
    return candidates[0]


def collect_targets(doc: CsvDocument, graph: RoutingGraph) -> None:
    for row in doc.rows:
        for column in TARGET_COLUMNS:
            if column not in row:
                continue
            for ref in split_refs(row.get(column)):
                # Frame paths may point at a directory that contains a nested router.
                target = resolve_target(graph.skill_dir, doc.path, ref)
                graph.target_paths.add(target.resolve())
                if not (target.exists() or target.is_symlink()):
                    graph.fail(f"{graph.rel(doc.path)}: {column} references missing target: {ref}")


def first_existing_csv(skill_dir: Path, csv_path: Path, ref: str) -> Path | None:
    target = resolve_target(skill_dir, csv_path, ref)
    if target.is_file() and target.suffix == ".csv":
        return target
    if target.is_dir():
        for candidate in ("intent-router.csv", "surface-router.csv", "frame-router.csv"):
            nested = target / candidate
            if nested.is_file():
                return nested
    return None


def collect_route_ids(graph: RoutingGraph) -> None:
    by_path = {doc.path.resolve(): doc for doc in graph.csvs}
    for doc in graph.csvs:
        for row in doc.rows:
            for column in ROUTE_ID_COLUMNS:
                value = row.get(column, "").strip()
                if value:
                    graph.route_ids.add(value)
            for column in SURFACE_ID_COLUMNS:
                value = row.get(column, "").strip()
                if value:
                    graph.route_ids.add(value)

            intent = row.get("intent", "").strip()
            registry = row.get("registry_file", "").strip()
            if intent and registry:
                graph.route_ids.update(f"{intent}/{suffix}" for suffix in VIRTUAL_ROUTE_SUFFIXES)
                nested = first_existing_csv(graph.skill_dir, doc.path, registry)
                if nested and nested.resolve() in by_path:
                    graph.nested_route_prefixes.add(intent)
                    nested_doc = by_path[nested.resolve()]
                    for nested_row in nested_doc.rows:
                        surface = nested_row.get("surface", "").strip()
                        if surface:
                            graph.route_ids.add(f"{intent}/{surface}")

            frame = row.get("frame", "").strip()
            frame_path = row.get("path", "").strip()
            if frame and frame_path:
                graph.route_ids.update(f"{frame}/{suffix}" for suffix in VIRTUAL_ROUTE_SUFFIXES)
                nested = first_existing_csv(graph.skill_dir, doc.path, frame_path)
                if nested and nested.resolve() in by_path:
                    graph.nested_route_prefixes.add(frame)
                    nested_doc = by_path[nested.resolve()]
                    for nested_row in nested_doc.rows:
                        nested_intent = nested_row.get("intent", "").strip()
                        nested_registry = nested_row.get("registry_file", "").strip()
                        if nested_intent:
                            graph.route_ids.add(f"{frame}/{nested_intent}")
                            graph.nested_route_prefixes.add(f"{frame}/{nested_intent}")
                            graph.route_ids.update(
                                f"{frame}/{nested_intent}/{suffix}"
                                for suffix in VIRTUAL_ROUTE_SUFFIXES
                            )
                        if nested_intent and nested_registry:
                            child = first_existing_csv(graph.skill_dir, nested_doc.path, nested_registry)
                            if child and child.resolve() in by_path:
                                for child_row in by_path[child.resolve()].rows:
                                    surface = child_row.get("surface", "").strip()
                                    if surface:
                                        graph.route_ids.add(f"{frame}/{nested_intent}/{surface}")


def check_orphan_playbooks(graph: RoutingGraph) -> None:
    refs = graph.skill_dir / "references"
    referenced = {path.resolve() for path in graph.target_paths}
    for dirname in ("playbooks", "layers"):
        directory = refs / dirname
        if not directory.is_dir():
            continue
        for playbook in sorted(directory.glob("*.md")):
            if playbook.resolve() not in referenced:
                graph.fail(f"{graph.rel(playbook)} is not referenced by any routing CSV")


def expected_trigger_routes(skill_dir: Path, graph: RoutingGraph) -> set[str]:
    path = skill_dir / "evals" / "trigger-evals.json"
    if not path.is_file():
        return set()
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        graph.fail(f"{graph.rel(path)}: invalid JSON ({exc})")
        return set()
    routes = set()
    for query in data.get("queries", []):
        route = query.get("expected_route")
        if route:
            routes.add(str(route))
    return routes


def check_trigger_routes(graph: RoutingGraph) -> None:
    if not graph.route_ids:
        return
    for route in sorted(expected_trigger_routes(graph.skill_dir, graph)):
        if route in graph.route_ids:
            continue
        parts = route.split("/")
        prefixes = {"/".join(parts[:index]) for index in range(1, len(parts))}
        if prefixes & graph.nested_route_prefixes:
            graph.fail(f"evals/trigger-evals.json expected_route {route!r} is not in routing graph")
            continue
        # Some single-route skills use route IDs as output modes below a valid
        # first-segment route. This still catches drift in the routed seam while
        # preserving current single-skill vocabulary.
        prefix = parts[0]
        if prefix in graph.route_ids:
            continue
        graph.fail(f"evals/trigger-evals.json expected_route {route!r} is not in routing graph")


def build_routing_graph(skill_dir: Path) -> RoutingGraph:
    graph = RoutingGraph(skill_dir=skill_dir)
    refs = skill_dir / "references"
    if not refs.is_dir():
        return graph
    csv_paths = sorted(
        path
        for path in refs.rglob("*.csv")
        if path.name.endswith("-router.csv") or "intents" in path.relative_to(refs).parts
    )
    for path in csv_paths:
        doc = read_csv_document(path, graph)
        if doc is None:
            continue
        graph.csvs.append(doc)
        check_header(doc, graph)
        collect_targets(doc, graph)
    collect_route_ids(graph)
    check_orphan_playbooks(graph)
    check_trigger_routes(graph)
    return graph
