from fly_in import Zone, ZoneMetadata, Connection, ConnectionMetadata


def test_zone() -> None:
    zone: Zone = Zone(
        prefix="start_hub",
        name="Hello",
        coordinate=(2, 3),
        metadata=ZoneMetadata(
            zone="normal",
            color="red",
            max_drones=4
        )
    )

    print(
        f"{zone.prefix}: {zone.name} {zone.coordinate} "
        f"[{zone.metadata.zone} {zone.metadata.color} "
        f"{zone.metadata.max_drones}]"
    )


def test_connection() -> None:
    zone1: Zone = Zone(
        prefix="start_hub",
        name="Hello",
        coordinate=(2, 3),
        metadata=ZoneMetadata(
            zone="normal",
            color="red",
            max_drones=4
        )
    )

    zone2: Zone = Zone(
        prefix="end_hub",
        name="Hello",
        coordinate=(2, 3),
        metadata=ZoneMetadata(
            zone="normal",
            color="red",
            max_drones=4
        )
    )

    conn: Connection = Connection(
        source=zone1,
        destination=zone2,
        metadata=ConnectionMetadata(
            max_link_capacity=5
        )
    )

    print(
        f"{conn.source.name} - {conn.destination.name} "
        f"[{conn.metadata.max_link_capacity}]"
    )
