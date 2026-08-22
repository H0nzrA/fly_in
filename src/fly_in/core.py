from .cli.map_selector import MapSelector
from .parser import Parser
from .domain import Map, Zone, Connection
from .graph import Graph
from .solver import SpaceTimeAStar


class Program:
    def run(self) -> None:
        selector: MapSelector = MapSelector()
        parser: Parser = Parser(path=selector.get_map_path())
        map: Map = parser.get_map()

        graph: Graph = Graph(map=map)
        stas: SpaceTimeAStar = SpaceTimeAStar(graph)
        del stas

    def __print_zone(self, zone: Zone) -> None:
        res: str = ""

        res += zone.name + f" {zone.id} : "
        res += str(zone.coordinate) + " "
        res += zone.metadata.zone + " "
        res += str(zone.metadata.color) + " "
        res += str(zone.metadata.max_drones) + " "

        print(res)

    def __print_connection(
        self,
        connection: Connection
    ) -> None:
        res: str = ""

        res += connection.zone_a.name + " - "
        res += connection.zone_b.name
        res += f" [{connection.metadata.max_link_capacity}]"

        print(res)
