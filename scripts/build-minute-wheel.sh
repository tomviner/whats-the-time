#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
cd "$REPO_ROOT"

BUILD_MINUTE=${WHATS_THE_TIME_BUILD_MINUTE:-$(date -u '+%Y-%m-%d %H:%M')}
BUILD_TAG=${WHATS_THE_TIME_BUILD_TAG:-$(date -u '+%Y%m%d%H%M%S')}
VERSION=$(uv version --short)

printf 'Building wheel with embedded minute: %s\n' "$BUILD_MINUTE"
printf 'Wheel build tag: %s\n' "$BUILD_TAG"
WHATS_THE_TIME_BUILD_MINUTE="$BUILD_MINUTE" \
WHATS_THE_TIME_BUILD_TAG="$BUILD_TAG" \
uv build --wheel --clear --out-dir dist
VERSION="$VERSION" BUILD_TAG="$BUILD_TAG" python3 - <<'PY'
from pathlib import Path
import os
import re
import shutil
import tempfile
import zipfile

version = os.environ["VERSION"]
build_tag = os.environ["BUILD_TAG"]
wheel_path = Path(f"dist/whats_the_time-{version}-py3-none-any.whl")
new_wheel_path = wheel_path.with_name(
    f"whats_the_time-{version}-{build_tag}-py3-none-any.whl"
)

fd, temp_name = tempfile.mkstemp(dir=wheel_path.parent, suffix=".whl")
Path(temp_name).unlink(missing_ok=True)
temp_path = Path(temp_name)

try:
    with zipfile.ZipFile(wheel_path) as source, zipfile.ZipFile(temp_path, "w") as target:
        for info in source.infolist():
            data = source.read(info.filename)
            if info.filename.endswith(".dist-info/WHEEL"):
                text = data.decode("utf-8")
                if re.search(r"^Build: .*$", text, flags=re.MULTILINE):
                    text = re.sub(r"^Build: .*$", f"Build: {build_tag}", text, flags=re.MULTILINE)
                else:
                    lines = text.splitlines()
                    text = "\n".join([lines[0], f"Build: {build_tag}", *lines[1:]]) + "\n"
                data = text.encode("utf-8")
            target.writestr(info, data)
    shutil.move(temp_path, new_wheel_path)
    wheel_path.unlink()
finally:
    if temp_path.exists():
        temp_path.unlink()
PY
