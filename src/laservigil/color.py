"""The one and only color helper: cyan/magenta on black.

Color is disabled when the NO_COLOR environment variable is set to a
non-empty value (https://no-color.org) or when the stream is not a TTY.
"""

from __future__ import annotations

import os
import sys
from typing import Mapping, TextIO

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36;40m"
MAGENTA = "\033[35;40m"
BRIGHT_CYAN = "\033[96;40m"
BRIGHT_MAGENTA = "\033[95;40m"


def color_enabled(
    stream: TextIO | None = None, env: Mapping[str, str] | None = None
) -> bool:
    """Return True if ANSI color should be written to ``stream``."""
    env = os.environ if env is None else env
    if env.get("NO_COLOR", ""):
        return False
    stream = sys.stdout if stream is None else stream
    isatty = getattr(stream, "isatty", None)
    try:
        return bool(isatty and isatty())
    except (ValueError, OSError):
        return False


class Palette:
    """Wraps text in synthwave colors, or passes it through untouched."""

    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    @classmethod
    def for_stream(
        cls, stream: TextIO | None = None, env: Mapping[str, str] | None = None
    ) -> "Palette":
        return cls(color_enabled(stream, env))

    def _wrap(self, code: str, text: str, bold: bool = False) -> str:
        if not self.enabled:
            return text
        prefix = (BOLD if bold else "") + code
        return f"{prefix}{text}{RESET}"

    def cyan(self, text: str, bold: bool = False) -> str:
        return self._wrap(CYAN, text, bold)

    def magenta(self, text: str, bold: bool = False) -> str:
        return self._wrap(MAGENTA, text, bold)

    def glow(self, text: str) -> str:
        """Headline style: bright magenta, bold."""
        return self._wrap(BRIGHT_MAGENTA, text, bold=True)

    def accent(self, text: str) -> str:
        """Secondary highlight: bright cyan."""
        return self._wrap(BRIGHT_CYAN, text)
