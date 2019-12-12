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


def interpret(stream):
    # reset the state object
    state.clean()

    # build the AST
    parser.parse(stream, lexer=lexer)

    with Pool() as p:
        state._questions = p.map(
            partial(worker, setup=state.setup, teardown=state.teardown), state.questions)
    if not state.output:
        [print(q.report()) for q in state.questions]
    elif 'json' in state.output:
        print(state.json)
    elif 'markdown' in state.output:
        print(state.markdown)
    return


def worker(question: Question, setup, teardown):
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
