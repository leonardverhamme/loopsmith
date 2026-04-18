from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.research import _research_status, choose_github_mode


class ResearchTests(unittest.TestCase):
    def test_choose_github_mode_for_issues(self) -> None:
        self.assertEqual(choose_github_mode("next.js is:issue cache components"), "issues")

    def test_choose_github_mode_for_code(self) -> None:
        self.assertEqual(choose_github_mode("repo:vercel/next.js path:packages/app-router"), "code")

    def test_choose_github_mode_for_repos(self) -> None:
        self.assertEqual(choose_github_mode("agent skills cli"), "repos")

    def test_research_status_is_degraded_when_sources_exist_with_caveats(self) -> None:
        status = _research_status(
            {
                "shortlist": [{"title": "skills-cli", "url": "https://example.com"}],
                "caveats": ["GitHub CLI auth is unavailable."],
            }
        )
        self.assertEqual(status, "degraded")

    def test_research_status_is_error_when_no_sources_and_only_caveats_exist(self) -> None:
        status = _research_status({"shortlist": [], "caveats": ["search failed"]})
        self.assertEqual(status, "error")


if __name__ == "__main__":
    unittest.main()
