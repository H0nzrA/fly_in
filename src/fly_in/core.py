from .cli import MapSelector
from .parser import Parser
from pathlib import Path
from .domain import Map
from .graph import Graph, State
from .solver import PrioritizedCooperative


class Program:
    def __init__(self) -> None:
        selector: MapSelector = MapSelector()
        path: Path = selector.get_map_path()
        parser: Parser = Parser(path=path)

        self.__map: Map = parser.get_map()
        self.__graph: Graph = Graph(map=self.__map)

        self.__solver: PrioritizedCooperative = PrioritizedCooperative(
            self.__graph
        )

    def run(self) -> None:
        paths: dict[int, list[State]] = self.__solver.compute(
            self.__map.nb_drones
        )
        for p in paths:
            path = " - ".join(
                f"{node}/{time}"
                for node, time in paths[p]
            )
            print(f"D{p}: {path}")
