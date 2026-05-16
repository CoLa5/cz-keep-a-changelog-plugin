"""Test of Plugin."""

from collections import OrderedDict
import pathlib
import re
from typing import Any

from commitizen import git
from commitizen.config import BaseConfig
import pytest

from cz_keep_a_changelog_plugin import CzKeepAChangelogPlugin

HERE: pathlib.Path = pathlib.Path(__file__).parent.resolve()


@pytest.fixture
def changelog_header() -> str:
    return (
        HERE
        / ".."
        / "cz_keep_a_changelog_plugin"
        / "templates"
        / "CHANGELOG_HEADER.md.j2"
    ).read_text(encoding="utf-8")


def test_bump_map(config: BaseConfig) -> None:
    plugin = CzKeepAChangelogPlugin(config)
    assert plugin.bump_map == OrderedDict(
        (
            (r"^.+!$", "MAJOR"),
            (r"^feat", "MINOR"),
            (r"^revert", "MINOR"),
            (r"^fix", "PATCH"),
            (r"^perf", "PATCH"),
            (r"^refactor", "PATCH"),
        )
    )


def test_bump_map_major_version_zero(config: BaseConfig) -> None:
    plugin = CzKeepAChangelogPlugin(config)
    assert plugin.bump_map_major_version_zero == OrderedDict(
        (
            (r"^.+!$", "MINOR"),
            (r"^feat", "MINOR"),
            (r"^revert", "MINOR"),
            (r"^fix", "PATCH"),
            (r"^perf", "PATCH"),
            (r"^refactor", "PATCH"),
        )
    )


def test_bump_pattern(config: BaseConfig) -> None:
    plugin = CzKeepAChangelogPlugin(config)
    assert plugin.bump_pattern == r"^(\w+(\(.+\))?!?):"
    assert isinstance(re.compile(plugin.bump_pattern), re.Pattern)


@pytest.mark.parametrize(
    ("changelog_out", "add_header"),
    [
        (
            "## [0.0.1] - 2026-05-10\n"
            "\n"
            "### Added\n"
            "\n"
            "- Name plugin settings properly\n"
            "- Add plugin\n"
            "\n"
            "### Fixed\n"
            "\n"
            "- Fix template loader location\n",
            False,
        ),
        (
            "## [0.0.1] - 2026-05-10\n"
            "\n"
            "### Added\n"
            "\n"
            "- Name plugin settings properly\n"
            "- Add plugin\n"
            "\n"
            "### Fixed\n"
            "\n"
            "- Fix template loader location\n",
            True,
        ),
    ],
)
def test_changelog_hook(
    changelog_out: str,
    add_header: bool,
    changelog_header: str,
    config: BaseConfig,
) -> None:
    plugin = CzKeepAChangelogPlugin(config)
    new_changelog_out = plugin.changelog_hook(
        (changelog_header + "\n" if add_header else "") + changelog_out,
        changelog_out,
    )
    assert changelog_header in new_changelog_out
    assert new_changelog_out == (changelog_header + "\n" + changelog_out)


@pytest.mark.parametrize(
    ("message", "parsed_message", "commit"),
    [
        (
            {
                "message": (
                    "feat: Issue #123, [#123](www.example.com), "
                    "[link](www.example.com/#123)"
                )
            },
            {
                "message": (
                    "feat: Issue [#123](https://github.com/CoLa5/cz-keep-a-changelog-plugin/issues/123), "  # noqa: E501
                    "[#123](www.example.com), [link](www.example.com/#123)"
                )
            },
            git.GitCommit(
                rev="3278ffc707aaacc6f78c3d46d2130da0cfff9e3b",
                title="Issue 123",
            ),
        )
    ],
)
def test_changelog_message_builder_hook(
    message: dict[str, Any],
    parsed_message: dict[str, Any],
    commit: git.GitCommit,
    config: BaseConfig,
) -> None:
    plugin = CzKeepAChangelogPlugin(config)
    message = plugin.changelog_message_builder_hook(message, commit)
    for key in parsed_message:
        assert key in message
        assert message[key] == parsed_message[key]


def test_commit_parser(config: BaseConfig) -> None:
    plugin = CzKeepAChangelogPlugin(config)
    assert plugin.commit_parser == (
        r"^((?P<change_type>feat|fix|perf|refactor|revert)"
        r"(?:\((?P<scope>[^()\r\n]*)\)|\()?(?P<breaking>!)?|\w+!):"
        r"\s(?P<message>.*)?"
    )
    assert isinstance(re.compile(plugin.commit_parser), re.Pattern)


def test_questions(config: BaseConfig) -> None:
    plugin = CzKeepAChangelogPlugin(config)
    questions = plugin.questions()
    assert isinstance(questions, list)
    assert isinstance(questions[0], dict)


def test_choices_all_have_keyboard_shortcuts(config: BaseConfig) -> None:
    plugin = CzKeepAChangelogPlugin(config)
    questions = plugin.questions()

    list_questions = (q for q in questions if q["type"] == "list")
    for select in list_questions:
        assert all("key" in choice for choice in select["choices"])


def test_small_answer(config: BaseConfig) -> None:
    plugin = CzKeepAChangelogPlugin(config)
    answers = {
        "prefix": "fix",
        "scope": "users",
        "subject": "email pattern corrected",
        "is_breaking_change": False,
        "body": "",
        "footer": "",
    }
    message = plugin.message(answers)
    assert message == "fix(users): email pattern corrected"


def test_long_answer(config: BaseConfig) -> None:
    plugin = CzKeepAChangelogPlugin(config)
    answers = {
        "prefix": "fix",
        "scope": "users",
        "subject": "email pattern corrected",
        "is_breaking_change": False,
        "body": "complete content",
        "footer": "closes #24",
    }
    message = plugin.message(answers)
    assert message == (
        "fix(users): email pattern corrected\n\ncomplete content\n\ncloses #24"
    )


def test_breaking_change_in_footer(config: BaseConfig) -> None:
    plugin = CzKeepAChangelogPlugin(config)
    answers = {
        "prefix": "fix",
        "scope": "users",
        "subject": "email pattern corrected",
        "is_breaking_change": True,
        "body": "complete content",
        "footer": "migrate by renaming user to users",
    }
    message = plugin.message(answers)
    assert message == (
        "fix(users): email pattern corrected\n\ncomplete content\n\n"
        "BREAKING CHANGE: migrate by renaming user to users"
    )


@pytest.mark.parametrize(
    ("scope", "breaking_change_exclamation_in_title", "expected_message"),
    [
        # Test with scope and breaking_change_exclamation_in_title enabled
        (
            "users",
            True,
            (
                "feat(users)!: email pattern corrected\n\ncomplete content\n\n"
                "BREAKING CHANGE: migrate by renaming user to users"
            ),
        ),
        # Test without scope and breaking_change_exclamation_in_title enabled
        (
            "",
            True,
            (
                "feat!: email pattern corrected\n\ncomplete content\n\n"
                "BREAKING CHANGE: migrate by renaming user to users"
            ),
        ),
        # Test with scope and breaking_change_exclamation_in_title disabled
        (
            "users",
            False,
            (
                "feat(users): email pattern corrected\n\ncomplete content\n\n"
                "BREAKING CHANGE: migrate by renaming user to users"
            ),
        ),
        # Test without scope and breaking_change_exclamation_in_title disabled
        (
            "",
            False,
            (
                "feat: email pattern corrected\n\ncomplete content\n\n"
                "BREAKING CHANGE: migrate by renaming user to users"
            ),
        ),
    ],
)
def test_breaking_change_message_formats(
    config: BaseConfig,
    scope: str,
    breaking_change_exclamation_in_title: bool,
    expected_message: str,
) -> None:
    # Set the breaking_change_exclamation_in_title setting
    config.settings["breaking_change_exclamation_in_title"] = (
        breaking_change_exclamation_in_title
    )
    plugin = CzKeepAChangelogPlugin(config)
    answers = {
        "prefix": "feat",
        "scope": scope,
        "subject": "email pattern corrected",
        "is_breaking_change": True,
        "body": "complete content",
        "footer": "migrate by renaming user to users",
    }
    message = plugin.message(answers)
    assert message == expected_message


def test_example(config: BaseConfig) -> None:
    """just testing a string is returned. not the content"""
    plugin = CzKeepAChangelogPlugin(config)
    example = plugin.example()
    assert isinstance(example, str)


def test_schema(config: BaseConfig) -> None:
    """just testing a string is returned. not the content"""
    plugin = CzKeepAChangelogPlugin(config)
    schema = plugin.schema()
    assert isinstance(schema, str)


def test_info(config: BaseConfig) -> None:
    """just testing a string is returned. not the content"""
    plugin = CzKeepAChangelogPlugin(config)
    info = plugin.info()
    assert isinstance(info, str)
