from __future__ import annotations

import argparse
import os
import shutil
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the agentctl-platform bundle into a CODEX_HOME directory.")
    parser.add_argument("--codex-home", help="Target CODEX_HOME. Defaults to $CODEX_HOME or ~/.codex")
    args = parser.parse_args()

    source_root = repo_root()
    target_root = Path(args.codex_home).resolve() if args.codex_home else default_codex_home()
    target_root.mkdir(parents=True, exist_ok=True)

    for relative in BUNDLE_ITEMS:
        copy_item(source_root, target_root, relative)

    ensure_plugin_enabled(target_root / "config.toml")

    print(f"Installed agentctl-platform into {target_root}")
    print(f"Run: python {target_root / 'agentctl' / 'agentctl.py'} doctor")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
