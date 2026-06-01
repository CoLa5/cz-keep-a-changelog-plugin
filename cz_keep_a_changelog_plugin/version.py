"""Version."""

import importlib.metadata
import pathlib
from typing import Final

CZ_KEEP_A_CHANGELOG_PLUGIN_VERSION: Final[str] = importlib.metadata.version(
    pathlib.Path(__file__).parent.name
)
