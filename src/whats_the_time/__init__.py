from __future__ import annotations

from importlib.metadata import metadata


def main() -> None:
    print(metadata("whats-the-time")["Summary"])
