from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.guidance import build_guidance_snapshot


class GuidanceTests(unittest.TestCase):
    def test_guidance_snapshot_tracks_files_and_budget(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            user_dir = root / "user-guidance"
            repo_dir = root / "repo-guidance"
            user_dir.mkdir(parents=True, exist_ok=True)
            repo_dir.mkdir(parents=True, exist_ok=True)
            (user_dir / "style.md").write_text("# Style\nKeep menus short.\n", encoding="utf-8")
            (repo_dir / "repo.md").write_text("# Repo\nPrefer repo-native commands.\n", encoding="utf-8")

            with mock.patch("lib.guidance.effective_config") as effective_config:
                effective_config.return_value = {
                    "guidance": {
                        "user_dir": str(user_dir),
                        "repo_dir": str(repo_dir),
                        "max_files": 4,
                        "max_total_lines": 20,
                    }
                }
                snapshot = build_guidance_snapshot(repo=root)

        self.assertEqual(snapshot["summary"]["status"], "ok")
        self.assertEqual(snapshot["summary"]["file_count"], 2)
        self.assertTrue(snapshot["summary"]["within_budget"])

    def test_guidance_snapshot_degrades_when_budget_is_exceeded(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo_dir = root / "repo-guidance"
            repo_dir.mkdir(parents=True, exist_ok=True)
            (repo_dir / "one.md").write_text("line 1\nline 2\nline 3\n", encoding="utf-8")
            (repo_dir / "two.md").write_text("line 1\nline 2\nline 3\n", encoding="utf-8")

            with mock.patch("lib.guidance.effective_config") as effective_config:
                effective_config.return_value = {
                    "guidance": {
                        "user_dir": "",
                        "repo_dir": str(repo_dir),
                        "max_files": 1,
                        "max_total_lines": 4,
                    }
                }
                snapshot = build_guidance_snapshot(repo=root)

        self.assertEqual(snapshot["summary"]["status"], "degraded")
        self.assertFalse(snapshot["summary"]["within_budget"])


if __name__ == "__main__":
    unittest.main()
