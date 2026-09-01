from pathlib import Path
from typing import Callable, Any
from functools import wraps
import tracemalloc
from dataclasses import dataclass
import time
from datetime import timedelta


@dataclass
class MemoryState:
    current: float
    peak: float
    execution: float


class Benchmark:
    def __init__(self, path: str | Path) -> None:
        self.__path: Path = Path(path)
        self.__saved: dict[str, MemoryState] = {}

    def mark_memory(self, name: str) -> Callable[..., Any]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                tracemalloc.start()

                start: float = time.perf_counter()
                res: Any = func(*args, **kwargs)
                end: float = time.perf_counter()

                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                mem_state: MemoryState = MemoryState(
                    current=(current / 1024 / 1024),
                    peak=(peak / 1024 / 1024),
                    execution=(end - start)
                )

                self.__saved[name] = mem_state

                return res

            return wrapper

        return decorator

    def output_benchmark(self) -> None:
        content: str = "\n\n".join(
            [
                self.__format_output(title, bench)
                for title, bench in self.__saved.items()
            ]
        )

        with self.__path.open("w") as f:
            f.write(content)

    def __format_output(
        self,
        title: str,
        state: MemoryState
    ) -> str:
        res: str = f"=== {title} ===\n"
        res += f"- Current: {state.current:.2f}MB\n"
        res += f"- Peak: {state.peak:.2f}MB\n"

        t: timedelta = timedelta(seconds=state.execution)
        res += f"- Executed in: {t}"

        return res
