"""
utils.py - Shared Runtime Utilities for BookletsGo.
Provides path resolution helpers that work correctly both in development
and when the application is bundled with PyInstaller.
"""

import os
import sys


def resource_path(*parts: str) -> str:
    """
    Resolves the absolute path to a bundled resource file.

    In development, paths are resolved relative to the project root (where run.py lives).
    When bundled with PyInstaller, resources are extracted to a temporary _MEIPASS
    directory at runtime — this function handles both cases transparently.

    Usage:
        resource_path("bookletsgo.ico")
        resource_path("assets", "fonts", "Inter-Regular.ttf")
        resource_path("assets", "icons", "bookletsgo.ico")
        (if the sample files are located in the assets/fonts/ or assets/icons/ folders)

    Args:
        *parts: Path components, joined with os.path.join.
                Accepts both flat strings and nested path segments.

    Returns:
        Absolute path string to the requested resource.

    Raises:
        FileNotFoundError: If the resolved path does not exist on disk.
    """
    base = getattr(sys, "_MEIPASS", _project_root())
    resolved = os.path.join(base, *parts)

    if not os.path.exists(resolved):
        raise FileNotFoundError(
            f"Resource not found: '{resolved}'\n"
            f"Make sure it is included via --add-data in your PyInstaller command."
        )

    return resolved


def _project_root() -> str:
    """
    Returns the absolute path of the project root directory.
    Defined as the directory containing run.py (one level above this file's package).
    """
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
