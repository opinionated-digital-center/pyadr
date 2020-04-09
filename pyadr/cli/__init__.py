import sys

from .application import Application


def main(args=None):
    return Application().run()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
