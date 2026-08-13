from fly_in import MapSelector, Parser, Map, Zone, ZoneMetadata, Connection

def test_shared_memory() -> None:
    path = "src/fly_in/maps/easy/03_basic_capacity.txt"
    parser = Parser(path=path)

    fmap: Map = parser.get_map()

    assert fmap.connections[0].zone_a is fmap.start_hub
    assert fmap.connections[2].zone_b is fmap.end_hub
