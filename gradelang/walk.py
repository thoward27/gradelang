""" gradelang Tree Walker.
"""

from grade.pipeline import *

from .types import Program

from .state import state

def outputFile(ast):
    WriteOutput()
    
def assign(ast):
    dict = {}
    if ast[1] == 'string':
        dict = {ast[2]: str(ast[2])}
    elif ast[1] == 'int':
        dict = {ast[2]: int(ast[2])}
    elif isinstance(state.symbol_table[ast[2]], Program):
        
        dict = {ast[2]: Program(walk(ast[3]))}
    else:
        dict = {ast[2]: state.symbol_table[ast[2]](walk(ast[3]))}
        
    state.symbol_table.update(dict)
        
    
    
dispatch = {
    # (SEQ, stmt, stmt_list)
    'seq': lambda ast: (walk(ast[1]), walk(ast[2])),

    # (NIL, )
    'nil': lambda ast: '',

    # (ASSERT, exp)
    'assert': lambda ast: walk(ast[1]),

    # (RUN, STRING)
    'run': lambda ast: state.update_results(Run(ast[1], shell=True)()),

    # (EXIT, code)
    'exit': lambda ast: (AssertExitSuccess() if ast[1] == 'successful' else AssertExitFailure())(state.results),

    # (IN, exp, stream)
    'in': lambda ast: (AssertRegexStdout if ast[2] == 'stdout' else AssertRegexStderr)(pattern=walk(ast[1]))(state.results),

    # (ASSIGN, type, id, exp)
    #'assign': lambda ast: state.symbol_table.update({ast[2]: state.symbol_table[ast[2]](walk(ast[3]))}),
    'assign': assign,

    # (INT, value)
    'integer': lambda ast: int(ast[1]),

    # (STRING, value)
    'string': lambda ast: ast[1],

    # (ID, value)
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

    # (LT, exp exp)
    '<': lambda ast: int(walk(ast[1])) <= int(walk(ast[2])),

    # (GEQ, exp, exp)
    '>=': lambda ast: int(walk(ast[1])) <= int(walk(ast[2])),

    # (GT, exp, exp)
    '>': lambda ast: int(walk(ast[1])) > int(walk(ast[2])),
    
    #('award', INTEGER)
    'award': lambda ast: state.updateAward(int(ast[1])),
    
    'json': outputFile,
    
    'markdown': outputFile,
    
    
}


def walk(ast) -> str:
    action = ast[0]
    if action in dispatch:
        return dispatch[action](ast)
    raise ValueError(f"Unknown node: {ast}")
    

