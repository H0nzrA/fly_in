from .cli import MapSelector
from .parser import Parser
from pathlib import Path
from .domain import Map
from .graph import Graph
from .solver import Dijkstra, AStar


class Program:
    def __init__(self) -> None:
        selector: MapSelector = MapSelector()
        path: Path = selector.get_map_path()
        parser: Parser = Parser(path=path)

        self.__map: Map = parser.get_map()
        self.__graph: Graph = Graph(map=self.__map)

    def run(self) -> None:
        if self.__map and self.__graph:
            print("Everything is initialized")

        distances: dict[int, float] = Dijkstra().compute_distance(
            self.__graph,
            self.__graph.end_node(),
            self.__graph.start_node()
        )

        for node, dist in distances.items():
            print(
                f"{self.__graph.get_zone_by_id(node).name} - {dist}"
            )
        solver: AStar = AStar()

        path: list[int] = solver.solve(
            self.__graph,
            self.__graph.end_node(),
            self.__graph.start_node(), distances
        )

        for p in path:
            print(self.__graph.get_zone_by_id(p).name)
