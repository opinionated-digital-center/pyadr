import sys

from pyadr.cli.config import LoggingAppConfig
from pyadr.git.cli.application import App


def main(args=None):
    return App(config=LoggingAppConfig()).run()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
