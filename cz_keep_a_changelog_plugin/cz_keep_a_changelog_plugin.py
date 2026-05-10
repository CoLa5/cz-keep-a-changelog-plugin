"""'Keep a Changelog'-Conventional Commits-Plugin."""

# mypy: disable-error-code=assignment
# ruff: noqa: RUF012

from collections import OrderedDict
from collections.abc import Iterable
import re
from typing import Any, TypedDict

from commitizen import git
from commitizen.config.base_config import BaseConfig
from commitizen.cz.conventional_commits.conventional_commits import (
    ConventionalCommitsCz,
)
from commitizen.cz.conventional_commits.conventional_commits import _parse_scope
from commitizen.cz.conventional_commits.conventional_commits import (
    _parse_subject,
)
from commitizen.cz.utils import multiple_line_breaker
from commitizen.defaults import MAJOR
from commitizen.defaults import MINOR
from commitizen.defaults import PATCH
from commitizen.question import CzQuestion
import jinja2 as j2


class CzPluginSettings(TypedDict, total=False):
    """Plugin Settings."""

    issue_url_template: str


class CzKeepAChangelogPlugin(ConventionalCommitsCz):
    """'Keep a Changelog'-Conventional Commits-Plugin."""

    bump_pattern: str | None = r"^(\w+)(\(.+\))?!?):"
    bump_map: dict[str, str] | None = OrderedDict(
        (
            (r"^.+!$", MAJOR),
            (r"^feat", MINOR),
            (r"^revert", MINOR),
            (r"^fix", PATCH),
            (r"^perf", PATCH),
            (r"^refactor", PATCH),
        )
    )
    bump_map_major_version_zero: dict[str, str] | None = OrderedDict(
        (
            (r"^.+!$", MINOR),
            (r"^feat", MINOR),
            (r"^revert", MINOR),
            (r"^fix", PATCH),
            (r"^perf", PATCH),
            (r"^refactor", PATCH),
        )
    )

    commit_parser: str | None = (
        r"^((?P<change_type>feat|fix|perf|refactor|revert)"
        r"(?:\((?P<scope>[^()\r\n]*)\)|\()?(?P<breaking>!)?|\w+!):"
        r"\s(?P<message>.*)?"
    )
    changelog_pattern: str | None = bump_pattern
    change_type_map: dict[str, str] | None = {
        "feat": "Added",
        "fix": "Fixed",
        "perf": "Changed",
        "refactor": "Changed",
        "revert": "Removed",
    }
    change_type_order: list[str] | None = [
        "Added",
        "Changed",
        "Deprecated",
        "Removed",
        "Fixed",
        "Security",
    ]

    template_header: str = "CHANGELOG_HEADER.md.j2"
    template_loader: j2.BaseLoader = j2.PackageLoader(
        "cz_keep_a_changelog_plugin", "templates"
    )
    template_extras: dict[str, Any] = {}

    def __init__(self, config: BaseConfig) -> None:
        """Initializes the class.

        Args:
            config: The base config of `commitizen`.
        """
        super().__init__(config)
        self.plugin_settings: CzPluginSettings = self.config.settings.get(
            "cz_keep_a_changelog_plugin", {}
        )

    def changelog_hook(
        self,
        changelog_out: str,
        partial_changelog: str | None,
    ) -> str:
        """Customizes the complete changelog or uses it to call further
        functionality.

        Here, the header will be added if not done before.

        Args:
            changelog_out: The full changelog.
            partial_changelog: The partial (if used `incremental`) changelog,
                else `None`.

        Returns:
            Must return the complete changelog.
        """
        loader = j2.ChoiceLoader(
            [j2.FileSystemLoader("."), self.template_loader]
        )
        env = j2.Environment(loader=loader, trim_blocks=True)
        jinja_template_header = env.get_template(self.template_header)
        header = jinja_template_header.render(
            **self.template_extras,
            **self.config.settings["extras"],
        )
        header = header.strip()
        if changelog_out.startswith(header):
            return changelog_out
        return "\n\n".join((header, changelog_out))

    def changelog_message_builder_hook(
        self,
        message: dict[str, Any],
        commit: git.GitCommit,
    ) -> dict[str, Any] | Iterable[dict[str, Any]] | None:
        """Customizes the changelog message with extra information, like adding
        links.

        This function is executed per parsed commit. Each `GitCommit` contains
        the following attrs: `rev`, `title`, `body`, `author`, `author_email`.

        Here, the issue number is replaced by a markdown link using the issue
        url template.

        Args:
            message: The message to customize.
            commit: The original `GitCommit`.

        Returns:
            A customized message or a falsy value to ignore the commit.
        """
        if "issue_url_template" in self.plugin_settings:
            issue_url_template = j2.Template(
                self.plugin_settings["issue_url_template"]
            )

            def sub_issue_num(match: re.Match[str]) -> str:
                issue_num = match.group(1)
                issue_url = issue_url_template.render(issue=issue_num)
                return f"[#{issue_num:s}]({issue_url:s})"

            message["message"] = re.sub(
                r"#(\d+)", sub_issue_num, message["message"]
            )

        return message

    def questions(self) -> list[CzQuestion]:
        """Returns the questions regarding the commit message.

        Returns:
            The questions.
        """
        return [
            {
                "type": "list",
                "name": "prefix",
                "message": "Select the type of change you are committing",
                "choices": [
                    {
                        "value": "feat",
                        "name": (
                            "feat: A new feature. Correlates with MINOR in "
                            "SemVer"
                        ),
                        "key": "f",
                    },
                    {
                        "value": "fix",
                        "name": (
                            "fix: A bug fix. Correlates with PATCH in SemVer"
                        ),
                        "key": "x",
                    },
                    {
                        "value": "docs",
                        "name": "docs: Documentation only changes",
                        "key": "d",
                    },
                    {
                        "value": "style",
                        "name": (
                            "style: Changes that do not affect the meaning of "
                            "the code (white-space, formatting, missing "
                            "semi-colons, etc)"
                        ),
                        "key": "s",
                    },
                    {
                        "value": "refactor",
                        "name": (
                            "refactor: A code change that neither fixes a bug "
                            "nor adds a feature"
                        ),
                        "key": "r",
                    },
                    {
                        "value": "perf",
                        "name": "perf: A code change that improves performance",
                        "key": "p",
                    },
                    {
                        "value": "test",
                        "name": (
                            "test: Adding missing tests or correcting existing "
                            "tests"
                        ),
                        "key": "t",
                    },
                    {
                        "value": "build",
                        "name": (
                            "build: Changes that affect the build system or "
                            "external dependencies (example scopes: pip, "
                            "docker, npm)"
                        ),
                        "key": "b",
                    },
                    {
                        "value": "ci",
                        "name": (
                            "ci: Changes to CI configuration files and scripts "
                            "(example scopes: GitLabCI)"
                        ),
                        "key": "c",
                    },
                    {
                        "value": "chore",
                        "name": (
                            "Other changes that don't modify src or test files"
                        ),
                        "key": "h",
                    },
                    {
                        "value": "revert",
                        "name": (
                            "Reverts a previous commit. Put reverted commit "
                            "SHAs into footer as'Refs: 676104e, a215868'"
                        ),
                        "key": "v",
                    },
                ],
            },
            {
                "type": "input",
                "name": "scope",
                "message": (
                    "What is the scope of this change? (class or file name): "
                    "(press [enter] to skip)\n"
                ),
                "filter": _parse_scope,
            },
            {
                "type": "input",
                "name": "subject",
                "filter": _parse_subject,
                "message": (
                    "Write a short and imperative summary of the code changes: "
                    "(lower case and no period)\n"
                ),
            },
            {
                "type": "input",
                "name": "body",
                "message": (
                    "Provide additional contextual information about the code "
                    "changes: (press [enter] to skip)\n"
                ),
                "filter": multiple_line_breaker,
            },
            {
                "type": "confirm",
                "name": "is_breaking_change",
                "message": (
                    "Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer"
                ),
                "default": False,
            },
            {
                "type": "input",
                "name": "footer",
                "message": (
                    "Footer. Information about Breaking Changes and reference "
                    "issues that this commit closes: (press [enter] to skip)\n"
                ),
            },
        ]
