from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import workflow_common
from workflow_common import default_state, save_json
from workflow_guard import evaluate_guard


class WorkflowGuardTests(unittest.TestCase):
    def test_save_json_retries_after_permission_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "state.json"
            payload = {"ok": True}
            real_replace = workflow_common.os.replace
            calls = {"count": 0}

            def flaky_replace(src: Path, dst: Path) -> None:
                if calls["count"] == 0:
                    calls["count"] += 1
                    raise PermissionError("file locked")
                real_replace(src, dst)

            with mock.patch.object(workflow_common.os, "replace", side_effect=flaky_replace):
                save_json(target, payload)

            self.assertEqual(json.loads(target.read_text(encoding="utf-8")), payload)

    def test_complete_when_all_items_checked(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            checklist_path = repo_root / "docs" / "ui-deep-audit-checklist.md"
            checklist_path.parent.mkdir(parents=True, exist_ok=True)
            checklist_path.write_text("- [x] done\n", encoding="utf-8")
            state_path = repo_root / ".codex-workflows" / "ui-deep-audit" / "state.json"
            state = default_state(
                workflow_name="ui-deep-audit",
                skill_name="ui-deep-audit",
                repo_root=repo_root,
                checklist_path=checklist_path,
                progress_path=repo_root / "docs" / "ui-deep-audit-progress.md",
            )
            state.update({"tasks_total": 1, "tasks_done": 1, "tasks_open": 0, "tasks_blocked": 0})
            save_json(state_path, state)

            code, _, _ = evaluate_guard(state_path)
            self.assertEqual(code, 0)

    def test_invalid_when_state_counts_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            checklist_path = repo_root / "docs" / "test-deep-audit-checklist.md"
            checklist_path.parent.mkdir(parents=True, exist_ok=True)
            checklist_path.write_text("- [ ] open\n", encoding="utf-8")
            state_path = repo_root / ".codex-workflows" / "test-deep-audit" / "state.json"
            state = default_state(
                workflow_name="test-deep-audit",
                skill_name="test-deep-audit",
                repo_root=repo_root,
                checklist_path=checklist_path,
                progress_path=repo_root / "docs" / "test-deep-audit-progress.md",
            )
            state.update({"tasks_total": 1, "tasks_done": 1, "tasks_open": 0, "tasks_blocked": 0})
            save_json(state_path, state)

            code, _, _ = evaluate_guard(state_path)
            self.assertEqual(code, 3)


if __name__ == "__main__":
    unittest.main()
