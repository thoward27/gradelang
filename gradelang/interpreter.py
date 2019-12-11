""" gradelang Interpreter.
"""

from . import lexer, parser
from .state import state
from .walk import walk


def interpret(stream):
    # clean the state object between runs
    state.clean()

    # build the AST
    parser.parse(stream, lexer=lexer)

    for question in state.questions:
        try:
            if state.setup:
                walk(state.setup)

            walk(question.body)

            if state.teardown:
                walk(state.teardown)
            #state.reset()
        except Exception as err:
            raise
        finally:
            # TODO: Migrate results away from global state.
            state.results = None
