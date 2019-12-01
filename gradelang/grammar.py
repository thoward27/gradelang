""" gradelang Grammar.
"""

from ply import yacc

# set precedence and associativity
precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQ', 'LE', 'LT', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS', 'NOT')
)


def p_grammar(_):
    """
    prog : block_list

    block_list : block block_list
               | empty

    block : block_type '{' stmt_list '}'

    block_type : SETUP
          | QUESTION name
          | TEARDOWN
          | SAVE

    name : STRING | INTEGER

    stmt_list : stmt ';' stmt_list
              | empty

    stmt : FOR ID IN type
         | type ID '=' exp
         | builtin exp
         | AWARD INTEGER

    type : STRING_TYPE
         | PROGRAM_TYPE

    builtin : ASSERT
            | ASSUME
            | PRINT

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
