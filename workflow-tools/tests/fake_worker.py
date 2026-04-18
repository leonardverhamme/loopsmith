from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def write_text(path: str, content: str) -> None:
    resolved = Path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(content, encoding="utf-8")


def main() -> int:
    mode = sys.argv[1]
    state_path = Path(os.environ["CODEX_WORKFLOW_STATE"])
    checklist_path = Path(os.environ["CODEX_WORKFLOW_CHECKLIST"])
    iteration = int(os.environ["CODEX_WORKFLOW_ITERATION"])
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["last_validation"] = {"worker_mode": mode, "iteration": iteration}

    if mode == "complete_after_two":
        if iteration == 1:
            write_text(
                checklist_path,
                "# Checklist\n\n## Status\n\n- Unchecked: 1\n- Checked: 1\n\n- [x] first item\n- [ ] second item\n",
            )
        else:
            write_text(
                checklist_path,
                "# Checklist\n\n## Status\n\n- Unchecked: 0\n- Checked: 2\n\n- [x] first item\n- [x] second item\n",
            )
    elif mode == "stall":
        write_text(
            checklist_path,
            "# Checklist\n\n## Status\n\n- Unchecked: 1\n- Checked: 0\n\n- [ ] unresolved item\n",
        )
    elif mode == "blocked":
        write_text(
            checklist_path,
            "# Checklist\n\n## Status\n\n- Unchecked: 1\n- Checked: 0\n- Blocked: 1\n\n- [ ] blocked item\n  Blocked: waiting on external system\n",
        )
    else:
        raise SystemExit(f"unknown mode: {mode}")

    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
