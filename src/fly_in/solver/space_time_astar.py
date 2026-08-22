from ..graph import Graph
from .dijkstra import Dijkstra


class SpaceTimeAStar:
    def __init__(self, graph: Graph) -> None:
        self.__heuristic: dict[int, float] = Dijkstra().compute_distances(
            graph.end_node(),
            graph
        )

        for p in self.__heuristic:
            print(f"{graph.get_zone_by_id(p).name} - {self.__heuristic[p]}")
