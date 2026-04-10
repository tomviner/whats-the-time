# whats-the-time

_same version, different time_

A packaging stunt about mutability.

`whats-the-time==1.0.0` looks like it's fixed.
It isn't.


```sh
uvx --no-cache --refresh whats-the-time==1.0.0
```

It tells you the time, using a pinned package version.

## What's the point?

Recent supply chain attacks have made it clear any library could get compromised at any time.
Exact version alone is not enough.

`uvx mypackage` will fetch a fresh package, potentially not audited yet.
Even `uvx mypackage==1.2.3` can fetch a fresh wheel, potentially not audited yet.
Only `uvx --exclude-newer 2026-04-10T22:20:39Z mypackage==1.2.3` restricts resolution to what existed at that moment.

## What are build tags?

Wheel filenames can include an extra [build tag](https://packaging.python.org/en/latest/specifications/binary-distribution-format/#file-name-convention:~:text=e.g.%201.0.-,build%20tag,-Optional%20build%20number), like:

```text
whats_the_time-1.0.0-20260409002810-py3-none-any.whl
```

That `20260409002810` part is not part of the package version. The version is still `1.0.0`.

It distinguishes multiple wheels for the same name, version, and compatibility tags, which means the same release can be uploaded again and again as new wheel files.

Hat tip to my friend [@graingert](https://github.com/graingert), who told me about build tags.

## PyPI Is Not Atomic

PyPI publishes files, not whole releases atomically.

This project leans on that. A release at a fixed version is not immutable: new wheels can appear for `whats-the-time==1.0.0` at any time. [And they do](https://pypi.org/project/whats-the-time/1.0.0/#files).

## Reproducible Resolution

If you want a community-auditable, frozen answer, you need to pin time as well as version:

```sh
uvx --exclude-newer 2026-04-10T22:20:39Z whats-the-time==1.0.0
```

That asks `uv` to [resolve as though nothing newer exists](https://docs.astral.sh/uv/concepts/resolution/#reproducible-resolutions). For a shell-generated cutoff, use `$(date -u +%FT%TZ)`.

## Local Build

Build locally:

```sh
./scripts/build-minute-wheel.sh
uv tool run --from dist/*.whl whats-the-time
```
