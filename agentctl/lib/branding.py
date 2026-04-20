from __future__ import annotations

PUBLIC_DISPLAY_NAME = "Agent CLI OS"
PUBLIC_DISPLAY_TAGLINE = "OS stands for On Steroids, not operating system."

PUBLIC_PRODUCT_NAME = "agent-cli-os"
LEGACY_PRODUCT_NAME = "loopsmith"

PUBLIC_COMMAND = "agentcli"
COMPATIBILITY_COMMAND = "loopsmith"
LEGACY_COMMAND = "agentctl"

PUBLIC_REPO_URL = "https://github.com/leonardverhamme/agent-cli-os"
LEGACY_REPO_URL = "https://github.com/leonardverhamme/loopsmith"

PUBLIC_PLUGIN_NAME = "agent-cli-os"
LEGACY_PLUGIN_NAMES = ("loopsmith", "agentctl", "agentctl-platform")

PUBLIC_DOCS_DIRNAME = "agent-cli-os"
LEGACY_DOCS_DIRNAME = "loopsmith"

RELEASE_ASSET_PREFIX = PUBLIC_PRODUCT_NAME
RELEASE_BUNDLE_PREFIX = f"{PUBLIC_PRODUCT_NAME}-bundle"


def command_names() -> tuple[str, str]:
    return PUBLIC_COMMAND, COMPATIBILITY_COMMAND
