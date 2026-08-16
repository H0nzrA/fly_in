from fly_in import Graph, Map, Parser, Zone
from pathlib import Path


def test_graph() -> None:
    path: str = "src/fly_in/cli/maps/hard/03_ultimate_challenge.txt"
    parser: Parser = Parser(path=Path(path))
    map: Map = parser.get_map()
    graph: Graph = Graph(map=map)

    assert graph.start_zone() is map.start_hub
    assert graph.end_zone() is map.end_hub

    start_zone = graph.start_zone()

    start_neighbor: list[Zone] = [
        graph.get_zone(1),
        graph.get_zone(2),
        graph.get_zone(3),
    ]

    assert graph.get_zone(0) == map.start_hub
    assert graph.get_zone(30) == map.end_hub
    assert graph.neighbors(start_zone) == set(start_neighbor)
