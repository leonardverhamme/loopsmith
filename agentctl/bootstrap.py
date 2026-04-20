from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from .bundle_install import DEFAULT_REPO_URL, bootstrap_bundle, default_codex_home
from .lib.branding import COMPATIBILITY_COMMAND, PUBLIC_COMMAND, PUBLIC_DISPLAY_NAME, PUBLIC_DISPLAY_TAGLINE, PUBLIC_PRODUCT_NAME


def _installed_entry(codex_home: Path) -> Path:
    return codex_home / "agentctl" / "agentctl.py"


def _delegate(args: list[str], codex_home: Path) -> int:
    entry = _installed_entry(codex_home)
    env = os.environ.copy()
    env["CODEX_HOME"] = str(codex_home)
    result = subprocess.run([sys.executable, str(entry), *args], check=False, env=env)
    return result.returncode


def _bootstrap_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=f"{PUBLIC_COMMAND} bootstrap", description=f"Bootstrap the public {PUBLIC_DISPLAY_NAME} bundle into CODEX_HOME.")
    parser.add_argument("--codex-home", help="Target CODEX_HOME. Defaults to $CODEX_HOME or ~/.codex")
    parser.add_argument("--source-root", help="Install from a local checkout instead of downloading the public repo archive")
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL, help="GitHub repo URL used when downloading release assets or fallback archives")
    parser.add_argument("--version", help="Release version tag to bootstrap, for example v0.1.0. Defaults to the latest release.")
    parser.add_argument("--ref", default="main", help="Fallback git ref used only when release assets are unavailable")
    parser.add_argument("--ref-type", choices=("branch", "tag"), default="branch", help="Interpret --ref as a branch or tag")
    parser.add_argument("--skip-post-checks", action="store_true", help="Skip post-install doctor/capabilities/maintenance checks")
    return parser


def _bootstrap(argv: list[str]) -> int:
    parser = _bootstrap_parser()
    args = parser.parse_args(argv)
    target_root = Path(args.codex_home).resolve() if args.codex_home else default_codex_home()
    source_root = Path(args.source_root).resolve() if args.source_root else None
    summary = bootstrap_bundle(
        target_root=target_root,
        source_root=source_root,
        repo_url=args.repo_url,
        version=args.version,
        ref=args.ref,
        ref_type=args.ref_type,
        skip_post_checks=args.skip_post_checks,
    )
    print(f"Installed {PUBLIC_DISPLAY_NAME} into {target_root}")
    if summary.get("post_checks") is not None:
        print(f"Post-install checks: {summary['status']}")
        print(f"Bootstrap report: {target_root / 'agentctl' / 'state' / 'bootstrap-report.json'}")
    else:
        print("Post-install checks: skipped")
    return 0 if summary["status"] == "ok" else 1


def _print_wrapper_help() -> None:
    print(f"{PUBLIC_DISPLAY_NAME} package wrapper")
    print(PUBLIC_DISPLAY_TAGLINE)
    print("")
    print(f"Use `{PUBLIC_COMMAND} bootstrap` to install the public bundle into CODEX_HOME.")
    print(f"After bootstrap, both `{PUBLIC_COMMAND}` and `{COMPATIBILITY_COMMAND}` delegate to the installed bundle.")
    print("")
    print("Examples")
    print(f"- {PUBLIC_COMMAND} bootstrap")
    print(f"- {PUBLIC_COMMAND} bootstrap --source-root C:\\path\\to\\{PUBLIC_PRODUCT_NAME}")
    print(f"- {PUBLIC_COMMAND} doctor")


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    codex_home = default_codex_home()

    if not args or args[0] in {"-h", "--help"}:
        if _installed_entry(codex_home).exists():
            return _delegate(args, codex_home)
        _print_wrapper_help()
        return 0

    if args[0] in {"bootstrap", "install"}:
        return _bootstrap(args[1:])

    if _installed_entry(codex_home).exists():
        return _delegate(args, codex_home)

    print(f"{PUBLIC_DISPLAY_NAME} bundle is not installed in CODEX_HOME.", file=sys.stderr)
    print(
        f"Run `{PUBLIC_COMMAND} bootstrap` first (or `{COMPATIBILITY_COMMAND} bootstrap`), "
        f"or use `{PUBLIC_COMMAND} bootstrap --source-root <repo>` from a local checkout.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
