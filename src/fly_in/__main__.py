from .core import Program


def main() -> None:
    try:
        program: Program = Program()
        program.run()

    except (KeyboardInterrupt, EOFError):
        print("\n=== Program Stopped ===\n")

    # except Exception as e:
    #     print(e)
    #     print("\n=== Program Stopped ===\n")


if __name__ == "__main__":
    main()
