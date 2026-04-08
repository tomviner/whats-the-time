# whats-the-time

`whats-the-time` is a packaging stunt.

The intended joke:

```sh
uvx 'whats-the-time==1.0.0'
```

prints the minute embedded into the selected wheel, while the package version
stays fixed at `1.0.0`.

The mechanism is wheel build tags. We can publish multiple wheels for the same
package version, interpreter tag, ABI tag, and platform tag, while changing
only the wheel filename's build tag. That lets us test how installers behave
when multiple same-version wheels exist.

The CLI prints only the wheel metadata summary.

If the stunt works for a given user flow, the printed minute changes as newer
build-tagged wheels are selected. If caching wins, it stays stale.

The minute is embedded by a Hatchling custom metadata hook during wheel build,
specifically into the wheel's `dist-info/METADATA` `Summary:` field.

The runtime code is intentionally tiny and static. It just reads installed
package metadata and prints the summary.

The build hook also rewrites the finished wheel to add a wheel build tag, so
multiple wheels can coexist for the same package version.

The bundled GitHub Actions workflow publishes every 5 minutes, because that is
the minimum schedule interval GitHub Actions currently supports.

Build a wheel with an embedded minute:

```sh
./scripts/build-minute-wheel.sh
```

Build with explicit minute and build tag:

```sh
WHATS_THE_TIME_BUILD_MINUTE='2099-12-31 23:59' \
WHATS_THE_TIME_BUILD_TAG='20991231235959' \
./scripts/build-minute-wheel.sh
```

Run locally:

```sh
uv tool run --from dist/whats_the_time-0.1.0-py3-none-any.whl whats-the-time
```
