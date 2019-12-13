""" CLI for gradelang.
"""
import click

from .interpreter import interpret


@click.command()
@click.argument('file', type=click.File('r'))
def cli(file):
    stream = file.read()
    interpret(stream)
    return


if __name__ == "__main__":
    cli()
