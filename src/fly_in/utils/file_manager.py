"""Helpers for writing generated content to disk."""

from pathlib import Path


def write_content(path: str | Path, content: str) -> None:
    """Write text content to a file, creating parent directories as needed.

    Args:
        path (str | Path): Destination file path.
        content (str): Text content to write.
    """
    p: Path = Path(path)

    parent: Path = p.parent
    parent.mkdir(parents=True, exist_ok=True)

    with p.open("w") as f:
        f.write(content)
