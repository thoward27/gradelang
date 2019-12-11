""" gradelang Tree Walker.
"""

from grade.pipeline import *

#from .types import Program

from .state import state
    
def assign(ast):
    dict = {}
    if ast[1] == 'String':
        dict = {ast[2]: str(ast[2])}
    elif ast[1] == 'Int':
        dict = {ast[2]: int(ast[2])}
    elif ast[1] == "Float":
        dict = {ast[2]: float(ast[2])}
        
    state.symbol_table.update(dict)

def walkParamList(ast, flat_list=[]):
    
    flat_list.append(ast[1])
    if ast[2][0] == "paramlist":

       walkParamList(ast[2], flat_list)
    else:

       flat_list.append(ast[2])
       return flat_list;    
    
def run(ast):

    if ast[1][0] != "paramlist":
        state.update_results(Run(str(walk(ast[1])), shell=True)())
        
    else:
        walkable_params = walkParamList(ast[1], [])
      
        params = []
        for node in walkable_params:
            params.append(str(walk(node)))
        #print("run parameters", params)
        state.update_results(Run(params, shell=True)())       
    
dispatch = {
    # (SEQ, stmt, stmt_list)
    'seq': lambda ast: (walk(ast[1]), walk(ast[2])),

    # (NIL, )
    'nil': lambda ast: '',

    # (ASSERT, exp)
    'assert': lambda ast: walk(ast[1]),

    # (RUN, STRING)
    'run': run,#lambda ast: state.update_results(Run(ast[1], shell=True)()),

    # (EXIT, code)
    'exit': lambda ast: (AssertExitSuccess() if ast[1] == 'successful' else AssertExitFailure())(state.results),

    # (IN, exp, stream)
    'in': lambda ast: (AssertRegexStdout if ast[2] == 'stdout' else AssertRegexStderr)(pattern=walk(ast[1]))(state.results),
    
    #("not in", exp, stream)
    #^((?!badword).)*$
    'not in': lambda ast: (AssertRegexStdout if ast[2] == 'stdout' else AssertRegexStderr)(pattern="^((?!" + str(walk(ast[1])) + ").)*$")(state.results),


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
    
    #('award', INTEGER)
    'award': lambda ast: state.updateAward(int(ast[1])),    
}


def walk(ast) -> str:
    action = ast[0]
    if action in dispatch:
        return dispatch[action](ast)
    raise ValueError(f"Unknown node: {ast}")
    

