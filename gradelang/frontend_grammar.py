""" gradelang Frontend Grammar
# TODO Pull lexer tokens in?
"""
from .lexer import *
from .state import state
from .types import DICT as TYPE_DICT

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
def p_prog(p):
    """
    prog : block_list
    """
    state.AST = p[1]


def p_block_list(p):
    """
    block_list : block block_list
               | empty
    """
    if len(p) == 3:
        p[0] = ('blocks', p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]
    return


def p_block(p):
    """
    block : block_generic '{' stmt_list '}'
          | OUTPUT '{' format_list '}'
    """
    if p[1] == 'setup':
        state.setup = p[3]

    elif p[1] == 'question':
        state.questions.append(p[3])

    elif p[1] == 'teardown':
        state.teardown = p[3]

    elif p[1] == 'output':
        state.save = p[3]

    else:
        raise ValueError(f'Unexpected block: {p[1]}')
    return


def p_format_list(p):
    """
    format_list : output_format ';' format_list
               | empty
    """
    if len(p) == 3:
        p[0] = ('formats', p[1], p[3])
    elif len(p) == 2:
        p[0] = p[1]
    return


def p_output_format(p):
    """
    output_format : JSON
                  | MARKDOWN
    """
    p[0] = p[1]
    return


def p_block_generic(p):
    """
    block_generic : SETUP
                  | QUESTION
                  | TEARDOWN
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
    stmt : FOR ID IN type
         | type ID '=' exp
         | builtin exp
         | AWARD INTEGER
    """
    # TODO: Check strings before eval.
    if p[1] == 'for':
        p[0] = ('for', p[2], eval(p[4]))

    elif p[1] == 'award':
        p[0] = ('award', p[2])

    elif p[1] in types.keys():
        state.symbol_table[p[2]] = TYPE_DICT[p[1]]
        p[0] = ('assign', p[1], p[2], p[4])

    elif p[1] in builtins.keys():
        p[0] = (p[1], p[2])

    else:
        raise ValueError(f"Unexpected symbol {p[1]}")
    return


def p_type(p):
    """
    type : STRING_TYPE
         | PROGRAM_TYPE
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


def p_integer_exp(p):
    """
    exp : INTEGER
    """
    p[0] = ('integer', int(p[1]))
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
    p[0] = ('!', p[2])


def p_empty(p):
    """
    empty :
    """
    p[0] = ('nil',)


def p_error(t):
    raise SyntaxError(str(t))
