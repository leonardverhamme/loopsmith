from __future__ import annotations

import argparse
import sys
from pathlib import Path

from workflow_common import ensure_parent, load_json, parse_checklist, render_progress_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Render human-readable progress from workflow state.")
    parser.add_argument("--state", required=True, help="Path to .codex-workflows/<workflow>/state.json")
    parser.add_argument("--output", help="Optional output path. Defaults to state.progress_path.")
    parser.add_argument("--stdout", action="store_true", help="Print the rendered markdown to stdout.")
    args = parser.parse_args()

    state = load_json(args.state)
    checklist = parse_checklist(state["checklist_path"])
    rendered = render_progress_markdown(state, checklist)

    output_path = Path(args.output) if args.output else Path(state["progress_path"])
    ensure_parent(output_path).write_text(rendered, encoding="utf-8")

    if args.stdout:
        print(rendered, end="")
    else:
        print(output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
