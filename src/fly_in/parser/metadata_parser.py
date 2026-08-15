from typing import Any


def get_metadata(value: str) -> dict[str, Any]:
    if value.startswith("[") and value.endswith("]"):
        content: list[str] = value[1:-1].split()
        res: dict[str, Any] = {}

        for c in content:
            k, v = c.split("=")
            res[k] = v

        return res

    else:
        raise ValueError("Metadata must be enclosed with []")
