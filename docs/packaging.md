# Packaging and releasing

How the image is built and published. For the image itself, see [architecture](architecture.md).

## What is built

| Where | What you get | Built with |
| --- | --- | --- |
| Any machine with Docker | The image, for your machine's platform | `docker build -t my-image .` |
| A release | `ghcr.io/<owner>/<image-name>` and/or `docker.io/<namespace>/<image-name>`, `linux/amd64` | `release.yml` |

The image name is set when you run Init and is stored as `IMAGE_NAME` in `release.yml`.

## Build arguments

| Argument | Default | Meaning |
| --- | --- | --- |
| `PYTHON_VERSION` | `3.15` | The Python version of the base image |
| `VERSION` | `0.0.0` | Written to the `org.opencontainers.image.version` label |

```bash
docker build --build-arg VERSION=1.2.3 -t my-image:1.2.3 .
```

## Checks on every change

`ci.yml` lints the `Dockerfile`, runs the tests and builds the image on every pull request and push to `main`. Nothing is pushed.

## Releasing

A release starts from a GitHub release, not from a tag alone.

1. In a pull request, move the `[Unreleased]` entries in `CHANGELOG.md` under the new version.
2. After it is merged, publish a GitHub release tagged `v<version>`, for example `v1.2.3`. The tag must be a semantic version; otherwise the image gets no tags and the publish fails.
3. `release.yml` runs one job per registry that you have enabled. A registry that is not enabled is skipped.
4. Check the result: `docker run --rm ghcr.io/<owner>/<image-name>:1.2.3`.

Images are tagged with the version and the minor version (`1.2.3` and `1.2`) and built with `VERSION` set to the release version.

## Enabling registries

Set these in the repository under Settings > Secrets and variables > Actions. Nothing is published until you do.

| Registry | Setting | Notes |
| --- | --- | --- |
| GitHub Container Registry | variable `PUBLISH_GHCR` = `true` | Uses the workflow's own `GITHUB_TOKEN`; no secret to store |
| Docker Hub | variable `DOCKERHUB_USERNAME` and secret `DOCKERHUB_TOKEN` | The token is a Docker Hub access token. The namespace is the one chosen at init, otherwise the username |

Both can be enabled together; each registry gets its own build and push.
