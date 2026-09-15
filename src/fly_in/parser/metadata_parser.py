"""Parsing of bracketed key=value metadata strings."""

from typing import Any


def get_metadata(value: str) -> dict[str, Any]:
    """Parse a bracketed `[key=value ...]` metadata string.

    Args:
        value (str): Metadata string, e.g. `"[zone=blocked]"`.

    Returns:
        dict[str, Any]: Parsed key-value pairs.

    Raises:
        ValueError: If the string is not enclosed in square brackets.
    """
    if value.startswith("[") and value.endswith("]"):
        content: list[str] = value[1:-1].split()
        res: dict[str, Any] = {}

        for c in content:
            k, v = c.split("=")
            res[k] = v

        return res

    else:
        raise ValueError("Metadata must be enclosed with []")
