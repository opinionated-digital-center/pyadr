import sys

from pyadr.cli.application import App


def main(args=None):
    return App().run()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
