""" gradelang Interpreter.
"""
import io
from contextlib import redirect_stdout
from multiprocessing.pool import Pool

from gradelang.question import Question
from . import lexer, parser
from .state import state
from .walk import walk


def interpret(stream):
    # clean the state object between runs
    state.clean()

    # build the AST
    parser.parse(stream, lexer=lexer)

    with Pool() as p:
        state._questions = p.map(run, state.questions)
    # TODO: OUTPUT
    [print(q) for q in state.questions]
    return


def run(question: Question):
    try:
        if state.setup:
            walk(state.setup)

        state.question = question
        output = io.StringIO()
        with redirect_stdout(output):
            walk(question.body)
        question.output = output.getvalue()

        if state.teardown:
            walk(state.teardown)
    except Exception as err:
        question.exception = err
    finally:
        return question
