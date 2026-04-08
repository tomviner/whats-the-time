from __future__ import annotations

from datetime import datetime, timezone
from hatchling.metadata.plugin.interface import MetadataHookInterface


class CustomMetadataHook(MetadataHookInterface):
    def update(self, metadata: dict[str, object]) -> None:
        metadata["description"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
