from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from .common import load_json, run_command, save_json, utc_now
from .paths import SKILLS_DIR, SKILLS_LOCK_PATH


def _lock_file() -> dict[str, Any]:
    payload = load_json(SKILLS_LOCK_PATH, default={"schema_version": 2, "updated_at": None, "entries": []})
    payload.setdefault("schema_version", 2)
    payload.setdefault("updated_at", None)
    payload.setdefault("entries", [])
    return payload


def _save_lock(payload: dict[str, Any]) -> None:
    payload["updated_at"] = utc_now()
    save_json(SKILLS_LOCK_PATH, payload)


def _discover_local_skill_names() -> set[str]:
    names: set[str] = set()
    if not SKILLS_DIR.exists():
        return names
    for path in SKILLS_DIR.glob("*/SKILL.md"):
        if path.parent.name == ".system":
            continue
        names.add(path.parent.name)
    return names


def _tracked_names(lock: dict[str, Any], *, scope: str, kind: str | None = None) -> set[str]:
    names: set[str] = set()
    for entry in lock.get("entries", []):
        if entry.get("scope") != scope:
            continue
        if kind and entry.get("kind") != kind:
            continue
        names.update(entry.get("skills", []))
    return names


def _sync_local_entries(lock: dict[str, Any], *, global_scope: bool) -> dict[str, Any]:
    if not global_scope:
        return lock
    scope = "global"
    remote_names = _tracked_names(lock, scope=scope, kind="managed")
    local_names = sorted(_discover_local_skill_names() - remote_names)
    entries = [
        entry
        for entry in lock.get("entries", [])
        if not (entry.get("scope") == scope and entry.get("kind") == "local")
    ]
    if local_names:
        entries.append(
            {
                "kind": "local",
                "scope": scope,
                "source": "codex-home",
                "ref": None,
                "skills": local_names,
                "agents": ["codex"],
                "path_root": str(SKILLS_DIR),
                "managed_by": "agentctl",
            }
        )
    lock["entries"] = entries
    lock["schema_version"] = max(lock.get("schema_version", 1), 2)
    return lock


def list_skills(*, global_scope: bool) -> dict[str, Any]:
    command = ["npx", "skills", "ls", "--json"]
    if global_scope:
        command.insert(3, "-g")
    result = run_command(command, timeout=60)
    if not result["ok"]:
        return {"summary": {"status": "error"}, "error": result["stderr"] or result["stdout"] or "failed to list skills"}
    import json

    return {"summary": {"status": "ok", "scope": "global" if global_scope else "project"}, "skills": json.loads(result["stdout"] or "[]")}


def _normalize_source(source: str, ref: str | None) -> tuple[str, str | None]:
    if ref is None:
        return source, None
    if source.startswith("http://") or source.startswith("https://"):
        base = source.removesuffix(".git")
        return base + ".git", ref
    if "/" in source and not Path(source).exists():
        return f"https://github.com/{source}.git", ref
    raise ValueError("pinned installs require a GitHub shorthand or git URL source")


def _clone_source_at_ref(source: str, ref: str) -> str:
    clone_url, normalized_ref = _normalize_source(source, ref)
    temp_dir = tempfile.mkdtemp(prefix="agentctl-skill-")
    clone_result = run_command(["git", "clone", "--depth", "1", clone_url, temp_dir], timeout=120)
    if not clone_result["ok"]:
        raise RuntimeError(clone_result["stderr"] or clone_result["stdout"] or "failed to clone skill source")
    checkout_result = run_command(["git", "-C", temp_dir, "checkout", normalized_ref], timeout=60)
    if not checkout_result["ok"]:
        raise RuntimeError(checkout_result["stderr"] or checkout_result["stdout"] or "failed to checkout requested ref")
    return temp_dir


def _perform_add(*, source: str, skill_names: list[str], ref: str | None, global_scope: bool, record_lock: bool) -> dict[str, Any]:
    before = list_skills(global_scope=global_scope)
    if before["summary"]["status"] != "ok":
        return before

    install_source = source
    try:
        if ref:
            install_source = _clone_source_at_ref(source, ref)
    except Exception as exc:
        return {"summary": {"status": "error"}, "error": str(exc)}

    command = ["npx", "skills", "add", install_source, "-y", "--copy"]
    if global_scope:
        command.append("-g")
    for name in skill_names:
        command.extend(["--skill", name])
    command.extend(["--agent", "codex"])
    result = run_command(command, timeout=120)
    if not result["ok"]:
        return {"summary": {"status": "error"}, "error": result["stderr"] or result["stdout"] or "failed to add skills"}

    after = list_skills(global_scope=global_scope)
    if after["summary"]["status"] != "ok":
        return after

    before_names = {item["name"] for item in before["skills"]}
    after_names = {item["name"] for item in after["skills"]}
    added_names = sorted((after_names - before_names) or set(skill_names))

    if record_lock:
        lock = _lock_file()
        lock["entries"].append(
            {
                "kind": "managed",
                "installed_at": utc_now(),
                "scope": "global" if global_scope else "project",
                "source": source,
                "ref": ref,
                "skills": added_names,
                "agents": ["codex"],
                "install_source": install_source if ref else source,
                "mode": "copy",
            }
        )
        lock = _sync_local_entries(lock, global_scope=global_scope)
        _save_lock(lock)
    return {
        "summary": {"status": "ok"},
        "added_skills": added_names,
        "scope": "global" if global_scope else "project",
        "source": source,
        "ref": ref,
    }


def add_skill(*, source: str, skill_names: list[str], ref: str | None, global_scope: bool) -> dict[str, Any]:
    return _perform_add(source=source, skill_names=skill_names, ref=ref, global_scope=global_scope, record_lock=True)


def check_skills(*, global_scope: bool) -> dict[str, Any]:
    listed = list_skills(global_scope=global_scope)
    if listed["summary"]["status"] != "ok":
        return listed
    lock = _lock_file()
    lock = _sync_local_entries(lock, global_scope=global_scope)
    _save_lock(lock)
    scope = "global" if global_scope else "project"
    installed_names = {item["name"] for item in listed["skills"]}
    tracked_external = _tracked_names(lock, scope=scope, kind="managed")
    tracked_local = _tracked_names(lock, scope=scope, kind="local")
    tracked_names = tracked_external | tracked_local
    unmanaged_installed = sorted(installed_names - tracked_names)
    status = "degraded" if unmanaged_installed or (tracked_names - installed_names) else "ok"
    return {
        "summary": {"status": status, "scope": scope},
        "scope": scope,
        "tracked_missing": sorted(tracked_names - installed_names),
        "unmanaged_installed": unmanaged_installed,
        "tracked_local": sorted(tracked_local),
        "tracked_external": sorted(tracked_external),
        "tracked": sorted(tracked_names),
        "installed": sorted(installed_names),
    }


def update_skills(*, global_scope: bool) -> dict[str, Any]:
    lock = _lock_file()
    lock = _sync_local_entries(lock, global_scope=global_scope)
    _save_lock(lock)
    scope = "global" if global_scope else "project"
    entries = [entry for entry in lock["entries"] if entry["scope"] == scope and entry.get("kind") == "managed"]
    if not entries:
        return {
            "summary": {"status": "ok", "scope": scope},
            "updated": [],
            "scope": scope,
            "note": "no externally tracked skills for the requested scope",
        }

    updated: list[dict[str, Any]] = []
    for entry in entries:
        result = _perform_add(
            source=entry["source"],
            skill_names=entry.get("skills", []),
            ref=entry.get("ref"),
            global_scope=global_scope,
            record_lock=False,
        )
        if result["summary"]["status"] != "ok":
            return result
        updated.append(result)
    return {"summary": {"status": "ok", "scope": scope}, "updated": updated, "scope": scope}
