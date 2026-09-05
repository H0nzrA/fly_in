from pathlib import Path
from typing import Callable, Any
import tracemalloc
from dataclasses import dataclass
import time
from datetime import timedelta
from ..domain import Map
from ..utils import write_content


@dataclass
class BenchmarkState:
    current: float
    peak: float
    execution: float


class Benchmark:
    def __init__(
        self,
        path: str | Path,
        _map: Map,
        map_file: str | Path
    ) -> None:
        self.__path: Path = Path(path)
        self.__saved: dict[str, BenchmarkState] = {}
        self.__map_info: str = self.__extract_map_mark(_map, map_file)

    def __extract_map_mark(self, _map: Map, map_file: str | Path) -> str:
        res: str = ""

        title: str = str(map_file)
        nb_drone: str = str(_map.nb_drones)
        nb_zone: str = str(len(_map.hubs) + 2)
        nb_edge: str = str(len(_map.connections))

        res += f"- Map file: {title}\n\n"
        res += f"- Number of drones: {nb_drone}\n"
        res += f"- Number of zones: {nb_zone}\n"
        res += f"- Number of edge: {nb_edge}\n"

        return res

    def run(
        self,
        name: str,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any
    ) -> Any:
        tracemalloc.start()
        start: float = time.perf_counter()

        try:
            return func(*args, **kwargs)
        finally:
            end: float = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            state: BenchmarkState = BenchmarkState(
                current=(current / 1024 / 1024),
                peak=(peak / 1024 / 1024),
                execution=(end - start)
            )
            self.__saved[name] = state

    def output_benchmark(self) -> None:
        content: str = self.__format_title()
        content += "\n\n".join(
            [
                self.__format_output(title, bench)
                for title, bench in self.__saved.items()
            ]
        )

        write_content(self.__path, content)

    def __format_output(
        self,
        title: str,
        state: BenchmarkState
    ) -> str:

        res: str = f"\n--- {title} ---\n"
        res += f"- Current: {state.current:.2f}MB\n"
        res += f"- Peak: {state.peak:.2f}MB\n"

        t: timedelta = timedelta(seconds=state.execution)
        res += f"- Executed in: {t}"

        return res

    def __format_title(self) -> str:
        res: str = "=" * 30
        res += "\n" + self.__map_info + "\n"
        res += "=" * 30
        res += "\n\n"
        return res
