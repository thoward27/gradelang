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

    for question in state.questions:
        try:
            walk(state.setup)
            walk(question)
            walk(state.teardown)
        except Exception as err:
            print(err)
        finally:
            walk(state.save)
