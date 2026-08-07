from .map_selector import MapSelector
from .parser import Parser
from ..models import Map, Zone


class Program:
    def run(self) -> None:
        selector: MapSelector = MapSelector()
        parser: Parser = Parser(path=selector.get_map_path())
        maps: Map = parser.get_map()

        self.__print_zone(maps.start_hub)

        for hub in maps.hubs:
            self.__print_zone(hub)

        self.__print_zone(maps.end_hub)

    def __print_zone(self, zone: Zone) -> None:
        res: str = ""

        res += zone.name + ": "
        res += str(zone.coordinate) + " "
        res += zone.metadata.zone + " "
        res += str(zone.metadata.color) + " "
        res += str(zone.metadata.max_drones) + " "

        print(res)


def main() -> None:
    try:
        program: Program = Program()
        program.run()

    except (KeyboardInterrupt, EOFError):
        print("\n=== Program Stopped ===\n")

    except Exception as e:
        print(e)
