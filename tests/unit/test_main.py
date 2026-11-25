"""Unit tests for the application code. They need neither Docker nor a built image."""

from __future__ import annotations

import pytest

from app.main import greeting, main


def test_greeting() -> None:
    assert greeting()


def test_main_prints_greeting(capsys: pytest.CaptureFixture[str]) -> None:
    main()
    assert capsys.readouterr().out.strip() == greeting()
