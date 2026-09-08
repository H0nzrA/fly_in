from fly_in import MapSelector, Parser, Map, Zone, ZoneMetadata, Connection

def test_path1() -> None:
    path = "src/fly_in/resources/maps/mandatory/hard/03_ultimate_challenge.txt"
    parser = Parser(path=path)

    fmap: Map = parser.get_map()

def test_path2() -> None:
    path = "src/fly_in/resources/maps/mandatory/easy/03_basic_capacity.txt"
    parser = Parser(path=path)

    fmap: Map = parser.get_map()

    assert fmap.nb_drones == 4
    start = Zone(
        id=0,
        prefix="start_hub",
        name="start",
        coordinate=(0, 0),
        metadata=ZoneMetadata(
            color="green",
            max_drones=4
        )
    )
    bt = Zone(
        id=1,
        prefix="hub",
        name="bottleneck",
        coordinate=(1, 0),
        metadata=ZoneMetadata(
            color="orange",
            max_drones=2
        )
    )
    assert fmap.start_hub == start
    assert fmap.connections[0] == Connection(
        zone_a=start,
        zone_b=bt
    )
