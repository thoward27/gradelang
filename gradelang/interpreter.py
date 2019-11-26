""" gradelang Interpreter.
"""

from . import lexer, parser
from .state import state
from .walk import walk


def interpret(stream):
    # reset the state object
    state.reset()

    # build the AST
    parser.parse(stream, lexer=lexer)

    # walk the AST
    try:
        walk(state.AST)
    except SystemExit:
        pass
