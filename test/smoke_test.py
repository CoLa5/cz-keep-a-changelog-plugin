"""Check that basic features work.

Catch cases where e.g. files are missing so the import doesn't work. It is
recommended to check that e.g. assets are included.
"""
# ruff: noqa: F401

import commitizen

import cz_keep_a_changelog_plugin

print("Basic import does work")
