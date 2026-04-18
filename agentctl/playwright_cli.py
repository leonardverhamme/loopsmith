#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys


def main() -> int:
    if not shutil.which("npx"):
        print("Error: npx is required but not found on PATH.", file=sys.stderr)
        return 1

    args = sys.argv[1:]
    has_session_flag = any(arg == "--session" or arg.startswith("--session=") for arg in args)
    npx_path = shutil.which("npx") or "npx"
    command = [npx_path, "--yes", "--package", "@playwright/cli", "playwright-cli"]
    if not has_session_flag and os.environ.get("PLAYWRIGHT_CLI_SESSION"):
        command.extend(["--session", os.environ["PLAYWRIGHT_CLI_SESSION"]])
    command.extend(args)
    suffix = os.path.splitext(npx_path)[1].lower()
    shell = suffix in {".cmd", ".bat", ".ps1"}
    completed = subprocess.run(subprocess.list2cmdline(command) if shell else command, check=False, shell=shell)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
