"""Fixtures that build the image once and run it."""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
IMAGE = "docker-template-test"

Run = Callable[..., subprocess.CompletedProcess[str]]


@pytest.fixture(scope="session")
def image() -> str:
    subprocess.run(["docker", "build", "-t", IMAGE, str(ROOT)], check=True)
    return IMAGE


@pytest.fixture
def run(image: str) -> Run:
    def _run(*args: str, entrypoint: str | None = None) -> subprocess.CompletedProcess[str]:
        cmd = ["docker", "run", "--rm"]
        if entrypoint:
            cmd += ["--entrypoint", entrypoint]
        return subprocess.run([*cmd, image, *args], capture_output=True, text=True)

    return _run
