# whats-the-time

same version, different time


```sh
uvx --no-cache --refresh whats-the-time==1.0.0
```

It tells you the time.

Build locally:

```sh
./scripts/build-minute-wheel.sh
uv tool run --from dist/*.whl whats-the-time
```

## What are build tags?

Wheel filenames can include an extra build tag, like:

```text
whats_the_time-1.0.0-20260409002810-py3-none-any.whl
```

That `20260409002810` part is not part of the package version. The version is still `1.0.0`.

It only distinguishes multiple wheels for the same name, version, and compatibility tags, which means the same release can be uploaded again and again as new wheel files.

Hat tip to my friend [@graingert](https://github.com/graingert), who told me about build tags.

## PyPI Is Not Atomic

PyPI publishes files, not whole releases atomically.

This project leans on that. A release at a fixed version is not necessarily immutable: new wheels can appear for `whats-the-time==1.0.0` while older wheels for the same version still exist.
