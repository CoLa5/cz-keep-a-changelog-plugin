"""Test of Plugin."""

from collections import OrderedDict
import re

from commitizen.config import BaseConfig
import pytest

from cz_keep_a_changelog_plugin import CzKeepAChangelogPlugin


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
