from __future__ import annotations

import importlib.metadata
import json
import tomllib
from pathlib import Path
from typing import Any

try:
    from ..bundle_install import read_install_metadata
    from .branding import LEGACY_PRODUCT_NAME, PUBLIC_PRODUCT_NAME
    from .common import print_json, utc_now
    from .config_layers import CONFIG_SCHEMA_VERSION, config_snapshot
except ImportError:
    from bundle_install import read_install_metadata
    from lib.branding import LEGACY_PRODUCT_NAME, PUBLIC_PRODUCT_NAME
    from lib.common import print_json, utc_now
    from lib.config_layers import CONFIG_SCHEMA_VERSION, config_snapshot


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _pyproject_version() -> str | None:
    pyproject_path = _repo_root() / "pyproject.toml"
    if not pyproject_path.exists():
        return None
    payload = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    return payload.get("project", {}).get("version")


def wrapper_version() -> str | None:
    for name in (PUBLIC_PRODUCT_NAME, LEGACY_PRODUCT_NAME):
        try:
            return importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            continue
    return _pyproject_version()


def build_self_check(capabilities: dict[str, Any], *, repo: str | Path | None = None) -> dict[str, Any]:
    install_metadata = read_install_metadata()
    effective_config = config_snapshot(repo)
    wrapper = wrapper_version()
    bundle = install_metadata.get("version") or _pyproject_version()
    checks = [
        {"name": "wrapper-version", "status": "ok" if wrapper else "degraded", "detail": wrapper or "wrapper version unavailable"},
        {"name": "bundle-version", "status": "ok" if bundle else "degraded", "detail": bundle or "bundle version unavailable"},
        {
            "name": "config-schema",
            "status": "ok" if effective_config["effective"].get("schema_version") == CONFIG_SCHEMA_VERSION else "degraded",
            "detail": f"expected {CONFIG_SCHEMA_VERSION}, found {effective_config['effective'].get('schema_version')}",
        },
        {
            "name": "plugin-health",
            "status": "ok" if capabilities.get("summary", {}).get("status") != "error" else "error",
            "detail": capabilities.get("summary", {}).get("status", "unknown"),
        },
        {
            "name": "install-metadata",
            "status": "ok" if install_metadata else "degraded",
            "detail": json.dumps(install_metadata, sort_keys=True) if install_metadata else "install metadata missing",
        },
    ]
    statuses = {item["status"] for item in checks}
    status = "error" if "error" in statuses else "degraded" if "degraded" in statuses else "ok"
    return {
        "status": status,
        "generated_at": utc_now(),
        "wrapper_version": wrapper,
        "bundle_version": bundle,
        "install_metadata": install_metadata,
        "config": effective_config,
        "checks": checks,
    }


def print_self_check(payload: dict[str, Any], *, as_json: bool = False) -> None:
    if as_json:
        print_json(payload)
        return

    print(f"Status: {payload.get('status', 'unknown')}")
    print(f"Wrapper version: {payload.get('wrapper_version') or 'unknown'}")
    print(f"Bundle version: {payload.get('bundle_version') or 'unknown'}")
    print("")
    print("Checks")
    for item in payload.get("checks", []):
        print(f"- {item['name']}: {item['status']} | {item['detail']}")
