# Docker image

Technical notes for the image defined in the `Dockerfile`.

## Layout

- `Dockerfile`: multi-stage build. The `build` stage prepares a virtual environment; the `runtime` stage copies only that and `app/`, and runs as the unprivileged user `10001`.
- `Dockerfile.dockerignore`: allow-list build context, so only `app/` is sent to the daemon.
- `app/`: placeholder application. Replace it.
- `mypy.ini`: strict type checking of `app/` and `tests/`; CI runs `mypy`.
- `tests/`: `unit/` tests the application code; `integration/` builds the image with Docker and checks it runs and stays non-root. The default `pytest` run skips integration tests; run them with `pytest -m integration`.

## Workflow

`.github/workflows/ci.yml` runs on every pull request and push to `main`. It runs pre-commit, lints the Dockerfile with hadolint, runs the unit tests (`tests`) and the integration tests (`int-tests`), and builds the image without pushing.

`.github/workflows/release.yml` runs when a GitHub release is published, with one job per registry (`publish-ghcr`, `publish-dockerhub`). A job runs only when its repository variable is set (Settings > Secrets and variables > Actions > Variables); with none set, nothing is published. Images are tagged with the release version, for example `1.2.3` and `1.2`.

| Registry | Enable with | Image |
|---|---|---|
| GitHub Container Registry | variable `PUBLISH_GHCR` = `true` | `ghcr.io/<owner>/<image-name>` |
| Docker Hub | variable `DOCKERHUB_USERNAME` = your user or organisation (the namespace, unless one was set at init), and secret `DOCKERHUB_TOKEN` = a Docker Hub access token | `docker.io/<namespace>/<image-name>` |

Both can be enabled together; one build is pushed to each.

## Build and test locally

```
docker build -t my-image .
pip install mypy pytest && mypy && pytest
pytest -m integration
```
