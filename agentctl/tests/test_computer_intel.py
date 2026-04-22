from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import computer_intel


class ComputerIntelTests(unittest.TestCase):
    def test_status_missing_when_registry_is_absent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "computer-graph.json"
            root = Path(temp_dir) / "root"
            root.mkdir(parents=True, exist_ok=True)
            with mock.patch.object(computer_intel, "COMPUTER_GRAPH_PATH", state_path), mock.patch.object(
                computer_intel, "_default_roots", return_value=[root]
            ), mock.patch.object(
                computer_intel, "effective_config", return_value={"computer_intel": {"enabled": True, "scan_scope": "laptop", "directory_budget": 1000, "search_limit": 20, "live_search_limit": 20}}
            ):
                payload = computer_intel.computer_intel_status()

        self.assertEqual(payload["status"], "missing")
        self.assertEqual(payload["recommended_action"], "agentcli computer-intel refresh")

    def test_refresh_discovers_repos_vaults_graphs_and_services(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "scan-root"
            repo_root = root / "repo-one"
            vault_root = root / "vault-one"
            service_root = root / "service-one"
            repo_root.mkdir(parents=True, exist_ok=True)
            vault_root.mkdir(parents=True, exist_ok=True)
            service_root.mkdir(parents=True, exist_ok=True)
            (repo_root / ".git").mkdir()
            (repo_root / ".agentcli").mkdir()
            (repo_root / "graphify-out").mkdir()
            (repo_root / "graphify-out" / "graph.json").write_text("{}", encoding="utf-8")
            (repo_root / "graphify-out" / "GRAPH_REPORT.md").write_text("# Report\n", encoding="utf-8")
            (repo_root / ".git" / "config").write_text('[remote "origin"]\nurl = https://example.com/repo-one.git\n', encoding="utf-8")
            (vault_root / ".obsidian").mkdir()
            (service_root / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")
            state_path = Path(temp_dir) / "computer-graph.json"

            with mock.patch.object(computer_intel, "COMPUTER_GRAPH_PATH", state_path), mock.patch.object(
                computer_intel, "_default_roots", return_value=[root]
            ), mock.patch.object(
                computer_intel, "trusted_projects", return_value=[{"path": str(repo_root), "trust_level": "trusted"}]
            ), mock.patch.object(
                computer_intel, "repo_intel_status", return_value={"status": "fresh", "detail": "ok"}
            ), mock.patch.object(
                computer_intel, "effective_config", return_value={"computer_intel": {"enabled": True, "scan_scope": "laptop", "directory_budget": 5000, "search_limit": 20, "live_search_limit": 20}}
            ):
                payload = computer_intel.computer_intel_refresh()

                self.assertTrue(state_path.exists())
                persisted = json.loads(state_path.read_text(encoding="utf-8"))
                self.assertEqual(persisted["summary"]["repo_count"], 1)

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["summary"]["repo_count"], 1)
        self.assertEqual(payload["summary"]["audit_candidate_repo_count"], 1)
        self.assertEqual(payload["summary"]["vault_count"], 1)
        self.assertEqual(payload["summary"]["graph_count"], 1)
        self.assertEqual(payload["summary"]["service_count"], 1)
        self.assertEqual(payload["summary"]["trusted_repo_count"], 1)

    def test_search_reads_registry_and_live_matches(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "scan-root"
            repo_root = root / "tenant-service-project"
            repo_root.mkdir(parents=True, exist_ok=True)
            file_path = root / "tenant-service-notes.md"
            file_path.write_text("notes\n", encoding="utf-8")
            state_path = Path(temp_dir) / "computer-graph.json"
            state_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "generated_at": "2026-04-21T00:00:00+00:00",
                        "status": "ok",
                        "detail": "ready",
                        "summary": {"root_count": 1, "repo_count": 1, "trusted_repo_count": 0, "managed_repo_count": 0, "vault_count": 0, "graph_count": 0, "service_count": 0, "truncated": False},
                        "roots": [{"kind": "root", "name": "scan-root", "path": str(root)}],
                        "repos": [{"kind": "repo", "name": repo_root.name, "path": str(repo_root), "trusted": False, "managed": False, "repo_intel_status": "discovered"}],
                        "vaults": [],
                        "graphs": [],
                        "services": [],
                        "scan_stats": {"scanned_directories": 1, "skipped_directories": 0, "inaccessible_directories": 0, "truncated": False, "directory_budget": 1000},
                        "config": {"enabled": True},
                    }
                ),
                encoding="utf-8",
            )

            with mock.patch.object(computer_intel, "COMPUTER_GRAPH_PATH", state_path), mock.patch.object(
                computer_intel, "effective_config", return_value={"computer_intel": {"enabled": True, "scan_scope": "laptop", "directory_budget": 5000, "search_limit": 20, "live_search_limit": 20}}
            ):
                payload = computer_intel.computer_intel_search("tenant service", kind="all", limit=10)

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["summary"]["registry_match_count"], 1)
        self.assertTrue(any(item.get("path") == str(repo_root) for item in payload["registry_matches"]))
        self.assertTrue(any(item.get("path") == str(file_path) for item in payload["live_matches"]))

    def test_discovered_repo_paths_excludes_transient_repo_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "computer-graph.json"
            trusted_repo = Path(temp_dir) / "repo"
            transient_repo = Path(temp_dir) / ".wq" / "temp-repo"
            trusted_repo.mkdir(parents=True, exist_ok=True)
            transient_repo.mkdir(parents=True, exist_ok=True)
            state_path.write_text(
                json.dumps(
                    {
                        "repos": [
                            {
                                "kind": "repo",
                                "name": trusted_repo.name,
                                "path": str(trusted_repo),
                                "repo_scope": "user",
                                "audit_candidate": True,
                            },
                            {
                                "kind": "repo",
                                "name": transient_repo.name,
                                "path": str(transient_repo),
                                "repo_scope": "transient",
                                "audit_candidate": False,
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            with mock.patch.object(computer_intel, "COMPUTER_GRAPH_PATH", state_path):
                paths = computer_intel.discovered_repo_paths()

        self.assertEqual(paths, [trusted_repo.resolve()])

    def test_repo_scope_marks_editor_task_checkpoints_as_transient(self) -> None:
        checkpoint_repo = Path(
            r"C:\Users\leona\AppData\Roaming\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\tasks\019c8abf-6b36-72f8-80c5-8b908c63b563\checkpoints"
        )

        scope = computer_intel._repo_scope(checkpoint_repo)

        self.assertEqual(scope, "transient")


if __name__ == "__main__":
    unittest.main()
