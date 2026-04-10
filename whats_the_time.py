from __future__ import annotations

from datetime import datetime, timezone
from importlib.metadata import distribution


def main() -> None:
    dist = distribution("whats-the-time")
    summary = dist.metadata["Summary"]

    # Parse WHEEL file for build tag and compatibility tag
    wheel_text = dist.read_text("WHEEL") or ""
    build_tag = None
    tags = []
    for line in wheel_text.splitlines():
        if line.startswith("Build: "):
            build_tag = line.split(": ", 1)[1]
        elif line.startswith("Tag: "):
            tags.append(line.split(": ", 1)[1])

    # Reconstruct wheel filename
    name = dist.metadata["Name"].replace("-", "_")
    version = dist.metadata["Version"]
    tag = tags[0] if tags else "py3-none-any"

    if build_tag:
        wheel_name = f"{name}-{version}-{build_tag}-{tag}.whl"
    else:
        wheel_name = f"{name}-{version}-{tag}.whl"

    resolution_time = None
    if build_tag:
        build_time = datetime.strptime(build_tag, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
        resolution_time = build_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    print(summary)
    print(wheel_name)
    print(f"Version: {version} (never to change)")
    if resolution_time:
        print(f"Reproduce: uvx --exclude-newer {resolution_time} whats-the-time=={version}")
