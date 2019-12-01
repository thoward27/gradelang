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
            if state.setup:
                walk(state.setup)

            walk(question.body)

            if state.teardown:
                walk(state.teardown)
        except Exception as err:
            raise
            print("Exception Raised!" + err)
        finally:
            if state.output:
                walk(state.output)
