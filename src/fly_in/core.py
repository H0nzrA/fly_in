from .cli import MapSelector
from .parser import Parser
from pathlib import Path
from .domain import Map
from .graph import Graph


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
