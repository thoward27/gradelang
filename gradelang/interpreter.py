""" gradelang Interpreter.
"""
import io
import traceback
from contextlib import redirect_stdout
from functools import partial
from multiprocessing.pool import Pool

from gradelang.question import Question
from . import lexer, parser
from .state import state
from .walk import walk


def interpret(stream) -> None:
    """ Interprets the given stream. """
    # reset the state object
    state.clean()

    # build the AST
    parser.parse(stream, lexer=lexer)

    # Execute Questions.
    _worker = partial(worker, setup=state.setup, teardown=state.teardown)
    with Pool() as p:
        state._questions = p.map(_worker, state.questions)

    # Generate Output.
    if not state.output:
        print(state.report())
    elif 'json' in state.output:
        print(state.json())
    elif 'markdown' in state.output:
        print(state.markdown())
    return


def worker(question: Question, setup: tuple, teardown: tuple) -> Question:
    """ Worker Process for questions.

    Passing setup and teardown explicitly because Windows uses `spawn` instead
    of `fork`, which means we lose the global state on Win. In either case,
    state is not returned from neither spawn or fork, so any changes made
    within this function cannot impact the caller.
    """
    state.question = question
    output = io.StringIO()
    with redirect_stdout(output):
        try:
            if setup:
                walk(setup)

            walk(question.body)

            if teardown:
                walk(teardown)
        except Exception as err:
            question.exception = repr(err)
            question.traceback = traceback.format_exc()
        finally:
            question.output = output.getvalue()
            return question
