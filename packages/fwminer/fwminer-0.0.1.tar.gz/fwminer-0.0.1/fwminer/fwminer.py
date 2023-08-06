import click
import sys

"""Main module."""


@click.command()
def main(args=None):
    """Console script for fwminer."""
    click.echo("fwminer: the miner with AI")
    return 0


if __name__ == "__main__":
    sys.exit(main())
