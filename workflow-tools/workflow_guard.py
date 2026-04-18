from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from workflow_common import load_json, parse_checklist, validate_state_payload


def evaluate_guard(state_path: str | Path) -> tuple[int, str, dict]:
    try:
        state = load_json(state_path)
    except Exception as exc:  # pragma: no cover - defensive entrypoint guard
        return 3, f"failed to read state: {exc}", {}

    errors = validate_state_payload(state)
    if errors:
        return 3, "; ".join(errors), state

    checklist = parse_checklist(state["checklist_path"])
    if not checklist["exists"]:
        return 3, "checklist file does not exist", state

    mismatches = []
    for field, actual in (
        ("tasks_total", checklist["total"]),
        ("tasks_done", checklist["done"]),
        ("tasks_open", checklist["open"]),
        ("tasks_blocked", checklist["blocked"]),
    ):
        if state.get(field) != actual:
            mismatches.append(f"{field}={state.get(field)} expected {actual}")

    visible = checklist["visible_counts"]
    visible_map = {
        "unchecked": checklist["open"],
        "open": checklist["open"],
        "checked": checklist["done"],
        "done": checklist["done"],
        "blocked": checklist["blocked"],
    }
    for label, expected in visible_map.items():
        if label in visible and visible[label] != expected:
            mismatches.append(f"visible {label}={visible[label]} expected {expected}")

    if state.get("status") == "complete" and checklist["open"] > 0:
        mismatches.append("state says complete but checklist still has open items")

    if mismatches:
        return 3, "; ".join(mismatches), state

    if checklist["open"] == 0 and checklist["blocked"] == 0:
        return 0, "all checklist items complete; ready allowed", state

    if checklist["open"] > 0 and checklist["blocked"] == checklist["open"]:
        return 2, "all remaining items are blocked", state

    if state.get("status") in {"blocked", "stalled", "error"} and checklist["open"] > 0:
        return 2, f"workflow status is {state['status']} with open items remaining", state

    return 1, "unchecked items remain", state


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic stop-rule checker for deep-skill workflows.")
    parser.add_argument("--state", required=True, help="Path to .codex-workflows/<workflow>/state.json")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of plain text")
    args = parser.parse_args()

    code, message, state = evaluate_guard(args.state)
    if args.json:
        print(
            json.dumps(
                {
                    "exit_code": code,
                    "message": message,
                    "workflow_name": state.get("workflow_name"),
                    "status": state.get("status"),
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print(message)
    return code


if __name__ == "__main__":
    sys.exit(main())
