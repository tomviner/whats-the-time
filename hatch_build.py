from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from hatchling.metadata.plugin.interface import MetadataHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict[str, object]) -> None:
        build_minute = os.environ.get("WHATS_THE_TIME_BUILD_MINUTE")
        if not build_minute:
            build_minute = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

        build_tag = os.environ.get("WHATS_THE_TIME_BUILD_TAG")
        if not build_tag:
            build_tag = datetime.now(timezone.utc).strftime("%Y%m%d%H%M")

        os.environ["WHATS_THE_TIME_BUILD_MINUTE"] = build_minute
        os.environ["WHATS_THE_TIME_BUILD_TAG"] = build_tag


class CustomMetadataHook(MetadataHookInterface):
    def update(self, metadata: dict[str, object]) -> None:
        build_minute = os.environ.get("WHATS_THE_TIME_BUILD_MINUTE")
        if not build_minute:
            build_minute = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

        metadata["description"] = build_minute
