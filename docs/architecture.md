# Architecture

How the image is put together. For working on it, see [development](development.md); for building and releasing it, see [packaging](packaging.md); for the workflows, see the [Docker guide](docker.md).

## What the image is

A small, non-root Python image that runs `app/main.py`. The application is a placeholder, so replace it and adjust the `Dockerfile` for what you ship.

## Files

```text
Dockerfile                the two-stage build
Dockerfile.dockerignore   keeps the build context to app/
app/                      the application the image runs
tests/unit/               tests of the application code (no Docker needed)
tests/integration/        tests that build and run the image (Docker needed)
.github/workflows/        ci.yml (checks) and release.yml (publishing)
docs/                     this documentation
```

The build context is the repository root. `Dockerfile.dockerignore` is an allow-list, so only `app/` is sent to the Docker daemon.

## Stages

| Stage | Purpose |
| --- | --- |
| `build` | A slim Python image that prepares a virtual environment at `/opt/venv` and copies in `app/`. Install your dependencies here. |
| `runtime` | The same slim base with only `/opt/venv` and the application copied in, so no build tools or sources are left. |

Splitting the stages keeps the final image small. The Python version is the `PYTHON_VERSION` build argument (default 3.15).

## The runtime image

- **User.** A fixed system user `app` (uid `10001`) with no home folder and no login shell. The image never runs as root; an integration test checks this.
- **Entry point.** `ENTRYPOINT ["python", "main.py"]` in `/app`, so anything after the image name is passed to the application.
- **Environment.** `/opt/venv/bin` is first on `PATH`. Python output is unbuffered and no bytecode is written.
- **Labels.** The OCI labels (title, description, source, license and `VERSION`) are set so registries show the right details. Init fills in the title and source.

## Platforms

CI and releases build for the platform of the GitHub runner, `linux/amd64`. To publish `linux/arm64` as well, add the QEMU setup action to `release.yml` and set `platforms: linux/amd64,linux/arm64` on the build step.
