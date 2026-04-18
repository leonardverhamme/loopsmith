from __future__ import annotations

import http.server
import os
import socketserver
import subprocess
import sys
import tempfile
import threading
import unittest
import uuid
from pathlib import Path


PLAYWRIGHT_ENTRY = Path(__file__).resolve().parents[1] / "playwright_cli.py"


def _browser_name() -> str:
    configured = os.environ.get("AGENTCTL_BROWSER")
    if configured:
        return configured
    return "msedge" if os.name == "nt" else "chrome"


@unittest.skipUnless(os.environ.get("AGENTCTL_RUN_BROWSER_SMOKE") == "1", "Browser smoke disabled unless AGENTCTL_RUN_BROWSER_SMOKE=1.")
class BrowserSmokeTests(unittest.TestCase):
    def _run_playwright(self, args: list[str], *, cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(PLAYWRIGHT_ENTRY), *args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )

    def test_playwright_wrapper_can_open_and_inspect_local_page(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            site_root = root / "site"
            site_root.mkdir(parents=True, exist_ok=True)
            (site_root / "index.html").write_text(
                (
                    "<!doctype html><html><head><title>agentctl smoke</title>"
                    '<link rel="icon" href="/favicon.ico"></head>'
                    "<body><h1>agentctl browser smoke</h1><button id=\"go\">Go</button></body></html>"
                ),
                encoding="utf-8",
            )
            (site_root / "favicon.ico").write_bytes(b"\x00")

            session_id = f"agentctl-browser-smoke-{uuid.uuid4().hex[:8]}"
            env = os.environ.copy()
            env["PLAYWRIGHT_CLI_SESSION"] = session_id

            class Handler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=str(site_root), **kwargs)

                def log_message(self, format: str, *args) -> None:
                    return None

            class ReusableTCPServer(socketserver.TCPServer):
                allow_reuse_address = True

            with ReusableTCPServer(("127.0.0.1", 0), Handler) as httpd:
                port = httpd.server_address[1]
                thread = threading.Thread(target=httpd.serve_forever, daemon=True)
                thread.start()

                try:
                    self._run_playwright(["close-all"], cwd=root, env=env)

                    open_result = self._run_playwright(
                        ["open", f"http://127.0.0.1:{port}", "--browser", _browser_name()],
                        cwd=root,
                        env=env,
                    )
                    self.assertEqual(open_result.returncode, 0, open_result.stderr or open_result.stdout)
                    self.assertIn("Page URL", open_result.stdout)

                    eval_result = self._run_playwright(["eval", "() => document.body.innerText"], cwd=root, env=env)
                    self.assertEqual(eval_result.returncode, 0, eval_result.stderr or eval_result.stdout)
                    self.assertIn("agentctl browser smoke", eval_result.stdout)
                    self.assertIn("Go", eval_result.stdout)

                    snapshot_result = self._run_playwright(["snapshot"], cwd=root, env=env)
                    self.assertEqual(snapshot_result.returncode, 0, snapshot_result.stderr or snapshot_result.stdout)
                    self.assertIn('heading "agentctl browser smoke"', snapshot_result.stdout)
                    self.assertIn('button "Go"', snapshot_result.stdout)
                finally:
                    self._run_playwright(["close"], cwd=root, env=env)
                    self._run_playwright(["close-all"], cwd=root, env=env)
                    httpd.shutdown()


if __name__ == "__main__":
    unittest.main()
