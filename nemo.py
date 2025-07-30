import sys

from src.interface import Interface


def main():
    """Entrypoint"""
    try:
        interface = Interface()
        interface.execute()
    except KeyboardInterrupt:
        print("\n\nInterrupted by the user")
        sys.exit(1)
    except Exception as exception:
        print(f"Error: {exception}")
        sys.exit(1)


if __name__ == "__main__":
    main()
