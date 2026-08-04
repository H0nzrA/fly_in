from .cli import MapSelector


def main() -> None:
    try:
        maps: MapSelector = MapSelector()
        print(maps.get_map_path().read_text())

    except (KeyboardInterrupt, EOFError):
        print("\n=== Program Stopped ===\n")

    except Exception as e:
        print(f"Caught Error: {e}\n")


if __name__ == "__main__":
    main()
