from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import print_json, save_json, utc_now
from .config_layers import effective_config
from .paths import CODEX_HOME, GUIDANCE_PATH


GUIDANCE_SCHEMA_VERSION = 1
SNIPPET_SUFFIXES = {".md", ".txt"}


def _resolve_dir(raw: str, *, base: Path) -> Path | None:
    value = (raw or "").strip()
    if not value:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = base / path
    return path.resolve()


def _snippet_files(path: Path | None) -> list[Path]:
    if path is None or not path.exists() or not path.is_dir():
        return []
    return sorted(
        file_path
        for file_path in path.rglob("*")
        if file_path.is_file() and file_path.suffix.lower() in SNIPPET_SUFFIXES
    )


def _first_non_empty_line(text: str) -> str:
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line:
            return line[:120]
    return ""


def build_guidance_snapshot(repo: str | Path | None = None) -> dict[str, Any]:
    repo_root = Path(repo).resolve() if repo else Path.cwd().resolve()
    config = effective_config(repo_root)
    guidance_config = config.get("guidance", {})
    max_files = int(guidance_config.get("max_files", 8) or 8)
    max_total_lines = int(guidance_config.get("max_total_lines", 200) or 200)

    user_dir = _resolve_dir(str(guidance_config.get("user_dir", "")), base=CODEX_HOME)
    repo_dir = _resolve_dir(str(guidance_config.get("repo_dir", "")), base=repo_root)

    items: list[dict[str, Any]] = []
    total_lines = 0
    for scope, directory in (("user", user_dir), ("repo", repo_dir)):
        for file_path in _snippet_files(directory):
            content = file_path.read_text(encoding="utf-8")
            line_count = len(content.splitlines())
            total_lines += line_count
            items.append(
                {
                    "name": file_path.name,
                    "scope": scope,
                    "path": str(file_path),
                    "line_count": line_count,
                    "title": _first_non_empty_line(content),
                }
            )

    file_count = len(items)
    within_budget = file_count <= max_files and total_lines <= max_total_lines
    status = "ok" if within_budget else "degraded"

    snapshot = {
        "schema_version": GUIDANCE_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "config": {
            "user_dir": str(user_dir) if user_dir else "",
            "repo_dir": str(repo_dir) if repo_dir else "",
            "max_files": max_files,
            "max_total_lines": max_total_lines,
        },
        "summary": {
            "status": status,
            "file_count": file_count,
            "total_lines": total_lines,
            "within_budget": within_budget,
        },
        "items": items,
    }
    return snapshot


def refresh_guidance_snapshot(repo: str | Path | None = None, *, output_path: str | Path | None = None) -> dict[str, Any]:
    snapshot = build_guidance_snapshot(repo)
    save_json(output_path or GUIDANCE_PATH, snapshot)
    return snapshot


def load_guidance_snapshot(
    repo: str | Path | None = None,
    *,
    refresh: bool = False,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    path = Path(output_path).resolve() if output_path else GUIDANCE_PATH
    if refresh or not path.exists():
        return refresh_guidance_snapshot(repo, output_path=path)
    import json

    return json.loads(path.read_text(encoding="utf-8"))


def print_guidance_human(payload: dict[str, Any], *, as_json: bool = False) -> None:
    if as_json:
        print_json(payload)
        return

    summary = payload.get("summary", {})
    print(f"Status: {summary.get('status', 'unknown')}")
    print(f"Files: {summary.get('file_count', 0)}")
    print(f"Total lines: {summary.get('total_lines', 0)}")
    print("")
    print("Guidance snippets")
    items = payload.get("items", [])
    if not items:
        print("- none")
        return
    for item in items:
        suffix = f" | {item['title']}" if item.get("title") else ""
        print(f"- {item['scope']}: {item['path']} [{item['line_count']} lines]{suffix}")
