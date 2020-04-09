import sys

from .application import App, LoggingAppConfig


def main(args=None):
    return App(config=LoggingAppConfig()).run()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
