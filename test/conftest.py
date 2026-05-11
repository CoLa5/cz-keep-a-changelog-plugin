"""Pytest Fixtures."""

from commitizen.config import BaseConfig
import pytest


@pytest.fixture
def config() -> BaseConfig:
    config_ = BaseConfig()
    config_.settings.update({"name": "cz_keep_a_changelog_plugin"})
    return config_
