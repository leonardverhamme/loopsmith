from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import skill_map as skill_map_module


class SkillMapTests(unittest.TestCase):
    def _capabilities(self) -> dict:
        return {
            "capabilities": [
                {
                    "key": "context-workflows",
                    "label": "Repo context workflows",
                    "group": "workflows",
                    "front_door": "$context-skill",
                    "entrypoints": ["$context-skill"],
                    "skills": ["context-skill"],
                    "summary": "Keep durable repo context aligned with the code.",
                    "status": "ok",
                },
                {
                    "key": "ui-workflows",
                    "label": "UI workflows",
                    "group": "workflows",
                    "front_door": "$ui-skill / $ui-deep-audit",
                    "entrypoints": ["$ui-skill", "$ui-deep-audit", "agentcli run ui-deep-audit"],
                    "skills": ["ui-skill", "ui-deep-audit"],
                    "summary": "Use for normal UI work and full-app UI audits.",
                    "status": "ok",
                },
            ],
            "capability_groups": [
                {
                    "key": "workflows",
                    "label": "Workflows",
                    "summary": "Repeatable cross-repo workflows.",
                    "items": ["context-workflows", "ui-workflows"],
                }
            ],
        }

    def _inventory(self, root: Path) -> dict:
        def skill_file(name: str, description: str) -> str:
            path = root / "skills" / name / "SKILL.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n",
                encoding="utf-8",
            )
            return str(path)

        return {
            "summary": {"status": "ok", "total_items": 8},
            "items": [
                {"kind": "skill", "name": "context-skill", "source_scope": "user", "status": "ok", "source_path": skill_file("context-skill", "Context skill."), "installed": True},
                {"kind": "skill", "name": "ui-skill", "source_scope": "user", "status": "ok", "source_path": skill_file("ui-skill", "UI implementation skill."), "installed": True},
                {"kind": "skill", "name": "ui-deep-audit", "source_scope": "user", "status": "ok", "source_path": skill_file("ui-deep-audit", "Deep UI audit skill."), "installed": True},
                {"kind": "skill", "name": "editskill", "source_scope": "user", "status": "ok", "source_path": skill_file("editskill", "Preferred edit skill."), "installed": True},
                {"kind": "skill", "name": "skill-edit-mode", "source_scope": "user", "status": "ok", "source_path": skill_file("skill-edit-mode", "Legacy edit-skill alias."), "installed": True},
                {"kind": "plugin", "name": "build-web-apps", "source_scope": "user", "status": "ok", "installed": True},
                {"kind": "skill", "name": "build-web-apps:frontend-skill", "source_scope": "plugin", "status": "ok", "installed": True},
                {"kind": "skill", "name": "build-web-apps:react-best-practices", "source_scope": "plugin", "status": "ok", "installed": True},
            ],
        }

    def test_build_skill_map_payload_surfaces_ui_context_and_editskill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            payload = skill_map_module.build_skill_map_payload(self._capabilities(), self._inventory(root), cwd=root)

        workflow_group = next(group for group in payload["menu_groups"] if group["key"] == "workflows")
        capability_keys = {item["key"] for item in workflow_group["items"]}
        helper_names = {item["name"] for item in payload["helper_skills"]}
        self.assertIn("ui-workflows", capability_keys)
        self.assertIn("context-workflows", capability_keys)
        self.assertIn("editskill", helper_names)
        self.assertIn("skill-edit-mode", helper_names)
        self.assertTrue(any("ui-skill" in note for note in payload["notes"]))

    def test_write_skill_map_docs_creates_markdown_and_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            docs_dir = root / "docs" / "agent-cli-os"
            workspace = SimpleNamespace(docs_dir=docs_dir)
            with mock.patch.object(skill_map_module, "maintenance_workspace", return_value=workspace):
                payload = skill_map_module.write_skill_map_docs(self._capabilities(), self._inventory(root), cwd=root)

            markdown_path = Path(payload["markdown_path"])
            pdf_path = Path(payload["pdf_path"])
            self.assertTrue(markdown_path.exists())
            self.assertTrue(pdf_path.exists())
            self.assertIn("# Agent CLI OS Skill Map", markdown_path.read_text(encoding="utf-8"))
            self.assertGreater(pdf_path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
