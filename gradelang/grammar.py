""" gradelang Grammar.
"""

from ply import yacc

# set precedence and associativity
precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQ', 'LE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS', 'NOT')
)


def p_grammar(_):
    """
    prog : stmt_list
    
    stmt_list : stmt stmt_list
              | empty

    stmt : SETUP '{' stmt_list '}'
         | TEARDOWN '{' stmt_list '}'
         | SAVE '{' stmt_list '}'
         | QUESTION WORTH INTEGER '{' stmt_list '}'
         | ASSERT exp ';'
         | TYPE ID '=' exp ';'
         | LET ID BE A type ';'
         | ASSUME exp ';'

    type : STRING_TYPE
         | PROGRAM_TYPE

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
        | INTEGER
        | ID
        | STRING
        | '(' exp ')'
        | MINUS exp %prec UMINUS
        | NOT exp
    """
    pass


def p_empty(_):
    """empty :"""
    pass


def p_error(t):
    raise SyntaxError(f"Syntax error at '{t.value}'")


# build the parser
parser = yacc.yacc()
