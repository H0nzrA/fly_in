"""Command-line argument parsing."""

from argparse import ArgumentParser, Namespace


def argument_parser() -> Namespace:
    """Parse command-line arguments for the application.

    Returns:
        Namespace: Parsed --input, --output, --benchmark, and --visual
            arguments.
    """
    args: ArgumentParser = ArgumentParser()

    args.add_argument(
        "--input",
        "-i",
        default=None
    )
    args.add_argument(
        "--output",
        "-o",
        default="./logs/simulation.log"
    )
    args.add_argument(
        "--benchmark",
        "-b",
        default="./logs/benchmark.log"
    )
    args.add_argument(
        "--visual",
        "-v",
        action="store_true"
    )

    return args.parse_args()
