""" CLI for Gradelang.
"""
import click

from .interpreter import interpret


@click.command()
@click.argument('file', type=click.File('r'))
def cli(file) -> None:
    """ Main entry-point.

    Expects one positional argument, a .grade file.
    """
    stream = file.read()
    interpret(stream)
    return


if __name__ == "__main__":
    cli()
