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
          | QUESTION opt_name '{' stmt_list '}'
          | TEARDOWN '{' stmt_list '}'
          | OUTPUT '{' format_list '}'

    opt_name : INTEGER | STRING | empty

    format_list : output_format ';' format_list
                | empty

    output_format : JSON opt_string
                 | MARKDOWN opt_string

    opt_string : STRING | empty

    stmt_list : stmt ';' stmt_list
              | empty

    stmt : LET ID be type '(' param_list ')'
         | String ID '=' STRING
         | Int ID '=' INTEGER
         | Float ID '=' FLOAT
         | builtin exp
         | AWARD INTEGER
         | RUN param_list
         | TOUCH STRING
         | REMOVE STRING
         | REQUIRE STRING string_list

    string_list : ',' STRING string_list
                | empty

    param_list : param ',' param_list
               | param
               | empty

    param : exp
          | param_assign

    param_assign : ID '=' exp

    builtin : ASSERT
            | PRINT

    type : String | Int | Float

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
        | EXIT exit_status
        | exp IN STDOUT
        | exp IN STDERR
        | exp NOT IN STDOUT
        | exp NOT IN STDERR
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
