#!/usr/bin/env sh
set -eu

BUILD_TAG=$(date -u '+%Y%m%d%H%M%S')

uv build --wheel --clear --out-dir dist
uvx --with wheel wheel tags --build "$BUILD_TAG" dist/whats_the_time-1.0.0-py3-none-any.whl
rm -f dist/whats_the_time-1.0.0-py3-none-any.whl
