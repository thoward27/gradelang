""" gradelang Tree Walker.
"""

from grade.pipeline import *
from hypothesis.strategies import characters, floats, integers

# from .types import Program

from .state import state


# from .types import Program

def assign(ast):
    dict = {}
    if ast[1] == 'String':
        dict = {ast[2]: str(ast[3])}
    elif ast[1] == 'Int':
        dict = {ast[2]: int(ast[3])}
    elif ast[1] == "Float":
        dict = {ast[2]: float(ast[3])}

    state.symbol_table.update(dict)


def walkParamList(ast, flat_list=[]):
    flat_list.append(ast[1])
    if ast[2][0] == "paramlist":

        walkParamList(ast[2], flat_list)
    else:

        flat_list.append(ast[2])
        return flat_list


def getWalkedParamsAsListOfStrings(ast):
    walkable_params = walkParamList(ast, [])

    params = []
    for node in walkable_params:
        params.append(str(walk(node)))

    return params


def run(ast):
    if ast[1][0] != "paramlist":
        state.question.results = Run(str(walk(ast[1])), shell=True)()
        # state.update_results(Run(str(walk(ast[1])), shell=True)())
    else:
        params = getWalkedParamsAsListOfStrings(ast[1])

        print("run params: ", params)
        state.question.results = Run(params)()
        # state.update_results(Run(params, shell=True)())


def let(ast):
    # ('let', ID, type, opt_param_list)
    params = ""
    if ast[3]:
        if ast[3][1] != "paramlist":
            params = str(walk(ast[3]))
        else:
            params = getWalkedParamsAsListOfStrings(ast[3])

    if ast[2] == 'String':
        if params != "":
            new_string = characters(params)
        else:
            new_string = characters()
        print("string", new_string)
        dict = {ast[1]: "This is a random string, trust me"}
    elif ast[2] == 'Int':
        if params != "":
            new_int = integers(params)
        else:
            new_int = integers()
        print("int", new_int)
        dict = {ast[1]: 7}
    if ast[2] == "Float":
        if params != "":
            new_float = floats(params)
        else:
            new_float = floats()
        print("float", new_float)
        dict = {ast[1]: 7.0}

    print("dict", dict)
    state.symbol_table.update(dict)


def _assert(ast):
    result = walk(ast)
    if not result:
        raise AssertionError
    return result


dispatch = {
    # (SEQ, stmt, stmt_list)
    'seq': lambda ast: (walk(ast[1]), walk(ast[2])),

    # (NIL, )
    'nil': lambda ast: '',

    # (ASSERT, exp)
    'assert': lambda ast: _assert(ast[1]),

    # (TOUCH, STRING)
    'touch': lambda ast: (open(ast[1], "w+")),

    # (RUN, STRING)
    'run': run,  # lambda ast: state.update_results(Run(ast[1], shell=True)()),

    # (EXIT, code)
    'exit': lambda ast: (AssertExitSuccess() if ast[1] == 'successful' else AssertExitFailure())(
        state.question.results),

    # (IN, exp, stream)
    'in': lambda ast: (AssertRegexStdout if ast[2] == 'stdout' else AssertRegexStderr)(pattern=str(walk(ast[1])))(
        state.question.results),

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
