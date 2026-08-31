"""
ANSI terminal formatting codes.

Defined ANSI escape sequences for text styling, colors,
and cursor control used by the command-line interface.
"""

from enum import StrEnum


class Syntax(StrEnum):
    """
    ANSI escape sequences for terminal formatting.

    Provides constants for text styles, colors,
    screen clearing and cursor movement.
    """

    RESET = "\033[0m"
    CLEAR = "\033[H\033[J"
    CLEAR_LINE = "\033[2K"

    CURSOR_HOME = "\r"
    CURSOR_UP = "\033[1A"

    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    DARK_CYAN = "\033[38;5;30m"
    DARK_BLUE = "\033[38;5;24m"
    DARK_GREEN = "\033[38;5;28m"
    DARK_PURPLE = "\033[38;5;54m"
