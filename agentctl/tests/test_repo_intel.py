from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import repo_intel


class RepoIntelTests(unittest.TestCase):
    def _runtime_ok(self) -> dict:
        return {
            "name": "graphify",
            "command": "graphify",
            "path": r"C:\tools\graphify.exe",
            "installed": True,
            "status": "ok",
            "version": "graphify v4",
        }

    def _obsidian_ok(self) -> dict:
        return {
            "name": "obsidian",
            "command": "obsidian",
            "path": r"C:\Program Files\Obsidian\Obsidian.exe",
            "installed": True,
            "status": "ok",
        }

    def _seed_repo(self, root: Path) -> None:
        root.mkdir(parents=True, exist_ok=True)
        (root / "app.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
        (root / "README.md").write_text("# Repo\n", encoding="utf-8")

    def _write_graph_artifacts(self, root: Path) -> None:
        graph_dir = root / "graphify-out"
        graph_dir.mkdir(parents=True, exist_ok=True)
        (graph_dir / "graph.json").write_text(json.dumps({"nodes": [], "links": []}), encoding="utf-8")
        (graph_dir / "GRAPH_REPORT.md").write_text("# Graph Report\n\nHealthy.\n", encoding="utf-8")

    def _write_manifest(self, root: Path) -> None:
        config = repo_intel._repo_intel_config(root)
        (root / ".graphifyignore").write_text(repo_intel.GRAPHIFYIGNORE_TEMPLATE, encoding="utf-8")
        (root / ".gitignore").write_text(repo_intel.GITIGNORE_TEMPLATE, encoding="utf-8")
        (root / "AGENTS.md").write_text(repo_intel._repo_intel_agents_block(), encoding="utf-8")
        code_files, semantic_files = repo_intel._iter_repo_files(root)
        manifest = repo_intel._repo_intel_manifest(
            root,
            config=config,
            graphify=self._runtime_ok(),
            code_fingerprint=repo_intel._fingerprint(code_files, root),
            semantic_fingerprint=repo_intel._fingerprint(semantic_files, root),
            graph_paths=repo_intel.repo_intel_graph_paths(root),
            obsidian_export_path=None,
        )
        repo_intel.save_json(repo_intel.repo_intel_manifest_path(root), manifest)

    def _patch_runtime(self, registry_path: Path | None = None) -> ExitStack:
        stack = ExitStack()
        stack.enter_context(mock.patch.object(repo_intel, "detect_graphify_runtime", return_value=self._runtime_ok()))
        stack.enter_context(mock.patch.object(repo_intel, "detect_obsidian_runtime", return_value=self._obsidian_ok()))
        stack.enter_context(mock.patch.object(repo_intel, "effective_config", return_value={}))
        if registry_path is not None:
            stack.enter_context(mock.patch.object(repo_intel, "WORKSPACE_REGISTRY_PATH", registry_path))
        return stack

    def test_status_missing_when_required_artifacts_are_absent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json"):
                payload = repo_intel.repo_intel_status(repo_root)
        self.assertEqual(payload["status"], "missing")
        self.assertEqual(payload["recommended_action"], "agentcli repo-intel ensure")
        self.assertEqual(payload["policy"]["default_mode"], "repo-first")
        self.assertEqual(payload["policy"]["computer_intel_role"], "exception-only")
        self.assertTrue(any("current local branch as canonical" in item for item in payload["policy"]["agent_path"]))
        self.assertTrue(any("worktrees as temporary isolation" in item for item in payload["policy"]["agent_path"]))

    def test_status_marks_trusted_repo_as_auto_ensure_on_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json") as stack:
                stack.enter_context(mock.patch.object(repo_intel, "_trusted_repo_root_strings", return_value={str(repo_root.resolve())}))
                payload = repo_intel.repo_intel_status(repo_root)

        self.assertTrue(payload["trusted"])
        self.assertTrue(payload["policy"]["auto_ensure_on_entry"])

    def test_repo_root_resolves_enclosing_git_root_from_nested_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            nested = repo_root / "src" / "feature"
            self._seed_repo(repo_root)
            nested.mkdir(parents=True, exist_ok=True)
            (repo_root / ".git").mkdir()

            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json"):
                payload = repo_intel.repo_intel_status(nested)

        self.assertEqual(payload["repo_root"], str(repo_root.resolve()))
        self.assertEqual(payload["repo_name"], "repo")

    def test_status_fresh_when_manifest_matches_repo_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)
            self._write_graph_artifacts(repo_root)
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json"):
                self._write_manifest(repo_root)
                payload = repo_intel.repo_intel_status(repo_root)
        self.assertEqual(payload["status"], "fresh")

    def test_status_stale_code_when_code_fingerprint_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)
            self._write_graph_artifacts(repo_root)
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json"):
                self._write_manifest(repo_root)
                (repo_root / "app.py").write_text("def run():\n    return 'changed'\n", encoding="utf-8")
                payload = repo_intel.repo_intel_status(repo_root)
        self.assertEqual(payload["status"], "stale_code")

    def test_status_stale_semantic_when_docs_change(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)
            self._write_graph_artifacts(repo_root)
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json"):
                self._write_manifest(repo_root)
                (repo_root / "README.md").write_text("# Repo\n\nChanged.\n", encoding="utf-8")
                payload = repo_intel.repo_intel_status(repo_root)
        self.assertEqual(payload["status"], "stale_semantic")

    def test_status_stale_config_when_graphifyignore_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)
            self._write_graph_artifacts(repo_root)
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json"):
                self._write_manifest(repo_root)
                (repo_root / ".graphifyignore").write_text("dist/\n", encoding="utf-8")
                payload = repo_intel.repo_intel_status(repo_root)
        self.assertEqual(payload["status"], "stale_config")

    def test_status_stale_config_when_agents_hint_is_outdated(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)
            self._write_graph_artifacts(repo_root)
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json"):
                self._write_manifest(repo_root)
                (repo_root / "AGENTS.md").write_text("# Old guidance\n", encoding="utf-8")
                payload = repo_intel.repo_intel_status(repo_root)
        self.assertEqual(payload["status"], "stale_config")
        self.assertIn("AGENTS guidance", payload["detail"])

    def test_status_stale_config_when_gitignore_hygiene_is_outdated(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)
            self._write_graph_artifacts(repo_root)
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json"):
                self._write_manifest(repo_root)
                (repo_root / ".gitignore").write_text("coverage/\n", encoding="utf-8")
                payload = repo_intel.repo_intel_status(repo_root)
        self.assertEqual(payload["status"], "stale_config")
        self.assertIn(".gitignore", payload["detail"])

    def test_status_broken_when_graph_json_is_unreadable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)
            graph_dir = repo_root / "graphify-out"
            graph_dir.mkdir(parents=True, exist_ok=True)
            (graph_dir / "graph.json").write_text("{", encoding="utf-8")
            (graph_dir / "GRAPH_REPORT.md").write_text("# Graph Report\n", encoding="utf-8")
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json"):
                payload = repo_intel.repo_intel_status(repo_root)
        self.assertEqual(payload["status"], "broken")

    def test_ensure_builds_missing_repo_and_creates_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)

            def fake_stream(command: list[str], *, cwd: Path) -> dict:
                self._write_graph_artifacts(cwd)
                return {"ok": True, "returncode": 0, "stderr": ""}

            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json") as stack:
                stack.enter_context(mock.patch.object(repo_intel, "_stream_command", side_effect=fake_stream))
                payload = repo_intel.repo_intel_ensure(repo_root)

            self.assertEqual(payload["status"], "fresh")
            self.assertEqual(payload["action"], "built")
            self.assertTrue((repo_root / ".graphifyignore").exists())
            self.assertTrue((repo_root / ".gitignore").exists())
            self.assertTrue((repo_root / "AGENTS.md").exists())
            self.assertTrue(repo_intel.repo_intel_manifest_path(repo_root).exists())
            agents_text = (repo_root / "AGENTS.md").read_text(encoding="utf-8")
            gitignore_text = (repo_root / ".gitignore").read_text(encoding="utf-8")

        self.assertIn("default working universe", agents_text)
        self.assertIn("agentcli repo-intel status", agents_text)
        self.assertIn("agentcli computer-intel", agents_text)
        self.assertIn("current local branch as the canonical place", agents_text)
        self.assertIn("worktrees as temporary isolation", agents_text)
        self.assertIn("agentcli:repo-hygiene:start", gitignore_text)
        self.assertIn("playwright-report/", gitignore_text)

    def test_ensure_repairs_agents_hint_without_triggering_graph_rebuild(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)
            self._write_graph_artifacts(repo_root)
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json") as stack:
                self._write_manifest(repo_root)
                (repo_root / "AGENTS.md").write_text("# stale\n", encoding="utf-8")
                stream = stack.enter_context(mock.patch.object(repo_intel, "_stream_command"))
                payload = repo_intel.repo_intel_ensure(repo_root)

            self.assertEqual(payload["status"], "fresh")
            self.assertEqual(payload["action"], "noop")
            stream.assert_not_called()

    def test_ensure_repairs_gitignore_hygiene_without_triggering_graph_rebuild(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)
            self._write_graph_artifacts(repo_root)
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json") as stack:
                self._write_manifest(repo_root)
                (repo_root / ".gitignore").write_text("coverage/\n", encoding="utf-8")
                stream = stack.enter_context(mock.patch.object(repo_intel, "_stream_command"))
                payload = repo_intel.repo_intel_ensure(repo_root)

            self.assertEqual(payload["status"], "fresh")
            self.assertEqual(payload["action"], "noop")
            stream.assert_not_called()

    def test_ensure_accepts_graphify_no_viz_failures_when_core_artifacts_refresh(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)

            def fake_stream(command: list[str], *, cwd: Path) -> dict:
                self._write_graph_artifacts(cwd)
                return {"ok": False, "returncode": 1, "stderr": ""}

            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json") as stack:
                stack.enter_context(mock.patch.object(repo_intel, "_stream_command", side_effect=fake_stream))
                payload = repo_intel.repo_intel_ensure(repo_root)

            self.assertEqual(payload["status"], "fresh")
            self.assertEqual(payload["action"], "built-no-viz")

    def test_ensure_uses_code_only_update_for_stale_code(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)
            self._write_graph_artifacts(repo_root)
            (repo_root / ".graphifyignore").write_text(repo_intel.GRAPHIFYIGNORE_TEMPLATE, encoding="utf-8")

            def fake_stream(command: list[str], *, cwd: Path) -> dict:
                self.assertEqual(command[:2], ["graphify", "update"])
                self._write_graph_artifacts(cwd)
                return {"ok": True, "returncode": 0, "stderr": ""}

            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json") as stack:
                self._write_manifest(repo_root)
                (repo_root / "app.py").write_text("def run():\n    return 'changed'\n", encoding="utf-8")
                stack.enter_context(mock.patch.object(repo_intel, "_stream_command", side_effect=fake_stream))
                payload = repo_intel.repo_intel_ensure(repo_root)

        self.assertEqual(payload["status"], "fresh")
        self.assertEqual(payload["action"], "updated")

    def test_audit_aggregates_multiple_repos(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_one = Path(temp_dir) / "repo-one"
            repo_two = Path(temp_dir) / "repo-two"
            self._seed_repo(repo_one)
            self._seed_repo(repo_two)
            self._write_graph_artifacts(repo_two)
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json") as stack:
                self._write_manifest(repo_two)
                stack.enter_context(mock.patch.object(repo_intel, "trusted_repo_paths", return_value=[repo_one, repo_two]))
                payload = repo_intel.repo_intel_audit(all_trusted=True)

        self.assertEqual(payload["summary"]["repo_count"], 2)
        self.assertEqual(payload["summary"]["counts"]["missing"], 1)
        self.assertEqual(payload["summary"]["counts"]["fresh"], 1)

    def test_audit_can_include_discovered_repos_but_only_fix_trusted_ones(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            trusted_repo = Path(temp_dir) / "trusted-repo"
            discovered_repo = Path(temp_dir) / "discovered-repo"
            self._seed_repo(trusted_repo)
            self._seed_repo(discovered_repo)
            self._write_graph_artifacts(trusted_repo)
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json") as stack:
                self._write_manifest(trusted_repo)
                stack.enter_context(mock.patch.object(repo_intel, "trusted_repo_paths", return_value=[trusted_repo]))
                stack.enter_context(mock.patch.object(repo_intel, "discovered_repo_paths", return_value=[trusted_repo, discovered_repo]))
                payload = repo_intel.repo_intel_audit(all_trusted=True, all_discovered=True, fix=True)

        self.assertEqual(payload["summary"]["repo_count"], 2)
        by_name = {item["repo_name"]: item for item in payload["repos"]}
        self.assertEqual(by_name["trusted-repo"]["status"], "fresh")
        self.assertTrue(by_name["trusted-repo"]["trusted"])
        self.assertEqual(by_name["discovered-repo"]["status"], "missing")
        self.assertFalse(by_name["discovered-repo"]["trusted"])
        self.assertIn("Auto-fix skipped", by_name["discovered-repo"]["detail"])

    def test_discovered_repo_paths_excludes_non_audit_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            registry_path = Path(temp_dir) / "computer-graph.json"
            user_repo = Path(temp_dir) / "user-repo"
            transient_repo = Path(temp_dir) / ".wq" / "temp-repo"
            user_repo.mkdir(parents=True, exist_ok=True)
            transient_repo.mkdir(parents=True, exist_ok=True)
            repo_intel.save_json(
                registry_path,
                {
                    "repos": [
                        {"path": str(user_repo), "audit_candidate": True},
                        {"path": str(transient_repo), "audit_candidate": False},
                    ]
                },
            )

            with mock.patch.object(repo_intel, "COMPUTER_GRAPH_PATH", registry_path):
                paths = repo_intel.discovered_repo_paths()

        self.assertEqual(paths, [user_repo.resolve()])

    def test_trusted_repo_paths_only_returns_real_repo_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            folder_root = Path(temp_dir) / "folder"
            repo_root.mkdir(parents=True, exist_ok=True)
            folder_root.mkdir(parents=True, exist_ok=True)
            (repo_root / ".git").mkdir()
            config_path = Path(temp_dir) / "config.toml"
            config_path.write_text(
                "\n".join(
                    [
                        f'[projects."{repo_root}"]',
                        'trust_level = "trusted"',
                        "",
                        f'[projects."{folder_root}"]',
                        'trust_level = "trusted"',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            with mock.patch.object(repo_intel, "CONFIG_PATH", config_path):
                trusted = repo_intel.trusted_repo_paths()

        self.assertEqual(trusted, [repo_root.resolve()])

    def test_status_does_not_register_untrusted_repo_in_workspace_registry(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            registry_path = Path(temp_dir) / "workspace-graph.json"
            self._seed_repo(repo_root)
            with self._patch_runtime(registry_path) as stack:
                stack.enter_context(mock.patch.object(repo_intel, "_trusted_repo_root_strings", return_value=set()))
                payload = repo_intel.repo_intel_status(repo_root)
        self.assertEqual(payload["status"], "missing")
        self.assertFalse(registry_path.exists())

    def test_audit_prunes_untrusted_workspace_registry_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "trusted-repo"
            registry_path = Path(temp_dir) / "workspace-graph.json"
            stale_registry = {
                "schema_version": 1,
                "generated_at": "2026-04-20T00:00:00+00:00",
                "repos": [
                    {
                        "repo_root": str(Path(temp_dir) / "tmp-repo"),
                        "repo_name": "tmp-repo",
                        "status": "missing",
                        "graph_json": str(Path(temp_dir) / "tmp-repo" / "graphify-out" / "graph.json"),
                        "graph_report": str(Path(temp_dir) / "tmp-repo" / "graphify-out" / "GRAPH_REPORT.md"),
                        "manifest_path": str(Path(temp_dir) / "tmp-repo" / ".agentcli" / "repo-intel.json"),
                        "graphify_version": None,
                        "last_successful_build_at": None,
                        "obsidian_export_path": None,
                        "last_audited_at": "2026-04-20T00:00:00+00:00",
                    }
                ],
            }
            repo_intel.save_json(registry_path, stale_registry)
        with self._patch_runtime(registry_path) as stack:
            stack.enter_context(mock.patch.object(repo_intel, "_trusted_repo_root_strings", return_value={str(repo_root)}))
            repo_intel._sync_workspace_registry(
                {
                        "repo_root": str(repo_root),
                        "repo_name": repo_root.name,
                        "status": "fresh",
                        "graph_paths": repo_intel.repo_intel_graph_paths(repo_root),
                        "manifest_path": str(repo_intel.repo_intel_manifest_path(repo_root)),
                        "manifest": {
                            "graphify_version": "graphify v4",
                            "last_successful_build_at": "2026-04-20T00:00:00+00:00",
                            "obsidian_export_path": None,
                        },
                }
            )
        registry = repo_intel.load_json(registry_path, default={})
        self.assertFalse(any(item.get("repo_root", "").endswith("tmp-repo") for item in registry.get("repos", [])))

    def test_workspace_registry_salvages_concatenated_json_and_rewrites_clean_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            registry_path = Path(temp_dir) / "workspace-graph.json"
            valid = {
                "schema_version": 1,
                "generated_at": "2026-04-21T00:00:00+00:00",
                "repos": [
                    {
                        "repo_root": r"C:\repo",
                        "repo_name": "repo",
                        "status": "fresh",
                        "graph_json": r"C:\repo\graphify-out\graph.json",
                        "graph_report": r"C:\repo\graphify-out\GRAPH_REPORT.md",
                        "manifest_path": r"C:\repo\.agentcli\repo-intel.json",
                        "graphify_version": "graphify v4",
                        "last_successful_build_at": "2026-04-21T00:00:00+00:00",
                        "obsidian_export_path": None,
                        "last_audited_at": "2026-04-21T00:00:00+00:00",
                    }
                ],
            }
            registry_path.write_text(
                json.dumps(valid, indent=2) + "\n" + json.dumps({"unexpected": True}, indent=2) + "\n",
                encoding="utf-8",
            )

            with self._patch_runtime(registry_path):
                payload = repo_intel._workspace_registry()

            self.assertEqual(len(payload["repos"]), 1)
            repaired = json.loads(registry_path.read_text(encoding="utf-8"))
            self.assertEqual(repaired["schema_version"], 1)
            self.assertEqual(len(repaired["repos"]), 1)
            self.assertEqual(repaired["repos"][0]["repo_name"], "repo")

    def test_workspace_registry_resets_to_default_when_unreadable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            registry_path = Path(temp_dir) / "workspace-graph.json"
            registry_path.write_text("{ definitely not json", encoding="utf-8")

            with self._patch_runtime(registry_path):
                payload = repo_intel._workspace_registry()

            self.assertEqual(payload["schema_version"], 1)
            self.assertEqual(payload["repos"], [])
            repaired = json.loads(registry_path.read_text(encoding="utf-8"))
            self.assertEqual(repaired["repos"], [])

    def test_serve_blocks_without_graph(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json"):
                payload = repo_intel.repo_intel_serve(repo_root)
        self.assertEqual(payload["action"], "blocked")

    def test_serve_returns_command_when_graph_is_healthy(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            self._seed_repo(repo_root)
            self._write_graph_artifacts(repo_root)
            with self._patch_runtime(Path(temp_dir) / "workspace-graph.json") as stack:
                self._write_manifest(repo_root)
                stack.enter_context(
                    mock.patch.object(
                        repo_intel,
                        "_graphify_serve_command",
                        return_value=[sys.executable, "-m", "graphify.serve", str(repo_root / "graphify-out" / "graph.json")],
                    )
                )
                payload = repo_intel.repo_intel_serve(repo_root)
        self.assertEqual(payload["action"], "ready")
        self.assertIn("graphify.serve", " ".join(payload["command"]))


if __name__ == "__main__":
    unittest.main()
