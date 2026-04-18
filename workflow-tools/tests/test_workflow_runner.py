from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from workflow_common import load_json


RUNNER = Path(__file__).resolve().parent.parent / "workflow_runner.py"
FAKE_WORKER = Path(__file__).resolve().parent / "fake_worker.py"


class WorkflowRunnerTests(unittest.TestCase):
    def run_runner(self, repo_root: Path, skill: str, mode: str, *, max_stagnant: int = 3) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(RUNNER),
            "--skill",
            skill,
            "--repo",
            str(repo_root),
            "--worker-command",
            f'"{sys.executable}" "{FAKE_WORKER}" {mode}',
            "--max-iterations",
            "5",
            "--max-stagnant",
            str(max_stagnant),
        ]
        return subprocess.run(command, capture_output=True, text=True, check=False)

    def test_runner_initializes_and_completes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            result = self.run_runner(repo_root, "ui-deep-audit", "complete_after_two")
            self.assertEqual(result.returncode, 0, result.stderr)
            state = load_json(repo_root / ".codex-workflows" / "ui-deep-audit" / "state.json")
            self.assertEqual(state["status"], "complete")
            self.assertTrue((repo_root / "docs" / "ui-deep-audit-progress.md").exists())

    def test_runner_stalls_after_no_progress(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            result = self.run_runner(repo_root, "docs-deep-audit", "stall", max_stagnant=2)
            self.assertEqual(result.returncode, 2, result.stderr)
            state = load_json(repo_root / ".codex-workflows" / "docs-deep-audit" / "state.json")
            self.assertEqual(state["status"], "stalled")

    def test_runner_marks_blocked_after_repeated_blockers(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            result = self.run_runner(repo_root, "cicd-deep-audit", "blocked", max_stagnant=2)
            self.assertEqual(result.returncode, 2, result.stderr)
            state = load_json(repo_root / ".codex-workflows" / "cicd-deep-audit" / "state.json")
            self.assertEqual(state["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
