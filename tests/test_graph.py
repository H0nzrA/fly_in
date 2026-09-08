from fly_in import Graph, Map, Parser, Zone
from pathlib import Path


def test_graph() -> None:
    path: str = "src/fly_in/resources/maps/mandatory/hard/03_ultimate_challenge.txt"
    parser: Parser = Parser(path=Path(path))
    map: Map = parser.get_map()
    graph: Graph = Graph(map=map)

    assert graph.start_node() == map.start_hub.id
    assert graph.end_node() == map.end_hub.id

    start_zone = graph.start_node()

    start_neighbor: list[Zone] = [
        graph.get_zone_by_id(1),
        graph.get_zone_by_id(2),
        graph.get_zone_by_id(3),
    ]

    assert graph.get_zone_by_id(0) == map.start_hub
    assert graph.get_zone_by_id(30) == map.end_hub
