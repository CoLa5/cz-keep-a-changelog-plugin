"""Pytest Fixtures."""

from commitizen.config import BaseConfig
import pytest


@pytest.fixture
def config() -> BaseConfig:
    config_ = BaseConfig()
    config_.settings.update(
        {
            "name": "cz_keep_a_changelog_plugin",
            "cz_keep_a_changelog_plugin": {
                "issue_url_template": (
                    "https://github.com/CoLa5/cz-keep-a-changelog-plugin"
                    "/issues/{{issue}}"
                )
            },
        }
    )
    return config_
