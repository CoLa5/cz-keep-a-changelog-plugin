"""
.. include:: ../README.md
   :end-before: # Commitizen - Keep a Changelog-Plugin

---

.. include:: ../README.md
   :start-after: # Commitizen - Keep a Changelog-Plugin

---
"""  # noqa: D212, D415

# ruff: noqa: RUF067

from cz_keep_a_changelog_plugin.utils import stop_circular_import

with stop_circular_import():
    from cz_keep_a_changelog_plugin.cz_keep_a_changelog_plugin import (
        CzKeepAChangelogPlugin,
    )
from cz_keep_a_changelog_plugin.version import (
    CZ_KEEP_A_CHANGELOG_PLUGIN_VERSION,
)

__docformat__ = "google"
__license__ = "MIT"
__version__ = CZ_KEEP_A_CHANGELOG_PLUGIN_VERSION

__all__ = (
    "CzKeepAChangelogPlugin",
    "__license__",
    "__version__",
)
