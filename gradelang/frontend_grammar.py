""" gradelang Frontend Grammar
# TODO Pull lexer tokens in?
"""
from .lexer import *
from .state import state

# from .types import DICT as TYPE_DICT

#########################################################################
# set precedence and associativity
# NOTE: all operators need to have tokens
#       so that we can put them into the precedence table
precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQ', 'LE', 'LT', 'GE', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS', 'NOT')
)


#########################################################################
# grammar rules with embedded actions
#########################################################################
def p_prog(_):
    """
    prog : block_list
    """
    return


def p_block_list(_):
    """
    block_list : block block_list
               | empty
    """
    return


def p_block(p):
    """
    block : SETUP '{' stmt_list '}'
          | QUESTION opt_name '{' stmt_list '}'
          | TEARDOWN '{' stmt_list '}'
          | OUTPUT '{' format_list '}'
    """
    if p[1] == 'setup':
        state.setup = p[3]

    elif p[1] == 'question':
        # print("Question parsed:", p[2])
        state.add_question(
            name=p[2],
            body=p[4]
        )

    elif p[1] == 'teardown':
        state.teardown = p[3]

    elif p[1] == 'output':
        state.output = p[3]

    else:
        raise ValueError(f'Unexpected block: {p[1]}')
    return


def p_opt_name(p):
    """
    opt_name : INTEGER
         | STRING
         | empty
    """
    p[0] = p[1]
    return


def p_format_list(p):
    """
    format_list : output_format ';' format_list
               | empty
    """
    if len(p) >= 3:
        # If we have at least one format, filter out the empty tag.
        p[0] = {**p[1], **{fmt: file for fmt, file in p[3].items() if fmt != ('nil',)}}
    elif len(p) == 2:
        p[0] = {p[1]: ''}
    return


def p_output_format(p):
    """
    output_format : JSON opt_string
                  | MARKDOWN opt_string
    """
    p[0] = {p[1]: p[2]}
    return


def p_opt_string(p):
    """
    opt_string : STRING
               | empty
    """
    p[0] = p[1]
    return


def p_stmt_list(p):
    """
    stmt_list : stmt ';' stmt_list
              | empty
    """
    if len(p) == 4:
        p[0] = ('seq', p[1], p[3])

    elif len(p) == 2:
        p[0] = p[1]
    return


def p_stmt(p):
    """
    stmt : LET ID BE type opt_param_list
         | String ID '=' STRING
         | Int ID '=' INTEGER
         | Float ID '=' FLOAT
         | builtin exp
         | AWARD INTEGER
         | RUN param_list
         | REQUIRE STRING string_list
         | TOUCH STRING
         | REMOVE STRING
    """
    if p[1] == 'let':
        p[0] = ('let', p[2], p[4], p[5])

    elif p[1] == 'award':
        p[0] = ('award', p[2])

    elif p[1] == 'require':
        p[0] = ('require', p[2], p[3])

    # elif p[1] in types.keys():
    #    #print(TYPE_DICT)
    #    dict = TYPE_DICT[p[1]]
    #    state.symbol_table[p[2]] = dict
    #    p[0] = ('assign', p[1], p[2], p[4])

    elif p[1] in builtins.keys():
        p[0] = (p[1], p[2])

    elif p[1] == 'run':
        p[0] = ('run', p[2])

    elif p[1] == 'touch':
        p[0] = ('touch', p[2])

    elif p[1] == 'remove':
        p[0] = ('remove', p[2])

    elif p[3] == '=':
        if p[1] == 'String' or p[1] == 'Int' or 'Float':
            p[0] = ('assign', p[1], p[2], p[4])
        # elif p[1] in types.keys():
        #    dict = TYPE_DICT[p[1]]
        #    state.symbol_table[p[2]] = dict
        #    p[0] = ('assign', p[1], p[2], p[4])
    else:
        raise ValueError(f"Unexpected symbol {p[1]}")
    return


def p_string_list(p):
    """
    string_list : ',' STRING string_list
                | empty
    """
    if len(p) == 4:
        p[0] = (p[2], *p[3])
    else:
        p[0] = (p[1],)
    return


def p_opt_param_list(p):
    """
    opt_param_list : '(' param_list ')'
                   | '(' ')'
    """
    if len(p) > 3:
        p[0] = p[2]


def p_param_list(p):
    """
    param_list : param ',' param_list
               | param
    """
    # print("parsing paramlist", len(p), p)
    if len(p) == 4:
        p[0] = ("paramlist", p[1], p[3])
    else:
        p[0] = p[1]


def p_param(p):
    """
    param : exp
          | param_assign

    """
    p[0] = p[1]


def p_param_assign(p):
    """
    param_assign : ID '=' exp
    """
    p[0] = ("paramassign", p[1], p[3])


def p_type(p):
    """
    type : String
         | Int
         | Float
    """
    p[0] = p[1]
    return


def p_builtin(p):
    """
    builtin : ASSERT
            | ASSUME
            | PRINT
    """
    p[0] = p[1]
    return


def p_binop_exp(p):
    """
    exp : exp PLUS exp
        | exp MINUS exp
        | exp TIMES exp
        | exp DIVIDE exp
        | exp EQ exp
        | exp LE exp
        | exp LT exp
        | exp GE exp
        | exp GT exp
        | exp AND exp
        | exp OR exp
    """
    p[0] = (p[2], p[1], p[3])
    return


def p_bool_exp(p):
    """
    exp : EXIT SUCCESSFUL
        | EXIT FAILURE
        | exp IN STDOUT
        | exp IN STDERR
        | exp NOT IN STDOUT
        | exp NOT IN STDERR
        
    """
    # TODO: Should this be called exited?
    if p[1] == 'exit':
        p[0] = ('exit', p[2])
    elif p[2] == 'in':
        p[0] = ('in', p[1], p[3])
    elif p[3] == 'in':
        p[0] = ('notin', p[1], p[3])
    return


def p_integer_exp(p):
    """
    exp : INTEGER
    """
    p[0] = ('integer', int(p[1]))
    return


def p_float_exp(p):
    """
    exp : FLOAT
    """
    p[0] = ('float', float(p[1]))
    return


def p_id_exp(p):
    """
    exp : ID
    """
    p[0] = ('id', p[1])
    return


def p_string_exp(p):
    """
    exp : STRING
    """
    p[0] = ('string', p[1])
    return


def p_paren_exp(p):
    """
    exp : '(' exp ')'
    """
    p[0] = ('paren', p[2])
    return


def p_uminus_exp(p):
    """
    exp : MINUS exp %prec UMINUS
    """
    p[0] = ('uminus', p[2])


def p_not_exp(p):
    """
    exp : NOT exp
    """
    p[0] = ('not', p[2])


def p_empty(p):
    """
    empty :
    """
    p[0] = ('nil',)


def p_error(t):
    raise SyntaxError(str(t))
