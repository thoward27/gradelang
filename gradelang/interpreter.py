""" gradelang Interpreter.
"""

from .state import state
from .walk import walk
from . import lexer, parser


def interpret(stream):
    # initialize the state object
    state.initialize()

    # build the AST
    parser.parse(stream, lexer=lexer)

    # walk the AST
    try:
        walk(state.AST)
    except SystemExit:
        pass
