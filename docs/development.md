# Development

How to work on the image. For how it is built, see [architecture](architecture.md); for releasing, see [packaging](packaging.md).

## Build and run

```bash
docker build -t my-image .
docker build --build-arg PYTHON_VERSION=3.14 -t my-image:py314 .

docker run --rm my-image
```

## Tests

The tests are Python, run with pytest, and live in two folders:

| Folder | What it checks | Needs Docker |
| --- | --- | --- |
| `tests/unit/` | The application code in `app/` | No |
| `tests/integration/` | The built image: it runs and stays non-root | Yes |

A plain `pytest` runs only the unit tests. Integration tests carry the `integration` marker and run on request:

```bash
pip install mypy pytest
mypy                      # strict type check of app/ and tests/
pytest                    # unit tests
pytest -m integration     # builds the image, then tests it
```

Put anything slow or Docker-dependent under `tests/integration/` so the default run stays fast.

## Continuous integration

`.github/workflows/ci.yml` runs on every pull request and push to `main`:

| Job | What it does |
| --- | --- |
| `ci` | Runs the pre-commit hooks |
| `lint` | Lints the `Dockerfile` with hadolint |
| `tests` | Runs mypy and the unit tests |
| `int-tests` | Runs the integration tests |
| `build` | Builds the image without pushing it |

These job names are the required status checks in `.github/rulesets/main.json`. If you rename or remove a job, change the ruleset to match, or pull requests will wait for a check that never runs. The Init workflow does this for `tests` and `int-tests` when you turn pytest or mypy off.

## Local checks

Install the commit hooks once: `pre-commit install --hook-type pre-commit --hook-type post-commit`. The post-commit hook runs Sweepito, configured in `sweepito.toml`, to clean caches and BuildKit cache exports.
