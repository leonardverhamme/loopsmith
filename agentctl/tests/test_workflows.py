from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.workflows import run_workflow, workflow_status


CLI_ENTRY = Path(__file__).resolve().parents[1] / "agentctl.py"
REPO_ROOT = Path(__file__).resolve().parents[2]
FAKE_WORKER = REPO_ROOT / "workflow-tools" / "tests" / "fake_worker.py"


class WorkflowStatusTests(unittest.TestCase):
    def test_status_reads_schema_version(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            state_path = repo_root / ".codex-workflows" / "ui-deep-audit" / "state.json"
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "workflow_name": "ui-deep-audit",
                        "skill_name": "ui-deep-audit",
                        "repo_root": str(repo_root),
                        "checklist_path": str(repo_root / "docs" / "ui-deep-audit-checklist.md"),
                        "progress_path": str(repo_root / "docs" / "ui-deep-audit-progress.md"),
                        "status": "running",
                        "iteration": 1,
                        "max_iterations": 30,
                        "stagnant_iterations": 0,
                        "max_stagnant_iterations": 3,
                        "tasks_total": 2,
                        "tasks_done": 1,
                        "tasks_open": 1,
                        "tasks_blocked": 0,
                        "last_batch": [],
                        "last_validation": {},
                        "last_error": {},
                        "ready_allowed": False,
                        "remaining_items": [],
                        "blocked_items": [],
                        "evidence": [],
                    }
                ),
                encoding="utf-8",
            )
            result = workflow_status(repo=str(repo_root), use_registry=False)
            self.assertEqual(result["summary"]["status"], "ok")
            self.assertEqual(result["workflows"][0]["schema_version"], 1)

    def test_status_flags_complete_without_ready_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            state_path = repo_root / ".codex-workflows" / "ui-deep-audit" / "state.json"
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "workflow_name": "ui-deep-audit",
                        "skill_name": "ui-deep-audit",
                        "repo_root": str(repo_root),
                        "checklist_path": str(repo_root / "docs" / "ui-deep-audit-checklist.md"),
                        "progress_path": str(repo_root / "docs" / "ui-deep-audit-progress.md"),
                        "status": "complete",
                        "iteration": 1,
                        "max_iterations": 30,
                        "stagnant_iterations": 0,
                        "max_stagnant_iterations": 3,
                        "tasks_total": 1,
                        "tasks_done": 1,
                        "tasks_open": 0,
                        "tasks_blocked": 0,
                        "last_batch": [],
                        "last_validation": {},
                        "last_error": {},
                        "ready_allowed": False,
                        "remaining_items": [],
                        "blocked_items": [],
                        "evidence": [],
                    }
                ),
                encoding="utf-8",
            )
            result = workflow_status(repo=str(repo_root), use_registry=False)
            self.assertEqual(result["summary"]["status"], "error")
            self.assertIn("ready_allowed=true", result["workflows"][0]["errors"][0])

    def test_registry_hides_ephemeral_history_from_active_workflows(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            registry_path = Path(temp_dir) / "registry.json"
            durable_repo = Path(temp_dir) / "repo"
            durable_state = durable_repo / ".codex-workflows" / "agentctl-maintenance" / "state.json"
            durable_state.parent.mkdir(parents=True, exist_ok=True)
            durable_state.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "workflow_name": "agentctl-maintenance",
                        "skill_name": "agentctl-maintenance-engineer",
                        "repo_root": str(durable_repo),
                        "checklist_path": str(durable_repo / "docs" / "maintenance.md"),
                        "progress_path": str(durable_repo / "docs" / "maintenance-report.json"),
                        "status": "complete",
                        "iteration": 1,
                        "max_iterations": 1,
                        "stagnant_iterations": 0,
                        "max_stagnant_iterations": 1,
                        "tasks_total": 1,
                        "tasks_done": 1,
                        "tasks_open": 0,
                        "tasks_blocked": 0,
                        "last_batch": [],
                        "last_validation": {},
                        "last_error": {},
                        "ready_allowed": True,
                        "remaining_items": [],
                        "blocked_items": [],
                        "evidence": [],
                    }
                ),
                encoding="utf-8",
            )
            registry_path.write_text(
                json.dumps(
                    {
                        f"{durable_repo}::agentctl-maintenance": {
                            "workflow_name": "agentctl-maintenance",
                            "skill_name": "agentctl-maintenance-engineer",
                            "repo_root": str(durable_repo),
                            "status": "complete",
                        },
                        "C:\\Users\\leona\\AppData\\Local\\Temp\\tmp123::ui-deep-audit": {
                            "workflow_name": "ui-deep-audit",
                            "skill_name": "ui-deep-audit",
                            "repo_root": "C:\\Users\\leona\\AppData\\Local\\Temp\\tmp123",
                            "status": "error",
                        },
                    }
                ),
                encoding="utf-8",
            )

            ephemeral_repo = "C:\\Users\\leona\\AppData\\Local\\Temp\\tmp123"
            with mock.patch("lib.workflows.WORKFLOW_REGISTRY_PATH", registry_path), mock.patch(
                "lib.workflows._is_ephemeral_repo",
                side_effect=lambda repo_root: str(repo_root) == ephemeral_repo,
            ):
                result = workflow_status(repo=None, use_registry=True)

        self.assertEqual(result["summary"]["status"], "ok")
        self.assertEqual(result["summary"]["count"], 1)
        self.assertEqual(result["summary"]["historical_count"], 1)
        self.assertEqual(result["workflows"][0]["workflow_name"], "agentctl-maintenance")

    @mock.patch("lib.workflows.subprocess.run")
    @mock.patch("lib.workflows.resolve_codex_worker_command")
    def test_run_workflow_uses_codex_template_in_auto_mode(self, resolve_codex_worker_command: mock.Mock, run_mock: mock.Mock) -> None:
        resolve_codex_worker_command.return_value = "codex-template-worker"
        run_mock.return_value = mock.Mock(returncode=0)
        with tempfile.TemporaryDirectory() as temp_dir:
            rc = run_workflow(
                workflow="ui-deep-audit",
                repo=temp_dir,
                checklist=None,
                progress=None,
                worker_command=None,
                worker_mode="auto",
                max_iterations=30,
                max_stagnant=3,
            )

        self.assertEqual(rc, 0)
        command = run_mock.call_args.args[0]
        self.assertIn("--worker-command", command)
        self.assertIn("codex-template-worker", command)
        self.assertIn("--worker-mode", command)
        self.assertIn("auto", command)

    @mock.patch("lib.workflows.subprocess.run")
    @mock.patch("lib.workflows.resolve_codex_worker_command")
    def test_run_workflow_keeps_explicit_worker_command(self, resolve_codex_worker_command: mock.Mock, run_mock: mock.Mock) -> None:
        resolve_codex_worker_command.return_value = "ignored-template"
        run_mock.return_value = mock.Mock(returncode=0)
        with tempfile.TemporaryDirectory() as temp_dir:
            rc = run_workflow(
                workflow="test-deep-audit",
                repo=temp_dir,
                checklist=None,
                progress=None,
                worker_command="explicit-worker",
                worker_mode="codex",
                max_iterations=30,
                max_stagnant=3,
            )

        self.assertEqual(rc, 0)
        command = run_mock.call_args.args[0]
        self.assertIn("explicit-worker", command)
        self.assertNotIn("ignored-template", command)

    def test_cli_run_completes_end_to_end_with_fake_worker(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            env = os.environ.copy()
            env["CODEX_HOME"] = str(REPO_ROOT)
            worker_command = f'"{sys.executable}" "{FAKE_WORKER}" complete_after_two'

            run_result = subprocess.run(
                [
                    sys.executable,
                    str(CLI_ENTRY),
                    "run",
                    "ui-deep-audit",
                    "--repo",
                    str(repo_root),
                    "--worker-command",
                    worker_command,
                    "--worker-mode",
                    "explicit",
                ],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )
            self.assertEqual(run_result.returncode, 0, run_result.stderr or run_result.stdout)

            status_result = subprocess.run(
                [
                    sys.executable,
                    str(CLI_ENTRY),
                    "status",
                    "--repo",
                    str(repo_root),
                    "--json",
                ],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )
            self.assertEqual(status_result.returncode, 0, status_result.stderr or status_result.stdout)
            payload = json.loads(status_result.stdout)
            self.assertEqual(payload["workflows"][0]["status"], "complete")
            self.assertTrue(payload["workflows"][0]["ready_allowed"])


if __name__ == "__main__":
    unittest.main()
