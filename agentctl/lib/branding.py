from __future__ import annotations

PUBLIC_PRODUCT_NAME = "loopsmith"
LEGACY_PRODUCT_NAME = "agentctl"

PUBLIC_COMMAND = "loopsmith"
COMPATIBILITY_COMMAND = "agentctl"

PUBLIC_REPO_URL = "https://github.com/leonardverhamme/loopsmith"
LEGACY_REPO_URL = "https://github.com/leonardverhamme/agentctl"

PUBLIC_PLUGIN_NAME = "loopsmith"
LEGACY_PLUGIN_NAMES = ("agentctl", "agentctl-platform")

PUBLIC_DOCS_DIRNAME = "loopsmith"
LEGACY_DOCS_DIRNAME = "agentctl"

RELEASE_ASSET_PREFIX = PUBLIC_PRODUCT_NAME
RELEASE_BUNDLE_PREFIX = f"{PUBLIC_PRODUCT_NAME}-bundle"


def command_names() -> tuple[str, str]:
    return PUBLIC_COMMAND, COMPATIBILITY_COMMAND
