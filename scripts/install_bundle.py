from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


BUNDLE_ITEMS = [
    "agentctl",
    "workflow-tools",
    "skills",
    "plugins",
    "docs/agentctl",
    "AGENTS.md",
    "agentctl.cmd",
    "agentctl.sh",
]

PLUGIN_SNIPPET = '\n[plugins."agentctl-platform"]\nenabled = true\n'


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or (Path.home() / ".codex")).resolve()


def copy_item(source_root: Path, target_root: Path, relative: str) -> None:
    source = source_root / relative
    target = target_root / relative
    if source.is_dir():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target, dirs_exist_ok=True)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def ensure_plugin_enabled(config_path: Path) -> None:
    existing = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    if '[plugins."agentctl-platform"]' in existing or "[plugins.agentctl-platform]" in existing:
        return
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(existing.rstrip() + PLUGIN_SNIPPET, encoding="utf-8")


def run_post_install_checks(target_root: Path) -> dict[str, object]:
    agentctl_entry = target_root / "agentctl" / "agentctl.py"
    checks: list[dict[str, object]] = []
    env = os.environ.copy()
    env["CODEX_HOME"] = str(target_root)
    for command_name in ("doctor", "capabilities", "maintenance"):
        command = [sys.executable, str(agentctl_entry), command_name]
        if command_name == "maintenance":
            command.append("audit")
        command.append("--json")
        result = subprocess.run(command, capture_output=True, text=True, check=False, env=env)
        checks.append(
            {
                "command": " ".join(command[2:-1]),
                "returncode": result.returncode,
                "ok": result.returncode == 0,
                "stdout_tail": result.stdout[-2000:],
                "stderr_tail": result.stderr[-2000:],
            }
        )

    summary = {
        "status": "ok" if all(check["ok"] for check in checks) else "error",
        "checks": checks,
        "target_codex_home": str(target_root),
    }
    report_path = target_root / "agentctl" / "state" / "bootstrap-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the agentctl-platform bundle into a CODEX_HOME directory.")
    parser.add_argument("--codex-home", help="Target CODEX_HOME. Defaults to $CODEX_HOME or ~/.codex")
    parser.add_argument("--skip-post-checks", action="store_true", help="Skip post-install doctor/capabilities/maintenance checks")
    args = parser.parse_args()

    source_root = repo_root()
    target_root = Path(args.codex_home).resolve() if args.codex_home else default_codex_home()
    target_root.mkdir(parents=True, exist_ok=True)

    for relative in BUNDLE_ITEMS:
        copy_item(source_root, target_root, relative)

    ensure_plugin_enabled(target_root / "config.toml")

    print(f"Installed agentctl-platform into {target_root}")
    print(f"Run: python {target_root / 'agentctl' / 'agentctl.py'} doctor")

    if args.skip_post_checks:
        return 0

    summary = run_post_install_checks(target_root)
    print(f"Post-install checks: {summary['status']}")
    print(f"Bootstrap report: {target_root / 'agentctl' / 'state' / 'bootstrap-report.json'}")
    return 0 if summary["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
