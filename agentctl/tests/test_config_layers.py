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

from lib import config_layers


CLI_ENTRY = Path(__file__).resolve().parents[1] / "agentctl.py"
REPO_ROOT = Path(__file__).resolve().parents[2]


class ConfigLayerTests(unittest.TestCase):
    def test_load_toml_normalizes_legacy_plugin_and_project_headers(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.toml"
            config_path.write_text(
                "\n".join(
                    [
                        "[plugins.vercel@openai-curated]",
                        "enabled = true",
                        "",
                        "[projects.C:\\Users\\leona\\Documents\\Playground\\agentctl]",
                        'trust_level = "trusted"',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            payload = config_layers._load_toml(config_path)

        self.assertTrue(payload["plugins"]["vercel@openai-curated"]["enabled"])
        self.assertEqual(
            payload["projects"][r"C:\Users\leona\Documents\Playground\agentctl"]["trust_level"],
            "trusted",
        )

    def test_effective_config_prefers_repo_over_user_over_bundled(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / ".codex"
            repo_root = Path(temp_dir) / "repo"
            codex_home.mkdir(parents=True, exist_ok=True)
            repo_root.mkdir(parents=True, exist_ok=True)

            with mock.patch.object(config_layers, "CONFIG_PATH", codex_home / "config.toml"):
                config_layers.write_scope("user", {"schema_version": 1, "browser": {"preferred_route": "cli"}})
                config_layers.write_scope("repo", {"schema_version": 1, "browser": {"preferred_route": "mcp"}}, repo=repo_root)
                effective = config_layers.effective_config(repo_root)

        self.assertEqual(effective["browser"]["preferred_route"], "mcp")
        self.assertEqual(effective["updates"]["source"], "github-release")

    def test_cli_config_set_and_show_repo_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / ".codex"
            repo_root = Path(temp_dir) / "repo"
            repo_root.mkdir(parents=True, exist_ok=True)
            env = os.environ.copy()
            env["CODEX_HOME"] = str(codex_home)

            set_result = subprocess.run(
                [
                    sys.executable,
                    str(CLI_ENTRY),
                    "config",
                    "set",
                    "browser.preferred_route",
                    "cli",
                    "--scope",
                    "repo",
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
            self.assertEqual(set_result.returncode, 0, set_result.stderr or set_result.stdout)

            show_result = subprocess.run(
                [
                    sys.executable,
                    str(CLI_ENTRY),
                    "config",
                    "show",
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
            self.assertEqual(show_result.returncode, 0, show_result.stderr or show_result.stdout)
            payload = json.loads(show_result.stdout)

        self.assertEqual(payload["effective"]["browser"]["preferred_route"], "cli")
        self.assertTrue(payload["paths"]["repo"].endswith(".agent-cli-os\\config.toml") or payload["paths"]["repo"].endswith(".agent-cli-os/config.toml"))


if __name__ == "__main__":
    unittest.main()
