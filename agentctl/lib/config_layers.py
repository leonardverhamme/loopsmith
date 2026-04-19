from __future__ import annotations

import tomllib
from copy import deepcopy
from pathlib import Path
from typing import Any

from .branding import PUBLIC_DOCS_DIRNAME
from .common import print_json
from .paths import CODEX_HOME, CONFIG_PATH


CONFIG_SCHEMA_VERSION = 1

DEFAULT_CONFIG: dict[str, Any] = {
    "schema_version": CONFIG_SCHEMA_VERSION,
    "worker": {
        "mode": "auto",
        "command": "",
        "template": "",
    },
    "updates": {
        "channel": "latest",
        "source": "github-release",
        "repo_url": "",
    },
    "browser": {
        "preferred_route": "auto",
    },
    "inventory": {
        "refresh_on_doctor": True,
    },
    "guidance": {
        "user_dir": "",
        "repo_dir": "",
        "max_files": 8,
        "max_total_lines": 200,
    },
    "menus": {
        "default_view": "groups",
        "max_items": 25,
        "names_only": True,
    },
}


def repo_config_path(repo: str | Path | None = None) -> Path:
    root = Path(repo).resolve() if repo else Path.cwd().resolve()
    return root / f".{PUBLIC_DOCS_DIRNAME}" / "config.toml"


def _quote_header_key(raw: str) -> str:
    key = raw.strip()
    if (key.startswith('"') and key.endswith('"')) or (key.startswith("'") and key.endswith("'")):
        key = key[1:-1]
    escaped = key.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _normalize_legacy_toml(raw: str) -> str:
    normalized_lines: list[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("[projects.") and stripped.endswith("]"):
            raw_key = stripped[len("[projects.") : -1]
            normalized_lines.append(f'[projects.{_quote_header_key(raw_key)}]')
            continue
        if stripped.startswith("[plugins.") and stripped.endswith("]"):
            raw_key = stripped[len("[plugins.") : -1]
            normalized_lines.append(f'[plugins.{_quote_header_key(raw_key)}]')
            continue
        normalized_lines.append(line)
    return "\n".join(normalized_lines)


def _load_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8")
    try:
        return tomllib.loads(raw)
    except tomllib.TOMLDecodeError:
        try:
            return tomllib.loads(_normalize_legacy_toml(raw))
        except tomllib.TOMLDecodeError:
            return {}


def _deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _format_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if value is None:
        return '""'
    return _quote(str(value))


def _dump_table(lines: list[str], prefix: list[str], payload: dict[str, Any]) -> None:
    scalar_items = [(key, value) for key, value in payload.items() if not isinstance(value, dict)]
    if prefix:
        lines.append(f"[{'.'.join(prefix)}]")
    for key, value in scalar_items:
        lines.append(f"{key} = {_format_scalar(value)}")
    if scalar_items and any(isinstance(value, dict) for value in payload.values()):
        lines.append("")
    nested_keys = [key for key, value in payload.items() if isinstance(value, dict)]
    for index, key in enumerate(nested_keys):
        _dump_table(lines, [*prefix, key], payload[key])
        if index != len(nested_keys) - 1:
            lines.append("")


def dump_toml(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    root_scalars = [(key, value) for key, value in payload.items() if not isinstance(value, dict)]
    for key, value in root_scalars:
        lines.append(f"{key} = {_format_scalar(value)}")
    if root_scalars and any(isinstance(value, dict) for value in payload.values()):
        lines.append("")
    nested_keys = [key for key, value in payload.items() if isinstance(value, dict)]
    for index, key in enumerate(nested_keys):
        _dump_table(lines, [key], payload[key])
        if index != len(nested_keys) - 1:
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_value(raw: str) -> Any:
    lowered = raw.strip().lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered.isdigit() or (lowered.startswith("-") and lowered[1:].isdigit()):
        return int(lowered)
    return raw


def _scope_path(scope: str, *, repo: str | Path | None = None) -> Path | None:
    if scope == "user":
        return CONFIG_PATH
    if scope == "repo":
        return repo_config_path(repo)
    return None


def _split_key(key: str) -> list[str]:
    return [part for part in key.split(".") if part]


def _set_nested(payload: dict[str, Any], key: str, value: Any) -> dict[str, Any]:
    updated = deepcopy(payload)
    parts = _split_key(key)
    cursor = updated
    for part in parts[:-1]:
        next_value = cursor.get(part)
        if not isinstance(next_value, dict):
            next_value = {}
            cursor[part] = next_value
        cursor = next_value
    cursor[parts[-1]] = value
    return updated


def _unset_nested(payload: dict[str, Any], key: str) -> dict[str, Any]:
    updated = deepcopy(payload)
    parts = _split_key(key)
    cursor = updated
    parents: list[tuple[dict[str, Any], str]] = []
    for part in parts[:-1]:
        next_value = cursor.get(part)
        if not isinstance(next_value, dict):
            return updated
        parents.append((cursor, part))
        cursor = next_value
    cursor.pop(parts[-1], None)
    while parents:
        parent, part = parents.pop()
        child = parent.get(part)
        if isinstance(child, dict) and not child:
            parent.pop(part, None)
    return updated


def layer_payloads(repo: str | Path | None = None) -> dict[str, dict[str, Any]]:
    return {
        "bundled": deepcopy(DEFAULT_CONFIG),
        "user": _load_toml(CONFIG_PATH),
        "repo": _load_toml(repo_config_path(repo)),
    }


def effective_config(repo: str | Path | None = None) -> dict[str, Any]:
    layers = layer_payloads(repo)
    return _deep_merge(_deep_merge(layers["bundled"], layers["user"]), layers["repo"])


def config_snapshot(repo: str | Path | None = None) -> dict[str, Any]:
    layers = layer_payloads(repo)
    return {
        "schema_version": CONFIG_SCHEMA_VERSION,
        "paths": {
            "user": str(CONFIG_PATH),
            "repo": str(repo_config_path(repo)),
        },
        "layers": layers,
        "effective": effective_config(repo),
    }


def write_scope(scope: str, payload: dict[str, Any], *, repo: str | Path | None = None) -> Path:
    path = _scope_path(scope, repo=repo)
    if path is None:
        raise ValueError(f"unsupported writable scope: {scope}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_toml(payload), encoding="utf-8")
    return path


def set_config_value(scope: str, key: str, value: Any, *, repo: str | Path | None = None) -> dict[str, Any]:
    path = _scope_path(scope, repo=repo)
    if path is None:
        raise ValueError(f"unsupported writable scope: {scope}")
    payload = _load_toml(path)
    updated = _set_nested(payload, key, value)
    if "schema_version" not in updated:
        updated["schema_version"] = CONFIG_SCHEMA_VERSION
    written = write_scope(scope, updated, repo=repo)
    return {
        "status": "ok",
        "scope": scope,
        "key": key,
        "value": value,
        "path": str(written),
        "effective": effective_config(repo),
    }


def unset_config_value(scope: str, key: str, *, repo: str | Path | None = None) -> dict[str, Any]:
    path = _scope_path(scope, repo=repo)
    if path is None:
        raise ValueError(f"unsupported writable scope: {scope}")
    payload = _load_toml(path)
    updated = _unset_nested(payload, key)
    if updated:
        updated.setdefault("schema_version", CONFIG_SCHEMA_VERSION)
        written = write_scope(scope, updated, repo=repo)
    else:
        if path.exists():
            path.unlink()
        written = path
    return {
        "status": "ok",
        "scope": scope,
        "key": key,
        "path": str(written),
        "effective": effective_config(repo),
    }


def config_path_payload(scope: str, *, repo: str | Path | None = None) -> dict[str, Any]:
    if scope == "bundled":
        return {"scope": scope, "path": "<bundled-defaults>"}
    path = _scope_path(scope, repo=repo)
    if path is None:
        raise ValueError(f"unknown scope: {scope}")
    return {"scope": scope, "path": str(path)}


def repair_user_config() -> dict[str, Any]:
    payload = _load_toml(CONFIG_PATH)
    changed = False
    if "schema_version" not in payload:
        payload["schema_version"] = CONFIG_SCHEMA_VERSION
        changed = True
    if changed or not CONFIG_PATH.exists():
        path = write_scope("user", payload, repo=None)
    else:
        path = CONFIG_PATH
    return {"status": "ok", "path": str(path), "changed": changed}


def print_config_human(payload: dict[str, Any], *, as_json: bool = False) -> None:
    if as_json:
        print_json(payload)
        return

    if "layers" in payload:
        print("Config layers")
        print(f"- bundled: <bundled-defaults>")
        print(f"- user: {payload['paths']['user']}")
        print(f"- repo: {payload['paths']['repo']}")
        print("")
        print("Effective config")
        for group, values in payload.get("effective", {}).items():
            if isinstance(values, dict):
                print(f"- {group}:")
                for key, value in values.items():
                    print(f"  - {key} = {value}")
            else:
                print(f"- {group} = {values}")
        return

    print(f"Status: {payload.get('status', 'ok')}")
    if payload.get("path"):
        print(f"Path: {payload['path']}")
    if payload.get("scope"):
        print(f"Scope: {payload['scope']}")
    if payload.get("key"):
        print(f"Key: {payload['key']}")
    if "value" in payload:
        print(f"Value: {payload['value']}")
