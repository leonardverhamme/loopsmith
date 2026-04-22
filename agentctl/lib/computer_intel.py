from __future__ import annotations

import os
import re
from collections import deque
from pathlib import Path
from typing import Any

from .common import load_json, print_json, save_json, utc_now
from .config_layers import effective_config, trusted_projects
from .paths import COMPUTER_GRAPH_PATH
from .repo_intel import repo_intel_status


SCHEMA_VERSION = 1
ROOT_SKIP_NAMES = {
    "$Recycle.Bin",
    "Config.Msi",
    "MSOCache",
    "PerfLogs",
    "ProgramData",
    "Recovery",
    "System Volume Information",
    "Windows",
}
COMMON_SKIP_NAMES = {
    ".git",
    ".svn",
    ".hg",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    ".next",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "graphify-out",
}
SERVICE_MARKERS = ("docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml")
SEARCHABLE_KINDS = {"repo", "vault", "graph", "service", "root", "path"}
TRANSIENT_REPO_MARKERS = (
    "\\.codex\\.tmp\\",
    "\\vendor_imports\\",
    "\\appdata\\local\\temp\\",
    "\\appdata\\local\\pnpm\\store\\",
    "\\appdata\\roaming\\code\\user\\globalstorage\\",
    "\\appdata\\roaming\\cursor\\user\\globalstorage\\",
    "\\.wq\\",
)
TOOLING_REPO_MARKERS = (
    "\\appdata\\local\\agent-tools\\",
    "\\appdata\\local\\github cli\\extensions\\",
)


def _computer_intel_config() -> dict[str, Any]:
    effective = effective_config()
    defaults = {
        "enabled": True,
        "scan_scope": "laptop",
        "directory_budget": 250000,
        "search_limit": 80,
        "live_search_limit": 120,
    }
    payload = defaults.copy()
    payload.update(effective.get("computer_intel", {}))
    return payload


def _safe_resolve(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def _drive_roots() -> list[Path]:
    roots: list[Path] = []
    if os.name == "nt":
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            candidate = Path(f"{letter}:\\")
            if candidate.exists():
                roots.append(candidate)
    else:
        roots.append(Path("/"))
    return roots


def _default_roots(config: dict[str, Any]) -> list[Path]:
    scope = str(config.get("scan_scope") or "laptop").strip().lower()
    home = Path.home().resolve()
    roots: list[Path] = []
    if scope == "laptop":
        roots.extend(_drive_roots())
    roots.extend(
        path
        for path in (
            home,
            home / "Desktop",
            home / "Documents",
            home / "Downloads",
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")),
            Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")),
            Path(os.environ.get("LOCALAPPDATA", str(home / "AppData" / "Local"))),
        )
        if path.exists()
    )
    for project in trusted_projects():
        path = _safe_resolve(project["path"])
        if path.exists():
            roots.append(path)
    deduped: dict[str, Path] = {}
    for root in roots:
        if not root.exists():
            continue
        deduped.setdefault(str(root), root)
    return [deduped[key] for key in sorted(deduped, key=str.lower)]


def _trusted_roots() -> set[str]:
    return {str(_safe_resolve(item["path"])) for item in trusted_projects()}


def _should_skip_child(parent: Path, child: Path, *, root: Path) -> bool:
    if child.is_symlink():
        return True
    name = child.name
    if name in COMMON_SKIP_NAMES:
        return True
    if parent == root and name in ROOT_SKIP_NAMES:
        return True
    if name.lower() == "temp" and "appdata" in {part.lower() for part in child.parts}:
        return True
    return False


def _read_git_remote(repo_root: Path) -> str | None:
    config_path = repo_root / ".git" / "config"
    if not config_path.exists():
        return None
    try:
        lines = config_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    for raw_line in lines:
        line = raw_line.strip()
        if line.startswith("url = "):
            return line.split("=", 1)[1].strip()
    return None


def _repo_scope(repo_root: Path) -> str:
    path = str(repo_root).lower()
    if any(marker in path for marker in TRANSIENT_REPO_MARKERS):
        return "transient"
    if any(marker in path for marker in TOOLING_REPO_MARKERS):
        return "tooling"
    return "user"


def _repo_record(repo_root: Path, *, trusted_roots: set[str]) -> dict[str, Any]:
    repo_str = str(repo_root)
    trusted = repo_str in trusted_roots
    scope = _repo_scope(repo_root)
    manifest_path = repo_root / ".agentcli" / "repo-intel.json"
    graph_json = repo_root / "graphify-out" / "graph.json"
    graph_report = repo_root / "graphify-out" / "GRAPH_REPORT.md"
    managed = trusted or manifest_path.exists() or (graph_json.exists() and graph_report.exists())
    audit_candidate = trusted or scope == "user"
    repo_status = None
    if managed:
        try:
            repo_status = repo_intel_status(repo_root)
        except Exception as exc:  # pragma: no cover - defensive
            repo_status = {"status": "error", "detail": str(exc)}
    return {
        "kind": "repo",
        "name": repo_root.name,
        "path": repo_str,
        "repo_scope": scope,
        "audit_candidate": audit_candidate,
        "trusted": trusted,
        "managed": managed,
        "repo_intel_status": (repo_status or {}).get("status", "discovered"),
        "repo_intel_detail": (repo_status or {}).get("detail"),
        "graph_present": graph_json.exists() and graph_report.exists(),
        "manifest_present": manifest_path.exists(),
        "remote_url": _read_git_remote(repo_root),
    }


def _vault_record(vault_root: Path) -> dict[str, Any]:
    return {
        "kind": "vault",
        "name": vault_root.name,
        "path": str(vault_root),
        "config_path": str(vault_root / ".obsidian"),
    }


def _graph_record(repo_root: Path) -> dict[str, Any]:
    graph_root = repo_root / "graphify-out"
    return {
        "kind": "graph",
        "name": repo_root.name,
        "path": str(graph_root),
        "repo_root": str(repo_root),
        "graph_json": str(graph_root / "graph.json"),
        "graph_report": str(graph_root / "GRAPH_REPORT.md"),
    }


def _service_record(service_root: Path, *, marker_names: list[str]) -> dict[str, Any]:
    return {
        "kind": "service",
        "name": service_root.name,
        "path": str(service_root),
        "markers": sorted(marker_names),
    }


def _root_record(root: Path) -> dict[str, Any]:
    return {"kind": "root", "name": root.name or str(root), "path": str(root)}


def _normalized_query_tokens(query: str) -> list[str]:
    return [token for token in re.split(r"[^a-z0-9]+", query.lower()) if token]


def _text_matches(query_tokens: list[str], *values: Any) -> bool:
    haystack = " ".join(str(value or "").lower() for value in values)
    return all(token in haystack for token in query_tokens)


def _discover_machine_records(config: dict[str, Any]) -> dict[str, Any]:
    roots = _default_roots(config)
    trusted_roots = _trusted_roots()
    directory_budget = max(int(config.get("directory_budget", 50000) or 50000), 1000)

    repos: dict[str, dict[str, Any]] = {}
    vaults: dict[str, dict[str, Any]] = {}
    graphs: dict[str, dict[str, Any]] = {}
    services: dict[str, dict[str, Any]] = {}
    root_records = [_root_record(root) for root in roots]

    visited: set[str] = set()
    scanned_directories = 0
    skipped_directories = 0
    inaccessible_directories = 0
    truncated = False

    queue: deque[tuple[Path, Path]] = deque((root, root) for root in roots)
    while queue:
        current, root = queue.popleft()
        current_key = str(current)
        if current_key in visited:
            continue
        visited.add(current_key)
        scanned_directories += 1
        if scanned_directories > directory_budget:
            truncated = True
            break
        try:
            entries = list(os.scandir(current))
        except (FileNotFoundError, NotADirectoryError, PermissionError, OSError):
            inaccessible_directories += 1
            continue

        dir_entries = [entry for entry in entries if entry.is_dir(follow_symlinks=False)]
        entry_names = {entry.name for entry in entries}

        if ".git" in entry_names:
            repos[current_key] = _repo_record(current, trusted_roots=trusted_roots)
        if ".obsidian" in entry_names:
            vaults[current_key] = _vault_record(current)
        if "graphify-out" in entry_names and (current / "graphify-out" / "graph.json").exists():
            graphs[current_key] = _graph_record(current)
        service_markers = [name for name in SERVICE_MARKERS if name in entry_names]
        if service_markers:
            services[current_key] = _service_record(current, marker_names=service_markers)

        for entry in dir_entries:
            child = Path(entry.path)
            if _should_skip_child(current, child, root=root):
                skipped_directories += 1
                continue
            queue.append((child, root))

    return {
        "roots": root_records,
        "repos": [repos[key] for key in sorted(repos, key=str.lower)],
        "vaults": [vaults[key] for key in sorted(vaults, key=str.lower)],
        "graphs": [graphs[key] for key in sorted(graphs, key=str.lower)],
        "services": [services[key] for key in sorted(services, key=str.lower)],
        "scan_stats": {
            "scanned_directories": scanned_directories,
            "skipped_directories": skipped_directories,
            "inaccessible_directories": inaccessible_directories,
            "truncated": truncated,
            "directory_budget": directory_budget,
        },
    }


def computer_intel_status(*, refresh: bool = False) -> dict[str, Any]:
    config = _computer_intel_config()
    if refresh:
        return computer_intel_refresh()
    payload = load_json(COMPUTER_GRAPH_PATH, default={})
    if not config.get("enabled", True):
        return {
            "kind": "computer-intel-status",
            "status": "disabled",
            "detail": "Computer intelligence is disabled in config.",
            "config": config,
            "state_path": str(COMPUTER_GRAPH_PATH),
            "recommended_action": "agentcli config set computer_intel.enabled true",
        }
    if not payload:
        return {
            "kind": "computer-intel-status",
            "status": "missing",
            "detail": "Machine-wide computer-intel state has not been built yet.",
            "config": config,
            "state_path": str(COMPUTER_GRAPH_PATH),
            "roots": [str(root) for root in _default_roots(config)],
            "recommended_action": "agentcli computer-intel refresh",
        }
    summary = payload.get("summary", {})
    return {
        **payload,
        "kind": "computer-intel-status",
        "status": payload.get("status", "ok"),
        "detail": payload.get("detail", "Machine-wide computer-intel state is available."),
        "config": config,
        "state_path": str(COMPUTER_GRAPH_PATH),
        "recommended_action": "agentcli computer-intel refresh" if summary.get("truncated") else "agentcli computer-intel search <query>",
    }


def computer_intel_refresh() -> dict[str, Any]:
    config = _computer_intel_config()
    if not config.get("enabled", True):
        payload = {
            "schema_version": SCHEMA_VERSION,
            "generated_at": utc_now(),
            "status": "disabled",
            "detail": "Computer intelligence is disabled in config.",
            "summary": {"root_count": 0, "repo_count": 0, "vault_count": 0, "graph_count": 0, "service_count": 0, "trusted_repo_count": 0, "managed_repo_count": 0, "truncated": False},
            "roots": [],
            "repos": [],
            "vaults": [],
            "graphs": [],
            "services": [],
            "scan_stats": {"scanned_directories": 0, "skipped_directories": 0, "inaccessible_directories": 0, "truncated": False, "directory_budget": 0},
            "config": config,
        }
        save_json(COMPUTER_GRAPH_PATH, payload)
        return {**payload, "kind": "computer-intel-refresh", "state_path": str(COMPUTER_GRAPH_PATH)}

    discovered = _discover_machine_records(config)
    repos = discovered["repos"]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "status": "ok",
        "detail": "Machine-wide computer-intel registry refreshed.",
        "summary": {
            "root_count": len(discovered["roots"]),
            "repo_count": len(repos),
            "audit_candidate_repo_count": sum(1 for item in repos if item.get("audit_candidate")),
            "trusted_repo_count": sum(1 for item in repos if item.get("trusted")),
            "managed_repo_count": sum(1 for item in repos if item.get("managed")),
            "vault_count": len(discovered["vaults"]),
            "graph_count": len(discovered["graphs"]),
            "service_count": len(discovered["services"]),
            "truncated": bool(discovered["scan_stats"].get("truncated")),
        },
        **discovered,
        "config": config,
    }
    save_json(COMPUTER_GRAPH_PATH, payload)
    return {**payload, "kind": "computer-intel-refresh", "state_path": str(COMPUTER_GRAPH_PATH)}


def _registry_search(registry: dict[str, Any], *, query: str, kind: str, limit: int) -> list[dict[str, Any]]:
    query_tokens = _normalized_query_tokens(query)
    if not query_tokens:
        return []
    matches: list[dict[str, Any]] = []
    for bucket_name in ("repos", "vaults", "graphs", "services", "roots"):
        for record in registry.get(bucket_name, []):
            record_kind = record.get("kind", bucket_name[:-1])
            if kind != "all" and record_kind != kind:
                continue
            if _text_matches(query_tokens, record.get("name"), record.get("path"), record.get("remote_url"), record.get("repo_intel_status"), record.get("markers")):
                matches.append(record)
    matches.sort(key=lambda item: (item.get("kind", ""), str(item.get("name", "")).lower(), str(item.get("path", "")).lower()))
    return matches[:limit]


def _live_search(roots: list[Path], *, query: str, kind: str, limit: int, directory_budget: int) -> list[dict[str, Any]]:
    query_tokens = _normalized_query_tokens(query)
    if not query_tokens or limit <= 0:
        return []
    matches: list[dict[str, Any]] = []
    visited: set[str] = set()
    queue: deque[tuple[Path, Path]] = deque((root, root) for root in roots)
    scanned_directories = 0
    while queue and len(matches) < limit:
        current, root = queue.popleft()
        current_key = str(current)
        if current_key in visited:
            continue
        visited.add(current_key)
        scanned_directories += 1
        if scanned_directories > directory_budget:
            break
        try:
            entries = list(os.scandir(current))
        except (FileNotFoundError, NotADirectoryError, PermissionError, OSError):
            continue
        for entry in entries:
            path = Path(entry.path)
            if entry.is_dir(follow_symlinks=False):
                if not _should_skip_child(current, path, root=root):
                    queue.append((path, root))
                if kind in {"all", "path"} and _text_matches(query_tokens, entry.name, str(path)):
                    matches.append({"kind": "path", "path_type": "directory", "name": entry.name, "path": str(path)})
            elif kind in {"all", "path"} and _text_matches(query_tokens, entry.name, str(path)):
                matches.append({"kind": "path", "path_type": "file", "name": entry.name, "path": str(path)})
            if len(matches) >= limit:
                break
    return matches[:limit]


def computer_intel_search(query: str, *, kind: str = "all", limit: int | None = None) -> dict[str, Any]:
    config = _computer_intel_config()
    if kind not in SEARCHABLE_KINDS and kind != "all":
        raise ValueError(f"unsupported search kind: {kind}")
    registry = load_json(COMPUTER_GRAPH_PATH, default={})
    if not registry:
        registry = computer_intel_refresh()
    search_limit = limit or int(config.get("search_limit", 40) or 40)
    live_limit = int(config.get("live_search_limit", 60) or 60)
    roots = [_safe_resolve(item["path"]) for item in registry.get("roots", []) if isinstance(item, dict) and item.get("path")]
    registry_matches = _registry_search(registry, query=query, kind=kind, limit=search_limit)
    live_matches = _live_search(
        roots,
        query=query,
        kind=kind,
        limit=min(live_limit, search_limit),
        directory_budget=max(int(config.get("directory_budget", 250000) or 250000), 1000),
    )
    return {
        "kind": "computer-intel-search",
        "status": "ok",
        "query": query,
        "search_kind": kind,
        "summary": {
            "registry_match_count": len(registry_matches),
            "live_match_count": len(live_matches),
            "root_count": len(roots),
        },
        "registry_matches": registry_matches,
        "live_matches": live_matches,
        "state_path": str(COMPUTER_GRAPH_PATH),
    }


def discovered_repo_paths() -> list[Path]:
    payload = load_json(COMPUTER_GRAPH_PATH, default={})
    repos: list[Path] = []
    for record in payload.get("repos", []):
        if not isinstance(record, dict):
            continue
        if not record.get("audit_candidate", True):
            continue
        raw_path = record.get("path")
        if not isinstance(raw_path, str):
            continue
        path = _safe_resolve(raw_path)
        if path.exists():
            repos.append(path)
    unique = {str(path): path for path in repos}
    return [unique[key] for key in sorted(unique, key=str.lower)]


def print_computer_intel_human(payload: dict[str, Any], *, as_json: bool = False) -> None:
    if as_json:
        print_json(payload)
        return

    kind = payload.get("kind", "computer-intel-status")
    if kind == "computer-intel-search":
        print(f"Status: {payload.get('status', 'unknown')}")
        print(f"Query: {payload.get('query', '')}")
        print("")
        print("Registry matches")
        registry_matches = payload.get("registry_matches", [])
        if not registry_matches:
            print("- none")
        else:
            for item in registry_matches:
                print(f"- {item.get('kind', 'item')}: {item.get('name', item.get('path', 'unknown'))}")
                print(f"  - {item.get('path', '')}")
                if item.get("repo_intel_status"):
                    print(f"  - repo-intel: {item['repo_intel_status']}")
        print("")
        print("Live path matches")
        live_matches = payload.get("live_matches", [])
        if not live_matches:
            print("- none")
        else:
            for item in live_matches:
                print(f"- {item.get('path_type', 'path')}: {item.get('path', '')}")
        return

    summary = payload.get("summary", {})
    print(f"Status: {payload.get('status', 'unknown')}")
    print(f"Detail: {payload.get('detail', '')}")
    if payload.get("generated_at"):
        print(f"Generated: {payload['generated_at']}")
    print(f"State: {payload.get('state_path', str(COMPUTER_GRAPH_PATH))}")
    print("")
    print("Counts")
    print(f"- roots: {summary.get('root_count', 0)}")
    print(f"- repos: {summary.get('repo_count', 0)}")
    print(f"- audit candidates: {summary.get('audit_candidate_repo_count', 0)}")
    print(f"- trusted repos: {summary.get('trusted_repo_count', 0)}")
    print(f"- managed repos: {summary.get('managed_repo_count', 0)}")
    print(f"- vaults: {summary.get('vault_count', 0)}")
    print(f"- graphify exports: {summary.get('graph_count', 0)}")
    print(f"- services: {summary.get('service_count', 0)}")
    if summary.get("truncated"):
        print("- scan truncated: true")
    print("")
    print("Use `agentcli computer-intel search <query>` for laptop-wide discovery and `agentcli repo-intel ...` for repo-specific graph work.")
