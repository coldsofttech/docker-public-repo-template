# docker-public-repo-template

[![CI](https://github.com/coldsofttech/docker-public-repo-template/actions/workflows/ci.yml/badge.svg)](https://github.com/coldsofttech/docker-public-repo-template/actions/workflows/ci.yml)
[![Release](https://github.com/coldsofttech/docker-public-repo-template/actions/workflows/release.yml/badge.svg)](https://github.com/coldsofttech/docker-public-repo-template/actions/workflows/release.yml)
[![Docker image](https://img.shields.io/badge/ghcr.io-image-2496ED?logo=docker&logoColor=white)](https://github.com/coldsofttech/docker-public-repo-template/pkgs/container/docker-public-repo-template)
[![License](https://img.shields.io/github/license/coldsofttech/docker-public-repo-template)](LICENSE)

A ready-to-use starting point for public GitHub repositories that ship a Docker image, with community files, issue and pull request templates, automated dependency updates and security checks already in place.

## What you get

- Contribution, conduct, support and security-reporting guidelines
- Issue forms and a pull request template
- Automated dependency updates and dependency review
- A starter Dockerfile that builds a small image running as a non-root user
- Automated Dockerfile linting, image tests and publishing to GitHub Container Registry and Docker Hub when you publish a release, once you turn them on
- Vulnerability scanning with Trivy for the Dockerfile and, weekly, the built image
- A changelog ready for your first release
- Consistent editor and line-ending settings
- Secret scanning before every commit

## Getting started

1. Click **Use this template** on GitHub and create your new repository.
2. Replace the placeholder in `app/` and adjust the `Dockerfile` for your application, then replace this README with a description of your project.
3. Run the **Init** workflow from the Actions tab and merge the pull request it opens. It asks for your Docker image name (required), an optional Docker Hub user or organisation, and whether to keep the pytest, mypy and Trivy checks; anything you switch off is removed. It also fills in your owner and repository name. Then add your contact details in `CODE_OF_CONDUCT.md`, delete `.github/workflows/init.yml`, and replace the description above.
4. Apply the repository protections by following the [setup guide](docs/repo-setup.md).
5. Install the commit checks: `pip install pre-commit && pre-commit install --hook-type pre-commit --hook-type post-commit`.

## Building the image

```bash
docker build -t my-image .
docker run --rm my-image
```

## Publishing the image

Publishing a GitHub release (for example `v1.0.0`) publishes the image to the registries you have switched on. Nothing is published until you do, so the template works as is. In your repository, go to **Settings > Secrets and variables > Actions**:

- **GitHub Container Registry:** add the variable `PUBLISH_GHCR` with the value `true`.
- **Docker Hub:** add the variable `DOCKERHUB_USERNAME` with your Docker Hub name, and the secret `DOCKERHUB_TOKEN` with an access token from Docker Hub.

You can turn on both.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please report security issues privately as described in [SECURITY.md](SECURITY.md).

## License

Released under the [MIT License](LICENSE).
