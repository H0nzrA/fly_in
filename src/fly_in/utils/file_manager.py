from pathlib import Path


def write_content(path: str | Path, content: str) -> None:
    p: Path = Path(path)

    parent: Path = p.parent
    parent.mkdir(parents=True, exist_ok=True)

    with p.open("w") as f:
        f.write(content)
