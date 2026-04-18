from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.capabilities import (
    print_doctor_human,
    print_research_human,
    print_skills_human,
    print_status_human,
)


class CliOutputTests(unittest.TestCase):
    def test_doctor_human_is_compact_and_health_focused(self) -> None:
        payload = {
            "summary": {"status": "ok", "installed_skill_count": 17},
            "tools": {
                "gh": {"installed": True, "skill_supported": False},
            },
            "detect_only_tools": ["firebase", "gcloud"],
            "capabilities": [
                {"label": "Research", "status": "ok", "front_door": "agentctl research", "required": True},
                {"label": "Supabase data", "status": "degraded", "front_door": "supabase + Supabase MCP", "required": False},
            ],
        }
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            print_doctor_human(payload)
        output = buffer.getvalue()
        self.assertIn("Healthy baseline capabilities: 1 / 1", output)
        self.assertIn("Needs attention", output)
        self.assertNotIn("Capability menu", output)

    def test_status_human_hides_history_and_surfaces_active_workflows(self) -> None:
        payload = {
            "summary": {"status": "ok", "count": 1, "historical_count": 4},
            "workflows": [
                {
                    "workflow_name": "agentctl-maintenance",
                    "status": "complete",
                    "tasks_done": 19,
                    "tasks_total": 19,
                    "tasks_open": 0,
                    "tasks_blocked": 0,
                    "iteration": 1,
                    "repo_root": r"C:\repo\agentctl-platform",
                    "checklist_path": r"docs/agentctl/maintenance.md",
                }
            ],
        }
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            print_status_human(payload)
        output = buffer.getvalue()
        self.assertIn("Active workflows: 1", output)
        self.assertIn("Historical workflows hidden: 4", output)
        self.assertIn("agentctl-maintenance: complete", output)

    def test_skills_human_distinguishes_local_and_external_management(self) -> None:
        payload = {
            "summary": {"status": "ok", "scope": "global"},
            "tracked_missing": [],
            "tracked_local": ["ui-skill", "test-skill"],
            "tracked_external": ["external-skill"],
            "unmanaged_installed": [],
        }
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            print_skills_human(payload)
        output = buffer.getvalue()
        self.assertIn("Managed local skills", output)
        self.assertIn("ui-skill", output)
        self.assertIn("Managed external skills", output)
        self.assertIn("external-skill", output)

    def test_research_human_shows_caveats_when_degraded(self) -> None:
        payload = {
            "status": "degraded",
            "mode": "github",
            "query": "agent skills cli",
            "evidence": {
                "shortlist": [{"title": "skills-cli", "url": "https://example.com"}],
                "caveats": ["GitHub CLI auth is unavailable."],
            },
            "paths": {"json": r"C:\tmp\evidence.json", "brief": r"C:\tmp\brief.md"},
        }
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            print_research_human(payload)
        output = buffer.getvalue()
        self.assertIn("Status: degraded", output)
        self.assertIn("Caveats", output)
        self.assertIn("GitHub CLI auth is unavailable.", output)


if __name__ == "__main__":
    unittest.main()
