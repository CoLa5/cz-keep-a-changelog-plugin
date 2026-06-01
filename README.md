[![Python Support](https://img.shields.io/pypi/pyversions/cz_keep_a_changelog_plugin)](https://pypi.org/project/cz_keep_a_changelog_plugin/)
[![Pypi Latest Version](https://img.shields.io/pypi/v/cz_keep_a_changelog_plugin)](https://pypi.org/project/cz_keep_a_changelog_plugin#history)
[![Python Types](https://img.shields.io/pypi/types/cz_keep_a_changelog_plugin)](https://pypi.org/project/cz_keep_a_changelog_plugin/)
[![Documentation](https://img.shields.io/badge/docs-github.io-blue.svg)](https://cola5.github.io/cz-keep-a-changelog-plugin)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://mit-license.org/2026)

[![CI](https://github.com/CoLa5/cz-keep-a-changelog-plugin/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/CoLa5/cz-keep-a-changelog-plugin/actions/workflows/ci.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/CoLa5/cz-keep-a-changelog-plugin/blob/main/.pre-commit-config.yaml)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/CoLa5/0fc173cdcadeefda86451e0f4c4d763c/raw/covbadge.json)](https://cola5.github.io/cz-keep-a-changelog-plugin/coverage/)
[![Pypi Trusted Publisher: enabled](https://img.shields.io/badge/Pypi_Trusted_Publisher-enabled-green.svg)](https://blog.pypi.org/posts/2023-04-20-introducing-trusted-publishers/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Checks: flake-8, isort, mypy](https://img.shields.io/badge/Checks-flake--8,_isort,_mypy-green.svg)](https://github.com/CoLa5/cz-keep-a-changelog-plugin/blob/main/.pyproject.toml)

[![Commitizen](https://img.shields.io/badge/Commitizen-enabled-9b1fe8.svg)](https://commitizen-tools.github.io/commitizen/)
[![Conventional Commits](https://img.shields.io/badge/Conventional_Commits-v1.0.0-fa6673.svg)](https://www.conventionalcommits.org/en/v1.0.0/)
[![Keep a Changelog](https://img.shields.io/badge/Keep_a_Changelog-v1.1.0-E05735.svg)](https://keepachangelog.com/en/1.1.0/)
[![GitHub last commit](https://img.shields.io/github/last-commit/CoLa5/cz-keep-a-changelog-plugin)](https://github.com/CoLa5/cz-keep-a-changelog-plugin/commits/main)

# Commitizen - Keep a Changelog-Plugin

<img src="https://cola5.github.io/cz-keep-a-changelog-plugin/assets/logo.svg" title="cz-keep-a-changelog-plugin logo" width="50%" />

Adds full compliance of
[Commitizen](https://commitizen-tools.github.io/commitizen/) with
[Keep a Changelog v1.1.0](https://keepachangelog.com/en/1.1.0/).

## Features

- Complete map of
  [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)-types
  to [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)-types of changes:
  - `feat`: `Added`
  - `fix`: `Fixed`
  - `perf`: `Changed`
  - `refactor`: `Changed`
  - `revert`: `Removed`
- Enables to replace issue numbers in the changelog by a markdown link to the
  issue:  
  `#123` -> `[#123](https://github.com/user/repo/issues/123)`
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)-like
  [header](https://github.com/CoLa5/cz-keep-a-changelog-plugin/blob/main/cz_keep_a_changelog_plugin/templates/CHANGELOG_HEADER.md.j2)
  for changelog file.

## Installation

**Using pip:**

```bash
# Install
pip install cz_keep_a_changelog_plugin

# Keep it updated
pip upgrade cz_keep_a_changelog_plugin
```

**Using uv:**

```bash
# Install
uv install cz_keep_a_changelog_plugin

# Keep it updated
uv upgrade cz_keep_a_changelog_plugin
```

## Usage

### Configuration

In the project's `pyproject.toml` set:

```toml
...

[tool.commitizen]
name = "cz_keep_a_changelog_plugin"
```

### Pre-Commit

To use in pre-commit, add this to your `pre-commit-config.yml`. Run pre-commit
autoupdate to get the latest version:

```yaml
repos:
  - repo: https://github.com/commitizen-tools/commitizen
    rev: main
    hooks:
      - id: commitizen
        additional_dependencies: [cz_keep_a_changelog_plugin]
        stages: [commit-msg]
      - id: commitizen-branch
        additional_dependencies: [cz_keep_a_changelog_plugin]
        stages: [pre-push]
```

## Additional Settings

In the project's `pyproject.toml`set the `issue_url_template` where `{{issue}}`
will be replaced by the issue number:

```toml
...

[tool.commitizen]
name = "cz_keep_a_changelog_plugin"
...

[tool.commitizen.cz_keep_a_changelog_plugin]
issue_url_template = "https://cola5.github.io/cz-keep-a-changelog-plugin/issues/{{issue}}"
```
