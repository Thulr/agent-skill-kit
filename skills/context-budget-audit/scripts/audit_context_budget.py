#!/usr/bin/env python3
"""Audit per-session context/token budget across local agent setups.

This finds the things that consume context on every session -- MCP servers,
skills, slash commands, subagents, and plugins -- estimates what each costs,
scans recent local history for usage evidence, and recommends what to remove or
disable to reclaim context.

It is read-only by default. It prints a decision view to stdout and writes
artifacts only when explicitly requested. It never deletes, disables, or edits a
configuration file; it only reports and recommends.

Usage tips:
  python3 audit_context_budget.py --no-write            # default decision view
  python3 audit_context_budget.py --only mcp            # one source kind
  python3 audit_context_budget.py --kinds mcp,skill     # a subset
  python3 audit_context_budget.py --json --no-write     # machine-readable
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

KINDS = ("mcp", "skill", "command", "subagent", "plugin")

# Rough conversion used for "always-on" context estimates. These are deliberate
# approximations surfaced as estimates, never as exact telemetry.
CHARS_PER_TOKEN = 4
# Average tokens for one MCP tool's JSON schema as injected into context. Real
# values vary widely; this is a planning estimate, documented as such in output.
MCP_TOKENS_PER_TOOL = 190
MCP_BASE_TOKENS = 40  # per-server framing overhead

TEXT_EXTENSIONS = {".json", ".jsonl", ".md", ".txt", ".toml", ".yaml", ".yml", ".log"}

SKIP_DIR_NAMES = {
    ".git",
    "node_modules",
    "__pycache__",
    "generated_images",
    "vendor_imports",
    ".tmp",
}

# Directories that hold definitions rather than usage traces. Scanning them would
# count a thing's own definition as "usage".
EVIDENCE_SKIP_DIR_NAMES = SKIP_DIR_NAMES | {
    "skills",
    "skills-archive",
    "agents",
    "commands",
    "plugins",
    "marketplaces",
    "cache",
    "tool-results",
    "worktrees",
    "telemetry",
}

SENSITIVE_NAME_PARTS = {
    ".env",
    "auth",
    "credential",
    "secret",
    "token",
    "cookie",
    "keychain",
    "private-key",
    "id_rsa",
    "id_ed25519",
}

# Names that are common English words / engineering actions. Plain-name mentions
# of these are treated as weak evidence only.
GENERIC_NAMES = {
    "qa",
    "tdd",
    "teach",
    "learn",
    "review",
    "research",
    "triage",
    "handoff",
    "run",
    "verify",
    "loop",
    "init",
    "diagnose",
    "simplify",
    "schedule",
}

SKIP_JSONL_TYPES = {
    "session_meta",
    "turn_context",
    "mode",
    "permission-mode",
    "file-history-snapshot",
    "summary",
    "attachment",
    "reasoning",
}


# ---------------------------------------------------------------------------
# Evidence text extraction (ported and generalized from unused-skill-audit)
# ---------------------------------------------------------------------------


def collect_strings(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(collect_strings(item))
        return out
    if isinstance(value, dict):
        out = []
        for item in value.values():
            out.extend(collect_strings(item))
        return out
    return []


def extract_tool_uses(obj: dict[str, Any]) -> list[str]:
    """Return tool names from genuine tool-use blocks in a transcript record.

    MCP usage must come from real invocations, not from tool *listings* that
    appear in system reminders. Tool-use blocks live in assistant message
    content as items with type "tool_use" and a "name".
    """
    names: list[str] = []

    def scan_content(content: Any) -> None:
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "tool_use":
                    name = item.get("name")
                    if isinstance(name, str):
                        names.append(name)

    message = obj.get("message")
    if isinstance(message, dict):
        scan_content(message.get("content"))
    payload = obj.get("payload")
    if isinstance(payload, dict):
        scan_content(payload.get("content"))
        # Codex function-call events
        if payload.get("type") in {"function_call", "tool_call"}:
            name = payload.get("name")
            if isinstance(name, str):
                names.append(name)
    return names


def useful_message_text(obj: dict[str, Any]) -> list[str]:
    if obj.get("isMeta"):
        return []
    record_type = str(obj.get("type") or "")
    if record_type in SKIP_JSONL_TYPES:
        return []

    payload = obj.get("payload")
    if isinstance(payload, dict):
        payload_type = str(payload.get("type") or "")
        role = str(payload.get("role") or "")
        if record_type == "response_item" and payload_type == "message" and role in {"user", "assistant"}:
            return collect_strings(payload.get("content"))
        if record_type == "event_msg":
            message = payload.get("message")
            return [message] if isinstance(message, str) else collect_strings(message)

    message = obj.get("message")
    if isinstance(message, dict) and str(message.get("role") or "") in {"user", "assistant"}:
        return collect_strings(message.get("content"))
    if record_type in {"user", "assistant"}:
        return collect_strings(obj.get("message"))

    return []


def read_evidence(path: Path, max_text_chars: int) -> tuple[str, list[str]]:
    """Return (joined message text, list of invoked tool names) for a file.

    .jsonl transcripts are streamed line by line so tool-use evidence is never
    missed in large session files. The text used for regex matching is capped at
    ``max_text_chars`` to bound cost, but tool invocations are always collected
    in full -- they are the precise signal for MCP usage.
    """
    if path.suffix.lower() != ".jsonl":
        return path.read_text(encoding="utf-8", errors="ignore"), []

    parts: list[str] = []
    parts_len = 0
    tool_uses: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                if parts_len < max_text_chars:
                    parts.append(line)
                    parts_len += len(line)
                continue
            if not isinstance(obj, dict):
                continue
            tool_uses.extend(extract_tool_uses(obj))
            if parts_len >= max_text_chars:
                continue
            for text in useful_message_text(obj):
                if "<local-command-stdout>" in text or "<local-command-stderr>" in text:
                    continue
                if "### Available skills" in text or "<skills_instructions>" in text:
                    continue
                parts.append(text)
                parts_len += len(text)
    return "\n".join(parts), tool_uses


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Evidence:
    strong_files: int = 0
    strong_matches: int = 0
    weak_files: int = 0
    weak_matches: int = 0
    last_seen: float | None = None
    examples: list[str] = field(default_factory=list)

    @property
    def has_strong(self) -> bool:
        return self.strong_files > 0

    @property
    def has_weak(self) -> bool:
        return self.weak_files > 0

    @property
    def total_files(self) -> int:
        return self.strong_files + self.weak_files

    @property
    def total_matches(self) -> int:
        return self.strong_matches + self.weak_matches


@dataclass
class ContextItem:
    kind: str
    name: str
    agent: str  # claude | codex | agents | pi | pi-agent
    scope: str  # active | enabled | disabled | project | system | cache | archive
    location: str = ""  # display path or config file (home-relative)
    description: str = ""
    detail: dict[str, Any] = field(default_factory=dict)
    est_tokens: int | None = None  # estimated always-on context cost
    est_basis: str = ""  # how est_tokens was derived (for honesty in output)
    in_repo: bool = False
    duplicate_count: int = 1
    sha1: str = ""
    evidence: Evidence = field(default_factory=Evidence)
    action: str = ""
    confidence: str = ""
    reasons: list[str] = field(default_factory=list)

    @property
    def key(self) -> str:
        return f"{self.kind}:{self.name}:{self.agent}"


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def expand(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def iso_from_ts(timestamp: float | None) -> str:
    if not timestamp:
        return ""
    return dt.datetime.fromtimestamp(timestamp, tz=dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def rel_home(path: Path, home: Path) -> str:
    try:
        return "~/" + str(Path(path).resolve().relative_to(home.resolve()))
    except (ValueError, OSError):
        return str(path)


def path_agent(path: Path, home: Path) -> str:
    """Infer which agent produced an evidence file from its root directory."""
    try:
        parts = Path(path).resolve().relative_to(home.resolve()).parts
    except (ValueError, OSError):
        return "unknown"
    if not parts:
        return "unknown"
    head = parts[0]
    if head == ".claude":
        return "claude"
    if head == ".codex":
        return "codex"
    if head == ".agents":
        return "agents"
    if head == ".pi":
        return "pi-agent" if len(parts) > 1 and parts[1] == "agent" else "pi"
    return "unknown"


def tokens_from_chars(chars: int) -> int:
    return math.ceil(chars / CHARS_PER_TOKEN) if chars else 0


def should_skip_sensitive(path: Path) -> bool:
    lowered = str(path).lower()
    return any(part in lowered for part in SENSITIVE_NAME_PARTS)


def should_skip_dir(path: Path, skip_names: set[str]) -> bool:
    return any(part in skip_names for part in path.parts)


def parse_frontmatter(md_file: Path) -> tuple[str, str]:
    """Return (name, description) from YAML frontmatter; fall back gracefully.

    Handles inline values (``description: text``) and YAML block scalars
    (``description: >`` / ``>-`` / ``|`` and an empty value), where the real
    text lives on the following indented lines. Missing the block-scalar case
    silently under-counts a skill's always-on token cost.
    """
    name = md_file.stem
    description = ""
    try:
        lines = md_file.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return name, description
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines):
            line = lines[i]
            if line.strip() == "---":
                break
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip("'\"") or name
                i += 1
            elif line.startswith("description:"):
                inline = line.split(":", 1)[1].strip()
                if inline and inline not in {">", ">-", ">+", "|", "|-", "|+"}:
                    description = inline.strip("'\"")
                    i += 1
                else:
                    # Block scalar: gather following more-indented (or blank) lines.
                    block: list[str] = []
                    i += 1
                    while i < len(lines):
                        nxt = lines[i]
                        if nxt.strip() == "---":
                            break
                        if nxt.strip() == "":
                            block.append("")
                            i += 1
                            continue
                        if nxt[:1] in (" ", "\t"):
                            block.append(nxt.strip())
                            i += 1
                            continue
                        break  # back to a top-level key
                    description = " ".join(part for part in block if part).strip()
            else:
                i += 1
        if description:
            return name, description
    # No frontmatter description: use the first non-heading prose line.
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith(("---", "#")):
            description = stripped
            break
    return name, description


def sha1_file(path: Path) -> str:
    h = hashlib.sha1()
    try:
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                h.update(chunk)
    except OSError:
        return ""
    return h.hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def repo_skill_names(repo_root: Path) -> set[str]:
    names: set[str] = set()
    skills_dir = repo_root / "skills"
    if not skills_dir.exists():
        return names
    for skill_file in skills_dir.glob("*/SKILL.md"):
        name, _ = parse_frontmatter(skill_file)
        names.add(name)
    return names


# ---------------------------------------------------------------------------
# Collectors -- one per context source kind
# ---------------------------------------------------------------------------


def collect_skills(home: Path, repo_root: Path) -> tuple[list[ContextItem], list[str]]:
    roots = [
        ("claude", home / ".claude" / "skills"),
        ("agents", home / ".agents" / "skills"),
        ("codex", home / ".codex" / "skills"),
        ("pi-agent", home / ".pi" / "agent" / "skills"),
        ("pi", home / ".pi" / "skills"),
    ]
    repo_names = repo_skill_names(repo_root)
    items: list[ContextItem] = []
    missing: list[str] = []
    for agent, root in roots:
        if not root.exists():
            missing.append(rel_home(root, home))
            continue
        for skill_file in root.rglob("SKILL.md"):
            if should_skip_dir(skill_file, {".git", "node_modules", "__pycache__"}):
                continue
            scope = "system" if ".system" in skill_file.parts else "active"
            name, description = parse_frontmatter(skill_file)
            items.append(
                ContextItem(
                    kind="skill",
                    name=name,
                    agent=agent,
                    scope=scope,
                    location=rel_home(skill_file.parent, home),
                    description=description,
                    est_tokens=tokens_from_chars(len(description)),
                    est_basis="SKILL.md description length",
                    in_repo=name in repo_names,
                    sha1=sha1_file(skill_file),
                    detail={"dir_name": skill_file.parent.name},
                )
            )
    counts: dict[str, int] = {}
    for item in items:
        if item.scope == "active":
            counts[item.name] = counts.get(item.name, 0) + 1
    for item in items:
        item.duplicate_count = counts.get(item.name, 1)
    return items, missing


def _codex_mcp_servers(config_path: Path) -> dict[str, dict[str, str]]:
    """Best-effort parse of [mcp_servers.NAME] tables without a TOML dependency."""
    servers: dict[str, dict[str, str]] = {}
    try:
        text = config_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return servers
    current: str | None = None
    header = re.compile(r"^\s*\[mcp_servers\.([^.\]]+)\]\s*$")
    subheader = re.compile(r"^\s*\[mcp_servers\.([^.\]]+)\.[^\]]+\]\s*$")
    kv = re.compile(r"^\s*(command|url)\s*=\s*(.+?)\s*$")
    for line in text.splitlines():
        m = header.match(line)
        if m:
            current = m.group(1)
            servers.setdefault(current, {})
            continue
        if subheader.match(line):
            current = None  # inside e.g. [mcp_servers.x.env]; ignore kv here
            continue
        if line.lstrip().startswith("["):
            current = None
            continue
        if current:
            kvm = kv.match(line)
            if kvm:
                servers[current][kvm.group(1)] = kvm.group(2).strip().strip("\"'")
    return servers


def collect_mcp_servers(home: Path) -> tuple[list[ContextItem], list[str]]:
    items: list[ContextItem] = []
    missing: list[str] = []

    claude_cfg = home / ".claude.json"
    data = load_json(claude_cfg)
    if data is None:
        missing.append(rel_home(claude_cfg, home))
    elif isinstance(data, dict):
        for name in (data.get("mcpServers") or {}):
            items.append(
                ContextItem(
                    kind="mcp",
                    name=name,
                    agent="claude",
                    scope="active",
                    location=rel_home(claude_cfg, home),
                    detail={"config_scope": "global"},
                )
            )
        seen_proj: set[str] = {i.name for i in items}
        for proj_path, proj in (data.get("projects") or {}).items():
            if not isinstance(proj, dict):
                continue
            for name in (proj.get("mcpServers") or {}):
                if name in seen_proj:
                    # also defined globally; record the project scope as detail
                    continue
                items.append(
                    ContextItem(
                        kind="mcp",
                        name=name,
                        agent="claude",
                        scope="project",
                        location=rel_home(claude_cfg, home),
                        detail={"config_scope": "project", "project": proj_path},
                    )
                )
                seen_proj.add(name)

    codex_cfg = home / ".codex" / "config.toml"
    if not codex_cfg.exists():
        missing.append(rel_home(codex_cfg, home))
    else:
        for name, info in _codex_mcp_servers(codex_cfg).items():
            items.append(
                ContextItem(
                    kind="mcp",
                    name=name,
                    agent="codex",
                    scope="active",
                    location=rel_home(codex_cfg, home),
                    detail={"config_scope": "global", **info},
                )
            )
    return items, missing


def collect_commands(home: Path) -> tuple[list[ContextItem], list[str]]:
    roots = [
        ("claude", home / ".claude" / "commands"),
        ("codex", home / ".codex" / "prompts"),
    ]
    items: list[ContextItem] = []
    missing: list[str] = []
    for agent, root in roots:
        if not root.exists():
            missing.append(rel_home(root, home))
            continue
        # rglob (not glob): namespaced commands live in subdirs, e.g.
        # ~/.claude/commands/team/deploy.md — they still cost command surface.
        for md in sorted(root.rglob("*.md")):
            name, description = parse_frontmatter(md)
            # The command's listed cost is roughly its name + description line.
            items.append(
                ContextItem(
                    kind="command",
                    name=str(md.relative_to(root).with_suffix("")),
                    agent=agent,
                    scope="active",
                    location=rel_home(md, home),
                    description=description,
                    est_tokens=tokens_from_chars(len(name) + len(description)),
                    est_basis="command name + description",
                )
            )
    return items, missing


def collect_subagents(home: Path) -> tuple[list[ContextItem], list[str]]:
    roots = [
        ("claude", home / ".claude" / "agents"),
        ("codex", home / ".codex" / "agents"),
    ]
    items: list[ContextItem] = []
    missing: list[str] = []
    for agent, root in roots:
        if not root.exists():
            missing.append(rel_home(root, home))
            continue
        for md in sorted(root.rglob("*.md")):
            if should_skip_dir(md, {".git", "node_modules"}):
                continue
            name, description = parse_frontmatter(md)
            items.append(
                ContextItem(
                    kind="subagent",
                    name=name,
                    agent=agent,
                    scope="active",
                    location=rel_home(md, home),
                    description=description,
                    est_tokens=tokens_from_chars(len(name) + len(description)),
                    est_basis="subagent name + description",
                )
            )
    return items, missing


def _plugin_component_tokens(install_path: Path) -> tuple[int, dict[str, int]]:
    """Estimate always-on tokens a plugin contributes from its bundled parts."""
    counts = {"skills": 0, "commands": 0, "agents": 0}
    chars = 0
    if not install_path.exists():
        return 0, counts
    for skill_file in install_path.rglob("SKILL.md"):
        _, desc = parse_frontmatter(skill_file)
        chars += len(desc)
        counts["skills"] += 1
    for sub in ("commands", "agents"):
        d = install_path / sub
        if d.exists():
            for md in d.rglob("*.md"):
                _, desc = parse_frontmatter(md)
                chars += len(desc)
                counts[sub] += 1
    return tokens_from_chars(chars), counts


def collect_plugins(home: Path) -> tuple[list[ContextItem], list[str]]:
    items: list[ContextItem] = []
    missing: list[str] = []
    installed_path = home / ".claude" / "plugins" / "installed_plugins.json"
    settings = load_json(home / ".claude" / "settings.json") or {}
    enabled_map = settings.get("enabledPlugins") if isinstance(settings, dict) else {}
    enabled_map = enabled_map if isinstance(enabled_map, dict) else {}

    data = load_json(installed_path)
    if data is None:
        missing.append(rel_home(installed_path, home))
        return items, missing
    plugins = data.get("plugins") if isinstance(data, dict) else None
    if not isinstance(plugins, dict):
        return items, missing

    for full_name, installs in plugins.items():
        if not isinstance(installs, list) or not installs:
            continue
        # Prefer the user-scoped install; else the most recently updated.
        install = next((i for i in installs if i.get("scope") == "user"), None) or installs[-1]
        install_path = Path(install.get("installPath", ""))
        enabled = bool(enabled_map.get(full_name, False))
        marketplace = full_name.split("@", 1)[1] if "@" in full_name else ""
        short = full_name.split("@", 1)[0]
        est_tokens, comp_counts = (_plugin_component_tokens(install_path) if enabled else (0, {}))
        items.append(
            ContextItem(
                kind="plugin",
                name=full_name,
                agent="claude",
                scope="enabled" if enabled else "disabled",
                location=rel_home(install_path, home) if install_path else "",
                est_tokens=est_tokens if enabled else 0,
                est_basis="bundled component descriptions" if enabled else "disabled: no context cost",
                detail={
                    "short": short,
                    "marketplace": marketplace,
                    "version": install.get("version", ""),
                    "install_scope": install.get("scope", ""),
                    "last_updated": install.get("lastUpdated", ""),
                    "components": comp_counts,
                },
            )
        )
    return items, missing


# ---------------------------------------------------------------------------
# Evidence scanning
# ---------------------------------------------------------------------------


def default_evidence_roots(home: Path) -> list[Path]:
    return [
        home / ".claude" / "history.jsonl",
        home / ".claude" / "projects",
        home / ".claude" / "tasks",
        home / ".claude" / "jobs",
        home / ".claude" / "plans",
        home / ".claude" / "todos",
        home / ".codex" / "history.jsonl",
        home / ".codex" / "session_index.jsonl",
        home / ".codex" / "sessions",
        home / ".codex" / "log",
        home / ".pi" / "agent" / "run-history.jsonl",
        home / ".pi" / "agent" / "sessions",
    ]


def iter_evidence_files(roots: list[Path], max_files: int, evidence_days: int) -> tuple[list[Path], list[str]]:
    selected: list[tuple[float, Path]] = []
    skipped: list[str] = []
    older_count = 0
    cutoff = None if evidence_days <= 0 else dt.datetime.now().timestamp() - (evidence_days * 86400)
    for root in roots:
        if not root.exists():
            continue
        iter_paths = [root] if root.is_file() else root.rglob("*")
        for path in iter_paths:
            if not path.is_file():
                continue
            if path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            if should_skip_dir(path, EVIDENCE_SKIP_DIR_NAMES):
                continue
            if should_skip_sensitive(path):
                skipped.append(f"sensitive name skipped: {path}")
                continue
            try:
                mtime = path.stat().st_mtime
            except OSError as exc:
                skipped.append(f"unreadable stat: {path} ({exc})")
                continue
            if cutoff is not None and mtime < cutoff:
                older_count += 1
                continue
            selected.append((mtime, path))
    if older_count:
        skipped.append(f"older than {evidence_days} days skipped: {older_count} files")
    selected.sort(key=lambda item: item[0], reverse=True)
    if max_files >= 0 and len(selected) > max_files:
        skipped.append(f"max evidence files reached: scanned newest {max_files} of {len(selected)}")
        selected = selected[:max_files]
    return [path for _, path in selected], skipped


def name_alternation(names: Iterable[str]) -> str:
    return "|".join(re.escape(name) for name in sorted(set(names), key=len, reverse=True))


def build_matchers(items: list[ContextItem]) -> dict[str, Any]:
    """Compile per-kind regexes once, keyed by kind."""
    by_kind: dict[str, set[str]] = {k: set() for k in KINDS}
    for item in items:
        by_kind[item.kind].add(item.name)
        if item.kind == "plugin":
            short = item.detail.get("short")
            if short:
                by_kind["plugin"].add(short)

    matchers: dict[str, Any] = {}

    # Skills: path refs, activation verbs, "<name> skill", skill: "name".
    if by_kind["skill"]:
        alt = name_alternation(by_kind["skill"])
        weak_names = {n for n in by_kind["skill"] if n not in GENERIC_NAMES and len(n) >= 7}
        matchers["skill"] = {
            "strong": [
                re.compile(rf"(?:\$|@|/)(?P<name>{alt})\b", re.IGNORECASE),
                re.compile(
                    rf"\b(?:use|using|invoke|invoking|load|loading|activate|trigger|run|call|apply)\s+(?:the\s+)?(?P<name>{alt})(?:\s+skill)?\b",
                    re.IGNORECASE,
                ),
                re.compile(rf"\b(?P<name>{alt})\s+skill\b", re.IGNORECASE),
                re.compile(rf"\bskill(?:[_ -]?name)?[\"']?\s*[:=]\s*[\"'](?P<name>{alt})[\"']", re.IGNORECASE),
                re.compile(rf"(?:^|[/\\])skills[/\\](?:\.system[/\\])?(?P<name>{alt})(?=[/\\])", re.IGNORECASE),
            ],
            "weak": re.compile(rf"(?<![a-z0-9-])(?P<name>{name_alternation(weak_names)})(?![a-z0-9-])", re.IGNORECASE)
            if weak_names
            else None,
        }

    # Commands: /name invocation, <command-name> tags.
    if by_kind["command"]:
        alt = name_alternation(by_kind["command"])
        matchers["command"] = {
            "strong": [
                re.compile(rf"(?<![\w./-])/(?P<name>{alt})\b"),
                re.compile(rf"command[_-]?name[\"'>]?\s*[:=>]?\s*[\"'/]*(?P<name>{alt})\b", re.IGNORECASE),
            ],
            "weak": None,
        }

    # Subagents: subagent_type / agentType fields, "<name> agent".
    if by_kind["subagent"]:
        alt = name_alternation(by_kind["subagent"])
        matchers["subagent"] = {
            "strong": [
                re.compile(rf"(?:subagent_type|agentType|agent_type|subagent)[\"']?\s*[:=]\s*[\"'](?P<name>{alt})[\"']", re.IGNORECASE),
                re.compile(rf"\b(?P<name>{alt})\s+(?:sub)?agent\b", re.IGNORECASE),
                re.compile(rf"(?:\$|@)(?P<name>{alt})\b"),
            ],
            "weak": None,
        }

    # Plugins: short name mentions are weak; component usage is handled via the
    # other kinds. We keep a weak plain-name matcher only.
    if by_kind["plugin"]:
        weak_plugin = {n for n in by_kind["plugin"] if len(n) >= 5 and n not in GENERIC_NAMES}
        matchers["plugin"] = {
            "strong": [],
            "weak": re.compile(rf"(?<![a-z0-9-])(?P<name>{name_alternation(weak_plugin)})(?![a-z0-9-])", re.IGNORECASE)
            if weak_plugin
            else None,
        }

    # MCP tool-call pattern, applied to invoked tool names only.
    matchers["_mcp_tool"] = re.compile(r"^mcp__(?P<server>[A-Za-z0-9_.-]+?)__(?P<tool>[A-Za-z0-9_.-]+)$")
    return matchers


def scan_evidence(
    items: list[ContextItem],
    evidence_files: list[Path],
    home: Path,
    max_file_bytes: int,
) -> list[str]:
    skipped: list[str] = []
    matchers = build_matchers(items)

    # Index items for fast attribution.
    ev: dict[str, Evidence] = {item.key: Evidence() for item in items}
    by_kind_name: dict[tuple[str, str], list[ContextItem]] = {}
    for item in items:
        by_kind_name.setdefault((item.kind, item.name.lower()), []).append(item)
    plugin_by_short: dict[str, list[ContextItem]] = {}
    for item in items:
        if item.kind == "plugin":
            short = str(item.detail.get("short", "")).lower()
            if short:
                plugin_by_short.setdefault(short, []).append(item)
    mcp_servers: dict[str, list[ContextItem]] = {}
    for item in items:
        if item.kind == "mcp":
            mcp_servers.setdefault(item.name.lower(), []).append(item)
    mcp_tool_re = matchers["_mcp_tool"]

    def record(targets: list[ContextItem], strong: bool, count: int, mtime: float, ref: str) -> None:
        for item in targets:
            e = ev[item.key]
            if strong:
                e.strong_files += 1
                e.strong_matches += min(count, 50)
            else:
                e.weak_files += 1
                e.weak_matches += min(count, 50)
            e.last_seen = max(e.last_seen or 0.0, mtime)
            if len(e.examples) < 4:
                e.examples.append(ref)

    for path in evidence_files:
        try:
            stat = path.stat()
        except OSError as exc:
            skipped.append(f"unreadable stat: {path} ({exc})")
            continue
        is_jsonl = path.suffix.lower() == ".jsonl"
        # .jsonl transcripts are streamed and carry the precise tool-use signal,
        # so the byte cap applies only to whole-file reads (configs, docs, logs).
        if not is_jsonl and stat.st_size > max_file_bytes:
            skipped.append(f"large file skipped: {path} ({stat.st_size} bytes)")
            continue
        try:
            text, tool_uses = read_evidence(path, max_text_chars=max_file_bytes)
        except OSError as exc:
            skipped.append(f"unreadable: {path} ({exc})")
            continue

        mtime = stat.st_mtime
        ref = rel_home(path, home)
        file_agent = path_agent(path, home)
        scan_text = f"{path}\n{text}"

        # --- MCP: from genuine tool invocations only ---
        server_tool_counts: dict[str, dict[str, int]] = {}
        for tool_name in tool_uses:
            m = mcp_tool_re.match(tool_name)
            if not m:
                continue
            server = m.group("server").lower()
            tool = m.group("tool")
            server_tool_counts.setdefault(server, {})
            server_tool_counts[server][tool] = server_tool_counts[server].get(tool, 0) + 1
        for server, tools in server_tool_counts.items():
            candidates = mcp_servers.get(server)
            if not candidates:
                continue
            # Attribute to the server configured for the agent that produced this
            # transcript; if no agent match, credit every same-named server.
            targets = [c for c in candidates if c.agent == file_agent] or candidates
            for item in targets:
                observed = item.detail.setdefault("observed_tools", {})
                for tool, c in tools.items():
                    observed[tool] = observed.get(tool, 0) + c
            record(targets, strong=True, count=sum(tools.values()), mtime=mtime, ref=ref)

        # --- Skill / command / subagent strong + weak ---
        for kind in ("skill", "command", "subagent"):
            m = matchers.get(kind)
            if not m:
                continue
            strong_counts: dict[str, int] = {}
            for pattern in m["strong"]:
                for match in pattern.finditer(scan_text):
                    nm = match.group("name").lower()
                    strong_counts[nm] = strong_counts.get(nm, 0) + 1
            for nm, c in strong_counts.items():
                targets = by_kind_name.get((kind, nm))
                if targets:
                    record(targets, strong=True, count=c, mtime=mtime, ref=ref)
            weak = m.get("weak")
            if weak:
                weak_counts: dict[str, int] = {}
                for match in weak.finditer(text):
                    nm = match.group("name").lower()
                    if nm not in strong_counts:
                        weak_counts[nm] = weak_counts.get(nm, 0) + 1
                for nm, c in weak_counts.items():
                    targets = by_kind_name.get((kind, nm))
                    if targets:
                        record(targets, strong=False, count=c, mtime=mtime, ref=ref)

        # --- Plugin weak by short name ---
        pm = matchers.get("plugin")
        if pm and pm.get("weak"):
            seen: dict[str, int] = {}
            for match in pm["weak"].finditer(text):
                nm = match.group("name").lower()
                seen[nm] = seen.get(nm, 0) + 1
            for nm, c in seen.items():
                targets = plugin_by_short.get(nm)
                if targets:
                    record(targets, strong=False, count=c, mtime=mtime, ref=ref)

    for item in items:
        item.evidence = ev.get(item.key, Evidence())
        # Refine MCP token estimate from observed tool count.
        if item.kind == "mcp":
            observed = item.detail.get("observed_tools") or {}
            if observed:
                item.est_tokens = MCP_BASE_TOKENS + len(observed) * MCP_TOKENS_PER_TOOL
                item.est_basis = f">={len(observed)} tools used x ~{MCP_TOKENS_PER_TOOL} tok (lower bound)"
            else:
                item.est_tokens = None
                item.est_basis = "tool schemas not observed; cost unknown"

    return skipped


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


def classify(items: list[ContextItem]) -> None:
    for item in items:
        reasons: list[str] = []
        e = item.evidence

        if item.scope == "system":
            item.action, item.confidence = "keep-managed-system", "high"
            reasons.append("system or built-in; not a normal prune target")
        elif item.scope == "cache":
            item.action, item.confidence = "ignore-managed-cache", "high"
            reasons.append("managed cache; clean only through the owning tool")
        elif item.kind == "plugin" and item.scope == "disabled":
            item.action, item.confidence = "disabled-no-cost", "high"
            reasons.append("installed but not enabled; costs no session context")
        elif e.has_strong:
            item.action, item.confidence = "keep-active", "medium"
            reasons.append("strong usage evidence in recent local history")
            if item.kind == "skill" and item.duplicate_count > 1:
                item.action = "consolidate-duplicates"
                reasons.append("multiple active copies share this skill name")
        elif e.has_weak:
            item.action, item.confidence = "review-weak-evidence", "low"
            reasons.append("only weak or plain-name evidence found")
        else:
            # No usage evidence: this is reclaimable context.
            item.action, item.confidence = "reclaim-unused", "medium"
            reasons.append("loaded into context but no usage evidence in the scan window")
            if item.kind == "skill" and item.in_repo:
                reasons.append("a copy exists in the current repo")
            if item.kind == "mcp" and not (item.detail.get("observed_tools")):
                reasons.append("no MCP tool calls observed; configured but idle")

        if item.name in GENERIC_NAMES:
            reasons.append("generic name; weak evidence is discounted")
            if item.action == "review-weak-evidence":
                item.confidence = "low"
        item.reasons = reasons


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def plural(count: int, singular: str, plural_value: str | None = None) -> str:
    return singular if count == 1 else (plural_value or f"{singular}s")


def cost_str(item: ContextItem) -> str:
    if item.est_tokens is None:
        return "~? tok"
    return f"~{item.est_tokens} tok"


def evidence_str(item: ContextItem) -> str:
    e = item.evidence
    parts: list[str] = []
    if e.strong_files:
        parts.append(f"strong {e.strong_files}f/{e.strong_matches}m")
    if e.weak_files:
        parts.append(f"weak {e.weak_files}f/{e.weak_matches}m")
    if e.last_seen:
        parts.append(f"last {iso_from_ts(e.last_seen)[:10]}")
    if item.kind == "mcp":
        observed = item.detail.get("observed_tools") or {}
        if observed:
            parts.append(f"{len(observed)} tools used")
    return "; ".join(parts) or "none"


def item_line(item: ContextItem, home: Path) -> str:
    bits = [f"  - [{item.agent}] {item.name}", cost_str(item)]
    detail = []
    if item.kind == "mcp" and item.detail.get("config_scope") == "project":
        detail.append("project-scoped")
    if item.kind == "plugin":
        detail.append(f"v{item.detail.get('version','?')}")
    if item.kind == "skill" and item.in_repo:
        detail.append("in-repo")
    extra = f" ({', '.join(detail)})" if detail else ""
    ev = evidence_str(item)
    return f"{bits[0]} — {bits[1]}{extra} — evidence: {ev}"


def make_decision_view(
    items: list[ContextItem],
    args: argparse.Namespace,
    home: Path,
    repo_root: Path,
    evidence_files: list[Path],
    skipped: list[str],
    missing: dict[str, list[str]],
) -> str:
    by_action: dict[str, list[ContextItem]] = {}
    for item in items:
        by_action.setdefault(item.action, []).append(item)

    reclaim = sorted(
        by_action.get("reclaim-unused", []),
        key=lambda i: (i.est_tokens is None, -(i.est_tokens or 0), i.kind, i.name),
    )
    reclaim_known = [i for i in reclaim if i.est_tokens]
    reclaim_tokens = sum(i.est_tokens or 0 for i in reclaim)
    unknown_reclaim = [i for i in reclaim if i.est_tokens is None]

    kind_counts: dict[str, int] = {}
    for item in items:
        kind_counts[item.kind] = kind_counts.get(item.kind, 0) + 1

    lines: list[str] = []
    lines.append("Context Budget Audit — Decision View")
    lines.append("")
    lines.append(f"Scope: home={home}")
    lines.append(
        "Inventory: "
        + ", ".join(f"{kind_counts.get(k,0)} {k}" for k in KINDS)
    )
    lines.append(
        f"Evidence: days={args.evidence_days} files={len(evidence_files)} skipped={len(skipped)}"
    )
    idle_mcp = [i for i in reclaim if i.kind == "mcp"]
    lines.append(
        f"Reclaimable now: ~{reclaim_tokens} measurable tokens across "
        f"{len(reclaim_known)} unused {plural(len(reclaim_known),'item')}."
    )
    if idle_mcp:
        lines.append(
            f"PLUS {len(idle_mcp)} idle MCP {plural(len(idle_mcp),'server')} with no observed tool calls — "
            "cost is unknown but MCP tool schemas are usually the single largest context drain. Verify these first."
        )
    lines.append("Nothing was deleted, disabled, or edited.")
    lines.append("")

    # Context footprint: total always-on cost across ALL items, not just unused.
    # This is the number that drives "descriptions compressed to save space"
    # warnings -- aggregate load, regardless of whether each item is used.
    foot: dict[str, list[int]] = {}  # kind -> [count, known_tokens, unknown]
    for item in items:
        row = foot.setdefault(item.kind, [0, 0, 0])
        row[0] += 1
        if item.est_tokens:
            row[1] += item.est_tokens
        else:
            row[2] += 1
    total_tokens = sum(r[1] for r in foot.values())
    total_unknown = sum(r[2] for r in foot.values())
    lines.append("== Context footprint (always-on, ALL items) ==")
    unk = f" (+{total_unknown} unknown)" if total_unknown else ""
    lines.append(f"  Total: ~{total_tokens} measurable tokens across {len(items)} items{unk}")
    ordered = sorted(foot.items(), key=lambda kv: -kv[1][1])
    for idx, (kind, (count, known, unknown)) in enumerate(ordered):
        u = f" +{unknown} unknown" if unknown else ""
        note = "  <- largest; aggregate count, not non-use, drives compression warnings" if idx == 0 and known else ""
        lines.append(f"  {kind:<8} {count:>3} {plural(count,'item'):<6} ~{known} tok{u}{note}")
    heaviest = sorted((i for i in items if i.est_tokens), key=lambda i: -(i.est_tokens or 0))[:6]
    if heaviest:
        lines.append(
            "  Heaviest: "
            + ", ".join(f"{i.name} ~{i.est_tokens}" for i in heaviest)
        )
    lines.append("")

    # Reclaim section, biggest levers first, grouped by kind for readability.
    lines.append("== Reclaim unused (loaded into context, no usage evidence) ==")
    if not reclaim:
        lines.append("  None — everything loaded shows usage evidence.")
    else:
        for kind in KINDS:
            group = [i for i in reclaim if i.kind == kind]
            if not group:
                continue
            known = [i for i in group if i.est_tokens]
            sub = sum(i.est_tokens or 0 for i in known)
            if len(known) == len(group):
                tag = f"~{sub} tok"
            elif known:
                tag = f"~{sub} tok known + {len(group) - len(known)} unknown"
            else:
                tag = "cost unknown"
            lines.append(f" {kind} ({tag}, {len(group)} {plural(len(group),'item')}):")
            for item in group:
                lines.append(item_line(item, home))
    lines.append("")

    def section(title: str, action: str) -> None:
        rows = sorted(by_action.get(action, []), key=lambda i: (i.kind, i.name))
        lines.append(title)
        if not rows:
            lines.append("  None.")
        for item in rows:
            lines.append(item_line(item, home))
        lines.append("")

    section("== Review weak evidence before removing ==", "review-weak-evidence")
    section("== Consolidate duplicate skills ==", "consolidate-duplicates")
    section("== Keep (usage evidence found) ==", "keep-active")

    disabled = by_action.get("disabled-no-cost", [])
    managed = by_action.get("keep-managed-system", []) + by_action.get("ignore-managed-cache", [])
    lines.append("== No context cost / managed ==")
    lines.append(
        f"  {len(disabled)} disabled plugin(s) cost no context; "
        f"{len(managed)} managed/system item(s) excluded from prune."
    )
    lines.append("")

    # Caveats
    caveats: list[str] = []
    missing_flat = [f"{k}: {', '.join(v)}" for k, v in missing.items() if v]
    if missing_flat:
        caveats.append("absent sources -> " + " | ".join(missing_flat[:8]))
    if skipped:
        caveats.append(f"{len(skipped)} evidence sources skipped (size/sensitive/window)")
    caveats.append("token figures are estimates, not exact context measurements")
    caveats.append("MCP cost counts only tools actually invoked, so it understates a server's full schema footprint; idle servers show unknown cost but are still flagged")
    caveats.append('"no evidence" means none in the scan window, not proof of lifetime non-use')
    caveats.append("removing MCP servers / plugins edits config; this tool only recommends, it does not edit")
    lines.append("== Caveats ==")
    for c in caveats:
        lines.append(f"  - {c}")
    lines.append("")
    lines.append("Next: name the items to remove (e.g. 'remove mcp memdb, disable plugin superpowers, move skill foo into repo').")
    return "\n".join(lines)


def items_to_json(items: list[ContextItem]) -> list[dict[str, Any]]:
    rows = []
    for item in sorted(items, key=lambda i: (i.action, i.kind, i.name)):
        rows.append(
            {
                "kind": item.kind,
                "name": item.name,
                "agent": item.agent,
                "scope": item.scope,
                "location": item.location,
                "description": item.description,
                "est_tokens": item.est_tokens,
                "est_basis": item.est_basis,
                "in_repo": item.in_repo,
                "duplicate_count": item.duplicate_count,
                "detail": item.detail,
                "evidence": {
                    "strong_files": item.evidence.strong_files,
                    "strong_matches": item.evidence.strong_matches,
                    "weak_files": item.evidence.weak_files,
                    "weak_matches": item.evidence.weak_matches,
                    "last_used_at": iso_from_ts(item.evidence.last_seen),
                    "examples": item.evidence.examples,
                },
                "action": item.action,
                "confidence": item.confidence,
                "reasons": item.reasons,
            }
        )
    return rows


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_kinds(value: str) -> list[str]:
    if not value or value.strip().lower() == "all":
        return list(KINDS)
    requested = [k.strip().lower() for k in value.split(",") if k.strip()]
    bad = [k for k in requested if k not in KINDS]
    if bad:
        raise SystemExit(f"Unknown kind(s): {', '.join(bad)}. Choose from: {', '.join(KINDS)}.")
    return requested


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit per-session context/token budget (MCP servers, skills, commands, subagents, plugins)."
    )
    parser.add_argument("--home", default=str(Path.home()), help="Home directory containing .claude/.codex/.agents/.pi.")
    parser.add_argument("--repo-root", default=str(Path.cwd()), help="Repo root used to detect skills already preserved.")
    parser.add_argument("--kinds", default="all", help=f"Comma list of source kinds to audit. Choices: {', '.join(KINDS)}, or 'all'.")
    parser.add_argument("--only", default="", help="Shorthand for --kinds with a single kind.")
    parser.add_argument("--evidence-days", type=int, default=90, help="Evidence mtime window in days. Use 0 for all history.")
    parser.add_argument("--max-evidence-files", type=int, default=1500, help="Max newest evidence files to scan. Use -1 for no cap.")
    parser.add_argument("--max-file-bytes", type=int, default=128 * 1024, help="Max bytes of text per evidence file used for regex matching. MCP tool-use detection streams every line regardless.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of the decision view.")
    parser.add_argument("--markdown-output", default="", help="Write a Markdown report to this exact path.")
    parser.add_argument("--json-output", default="", help="Write a JSON report to this exact path.")
    parser.add_argument("--no-write", action="store_true", help="Do not write any files (default unless an output path is given).")
    return parser.parse_args(argv)


COLLECTORS = {
    "mcp": lambda home, repo: collect_mcp_servers(home),
    "skill": lambda home, repo: collect_skills(home, repo),
    "command": lambda home, repo: collect_commands(home),
    "subagent": lambda home, repo: collect_subagents(home),
    "plugin": lambda home, repo: collect_plugins(home),
}


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    home = expand(args.home)
    repo_root = expand(args.repo_root)
    kinds = parse_kinds(args.only) if args.only else parse_kinds(args.kinds)

    items: list[ContextItem] = []
    missing: dict[str, list[str]] = {}
    for kind in kinds:
        collected, miss = COLLECTORS[kind](home, repo_root)
        items.extend(collected)
        if miss:
            missing[kind] = miss

    evidence_files, skipped = iter_evidence_files(
        default_evidence_roots(home), args.max_evidence_files, args.evidence_days
    )
    skipped.extend(scan_evidence(items, evidence_files, home, args.max_file_bytes))
    classify(items)

    payload = {
        "schema": "context-budget-audit.v1",
        "generated_at": dt.datetime.now(tz=dt.timezone.utc).astimezone().isoformat(timespec="seconds"),
        "home": str(home),
        "repo_root": str(repo_root),
        "kinds": kinds,
        "evidence_days": args.evidence_days,
        "evidence_files_scanned": len(evidence_files),
        "evidence_files_skipped": len(skipped),
        "missing_sources": missing,
        "skipped": skipped,
        "items": items_to_json(items),
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(make_decision_view(items, args, home, repo_root, evidence_files, skipped, missing))

    if not args.no_write:
        if args.json_output:
            expand(args.json_output).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            print(f"\nJSON artifact: {expand(args.json_output)}")
        if args.markdown_output:
            # Markdown report is the decision view wrapped with a heading.
            md = "# Context Budget Audit\n\n```\n" + make_decision_view(
                items, args, home, repo_root, evidence_files, skipped, missing
            ) + "\n```\n"
            expand(args.markdown_output).write_text(md, encoding="utf-8")
            print(f"Markdown artifact: {expand(args.markdown_output)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
