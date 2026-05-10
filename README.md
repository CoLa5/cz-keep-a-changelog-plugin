[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://mit-license.org/2026)
[![prek](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Checks: flake-8, isort, mypy](https://img.shields.io/badge/Checks-flake--8,_isort,_mypy-green.svg)](https://github.com/CoLa5/cz-keep-a-changelog-plugin/blob/main/.pyproject.toml)

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
[![GitHub last commit](https://img.shields.io/github/last-commit/CoLa5/cz-keep-a-changelog-plugin)](https://github.com/CoLa5/cz-keep-a-changelog-plugin/commits/main)

# cz-keep-a-changelog-plugin

Adds full compliance with
[Keep a Changelog v1.1.0](https://keepachangelog.com/en/1.1.0/)

## Features

- Complete map of Conventional Commits to "Keep a Changelog"-types of changes
- Enables to replace issue numbers by a markdown link to the issue in the
  changelog

## Additional Settings

In the project's `pyproject.toml`set:

```toml title="pyproject.toml"
...

[tool.commitizen]
name = "cz_keep_a_changelog_plugin"
...

[tool.commitizen.cz_keep_a_changelog_plugin]
issue_url_template = "https://cola5.github.io/cz-keep-a-changelog-plugin/issues/{{issue}}"
```
