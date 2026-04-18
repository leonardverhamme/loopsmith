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

    def test_parallel_runners_share_registry_without_losing_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            registry = root / "workflow-state" / "registry.json"
            repo_a = root / "repo-a"
            repo_b = root / "repo-b"

            command_a = [
                sys.executable,
                str(RUNNER),
                "--skill",
                "docs-deep-audit",
                "--repo",
                str(repo_a),
                "--worker-command",
                f'"{sys.executable}" "{FAKE_WORKER}" stall',
                "--max-iterations",
                "5",
                "--max-stagnant",
                "2",
                "--registry",
                str(registry),
            ]
            command_b = [
                sys.executable,
                str(RUNNER),
                "--skill",
                "cicd-deep-audit",
                "--repo",
                str(repo_b),
                "--worker-command",
                f'"{sys.executable}" "{FAKE_WORKER}" blocked',
                "--max-iterations",
                "5",
                "--max-stagnant",
                "2",
                "--registry",
                str(registry),
            ]

            proc_a = subprocess.Popen(command_a, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            proc_b = subprocess.Popen(command_b, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out_a, err_a = proc_a.communicate(timeout=20)
            out_b, err_b = proc_b.communicate(timeout=20)

            self.assertEqual(proc_a.returncode, 2, err_a or out_a)
            self.assertEqual(proc_b.returncode, 2, err_b or out_b)

            registry_payload = load_json(registry)
            self.assertIn(f"{repo_a.resolve()}::docs-deep-audit", registry_payload)
            self.assertIn(f"{repo_b.resolve()}::cicd-deep-audit", registry_payload)


if __name__ == "__main__":
    unittest.main()
