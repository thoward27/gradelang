""" gradelang Tree Walker.
"""

from sys import exit

from .state import state


def _for(ast):
    # (FOR, id, exp, exp, opt_step, stmt_list, id)
    for x in range(int(walk(ast[2])), int(walk(ast[3])) + 1, int(walk(ast[4])) if ast[4] != ('nil',) else 1):
        state.symbol_table.update({ast[1]: x})
        walk(ast[5])


def _while(ast):
    # (WHILE, exp, stmt_list)
    while walk(ast[1]):
        walk(ast[2])


dispatch = {
    # (SEQ, stmt, stmt_list)
    'seq': lambda ast: (walk(ast[1]), walk(ast[2])),

    # (NIL, )
    'nil': lambda ast: '',

    # (SETUP, stmt_list)
    'setup': lambda ast: walk(ast[1]),

    # (TEARDOWN, stmt_list)
    'teardown': lambda ast: walk(ast[1]),

    # (ASSIGN, id, exp)
    'assign': lambda ast: state.symbol_table.update({ast[1]: walk(ast[2])}),

    # (INPUT, opt_string, id)
    'input': lambda ast: state.symbol_table.update({ast[2]: int(input(ast[1]))}),

    # (PRINT, value, value_list)
    'print': lambda ast: print(walk(ast[1]), *(walk(n) for n in ast[2]) if ast[2] != ('nil',) else '', sep=''),

    # (END, )
    'end': lambda ast: exit(0),

    # (WHILE, exp, stmt_list)
    'while': _while,

    # (FOR, id, exp, exp, opt_step, stmt_list, id)
    'for': _for,

    # (IF, exp, stmt_list, opt_else)
    'if': lambda ast: walk(ast[2]) if walk(ast[1]) else walk(ast[3]),

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


def walk(ast, level=None) -> str:
    action = ast[0]

    if action in dispatch:
        return dispatch[action](ast)
    raise ValueError(f"Unknown node: {ast}")
