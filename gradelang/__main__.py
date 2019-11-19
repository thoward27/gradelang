""" CLI for gradelang.
"""
import click

from .interpreter import interpret


@click.command()
@click.argument('stream')
@click.option('--cmd/--no-cmd', default=False, help='Stream is a command, not a file.')
def cli(stream, cmd):
    if not cmd:
        with open(stream, 'r') as f:
            stream = f.read()

    interpret(stream)
    return


if __name__ == "__main__":
    cli()
