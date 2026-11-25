"""Checks on the built image: it runs and stays unprivileged. Needs Docker."""

from __future__ import annotations

import subprocess
from collections.abc import Callable

import pytest

pytestmark = pytest.mark.integration

Run = Callable[..., subprocess.CompletedProcess[str]]


def test_runs(run: Run) -> None:
    result = run()
    assert result.returncode == 0
    assert result.stdout.strip()


def test_runs_as_unprivileged_user(run: Run) -> None:
    result = run("-u", entrypoint="id")
    assert result.returncode == 0
    assert result.stdout.strip() == "10001"
