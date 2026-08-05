from fly_in import MapSelector, Parser, Map, Zone, ZoneMetadata, Connection

def test_shared_memory() -> None:
    path = "src/fly_in/maps/easy/03_basic_capacity.txt"
    parser = Parser(path=path)

    fmap: Map = parser.get_map()

    assert fmap.connections[0].source is fmap.start_hub
    assert fmap.connections[2].destination is fmap.end_hub
