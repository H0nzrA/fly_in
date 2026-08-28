from .cli import MapSelector
from .parser import Parser
from pathlib import Path
from .domain import Map
from .graph import Graph
from .solver import Manager


class Program:
    def __init__(self) -> None:
        selector: MapSelector = MapSelector()
        path: Path = selector.get_map_path()
        parser: Parser = Parser(path=path)

        self.__map: Map = parser.get_map()
        self.__graph: Graph = Graph(map=self.__map)

    def run(self) -> None:
        manager: Manager = Manager(
            graph=self.__graph,
            nb_agent=self.__map.nb_drones
        )

        paths: dict[int, list[int]] = manager.compute_drones()

        for drone, path in paths.items():
            print(f"{drone}: {path}")
