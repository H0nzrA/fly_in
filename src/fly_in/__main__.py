from .cli import MapSelector, Parser


class Program:
    def run(self) -> None:
        selector: MapSelector = MapSelector()
        parser: Parser = Parser(path=selector.get_map_path())
        _ = parser.get_map()


def main() -> None:
    try:
        program: Program = Program()
        program.run()

    except (KeyboardInterrupt, EOFError):
        print("\n=== Program Stopped ===\n")

    except Exception as e:
        print(f"Caught Error: {e}\n")


if __name__ == "__main__":
    main()
