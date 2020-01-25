""" Tree Walker.
"""
import os
import warnings
from pathlib import Path

from grade.pipeline import *
from hypothesis.strategies import characters, floats, integers

from .fns import *
from .state import state, NIL


def assign(ast):
    elem = {}
    if ast[1] == 'String':
        elem = {ast[2]: str(ast[3])}
    elif ast[1] == 'Int':
        elem = {ast[2]: int(ast[3])}
    elif ast[1] == "Float":
        elem = {ast[2]: float(ast[3])}

    state.symbol_table.update(elem)


def __assert(cond: any, message: str = None):
    if not cond:
        raise AssertionError(f'{cond} was not true! {message}')
    return


def __thread_path(p):
    return str(p).replace('@/', state.question.workdir.name)


dispatch = {
    # (ASSERT, exp)
    'assert': lambda ast: __assert(walk(ast[1]), ast[1]),

    # (ASSIGN, type, id, exp)
    'assign': assign,

    # (AWARD, INTEGER)
    'award': lambda ast: state.question.award(int(ast[1])),

    # (COMPARATOR, exp, exp)
    '==': lambda ast: int(walk(ast[1])) == int(walk(ast[2])),
    '<=': lambda ast: int(walk(ast[1])) <= int(walk(ast[2])),
    '<': lambda ast: int(walk(ast[1])) <= int(walk(ast[2])),
    '>=': lambda ast: int(walk(ast[1])) <= int(walk(ast[2])),
    '>': lambda ast: int(walk(ast[1])) > int(walk(ast[2])),

    # (EXIT, code)
    'exit': lambda ast: (
        AssertExitSuccess if ast[1] == 'successful' else AssertExitFailure
    )()(state.question.results),

    # (ID, value)
    'id': lambda ast: state.symbol_table[ast[1]],

    # (IN, exp, stream)
    'in': lambda ast: (
        AssertStdoutContains if ast[2] == 'stdout' else AssertStderrContains
    )(strings=[str(walk(ast[1]))])(state.question.results),

    # (LOGICAL, exp)
    'not': lambda ast: int(not walk(ast[1])),
    'and': lambda ast: int(bool(walk(ast[1])) and bool(walk(ast[2]))),
    'or': lambda ast: int(bool(walk(ast[1])) or bool(walk(ast[2]))),

    # (NIL, )
    'nil': lambda ast: '',

    # (NOT IN, exp, stream)
    # ^((?!badword).)*$
    'notin': lambda ast: Not(
        (AssertStderrContains if ast[2] == 'stdout' else AssertStderrContains)(strings=[ast[1]])
    )(state.question.results),

    # (OPERATOR, exp, exp)
    '+': lambda ast: int(walk(ast[1])) + int(walk(ast[2])),
    '-': lambda ast: int(walk(ast[1])) - int(walk(ast[2])),
    '*': lambda ast: int(walk(ast[1])) * int(walk(ast[2])),
    '/': lambda ast: int(walk(ast[1])) / int(walk(ast[2])),

    # (PARAM ASSIGN, ID, exp)
    'paramassign': lambda ast: walk(ast[2]),

    # (PAREN, exp)
    'paren': lambda ast: walk(ast[1]),

    # (REMOVE, STRING)
    'remove': lambda ast: (os.remove(__thread_path(ast[1]))),

    # (REQUIRE, STRING, string_list)
    'require': lambda ast: [__assert(os.path.exists(p), f'{p} does not exist!')
                            for p in [ast[1], *ast[2]] if p != NIL],

    # (RUN, param_list)
    'run': lambda ast: state.question.update(
        results=Run(
            command=[__thread_path(walk(p)) for p in ast[1]] if len(ast[1]) > 1 else __thread_path(walk(ast[1][0])),
            shell=len(ast[1]) == 1
        )()
    ),

    # (SEQ, stmt, stmt_list)
    'seq': lambda ast: (walk(ast[1]), walk(ast[2])),

    # (TOUCH, STRING)
    'touch': lambda ast: Path(__thread_path(ast[1])).touch(),

    # (TYPE, value)
    'integer': lambda ast: int(ast[1]),
    'float': lambda ast: float(ast[1]),
    'string': lambda ast: ast[1],

    # (UMINUS, exp)
    'uminus': lambda ast: -int(walk(ast[1])),
}


def walk(ast) -> any:
    action = ast[0]
    if action in dispatch:
        return dispatch[action](ast)
    raise ValueError(f"Unknown node: {ast}")
