from __future__ import annotations

from datetime import datetime, timezone
from importlib.metadata import distribution


def main() -> None:
    dist = distribution("whats-the-time")
    the_time = dist.metadata["Summary"]
    version = dist.metadata["Version"]

    print(the_time, end="\n\n")
    print(f"Version: {version} (never to change)")

    resolution_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"Reproduce: uvx --exclude-newer {resolution_time} whats-the-time=={version}")
