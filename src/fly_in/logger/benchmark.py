"""Performance benchmarking and report generation."""

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
    """Snapshot of memory usage and execution time for one run.

    Attributes:
        current (float): Current traced memory usage, in megabytes.
        peak (float): Peak traced memory usage, in megabytes.
        execution (float): Execution time, in seconds.
    """

    current: float
    peak: float
    execution: float


class Benchmark:
    """Measures and reports execution time and memory usage of tasks."""

    def __init__(
        self,
        path: str | Path,
        _map: Map,
        map_file: str | Path
    ) -> None:
        """Initialize the benchmark with an output path and map summary.

        Args:
            path (str | Path): Destination file for the benchmark report.
            _map (Map): Map being benchmarked, used to summarize its size.
            map_file (str | Path): Path to the source map file, for display.
        """
        self.__path: Path = Path(path)
        self.__saved: dict[str, BenchmarkState] = {}
        self.__map_info: str = self.__extract_map_mark(_map, map_file)

    def __extract_map_mark(self, _map: Map, map_file: str | Path) -> str:
        """Build a text summary describing the map being benchmarked.

        Args:
            _map (Map): Map to summarize.
            map_file (str | Path): Path to the source map file, for display.

        Returns:
            str: A formatted summary of the map's size and source file.
        """
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
        """Run a function while tracking its execution time and memory usage.

        Args:
            name (str): Label under which to store the measured results.
            func (Callable[..., Any]): Function to run and measure.
            *args (Any): Positional arguments passed to `func`.
            **kwargs (Any): Keyword arguments passed to `func`.

        Returns:
            Any: The return value of `func`.
        """
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
        """Write the accumulated benchmark results to the output file."""
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
        """Format a single benchmark result as a text block.

        Args:
            title (str): Label of the benchmark entry.
            state (BenchmarkState): Measured memory and execution data.

        Returns:
            str: The formatted benchmark entry.
        """
        res: str = f"\n--- {title} ---\n"
        res += f"- Current: {state.current:.2f}MB\n"
        res += f"- Peak: {state.peak:.2f}MB\n"

        t: timedelta = timedelta(seconds=state.execution)
        res += f"- Executed in: {t}"

        return res

    def __format_title(self) -> str:
        """Format the report header containing the map summary.

        Returns:
            str: The formatted report header.
        """
        res: str = "=" * 30
        res += "\n" + self.__map_info + "\n"
        res += "=" * 30
        res += "\n\n"
        return res
