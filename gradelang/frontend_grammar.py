""" gradelang Frontend Grammar
"""
from gradelang.Program import Program
from .state import state

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
    prog : stmt_list
    """
    state.AST = p[1]


def p_stmt_list(p):
    """
    stmt_list : stmt stmt_list
              | empty
    """
    if len(p) == 3:
        p[0] = ('seq', p[1], p[2])

    elif len(p) == 2:
        p[0] = p[1]
    return


def p_type(p):
    """
    type : STRING_TYPE
         | PROGRAM_TYPE
    """
    p[0] = p[1]


def p_stmt(p):
    """
    stmt : SETUP '{' stmt_list '}'
         | TEARDOWN '{' stmt_list '}'
         | SAVE '{' stmt_list '}'
         | QUESTION WORTH INTEGER '{' stmt_list '}'
         | ASSERT exp ';'
         | type ID '=' exp ';'
         | LET ID BE A type ';'
         | ASSUME exp ';'
    """
    if p[1] == 'setup':
        state.setup = p[3]
        p[0] = ('setup', p[3])

    elif p[1] == 'teardown':
        state.teardown = p[3]
        p[0] = ('teardown', p[3])

    elif p[1] == 'save':
        p[0] = ('save', p[3])

    elif p[1] == 'question':
        # TODO: This should be appending an identifier.
        state.questions.append(p[5])
        p[0] = ('question', p[3], p[5])

    elif p[1] == 'assert':
        p[0] = ('assert', p[2])

    elif p[1] in {Program.__name__, 'String'}:
        state.symbol_table[p[2]] = eval(p[1])
        p[0] = ('assign', p[1], p[2], p[4])

    elif p[1] == 'let':
        p[0] = ('for', p[2], p[4], p[6], p[7], p[8], p[10])

    elif p[1] == 'assume':
        p[0] = ('assume', p[2])

    else:
        raise ValueError("unexpected symbol {}".format(p[1]))
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
