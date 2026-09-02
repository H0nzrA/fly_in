from argparse import ArgumentParser, Namespace


def argument_parser() -> Namespace:
    args: ArgumentParser = ArgumentParser()

    args.add_argument(
        "--input",
        "-i",
        default=None
    )
    args.add_argument(
        "--output",
        "-o",
        default="./logs/output.log"
    )
    args.add_argument(
        "--benchmark",
        "-b",
        default="./logs/benchmark.log"
    )

    return args.parse_args()
