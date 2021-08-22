"""Console script for pidj."""
import sys

import click

import pidj.pidj as pi_dj


@click.command()
def main():
    """Console script for pidj."""
    pi_dj.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
