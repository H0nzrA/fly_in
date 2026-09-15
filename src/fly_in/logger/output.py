"""Formatting and writing of solved drone paths."""

from ..graph import Graph, State
from pathlib import Path
from ..utils import write_content


class Output:
    """Formats solved drone paths into a turn-by-turn text report."""

    def __init__(self, graph: Graph, path: str | Path) -> None:
        """Initialize the output writer.

        Args:
            graph (Graph): Graph used to resolve node ids to zone names.
            path (str | Path): Destination file for the output report.
        """
        self.__graph: Graph = graph
        self.__path: str | Path = path

    def make_output(self, paths: dict[int, list[State]]) -> None:
        """Format and write the solved drone paths to the output file.

        Args:
            paths (dict[int, list[State]]): Solved path per drone id.
        """
        content: str = self.formated_output(paths)
        write_content(self.__path, content)

    def formated_output(self, paths: dict[int, list[State]]) -> str:
        """Format the solved drone paths into a turn-by-turn report.

        Args:
            paths (dict[int, list[State]]): Solved path per drone id.

        Returns:
            str: The formatted report text.
        """
        per_turns: dict[int, list[str]] = self.__drones_paths(paths)
        total_turn: int = self.__get_total_turn(paths)

        per_content: list[str] = []
        for turn in per_turns.values():
            res: str = " ".join(turn)
            per_content.append(res)

        content: str = "\n".join(per_content)
        content += "\n\n" + f"Total turn: {total_turn}"

        return content

    def __drones_paths(
        self,
        paths: dict[int, list[State]],
    ) -> dict[int, list[str]]:
        """Group drone movements by the turn in which they occur.

        Args:
            paths (dict[int, list[State]]): Solved path per drone id.

        Returns:
            dict[int, list[str]]: Movement descriptions per turn.

        Raises:
            ValueError: If the extracted turns do not match the total turn
                count.
        """
        total_turn: int = self.__get_total_turn(paths)
        turns: dict[int, list[str]] = {
            i: []
            for i in range(1, total_turn + 1)
        }

        for drone_id, path in paths.items():
            for i in range(len(path) - 1):
                current_node, current_time = path[i]
                next_node, next_time = path[i + 1]

                if next_time <= current_time:
                    continue

                if current_node == next_node:
                    continue

                delta: int = next_time - current_time
                drone: str = f"D{drone_id}"
                czone: str = self.__graph.get_zone_by_id(current_node).name
                nzone: str = self.__graph.get_zone_by_id(next_node).name

                on_zone: str = "-".join([drone, nzone])
                on_connection = "-".join([drone, czone, nzone])

                if delta != 1:

                    for time in range(current_time + 1, next_time):
                        turns[time].append(on_connection)

                turns[next_time].append(on_zone)

        if len(turns) != total_turn:
            raise ValueError(
                f"Extracted turns have not total turn = {total_turn}"
            )

        return turns

    def __get_total_turn(self, paths: dict[int, list[State]]) -> int:
        """Find the last turn number reached across all drone paths.

        Args:
            paths (dict[int, list[State]]): Solved path per drone id.

        Returns:
            int: The final turn number.
        """
        return max(
            state[1]
            for path in paths.values()
            for state in path
        )
