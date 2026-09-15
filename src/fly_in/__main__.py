from .core import Simulation


def main() -> None:
    try:
        simulation: Simulation = Simulation()
        simulation.run()

    except (KeyboardInterrupt, EOFError):
        print("\n=== Program Stopped ===\n")

    except Exception as e:
        print("Unexpected Error:", e)
        print("\n=== Program Stopped ===\n")


if __name__ == "__main__":
    main()
