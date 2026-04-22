from __future__ import annotations

from collections import defaultdict
from typing import Any

from .branding import PUBLIC_COMMAND
from .capabilities import build_capabilities_report
from .common import print_json
from .inventory import load_inventory_snapshot
from .repo_intel import detect_repo_root, repo_intel_status


_STATUS_ORDER = ("healthy", "degraded", "missing", "disabled", "error", "unknown")
_STATUS_ALIASES = {
    "ok": "healthy",
    "configured": "healthy",
    "enabled": "healthy",
}


def _display_status(status: Any) -> str:
    if not isinstance(status, str):
        return "unknown"
    return _STATUS_ALIASES.get(status, status)


def _aggregate_status(statuses: list[str]) -> str:
    normalized = {_display_status(status) for status in statuses}
    if "error" in normalized:
        return "error"
    if {"degraded", "missing", "disabled"} & normalized:
        return "degraded"
    if normalized:
        return "healthy"
    return "unknown"


def _status_buckets(items: list[dict[str, Any]], *, name_key: str = "name", extra_key: str | None = None) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = defaultdict(list)
    for item in sorted(items, key=lambda entry: (str(entry.get(name_key, "")).lower(), str(entry.get(extra_key, "")) if extra_key else "")):
        status = _display_status(item.get("status"))
        name = str(item.get(name_key, "unknown"))
        if extra_key:
            extra = item.get(extra_key)
            if extra and extra != name:
                name = f"{name} [connector: {extra}]"
        buckets[status].append(name)
    return {status: buckets[status] for status in _STATUS_ORDER if buckets.get(status)}


def _format_names(names: list[str], *, limit: int | None = None) -> str:
    if not names:
        return "-"
    if limit is None or len(names) <= limit:
        return ", ".join(names)
    visible = ", ".join(names[:limit])
    remaining = len(names) - limit
    return f"{visible}, +{remaining} more"


def _capability_group_sections(payload: dict[str, Any]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in payload.get("capabilities", []):
        grouped[item.get("group", "other")].append(item)

    sections: list[dict[str, Any]] = []
    for group in payload.get("capability_groups", []):
        items = sorted(grouped.get(group["key"], []), key=lambda entry: (entry.get("label", entry.get("key", "")).lower(), entry.get("key", "")))
        group_status = _display_status(group.get("status"))
        if group_status == "unknown":
            group_status = _aggregate_status([item.get("status", "unknown") for item in items])
        sections.append(
            {
                "key": group["key"],
                "label": group.get("label", group["key"]),
                "status": group_status,
                "count": len(items),
                "items": [item.get("label", item.get("key", "unknown")) for item in items],
            }
        )
    return [section for section in sections if section["count"]]


def build_overview_report(
    *,
    capabilities_report: dict[str, Any] | None = None,
    inventory_snapshot: dict[str, Any] | None = None,
    repo: str | None = None,
    refresh_inventory: bool = False,
) -> dict[str, Any]:
    inventory = inventory_snapshot or load_inventory_snapshot(repo, refresh=refresh_inventory)
    capabilities = capabilities_report or build_capabilities_report(inventory_snapshot=inventory)
    active_repo_root = detect_repo_root(repo)
    active_repo_intel = repo_intel_status(active_repo_root) if active_repo_root else None

    front_door_sections = _capability_group_sections(capabilities)
    cli_items = _status_buckets(list(capabilities.get("tools", {}).values()))
    app_items = _status_buckets(list(capabilities.get("apps", {}).get("items", [])), extra_key="connector_id")
    mcp_items = _status_buckets(list(capabilities.get("mcp_servers", {}).get("items", [])))
    plugin_items = _status_buckets(list(capabilities.get("plugins", {}).get("items", [])))

    summary_status = _aggregate_status(
        [
            _display_status(capabilities.get("summary", {}).get("status")),
            _display_status(inventory.get("summary", {}).get("status")),
        ]
    )

    return {
        "kind": "overview",
        "generated_at": capabilities.get("generated_at") or inventory.get("generated_at"),
        "summary": {
            "status": summary_status,
            "front_door_group_count": len(front_door_sections),
            "cli_count": sum(len(names) for names in cli_items.values()),
            "app_count": sum(len(names) for names in app_items.values()),
            "mcp_count": sum(len(names) for names in mcp_items.values()),
            "plugin_count": sum(len(names) for names in plugin_items.values()),
        },
        "repo_intel": (
            {
                "repo_root": active_repo_intel["repo_root"],
                "repo_name": active_repo_intel["repo_name"],
                "status": active_repo_intel["status"],
                "detail": active_repo_intel["detail"],
                "trusted": active_repo_intel.get("trusted", False),
                "recommended_action": active_repo_intel["recommended_action"],
                "default_mode": active_repo_intel.get("policy", {}).get("default_mode", "unknown"),
                "computer_intel_role": active_repo_intel.get("policy", {}).get("computer_intel_role", "unknown"),
            }
            if active_repo_intel
            else None
        ),
        "front_doors": front_door_sections,
        "clis": {
            "status": _aggregate_status([status for status in cli_items]),
            "items": cli_items,
        },
        "apps": {
            "status": _aggregate_status([status for status in app_items]),
            "items": app_items,
        },
        "mcps": {
            "status": _aggregate_status([status for status in mcp_items]),
            "items": mcp_items,
        },
        "plugins": {
            "status": _aggregate_status([status for status in plugin_items]),
            "items": plugin_items,
        },
        "counts": {
            "front_door_groups": len(front_door_sections),
            "clis": sum(len(names) for names in cli_items.values()),
            "apps": sum(len(names) for names in app_items.values()),
            "mcps": sum(len(names) for names in mcp_items.values()),
            "plugins": sum(len(names) for names in plugin_items.values()),
        },
    }


def print_overview_human(payload: dict[str, Any], *, as_json: bool = False) -> None:
    if as_json:
        print_json(payload)
        return

    summary = payload.get("summary", {})
    print(f"Status: {summary.get('status', 'unknown')}")
    repo_intel = payload.get("repo_intel")
    if repo_intel:
        print("")
        print("Current repo intelligence")
        print(
            f"- {repo_intel['repo_name']} [{repo_intel.get('status', 'unknown')}] "
            f"{repo_intel.get('default_mode', 'unknown')}"
        )
        print(f"- Trusted: {repo_intel.get('trusted', False)}")
        print(f"- Detail: {repo_intel.get('detail', '-')}")
        print(f"- Next: {repo_intel.get('recommended_action', '-')}")
        print(f"- computer-intel role: {repo_intel.get('computer_intel_role', 'unknown')}")
    print("")
    print("Front-door capabilities")
    front_doors = payload.get("front_doors", [])
    if not front_doors:
        print("- none")
    else:
        for group in front_doors:
            names = _format_names(group.get("items", []))
            print(f"- {group['label']} [{group.get('status', 'unknown')}] {group.get('count', 0)}: {names}")

    print("")
    print("CLIs")
    _print_status_section(payload.get("clis", {}), limit=8)

    print("")
    print("Apps / connectors")
    _print_status_section(payload.get("apps", {}), limit=8)

    print("")
    print("MCPs")
    _print_status_section(payload.get("mcps", {}), limit=8)

    print("")
    print("Plugins")
    _print_status_section(payload.get("plugins", {}), limit=8)

    print("")
    print(f"Use `{PUBLIC_COMMAND} capabilities` for the compact front door and `{PUBLIC_COMMAND} inventory show` for raw inventory.")


def _print_status_section(section: dict[str, Any], *, limit: int = 8) -> None:
    items = section.get("items", {})
    if not items:
        print("- none")
        return
    for status in _STATUS_ORDER:
        names = items.get(status, [])
        if not names:
            continue
        print(f"- {status} [{len(names)}]: {_format_names(names, limit=limit)}")
