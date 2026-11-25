# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

- Added a starter Dockerfile, image tests and CI to lint, test and build the image, and a release workflow that publishes it to GitHub Container Registry and Docker Hub when enabled.
- Added a Sweepito configuration that cleans Docker build caches and Python test caches.
- The Init workflow now asks for the image name (and optionally a Docker Hub namespace) and whether to keep pytest and mypy, then sets up the repository to match.
