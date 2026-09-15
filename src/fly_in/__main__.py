"""Command-line entry point for the Fly-in application."""

from .core import Simulation


def main() -> None:
    """Run the simulation, handling interrupts and unexpected errors."""
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
