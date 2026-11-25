# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.1] - 2026-11-25

### Fixed

- The Init workflow no longer fails when GitHub refuses to push changes to workflow files; it explains how to finish the setup locally.

## [0.1.0] - 2026-11-25

### Added

- A starter Dockerfile for a small, non-root image, with a placeholder application.
- CI that lints the Dockerfile, runs unit and integration tests with strict type checking, and builds the image.
- A release workflow that publishes the image to GitHub Container Registry and Docker Hub when you enable them.
- An Init workflow that asks for the image name, an optional Docker Hub namespace and whether to keep pytest and mypy, then sets up the repository to match.
- A Sweepito configuration that cleans Docker build caches and Python test caches.
- Trivy security scanning of the Dockerfile and, weekly, the built image, which the Init workflow can turn off.
- Docker-specific documentation, issue and pull request templates, and ignore rules.
