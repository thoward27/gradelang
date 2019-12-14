""" gradelang Tree Walker.
"""
import os
from pathlib import Path

from grade.pipeline import *
from hypothesis.strategies import characters, floats, integers

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


def walk_param_list(ast, flat_list=[]):
    flat_list.append(ast[1])
    if ast[2][0] == "paramlist":

        walk_param_list(ast[2], flat_list)
    else:

        flat_list.append(ast[2])
        return flat_list


def get_walked_params_as_list(ast):
    walkable_params = walk_param_list(ast, [])
    params = []
    for node in walkable_params:
        params.append(walk(node))

    return params


def run(ast):
    if ast[1][0] != "paramlist":
        state.question.results = Run(__safe_path(str(walk(ast[1]))), shell=True)()
    else:
        params = get_walked_params_as_list(ast[1])

        params = [__safe_path(str(i)) for i in params]

        state.question.results = Run(params)()


def let(ast):
    # ('let', ID, type, opt_param_list)
    params = ""
    if ast[3]:
        if ast[3][1] != "paramlist":
            params = walk(ast[3])
        else:
            params = get_walked_params_as_list(ast[3])

    if ast[2] == 'String':
        if params != "":
            new_string = characters(params)
        else:
            new_string = characters()
        dict = {ast[1]: new_string.example()}
    elif ast[2] == 'Int':
        if params != "":
            new_int = integers(params)
        else:
            new_int = integers()
        dict = {ast[1]: new_int.example()}
    elif ast[2] == "Float":
        if params != "":
            new_float = floats(params)
        else:
            new_float = floats()
        dict = {ast[1]: new_float.example()}

    state.symbol_table.update(dict)


def _assert(ast):
    result = walk(ast)
    if not result:
        raise AssertionError
    return result


def __assert(cond: bool, message: str = None):
    if not cond:
        raise AssertionError(message)
    return


def __safe_path(p: str):
    return p.replace('@/', state.question.workdir.name)


dispatch = {
    # (SEQ, stmt, stmt_list)
    'seq': lambda ast: (walk(ast[1]), walk(ast[2])),

    # (NIL, )
    'nil': lambda ast: '',

    # (ASSERT, exp)
    'assert': lambda ast: _assert(ast[1]),

    # (RUN, STRING)
    'run': run,  # lambda ast: state.update_results(Run(ast[1], shell=True)()),

    # (TOUCH, STRING)
    'touch': lambda ast: Path(__safe_path(ast[1])).touch(),

    # (REMOVE, STRING)
    'remove': lambda ast: (os.remove(__safe_path(ast[1]))),

    # (REQUIRE, STRING, string_list)
    'require': lambda ast: [__assert(os.path.exists(p), f'{p} does not exist!') for p in [ast[1], *ast[2]] if p != NIL],

    # (EXIT, code)
    'exit': lambda ast: (
        AssertExitSuccess() if ast[1] == 'successful' else AssertExitFailure())
    (state.question.results),

    # (IN, exp, stream)
    'in': lambda ast: (
        AssertStdoutContains if ast[2] == 'stdout' else AssertStderrContains
    )(strings=[str(walk(ast[1]))])(state.question.results),

    # ("not in", exp, stream)
    # ^((?!badword).)*$
    'notin': lambda ast: (AssertRegexStdout if ast[2] == 'stdout' else AssertRegexStderr)(
        pattern="^((?!" + str(walk(ast[1])) + ").)*$")(state.question.results),

    # (ASSIGN, type, id, exp)
    # 'assign': lambda ast: state.symbol_table.update({ast[2]: state.symbol_table[ast[2]](walk(ast[3]))}),
    'assign': assign,

    # (INT, value)
    'integer': lambda ast: int(ast[1]),

    # (STRING, value)
    'string': lambda ast: ast[1],

    # (PARAM_ASSIGN, ID, exp)
    'paramassign': lambda ast: walk(ast[2]),

    # (ID, value)
    'id': lambda ast: state.symbol_table[ast[1]],

    # (UMINUS, exp)
    'uminus': lambda ast: -int(walk(ast[1])),

    # (NOT, exp)
    'not': lambda ast: int(not walk(ast[1])),

    # (and, exp, exp)
    '&': lambda ast: int(bool(walk(ast[1])) and bool(walk(ast[2]))),

    # (OR, exp, exp)
    '|': lambda ast: int(bool(walk(ast[1])) or bool(walk(ast[2]))),

    # (PAREN, exp)
    'paren': lambda ast: walk(ast[1]),

    # (op, exp, exp)
    '+': lambda ast: int(walk(ast[1])) + int(walk(ast[2])),
    '-': lambda ast: int(walk(ast[1])) - int(walk(ast[2])),
    '*': lambda ast: int(walk(ast[1])) * int(walk(ast[2])),
    '/': lambda ast: int(walk(ast[1])) / int(walk(ast[2])),

    # (EQ, exp, exp)
    '==': lambda ast: int(walk(ast[1])) == int(walk(ast[2])),

    # (LEQ, exp, exp)
    '<=': lambda ast: int(walk(ast[1])) <= int(walk(ast[2])),

    # (LT, exp exp)
    '<': lambda ast: int(walk(ast[1])) <= int(walk(ast[2])),

    # (GEQ, exp, exp)
    '>=': lambda ast: int(walk(ast[1])) <= int(walk(ast[2])),

    # (GT, exp, exp)
    '>': lambda ast: int(walk(ast[1])) > int(walk(ast[2])),

    # ('award', INTEGER)
    'award': lambda ast: state.question.award(int(ast[1])),

    # ('let', ID, type, opt_param_list)
    'let': let,
}


def walk(ast) -> str:
    action = ast[0]
    if action in dispatch:
        return dispatch[action](ast)
    raise ValueError(f"Unknown node: {ast}")
