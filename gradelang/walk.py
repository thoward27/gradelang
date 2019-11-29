""" gradelang Tree Walker.
"""

from .state import state


def _question(ast):
    # (QUESTION, worth, stmt_list)
    try:
        walk(ast[2])
    except Exception as err:
        print(err)
    return


dispatch = {
    # (SEQ, stmt, stmt_list)
    'seq': lambda ast: (walk(ast[1]), walk(ast[2])),

    # (NIL, )
    'nil': lambda ast: '',

    # (SETUP, stmt_list)
    'setup': lambda ast: walk(ast[1]),

    # (TEARDOWN, stmt_list)
    'teardown': lambda ast: walk(ast[1]),

    # (SAVE, stmt_list)
    'save': lambda ast: walk(ast[1]),

    # (QUESTION, worth, stmt_list)
    'question': _question,

    # (ASSERT, exp)
    'assert': lambda ast: walk(ast[1]),

    # (ASSIGN, type, id, exp)
    'assign': lambda ast: state.symbol_table.update({ast[2]: state.symbol_table[ast[2]](walk(ast[3]))}),

    # (INT, value)
    'integer': lambda ast: int(ast[1]),
    'string': lambda ast: ast[1],

    # (ID, )
    'id': lambda ast: state.symbol_table[ast[1]],

    # (UMINUS, exp)
    'uminus': lambda ast: -int(walk(ast[1])),

    # (NOT, exp)
    '!': lambda ast: int(not walk(ast[1])),

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
}


def walk(ast) -> str:
    action = ast[0]
    if action in dispatch:
        return dispatch[action](ast)
    raise ValueError(f"Unknown node: {ast}")
