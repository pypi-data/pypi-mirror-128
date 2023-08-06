"""Entrypoint."""

import sys

from . import render


def main() -> None:
    """Entrypoint."""
    sys.stdout.buffer.write(render(sys.stdin.read()))


if __name__ == "__main__":
    main()
