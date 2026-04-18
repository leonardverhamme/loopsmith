from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.skills_ops import _normalize_source, _sync_local_entries, update_skills


class SkillsOpsTests(unittest.TestCase):
    def test_normalize_github_source_with_ref(self) -> None:
        source, ref = _normalize_source("vercel-labs/agent-skills", "main")
        self.assertEqual(source, "https://github.com/vercel-labs/agent-skills.git")
        self.assertEqual(ref, "main")

    def test_local_source_with_ref_raises(self) -> None:
        with self.assertRaises(ValueError):
            _normalize_source(str(Path.cwd()), "main")

    @mock.patch("lib.skills_ops._discover_local_skill_names", return_value={"ui-skill", "test-skill"})
    def test_sync_local_entries_tracks_local_skills(self, discover_local_skills: mock.Mock) -> None:
        lock = {
            "schema_version": 2,
            "updated_at": None,
            "entries": [
                {
                    "kind": "managed",
                    "scope": "global",
                    "source": "vercel-labs/skills",
                    "skills": ["external-skill"],
                }
            ],
        }
        synced = _sync_local_entries(lock, global_scope=True)
        local_entries = [entry for entry in synced["entries"] if entry.get("kind") == "local"]
        self.assertEqual(len(local_entries), 1)
        self.assertEqual(local_entries[0]["skills"], ["test-skill", "ui-skill"])

    @mock.patch("lib.skills_ops._save_lock")
    @mock.patch("lib.skills_ops._sync_local_entries")
    @mock.patch("lib.skills_ops._lock_file")
    def test_update_skills_ok_when_only_local_entries_exist(
        self,
        lock_file: mock.Mock,
        sync_local_entries: mock.Mock,
        save_lock: mock.Mock,
    ) -> None:
        lock_file.return_value = {"schema_version": 2, "updated_at": None, "entries": []}
        sync_local_entries.return_value = {
            "schema_version": 2,
            "updated_at": None,
            "entries": [
                {
                    "kind": "local",
                    "scope": "global",
                    "source": "codex-home",
                    "skills": ["ui-skill"],
                }
            ],
        }
        result = update_skills(global_scope=True)
        self.assertEqual(result["summary"]["status"], "ok")
        self.assertEqual(result["updated"], [])
        self.assertIn("no externally tracked skills", result["note"])


if __name__ == "__main__":
    unittest.main()
