import sys


def main() -> None:
    print("Hello from fly-in")
    print(f"Sys lenght: {len(sys.argv)}")


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, EOFError):
        print("\n=== Program Stopped ===\n")

    except Exception as e:
        print(f"Caught Error: {e}\n")
