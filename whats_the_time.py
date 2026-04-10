from __future__ import annotations

from importlib.metadata import distribution


def main() -> None:
    dist = distribution("whats-the-time")
    summary = dist.metadata["Summary"]
    version = dist.metadata["Version"]

    print(summary, end="\n\n")
    print(f"Version: {version} (never to change)")
    print(f"Reproduce: uvx --exclude-newer now whats-the-time=={version}")
