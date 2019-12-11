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

    block : SETUP '{' stmt_list '}'
          | QUESTION name '{' stmt_list '}'
          | TEARDOWN '{' stmt_list '}'
          | OUTPUT '{' format_list '}'

    format_list : output_format ';' format_list
                | empty

    name : STRING | INTEGER

    output_format : JSON | MARKDOWN

    stmt_list : stmt ';' stmt_list
              | empty

    stmt : FOR ID IN type
         | type ID '=' exp
         | builtin exp
         | AWARD INTEGER
         | RUN STRING

    type : STRING_TYPE
         | PROGRAM_TYPE

    builtin : ASSERT
            | ASSUME
            | PRINT
            | TOUCH
            | REMOVE

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
        | EXIT SUCCESSFUL
        | EXIT FAILURE
        | STRING IN STDOUT
        | STRING IN STDERR
        | INTEGER
        | ID
        | STRING
        | '(' exp ')'
        | MINUS exp %prec UMINUS
        | NOT exp
        | ID '(' argument_list ')'
    """
    pass


def p_empty(_):
    """empty :"""
    pass


def p_error(t):
    raise SyntaxError(f"Syntax error at '{t.value}'")


# build the parser
parser = yacc.yacc()
